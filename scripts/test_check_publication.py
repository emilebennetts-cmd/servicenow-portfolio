"""Publication gate regression tests: synthetic data only."""
import hashlib
import tempfile
import unittest
from pathlib import Path
from check_publication import check, scan_text, scan_visual_embeds

VALID_PNG = bytes.fromhex("89504e470d0a1a0a0000000d49484452000000010000000108060000001f15c4890000000b49444154789c636000020000050001a5f645400000000049454e44ae426082")

class PublicationTests(unittest.TestCase):
    def test_detects_private_key_header(self):
        self.assertIn("private key", scan_text("-----BEGIN PRIVATE KEY-----"))
    def test_detects_github_token(self):
        self.assertIn("GitHub token", scan_text("ghp_" + "A" * 36))
    def test_does_not_flag_normal_marketing_copy(self):
        self.assertEqual([], scan_text("Source-only case study. DEV not verified."))
    def test_unapproved_image_is_blocked(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "assets" / "screenshots").mkdir(parents=True, exist_ok=True)
            (root / "assets" / "screenshots" / "screen.png").write_bytes(b"fake")
            self.assertEqual(1, len(check(root, root / "missing.txt")))
    def test_allowlisted_image_is_accepted(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "assets" / "screenshots").mkdir(parents=True, exist_ok=True)
            (root / "assets" / "screenshots" / "screen.png").write_bytes(VALID_PNG)
            allowlist = root / "approved.txt"
            allowlist.write_text("assets/screenshots/screen.png " + hashlib.sha256(VALID_PNG).hexdigest() + "\n", encoding="utf-8")
            self.assertEqual([], check(root, allowlist))
    def test_changed_image_requires_fresh_approval(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "assets" / "screenshots").mkdir(parents=True, exist_ok=True)
            (root / "assets" / "screenshots" / "screen.png").write_bytes(b"original")
            allowlist = root / "approved.txt"
            allowlist.write_text("assets/screenshots/screen.png " + hashlib.sha256(b"original").hexdigest() + "\n", encoding="utf-8")
            (root / "assets" / "screenshots").mkdir(parents=True, exist_ok=True)
            (root / "assets" / "screenshots" / "screen.png").write_bytes(b"changed")
            self.assertTrue(any("changed since" in issue for issue in check(root, allowlist)))
    def test_legacy_path_only_approval_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "assets" / "screenshots").mkdir(parents=True, exist_ok=True)
            (root / "assets" / "screenshots" / "screen.png").write_bytes(b"fake")
            allowlist = root / "approved.txt"
            allowlist.write_text("assets/screenshots/screen.png\n", encoding="utf-8")
            self.assertTrue(check(root, allowlist))
    def test_approval_outside_screenshot_directory_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "screen.png").write_bytes(b"fake")
            allowlist = root / "approved.txt"
            allowlist.write_text("screen.png " + hashlib.sha256(b"fake").hexdigest() + "\n", encoding="utf-8")
            self.assertTrue(any("unsafe image path" in issue for issue in check(root, allowlist)))
    def test_detects_secret_in_html(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "index.html").write_text("-----BEGIN PRIVATE KEY-----", encoding="utf-8")
            self.assertEqual(1, len(check(root, root / "missing.txt")))

    def test_embedded_raster_data_url_in_html_is_blocked(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "index.html").write_text(
                '<img alt="example" src="data:image/png;base64,aGVsbG8=">', encoding="utf-8")
            self.assertTrue(any("embedded image data URL" in x for x in check(root, root / "missing.txt")))

    def test_remote_image_element_is_blocked(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "index.html").write_text(
                '<picture><source srcset="//example.test/preview.png"></picture>', encoding="utf-8")
            self.assertTrue(any("remote image element" in x for x in check(root, root / "missing.txt")))

    def test_svg_raster_reference_is_blocked(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "diagram.svg").write_text(
                '<svg xmlns="http://www.w3.org/2000/svg"><image href="local.png"/></svg>', encoding="utf-8")
            self.assertTrue(any("SVG image element" in x for x in check(root, root / "missing.txt")))

    def test_svg_foreign_object_is_blocked(self):
        self.assertIn("embedded foreignObject element", scan_visual_embeds(
            '<svg><foreignObject><div>unreviewed screen</div></foreignObject></svg>', ".svg"))

    def test_svg_remote_css_and_script_are_blocked(self):
        found = scan_visual_embeds(
            '<svg><script>alert(1)</script><rect fill="url(https://example.test/pixel.png)"/></svg>', ".svg")
        self.assertIn("SVG executable script", found)
        self.assertIn("SVG CSS remote image", found)

    def test_safe_vector_diagram_and_external_font_stylesheet_are_allowed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "diagram.svg").write_text(
                '<svg xmlns="http://www.w3.org/2000/svg"><rect width="10" height="10"/></svg>', encoding="utf-8")
            (root / "index.html").write_text(
                "<link rel='stylesheet' href='https://fonts.googleapis.com/css2'>", encoding="utf-8")
            self.assertEqual([], check(root, root / "missing.txt"))

    def test_remote_css_background_is_blocked_without_blocking_web_fonts(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "style.css").write_text(
                "div{background-image:url('https://example.test/secret.png')}", encoding="utf-8")
            self.assertTrue(any("remote CSS background image" in x for x in check(root, root / "missing.txt")))

    def test_inline_svg_image_and_external_use_are_blocked(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "index.html").write_text(
                "<svg><image href='local-private.png'/><use href='https://example.test/icon'/></svg>",
                encoding="utf-8")
            findings = check(root, root / "missing.txt")
            self.assertTrue(any("SVG image element" in x for x in findings))
            self.assertTrue(any("remote SVG use reference" in x for x in findings))

    def test_markdown_embedded_image_is_blocked(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "release.md").write_text(
                "![capture](data:image/png;base64,aGVsbG8=)", encoding="utf-8")
            self.assertTrue(any("embedded image data URL" in x for x in check(root, root / "missing.txt")))

if __name__ == "__main__":
    unittest.main()

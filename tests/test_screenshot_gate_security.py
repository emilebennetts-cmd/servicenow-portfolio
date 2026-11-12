"""Security regressions for the public screenshot publication gate."""
import hashlib
import tempfile
import unittest
from pathlib import Path
from scripts.check_publication import check


class ScreenshotGateSecurityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "site"
        (self.root / "evidence").mkdir(parents=True)
        (self.root / "assets" / "screenshots").mkdir(parents=True)
        self.manifest = self.root / "evidence" / "approved-public-images.txt"

    def test_approved_matching_bytes(self):
        image = self.root / "assets" / "screenshots" / "approved.png"
        image.write_bytes(b"\x89PNG\r\n\x1a\nsynthetic-no-metadata")
        digest = hashlib.sha256(image.read_bytes()).hexdigest()
        self.manifest.write_text(f"assets/screenshots/approved.png {digest}\n")
        self.assertEqual(check(self.root, self.manifest), [])

    def test_rejects_unreviewed_active_embed(self):
        page = self.root / "embedded.html"
        page.write_text('<iframe src="https://example.invalid/secret-capture"></iframe>')
        self.assertTrue(any("active HTML embed" in x for x in check(self.root, self.manifest)))

    def test_rejects_inline_svg_filter_image(self):
        page = self.root / "case.html"
        page.write_text('<svg><filter><feImage href="local.png"/></filter></svg>')
        self.assertTrue(any("SVG filter image element" in x for x in check(self.root, self.manifest)))

    def test_rejects_remote_video_poster(self):
        page = self.root / "case.html"
        page.write_text('<video poster="https://example.invalid/capture.png"></video>')
        self.assertTrue(any("remote video poster" in x for x in check(self.root, self.manifest)))

    def test_rejects_remote_css_content_image(self):
        sheet = self.root / "style.css"
        sheet.write_text('.leak::before { content: url(https://example.invalid/capture.png); }')
        self.assertTrue(any("remote CSS image property" in x for x in check(self.root, self.manifest)))

    def test_plain_text_use_of_iframe_does_not_trigger_in_markdown(self):
        page = self.root / "notes.md"
        page.write_text('Example markup: <iframe src="https://example.invalid/">')
        self.assertFalse(any("active HTML embed" in x for x in check(self.root, self.manifest)))

    def test_rejects_traversal_manifest(self):
        self.manifest.write_text("assets/screenshots/../../secret.png " + "a" * 64 + "\n")
        self.assertTrue(any("unsafe image path" in x for x in check(self.root, self.manifest)))

    def test_rejects_absolute_manifest(self):
        self.manifest.write_text("/tmp/secret.png " + "a" * 64 + "\n")
        self.assertTrue(any("unsafe image path" in x for x in check(self.root, self.manifest)))

    def test_rejects_external_symlink(self):
        outside = Path(self.temp.name) / "private.png"
        outside.write_bytes(b"private bytes")
        link = self.root / "assets" / "screenshots" / "linked.png"
        link.symlink_to(outside)
        self.assertTrue(any("symlink escapes" in x for x in check(self.root, self.manifest)))

    def test_rejects_modified_approved_image(self):
        image = self.root / "assets" / "screenshots" / "approved.png"
        image.write_bytes(b"changed")
        self.manifest.write_text("assets/screenshots/approved.png " + "0" * 64 + "\n")
        self.assertTrue(any("image bytes changed" in x for x in check(self.root, self.manifest)))


if __name__ == "__main__":
    unittest.main()

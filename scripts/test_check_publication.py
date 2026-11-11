"""Publication gate regression tests: synthetic data only."""
import hashlib
import tempfile
import unittest
from pathlib import Path
from check_publication import check, scan_text

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

if __name__ == "__main__":
    unittest.main()

"""Publication gate regression tests: synthetic data only."""
import tempfile
import unittest
from pathlib import Path
from check_publication import check, scan_text

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
            (root / "screen.png").write_bytes(b"fake")
            self.assertEqual(1, len(check(root, root / "missing.txt")))
    def test_allowlisted_image_is_accepted(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "screen.png").write_bytes(b"fake")
            allowlist = root / "approved.txt"
            allowlist.write_text("screen.png\n", encoding="utf-8")
            self.assertEqual([], check(root, allowlist))
    def test_detects_secret_in_html(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "index.html").write_text("-----BEGIN PRIVATE KEY-----", encoding="utf-8")
            self.assertEqual(1, len(check(root, root / "missing.txt")))

if __name__ == "__main__":
    unittest.main()

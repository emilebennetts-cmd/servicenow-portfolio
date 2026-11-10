"""Regression tests for the screenshot publication boundary."""
import hashlib
import tempfile
import unittest
from pathlib import Path

from check_publication import check, image_format_matches, MAX_PUBLIC_IMAGE_BYTES


class ScreenshotPublicationTests(unittest.TestCase):
    def test_image_signatures(self):
        self.assertTrue(image_format_matches(Path("screen.png"), b"\x89PNG\r\n\x1a\nmore"))
        self.assertFalse(image_format_matches(Path("screen.png"), b"<html>not an image</html>"))
        self.assertTrue(image_format_matches(Path("screen.jpg"), b"\xff\xd8\xffpayload\xff\xd9"))
        self.assertFalse(image_format_matches(Path("screen.jpg"), b"\xff\xd8\xfftruncated"))
        self.assertTrue(image_format_matches(Path("screen.webp"), b"RIFFxxxxWEBP"))
        self.assertFalse(image_format_matches(Path("screen.webp"), b"RIFFxxxxWAVE"))

    def test_approved_file_must_match_bytes_and_type(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            folder = root / "assets" / "screenshots"
            folder.mkdir(parents=True)
            file = folder / "screen.png"
            file.write_bytes(b"<script>not an image</script>")
            manifest = root / "approved.txt"
            digest = hashlib.sha256(file.read_bytes()).hexdigest()
            manifest.write_text(f"assets/screenshots/screen.png {digest}\n")
            self.assertTrue(any("signature" in issue for issue in check(root, manifest)))
            file.write_bytes(b"\x89PNG\r\n\x1a\nfixture")
            manifest.write_text(f"assets/screenshots/screen.png {hashlib.sha256(file.read_bytes()).hexdigest()}\n")
            self.assertEqual(check(root, manifest), [])

    def test_large_image_rejected_even_if_approved(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            folder = root / "assets" / "screenshots"
            folder.mkdir(parents=True)
            file = folder / "screen.png"
            file.write_bytes(b"\x89PNG\r\n\x1a\n" + b"0" * MAX_PUBLIC_IMAGE_BYTES)
            manifest = root / "approved.txt"
            manifest.write_text(f"assets/screenshots/screen.png {hashlib.sha256(file.read_bytes()).hexdigest()}\n")
            self.assertTrue(any("size limit" in issue for issue in check(root, manifest)))


if __name__ == "__main__":
    unittest.main()

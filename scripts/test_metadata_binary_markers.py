"""Regression coverage for byte-level metadata detection in the public image gate.

The CI workflow discovers scripts/test_*.py. Fixtures are synthetic and never
represent real ServiceNow evidence or publication approval.
"""
import hashlib
import tempfile
import unittest
from pathlib import Path

from check_publication import check, embedded_metadata_markers


class ImageMetadataRegressionTests(unittest.TestCase):
    def test_jpeg_exif_uses_actual_nul_bytes(self):
        jpeg = b"\xff\xd8\xff\xe1\x00\x0eExif\x00\x00payload\xff\xd9"
        self.assertIn("EXIF", embedded_metadata_markers(Path("synthetic.jpg"), jpeg))

    def test_literal_escape_characters_are_not_exif(self):
        literal = b"\xff\xd8\xff" + b"Exif\\x00\\x00" + b"\xff\xd9"
        self.assertNotIn("EXIF", embedded_metadata_markers(Path("synthetic.jpg"), literal))

    def test_gif_binary_comment_extension(self):
        gif = b"GIF89a" + bytes((0x21, 0xFE, 0x05)) + b"hello"
        self.assertIn("GIF comment", embedded_metadata_markers(Path("synthetic.gif"), gif))

    def test_png_text_chunk_marker(self):
        png = b"\x89PNG\r\n\x1a\n" + b"tEXt" + b"Creator name"
        self.assertIn("tEXt", embedded_metadata_markers(Path("synthetic.png"), png))

    def test_clean_jpeg_has_no_detected_metadata(self):
        jpeg = b"\xff\xd8\xffplain-synthetic-data\xff\xd9"
        self.assertEqual([], embedded_metadata_markers(Path("synthetic.jpeg"), jpeg))

    def test_hash_approved_jpeg_still_blocks_exif(self):
        self.assert_metadata_causes_publication_failure(
            "capture.jpg", b"\xff\xd8\xffExif\x00\x00test\xff\xd9", "EXIF"
        )

    def test_hash_approved_gif_still_blocks_comment(self):
        self.assert_metadata_causes_publication_failure(
            "capture.gif", b"GIF89a" + bytes((0x21, 0xFE, 0x01, 65)), "GIF comment"
        )

    def assert_metadata_causes_publication_failure(self, filename, payload, label):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            target = root / "assets" / "screenshots" / filename
            target.parent.mkdir(parents=True)
            target.write_bytes(payload)
            manifest = root / "allowlist.txt"
            manifest.write_text(
                f"assets/screenshots/{filename} {hashlib.sha256(payload).hexdigest()}\n",
                encoding="utf-8",
            )
            problems = check(root, manifest)
            self.assertTrue(
                any(f"embedded {label} metadata" in problem for problem in problems),
                problems,
            )


if __name__ == "__main__":
    unittest.main()

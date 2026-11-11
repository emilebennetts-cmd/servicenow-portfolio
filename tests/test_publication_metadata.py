"""Regression tests for conservative screenshot metadata detection."""
import importlib.util
from pathlib import Path
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check_publication.py"
spec = importlib.util.spec_from_file_location("publication_gate", SCRIPT)
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)


class MetadataGateTests(unittest.TestCase):
    def test_png_text_chunk(self):
        self.assertIn("tEXt", gate.embedded_metadata_markers(Path("a.png"), b"\x89PNG\r\n\x1a\n...tEXt..."))

    def test_jpeg_exif(self):
        self.assertIn("EXIF", gate.embedded_metadata_markers(Path("a.jpg"), b"\xff\xd8\xffExif\x00\x00...\xff\xd9"))

    def test_webp_xmp(self):
        self.assertIn("XMP", gate.embedded_metadata_markers(Path("a.webp"), b"RIFFxxxxWEBPXMP "))

    def test_gif_comment(self):
        self.assertIn("GIF comment", gate.embedded_metadata_markers(Path("a.gif"), b"GIF89a\x21\xfe"))

    def test_plain_png_has_no_known_markers(self):
        self.assertEqual([], gate.embedded_metadata_markers(Path("a.png"), b"\x89PNG\r\n\x1a\nIHDR"))

if __name__ == "__main__":
    unittest.main()

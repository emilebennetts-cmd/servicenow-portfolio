"""CI-discovered safety contract for the public visual-evidence intake.

Run by Portfolio quality gate: python -m unittest discover -s scripts.
The four inspected files are private; this HTML must contain summary metadata only.
"""
from html.parser import HTMLParser
from pathlib import Path
import re
import unittest


GALLERY = Path(__file__).resolve().parents[1] / "visual-evidence.html"


class Tags(HTMLParser):
    def __init__(self):
        super().__init__()
        self.images = []
        self.anchors = []
        self.candidates = []
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get("id"):
            self.ids.add(a["id"])
        if tag == "img":
            self.images.append(a)
        if tag == "a":
            self.anchors.append(a.get("href", ""))
        if tag == "article" and a.get("data-evidence-id"):
            self.candidates.append(a["data-evidence-id"])


class VisualIntakeSafetyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = GALLERY.read_text(encoding="utf-8")
        cls.tags = Tags()
        cls.tags.feed(cls.html)

    def test_intake_summary_is_explicitly_not_a_gallery_approval(self):
        self.assertIn("triage-title", self.tags.ids)
        self.assertIn("independent intake sample", self.html)
        self.assertIn("0</strong><span>Images approved", self.html)
        self.assertIn("All four files remain on HOLD", self.html)

    def test_source_document_and_synthetic_example_not_runtime_proof(self):
        self.assertIn("Overview document page, not a product screenshot", self.html)
        self.assertIn("MOCK-ONLY content", self.html)
        self.assertIn("installed release and execution unverified", self.html)

    def test_no_original_images_or_private_drive_links(self):
        self.assertEqual([], self.tags.images)
        self.assertFalse(any("drive.google.com" in a or "docs.google.com" in a
                             for a in self.tags.anchors))
        self.assertNotIn("servicenow-portfolio-control", self.html)

    def test_existing_candidate_register_remains_intact(self):
        self.assertEqual(10, len(self.tags.candidates))
        self.assertEqual(10, len(set(self.tags.candidates)))
        self.assertTrue(all(re.fullmatch(r"(DW|VD)-IMG-\\d{2}", i)
                            for i in self.tags.candidates))


if __name__ == "__main__":
    unittest.main()

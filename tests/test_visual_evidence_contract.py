#!/usr/bin/env python3
"""Offline safety and structural smoke checks for the public evidence gallery.

Run: python3 tests/test_visual_evidence_contract.py
No credentials, network, third-party packages or private image assets required.
"""
from html.parser import HTMLParser
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "visual-evidence.html"


class GalleryParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.duplicate_ids = set()
        self.candidates = []
        self.images = []
        self.links = []
        self.buttons = []
        self.details = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            if a["id"] in self.ids:
                self.duplicate_ids.add(a["id"])
            self.ids.add(a["id"])
        if tag == "article" and "data-evidence-id" in a:
            self.candidates.append((a["data-evidence-id"], a.get("data-group")))
        if tag == "img":
            self.images.append(a)
        if tag == "a":
            self.links.append(a.get("href", ""))
        if tag == "button":
            self.buttons.append(a)
        if tag == "details":
            self.details += 1


class EvidenceGalleryContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PAGE.read_text(encoding="utf-8")
        cls.page = GalleryParser()
        cls.page.feed(cls.html)

    def test_unique_dom_ids(self):
        self.assertFalse(self.page.duplicate_ids, "Duplicate DOM IDs: " + str(self.page.duplicate_ids))

    def test_local_fragment_links_resolve(self):
        broken = [href for href in self.page.links if href.startswith("#") and href != "#" and href[1:] not in self.page.ids]
        self.assertFalse(broken, "Broken in-page links: " + str(broken))

    def test_unique_candidate_identifiers(self):
        ids = [x[0] for x in self.page.candidates]
        self.assertEqual(len(ids), len(set(ids)), "Duplicate evidence ID")
        self.assertEqual(len(ids), 10, "Update inventory contract when candidate count changes")
        self.assertTrue(all(re.fullmatch(r"(DW|VD)-IMG-\d{2}", x) for x in ids))

    def test_group_and_review_details(self):
        self.assertEqual(sum(group == "diagnostic" for _, group in self.page.candidates), 6)
        self.assertEqual(sum(group == "delivery" for _, group in self.page.candidates), 4)
        self.assertGreaterEqual(self.page.details, len(self.page.candidates))

    def test_interactive_controls_exist(self):
        required = {"candidate-search", "reset-candidates", "candidate-count",
                    "export-candidates", "print-review", "candidate-empty", "gallery"}
        self.assertFalse(required - self.page.ids, "Missing controls: " + str(required - self.page.ids))
        self.assertIn('aria-live="polite"', self.html)

    def test_no_unreviewed_images_or_private_links(self):
        self.assertEqual(self.page.images, [], "Images require separate approval and review")
        self.assertFalse(any("drive.google.com" in url or "docs.google.com" in url
                             for url in self.page.links), "Private Drive links must not be public")
        self.assertNotIn("servicenow-portfolio-control", self.html)

    def test_review_boundary_is_visible(self):
        self.assertIn("HOLD", self.html)
        self.assertIn("Candidate only", self.html)
        self.assertIn("not a published screenshot gallery", self.html)

    def test_mobile_and_print_support(self):
        self.assertIn('name="viewport"', self.html)
        self.assertIn("@media print", self.html)
        self.assertIn("@media(max-width:650px)", self.html)


if __name__ == "__main__":
    unittest.main()

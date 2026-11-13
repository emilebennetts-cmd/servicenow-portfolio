#!/usr/bin/env python3
"""Contract checks for dated, public-safe Workbench source and DEV lineage."""
from html.parser import HTMLParser
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "technical-evidence-register.html"

class LineageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.cards = []
        self.filters = []
        self.ids = []
        self.links = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.append(a["id"])
        if tag == "article" and "lineage-card" in a.get("class", "").split():
            self.cards.append(a)
        if tag == "button" and "data-lineage-filter" in a:
            self.filters.append(a)
        if tag == "a" and a.get("href"):
            self.links.append(a["href"])

class SourceLineageTests(unittest.TestCase):
    def setUp(self):
        self.html = PAGE.read_text(encoding="utf-8")
        self.parser = LineageParser()
        self.parser.feed(self.html)

    def test_six_separate_lineage_records(self):
        cards = self.parser.cards
        self.assertEqual(len(cards), 6)
        self.assertEqual(len({c["data-evidence-id"] for c in cards}), 6)
        self.assertEqual(sum(c["data-class"] == "SOURCE-ONLY" for c in cards), 3)
        self.assertEqual(sum(c["data-class"] == "DEV-REPORTED" for c in cards), 3)
        self.assertEqual(self.html.count("data-evidence-id="), 6)

    def test_baseline_and_current_source_not_promoted(self):
        required = ("4.5.1", "4.6.1", "4.20.0", "4.22.2",
                    "30 September 2026", "5 October 2026",
                    "zero newly DEV-VERIFIED", "zero PRODUCTION-VERIFIED",
                    "mock-only", "image-specific owner approval")
        for term in required:
            with self.subTest(term=term):
                self.assertIn(term.lower(), self.html.lower())
        self.assertNotIn("4.22.2 was deployed and verified", self.html.lower())

    def test_accessibility_and_safe_links(self):
        self.assertEqual(len(self.parser.ids), len(set(self.parser.ids)))
        self.assertEqual(
            {c["data-lineage-filter"] for c in self.parser.filters},
            {"all", "SOURCE-ONLY", "DEV-REPORTED"},
        )
        self.assertIn('id="lineage-count"', self.html)
        self.assertIn('aria-live="polite"', self.html)
        self.assertIn('role="group"', self.html)
        self.assertIn("record.hidden=mode", self.html)
        for link in self.parser.links:
            self.assertFalse(link.startswith(("http://", "https://drive.google.com",
                                               "../", "javascript:")), link)
        for target in ("workbench-architecture-gallery.html",
                       "delivery-release-evolution.html",
                       "knowledge-intelligence-acceptance-matrix.html"):
            self.assertTrue(any(link.split("#", 1)[0] == target for link in self.parser.links), target)
            self.assertTrue((ROOT / target).exists(), target)

if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3
"""Offline structure, confidentiality and arithmetic contract for published pattern audit."""
from html.parser import HTMLParser
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "pattern-library-audit-trail.html"

class Scan(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.duplicates = set()
        self.cards = []
        self.filters = []
        self.links = []
        self.images = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        identifier = a.get("id")
        if identifier:
            if identifier in self.ids:
                self.duplicates.add(identifier)
            self.ids.add(identifier)
        if tag == "article" and "data-audit" in a:
            self.cards.append((a["data-audit"], a.get("data-category")))
        if tag == "button" and "data-filter" in a:
            self.filters.append((a["data-filter"], a.get("aria-pressed")))
        if tag == "a":
            self.links.append(a.get("href", ""))
        if tag == "img":
            self.images.append(a)

class PatternAuditContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PAGE.read_text(encoding="utf-8")
        cls.scan = Scan()
        cls.scan.feed(cls.html)

    def test_eight_unique_review_records_and_accessibility(self):
        self.assertEqual(len(self.scan.cards), 8)
        self.assertEqual({key for key, _ in self.scan.cards},
                         {"AUD-%02d" % n for n in range(1, 9)})
        self.assertEqual({cat for _, cat in self.scan.cards},
                         {"authoring", "quality", "readiness"})
        self.assertEqual({v for v, _ in self.scan.filters},
                         {"all", "authoring", "quality", "readiness"})
        self.assertEqual(sum(v == "true" for _, v in self.scan.filters), 1)
        self.assertFalse(self.scan.duplicates)
        self.assertTrue({"main", "audit-search", "result-count", "audit-cards",
                         "export-csv", "clear"} <= self.scan.ids)
        self.assertIn('role="status" aria-live="polite"', self.html)
        self.assertIn("@media(max-width:650px)", self.html)
        self.assertIn('name="viewport"', self.html)

    def test_no_false_count_addition_or_runtime_claim(self):
        for marker in ("585", "13", "572", "96", "668", "28", "2,234",
                       "11,000", "23/23", "3,450", "670", "3,352", "2,897",
                       "179", "276", "SOURCE-ONLY", "DEV-REPORTED",
                       "DEV-VERIFIED", "PRODUCTION-VERIFIED", "MOCK-ONLY",
                       "HOLD", "NOT additive", "no ServiceNow licence"):
            self.assertIn(marker, self.html)
        self.assertEqual(585 - 13, 572)
        self.assertEqual(572 + 96, 668)
        self.assertEqual(2897 + 179 + 276, 3352)
        self.assertIn("target read-back", self.html)
        self.assertIn("candidate maturity", self.html)
        self.assertIn("no genuine screenshot pixels", self.html.lower())

    def test_fail_closed_csv_and_private_source_exclusion(self):
        for item in ("'SOURCE-ONLY','HOLD'", "source-audit-HOLD.csv",
                     "cards.filter(c=>!c.hidden)", "c.dataset.category",
                     "URL.createObjectURL(blob)", "a.remove();URL.revokeObjectURL(url)",
                     "document.getElementById('clear')", "card.hidden=!matches"):
            self.assertIn(item, self.html)
        self.assertFalse(self.scan.images)
        for key in ("connect-src 'none'", "img-src 'none'",
                    "object-src 'none'", "form-action 'none'"):
            self.assertIn(key, self.html)
        self.assertNotRegex(self.html, r"\b(?:fetch|XMLHttpRequest|localStorage|sendBeacon)\s*\(")
        self.assertNotIn("drive.google.com", self.html)
        self.assertNotIn("servicenow-portfolio-control", self.html)
        self.assertNotIn("dev438211", self.html)
        self.assertNotIn("x_1577958", self.html)
        self.assertNotIn("api.github.com/repos", self.html)

    def test_links_exist(self):
        self.assertIn("pattern-library-audit-trail.html",
                      (ROOT / "sitemap.xml").read_text(encoding="utf-8"))
        self.assertIn("pattern-library-audit-trail.html",
                      (ROOT / "index.html").read_text(encoding="utf-8"))
        for link in self.scan.links:
            if link.startswith(("#", "https:", "mailto:")):
                continue
            path = link.split("#", 1)[0]
            if path:
                self.assertTrue((ROOT / path).exists(), link)

if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3
"""Public source-only operations runbook contract: no private data or runtime claims."""
from html.parser import HTMLParser
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "operational-readiness-runbook.html"


class Scan(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.dupes = set()
        self.cards = []
        self.filters = []
        self.links = []
        self.images = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        ident = attrs.get("id")
        if ident:
            if ident in self.ids:
                self.dupes.add(ident)
            self.ids.add(ident)
        if tag == "article" and "data-code" in attrs:
            self.cards.append((attrs["data-code"], attrs.get("data-cadence")))
        if tag == "button" and "data-cadence" in attrs:
            self.filters.append((attrs["data-cadence"], attrs.get("aria-pressed")))
        if tag == "a":
            self.links.append(attrs.get("href", ""))
        if tag == "img":
            self.images += 1


class OperationsContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PAGE.read_text(encoding="utf-8")
        cls.scan = Scan()
        cls.scan.feed(cls.html)

    def test_twelve_source_backed_controls(self):
        self.assertFalse(self.scan.dupes)
        self.assertEqual(
            {k for k, _ in self.scan.cards},
            {"OPS-%02d" % i for i in range(1, 13)}
        )
        self.assertEqual(
            {v: sum(c == v for _, c in self.scan.cards)
             for v in ("daily", "weekly", "release", "quarterly")},
            {"daily": 3, "weekly": 2, "release": 3, "quarterly": 4}
        )
        self.assertEqual(
            {x for x, _ in self.scan.filters},
            {"all", "daily", "weekly", "release", "quarterly"}
        )
        self.assertEqual(sum(x == "true" for _, x in self.scan.filters), 1)
        self.assertTrue(
            {"main", "q", "count", "runbooks", "reset", "print",
             "failure-select", "failure-output"} <= self.scan.ids
        )
        self.assertIn('role="status" aria-live="polite"', self.html)
        self.assertIn('@media(max-width:760px)', self.html)
        self.assertIn('@media print', self.html)

    def test_evidence_boundaries_and_entitlement(self):
        for phrase in ("SOURCE-ONLY", "MOCK-ONLY", "DEV-REPORTED",
                       "DEV-VERIFIED", "PRODUCTION-VERIFIED",
                       "4.6.1", "4.5.1", "30 September 2026",
                       "no ServiceNow licence", "NOT ESTABLISHED",
                       "not independently repeated"):
            self.assertIn(phrase.lower(), self.html.lower())
        self.assertIn("no current native DEV/production execution", self.html)
        self.assertNotIn("DEV-VERIFIED: passed", self.html)

    def test_publication_safety_and_local_only(self):
        self.assertEqual(self.scan.images, 0)
        for token in ("connect-src 'none'", "img-src 'none'",
                      "object-src 'none'", "form-action 'none'"):
            self.assertIn(token, self.html)
        self.assertNotRegex(self.html, r"\b(?:fetch|XMLHttpRequest|localStorage|sendBeacon)\s*\(")
        for forbidden in ("drive.google.com", "servicenow-portfolio-control",
                          "dev438211", "x_1577958", "api.github.com/repos",
                          "Bearer ", "password="):
            self.assertNotIn(forbidden, self.html)

    def test_site_link_integrity(self):
        for page in ("index.html", "portfolio-review-guide.html", "sitemap.xml"):
            self.assertIn(PAGE.name, (ROOT / page).read_text(encoding="utf-8"))
        for link in self.scan.links:
            if link.startswith(("#", "https:", "mailto:")):
                continue
            target = link.split("#", 1)[0]
            if target:
                self.assertTrue((ROOT / target).exists(), link)


if __name__ == "__main__":
    unittest.main()

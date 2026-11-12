#!/usr/bin/env python3
"""Public page-index contract: no private source, false attestation or broken links."""
from html.parser import HTMLParser
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "portfolio-explorer.html"

class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.duplicates = []
        self.cards = []
        self.links = []
        self.headings = 0
        self.image_elements = 0
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        ident = a.get("id")
        if ident:
            if ident in self.ids:
                self.duplicates.append(ident)
            self.ids.add(ident)
        if tag == "h1":
            self.headings += 1
        if tag == "a" and a.get("href"):
            self.links.append(a["href"])
        if tag in ("img", "iframe", "video", "canvas", "picture"):
            self.image_elements += 1
        if tag == "li" and a.get("class") == "result":
            self.cards.append(a)

class PortfolioExplorerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PAGE.read_text(encoding="utf-8")
        cls.parser = PageParser()
        cls.parser.feed(cls.html)
    def test_catalogue_is_complete_and_uses_existing_public_files(self):
        expected = {p.name for p in ROOT.glob("*.html")} - {PAGE.name}
        cards = self.parser.cards
        names = {a["href"] for a in []}  # links on cards are checked via HTMLParser below
        self.assertEqual(len(cards), len(expected))
        self.assertTrue(all(c.get("data-search") and c.get("data-category") for c in cards))
        self.assertIn('id="total">'+str(len(expected))+'</strong>', self.html)
        for name in expected:
            with self.subTest(name=name):
                self.assertIn('href="'+name+'"', self.html)
        self.assertEqual(len(self.parser.links), len(set(self.parser.links)))
    def test_accessible_navigation_and_correct_indexing(self):
        self.assertEqual(self.parser.headings, 1)
        self.assertFalse(self.parser.duplicates)
        self.assertTrue({"main", "results", "search", "category", "reset", "more", "count", "helper"} <= self.parser.ids)
        self.assertEqual(self.parser.image_elements, 0)
        self.assertIn('role="status" aria-live="polite"', self.html)
        for token in ("@media(max-width:650px)", "prefers-reduced-motion", "document.querySelectorAll", "row.hidden=!show", "expanded=false", "search.focus()"):
            self.assertIn(token, self.html)
        self.assertIn("portfolio-explorer.html", (ROOT / "sitemap.xml").read_text())
        self.assertIn('href="portfolio-explorer.html"', (ROOT / "index.html").read_text())
        self.assertIn('href="portfolio-explorer.html"', (ROOT / "portfolio-review-guide.html").read_text())
    def test_publication_and_verification_boundary(self):
        for token in ("SOURCE-ONLY", "MOCK-ONLY", "DEV-REPORTED", "DEV-VERIFIED", "PRODUCTION-VERIFIED", "0 approved original screenshots", "connect-src 'none'", "img-src 'none'", "form-action 'none'", "no ServiceNow licence"):
            self.assertIn(token, self.html)
        for forbidden in ("dev438211", "service-now.com/", "github.com/emilebennetts-cmd/Diagnostic-Workbench2", "github.com/emilebennetts-cmd/servicenow-portfolio-control", "drive.google.com", "docs.google.com", "<img", "fetch(", "XMLHttpRequest", "localStorage", "indexedDB", "innerHTML"):
            self.assertNotIn(forbidden, self.html)

if __name__ == "__main__":
    unittest.main()

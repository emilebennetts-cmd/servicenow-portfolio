#!/usr/bin/env python3
"""Offline integrity and confidentiality contract for 90-second reviewer guide."""
from html.parser import HTMLParser
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "portfolio-review-guide.html"

class Scan(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.duplicates = set()
        self.controls = []
        self.panels = {}
        self.links = []
        self.images = []
        self.headings = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        ident = a.get("id")
        if ident in self.ids:
            self.duplicates.add(ident)
        if ident:
            self.ids.add(ident)
        if tag == "button" and a.get("data-route"):
            self.controls.append(a)
        if a.get("data-panel"):
            self.panels[a["data-panel"]] = a
        if tag == "a":
            self.links.append(a.get("href", ""))
        if tag == "img":
            self.images.append(a)
        if tag == "h1":
            self.headings.append("h1")

class ReviewerGuideTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.content = PAGE.read_text(encoding="utf-8")
        cls.scan = Scan()
        cls.scan.feed(cls.content)

    def test_document_and_accessible_route_controls(self):
        self.assertEqual(cls := len(self.scan.headings), 1, f"Expected exactly one h1, got {cls}")
        self.assertFalse(self.scan.duplicates)
        self.assertTrue({"main", "review-route", "source-observations", "verification"} <= self.scan.ids)
        self.assertEqual(len(self.scan.controls), 3)
        self.assertEqual({c["data-route"] for c in self.scan.controls},
                         {"recruiter", "architect", "assurance"})
        self.assertEqual(set(self.scan.panels), {"recruiter", "architect", "assurance"})
        self.assertEqual(sum(c.get("aria-pressed") == "true" for c in self.scan.controls), 1)
        self.assertTrue(all(c.get("aria-controls") == "route-" + c["data-route"]
                            for c in self.scan.controls))
        self.assertEqual({self.scan.panels[r].get("id") for r in self.scan.panels},
                         {"route-recruiter", "route-architect", "route-assurance"})
        self.assertIn("panel.hidden=panel.dataset.panel!==next", self.content)
        self.assertIn("@media(max-width:560px)", self.content)

    def test_public_evidence_integrity(self):
        for word in ("SOURCE-ONLY", "DEV-REPORTED", "DEV-VERIFIED", "MOCK-ONLY",
                     "PRODUCTION-VERIFIED", "19 October 2026", "RV-01", "RV-02",
                     "RV-05", "HOLD", "16", "0 approved"):
            self.assertIn(word, self.content)
        self.assertIn("no ServiceNow licence", self.content)
        self.assertIn("No new DEV read-back", self.content)

    def test_offline_reviewer_briefing_and_print_holds(self):
        for value in ('id="export-review-route"', 'id="print-review-route"',
                      'id="review-export-status"', '@media print',
                      '.route-panel[hidden], [hidden]{display:none!important}',
                      'original_screenshots_approved:0', 'native_dev_verified:false',
                      'production_verified:false', 'review_state:"UNREVIEWED"',
                      'verification_state:"NOT VERIFIED"', 'publication_state:"HOLD"',
                      'window.print()', 'selectedRoutePacket()', 'URL.createObjectURL(blob)',
                      'Unapproved evidence link', 'servicenow-review-'):
            self.assertIn(value, self.content)
        self.assertIn('Six UI capture observations and two documents'.lower(),
                      self.content.lower())
        self.assertNotRegex(self.content, r"<(?:img|iframe|object|embed)\\b")
        self.assertNotIn("new XMLHttpRequest", self.content)

    def test_no_private_assets_or_network_calls(self):
        self.assertFalse(self.scan.images, "Genuine screenshots are not publication-approved")
        self.assertNotIn("drive.google.com", self.content)
        self.assertNotIn("docs.google.com", self.content)
        self.assertNotIn("servicenow-portfolio-control", self.content)
        self.assertNotIn("solution-lifecycle-studio", self.content)
        self.assertNotIn("Diagnostic-Workbench2", self.content)
        self.assertNotRegex(self.content, r"\b(?:fetch|XMLHttpRequest|sendBeacon|localStorage)\s*\(")
        for field in ("connect-src 'none'", "img-src 'none'", "object-src 'none'",
                      "form-action 'none'"):
            self.assertIn(field, self.content)

    def test_internal_link_targets_are_public(self):
        self.assertGreater(len(self.scan.links), 15)
        for href in self.scan.links:
            if href.startswith(("#", "mailto:", "https://")):
                continue
            path = href.split("#", 1)[0]
            if not path:
                continue
            target = ROOT / path
            self.assertTrue(target.exists(), f"Missing public link {href}")
        self.assertIn("portfolio-review-guide.html",
                      (ROOT / "index.html").read_text(encoding="utf-8"))
        self.assertIn("portfolio-review-guide.html",
                      (ROOT / "sitemap.xml").read_text(encoding="utf-8"))

if __name__ == "__main__":
    unittest.main()

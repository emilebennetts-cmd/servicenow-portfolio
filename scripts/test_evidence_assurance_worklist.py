#!/usr/bin/env python3
"""SOURCE-ONLY public assurance worklist contract; no native verification implied."""
import json
import unittest
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "evidence-assurance-worklist.html"
REGISTER = ROOT / "evidence/public-verification-register.json"

class Structure(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.links = [], []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get("id"):
            self.ids.append(a["id"])
        if tag == "a" and a.get("href"):
            self.links.append(a["href"])

class WorklistContract(unittest.TestCase):
    def setUp(self):
        self.html = PAGE.read_text(encoding="utf-8")
        self.data = json.loads(REGISTER.read_text(encoding="utf-8"))

    def test_public_authority_and_conservative_status(self):
        source = self.html
        self.assertIn("fetch('evidence/public-verification-register.json',{cache:'no-store'})", source)
        self.assertIn("schema_version!=='1.0'", source)
        self.assertIn("used.has(entry.id)", source)
        self.assertIn("!allowed.has(entry.classification)", source)
        self.assertIn("results.replaceChildren()", source)
        self.assertIn("el.textContent=value", source)
        self.assertNotIn("innerHTML", source)
        self.assertIn("source:'evidence/public-verification-register.json'", source)
        self.assertIn("review_state:'UNREVIEWED'", source)
        self.assertIn("verification_state:'NOT VERIFIED'", source)
        self.assertIn("release_state:'HOLD'", source)
        self.assertIn("independent_native_verification:false", source)
        self.assertIn("production_acceptance:false", source)
        self.assertIn("screenshot_publication_approved:false", source)
        self.assertNotIn("localStorage", source)
        self.assertNotIn("sessionStorage", source)

    def test_responsive_accessibility_and_navigation(self):
        parser = Structure()
        parser.feed(self.html)
        self.assertEqual(len(parser.ids), len(set(parser.ids)))
        for required in ("main", "search", "classification", "action-filter", "results",
                         "download", "load-more", "failure", "status"):
            self.assertIn(required, parser.ids)
        self.assertIn('aria-live="polite"', self.html)
        self.assertIn('@media(max-width:760px)', self.html)
        self.assertIn('meta http-equiv="Content-Security-Policy"', self.html)
        self.assertIn("connect-src 'self'", self.html)
        for link in ("portfolio-explorer.html", "technical-evidence-register.html#claim-catalogue",
                     "workbench-acceptance-playbook.html"):
            self.assertIn(link, parser.links)

    def test_counts_and_catalogue_provenance(self):
        self.assertEqual(len(self.data["items"]), 87)
        counts = {kind: sum(c["classification"] == kind for c in self.data["items"])
                  for kind in self.data["classification_definitions"]}
        self.assertEqual(counts["source-only"], 54)
        self.assertEqual(counts["DEV-reported"], 4)
        self.assertEqual(counts["mock-only"], 20)
        self.assertEqual(counts["proposed"], 9)
        self.assertEqual(counts["DEV-verified"], 0)
        self.assertEqual(counts["production-verified"], 0)
        record = [x for x in self.data["items"]
                  if x["id"] == "PUBLIC-EVIDENCE-ASSURANCE-WORKLIST-20261114"]
        self.assertEqual(len(record), 1)
        self.assertEqual(record[0]["classification"], "source-only")
        self.assertEqual(record[0]["page"], PAGE.name)
        self.assertIn("evidence-assurance-worklist.html", (ROOT / "index.html").read_text(encoding="utf-8"))
        self.assertIn("evidence-assurance-worklist.html", (ROOT / "portfolio-explorer.html").read_text(encoding="utf-8"))
        self.assertIn("evidence-assurance-worklist.html", (ROOT / "sitemap.xml").read_text(encoding="utf-8"))

if __name__ == "__main__":
    unittest.main()

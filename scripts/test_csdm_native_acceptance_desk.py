#!/usr/bin/env python3
"""CSDM acceptance desk contract: accessible, offline and never a native approval."""
from html.parser import HTMLParser
from pathlib import Path
import json
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]

class Elements(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.gates = []
        self.links = []
        self.selects = []
        self.scripts = []
        self.images = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get("id"):
            self.ids.append(a["id"])
        if tag == "article" and a.get("data-gate"):
            self.gates.append(a["data-gate"])
        if tag == "a" and a.get("href"):
            self.links.append(a["href"])
        if tag == "select" and a.get("id"):
            self.selects.append(a["id"])
        if tag == "script":
            self.scripts.append(a.get("src"))
        if tag in ("img", "iframe", "picture", "object", "embed", "video"):
            self.images += 1

class Contract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = (ROOT / "csdm-native-acceptance.html").read_text(encoding="utf-8")
        cls.js = (ROOT / "csdm-native-acceptance.js").read_text(encoding="utf-8")
        cls.dom = Elements()
        cls.dom.feed(cls.html)

    def test_complete_accessible_offline_page(self):
        self.assertEqual(self.dom.images, 0)
        self.assertEqual(len(self.dom.ids), len(set(self.dom.ids)))
        self.assertEqual(self.dom.scripts, ["csdm-native-acceptance.js"])
        self.assertEqual(self.dom.gates, ["target", "ire", "owner", "relation", "health", "release"])
        self.assertEqual(len(self.dom.selects), 7)
        self.assertIn('role="status" aria-live="polite"', self.html)
        self.assertIn('href="cmdb-ire-assurance.html#csdm-ownership"', self.html)
        self.assertIn("@media(max-width:560px)", self.html)
        self.assertIn("prefers-reduced-motion", self.html)
        for directive in ("connect-src 'none'", "img-src 'none'", "form-action 'none'", "script-src 'self'"):
            self.assertIn(directive, self.html)
        for text in ("MOCK-ONLY", "DEV / PRODUCTION NOT VERIFIED", "SCREENSHOTS: HOLD", "no ServiceNow licence"):
            self.assertIn(text, self.html)

    def test_export_is_non_certifying(self):
        for token in ('evidence_classification:"MOCK-ONLY"', 'native_execution_status:"NOT RUN"',
                      'native_verification_status:"NOT VERIFIED"', 'independent_review_approved:false',
                      'production_verified:false', 'publication_status:"HOLD"',
                      'approval_status:"UNREVIEWED"', 'scenario.value'):
            self.assertIn(token, self.js)
        for token in ('Object.freeze(["target","ire","owner","relation","health","release"])',
                      'Object.freeze(["not-assessed","requested","gap","staged"])',
                      'ownership:', 'identity:', 'offering:',
                      'URL.createObjectURL', 'URL.revokeObjectURL'):
            self.assertIn(token, self.js)
        for forbidden in ("fetch(", "XMLHttpRequest", "sendBeacon", "localStorage", "sessionStorage",
                          "indexedDB", "innerHTML", "eval(", "new Function(", "WebSocket",
                          "drive.google.com", "dev438211", "service-now.com/"):
            self.assertNotIn(forbidden, self.html + self.js)
        self.assertNotIn("approved:true", self.js)
        self.assertNotIn("verified:true", self.js)

    def test_sitemap_explorer_claims(self):
        home = (ROOT / "index.html").read_text(encoding="utf-8")
        explorer = (ROOT / "portfolio-explorer.html").read_text(encoding="utf-8")
        cmdb = (ROOT / "cmdb-ire-assurance.html").read_text(encoding="utf-8")
        sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
        claims = json.loads((ROOT / "evidence/public-verification-register.json").read_text(encoding="utf-8"))["items"]
        self.assertIn('href="csdm-native-acceptance.html"', home)
        self.assertIn('href="csdm-native-acceptance.html"', cmdb)
        self.assertIn('data-evidence="mock-only"', explorer)
        self.assertIn('href="csdm-native-acceptance.html"', explorer)
        self.assertIn('csdm-native-acceptance.html</loc>', sitemap)
        matched = [x for x in claims if x["page"] == "csdm-native-acceptance.html"]
        self.assertEqual(len(matched), 1)
        self.assertEqual(matched[0]["classification"], "mock-only")
        self.assertIn("NO NATIVE CMDB QUERY", matched[0]["runtime_verification"].upper())

if __name__ == "__main__":
    unittest.main()

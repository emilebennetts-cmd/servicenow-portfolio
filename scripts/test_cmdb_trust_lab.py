#!/usr/bin/env python3
"""Public CMDB Trust Lab contract: source-only page, no live data or media.

These checks validate public HTML structure and publication boundaries. Browser
execution is covered separately by browser_navigation_smoke.py.
"""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
import unittest

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "cmdb-diagnostic-trust-lab.html"
BANNED = (
    "github.com/emilebennetts-cmd/Diagnostic-Workbench2",
    "github.com/emilebennetts-cmd/solution-lifecycle-studio",
    "github.com/emilebennetts-cmd/servicenow-portfolio-control",
    "fetch(", "XMLHttpRequest", "localStorage", "sessionStorage",
    "https://dev", "mailto:", "getDisplayValue(",
)

class Structure(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.ids = []
        self.main = 0
        self.headings = 0
        self.media = []
        self.buttons = []

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if "id" in d:
            self.ids.append(d["id"])
        if tag == "main":
            self.main += 1
        if tag == "h1":
            self.headings += 1
        if tag == "a":
            self.links.append(d.get("href", ""))
        if tag in ("img", "picture", "iframe", "video", "source", "canvas"):
            self.media.append(tag)
        if tag == "button" and "data-scenario" in d:
            self.buttons.append(d)

class CMDBTrustLabContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.content = TARGET.read_text(encoding="utf-8")
        cls.parsed = Structure()
        cls.parsed.feed(cls.content)

    def test_semantics_and_accessibility(self):
        p = self.parsed
        self.assertEqual(p.main, 1)
        self.assertEqual(p.headings, 1)
        self.assertEqual(len(p.ids), len(set(p.ids)), "Duplicate HTML id")
        self.assertIn("href=\"#main\"", self.content)
        self.assertIn('aria-live="polite"', self.content)
        self.assertIn("width=device-width", self.content)
        self.assertIn("@media(max-width:650px)", self.content)
        self.assertIn("prefers-reduced-motion:reduce", self.content)

    def test_mock_is_not_instance_evidence(self):
        for marker in ("MOCK-ONLY", "SOURCE-ONLY", "DEV-VERIFIED",
                       "PRODUCTION-VERIFIED", "No ServiceNow instance execution",
                       "no ServiceNow licence", "publication approval"):
            with self.subTest(marker=marker):
                self.assertIn(marker.lower(), self.content.lower())
        self.assertEqual(set(b["data-scenario"] for b in self.parsed.buttons),
                         {"baseline", "truncated", "unavailable", "overlap", "ownership"})
        self.assertEqual(self.parsed.media, [])
        for token in BANNED:
            self.assertNotIn(token, self.content)

    def test_public_navigation_targets_exist(self):
        self.assertTrue(self.parsed.links)
        for href in self.parsed.links:
            u = urlsplit(href)
            self.assertFalse(u.scheme or u.netloc, "Nonlocal link: " + href)
            path = u.path or TARGET.name
            self.assertTrue((ROOT / path).is_file(), "Missing link: " + href)
            if not u.path and u.fragment:
                self.assertIn(u.fragment, self.parsed.ids)

    def test_core_decision_rules_are_visible_and_guarded(self):
        for token in ("!record.tableAvailable", "record.truncated",
                      "record.missingParent + record.missingChild - record.bothMissing",
                      "return {status:\"NOT ASSESSED\"", "return {status:\"PARTIAL\"",
                      "return {status:\"REVIEW\"", "return {status:\"PASS\"",
                      'textContent=JSON.stringify(receipt,null,2)'):
            with self.subTest(token=token):
                self.assertIn(token, self.content)

if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3
"""Source-target portfolio boundary: fail closed on accidental certification."""
import json
import re
import unittest
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "source-target-compatibility.html"
REGISTER = ROOT / "evidence" / "public-verification-register.json"

class Inspector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.duplicates = set()
        self.selects = set()
        self.links = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get("id"):
            if a["id"] in self.ids:
                self.duplicates.add(a["id"])
            self.ids.add(a["id"])
        if tag == "select":
            self.selects.add(a.get("id"))
        if tag == "a":
            self.links.append(a.get("href"))

class ScopeBoundaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PAGE.read_text(encoding="utf-8")
        cls.doc = Inspector()
        cls.doc.feed(cls.html)

    def test_all_seven_review_gates_have_labels_and_controls(self):
        self.assertFalse(self.doc.duplicates)
        self.assertEqual(self.doc.selects,
                         {"gate-G%02d" % x for x in range(1, 8)})
        self.assertEqual(len(re.findall(r'data-gate="G\d{2}"', self.html)), 7)
        for number in range(1, 8):
            self.assertIn('for="gate-G%02d"' % number, self.html)

    def test_self_report_never_becomes_certification(self):
        self.assertIn('publication_status:"HOLD"', self.html)
        self.assertIn('independent_dev_verified:false', self.html)
        self.assertIn('production_verified:false', self.html)
        self.assertIn('review_type:"untrusted_self_report"', self.html)
        self.assertIn('scope_parity:"historically_mismatched_not_independently_rechecked"', self.html)
        self.assertIn('29 native acceptance cases NOT RUN', self.html)
        self.assertIn('DEV-REPORTED', self.html)
        self.assertIn('MOCK-ONLY', self.html)

    def test_no_instance_ids_or_remote_visuals_or_persistence(self):
        for forbidden in ('dev438211', 'x_1577958_', 'x_eitsp_', 'sys_id=',
                          'http://', '<img', '<iframe', 'localStorage',
                          'sessionStorage', 'fetch(', 'XMLHttpRequest'):
            self.assertNotIn(forbidden, self.html)
        self.assertIn("connect-src 'none'", self.html)
        self.assertIn("img-src 'none'", self.html)

    def test_public_navigation_and_evidence_register(self):
        self.assertIn('source-target-compatibility.html',
                      (ROOT / "index.html").read_text(encoding="utf-8"))
        self.assertIn('source-target-compatibility.html',
                      (ROOT / "portfolio-review-guide.html").read_text(encoding="utf-8"))
        self.assertIn('source-target-compatibility.html',
                      (ROOT / "sitemap.xml").read_text(encoding="utf-8"))
        items = json.loads(REGISTER.read_text(encoding="utf-8"))["items"]
        entries = [x for x in items if x.get("id") == "SCOPE-COMPATIBILITY"]
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0]["classification"], "source-only")
        self.assertEqual(entries[0]["page"], PAGE.name)

if __name__ == "__main__":
    unittest.main()

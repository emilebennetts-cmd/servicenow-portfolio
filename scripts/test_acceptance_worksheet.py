#!/usr/bin/env python3
"""Structural and publication-boundary tests for the browser-local acceptance worksheet."""
from html.parser import HTMLParser
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "workbench-acceptance-playbook.html"

class PageScan(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.duplicates = set()
        self.tests = []
        self.links = []
        self.scripts = 0

    def handle_starttag(self, tag, attrs):
        fields = dict(attrs)
        if fields.get("id"):
            if fields["id"] in self.ids:
                self.duplicates.add(fields["id"])
            self.ids.add(fields["id"])
        if fields.get("data-test"):
            self.tests.append(fields["data-test"])
        if tag == "a":
            self.links.append(fields.get("href", ""))
        if tag == "script":
            self.scripts += 1

class AcceptanceWorksheetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PAGE.read_text(encoding="utf-8")
        cls.page = PageScan()
        cls.page.feed(cls.html)

    def test_evidence_classes_and_six_native_scenarios(self):
        self.assertEqual(set(self.page.tests),
                         {"A01", "A02", "A03", "A04", "A05", "A06"})
        self.assertEqual(len(self.page.tests), 6)
        self.assertFalse(self.page.duplicates)
        self.assertIn("native-execution-ledger", self.page.ids)
        self.assertEqual(self.page.scripts, 1)
        self.assertEqual(self.html.count('data-result'), 7) # six fields and one selector
        for key in ("SOURCE-ONLY", "MOCK-ONLY", "DEV-VERIFIED",
                    "PRODUCTION-VERIFIED", "HOLD", "independent", "entitlement"):
            self.assertIn(key, self.html)

    def test_fail_closed_receipt(self):
        for item in (
            'verification_classification:"SOURCE-ONLY"',
            'publication_status:"HOLD"',
            "publication_authorised:false",
            "dev_verified:false",
            "production_verified:false",
            "native_test_execution_by_this_tool:false",
            "review_required:true",
            'review_gaps:data.violations',
            "safeAlias(t.receipt_alias)",
            "t.result===\"PASS\"&&!t.receipt_alias",
        ):
            self.assertIn(item, self.html)
        self.assertNotIn('verification_classification:"DEV-VERIFIED"', self.html)
        self.assertNotIn('publication_authorised:true', self.html)

    def test_private_data_safety_and_accessibility(self):
        self.assertIn("connect-src 'none'", self.html)
        self.assertIn("form-action 'none'", self.html)
        self.assertIn('role="status" aria-live="polite"', self.html)
        self.assertIn('autocomplete="off"', self.html)
        self.assertIn('data-receipt', self.html)
        self.assertNotRegex(self.html, r"\b(?:fetch|XMLHttpRequest|localStorage|sendBeacon)\s*\(")
        self.assertNotIn("https://drive.google.com", self.html)
        self.assertNotIn("servicenow-portfolio-control", self.html)
        self.assertNotRegex(self.html, r"<img\b")

    def test_import_is_untrusted_and_fail_closed(self):
        for token in (
            'id="worksheet-import"', 'id="receipt-import-output"',
            'id="receipt-comparison"', 'accept=".json,application/json"',
            'file.size>32768', 'inspectReceipt(JSON.parse(raw))',
            'exactKeys(data,top)', 'data.publication_authorised!==false',
            'data.dev_verified!==false', 'data.production_verified!==false',
            'data.native_test_execution_by_this_tool!==false',
            'data.independent_reviewer_approval!==false',
            'ids.has(item.test_id)', 'safeAlias(item.receipt_alias)',
            'comparisonBody.replaceChildren()', 'td.textContent=cell',
            'comparison.hidden=true', 'importInput.value=""',
        ):
            self.assertIn(token, self.html)
        self.assertNotIn('innerHTML=', self.html)
        self.assertNotIn('eval(', self.html)

    def test_public_navigation(self):
        for href in self.page.links:
            if href.startswith(("https:", "mailto:", "#")):
                continue
            path = href.split("#", 1)[0]
            if path:
                self.assertTrue((ROOT / path).exists(), href)
        self.assertIn("workbench-acceptance-playbook.html",
                      (ROOT / "index.html").read_text(encoding="utf-8"))

if __name__ == "__main__":
    unittest.main()

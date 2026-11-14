#!/usr/bin/env python3
"""Offline contract for the synthetic KI collector failure-mode gallery.

Asserts the public page stays source-informed, customer-neutral and non-certifying.
No ServiceNow access or external Python dependencies are required.
"""
from html.parser import HTMLParser
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "knowledge-intelligence-acceptance-matrix.html"


class Collector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.duplicate = set()
        self.fixtures = []
        self.images = []
        self.embeds = []

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        key = values.get("id")
        if key:
            if key in self.ids:
                self.duplicate.add(key)
            self.ids.add(key)
        if "data-contract" in values:
            self.fixtures.append(values["data-contract"])
        if tag in {"img", "svg", "picture"}:
            self.images.append(tag)
        if tag in {"iframe", "object", "embed"}:
            self.embeds.append(tag)


class CollectorFaultContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PAGE.read_text(encoding="utf-8")
        cls.page = Collector()
        cls.page.feed(cls.html)

    def test_four_fixed_examples_and_unique_selectors(self):
        self.assertEqual(self.page.fixtures, ["complete", "table", "field", "mutation"])
        self.assertFalse(self.page.duplicate)
        for key in ("collector-contract", "collector-contract-detail", "collector-contract-heading",
                    "collector-contract-status", "collector-contract-title",
                    "collector-contract-explanation", "collector-contract-handling",
                    "collector-contract-test", "collector-contract-boundary",
                    "collector-contract-export"):
            self.assertIn(key, self.page.ids)
        self.assertIn('aria-live="polite"', self.html)
        self.assertIn('aria-atomic="true"', self.html)

    def test_source_truth_and_native_negative_cases(self):
        for text in ("ki-evidence/1.0", "table_unavailable", "field_unavailable",
                     "two-minute duration", "45 read-only collectors",
                     "KI-COL-01", "KI-COL-02", "KI-COL-03", "KI-COL-04",
                     "source-informed, synthetic contract gallery"):
            self.assertIn(text, self.html)
        self.assertIn("DEV-REPORTED", self.html)
        self.assertIn("no dev read-back", self.html.lower())
        self.assertIn("no ServiceNow licence", self.html)

    def test_export_is_immutable_mock_only_not_native(self):
        script = self.html.split("/* Fixed public fixtures only.", 1)[1]
        for literal in ('evidence_classification:"MOCK-ONLY"',
                        'collector_runtime:"NOT RUN"', "dev_verified:false",
                        "production_verified:false", "review_approved:false",
                        "actual_collector_output:null", "customer_information:null",
                        'publication_approval:"HOLD"'):
            self.assertIn(literal, script)
        self.assertIn('portfolio-ki-collector-fault-contract/1.0', script)
        self.assertIn('Object.hasOwn(outcomes,key)', script)
        self.assertNotRegex(script, r"(?i)\b(?:fetch|XMLHttpRequest|localStorage|sessionStorage)\s*\(")

    def test_no_unreviewed_visual_or_private_links(self):
        self.assertFalse(self.page.images)
        self.assertFalse(self.page.embeds)
        for forbidden in ("servicenow-portfolio-control", "drive.google.com/file/",
                          "docs.google.com/", "x_1577958_dw2", "client_secret",
                          "<img", "data:image/"):
            self.assertNotIn(forbidden, self.html)
        self.assertIn("connect-src 'none'", self.html)
        self.assertIn("@media(max-width:760px)", self.html)

    def test_old_acceptance_contract_preserved(self):
        self.assertEqual(len(re.findall(r'<tr class="module" data-code=', self.html)), 45)
        self.assertEqual(self.html.count('data-schema-table="source-only"'), 16)
        self.assertIn('id="acceptance"', self.html)
        self.assertIn('id="taxonomy"', self.html)


    def test_source_module_acceptance_export_is_plan_only(self):
        for key in ("ki-test-matrix", "ki-test-matrix-heading", "ki-export-all",
                    "ki-export-filtered", "matrix-export-status"):
            self.assertIn(key, self.page.ids)
        self.assertEqual(len(re.findall(r'<tr class="module" data-code=', self.html)), 45)
        self.assertIn("180 executable acceptance questions", self.html)
        self.assertIn("PROPOSED", self.html)
        self.assertIn("never delete real tables", self.html.lower())
        script = self.html.split("/* Native test matrix exporter:", 1)[1].split("/* Fixed public fixtures only.", 1)[0]
        for required in ('"SOURCE-ONLY","PROPOSED","NOT RUN","false","false","HOLD","",""',
                         'test.id', 'ki-evidence/1.0', 'table_unavailable', 'field_unavailable',
                         'row.hidden', 'text/csv;charset=utf-8', 'safeCell', '120',
                         'replace(/"/g', 'connect'):
            if required == 'connect':
                self.assertNotRegex(script, r"(?i)\b(?:fetch|XMLHttpRequest|localStorage|sessionStorage)\s*\(")
            else:
                self.assertIn(required, script)
        self.assertIn("no native execution or approval is asserted", script.lower())
        self.assertIn("ki-source-acceptance-all-45-modules-HOLD.csv", script)
        self.assertIn("ki-source-acceptance-filtered-HOLD.csv", script)



if __name__ == "__main__":
    unittest.main()

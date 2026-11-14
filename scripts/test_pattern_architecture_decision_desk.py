#!/usr/bin/env python3
"""Static regression for source-informed, MOCK-ONLY pattern architecture decision UI."""
from html.parser import HTMLParser
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "reusable-delivery-patterns-case-study.html"

class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.options = []
        self.checks = []
        self.links = []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            self.ids.append(attrs["id"])
        if tag == "option":
            self.options.append(attrs.get("value"))
        if attrs.get("data-fit-check"):
            self.checks.append(attrs["data-fit-check"])
        if tag == "a" and attrs.get("href"):
            self.links.append(attrs["href"])

class PatternArchitectureDecisionDeskTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PAGE.read_text(encoding="utf-8")
        cls.dom = PageParser()
        cls.dom.feed(cls.html)

    def test_accessible_and_bounded_user_controls(self):
        self.assertEqual(len(self.dom.ids), len(set(self.dom.ids)))
        for ident in ("pattern-fit-desk","fit-scenario","fit-approach","fit-context",
                      "fit-status","fit-gaps","fit-export","fit-reset","fit-import-file","fit-export-feedback"):
            self.assertIn(ident, self.dom.ids)
        self.assertEqual(self.dom.options,
                         ["mim","cmdb","request","ootb","pattern","extension"])
        self.assertEqual(self.dom.checks,
                         ["owner","baseline","entitlement","security","acceptance","exception"])
        self.assertIn('aria-live="polite"', self.html)
        self.assertIn("@media(max-width:750px)", self.html)

    def test_non_certifying_export_and_missing_gate_controls(self):
        for marker in ("classification:'mock-only'","review_state:'UNREVIEWED'",
                       "verification_state:'NOT VERIFIED'","release_state:'HOLD'",
                       "native_service_now_execution:false","independent_review_approved:false",
                       "production_verified:false","public_screenshot_approved:false",
                       "open_gates:gaps","preparation_complete:gaps.length===0"):
            self.assertIn(marker,self.html)
        self.assertIn("required=checks.filter",self.html)
        self.assertIn("mode!=='ootb'||x[0]!=='exception'",self.html)
        self.assertIn("ul.replaceChildren()",self.html)
        self.assertIn("li.textContent=g",self.html)
        self.assertIn("JSON.stringify(payload,null,2)",self.html)
        for marker in ("function validateDraft(data)","Object.keys(data).length!==keys.length",
                       "Object.prototype.hasOwnProperty.call(scenarios,data.scenario)",
                       "new Set(selected).size!==selected.length","buildSnapshot(data.scenario",
                       "JSON.stringify(data[k])!==JSON.stringify(expected[k])",
                       "file.size>16384","Invalid, altered"):
            # The user-facing rejection uses lower case; do not depend on text capitalization.
            if marker=="Invalid, altered":
                marker="invalid, altered"
            self.assertIn(marker,self.html)

    def test_no_sensitive_data_or_unsanctioned_networking(self):
        for forbidden in ("localStorage","sessionStorage","fetch(","XMLHttpRequest",
                          "navigator.sendBeacon","servicenow-portfolio-control",
                          "dev438211.service-now.com","x_1577958_vdf",
                          "drive.google.com/file/d/","docs.google.com/document/d/"):
            self.assertNotIn(forbidden,self.html)
        self.assertNotIn("<img",self.html.lower())
        self.assertNotIn("<script src=",self.html.lower())

    def test_existing_technical_story_and_gate_still_present(self):
        for value in ("01 / The client's pain &amp; history","02 / The ServiceNow solution",
                      "03 / Architectural best practices","4.22.2","4.20.0",
                      "SOURCE-ONLY","MOCK-ONLY"):
            self.assertIn(value,self.html)
        self.assertIn("production",self.html.lower())
        self.assertIn("pattern-readiness.html",self.dom.links)
        self.assertTrue((ROOT / "pattern-readiness.html").is_file())

if __name__ == "__main__":
    unittest.main()

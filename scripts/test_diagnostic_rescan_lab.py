"""Contract tests for the public synthetic baseline/rescan decision lab.

This test does not authenticate to ServiceNow and deliberately contains
no real collector output, screenshots or customer data.
"""
import json
import unittest
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "diagnostic-rescan-decision-lab.html"

class Reader(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.duplicates = []
        self.links = []
        self.image_count = 0
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            if a["id"] in self.ids:
                self.duplicates.append(a["id"])
            self.ids.add(a["id"])
        if tag == "a":
            self.links.append(a.get("href"))
        if tag in {"img", "iframe", "picture", "video"}:
            self.image_count += 1

class RescanLabTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PAGE.read_text(encoding="utf-8")
        cls.parser = Reader()
        cls.parser.feed(cls.html)

    def test_accessibility_and_safe_navigation(self):
        self.assertFalse(self.parser.duplicates)
        self.assertEqual(self.parser.image_count, 0)
        self.assertTrue({"main","scenario","threshold","threshold-value",
                         "decision","decision-description","metrics","gates",
                         "reviewer","limitations","download","reset",
                         "print","export-message"} <= self.parser.ids)
        self.assertIn("prefers-reduced-motion", self.html)
        self.assertIn("aria-live=\"polite\"", self.html)
        self.assertIn("diagnostic-rescan-decision-lab.html",
                      (ROOT / "sitemap.xml").read_text(encoding="utf-8"))
        for host_page in ("index.html", "portfolio-review-guide.html",
                          "portfolio-explorer.html"):
            self.assertIn('href="diagnostic-rescan-decision-lab.html"',
                          (ROOT / host_page).read_text(encoding="utf-8"))

    def test_deny_by_default_and_evidence_classification(self):
        for required in ("SOURCE-ONLY","MOCK-ONLY","DEV-REPORTED","DEV-VERIFIED",
                         "PRODUCTION-VERIFIED","NOT ASSESSED","REGRESSION / HOLD",
                         "IMPROVEMENT CANDIDATE / HOLD","NOT RUN",
                         "public_release_authorised:false",
                         "servicenow_dev_verified:false",
                         "production_verified:false","actual_collector_output:null",
                         "connect-src 'none'","img-src 'none'",
                         "no ServiceNow licence","NO-DATA-REQUIRES-REVIEW"):
            if required == "NO-DATA-REQUIRES-REVIEW":
                continue
            self.assertIn(required, self.html)
        for forbidden in ("fetch(","XMLHttpRequest","localStorage","indexedDB",
                          "innerHTML","dev438211","service-now.com/",
                          "github.com/emilebennetts-cmd/Diagnostic-Workbench2",
                          "drive.google.com","<img"):
            self.assertNotIn(forbidden, self.html)
        manifest = json.loads((ROOT / "evidence/public-verification-register.json")
                              .read_text(encoding="utf-8"))
        claim = next(x for x in manifest["items"] if x["id"]=="DIAGNOSTIC-RESCAN-LAB")
        self.assertEqual(claim["classification"], "mock-only")
        self.assertEqual(claim["page"], PAGE.name)
        self.assertIn("HOLD", claim["runtime_verification"])

    def test_four_fixtures_and_guardrail_implementation(self):
        for token in ("improve:{","missing:{","drift:{","regress:{",
                      "baselineRate-rescanRate","cfg.baseline===cfg.rescan",
                      "rescanRate!==null","den<=0","regressions?",
                      "threshold.addEventListener","scenario.addEventListener",
                      "URL.createObjectURL","URL.revokeObjectURL"):
            self.assertIn(token, self.html)

if __name__ == "__main__":
    unittest.main()

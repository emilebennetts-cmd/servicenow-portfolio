#!/usr/bin/env python3
"""Contract tests for source-informed CSDM 5 architecture in the CMDB case study."""
from html.parser import HTMLParser
from pathlib import Path
import unittest
ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "cmdb-ire-assurance.html"
class Audit(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.images = 0
        self.scripts = 0
        self.disclosures = 0
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"): self.ids.append(attrs["id"])
        if tag in ("img", "iframe", "picture", "object", "embed"): self.images += 1
        if tag == "script": self.scripts += 1
        if tag == "details": self.disclosures += 1
class OwnershipContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PAGE.read_text(encoding="utf-8")
        cls.audit = Audit()
        cls.audit.feed(cls.html)
    def test_csdm_names_and_safe_semantics(self):
        for term in ("CSDM 5", "Business Application", "Service Instance", "Business Service",
                     "Service Offering", "Technology Management Service", "cmdb_ci_business_app",
                     "cmdb_ci_service_auto", "cmdb_ci_service_business", "service_offering",
                     "cmdb_ci_service_technical", "not</em> establish a direct native CI relationship"):
            self.assertIn(term, self.html)
        self.assertIn('id="csdm-ownership"', self.html)
        self.assertIn('href="#csdm-ownership"', self.html)
    def test_mobile_and_accessibility(self):
        self.assertEqual(len(self.audit.ids), len(set(self.audit.ids)))
        self.assertGreaterEqual(self.audit.disclosures, 7)
        self.assertIn('aria-labelledby="csdm-heading"', self.html)
        self.assertIn(".csdm-grid,.csdm-gates{grid-template-columns:1fr}", self.html)
        self.assertIn(".csdm-cases{grid-template-columns:1fr}", self.html)
        self.assertIn("summary:focus-visible", self.html)
    def test_publication_boundaries(self):
        self.assertIn("SOURCE-ONLY / PROPOSED", self.html)
        self.assertIn("no ServiceNow licence", self.html)
        self.assertIn("DEV-VERIFIED", self.html)
        self.assertIn("PRODUCTION-VERIFIED", self.html)
        self.assertEqual(self.audit.images, 0)
        self.assertEqual(self.audit.scripts, 0)
        for prohibited in ("drive.google.com", "github.com/emilebennetts-cmd/solution-lifecycle-studio",
                           "github.com/emilebennetts-cmd/Diagnostic-Workbench2",
                           "github.com/emilebennetts-cmd/servicenow-portfolio-control",
                           "localStorage", "fetch(", "onerror=", "onload="):
            self.assertNotIn(prohibited, self.html)
if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3
"""Contract tests for the public, synthetic CMDB source-onboarding lab.

These tests do not call ServiceNow, read confidential repositories, or approve
the publication of any original Workbench screenshot.
"""
from html.parser import HTMLParser
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "cmdb-source-onboarding-lab.html"


class Markup(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.gates = []
        self.images = 0
        self.scripts = 0
        self.external_scripts = 0
        self.lang = None

    def handle_starttag(self, name, attrs):
        attrs = dict(attrs)
        if name == "html":
            self.lang = attrs.get("lang")
        if attrs.get("id"):
            assert attrs["id"] not in self.ids, "Duplicate HTML ID"
            self.ids.add(attrs["id"])
        if name == "input" and "data-gate" in attrs:
            self.gates.append(attrs["data-gate"])
        if name in {"img", "picture", "iframe", "video", "canvas"}:
            self.images += 1
        if name == "script":
            self.scripts += 1
            self.external_scripts += int(bool(attrs.get("src")))


class CMDBSourceOnboardingLab(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PAGE.read_text(encoding="utf-8")
        cls.page = Markup()
        cls.page.feed(cls.html)

    def test_structure_and_navigation(self):
        self.assertEqual(self.page.lang, "en")
        self.assertEqual(self.page.images, 0, "No real or simulated captures should be embedded")
        self.assertEqual(self.page.scripts, 1)
        self.assertEqual(self.page.external_scripts, 0)
        for id_ in ("main", "scenario-select", "gate-count", "gate-status",
                    "missing-controls", "download-receipt", "receipt-preview"):
            self.assertIn(id_, self.page.ids)
        self.assertIn('href="cmdb-ire-assurance.html"', self.html)

    def test_complete_control_family_and_synthetic_cases(self):
        self.assertEqual(set(self.page.gates),
                         {"class", "identity", "authority", "access", "tests", "governance"})
        self.assertEqual(len(self.page.gates), 6)
        self.assertIn('value="stable"', self.html)
        self.assertIn('value="collision"', self.html)
        self.assertIn('value="attributes"', self.html)
        self.assertIn("fundamentalBlock:true", self.html)
        self.assertIn("READY_FOR_NATIVE_SIMULATION_NOT_APPROVED", self.html)
        self.assertIn("BLOCKED_DESIGN_INPUT", self.html)

    def test_evidence_and_no_native_runtime_claims(self):
        for marker in ("SOURCE-ONLY", "MOCK-ONLY", "DEV-VERIFIED",
                       "PRODUCTION-VERIFIED", "not the native",
                       "No genuine Workbench screenshot"):
            self.assertIn(marker, self.html)
        self.assertIn("servicenow_dev_verified:false", self.html)
        self.assertIn("production_verified:false", self.html)
        self.assertIn("approval_granted:false", self.html)
        self.assertIn("actual_ire_response:null", self.html)
        self.assertNotIn("dev438211", self.html)

    def test_no_network_storage_or_private_destinations(self):
        for prohibited in ("fetch(", "XMLHttpRequest", "sendBeacon(",
                           "localStorage", "sessionStorage", "indexedDB",
                           "github.com/emilebennetts-cmd/solution-lifecycle-studio",
                           "github.com/emilebennetts-cmd/Diagnostic-Workbench2",
                           "github.com/emilebennetts-cmd/servicenow-portfolio-control",
                           "drive.google.com", "innerHTML"):
            with self.subTest(term=prohibited):
                self.assertNotIn(prohibited, self.html)
        self.assertIn("connect-src 'none'", self.html)
        self.assertIn("base-uri 'none'", self.html)
        self.assertIn("form-action 'none'", self.html)
        self.assertIn("URL.createObjectURL", self.html)

    def test_no_real_hardware_identifiers(self):
        self.assertNotRegex(self.html, r"\b[0-9a-f]{32}\b")
        self.assertNotRegex(self.html, r"\b[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{4}\b")


if __name__ == "__main__":
    unittest.main()

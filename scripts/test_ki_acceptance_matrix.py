#!/usr/bin/env python3
"""Offline structural/security contract for the KI source and synthetic review matrix.

No network, credentials, private repository assets or ServiceNow instance required.
"""
from html.parser import HTMLParser
from pathlib import Path
import json
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "knowledge-intelligence-acceptance-matrix.html"


class Collector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.duplicate, self.modules, self.gates, self.options = set(), set(), [], [], []
        self.links, self.images = [], []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        element_id = a.get("id")
        if element_id:
            if element_id in self.ids:
                self.duplicate.add(element_id)
            self.ids.add(element_id)
        if tag == "tr" and "data-code" in a:
            self.modules.append((a["data-code"], a.get("data-pack")))
        if tag == "input" and "data-gate" in a:
            self.gates.append(a["data-gate"])
        if tag == "option":
            self.options.append(a.get("value"))
        if tag == "a":
            self.links.append(a.get("href", ""))
        if tag == "img":
            self.images.append(a)


class KIAcceptanceContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PAGE.read_text(encoding="utf-8")
        cls.parser = Collector()
        cls.parser.feed(cls.html)

    def test_taxonomy_counts_and_ids(self):
        self.assertEqual(len(self.parser.modules), 45)
        self.assertEqual(len(set(self.parser.modules)), 45)
        self.assertEqual(len(set(code for code, _ in self.parser.modules)), 45)
        self.assertEqual(len(set(pack for _, pack in self.parser.modules)), 16)
        self.assertTrue(all(re.fullmatch(r"[A-Z]+\.[A-Z]+", code)
                            for code, _ in self.parser.modules))
        self.assertIn(("CMDB.IRE", "CMDB & CSDM"), self.parser.modules)
        self.assertIn(("ITSM.MIM", "ITSM"), self.parser.modules)

    def test_exact_review_controls(self):
        self.assertEqual(len(self.parser.gates), 8)
        self.assertEqual(len(set(self.parser.gates)), 8)
        self.assertEqual(set(self.parser.gates), {
            "identity", "schema", "access", "collection", "coverage",
            "lineage", "content", "approval"
        })
        self.assertFalse(self.parser.duplicate)

    def test_accessible_controls_and_synthetic_boundaries(self):
        self.assertTrue({"module-search", "pack-filter", "reset-filter",
                         "module-count", "gate-list", "readiness-receipt",
                         "readiness-status", "download-packet"} <= self.parser.ids)
        for mark in ("SOURCE-ONLY", "MOCK-ONLY", "DEV-REPORTED", "DEV-VERIFIED",
                     "PRODUCTION-VERIFIED", "NOT ASSESSED", "REVIEW-READY · HOLD",
                     "public_release_authorised:false", "dev_execution_verified:false",
                     "production_deployment_verified:false", "service_now_instance:null"):
            self.assertIn(mark, self.html)
        self.assertIn('aria-live="polite"', self.html)
        self.assertIn('name="viewport"', self.html)
        self.assertIn("@media(max-width:650px)", self.html)

    def test_conflict_and_license_boundary(self):
        self.assertIn("16 unique table objects", self.html)
        self.assertIn("16 matching collection dictionary records", self.html)
        self.assertIn("previously said 17", self.html)
        self.assertEqual(self.html.count('data-schema-table="source-only"'), 16)
        self.assertIn("source_template_tables:16", self.html)
        self.assertIn("source_collection_dictionary_entries:16", self.html)
        self.assertIn("target_schema_readback_verified:false", self.html)
        self.assertIn("public_release_authorised:false", self.html)
        self.assertIn("30 September 2026", self.html)
        self.assertIn("no ServiceNow licence", self.html)
        self.assertIn("not additive", self.html)

    def test_private_information_and_network_exclusion(self):
        self.assertFalse(self.parser.images, "No source screenshot is cleared")
        self.assertFalse(any("drive.google.com" in url or "docs.google.com" in url
                             for url in self.parser.links))
        for excluded in ("servicenow-portfolio-control", "1pDhaRbcO9ab", "Authorization:",
                         "x_1577958_dw2", "client_secret", "api.github.com/repos/"):
            self.assertNotIn(excluded, self.html)
        self.assertIn("connect-src 'none'", self.html)
        self.assertIn("object-src 'none'", self.html)
        self.assertIn("form-action 'none'", self.html)

    def test_verification_register_route(self):
        register = json.loads((ROOT / "evidence/public-verification-register.json")
                              .read_text(encoding="utf-8"))
        matched = [x for x in register["items"]
                   if x["id"] == "KI-ACCEPTANCE-MATRIX"]
        self.assertEqual(len(matched), 1)
        self.assertEqual(matched[0]["classification"], "mock-only")
        self.assertEqual(matched[0]["page"], PAGE.name)
        self.assertIn(PAGE.name, (ROOT / "index.html").read_text(encoding="utf-8"))
        self.assertIn(PAGE.name, (ROOT / "sitemap.xml").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()

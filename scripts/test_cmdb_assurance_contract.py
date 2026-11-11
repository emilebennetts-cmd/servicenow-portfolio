#!/usr/bin/env python3
"""CMDB / IRE case-study contract: technical traceability, access and safety.

Public-only tests. These do not access private source or validate collectors on
a ServiceNow instance and cannot be used as a runtime acceptance receipt.
"""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
import unittest

ROOT = Path(__file__).resolve().parents[1]
TARGET = "cmdb-ire-assurance.html"
RESTRICTED = (
    "github.com/emilebennetts-cmd/Diagnostic-Workbench2",
    "github.com/emilebennetts-cmd/solution-lifecycle-studio",
    "github.com/emilebennetts-cmd/servicenow-portfolio-control",
)


class ContractParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.lang = None
        self.main_count = 0
        self.h1_count = 0
        self.ids = set()
        self.duplicates = set()
        self.links = []
        self.media = []
        self.skip = []

    def handle_starttag(self, tag, attrs):
        props = dict(attrs)
        if tag == "html":
            self.lang = props.get("lang")
        if tag == "main":
            self.main_count += 1
        if tag == "h1":
            self.h1_count += 1
        if props.get("id"):
            if props["id"] in self.ids:
                self.duplicates.add(props["id"])
            self.ids.add(props["id"])
        if tag == "a":
            self.links.append(props.get("href", ""))
            if props.get("class") == "skip":
                self.skip.append(props.get("href"))
        if tag in ("img", "picture", "video", "iframe", "canvas", "source"):
            self.media.append(tag)


class CMDBAssuranceContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.doc = (ROOT / TARGET).read_text(encoding="utf-8")
        cls.parsed = ContractParser()
        cls.parsed.feed(cls.doc)

    def test_semantic_and_responsive_baseline(self):
        p = self.parsed
        self.assertEqual(p.lang, "en")
        self.assertEqual(p.main_count, 1)
        self.assertEqual(p.h1_count, 1)
        self.assertEqual(p.duplicates, set())
        self.assertIn("main", p.ids)
        self.assertIn("#main", p.skip)
        self.assertIn("width=device-width", self.doc)
        self.assertIn("@media(max-width:580px)", self.doc)
        self.assertIn("prefers-reduced-motion", self.doc)

    def test_collector_coverage_and_limitations(self):
        for phrase in (
            "CI inventory", "IRE configuration", "Duplicate indicators",
            "Relationships", "Server lifecycle", "cmdb_ci",
            "cmdb_rel_ci", "SOURCE-ONLY", "DEV-VERIFIED", "MOCK-ONLY",
            "PRODUCTION-VERIFIED", "group limits", "double-count",
            "name", "serial", "NOT ASSESSED", "read-only",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase.lower(), self.doc.lower())
        self.assertIn("No collector was executed", self.doc)
        self.assertIn("no ServiceNow licence", self.doc)
        self.assertIn("publication approval", self.doc)

    def test_no_unapproved_media_or_private_links(self):
        self.assertEqual(self.parsed.media, [])
        for private in RESTRICTED:
            self.assertNotIn(private, self.doc)
        for href in self.parsed.links:
            if not href:
                self.fail("Empty link found")
            url = urlsplit(href)
            if url.scheme or url.netloc:
                continue
            path = url.path or TARGET
            if path in (".", "./"):
                path = "index.html"
            self.assertTrue((ROOT / path).is_file(), href)
            if url.fragment and path == TARGET:
                self.assertIn(url.fragment, self.parsed.ids)

    def test_discoverable_from_existing_case_study_and_home(self):
        for page in ("index.html", "diagnostic-workbench-case-study.html"):
            self.assertIn(TARGET, (ROOT / page).read_text(encoding="utf-8"))
        self.assertIn(TARGET, (ROOT / "sitemap.xml").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()

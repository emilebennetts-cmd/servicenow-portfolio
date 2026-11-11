#!/usr/bin/env python3
"""Public case-study contract: provenance, accessible structure and no image leaks.

These checks operate on the public site only. They do not inspect private source,
require ServiceNow credentials, or approve unpublished screenshot candidates.
"""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
import unittest

ROOT = Path(__file__).resolve().parents[1]
CASES = {
    "diagnostic-workbench-case-study.html": "implementation",
    "reusable-delivery-patterns-case-study.html": "build-map",
}
STATUS = ("SOURCE-ONLY", "DEV-VERIFIED", "MOCK-ONLY", "PRODUCTION-VERIFIED")
BLOCKED_DESTINATIONS = (
    "github.com/emilebennetts-cmd/solution-lifecycle-studio",
    "github.com/emilebennetts-cmd/Diagnostic-Workbench2",
    "github.com/emilebennetts-cmd/servicenow-portfolio-control",
)


class Structure(HTMLParser):
    def __init__(self):
        super().__init__()
        self.headings = []
        self.mains = 0
        self.ids = set()
        self.hrefs = []
        self.images = []
        self.lang = None

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "html":
            self.lang = attrs.get("lang")
        if tag == "h1":
            self.headings.append(tag)
        if tag == "main":
            self.mains += 1
        if attrs.get("id"):
            self.ids.add(attrs["id"])
        if tag == "a" and attrs.get("href"):
            self.hrefs.append(attrs["href"])
        if tag in {"img", "picture", "iframe", "video", "canvas"}:
            self.images.append((tag, attrs.get("src")))


class CaseStudyContract(unittest.TestCase):
    def test_structure_and_public_destinations(self):
        for filename, anchor in CASES.items():
            with self.subTest(page=filename):
                doc = (ROOT / filename).read_text(encoding="utf-8")
                parser = Structure()
                parser.feed(doc)
                self.assertEqual(parser.lang, "en")
                self.assertEqual(len(parser.headings), 1)
                self.assertEqual(parser.mains, 1)
                self.assertIn(anchor, parser.ids)
                self.assertIn(f"#{anchor}", parser.hrefs)
                self.assertIn("main", parser.ids)
                for href in parser.hrefs:
                    if href.startswith("#"):
                        self.assertIn(href[1:], parser.ids)
                    else:
                        target = urlsplit(href)
                        if not target.scheme and not target.netloc:
                            local = target.path or "index.html"
                            self.assertTrue((ROOT / local).is_file(), href)

    def test_evidence_status_and_publication_gate(self):
        for filename in CASES:
            with self.subTest(page=filename):
                doc = (ROOT / filename).read_text(encoding="utf-8")
                for item in STATUS:
                    self.assertIn(item, doc)
                self.assertIn("No genuine ServiceNow screenshots", doc)
                self.assertIn("publication approval", doc.lower())
                for blocked in BLOCKED_DESTINATIONS:
                    self.assertNotIn(blocked, doc)
                self.assertNotIn("dev438211.service-now.com", doc)
                parser = Structure()
                parser.feed(doc)
                self.assertFalse(parser.images, "Unreviewed media is not authorised")

    def test_diagnostic_lanes_are_not_conflated(self):
        doc = (ROOT / "diagnostic-workbench-case-study.html").read_text(encoding="utf-8")
        for required in (
            "two distinct runtime lanes", "IndexedDB local-first", "45 read-only collectors",
            "not yet wired", "not automatically synchronised", "30 September 2026",
            "1 September 2026", "rule version", "Not assessed",
        ):
            self.assertIn(required, doc)

    def test_delivery_source_does_not_inherit_dev_acceptance(self):
        doc = (ROOT / "reusable-delivery-patterns-case-study.html").read_text(encoding="utf-8")
        for required in (
            "SCHEMATIC ONLY", "Overview", "Milestones", "Deliverables", "RAID",
            "Dependencies", "Timeline", "Integrations", "4.22.2", "4.20.0",
            "not automatically reusable", "bidirectional writes",
        ):
            self.assertIn(required, doc)


if __name__ == "__main__":
    unittest.main()

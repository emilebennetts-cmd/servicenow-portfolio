#!/usr/bin/env python3
"""Public evidence library regression: no restricted source links or false runtime claims."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
import unittest

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "evidence.html"


class Structure(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.ids = set()
        self.lang = None
        self.mains = 0
        self.h1 = 0
        self.media = []

    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        if tag == "html":
            self.lang = data.get("lang")
        if tag == "main":
            self.mains += 1
        if tag == "h1":
            self.h1 += 1
        if data.get("id"):
            self.ids.add(data["id"])
        if tag == "a" and data.get("href"):
            self.links.append(data["href"])
        if tag in {"img", "picture", "video", "iframe", "object", "embed", "script"}:
            self.media.append(tag)


class EvidenceLibraryBoundaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PAGE.read_text(encoding="utf-8")
        cls.parser = Structure()
        cls.parser.feed(cls.html)

    def test_accessible_local_navigation_and_no_missing_routes(self):
        p = self.parser
        self.assertEqual("en", p.lang)
        self.assertEqual(1, p.mains)
        self.assertEqual(1, p.h1)
        self.assertIn("main", p.ids)
        self.assertIn("visual-evidence.html", p.links)
        for href in p.links:
            u = urlsplit(href)
            self.assertFalse(u.netloc, "Public evidence library must not require external logins")
            self.assertFalse(u.scheme)
            if u.path and u.path not in {".", "./"}:
                self.assertTrue((ROOT / u.path).is_file(), f"Missing public route: {href}")
            if u.fragment:
                self.assertIn(u.fragment, p.ids)

    def test_no_private_source_or_unapproved_screenshot_pixels(self):
        self.assertEqual([], self.parser.media)
        for blocked in (
            "drive.google.com", "docs.google.com",
            "github.com/emilebennetts-cmd/solution-lifecycle-studio",
            "github.com/emilebennetts-cmd/Diagnostic-Workbench2",
            "github.com/emilebennetts-cmd/servicenow-portfolio-control",
            "dev438211.service-now.com",
        ):
            self.assertNotIn(blocked, self.html)

    def test_historical_versions_and_evidence_tiers_remain_distinct(self):
        for phrase in (
            "SOURCE-ONLY", "MOCK-ONLY", "DEV-VERIFIED", "PRODUCTION-VERIFIED",
            "30 SEP 2026", "05 OCT 2026", "16 NOV 2026",
            "4.5.1", "4.20.0", "4.22.2",
            "No private source", "Current publication gate: HOLD",
            "Original ServiceNow screenshots approved for public release: 0",
            "No earlier historical DEV claim is inherited by later code",
            "Licence-free showcase",
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase, self.html)


if __name__ == "__main__":
    unittest.main()

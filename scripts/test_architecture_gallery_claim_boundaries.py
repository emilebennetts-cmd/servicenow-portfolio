#!/usr/bin/env python3
"""Contract tests for the public architecture gallery's dated claim boundaries.

Static-site checks only. These tests cannot attest native ServiceNow execution.
"""
from html.parser import HTMLParser
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / "workbench-architecture-gallery.html").read_text(encoding="utf-8")
BOUNDARY = HTML.split('<section id="baseline"', 1)[1].split('<section id="persona-tour"', 1)[0]


class BaselineCards(HTMLParser):
    def __init__(self):
        super().__init__()
        self.cards = 0
        self.links = []
        self.sources = []
        self.heading_ids = []

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if tag == "article" and attrs.get("class") == "baseline-card":
            self.cards += 1
        if tag == "a":
            self.links.append(attrs.get("href", ""))
        if tag == "h2":
            self.heading_ids.append(attrs.get("id", ""))
        if tag in {"script", "img", "iframe", "picture", "video", "object", "embed"}:
            self.sources.append(tag)


class ArchitectureGalleryAssurance(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser = BaselineCards()
        cls.parser.feed(BOUNDARY)

    def test_three_dated_not_interchangeable_evidence_snapshots(self):
        self.assertEqual(self.parser.cards, 3)
        for token in ("30 September 2026", "21 October 2026",
                      "4.6.1 source", "4.5.1", "4.22.2 source", "4.22.8 demo"):
            self.assertIn(token, BOUNDARY)
        self.assertIn("distinct application identity", BOUNDARY)
        self.assertIn("29-case native acceptance matrix remains NOT RUN", BOUNDARY)
        self.assertIn("not certification", BOUNDARY)

    def test_provenance_is_not_promoted_to_native_verification(self):
        self.assertIn("<dt>DEV-REPORTED</dt>", HTML)
        self.assertIn("<dt>DEV-VERIFIED</dt><dd>No new", HTML)
        self.assertIn("<dt>PRODUCTION-VERIFIED</dt><dd>Not established", HTML)
        self.assertNotIn("DEV-VERIFIED</dt><dd>Historical", HTML)
        self.assertNotIn("Browser-level rendering and interaction testing remain unverified", HTML)
        self.assertNotIn("234ff578", HTML)

    def test_accessible_responsive_architecture_cards(self):
        self.assertIn('href="#baseline"', HTML)
        self.assertIn('id="baseline" aria-labelledby="baseline-title"', HTML)
        self.assertIn("baseline-title", self.parser.heading_ids)
        self.assertIn("@media(max-width:880px)", HTML)
        self.assertIn("grid-template-columns:1fr", HTML)
        self.assertEqual(self.parser.sources, [])

    def test_links_and_private_source_containment(self):
        self.assertEqual(self.parser.links, ["incident-pack-native-pilot.html#native-matrix"])
        self.assertTrue((ROOT / "incident-pack-native-pilot.html").is_file())
        for forbidden in ("drive.google.com", "docs.google.com", "servicenow-portfolio-control",
                          "dev438211", "x_1577958", "x_eitsp", "sys_id",
                          "client_secret", "Bearer ", "https://", "<img"):
            self.assertNotIn(forbidden, BOUNDARY)
        self.assertNotRegex(BOUNDARY, r"(?i)(?:AKIA[A-Z0-9]{16}|[A-Fa-f0-9]{64})")

    def test_screenshot_remains_unpublished(self):
        self.assertIn("none published in this gallery", HTML)
        self.assertIn("explicit publication approval", HTML)
        self.assertNotIn("Approved genuine screenshots: 1", HTML)


if __name__ == "__main__":
    unittest.main()

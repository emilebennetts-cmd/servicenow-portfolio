#!/usr/bin/env python3
"""Static source-evidence contract for the 29 prepared native acceptance controls.

This file runs offline, performs no ServiceNow calls and does not assert execution.
"""
from html.parser import HTMLParser
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / "incident-pack-native-pilot.html").read_text(encoding="utf-8")
MATRIX = HTML.split('<section class="section native-matrix"', 1)[1].split(
    '<section class="line section"><div class="wrap">\n<div class="kicker">03 / Architectural best practices', 1
)[0]


class MatrixReader(HTMLParser):
    def __init__(self):
        super().__init__()
        self.cases = []
        self.options = []
        self.ids = []
        self.no_images = True

    def handle_starttag(self, tag, attrs):
        attr = dict(attrs)
        if "id" in attr:
            self.ids.append(attr["id"])
        if tag == "li" and "data-native-case" in attr:
            self.cases.append(attr)
        if tag == "option":
            self.options.append(attr.get("value", ""))
        if tag in {"img", "iframe", "picture", "svg", "embed", "video"}:
            self.no_images = False


class PreparedNativeMatrixContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser = MatrixReader()
        cls.parser.feed(MATRIX)

    def test_29_unique_source_cases_in_stable_order(self):
        self.assertEqual(
            [x["data-native-case"] for x in self.parser.cases],
            [f"NV-{n:03d}" for n in range(1, 30)],
        )
        self.assertEqual(len(self.parser.cases), 29)
        self.assertEqual(MATRIX.count("SOURCE-ONLY checklist · NOT RUN"), 29)

    def test_all_groups_and_personas_are_filterable(self):
        self.assertEqual(len(self.parser.ids), len(set(self.parser.ids)))
        self.assertEqual(self.parser.options.count("all"), 2)
        for case in self.parser.cases:
            self.assertIn(case["data-native-group"], self.parser.options)
            self.assertIn(case["data-native-persona"], self.parser.options)
        self.assertGreaterEqual(len(set(x["data-native-group"] for x in self.parser.cases)), 7)
        for phrase in ('for="native-group"', 'for="native-role"', 'role="status"',
                       'aria-live="polite"', 'id="native-export"',
                       'id="native-cases"', '0 of 29 evidenced'):
            self.assertIn(phrase, MATRIX)

    def test_does_not_promote_rehearsal_into_verified_approval(self):
        for phrase in ("21 October 2026", "SOURCE-ONLY", "NOT RUN",
                       "0 of 29 evidenced", "83/83", "no current"):
            # "no current" may appear in the surrounding historical claim; avoid assuming exact case.
            if phrase != "no current":
                self.assertIn(phrase.lower(), MATRIX.lower())
        self.assertIn('"NOT RUN","false","false","SOURCE-ONLY"', HTML)
        self.assertIn('native-pack-validation-NOT-RUN.csv', HTML)
        self.assertIn('const nativeRows=Array.from', HTML)
        self.assertIn('nativeGroup.addEventListener("change",updateNativeCases)', HTML)
        self.assertIn('nativeRole.addEventListener("change",updateNativeCases)', HTML)
        self.assertNotIn("DEV-VERIFIED · PASS", MATRIX)
        self.assertNotIn("PRODUCTION-VERIFIED · PASS", MATRIX)

    def test_no_private_pixels_or_executable_instance_connection(self):
        self.assertTrue(self.parser.no_images)
        for forbidden in (
            "drive.google.com", "docs.google.com", "servicenow-portfolio-control",
            "dev438211", "x_1577958", "<img", "<svg", "<iframe",
            "https://", "http://", "private-user-images", "client_secret",
            "fetch(", "XMLHttpRequest", "sendBeacon", "localStorage",
        ):
            self.assertNotIn(forbidden, MATRIX)
        self.assertNotRegex(MATRIX, r"(?i)(?:Bearer\\s+[A-Za-z0-9_]+|AKIA[A-Z0-9]{16})")

    def test_existing_historical_pilot_stays_distinct(self):
        self.assertIn("83 / 83", HTML)
        self.assertIn("36 linked draft", HTML)
        self.assertIn('id="journey"', HTML)
        self.assertIn('id="proof"', HTML)
        self.assertIn('href="#native-matrix"', HTML)
        self.assertIn("@media(max-width:760px)", HTML)


if __name__ == "__main__":
    unittest.main()

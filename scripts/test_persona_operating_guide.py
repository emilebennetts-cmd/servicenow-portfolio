#!/usr/bin/env python3
"""Offline source-bound and publication-safe persona guide regression checks."""
from html.parser import HTMLParser
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / "delivery-case-study.html").read_text(encoding="utf-8")
START = HTML.index('<section id="persona-operations"')
END = HTML.index('<section aria-labelledby="architecture">', START)
GUIDE = HTML[START:END]


class GuideParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.cards = []
        self.inputs = []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.append(attrs["id"])
        if tag == "li" and "persona-card" in attrs.get("class", "").split():
            self.cards.append(attrs)
        if tag == "input" and attrs.get("data-reviewed"):
            self.inputs.append(attrs)


class PersonaOperatingGuideContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.parser = GuideParser()
        cls.parser.feed(HTML)

    def test_twelve_distinct_procedures_and_matching_read_controls(self):
        self.assertEqual(len(self.parser.cards), 12)
        self.assertEqual(len(self.parser.inputs), 12)
        self.assertEqual(
            [c["data-procedure"] for c in self.parser.cards],
            [f"4.{i}" for i in range(1, 13)])
        self.assertEqual(
            [c["data-procedure"] for c in self.parser.cards],
            [i["data-reviewed"] for i in self.parser.inputs])

    def test_filter_covers_every_role_and_each_card_has_a_role(self):
        options = set(re.findall(r'<option value="([^"]+)">', GUIDE))
        self.assertEqual(options, {"all", "presales", "delivery", "architect",
                                    "developer", "approver", "scanner", "ai",
                                    "deployer", "operations"})
        for card in self.parser.cards:
            roles = set(card["data-roles"].split())
            self.assertTrue(roles)
            self.assertTrue(roles.issubset(options - {"all"}))

    def test_accessibility_and_mobile_layout(self):
        self.assertEqual(len(self.parser.ids), len(set(self.parser.ids)))
        for needed in ('id="persona-role"', 'for="persona-role"',
                       'id="persona-count"', 'role="status"', 'aria-live="polite"',
                       'id="persona-reset"', 'id="persona-export"',
                       '@media(max-width:720px)', 'input type="checkbox"'):
            self.assertIn(needed, GUIDE)
        self.assertIn('card.hidden=!matches', GUIDE)
        self.assertIn('role.addEventListener("change",render)', GUIDE)

    def test_version_pinned_truth_and_training_scope(self):
        for phrase in ("SOURCE-ONLY", "19 October 2026", "4.22.2",
                       "6 October 2026", "DEV-REPORTED", "NOT RUN", "HOLD",
                       "not independently", "no original screenshots"):
            self.assertIn(phrase.lower(), GUIDE.lower())
        self.assertIn("production_verified=false", GUIDE)
        self.assertIn("screenshot_approved=false", GUIDE)
        self.assertIn("REVIEWED ONLY", GUIDE)
        self.assertIn('delivery-workbench-rehearsal-hold.txt', GUIDE)

    def test_no_private_links_pixels_or_network_dependencies(self):
        for sensitive in ("drive.google.com", "docs.google.com",
                          "github.com/emilebennetts-cmd/solution-lifecycle-studio",
                          "servicenow-portfolio-control", "dev438211",
                          "<img", "<iframe", "<svg", "fetch(", "XMLHttpRequest",
                          "sendBeacon", "localStorage", "https://", "Bearer "):
            self.assertNotIn(sensitive, GUIDE)
        self.assertIn('href="workbench-acceptance-playbook.html"', GUIDE)
        self.assertIn('href="evidence-methodology.html"', GUIDE)

    def test_original_synthetic_plan_lab_is_preserved(self):
        self.assertIn('id="plan-tabs"', HTML)
        self.assertIn('id="doc-export"', HTML)
        self.assertIn('<section aria-labelledby="architecture">', HTML)


if __name__ == "__main__":
    unittest.main()

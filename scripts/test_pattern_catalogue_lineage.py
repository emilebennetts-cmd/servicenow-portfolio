"""Offline assertions for the dated, client-neutral pattern catalogue reconciliation.

Picked up by .github/workflows/portfolio-quality.yml. This is static site
integrity only: never a native ServiceNow validation result.
"""
from __future__ import annotations

from html.parser import HTMLParser
from pathlib import Path
import unittest

SITE = Path(__file__).resolve().parents[1]
PAGE = SITE / "pattern-library.html"


class LineageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.snapshots: list[str] = []
        self.lenses: list[tuple[str, str]] = []
        self.ids: set[str] = set()
        self.hrefs: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = dict(attrs)
        if "id" in attr:
            self.ids.add(attr["id"])
        if tag == "article" and "data-snapshot" in attr:
            self.snapshots.append(attr["data-snapshot"])
        if tag == "button" and "data-lens" in attr:
            self.lenses.append((attr["data-lens"], attr.get("aria-pressed", "")))
        if tag == "a" and attr.get("href"):
            self.hrefs.append(attr["href"])


class PatternCatalogueLineageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.html = PAGE.read_text(encoding="utf-8")
        cls.parser = LineageParser()
        cls.parser.feed(cls.html)

    def test_three_dated_snapshots_and_accessible_filter(self) -> None:
        self.assertEqual(self.parser.snapshots, ["sep", "oct", "nov"])
        self.assertEqual(
            self.parser.lenses,
            [("all", "true"), ("sep", "false"), ("oct", "false"), ("nov", "false")],
        )
        self.assertIn("catalogue-lineage", self.parser.ids)
        self.assertIn("lineage-feedback", self.parser.ids)
        self.assertIn("evidence-and-provenance", self.parser.ids)
        self.assertIn('role="status" aria-live="polite"', self.html)
        self.assertIn("card.hidden=lens", self.html)
        self.assertNotIn('class="lineage-card" data-snapshot="sep" hidden', self.html)

    def test_distinct_inventory_units_and_generated_ratio(self) -> None:
        for value in ("96", "4,595", "11,000", "2,234", "7,600", "20 archetypes"):
            with self.subTest(value=value):
                self.assertIn(value, self.html)
        self.assertAlmostEqual(7600 / 11000 * 100, 69.1, places=1)
        self.assertIn("69.1%", self.html)
        self.assertIn("not a defect rate", self.html)
        self.assertIn("must not be added together", self.html)

    def test_current_source_not_promoted_from_historical_dev(self) -> None:
        for label in ("4.15.0", "0.2.0", "4.20.0", "4.22.2",
                      "DEV-REPORTED", "SOURCE-ONLY", "PRODUCTION-VERIFIED"):
            with self.subTest(label=label):
                self.assertIn(label, self.html)
        self.assertIn("Later source cannot inherit earlier DEV receipts.", self.html)
        self.assertIn("No new DEV-VERIFIED or PRODUCTION-VERIFIED", self.html)
        self.assertIn("Live Chrome interaction was <em>not verified</em>", self.html)

    def test_provenance_and_publication_boundary(self) -> None:
        self.assertIn(
            "https://github.com/emilebennetts-cmd/solution-lifecycle-studio/blob/main/docs/releases/catalogue-11000-20261003.md",
            self.parser.hrefs,
        )
        self.assertIn(
            "https://github.com/emilebennetts-cmd/solution-lifecycle-studio/blob/main/README.md",
            self.parser.hrefs,
        )
        self.assertIn("#evidence-and-provenance", self.parser.hrefs)
        self.assertNotIn("dev438211.service-now.com", self.html)
        self.assertNotIn("servicenow-portfolio-control", self.html)
        self.assertNotRegex(self.html, r"<img\b")
        self.assertNotIn("genuine screenshot publication is approved", self.html.lower())

    def test_no_new_network_requirements(self) -> None:
        self.assertNotRegex(self.html, r"<script\s+src=")
        self.assertNotIn("fetch(", self.html)
        self.assertNotIn("XMLHttpRequest", self.html)


if __name__ == "__main__":
    unittest.main()

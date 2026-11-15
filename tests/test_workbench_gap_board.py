"""Workbench source-to-DEV board stays indexed, source-bound and fail closed."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "workbench-source-dev-gap-board.html"


class WorkbenchGapBoardTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PAGE.read_text(encoding="utf-8")

    def test_navigation_and_canonical_discovery(self):
        for filename in ("index.html", "portfolio-explorer.html", "sitemap.xml"):
            with self.subTest(filename=filename):
                text = (ROOT / filename).read_text(encoding="utf-8")
                self.assertIn("workbench-source-dev-gap-board.html", text)
        self.assertIn('rel="canonical"', self.html)
        self.assertIn('id="main"', self.html)

    def test_non_certifying_provenance(self):
        for marker in ("4.6.1", "4.5.1", "4.20.0", "4.22.2", "0.1.0",
                       "SOURCE-ONLY", "DEV-REPORTED", "NOT RUN", "HOLD",
                       "30 SEP 2026", "5 OCT 2026", "No genuine ServiceNow screenshots"):
            with self.subTest(marker=marker):
                self.assertIn(marker.lower(), self.html.lower())
        self.assertNotRegex(self.html, r"<(?:img|iframe|picture)\\b")
        self.assertNotIn("servicenow-portfolio-control", self.html)

    def test_later_asbuilt_conflict_remains_held(self):
        for marker in ('id="asbuilt-conflict"', '6 OCT 2026', '19 OCT 2026',
                       '0.4.2', 'not represented as installed', 'DEV-REPORTED',
                       'conflict open', 'id="lineage-download"', 'buildLineageCsv',
                       '"NOT RUN","HOLD"', 'independent_reviewer'):
            with self.subTest(marker=marker):
                self.assertIn(marker.lower(), self.html.lower())
        self.assertNotIn('drive.google.com/file/d/', self.html)
        self.assertNotIn('docs.google.com/document/d/', self.html)

    def test_twelve_unique_native_controls(self):
        matches = re.findall(r'<article class="gate" data-group="([^"]+)" aria-labelledby="gate-([^"]+)"', self.html)
        self.assertEqual(len(matches), 12)
        self.assertEqual(len(set(code for _, code in matches)), 12)
        self.assertEqual([sum(group == x for group, _ in matches) for x in
                          ("Delivery", "Diagnostic", "Cross-workbench")], [5, 4, 3])

    def test_offline_export_boundary(self):
        for marker in ("Content-Security-Policy", "connect-src 'none'", "img-src 'none'",
                       "URL.revokeObjectURL(url)", '"NOT RUN","HOLD","SOURCE-ONLY"',
                       "independent_reviewer"):
            self.assertIn(marker, self.html)
        self.assertNotIn("localStorage", self.html)
        self.assertNotIn("XMLHttpRequest", self.html)


if __name__ == "__main__":
    unittest.main()

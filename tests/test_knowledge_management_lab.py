"""Knowledge Management public lab: source-safe and fail-closed browser contract."""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "knowledge-management-implementation-lab.html"
JS = ROOT / "knowledge-management-implementation-lab.js"

class KnowledgeManagementLab(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.page = HTML.read_text(encoding="utf-8")
        cls.script = JS.read_text(encoding="utf-8")

    def test_accessibility_and_mobile_policy(self):
        for marker in ('lang="en"', 'id="main"', 'aria-live="polite"',
                       'aria-pressed="true"', '@media(max-width:480px)',
                       'prefers-reduced-motion', "script-src 'self'",
                       "connect-src 'none'", "img-src 'none'",
                       "form-action 'none'", 'id="export-all"'):
            with self.subTest(marker=marker):self.assertIn(marker, self.page)
        self.assertIn('src="knowledge-management-implementation-lab.js"', self.page)
        self.assertNotRegex(self.page, r'<(?:img|iframe|canvas|picture)\b')
        self.assertNotRegex(self.page, r'<script[^>]*>\s*[^<\s]')
        for banned in ("localStorage", "sessionStorage", "fetch(", "innerHTML", "XMLHttpRequest"):
            self.assertNotIn(banned, self.script)

    def test_native_boundary_and_prerequisites(self):
        for marker in ("kb_knowledge", "Knowledge Management Advanced",
                       "Can Read", "Can Contribute", "user criteria",
                       "MOCK-ONLY", "SOURCE-ONLY", "DEV-REPORTED",
                       "DEV-VERIFIED", "PRODUCTION-VERIFIED", "NOT RUN",
                       "HOLD", "No genuine ServiceNow screenshots",
                       "no ServiceNow licence"):
            with self.subTest(marker=marker):
                self.assertIn(marker.lower(), self.page.lower())

    def test_24_unique_gates_and_fail_closed_csv(self):
        ids = re.findall(r'\["(KN-[ART]\d\d)"', self.script)
        self.assertEqual(len(ids),24)
        self.assertEqual(len(set(ids)),24)
        for marker in ('native:"NOT RUN"', 'release:"HOLD"',
                       'classification:"MOCK-ONLY"', 'allCsv(marks)',
                       'URL.revokeObjectURL(url)'):
            self.assertIn(marker,self.script)
        self.assertNotIn('DEV-VERIFIED"', self.script)
        self.assertNotIn('PRODUCTION-VERIFIED"', self.script)

if __name__=="__main__":
    unittest.main()

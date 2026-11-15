"""Static, privacy and accessibility contract for the public Request Management lab."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "request-management-implementation-lab.html"
SCRIPT = ROOT / "request-management-implementation-lab.js"

class RequestManagementLabTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PAGE.read_text(encoding="utf-8")
        cls.js = SCRIPT.read_text(encoding="utf-8")

    def test_native_design_and_privacy_labels(self):
        for name in ("sc_cat_item", "sc_request", "sc_req_item", "sc_task",
                     "Workflow Studio", "user criteria", "separation of duties",
                     "MOCK-ONLY", "SOURCE-ONLY", "DEV-REPORTED",
                     "DEV-VERIFIED", "PRODUCTION-VERIFIED", "NOT RUN",
                     "HOLD", "No genuine ServiceNow screenshots",
                     "No browser storage", "no ServiceNow licence"):
            with self.subTest(name=name):
                self.assertIn(name, self.html)

    def test_accessible_responsive_without_external_images_or_scripts(self):
        for snippet in ('lang="en"', 'id="main"', 'aria-live="polite"',
                        'aria-pressed="true"', 'role="group"',
                        '@media(max-width:480px)', "connect-src 'none'",
                        "img-src 'none'", 'script-src &#39;self&#39;'):
            if snippet == 'script-src &#39;self&#39;':
                self.assertIn("script-src 'self'", self.html)
            else:
                self.assertIn(snippet, self.html)
        self.assertNotRegex(self.html, r"<(?:img|iframe|canvas)\b")
        self.assertNotRegex(self.html, r"<script[^>]*>\s*[^<\s]")
        self.assertIn('src="request-management-implementation-lab.js"', self.html)
        self.assertNotIn("localStorage", self.js)
        self.assertNotIn("sessionStorage", self.js)
        self.assertNotIn("fetch(", self.js)
        self.assertNotIn("innerHTML", self.js)

    def test_export_cannot_auto_certify_native_service_now(self):
        for marker in ('native:"NOT RUN"', 'release:"HOLD"', 'classification:"MOCK-ONLY"',
                       'acceptanceCsv(current,read.get(current))',
                       'URL.createObjectURL', 'URL.revokeObjectURL'):
            self.assertIn(marker, self.js)
        self.assertEqual(len(re.findall(r'\["(?:ACC|HW|SRV)-\d\d"', self.js)), 24)

if __name__ == "__main__":
    unittest.main()

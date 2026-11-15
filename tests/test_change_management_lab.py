"""Static regression contracts for the public Change Management rehearsal.

These tests inspect authored HTML/JS; they do NOT validate browser execution,
ServiceNow configuration, ATF, approvals, or any customer change record.
"""
from pathlib import Path
import re
import unittest

PAGE = Path(__file__).resolve().parents[1] / "change-management-implementation-lab.html"


class ChangeManagementLabContracts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PAGE.read_text(encoding="utf-8")

    def test_three_distinct_native_model_rehearsals(self):
        self.assertIn("data-model=\"normal\"", self.html)
        self.assertIn("data-model=\"standard\"", self.html)
        self.assertIn("data-model=\"emergency\"", self.html)
        for name, next_name in (("normal", "standard"), ("standard", "emergency"),
                                ("emergency", "let current")):
            start = self.html.index(name + ":{title:")
            end = self.html.index(next_name + (":{title:" if name != "emergency" else ""), start + 1)
            block = self.html[start:end]
            self.assertEqual(block.count("['"), 7, name + " requires seven reviewed design controls")

    def test_exports_fail_closed_even_after_reading_marks(self):
        self.assertIn("'NOT RUN','HOLD','MOCK-ONLY'", self.html)
        self.assertIn("Native acceptance NOT RUN · HOLD", self.html)
        self.assertIn("no gate has passed", self.html)
        self.assertIn("read=new Set();render()", self.html)
        self.assertIn("acceptance-HOLD.csv", self.html)

    def test_local_only_and_data_minimisation(self):
        self.assertIn("connect-src 'none'", self.html)
        self.assertIn("form-action 'none'", self.html)
        self.assertIn("img-src 'none'", self.html)
        self.assertNotRegex(self.html, r"<script[^>]+src=")
        self.assertNotRegex(self.html, r"\\bfetch\\s*\\(")
        self.assertIn("No user data is collected or transmitted.", self.html)

    def test_responsive_accessible_and_evidence_boundaries(self):
        self.assertIn('aria-pressed="true"', self.html)
        self.assertIn('aria-live="polite"', self.html)
        self.assertIn("@media(max-width:480px)", self.html)
        self.assertIn("Historical DEV descriptions are", self.html)
        self.assertIn("No new DEV-VERIFIED or PRODUCTION-VERIFIED", self.html)
        self.assertIn("ITSM/Change Management entitlement", self.html)


if __name__ == "__main__":
    unittest.main()

"""Regression tests for evidence classification and public provenance policy."""
import json
import tempfile
import unittest
from pathlib import Path

from check_verification_register import REGISTER, ROOT, validate


class VerificationRegisterTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(REGISTER.read_text(encoding="utf-8"))

    def test_current_register(self):
        self.assertEqual(validate(self.data, ROOT), [])

    def test_duplicate_claim_rejected(self):
        self.data["items"].append(dict(self.data["items"][0]))
        self.assertTrue(any("duplicate" in error for error in validate(self.data)))

    def test_unsupported_classification_rejected(self):
        self.data["items"][0]["classification"] = "production-ready"
        self.assertTrue(any("invalid classification" in error for error in validate(self.data)))

    def test_unverified_promotion_rejected(self):
        self.data["items"][0]["classification"] = "production-verified"
        self.assertTrue(any("dated evidence" in error for error in validate(self.data)))

    def test_path_traversal_rejected(self):
        self.data["items"][0]["page"] = "../private/notes.html"
        self.assertTrue(any("unsafe case-study page" in error for error in validate(self.data)))

    def test_missing_case_study_rejected(self):
        self.data["items"][0]["page"] = "missing-portfolio-case-study.html"
        self.assertTrue(any("missing or unsafe" in error for error in validate(self.data)))


    def test_future_verification_rejected(self):
        entry = self.data["items"][0]
        entry.update(classification="DEV-verified", verification_date="2999-01-01",
                     verification_reference="https://example.org/evidence")
        self.assertTrue(any("future" in error for error in validate(self.data)))

    def test_insecure_evidence_reference_rejected(self):
        entry = self.data["items"][0]
        entry.update(classification="DEV-verified", verification_date="2026-09-30",
                     verification_reference="http://example.org/evidence")
        self.assertTrue(any("HTTPS" in error for error in validate(self.data)))

    def test_production_authorisation_required(self):
        entry = self.data["items"][0]
        entry.update(classification="production-verified", verification_date="2026-09-30",
                     verification_reference="https://example.org/evidence")
        self.assertTrue(any("authorisation" in error for error in validate(self.data)))

    def test_non_html_evidence_page_rejected(self):
        self.data["items"][0]["page"] = "evidence/public-verification-register.json"
        self.assertTrue(any("unsafe case-study" in error for error in validate(self.data)))

if __name__ == "__main__":
    unittest.main()

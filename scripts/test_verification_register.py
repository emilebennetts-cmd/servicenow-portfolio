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


if __name__ == "__main__":
    unittest.main()

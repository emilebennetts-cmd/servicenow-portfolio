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


    def verified_fixture(self, classification="DEV-verified"):
        """Synthetic, complete metadata; this is NOT a real verification claim."""
        claim = dict(self.data["items"][0])
        claim.update(
            classification=classification,
            verification_date="2026-11-12",
            verification_reference="https://example.org/illustrative-review-only",
            source_commit_sha="a" * 40,
            installed_version="4.22.2",
            application_scope="x_1577958_vdf",
            execution_environment="PROD" if classification == "production-verified" else "DEV",
            environment_alias="SANDBOX_DEV_01",
            executed_test_ids=["A01", "A02"],
            evidence_receipt_alias="NATIVE_REVIEW_001",
            independent_review_approved=True,
        )
        if classification == "production-verified":
            claim["production_authorisation"] = "SYNTHETIC_CHANGE_001"
        self.data["items"][0] = claim
        return claim

    def test_complete_native_metadata_contract(self):
        self.verified_fixture()
        self.assertEqual(validate(self.data, ROOT), [])

    def test_native_claim_missing_build_identity_is_rejected(self):
        for field in ("source_commit_sha", "installed_version", "application_scope",
                      "execution_environment", "environment_alias", "executed_test_ids",
                      "evidence_receipt_alias", "independent_review_approved"):
            with self.subTest(field=field):
                self.setUp()
                self.verified_fixture().pop(field)
                self.assertTrue(validate(self.data, ROOT), field)

    def test_native_claim_wrong_environment_and_unsafe_receipts_rejected(self):
        claim = self.verified_fixture()
        claim["execution_environment"] = "PROD"
        self.assertTrue(any("execution_environment DEV" in e for e in validate(self.data, ROOT)))
        claim["execution_environment"] = "DEV"
        claim["environment_alias"] = "https://internal-instance.example"
        self.assertTrue(any("environment alias" in e for e in validate(self.data, ROOT)))
        claim["environment_alias"] = "SANDBOX_DEV_01"
        claim["evidence_receipt_alias"] = "../private"
        self.assertTrue(any("receipt alias" in e for e in validate(self.data, ROOT)))

    def test_native_claim_duplicate_tests_and_short_sha_rejected(self):
        claim = self.verified_fixture()
        claim["executed_test_ids"] = ["A01", "A01"]
        self.assertTrue(any("unique executed test" in e for e in validate(self.data, ROOT)))
        claim["executed_test_ids"] = ["A01", "A02"]
        claim["source_commit_sha"] = "abc1234"
        self.assertTrue(any("full lowercase source commit" in e for e in validate(self.data, ROOT)))

    def test_production_claim_requires_prod_baseline_and_authorisation(self):
        claim = self.verified_fixture("production-verified")
        self.assertEqual(validate(self.data, ROOT), [])
        claim["execution_environment"] = "DEV"
        self.assertTrue(any("execution_environment PROD" in e for e in validate(self.data, ROOT)))
        claim["execution_environment"] = "PROD"
        claim.pop("production_authorisation")
        self.assertTrue(any("authorisation" in e for e in validate(self.data, ROOT)))

if __name__ == "__main__":
    unittest.main()

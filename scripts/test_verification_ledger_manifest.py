"""Keep the public reviewer ledger, claim manifest and safety boundaries aligned.

This contract is run by the GitHub Portfolio quality workflow. It neither
accesses private repositories nor executes against a ServiceNow instance.
"""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / "verification-ledger.html").read_text(encoding="utf-8")
REGISTER = json.loads((ROOT / "evidence/public-verification-register.json").read_text(encoding="utf-8"))
REQUIRED = {
    "DELIVERY", "DELIVERY-DEV", "DIAGNOSTIC", "KNOWLEDGE",
    "EXTERNAL-INTEGRATIONS", "HANDOFF", "CMDB-IRE-ASSURANCE",
    "ITSM-GREENFIELD", "CMDB-TRUST-LAB", "MIM-READINESS-LAB",
    "VISUAL-REVIEWS", "REDACTION-DESK", "RECEIPT-VERIFIER",
    "REVIEW-PACKET", "CMDB-SOURCE-ONBOARDING", "DIAGNOSTIC-COVERAGE",
    "KI-ACCEPTANCE-MATRIX", "PATTERN-LIBRARY-AUDIT", "OPERATIONS-READINESS",
    "INCIDENT-PACK-PILOT", "SCOPE-COMPATIBILITY",
}


class LedgerManifestTests(unittest.TestCase):
    def test_complete_catalogue_has_public_pages(self):
        items = REGISTER["items"]
        ids = [item["id"] for item in items]
        self.assertEqual(len(ids), len(set(ids)), "Duplicate evidence claim IDs must fail closed")
        self.assertTrue(REQUIRED.issubset(set(ids)),
                        f"Missing baseline claims: {sorted(REQUIRED - set(ids))}")
        # The ledger is append-only. New claims must be validated, not rejected
        # merely for extending the catalogue (CI regression 2026-11-13).
        classifications = {item["id"]: item["classification"] for item in items}
        self.assertEqual("DEV-reported", classifications["INCIDENT-PACK-PILOT"])
        self.assertEqual("source-only", classifications["SCOPE-COMPATIBILITY"])
        for item in items:
            with self.subTest(item=item["id"]):
                self.assertTrue((ROOT / item["page"]).is_file())
                self.assertNotIn("production-verified", item["classification"].lower())
                self.assertNotEqual(item["classification"], "DEV-verified")
                self.assertTrue(item["runtime_verification"])
                self.assertTrue(item["public_screenshot_status"])

    def test_synthetic_labs_never_claim_native_service_now_acceptance(self):
        classes = {item["id"]: item["classification"] for item in REGISTER["items"]}
        for key in ("ITSM-GREENFIELD", "CMDB-TRUST-LAB", "MIM-READINESS-LAB", "CMDB-SOURCE-ONBOARDING", "KI-ACCEPTANCE-MATRIX"):
            self.assertEqual("mock-only", classes[key])
        self.assertEqual("source-only", classes["VISUAL-REVIEWS"])
        self.assertIn("HOLD", next(item["public_screenshot_status"] for item in REGISTER["items"]
                                   if item["id"] == "VISUAL-REVIEWS"))

    def test_ledger_uses_public_json_not_injected_external_source(self):
        self.assertIn("fetch('evidence/public-verification-register.json'", HTML)
        self.assertIn("textContent=item.title", HTML)
        self.assertIn("dd.textContent=value", HTML)
        self.assertNotIn("innerHTML", HTML)
        self.assertNotIn("drive.google.com", HTML)
        self.assertNotIn("servicenow-portfolio-control", HTML)
        self.assertNotIn("<img ", HTML)
        for name in ("records", "search", "count", "reset", "load-error"):
            self.assertIn('id="' + name + '"', HTML)

    def test_default_evidence_posture_is_explicit(self):
        for wording in ("No production verification", "zero", "0", "SOURCE-ONLY",
                        "MOCK-ONLY", "HOLD", "require no ServiceNow licence"):
            self.assertIn(wording.lower(), HTML.lower())


if __name__ == "__main__":
    unittest.main()

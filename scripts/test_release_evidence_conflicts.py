#!/usr/bin/env python3
"""Public release-claim provenance regression: source is not runtime acceptance."""
import re
import unittest
from html import unescape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REL = (ROOT / "delivery-release-evolution.html").read_text(encoding="utf-8")
DIAG = (ROOT / "diagnostic-workbench-case-study.html").read_text(encoding="utf-8")

class ReleaseClaimEvidenceBoundary(unittest.TestCase):
    def test_multiple_dated_baselines_are_preserved_without_upgrading_evidence(self):
        for marker in (
            'id="release-evidence-reconciliation"',
            "4.22.2", "4.20.0", "5 October 2026", "6 October 2026",
            "19 October", "DEV-REPORTED", "SOURCE-ONLY", "PRODUCTION-VERIFIED",
            "Release decision: HOLD.", "not a DEV install",
            "no new DEV-VERIFIED", "screenshot publication HOLD",
        ):
            with self.subTest(marker=marker):
                self.assertIn(marker.lower(), REL.lower())
        self.assertIn("not represented as installed", REL)
        self.assertIn("document-reported observation only", REL.lower())
        self.assertNotIn("drive.google.com/file/d/", REL)
        self.assertNotIn("docs.google.com/document/d/", REL)
        self.assertNotIn("servicenow-portfolio-control", REL)

    def test_diagnostic_historical_receipt_never_calls_itself_dev_verified(self):
        summaries = [unescape(re.sub(r"<[^>]+>", "", s)) for s in
                     re.findall(r"<summary\b[^>]*>(.*?)</summary>", DIAG, re.S | re.I)]
        self.assertTrue(any("DEV-REPORTED" in s and "historical" in s for s in summaries))
        self.assertFalse(any("DEV-VERIFIED" in s and "historical" in s for s in summaries))
        self.assertIn('delivery-release-evolution.html#release-evidence-reconciliation', DIAG)
        self.assertIn("not independently repeated tests", DIAG)

    def test_site_does_not_expose_originals_or_certify_runtime(self):
        self.assertNotIn("<img ", REL.lower())
        self.assertNotIn("fetch(", REL.lower())
        self.assertNotIn("localstorage", REL.lower())
        self.assertNotIn("service_now_execution:true", REL.lower())
        self.assertIn("Licensing and entitlements", REL)
        self.assertIn("no current target or package-identity receipt", REL.lower())

if __name__ == "__main__":
    unittest.main()

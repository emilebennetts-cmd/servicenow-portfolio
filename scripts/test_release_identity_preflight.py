#!/usr/bin/env python3
"""Static safety contract for the offline Delivery source-to-target preflight."""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / "delivery-release-evolution.html").read_text(encoding="utf-8")

class ReleaseIdentityPreflightContract(unittest.TestCase):
    def test_identity_and_non_certification(self):
        for required in (
            'id="release-identity-preflight"', 'id="target-scope"',
            'id="target-version"', 'id="preflight-export"',
            'x_1577958_vdf', '4.22.2', '4.20.0', 'x_eitsp_vdf',
            'TEXT MATCH · NOT VERIFIED', 'MISMATCH', 'INVALID INPUT',
            'release_decision:"HOLD"', 'native_execution:"NOT RUN"',
            'independent_dev_verified:false', 'production_verified:false',
            'target_package_hash_verified:false', 'image_publication_approved:false',
            'observed_values_included:false', 'approval_status:"UNREVIEWED"',
            'id="preflight-status"', 'aria-live="polite"',
        ):
            with self.subTest(required=required):
                self.assertIn(required, HTML)
        self.assertIn('MOCK-ONLY', HTML)
        self.assertIn('SOURCE-ONLY', HTML)

    def test_no_private_values_in_export_or_network(self):
        block = HTML.split('/* Release preflight is intentionally offline, non-certifying and value-redacting. */', 1)[1]
        self.assertNotIn("fetch(", block)
        self.assertNotIn("localStorage", block)
        self.assertNotIn("XMLHttpRequest", block)
        self.assertNotIn("sendBeacon", block)
        self.assertNotIn("sessionStorage", block)
        self.assertNotIn("JSON.stringify({scope:scope.value", block)
        packet = block.split("const packet={", 1)[1].split("};", 1)[0]
        self.assertNotIn("scope.value", packet)
        self.assertNotIn("version.value", packet)
        self.assertIn("comparison_results:result", packet)
        for prohibited in ("drive.google.com/file/d/", "docs.google.com/document/d/",
                           "servicenow-portfolio-control", "token="):
            self.assertNotIn(prohibited, HTML)
        self.assertNotIn("<img ", HTML.lower())

    def test_source_not_live_runtime(self):
        self.assertIn("An exact text match does not authenticate", HTML)
        self.assertIn("HOLD — labels align, runtime unverified", HTML)
        self.assertIn("not a ServiceNow connector", HTML)
        self.assertIn("No instance credentials", HTML)
        self.assertIn("Licensing and entitlements", HTML)

if __name__ == "__main__":
    unittest.main()

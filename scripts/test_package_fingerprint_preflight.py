#!/usr/bin/env python3
"""Contract checks for the browser-local package fingerprint gate (not native evidence)."""
import unittest
from pathlib import Path

PAGE = (Path(__file__).resolve().parents[1] / "delivery-release-evolution.html").read_text(encoding="utf-8")

class PackageFingerprintContract(unittest.TestCase):
    def test_user_controls_and_trust_boundary(self):
        for phrase in (
            'id="package-fingerprint"', 'id="package-file"',
            'id="expected-package-sha"', 'id="fingerprint-run"',
            'id="fingerprint-copy"', 'id="fingerprint-clear"',
            'id="fingerprint-status"', 'aria-live="polite"',
            'SHA-256', '25 MiB', 'independently obtained',
            'HASH MATCH — NOT VERIFIED', 'HASH MISMATCH',
            'DIGEST ONLY — NO TRUSTED REFERENCE', 'FILE TOO LARGE',
            'NOT RUN', 'HOLD', 'not a ServiceNow',
        ):
            with self.subTest(phrase=phrase):
                self.assertIn(phrase.lower(), PAGE.lower())

    def test_local_digest_and_redacted_export(self):
        block = PAGE.split("/* This review never uploads, persists or exports file contents, names or digests. */", 1)[1]
        for required in (
            'crypto.subtle.digest("SHA-256",buffer)',
            'file.arrayBuffer()', 'file.size>25*1024*1024',
            'fingerprintSequence', 'invalidateFingerprint',
            'local_package_fingerprint_status:fingerprintState',
            'package_file_bytes_included:false',
            'package_filename_included:false',
            'package_digests_included:false',
            'target_package_hash_verified:false',
            'independent_dev_verified:false',
            'production_verified:false',
            'release_decision:"HOLD"',
        ):
            with self.subTest(required=required):
                self.assertIn(required, block)
        packet = block.split("const packet={", 1)[1].split("};", 1)[0]
        for forbidden in (
            "computedDigest", "localFile.files", "file.name", "file.arrayBuffer",
            "trustedHash.value", "buffer", "reference.toLowerCase()"
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, packet)
        for forbidden in ("fetch(", "XMLHttpRequest", "sendBeacon", "localStorage", "sessionStorage"):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, block)

if __name__ == "__main__":
    unittest.main()

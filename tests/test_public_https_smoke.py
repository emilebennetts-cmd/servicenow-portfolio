#!/usr/bin/env python3
"""Offline contracts for public URL smoke and non-certifying receipts."""
import json
import hashlib
import os
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import check_public_https as smoke


class PublicHttpsSmokeTests(unittest.TestCase):
    def test_requires_same_https_origin_200_html_and_expected_marker(self):
        url = smoke.BASE + "visual-evidence.html"
        raw = b'<html><div id="gallery"></div></html>'
        smoke.validate_response(url, url, 200, "text/html; charset=utf-8", raw, 'id="gallery"')
        failures = [
            (url.replace("https:", "http:"), 200, "text/html", raw),
            ("https://external.example/visual-evidence.html", 200, "text/html", raw),
            (smoke.BASE, 200, "text/html", raw),
            (url, 404, "text/html", raw),
            (url, 200, "application/json", raw),
            (url + "?debug=true", 200, "text/html", raw),
            (url + "#gallery", 200, "text/html", raw),
            (url.replace("github.io", "github.io:443"), 200, "text/html", raw),
            (url.replace("https://", "https://reviewer@"), 200, "text/html", raw),
            (url, 200, "text/html-injected", raw),
            (url, 200, "text/html", b"<html></html>"),
            (url, 200, "text/html", b"\xff"),
        ]
        for final, code, mime, body in failures:
            with self.subTest(final=final, code=code, mime=mime):
                with self.assertRaises((ValueError, UnicodeError)):
                    smoke.validate_response(url, final, code, mime, body, 'id="gallery"')

    def test_exact_deployed_bytes_rejects_stale_content_with_valid_marker(self):
        url = smoke.BASE + "visual-evidence.html"
        current = b'<html><div id="gallery">new release</div></html>'
        stale = b'<html><div id="gallery">old release</div></html>'
        expected_sha256 = hashlib.sha256(current).hexdigest()
        smoke.validate_response(url, url, 200, "text/html", current,
                                'id="gallery"', expected_sha256=expected_sha256)
        with self.assertRaisesRegex(ValueError, "bytes differ"):
            smoke.validate_response(url, url, 200, "text/html", stale,
                                    'id="gallery"', expected_sha256=expected_sha256)

    def test_exact_deployed_receipt_requires_every_route_match(self):
        with tempfile.TemporaryDirectory() as directory:
            original = Path.cwd()
            try:
                os.chdir(directory)
                rows = [{"route": name, "status": "PASS", "http_status": 200,
                         "url": smoke.BASE if name == "index.html" else smoke.BASE + name,
                         "bytes_match_checkout": True,
                         "sha256": hashlib.sha256(name.encode()).hexdigest()}
                        for name in smoke.TARGETS]
                smoke.write_summary(rows, True, "live")
                doc = json.loads(Path(smoke.RECEIPT).read_text())
                self.assertTrue(doc["verified_exact_deployed_bytes"])
                self.assertFalse(doc["native_dev_verified"])
                self.assertFalse(doc["production_servicenow_verified"])
                self.assertFalse(doc["screenshot_publication_approved"])
                rows[0]["bytes_match_checkout"] = False
                smoke.write_summary(rows, True, "live")
                doc = json.loads(Path(smoke.RECEIPT).read_text())
                self.assertFalse(doc["verified_exact_deployed_bytes"])
                rows[0]["bytes_match_checkout"] = True
                rows[0]["route"] = rows[1]["route"]
                smoke.write_summary(rows, True, "live")
                doc = json.loads(Path(smoke.RECEIPT).read_text())
                self.assertFalse(doc["verified_exact_deployed_bytes"])
                rows[0]["route"] = next(iter(smoke.TARGETS))
                rows[0]["status"] = "UNCONFIRMED"
                smoke.write_summary(rows, True, "live")
                doc = json.loads(Path(smoke.RECEIPT).read_text())
                self.assertFalse(doc["verified_exact_deployed_bytes"])
                rows[0]["status"] = "PASS"
                smoke.write_summary(rows, True, "local")
                doc = json.loads(Path(smoke.RECEIPT).read_text())
                self.assertFalse(doc["verified_exact_deployed_bytes"])
            finally:
                os.chdir(original)


    def test_live_receipts_fail_closed_for_missing_routes_or_forged_http_metadata(self):
        with tempfile.TemporaryDirectory() as directory:
            original = Path.cwd()
            try:
                os.chdir(directory)
                rows = [
                    {"route": name, "status": "PASS", "http_status": 200,
                     "url": smoke.BASE if name == "index.html" else smoke.BASE + name,
                     "bytes_match_checkout": True,
                     "sha256": hashlib.sha256(name.encode()).hexdigest()}
                    for name in smoke.TARGETS
                ]
                def verify(records, expected_live, expected_exact):
                    smoke.write_summary(records, True, "live")
                    receipt = json.loads(Path(smoke.RECEIPT).read_text())
                    self.assertIs(receipt["verified_live_public_website"], expected_live)
                    self.assertIs(receipt["verified_exact_deployed_bytes"], expected_exact)
                verify(rows, True, True)
                verify(rows[:-1], False, False)
                cases = [
                    ("http_status", 302),
                    ("url", "https://another.example/"),
                    ("url", smoke.BASE + "wrong.html"),
                    ("status", "UNCONFIRMED"),
                    ("bytes_match_checkout", False),
                    ("sha256", "not-a-sha256-digest"),
                ]
                for field, invalid in cases:
                    with self.subTest(field=field):
                        altered = [dict(row) for row in rows]
                        altered[0][field] = invalid
                        # A digest/byte mismatch blocks exact identity, while
                        # genuine HTTP delivery can still be separately true.
                        delivery = field in ("bytes_match_checkout", "sha256")
                        verify(altered, delivery, False)
                duplicated = [dict(row) for row in rows]
                duplicated[0]["route"] = duplicated[1]["route"]
                verify(duplicated, False, False)
                verify(rows, True, True)
            finally:
                os.chdir(original)

    def test_local_fixture_markers_and_fail_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name, marker in smoke.TARGETS.items():
                (root / name).write_text(f"<html>{marker}</html>", encoding="utf-8")
            result = smoke.local_check(root)
            self.assertEqual(len(result), 14)
            self.assertTrue(all(r["verification"] == "LOCAL-ONLY" for r in result))
            (root / "index.html").write_text("<html></html>", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "required marker missing"):
                smoke.local_check(root)

    def test_release_route_set_covers_core_consulting_journey(self):
        expected = {
            "index.html", "delivery-release-evolution.html",
            "diagnostic-workbench-case-study.html", "visual-evidence.html",
            "delivery-case-study.html", "reusable-delivery-patterns-case-study.html",
            "diagnostic-delivery-handoff-contract.html", "cmdb-ire-assurance.html",
            "itsm-greenfield-build-sequencer.html", "ki-matrix-intake.html",
            "technical-evidence-register.html", "portfolio-review-guide.html",
            "problem-management-implementation-lab.html",
            "incident-management-implementation-lab.html",
        }
        self.assertEqual(set(smoke.TARGETS), expected)

    def test_local_receipt_never_promotes_native_claims(self):
        with tempfile.TemporaryDirectory() as directory:
            original = Path.cwd()
            try:
                os.chdir(directory)
                with patch.dict(os.environ, {"GITHUB_SHA": "source-hash"}, clear=False):
                    smoke.write_summary([{"route": "index.html", "status": "PASS"}], True, "local")
                    doc = json.loads(Path(smoke.RECEIPT).read_text())
                    for name in ("verified_live_public_website", "native_dev_verified",
                                 "production_servicenow_verified",
                                 "screenshot_publication_approved"):
                        self.assertFalse(doc[name])
                    smoke.write_summary([{"route": "index.html", "status": "PASS"}], True, "live")
                    doc = json.loads(Path(smoke.RECEIPT).read_text())
                    self.assertFalse(doc["verified_live_public_website"])
                    self.assertFalse(doc["verified_exact_deployed_bytes"])
                    self.assertFalse(doc["native_dev_verified"])
                    self.assertFalse(doc["production_servicenow_verified"])
            finally:
                os.chdir(original)


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3
"""Offline contracts for public URL smoke and non-certifying receipts."""
import json
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
            (url, 200, "text/html", b"<html></html>"),
            (url, 200, "text/html", b"\\xff"),
        ]
        for final, code, mime, body in failures:
            with self.subTest(final=final, code=code, mime=mime):
                with self.assertRaises((ValueError, UnicodeError)):
                    smoke.validate_response(url, final, code, mime, body, 'id="gallery"')

    def test_local_fixture_markers_and_fail_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name, marker in smoke.TARGETS.items():
                (root / name).write_text(f"<html>{marker}</html>", encoding="utf-8")
            result = smoke.local_check(root)
            self.assertEqual(len(result), 4)
            self.assertTrue(all(r["verification"] == "LOCAL-ONLY" for r in result))
            (root / "index.html").write_text("<html></html>", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "required marker missing"):
                smoke.local_check(root)

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
                    self.assertTrue(doc["verified_live_public_website"])
                    self.assertFalse(doc["native_dev_verified"])
                    self.assertFalse(doc["production_servicenow_verified"])
            finally:
                os.chdir(original)


if __name__ == "__main__":
    unittest.main()

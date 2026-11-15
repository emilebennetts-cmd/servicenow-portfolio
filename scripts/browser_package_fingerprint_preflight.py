#!/usr/bin/env python3
"""Four-width Chromium test for local SHA-256 comparison and non-certifying JSON exports."""
import hashlib
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

PAGE = (Path(__file__).resolve().parents[1] / "delivery-release-evolution.html").as_uri()
FIXTURE = b"<updates>NEVER_EXPORT_CUSTOMER_KEY is an invented test marker</updates>"
SHA = hashlib.sha256(FIXTURE).hexdigest()

def verify(browser, width):
    page = browser.new_page(viewport={"width": width, "height": 900}, accept_downloads=True)
    errors = []
    requests = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.on("request", lambda req: requests.append(req.url) if req.url.startswith(("https://", "http://")) else None)
    try:
        page.goto(PAGE, wait_until="domcontentloaded")
        page.locator("#package-fingerprint").scroll_into_view_if_needed()
        assert page.locator("#fingerprint-status").inner_text() == "NOT RUN · HOLD"
        page.locator("#fingerprint-run").click()
        assert page.locator("#fingerprint-status").inner_text() == "NO FILE · HOLD"
        page.locator("#package-file").set_input_files(
            {"name": "SENSITIVE_PRIVATE_PACKAGE.xml", "mimeType": "application/xml", "buffer": FIXTURE}
        )
        page.locator("#expected-package-sha").fill("NOT_A_SHA")
        page.locator("#fingerprint-run").click()
        assert page.locator("#fingerprint-status").inner_text() == "INVALID REFERENCE · HOLD"

        page.locator("#expected-package-sha").fill(SHA.upper())
        assert page.locator("#fingerprint-status").inner_text() == "NOT RUN · HOLD"
        page.locator("#fingerprint-run").click()
        page.locator("#fingerprint-status").get_by_text("HASH MATCH — NOT VERIFIED · HOLD").wait_for()
        assert not page.locator("#fingerprint-copy").is_disabled()
        with page.expect_download() as info:
            page.locator("#preflight-export").click()
        content = Path(info.value.path()).read_text(encoding="utf-8")
        packet = json.loads(content)
        assert packet["local_package_fingerprint_status"] == "HASH MATCH — NOT VERIFIED"
        assert packet["release_decision"] == "HOLD"
        assert packet["target_package_hash_verified"] is False
        assert packet["independent_dev_verified"] is False
        assert packet["production_verified"] is False
        assert packet["package_filename_included"] is False
        assert packet["package_digests_included"] is False
        assert packet["package_file_bytes_included"] is False
        assert "SENSITIVE_PRIVATE_PACKAGE" not in content
        assert "NEVER_EXPORT_CUSTOMER_KEY" not in content
        assert SHA.lower() not in content
        page.locator("#expected-package-sha").fill("0" * 64)
        assert page.locator("#fingerprint-status").inner_text() == "NOT RUN · HOLD"
        page.locator("#fingerprint-run").click()
        page.locator("#fingerprint-status").get_by_text("HASH MISMATCH · HOLD").wait_for()
        page.locator("#fingerprint-clear").click()
        assert page.locator("#package-file").input_value() == ""
        assert page.locator("#expected-package-sha").input_value() == ""
        assert page.locator("#fingerprint-status").inner_text() == "NOT RUN · HOLD"
        assert page.evaluate("document.documentElement.scrollWidth <= innerWidth + 2"), width
        assert not errors, errors
        assert not requests, requests
        print(f"PASS {width}px: local digest, mismatch, HOLD-only redaction, reset and no HTTP")
    finally:
        page.close()

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        try:
            for width in (390, 768, 1024, 1440):
                verify(browser, width)
        finally:
            browser.close()

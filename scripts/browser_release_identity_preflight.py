#!/usr/bin/env python3
"""Chromium four-width regression for local-only, HOLD-only release identity preparation."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

URL = (Path(__file__).resolve().parents[1] / "delivery-release-evolution.html").as_uri()

def verify(browser, width):
    page = browser.new_page(
        viewport={"width": width, "height": 900},
        accept_downloads=True,
        reduced_motion="reduce",
    )
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    try:
        page.goto(URL, wait_until="domcontentloaded", timeout=30000)
        assert page.locator("#preflight-status").inner_text().startswith("HOLD"), width
        assert "UNAVAILABLE" == page.locator("#scope-result").inner_text()
        assert page.evaluate("document.documentElement.scrollWidth <= window.innerWidth + 2"), width

        page.locator('[data-preflight-preset="scope"]').click()
        assert "MISMATCH" == page.locator("#scope-result").inner_text()
        assert "HOLD — divergent" in page.locator("#preflight-status").inner_text()
        page.locator('[data-preflight-preset="version"]').click()
        assert "MISMATCH" == page.locator("#version-result").inner_text()

        page.locator('[data-preflight-preset="aligned"]').click()
        assert "TEXT MATCH · NOT VERIFIED" == page.locator("#scope-result").inner_text()
        assert "TEXT MATCH · NOT VERIFIED" == page.locator("#version-result").inner_text()
        assert "HOLD — labels align, runtime unverified" == page.locator("#preflight-status").inner_text()

        page.locator("#target-scope").fill("CUSTOMER_SECRET_MARKER")
        assert "INVALID INPUT" == page.locator("#scope-result").inner_text()
        assert "HOLD — invalid" in page.locator("#preflight-status").inner_text()
        page.locator("#target-scope").fill("x_customer_secret_marker")
        assert "MISMATCH" == page.locator("#scope-result").inner_text()

        with page.expect_download() as info:
            page.locator("#preflight-export").click()
        download = info.value
        assert download.suggested_filename == "servicenow-release-identity-HOLD.json"
        raw = Path(download.path()).read_text(encoding="utf-8")
        packet = json.loads(raw)
        assert "customer_secret_marker" not in raw.lower()
        assert packet["schema"] == "portfolio.release-identity-preflight.v1"
        assert packet["comparison_results"]["scope"] == "MISMATCH"
        assert packet["observed_values_included"] is False
        assert packet["native_execution"] == "NOT RUN"
        assert packet["release_decision"] == "HOLD"
        for flag in ("independent_dev_verified", "production_verified",
                     "target_package_hash_verified", "image_publication_approved"):
            assert packet[flag] is False, flag

        page.locator('#release-preflight-form button[type="reset"]').click()
        assert page.locator("#target-scope").input_value() == ""
        assert page.locator("#target-version").input_value() == ""
        assert "insufficient" in page.locator("#preflight-status").inner_text()
        assert page.evaluate("document.documentElement.scrollWidth <= window.innerWidth + 2"), width
        assert not errors, errors
        print(f"PASS {width}px identity preflight: mismatch, alignment-HOLD, bad input, redacted export")
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

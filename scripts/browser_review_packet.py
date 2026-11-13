#!/usr/bin/env python3
"""Local-only Chromium coverage: eight source reviews, HOLD-only review export.

No ServiceNow access, private images, external URLs, uploads or approvals.
"""
import json
from pathlib import Path

from playwright.sync_api import sync_playwright

URL = (Path(__file__).resolve().parents[1] / "screenshot-review-packet.html").as_uri()


def verify(browser, width):
    page = browser.new_page(viewport={"width": width, "height": 900}, reduced_motion="reduce", accept_downloads=True)
    errors, external = [], []
    page.on("pageerror", lambda error: errors.append(str(error)))
    page.on("request", lambda request: external.append(request.url) if request.url.startswith(("https://", "http://")) else None)
    try:
        page.goto(URL, wait_until="domcontentloaded", timeout=30000)
        assert page.locator("h1").count() == 1
        assert page.locator('option[value^="RV-"]').count() == 8
        assert page.evaluate("() => document.documentElement.scrollWidth <= window.innerWidth + 2"), width
        for ident in range(1, 9):
            record = f"RV-{ident:02d}"
            page.locator("#review-id").select_option(record)
            packet = json.loads(page.locator("#packet-preview").text_content())
            assert packet["public_review_id"] == record
            assert packet["publication_status"] == "HOLD"
            assert packet["public_release_authorised"] is False
            assert packet["native_execution_established"] is False
            assert packet["service_now_dev_verified"] is False
            assert packet["production_verified"] is False
            assert packet["completed_gates"] == 0
            assert page.locator("#review-link").get_attribute("href") == f"visual-evidence.html#review-rv-{ident:02d}"
            is_document = ident in (4, 8)
            assert packet["source_kind"] == ("documentation" if is_document else ("synthetic_ui_capture" if ident in (3, 5, 6) else "ui_capture"))
            assert packet["gallery_eligibility"] == ("DOCUMENT_EXCERPT_ONLY" if is_document else "IMAGE_CANDIDATE_ONLY")
            assert ("DOCUMENT EXCERPT ONLY" in page.locator("#review-treatment").inner_text()) == is_document
        for box in page.locator("input[data-gate]").all():
            box.check()
        packet = json.loads(page.locator("#packet-preview").text_content())
        assert packet["completed_gates"] == 8
        assert packet["handoff_readiness"] == "READY_FOR_INDEPENDENT_REVIEW"
        assert packet["publication_status"] == "HOLD" and not packet["public_release_authorised"]
        assert page.locator("#gate-status").inner_text() == "REVIEW-READY · HOLD"
        with page.expect_download() as info:
            page.locator("#download-packet").click()
        download = info.value
        assert download.suggested_filename == "workbench-review-rv-08-HOLD.json"
        page.locator("#reset-packet").click()
        assert page.locator("#gate-count").inner_text() == "0 of 8 gates marked"
        assert not errors, errors
        assert not external, external
        print(f"PASS {width}px: eight classified reviews, HOLD export, reset, no network and mobile bounds")
    finally:
        page.close()


if __name__ == "__main__":
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        try:
            for viewport in (390, 768, 1024, 1440):
                verify(browser, viewport)
        finally:
            browser.close()

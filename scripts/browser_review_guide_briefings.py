#!/usr/bin/env python3
"""Chromium smoke: public reviewer route briefing and print integrity.

Tests the published offline page only. No native ServiceNow or private files.
"""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

URL = (Path(__file__).resolve().parents[1] / "portfolio-review-guide.html").as_uri()
PUBLIC = "https://emilebennetts-cmd.github.io/servicenow-portfolio/"
ROUTES = {"recruiter": 3, "architect": 4, "assurance": 7}


def verify(browser, width):
    page = browser.new_page(viewport={"width": width, "height": 950},
                            reduced_motion="reduce", accept_downloads=True)
    errors, external, downloads = [], [], []
    page.on("pageerror", lambda error: errors.append(str(error)))
    page.on("request", lambda request: external.append(request.url)
            if request.url.startswith(("http://", "https://")) else None)
    page.on("download", lambda download: downloads.append(download.suggested_filename))
    try:
        page.goto(URL, wait_until="domcontentloaded", timeout=30000)
        assert page.locator("h1").count() == 1
        assert page.locator("#review-export-status").is_visible()
        assert page.evaluate("() => document.documentElement.scrollWidth <= window.innerWidth + 2"), width
        page.evaluate("() => { window.__portfolioPrintCount = 0; window.print = () => window.__portfolioPrintCount++; }")
        for index, (role, expected_links) in enumerate(ROUTES.items(), start=1):
            page.locator(f'[data-route="{role}"]').click()
            selected = page.locator(f'[data-panel="{role}"]')
            assert selected.is_visible()
            assert page.locator('.route-panel:visible').count() == 1
            with page.expect_download() as event:
                page.locator("#export-review-route").click()
            download = event.value
            assert download.suggested_filename == f"servicenow-review-{role}-HOLD.json"
            packet = json.loads(Path(download.path()).read_text(encoding="utf-8"))
            assert packet["audience"] == role
            assert packet["schema_version"] == "1.0"
            assert packet["type"] == "portfolio-review-briefing"
            assert packet["claim_basis"] == "SOURCE-ONLY"
            assert packet["interaction_basis"] == "MOCK-ONLY"
            assert packet["native_dev_verified"] is False
            assert packet["production_verified"] is False
            assert packet["original_screenshots_approved"] == 0
            assert packet["review_state"] == "UNREVIEWED"
            assert packet["verification_state"] == "NOT VERIFIED"
            assert packet["publication_state"] == "HOLD"
            assert len(packet["evidence_links"]) == expected_links
            assert all(item["public_url"].startswith(PUBLIC) for item in packet["evidence_links"])
            page.locator("#print-review-route").click()
            assert page.evaluate("() => window.__portfolioPrintCount") == index
            page.emulate_media(media="print")
            assert selected.is_visible()
            assert page.locator(".topnav").is_hidden()
            assert page.locator(".packet-print-only").is_visible()
            page.emulate_media(media="screen")
        # Fail closed when an unapproved link is introduced into the live DOM.
        page.locator('[data-route="recruiter"]').click()
        page.locator('[data-panel="recruiter"] .route-links a').first.evaluate(
            "(el) => el.setAttribute('href', 'https://external.invalid/private')")
        before_downloads = len(downloads)
        page.locator("#export-review-route").click()
        assert "blocked" in page.locator("#review-export-status").inner_text().lower()
        assert len(downloads) == before_downloads
        page.locator("#print-review-route").click()
        assert page.evaluate("() => window.__portfolioPrintCount") == 3
        assert not errors, errors
        assert not external, external
    finally:
        page.close()


if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        try:
            for width in (390, 768, 1024, 1440):
                verify(browser, width)
                print(f"PASS {width}px: route export, print-only selection, immutable HOLD")
        finally:
            browser.close()

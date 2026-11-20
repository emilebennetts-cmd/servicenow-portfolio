#!/usr/bin/env python3
"""Offline four-width browser verification: screenshot review always remains non-authorising."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
URL = (ROOT / "screenshot-publication-gate.html").as_uri()

def check(browser, width):
    page = browser.new_page(
        viewport={"width": width, "height": 850},
        reduced_motion="reduce", accept_downloads=True)
    errors, external = [], []
    page.on("pageerror", lambda err: errors.append(str(err)))
    page.on("request", lambda req: external.append(req.url)
            if req.url.startswith(("https://", "http://")) else None)
    try:
        page.goto(URL, wait_until="domcontentloaded")
        assert page.locator("h1").count() == 1, width
        assert page.locator("main").count() == 1, width
        assert page.locator("#export").is_disabled(), width
        assert page.locator("#status").inner_text().startswith("BLOCKED"), width
        assert "eight source-held images" in page.locator(".notice").first.inner_text(), width
        assert page.locator('[data-check]').count() == 9, width

        page.locator("#id").fill("PUBLIC-IMG-01")
        page.locator("#digest").fill("a" * 64)
        for checkbox in page.locator('[data-check]').all():
            checkbox.check()
        assert "MANUAL SIGN-OFF REQUIRED" in page.locator("#status").inner_text(), width
        assert page.locator("#export").is_enabled(), width
        with page.expect_download() as event:
            page.locator("#export").click()
        download = event.value
        assert download.suggested_filename == "screenshot-review-hold-only.json"
        receipt = json.loads(Path(download.path()).read_text(encoding="utf-8"))
        assert receipt["schema"] == "portfolio-screenshot-review-v2", width
        assert receipt["redacted_file_sha256"] == "a" * 64, width
        assert receipt["publication_gate"] == "review_complete_not_auto_authorised", width
        assert receipt["reviewed_at_utc"] is None, width
        assert "approved" not in receipt["publication_gate"], width

        page.locator("#notes").fill("Owner email consultant@example.org")
        assert page.locator("#export").is_disabled(), width
        assert page.locator("#status").inner_text().startswith("BLOCKED"), width
        assert "sensitive details" in page.locator("#reason").inner_text(), width
        page.locator("#notes").fill("Controlled offline review, no identities recorded")
        assert page.locator("#export").is_enabled(), width
        page.locator("#digest").fill("")
        assert page.locator("#status").inner_text().startswith("BLOCKED"), width

        page.locator("#reset").click()
        assert page.locator("#id").input_value() == "", width
        assert page.locator("#digest").input_value() == "", width
        assert page.locator('[data-check]:checked').count() == 0, width
        assert page.locator("#export").is_disabled(), width
        assert page.evaluate("document.documentElement.scrollWidth <= innerWidth + 2"), width
        assert not errors, errors
        assert not external, external
        print(f"PASS {width}px: image-byte receipt, secret-safe export, HOLD, reset, no overflow or network")
    finally:
        page.close()

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        try:
            for width in (375, 768, 1024, 1440):
                check(browser, width)
        finally:
            browser.close()

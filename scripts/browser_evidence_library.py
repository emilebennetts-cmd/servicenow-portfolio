#!/usr/bin/env python3
"""Chromium evidence-library verification: public local HTML only, no screenshots or credentials."""
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
PAGE = (ROOT / "evidence.html").as_uri()

def check(browser, width):
    page = browser.new_page(viewport={"width": width, "height": 850}, reduced_motion="reduce")
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    try:
        page.goto(PAGE, wait_until="domcontentloaded")
        assert page.locator("h1").count() == 1, width
        assert page.locator("main").count() == 1, width
        assert page.locator("main").is_visible(), width
        assert page.evaluate("document.documentElement.scrollWidth <= innerWidth + 2"), width
        assert page.locator("#source-documents .card").count() == 6, width
        for tier in ("SOURCE-ONLY", "DEV-VERIFIED", "MOCK-ONLY", "PRODUCTION-VERIFIED"):
            assert tier in page.locator("body").inner_text(), (width, tier)
        assert page.locator("#verification .milestone").count() == 3, width
        assert page.locator("#visuals details").count() == 3, width
        d = page.locator("#visuals details").first
        d.locator("summary").click()
        assert d.evaluate("(el) => el.open"), width
        d.locator("summary").focus()
        page.keyboard.press("Enter")
        assert not d.evaluate("(el) => el.open"), width
        assert page.locator("img, video, iframe, object, embed, script").count() == 0, width
        assert page.evaluate("performance.getEntriesByType('resource').every(x => !x.name.startsWith('http'))"), width
        page.locator('a[href="visual-evidence.html"]').last.click()
        page.wait_for_url("**/visual-evidence.html")
        assert "visual-evidence.html" in page.url, width
        assert not errors, errors
        print(f"PASS {width}px: no overflow, accessible disclosures, internal gallery route, no remote resources")
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

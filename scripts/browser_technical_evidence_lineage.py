#!/usr/bin/env python3
"""Responsive browser check for the dated source-vs-runtime evidence matrix."""
from pathlib import Path
from playwright.sync_api import sync_playwright

PAGE = (Path(__file__).resolve().parents[1] / "technical-evidence-register.html").as_uri()

def check(browser, width):
    page = browser.new_page(viewport={"width": width, "height": 900}, reduced_motion="reduce")
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    try:
        page.goto(PAGE, wait_until="domcontentloaded")
        assert page.locator(".lineage-card").count() == 6
        assert page.locator(".lineage-card:visible").count() == 6
        assert page.evaluate("document.documentElement.scrollWidth <= innerWidth + 2"), width
        page.get_by_role("button", name="Source-only").click()
        assert page.locator(".lineage-card:visible").count() == 3
        assert page.locator(".lineage-card[data-class='SOURCE-ONLY']:visible").count() == 3
        assert page.locator("#lineage-count").inner_text().startswith("Showing 3 of 6")
        assert page.get_by_role("button", name="Source-only").get_attribute("aria-pressed") == "true"
        page.get_by_role("button", name="Historical DEV-reported").click()
        assert page.locator(".lineage-card:visible").count() == 3
        assert page.locator(".lineage-card[data-class='DEV-REPORTED']:visible").count() == 3
        assert page.get_by_role("button", name="Source-only").get_attribute("aria-pressed") == "false"
        page.get_by_role("button", name="All records").click()
        assert page.locator(".lineage-card:visible").count() == 6
        assert "newly verified" in page.locator("#lineage-count").inner_text()
        assert page.evaluate("document.documentElement.scrollWidth <= innerWidth + 2"), width
        assert not errors, errors
        print(f"PASS lineage {width}px: 6 records, three filters, no overflow / JS errors")
    finally:
        page.close()

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        try:
            for width in (390, 768, 1024, 1440):
                check(browser, width)
        finally:
            browser.close()

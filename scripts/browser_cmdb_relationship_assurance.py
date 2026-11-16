#!/usr/bin/env python3
"""Four-width browser proof for the offline CMDB Relationship Integrity Lab.
Fixture-only UI, no ServiceNow API, real screenshots, credentials or customer data.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
URL = (ROOT / "cmdb-relationship-assurance-lab.html").as_uri()
WIDTHS = (375, 768, 1024, 1440)
EXPECTED = {
    "duplicate": "Repeated parent, child, type and port",
    "orphan": "Missing endpoint or relationship type",
    "stale": "synthetically flagged stale",
    "direction": "fictional class/direction rule",
    "baseline": "No sample anomalies",
}


def check(browser, width):
    page = browser.new_page(
        viewport={"width": width, "height": 900},
        reduced_motion="reduce", accept_downloads=True
    )
    errors = []
    page.on("pageerror", lambda exc: errors.append(str(exc)))
    try:
        page.goto(URL, wait_until="domcontentloaded", timeout=30000)
        page.locator("#inspection .verdict").wait_for(timeout=10000)
        assert page.locator("main").count() == 1, f"{width}px: main landmark"
        assert page.locator("h1").count() == 1, f"{width}px: heading"
        assert page.locator("[data-case]").count() == 5, f"{width}px: scenarios"
        assert page.evaluate("() => document.documentElement.scrollWidth <= innerWidth + 2"), f"{width}px: horizontal overflow"

        for case, phrase in EXPECTED.items():
            button = page.locator(f'[data-case="{case}"]')
            button.click()
            assert button.get_attribute("aria-pressed") == "true", f"{width}px: selected state"
            assert phrase in page.locator("#inspection").inner_text(), f"{width}px: {case} finding"
            assert "NOT RUN / HOLD" in page.locator("#test-count").inner_text(), f"{width}px: native status"
        assert "REVIEW — NOT APPROVED" in page.locator("#inspection").inner_text(), f"{width}px: clean false approval"

        with page.expect_download(timeout=15000) as one:
            page.locator("#export-selected").click()
        selected = Path(one.value.path()).read_text(encoding="utf-8-sig")
        assert len(selected.splitlines()) == 7, f"{width}px: six-case CSV"
        assert selected.count('"NOT RUN","HOLD","MOCK-ONLY"') == 6, f"{width}px: selected promotion"

        with page.expect_download(timeout=15000) as all_download:
            page.locator('[data-export="all"]').click()
        complete = Path(all_download.value.path()).read_text(encoding="utf-8-sig")
        assert len(complete.splitlines()) == 31, f"{width}px: complete 30-case CSV"
        assert complete.count('"NOT RUN","HOLD","MOCK-ONLY"') == 30, f"{width}px: all promotion"
        assert not errors, f"{width}px: JS errors {errors}"
        print(f"PASS {width}px: five cases, HOLD-only native 6/30 downloads, no overflow")
    finally:
        page.close()


if __name__ == "__main__":
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        try:
            for width in WIDTHS:
                check(browser, width)
        finally:
            browser.close()

#!/usr/bin/env python3
"""Four-width offline CMDB Assurance Control Tower end-to-end browser test.

No native instance, ServiceNow API, customer data, or screenshots.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
URL = (ROOT / "cmdb-assurance-control-tower.html").as_uri()
WIDTHS = (375, 768, 1024, 1440)


def check(browser, width):
    page = browser.new_page(viewport={"width": width, "height": 900},
                            reduced_motion="reduce", accept_downloads=True)
    errors = []
    page.on("pageerror", lambda exc: errors.append(str(exc)))
    try:
        page.goto(URL, wait_until="domcontentloaded", timeout=30000)
        page.get_by_text("117 source-derived gates", exact=False).wait_for(timeout=10000)
        assert "117 source-derived gates" in page.locator("#tower-count").inner_text()
        assert not page.locator("[data-tower-export='all']").is_disabled()
        assert page.evaluate("() => document.documentElement.scrollWidth <= innerWidth + 2"), f"{width}: overflow"
        assert page.locator("h1").count() == 1

        page.locator("#tower-workstream").select_option("tags")
        assert "25 of 117" in page.locator("#tower-count").inner_text()
        page.locator("#tower-search").fill("nonexistent-source-term-123")
        assert "0 of 117" in page.locator("#tower-count").inner_text()
        page.locator("#tower-search").fill("")
        assert "25 of 117" in page.locator("#tower-count").inner_text()

        with page.expect_download(timeout=15000) as filtered:
            page.locator("[data-tower-export='filtered']").click()
        subset = Path(filtered.value.path()).read_text(encoding="utf-8-sig")
        assert len(subset.splitlines()) == 26, f"{width}: filtered CSV"
        assert subset.count('"NOT RUN","HOLD","MOCK-ONLY"') == 25

        with page.expect_download(timeout=15000) as all_controls:
            page.locator("[data-tower-export='all']").click()
        exported = Path(all_controls.value.path()).read_text(encoding="utf-8-sig")
        assert len(exported.splitlines()) == 118, f"{width}: all CSV"
        assert exported.count('"NOT RUN","HOLD","MOCK-ONLY"') == 117
        assert not errors, f"{width}: page errors {errors}"
        print(f"PASS {width}px: 117 source-derived HOLD controls, 25 filtered, responsive")
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

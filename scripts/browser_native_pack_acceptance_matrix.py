#!/usr/bin/env python3
"""Exercise the public, offline-only Native Acceptance Matrix at four widths."""
from pathlib import Path
import csv
from playwright.sync_api import sync_playwright

URL = (Path(__file__).resolve().parents[1] / "incident-pack-native-pilot.html").as_uri()
WIDTHS = (390, 768, 1024, 1440)


def run(browser, width):
    page = browser.new_page(viewport={"width": width, "height": 900},
                            reduced_motion="reduce", accept_downloads=True)
    try:
        page.goto(URL, wait_until="domcontentloaded")
        assert page.locator("[data-native-case]").count() == 29
        assert page.locator("[data-native-case]:visible").count() == 29
        assert "0 executed here" in page.locator("#native-count").inner_text()
        assert page.evaluate("document.documentElement.scrollWidth <= window.innerWidth + 2"), (
            f"Native matrix page overflow at {width}px"
        )
        page.select_option("#native-group", "Preflight")
        assert page.locator("[data-native-case]:visible").count() == 3
        page.select_option("#native-role", "Delivery A")
        assert page.locator("[data-native-case]:visible").count() == 0
        page.select_option("#native-group", "all")
        visible = page.locator("[data-native-case]:visible").count()
        assert 0 < visible < 29
        assert f"Showing {visible} of 29" in page.locator("#native-count").inner_text()
        with page.expect_download() as started:
            page.locator("#native-export").click()
        download = started.value
        assert download.suggested_filename == "native-pack-validation-NOT-RUN.csv"
        with open(download.path(), encoding="utf-8", newline="") as fh:
            rows = list(csv.DictReader(fh))
        assert len(rows) == visible
        assert all(r["persona"] == "Delivery A" for r in rows)
        assert all(r["status"] == "NOT RUN" and r["runtime_verified"] == "false"
                   and r["release_authorised"] == "false" for r in rows)
        page.select_option("#native-role", "all")
        assert page.locator("[data-native-case]:visible").count() == 29
        print(f"PASS native matrix: {width}px; 29 cases, filters, safe CSV export")
    finally:
        page.close()


if __name__ == "__main__":
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        try:
            for width in WIDTHS:
                run(browser, width)
        finally:
            browser.close()

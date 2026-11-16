#!/usr/bin/env python3
"""Four-width browser execution of the synthetic CMDB Health denominator review.

No ServiceNow API calls, customer data, network calls, persisted screenshots,
or native acceptance claims; compares an offline specimen only.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
URL = (ROOT / "cmdb-health-assurance-lab.html").as_uri()
WIDTHS = (375, 768, 1024, 1440)


def require(ok, message):
    if not ok:
        raise AssertionError(message)


def check(browser, width):
    page = browser.new_page(
        viewport={"width": width, "height": 900},
        reduced_motion="reduce",
        accept_downloads=True,
    )
    errors = []
    page.on("pageerror", lambda exc: errors.append(str(exc)))
    try:
        page.goto(URL, wait_until="domcontentloaded", timeout=30000)
        require(page.locator("h1").count() == 1 and page.locator("main").count() == 1, f"{width}px: missing landmarks")
        require(page.evaluate("() => document.documentElement.scrollWidth <= innerWidth + 2"), f"{width}px: horizontal overflow")
        require(page.locator("#cohort-select button").count() == 4, f"{width}px: missing comparative fixtures")
        require(page.locator('button[data-cohort="remediated"]').get_attribute("aria-pressed") == "true", f"{width}px: default fixture")
        require("LIKE-FOR-LIKE SYNTHETIC" in page.locator("#cohort-verdict").inner_text(), f"{width}px: safe default verdict")
        require("+12 percentage points" in page.locator("#cohort-delta").inner_text(), f"{width}px: arithmetic")

        page.locator('button[data-cohort="denominator"]').click()
        require(page.locator('button[data-cohort="denominator"]').get_attribute("aria-pressed") == "true", f"{width}px: pressed state")
        require("NOT COMPARABLE" in page.locator("#cohort-verdict").inner_text(), f"{width}px: denominator must fail")
        require("87.5%" in page.locator("#cohort-after-label").inner_text(), f"{width}px: changed fraction")
        require("Denominator changed" in page.locator("#cohort-reasons").inner_text(), f"{width}px: missing denominator reason")

        page.locator('button[data-cohort="rule-change"]').click()
        require("Metric rule version changed" in page.locator("#cohort-reasons").inner_text(), f"{width}px: rule change must fail")
        page.locator('button[data-cohort="incomplete"]').click()
        require("completed calculation receipt" in page.locator("#cohort-reasons").inner_text(), f"{width}px: incomplete job must fail")
        require("NATIVE DEV" in page.locator("#denominator-lab").inner_text(), f"{width}px: native hold disclosure")

        with page.expect_download(timeout=15000) as dl:
            page.locator("#download-cohort").click()
        comparison = Path(dl.value.path()).read_text(encoding="utf-8-sig")
        require(len(comparison.splitlines()) == 5, f"{width}px: four-case comparison CSV")
        require(comparison.count('"NOT RUN","HOLD","MOCK-ONLY"') == 4, f"{width}px: worksheet must stay HOLD")

        with page.expect_download(timeout=15000) as dl2:
            page.locator("#download-all").click()
        gates = Path(dl2.value.path()).read_text(encoding="utf-8-sig")
        require(len(gates.splitlines()) == 25, f"{width}px: original 24-gate handoff changed")
        require(gates.count('"NOT RUN","HOLD","MOCK-ONLY"') == 24, f"{width}px: native acceptance promoted")
        require(not errors, f"{width}px: page JS exceptions: {errors}")
        print(f"PASS {width}px: responsive, four synthetic comparisons, fail-closed CSV, unchanged 24 gates")
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

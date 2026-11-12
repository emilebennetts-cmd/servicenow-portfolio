#!/usr/bin/env python3
"""Chromium behaviour regression: synthetic rescan decisions at four viewport widths."""
from pathlib import Path
from playwright.sync_api import sync_playwright

PAGE = (Path(__file__).resolve().parents[1] / "diagnostic-rescan-decision-lab.html").as_uri()

def verify(browser, width):
    page = browser.new_page(viewport={"width": width, "height": 900},
                            reduced_motion="reduce", accept_downloads=True)
    errors, network = [], []
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.on("request", lambda r: network.append(r.url)
            if r.url.startswith(("http://","https://")) else None)
    try:
        page.goto(PAGE, wait_until="domcontentloaded", timeout=30000)
        assert not errors, errors
        assert page.locator("#metrics .metric").count() == 3
        assert "IMPROVEMENT CANDIDATE / HOLD" in page.locator("#decision").inner_text()
        assert page.locator("#gates li").count() == 7
        assert page.evaluate("() => document.documentElement.scrollWidth <= innerWidth + 2"), width

        page.locator("#scenario").select_option("missing")
        assert page.locator("#decision").inner_text() == "NOT ASSESSED / HOLD"
        assert page.locator("#metrics .delta").filter(has_text="NOT ASSESSED").count() == 3

        page.locator("#scenario").select_option("drift")
        assert page.locator("#decision").inner_text() == "NOT ASSESSED / HOLD"

        page.locator("#scenario").select_option("regress")
        assert page.locator("#decision").inner_text() == "REGRESSION / HOLD"
        assert page.locator("#metrics .delta").filter(has_text="REGRESSION").count() == 3

        page.locator("#scenario").select_option("improve")
        page.locator("#threshold").fill("15")
        assert page.locator("#decision").inner_text() == "INCONCLUSIVE / HOLD"

        page.locator("#reset").click()
        assert page.locator("#threshold").input_value() == "3"
        assert page.locator("#scenario").input_value() == "improve"

        with page.expect_download() as d:
            page.locator("#download").click()
        item = d.value
        assert item.suggested_filename == "synthetic-rescan-hold-improve.json"
        import json
        data = json.loads(Path(item.path()).read_text(encoding="utf-8"))
        assert data["approval_status"] == "HOLD"
        assert data["execution_status"] == "NOT RUN"
        assert data["public_release_authorised"] is False
        assert data["servicenow_dev_verified"] is False
        assert data["production_verified"] is False
        assert data["actual_collector_output"] is None

        assert not errors, errors
        assert not network, network
        print("PASS", width, "px: synthetic comparator, denial gates, export and no external requests")
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

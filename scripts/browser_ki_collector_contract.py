#!/usr/bin/env python3
"""Real Chromium smoke for KI synthetic collector failure contracts at four widths."""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright

URL = (Path(__file__).resolve().parents[1] / "knowledge-intelligence-acceptance-matrix.html").as_uri()
FIXTURES = {
    "complete": ("candidate evidence / HOLD", "ok", "KI-COL-01"),
    "table": ("unavailable data / HOLD", "table_unavailable", "KI-COL-02"),
    "field": ("incomplete coverage / HOLD", "field_unavailable", "KI-COL-03"),
    "mutation": ("security control / HOLD", "lint_rejected", "KI-COL-04"),
}


def verify(browser, width):
    page = browser.new_page(viewport={"width": width, "height": 900},
                            reduced_motion="reduce", accept_downloads=True)
    errors, network = [], []
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.on("request", lambda r: network.append(r.url)
            if r.url.startswith(("http://", "https://")) else None)
    try:
        page.goto(URL, wait_until="domcontentloaded")
        assert page.locator("#collector-contract").count() == 1
        assert page.locator("#collector-contract .contract-choices button").count() == 4
        assert page.evaluate("() => document.documentElement.scrollWidth <= innerWidth + 2"), width

        for key, (status, expected, test_id) in FIXTURES.items():
            button = page.locator(f'[data-contract="{key}"]')
            if key == "field":
                button.focus()
                page.keyboard.press("Enter")  # Keyboard activation works
            else:
                button.click()
            assert button.get_attribute("aria-pressed") == "true", key
            assert status.upper() in page.locator("#collector-contract-status").inner_text().upper(), (key, status, page.locator("#collector-contract-status").inner_text(), errors)
            assert test_id in page.locator("#collector-contract-test").inner_text()
            assert page.locator('.contract-choices button[aria-pressed="true"]').count() == 1
            with page.expect_download() as download:
                page.locator("#collector-contract-export").click()
            item = download.value
            assert item.suggested_filename == f"ki-synthetic-collector-{key}-HOLD.json"
            payload = json.loads(Path(item.path()).read_text(encoding="utf-8"))
            assert payload["schema"] == "portfolio-ki-collector-fault-contract/1.0"
            assert payload["expected_code"] == expected
            assert payload["native_test_id"] == test_id
            assert payload["evidence_classification"] == "MOCK-ONLY"
            assert payload["collector_runtime"] == "NOT RUN"
            assert payload["dev_verified"] is False
            assert payload["production_verified"] is False
            assert payload["review_approved"] is False
            assert payload["publication_approval"] == "HOLD"
            assert payload["actual_collector_output"] is None
            assert payload["customer_information"] is None

        assert page.locator('.module').count() == 45
        assert not errors, errors
        assert not network, network
        print(f"PASS {width}px: four failure modes, keyboard, HOLD exports, offline isolation")
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

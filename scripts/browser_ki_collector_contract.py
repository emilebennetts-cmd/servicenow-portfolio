#!/usr/bin/env python3
"""Real Chromium smoke for KI synthetic collector failure contracts at four widths."""
from pathlib import Path
import csv
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


        # Reusable source-scoped CSV plan: all 45 modules and 4 test cases each.
        with page.expect_download() as all_download:
            page.locator("#ki-export-all").click()
        all_file = all_download.value
        assert all_file.suggested_filename == "ki-source-acceptance-all-45-modules-HOLD.csv"
        with Path(all_file.path()).open(encoding="utf-8", newline="") as fp:
            all_cases = list(csv.DictReader(fp))
        assert len(all_cases) == 180, len(all_cases)
        assert len({r["module_code"] for r in all_cases}) == 45
        assert len({r["test_id"] for r in all_cases}) == 180
        assert {r["test_case"] for r in all_cases} == {"RUN", "TABLE", "FIELD", "LINT"}
        assert all(r["source_classification"] == "SOURCE-ONLY" for r in all_cases)
        assert all(r["test_plan_classification"] == "PROPOSED" for r in all_cases)
        assert all(r["runtime_status"] == "NOT RUN" for r in all_cases)
        assert all(r["review_approval"] == "HOLD" for r in all_cases)
        assert all(r["dev_verified"] == "false" and r["production_verified"] == "false" for r in all_cases)
        assert all(r["evidence_reference"] == "" and r["executed_at_utc"] == "" for r in all_cases)
        assert all(r["timeout_seconds"] == "120" for r in all_cases)

        # Filtering preserves only currently visible source modules.
        page.locator("#pack-filter").select_option(label="CMDB & CSDM")
        count = page.locator(".module:visible").count()
        assert 1 <= count < 45, count
        page.locator("#ki-export-filtered").focus()
        with page.expect_download() as filtered_download:
            page.keyboard.press("Enter")
        assert filtered_download.value.suggested_filename == "ki-source-acceptance-filtered-HOLD.csv"
        with Path(filtered_download.value.path()).open(encoding="utf-8", newline="") as fp:
            filtered = list(csv.DictReader(fp))
        assert len(filtered) == count * 4
        assert all(r["product_domain"] == "CMDB & CSDM" for r in filtered)
        assert "PROPOSED" in page.locator("#matrix-export-status").inner_text()

        # Empty search is a no-download state, and does not affect all-module export.
        page.locator("#module-search").fill("unlikely-no-such-module-xyz")
        assert page.locator(".module:visible").count() == 0
        page.locator("#ki-export-filtered").click()
        assert "no file exported" in page.locator("#matrix-export-status").inner_text().lower()
        page.locator("#reset-filter").click()
        assert page.locator(".module:visible").count() == 45

        assert page.locator('.module').count() == 45
        assert not errors, errors
        assert not network, network
        print(f"PASS {width}px: four failure modes, 180 planned tests, filtered CSV, keyboard, HOLD exports, offline isolation")
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

#!/usr/bin/env python3
"""Offline, four-viewport browser contract for the public Tag Governance training lab.

No API access, customer records, real screenshots or ServiceNow execution.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
URL = (ROOT / "cmdb-tag-governance-lab.html").as_uri()
WIDTHS = (375, 768, 1024, 1440)
CASES = {
    "key-drift": "Environment key variants",
    "missing-cost": "Required cost_center",
    "collision": "Conflicting values",
    "reingestion": "overwritten by discovery",
    "baseline": "No synthetic policy exceptions",
}


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
        page.locator("#tg-investigation .decision").wait_for(timeout=10000)
        assert page.locator("h1").count() == 1, f"{width}px: heading"
        assert page.locator("main").count() == 1, f"{width}px: landmark"
        assert page.locator("[data-tg-case]").count() == 5, f"{width}px: scenarios"
        assert page.evaluate("() => document.documentElement.scrollWidth <= innerWidth + 2"), f"{width}px: horizontal overflow"

        for scenario, phrase in CASES.items():
            b = page.locator(f'[data-tg-case="{scenario}"]')
            b.click()
            assert b.get_attribute("aria-pressed") == "true", f"{width}px: {scenario} button state"
            assert phrase in page.locator("#tg-investigation").inner_text(), f"{width}px: {scenario} findings"
            assert "NOT RUN / HOLD" in page.locator("#tg-gate-count").inner_text(), f"{width}px: native status changed"
        assert "REVIEW — NOT APPROVED" in page.locator("#tg-investigation").inner_text(), f"{width}px: clean fixture was falsely approved"

        with page.expect_download(timeout=15000) as download:
            page.locator('#tg-download-selected').click()
        selected = Path(download.value.path()).read_text(encoding="utf-8-sig")
        assert len(selected.splitlines()) == 6, f"{width}px: selected five gates"
        assert selected.count('"NOT RUN","HOLD","MOCK-ONLY"') == 5, f"{width}px: selected HOLD"

        with page.expect_download(timeout=15000) as download_all:
            page.locator('[data-export="all"]').click()
        all_rows = Path(download_all.value.path()).read_text(encoding="utf-8-sig")
        assert len(all_rows.splitlines()) == 26, f"{width}px: 25 native gates"
        assert all_rows.count('"NOT RUN","HOLD","MOCK-ONLY"') == 25, f"{width}px: native promotion forbidden"
        assert not errors, f"{width}px: javascript exceptions {errors}"
        print(f"PASS {width}px: five synthetic policies, safe decision and 25-gate HOLD CSV")
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

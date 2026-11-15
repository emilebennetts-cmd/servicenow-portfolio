#!/usr/bin/env python3
"""Chromium four-viewport contract for synthetic Incident Management portfolio lab.

Tests actual browser interactions and downloadable 24-gate HOLD-only CSV.
No network, credentials, ServiceNow target or screenshots are used.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
URL=(ROOT/"incident-management-implementation-lab.html").as_uri()
WIDTHS=(390,768,1024,1440)

def require(value,message):
    if not value:
        raise AssertionError(message)

def check(browser,width):
    page=browser.new_page(viewport={"width":width,"height":900},device_scale_factor=1,
                          reduced_motion="reduce",accept_downloads=True)
    errors=[]
    page.on("pageerror",lambda exc:errors.append(str(exc)))
    try:
        page.goto(URL,wait_until="domcontentloaded",timeout=30000)
        require(page.locator("main").count()==1 and page.locator("h1").count()==1,
                f"{width}px: missing semantic landmarks")
        require(page.evaluate("() => document.documentElement.scrollWidth <= innerWidth + 2"),
                f"{width}px: horizontal overflow")
        require(page.locator('#gates input[type="checkbox"]').count()==8,
                f"{width}px: missing intake controls")
        page.locator("#gates input").first.check()
        require("1 of 8" in page.locator("#progress").inner_text(),
                f"{width}px: intake mark not recorded")
        page.locator('button[data-scenario="restore"]').click()
        require(page.locator('button[data-scenario="restore"]').get_attribute("aria-pressed")=="true",
                f"{width}px: active scenario not accessible")
        require("0 of 8" in page.locator("#progress").inner_text(),
                f"{width}px: intake mark leaked into restoration")
        require("Internal only" in page.locator("#mock-fields").inner_text(),
                f"{width}px: reconstructed scene failed to change")
        with page.expect_download(timeout=15000) as eight_download:
            page.locator("#export-one").click()
        eight=Path(eight_download.value.path()).read_text(encoding="utf-8-sig")
        require(len(eight.strip().splitlines())==9,
                f"{width}px: scenario CSV must contain eight gates plus header")
        page.locator('button[data-scenario="close"]').click()
        require("0 of 8" in page.locator("#progress").inner_text(),
                f"{width}px: closure scenario not independent")
        page.locator('button[data-scenario="intake"]').click()
        require(page.locator("#gates input").first.is_checked(),
                f"{width}px: original intake reading mark lost")
        with page.expect_download(timeout=15000) as complete_download:
            page.locator("#export-all").click()
        csv=Path(complete_download.value.path()).read_text(encoding="utf-8-sig")
        require(len(csv.strip().splitlines())==25,
                f"{width}px: complete CSV must contain 24 gates plus header")
        for status in ('"NOT RUN"','"HOLD"','"MOCK-ONLY"'):
            require(csv.count(status)==24,
                    f"{width}px: export status count incorrect: {status}")
        require(csv.count('"IN-I01"')==1 and csv.count('"IN-C08"')==1,
                f"{width}px: missing acceptance IDs")
        require(csv.strip().splitlines()[-1].endswith(',"","","","","",""'),
                f"{width}px: private receipt columns must remain blank")
        require('"PASSED"' not in csv and '"APPROVED"' not in csv,
                f"{width}px: synthetic model must not promote native claims")
        require(not errors,f"{width}px: browser errors: {errors}")
        print(f"PASS {width}px: accessibility, no overflow, three independent journeys, 8/24 gate HOLD exports")
    finally:
        page.close()

if __name__=="__main__":
    with sync_playwright() as playwright:
        b=playwright.chromium.launch(headless=True)
        try:
            for width in WIDTHS:check(b,width)
        finally:
            b.close()

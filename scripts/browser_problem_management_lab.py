#!/usr/bin/env python3
"""Chromium smoke test for the public Problem Management mock-only lab.

No external ServiceNow requests, customer data or image/screenshot artifacts.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
URL=(ROOT/"problem-management-implementation-lab.html").as_uri()
WIDTHS=(390,768,1024,1440)

def require(value, message):
    if not value:
        raise AssertionError(message)

def check(browser, width):
    page=browser.new_page(viewport={"width":width,"height":900},device_scale_factor=1,
                          reduced_motion="reduce",accept_downloads=True)
    errors=[]
    page.on("pageerror",lambda exc: errors.append(str(exc)))
    try:
        page.goto(URL,wait_until="domcontentloaded",timeout=30000)
        require(page.locator("h1").count()==1 and page.locator("main").count()==1,
                f"{width}px: landmark count")
        require(page.evaluate("() => document.documentElement.scrollWidth <= window.innerWidth + 2"),
                f"{width}px: horizontal document overflow")
        require(page.locator('#gates input[type="checkbox"]').count()==8,
                f"{width}px: first scenario gates missing")
        first=page.locator('#gates input').first
        first.check()
        require("1 of 8" in page.locator("#progress").inner_text(),
                f"{width}px: design reading mark was not updated")
        page.locator('button[data-scenario="known"]').click()
        require(page.locator('button[data-scenario="known"]').get_attribute("aria-pressed")=="true",
                f"{width}px: scenario switch failed")
        require("0 of 8" in page.locator("#progress").inner_text(),
                f"{width}px: reading marks leaked between scenarios")
        page.locator('button[data-scenario="detect"]').click()
        require(page.locator('#gates input').first.is_checked(),
                f"{width}px: mark not preserved in original scenario")
        with page.expect_download(timeout=15000) as dl:
            page.locator("#export-all").click()
        download=dl.value
        csv=Path(download.path()).read_text(encoding="utf-8-sig")
        require(len(csv.strip().split("\r\n"))==25 if "\r\n" in csv else len(csv.strip().splitlines())==25,
                f"{width}px: exported acceptance row count")
        for status in ('"NOT RUN"','"HOLD"','"MOCK-ONLY"'):
            require(csv.count(status)==24,f"{width}px: CSV cannot promote {status}")
        require(csv.count('"PR-D01"')==1 and csv.count('"PR-F08"')==1,
                f"{width}px: evidence IDs missing")
        require('Private reviewer' not in csv and 'https://dev' not in csv,
                f"{width}px: private evidence must stay blank")
        page.locator("#reset").click()
        require("0 of 8" in page.locator("#progress").inner_text(),
                f"{width}px: reset failed")
        require(not errors,f"{width}px: browser errors: {errors}")
        print(f"PASS {width}px: no overflow, three scenarios, mark isolation and 24-gate HOLD export")
    finally:
        page.close()

if __name__=="__main__":
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True)
        try:
            for w in WIDTHS:check(browser,w)
        finally:
            browser.close()

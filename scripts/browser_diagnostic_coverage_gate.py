#!/usr/bin/env python3
"""Offline four-viewport Diagnostic coverage gate smoke; no ServiceNow access or images."""
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
URL = (ROOT / "diagnostic-coverage-explorer.html").as_uri()

def verify(browser, width):
    page=browser.new_page(viewport={"width":width,"height":850},
                          reduced_motion="reduce",accept_downloads=True)
    errors=[]
    page.on("pageerror", lambda err:errors.append(str(err)))
    try:
        page.goto(URL,wait_until="domcontentloaded",timeout=30000)
        page.locator("#coverage-rows tr").first.wait_for(timeout=10000)
        assert page.locator("#coverage-rows tr").count()==10
        assert "10 blocked" in page.locator("#coverage-summary").inner_text()
        assert "RELEASE HOLD" in page.locator("#coverage-summary").inner_text()
        assert page.evaluate("() => document.documentElement.scrollWidth <= innerWidth + 2"),f"{width}px overflow"
        page.locator("#coverage-scenario").select_option("mixed")
        assert "2 synthetic reviewed" in page.locator("#coverage-summary").inner_text()
        assert "7 blocked" in page.locator("#coverage-summary").inner_text()
        page.locator("#coverage-filter").select_option("attention")
        assert page.locator("#coverage-rows tr").count()==8
        page.locator("#coverage-filter").select_option("reviewed")
        assert page.locator("#coverage-rows tr").count()==2
        page.locator("#coverage-filter").select_option("all")
        page.locator("#coverage-scenario").select_option("denominator")
        assert "9 synthetic reviewed" in page.locator("#coverage-summary").inner_text()
        assert "1 blocked" in page.locator("#coverage-summary").inner_text()
        page.locator("#coverage-scenario").select_option("complete")
        assert "10 synthetic reviewed" in page.locator("#coverage-summary").inner_text()
        assert "0 native verified" in page.locator("#coverage-summary").inner_text()
        assert "RELEASE HOLD" in page.locator("#coverage-summary").inner_text()
        with page.expect_download(timeout=15000) as output:
            page.locator("#coverage-download").click()
        candidate=Path(output.value.path()).read_text(encoding="utf-8-sig")
        assert len(candidate.splitlines())==11,f"{width}px wrong CSV size"
        assert candidate.count('"NOT RUN"')==10
        assert candidate.count('"MOCK-ONLY"')==10
        assert candidate.count('"HOLD"')==10
        assert "GO" not in candidate
        assert not errors, f"{width}px JS errors: {errors}"
        assert page.evaluate("() => document.documentElement.scrollWidth <= innerWidth + 2"),f"{width}px overflow after interaction"
        print(f"PASS {width}px: 10 packs, four synthetic examples, immutable HOLD export")
    finally:
        page.close()

if __name__=="__main__":
    with sync_playwright() as pw:
        browser=pw.chromium.launch(headless=True)
        try:
            for width in (375,768,1024,1440):
                verify(browser,width)
        finally:
            browser.close()

#!/usr/bin/env python3
"""Four-viewport Playwright smoke for the fail-closed gate preparation model."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

URL=(Path(__file__).resolve().parents[1]/"diagnostic-gate-closure-lab.html").as_uri()

def verify(browser,width):
    page=browser.new_page(viewport={"width":width,"height":900},
                          reduced_motion="reduce",accept_downloads=True)
    errors,remote=[],[]
    page.on("pageerror",lambda e:errors.append(str(e)))
    page.on("request",lambda req:remote.append(req.url)
            if req.url.startswith(("http://","https://")) else None)
    try:
        page.goto(URL,wait_until="domcontentloaded")
        assert page.locator(".gate").count()==7
        assert page.locator("#prepared").inner_text()=="0 / 11"
        assert page.locator("#decision").inner_text()=="HOLD"
        assert "EVIDENCE GAP" in page.locator("#gate-outcome").inner_text()
        assert page.evaluate("() => document.documentElement.scrollWidth <= innerWidth + 2"),width

        page.locator("#scenario").select_option("review")
        assert page.locator("#prepared").inner_text()=="3 / 11"
        assert "NATIVE REVIEW REQUIRED" in page.locator("#gate-outcome").inner_text()
        page.locator('.gate[data-gate="3"]').click()
        page.locator('input[data-task="D4"]').check()
        assert page.locator("#prepared").inner_text()=="4 / 11"

        page.locator("#scenario").select_option("entitlement")
        assert page.locator("#prepared").inner_text()=="2 / 11"
        assert "EVIDENCE GAP" in page.locator("#gate-outcome").inner_text()
        page.locator("#scenario").select_option("complete")
        assert page.locator("#prepared").inner_text()=="11 / 11"
        page.locator('.gate[data-gate="6"]').click()
        assert "NATIVE REVIEW REQUIRED / HOLD" in page.locator("#gate-outcome").inner_text()
        with page.expect_download() as d:
            page.locator("#export").click()
        download=d.value
        assert download.suggested_filename=="gate-closure-preparation-HOLD.json"
        packet=json.loads(Path(download.path()).read_text(encoding="utf-8"))
        assert packet["release_decision"]=="HOLD"
        assert packet["publication_approved"] is False
        assert packet["production_verified"] is False
        assert packet["dev_verified"] is False
        assert all(g["native_status"]=="NOT RUN" and not g["approval"] for g in packet["gates"])
        assert len(packet["prepared_ids"])==11
        page.locator("#reset").click()
        assert page.locator("#prepared").inner_text()=="11 / 11"
        assert not errors,errors
        assert not remote,remote
        print(f"PASS {width}px: gates, scenario preparation, immutable HOLD export, no remote requests or overflow")
    finally:
        page.close()

if __name__=="__main__":
    with sync_playwright() as playwright:
        browser=playwright.chromium.launch(headless=True)
        try:
            for width in (390,768,1024,1440):
                verify(browser,width)
        finally:
            browser.close()

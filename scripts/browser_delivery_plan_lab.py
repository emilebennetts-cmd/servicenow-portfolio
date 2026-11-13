#!/usr/bin/env python3
"""Four-viewport Chromium exercise of synthetic Delivery Plan; no external I/O."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright
URL=(Path(__file__).resolve().parents[1]/"delivery-case-study.html").as_uri()

def verify(browser,width):
    page=browser.new_page(viewport={"width":width,"height":900},reduced_motion="reduce",accept_downloads=True)
    errors,requests=[],[]
    page.on("pageerror",lambda e:errors.append(str(e)))
    page.on("request",lambda r:requests.append(r.url) if r.url.startswith(("http://","https://")) else None)
    try:
        page.goto(URL,wait_until="domcontentloaded",timeout=30000)
        assert page.locator("#plan-tabs [role=tab]").count()==8
        assert page.locator("#plan-tab-0").get_attribute("aria-selected")=="true"
        assert page.locator("#plan-next").is_enabled()
        assert page.locator("#plan-prev").is_disabled()
        assert page.evaluate("() => document.documentElement.scrollWidth <= innerWidth+2"),f"{width}px overflow"
        page.locator("#plan-next").click()
        assert page.locator("#plan-view-title").inner_text()=="Scope and context"
        page.locator("#plan-tab-6").click()
        assert "NOT RUN" in page.locator("#plan-gate").inner_text()
        page.locator("#plan-tab-7").click()
        assert page.locator("#plan-next").is_disabled()
        page.locator("#doc-type").select_option(label="Statement of Work planning draft")
        page.locator("#doc-depth").select_option("Technical")
        assert "accepted-proposal gate" in page.locator("#doc-text").inner_text()
        with page.expect_download() as pending:
            page.locator("#doc-export").click()
        data=json.loads(Path(pending.value.path()).read_text(encoding="utf-8"))
        assert data["evidence"]=="MOCK-ONLY"
        assert data["native_test_status"]=="NOT RUN"
        assert data["publication"]=="HOLD"
        assert data["production_verified"] is False
        assert data["client_approved"] is False
        assert data["original_screenshots_approved"]==0
        assert pending.value.suggested_filename=="delivery-plan-synthetic-preview.json"
        # The source-backed operating guide is a rehearsal, not a native test.
        assert page.locator("#persona-cards .persona-card").count()==12
        page.locator("#persona-role").select_option("scanner")
        assert page.locator("#persona-cards .persona-card:visible").count()==1
        assert page.locator('#persona-cards .persona-card:visible').get_attribute("data-procedure")=="4.9"
        assert "1 of 12" in page.locator("#persona-count").inner_text()
        page.locator('#persona-cards .persona-card:visible input').check()
        assert "1 read" in page.locator("#persona-count").inner_text()
        with page.expect_download() as packet:
            page.locator("#persona-export").click()
        txt=Path(packet.value.path()).read_text(encoding="utf-8")
        assert packet.value.suggested_filename=="delivery-workbench-rehearsal-hold.txt"
        assert "NOT RUN | HOLD" in txt
        assert "production_verified=false" in txt
        assert "[x] Guide §4.9" in txt
        page.locator("#persona-role").select_option("all")
        page.locator("#persona-reset").click()
        assert "0 read" in page.locator("#persona-count").inner_text()
        assert page.locator("#persona-cards .persona-card:visible").count()==12
        assert page.evaluate("() => document.documentElement.scrollWidth <= innerWidth+2"),f"{width}px overflow after role switch"
        assert not errors,errors
        assert not requests,requests
        print(f"PASS {width}px: 8 views, SOW safety, 24 preview selector, export, no network")
    finally:page.close()

if __name__=="__main__":
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True)
        try:
            for w in (390,768,1024,1440):verify(browser,w)
        finally:browser.close()

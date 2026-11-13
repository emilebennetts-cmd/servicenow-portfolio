#!/usr/bin/env python3
"""Four-viewport interactive and export check: all results are synthetic and HOLD."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright
URL=(Path(__file__).resolve().parents[1]/"cmdb-remediation-decision-lab.html").as_uri()
def exercise(browser,width):
    page=browser.new_page(viewport={"width":width,"height":900},accept_downloads=True,reduced_motion="reduce")
    errors=[];remote=[]
    page.on("pageerror",lambda e:errors.append(str(e)))
    page.on("request",lambda req:remote.append(req.url) if req.url.startswith(("https://","http://")) else None)
    try:
        page.goto(URL,wait_until="domcontentloaded")
        assert page.locator("[data-fixture]").count()==4
        assert page.locator("#decision").inner_text()=="OWNERSHIP REVIEW"
        assert page.evaluate("() => document.documentElement.scrollWidth <= innerWidth + 2"),width
        page.locator('#evidence').select_option("unavailable")
        assert page.locator("#decision").inner_text()=="EVIDENCE GAP"
        page.locator('#evidence').select_option("capped")
        assert page.locator("#decision").inner_text()=="PARTIAL COVERAGE"
        page.locator('#evidence').select_option("complete")
        page.locator('#owner').select_option("confirmed")
        assert page.locator("#decision").inner_text()=="IMPACT ASSESSMENT"
        page.locator('#impact').select_option("reviewed")
        assert page.locator("#decision").inner_text()=="CHANGE CONTROL"
        page.locator('#change').select_option("approved")
        assert page.locator("#decision").inner_text()=="CONTROLLED REVIEW ONLY"
        assert "NOT RUN" in page.locator("#native").inner_text()
        with page.expect_download() as d:page.locator("#export").click()
        item=d.value
        assert item.suggested_filename=="cmdb-remediation-preparation-HOLD.json"
        packet=json.loads(Path(item.path()).read_text(encoding="utf-8"))
        assert packet["release_decision"]=="HOLD"
        assert packet["native_status"]=="NOT RUN"
        assert packet["dev_verified"] is False and packet["production_verified"] is False
        assert packet["approval"] is False and packet["screenshot_publication_approved"] is False
        page.locator('[data-fixture="relation"]').click()
        assert page.locator("#decision").inner_text()=="PARTIAL COVERAGE"
        page.locator('[data-fixture="stale"]').click()
        assert page.locator("#decision").inner_text()=="EVIDENCE GAP"
        page.locator('[data-fixture="ire"]').click()
        assert page.locator("#decision").inner_text()=="OWNERSHIP REVIEW"
        page.locator("#reset").click()
        assert page.locator("#decision").inner_text()=="OWNERSHIP REVIEW"
        assert not errors,errors
        assert not remote,remote
        print(f"PASS {width}px: control precedence, HOLD export, no network or overflow")
    finally:page.close()
if __name__=="__main__":
    with sync_playwright() as p:
        b=p.chromium.launch(headless=True)
        try:
            for width in (390,768,1024,1440):exercise(b,width)
        finally:b.close()

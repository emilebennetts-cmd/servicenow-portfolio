#!/usr/bin/env python3
"""Real Chromium interaction across four widths; the simulated decision is NOT a native test."""
from pathlib import Path
from playwright.sync_api import sync_playwright

URL=(Path(__file__).resolve().parents[1]/"governed-handoff-contract.html").as_uri()

def check(browser,width):
    page=browser.new_page(viewport={"width":width,"height":900},reduced_motion="reduce",accept_downloads=True)
    errors=[]; remote=[]
    page.on("pageerror",lambda e:errors.append(str(e)))
    page.on("request",lambda request:remote.append(request.url) if request.url.startswith(("http://","https://")) else None)
    try:
        page.goto(URL,wait_until="domcontentloaded")
        assert "DRAFT ELIGIBLE (SIMULATED)" in page.locator("#hc-status").inner_text()
        assert page.evaluate("() => document.documentElement.scrollWidth <= innerWidth + 2"), width
        page.locator("#handoff-decision-desk summary").click()
        for key,expected in (
            ("review","HOLD"),("version","REJECT"),("evidence","HOLD"),
            ("role","REJECT"),("scope","MANUAL"),("conflict","HOLD"),
            ("replay","REUSE"),("ready","DRAFT ELIGIBLE")
        ):
            page.locator("#hc-scenario").select_option(key)
            assert expected in page.locator("#hc-status").inner_text(),(width,key)
            payload=page.locator("#hc-output").text_content()
            assert '"native_execution": "NOT RUN"' in payload
            assert '"publication_decision": "HOLD"' in payload
        page.locator("#hc-scenario").select_option("replay")
        page.locator("#hc-reviewed").uncheck()
        assert "HOLD — INCOMPLETE REVIEW" in page.locator("#hc-status").inner_text()
        with page.expect_download() as event:
            page.locator("#hc-download").click()
        download=event.value
        assert download.suggested_filename=="synthetic-handoff-review.json"
        assert not remote,remote
        assert not errors,errors
        assert page.evaluate("() => document.documentElement.scrollWidth <= innerWidth + 2"),width
        print("PASS",width,"px: 8 scenarios, precedence, export, no external requests or overflow")
    finally:
        page.close()

if __name__=="__main__":
    with sync_playwright() as p:
        b=p.chromium.launch(headless=True)
        try:
            for w in (390,768,1024,1440): check(b,w)
        finally:b.close()

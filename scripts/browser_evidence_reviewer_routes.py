#!/usr/bin/env python3
"""Responsive Chromium verification for public evidence reviewer navigation.

Uses only local file:// pages and synthetic editorial links; never ServiceNow.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
URL=(ROOT/"engineering-case-studies.html").as_uri()
WIDTHS=(390,768,1024,1440)

def check(browser,width):
    page=browser.new_page(viewport={"width":width,"height":900},accept_downloads=True,reduced_motion="reduce")
    errors=[]
    external=[]
    page.on("pageerror",lambda err:errors.append(str(err)))
    page.on("request",lambda request:external.append(request.url) if request.url.startswith(("https://","http://")) else None)
    try:
        page.goto(URL,wait_until="domcontentloaded",timeout=30000)
        assert not errors,errors
        assert page.locator("h1").count()==1
        assert page.locator("#route-board .route-card").count()==3
        assert page.locator('[data-route="recruiter"]').get_attribute("aria-pressed")=="true"
        assert "Diagnostic" in page.locator("#route-board").inner_text()
        assert page.evaluate("() => document.documentElement.scrollWidth <= window.innerWidth + 2"),f"{width}px horizontal overflow"
        page.locator('[data-route="architect"]').click()
        assert page.locator('[data-route="architect"]').get_attribute("aria-pressed")=="true"
        assert page.locator("#route-board .route-card a").nth(1).get_attribute("href")=="source-target-compatibility.html"
        assert "4.22.2" in page.locator("#route-board").inner_text()
        page.locator('[data-route="architect"]').focus()
        page.keyboard.press("ArrowRight")
        assert page.locator('[data-route="delivery"]').get_attribute("aria-pressed")=="true"
        assert page.locator('[data-route="delivery"]').evaluate("(el)=>document.activeElement===el")
        assert page.locator("#route-board .route-card a").nth(2).get_attribute("href")=="finding-to-release-handoff.html"
        with page.expect_download(timeout=10000) as info:
            page.locator("#route-export").click()
        download=info.value
        assert download.suggested_filename=="servicenow-delivery-reading-route.txt"
        body=Path(download.path()).read_text(encoding="utf-8")
        assert "SOURCE-ONLY" in body and "HOLD" in body
        assert "finding-to-release-handoff.html" in body
        assert "DEV/production acceptance is not established" in body
        assert "not an acceptance receipt" in page.locator("#route-feedback").inner_text()
        assert not external,f"External network request: {external}"
        assert not errors,errors
        print(f"PASS {width}px: responsive reviewer selection, keyboard navigation, public routes, HOLD export")
    finally:
        page.close()

if __name__=="__main__":
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True)
        try:
            for width in WIDTHS:check(browser,width)
            context=browser.new_context(java_script_enabled=False)
            static=context.new_page()
            static.goto(URL,wait_until="domcontentloaded",timeout=30000)
            assert static.locator("#route-board .route-card").count()==3
            assert static.locator('#route-board a[href="diagnostic-workbench-case-study.html"]').count()==1
            context.close()
            print("PASS no-JavaScript: default hiring-manager reading route remains accessible")
        finally:
            browser.close()

#!/usr/bin/env python3
"""Four-viewport accessibility and boundary smoke for the source-informed CSDM page."""
from pathlib import Path
from playwright.sync_api import sync_playwright
URL = (Path(__file__).resolve().parents[1] / "cmdb-ire-assurance.html").as_uri() + "#csdm-ownership"

def run(browser, width):
    page = browser.new_page(viewport={"width":width, "height":900}, reduced_motion="reduce")
    errors = []
    requests = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.on("request", lambda r: requests.append(r.url) if r.url.startswith(("https://","http://")) else None)
    try:
        page.goto(URL, wait_until="domcontentloaded")
        model = page.locator("#csdm-ownership")
        assert model.count() == 1
        assert model.locator(".csdm-node").count() == 4
        assert model.locator(".csdm-gates li").count() == 6
        cases = model.locator(".csdm-cases details")
        assert cases.count() == 3
        assert cases.nth(0).get_attribute("open") is not None
        assert not cases.nth(1).locator("p").first.is_visible()
        cases.nth(1).locator("summary").click()
        assert cases.nth(1).locator("p").first.is_visible()
        cases.nth(2).locator("summary").focus()
        page.keyboard.press("Enter")
        assert cases.nth(2).locator("p").first.is_visible()
        assert page.evaluate("() => document.documentElement.scrollWidth <= window.innerWidth + 2"), width
        assert "SOURCE-ONLY / PROPOSED" in model.inner_text()
        assert "no ServiceNow licence" in model.inner_text()
        assert not errors, errors
        assert not requests, requests
        print(f"PASS {width}px: CSDM categories, disclosures, keyboard, no overflow/network")
    finally:
        page.close()

if __name__ == "__main__":
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        try:
            for width in (390, 768, 1024, 1440):
                run(browser, width)
        finally:
            browser.close()

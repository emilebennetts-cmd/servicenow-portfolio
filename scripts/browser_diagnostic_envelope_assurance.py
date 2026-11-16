#!/usr/bin/env python3
"""Four-width local Chromium smoke for synthetic DIAG envelope assurance; no ServiceNow calls."""
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
def check(browser,width):
    page=browser.new_page(viewport={"width":width,"height":820},accept_downloads=True,reduced_motion="reduce")
    errors=[]
    page.on("pageerror",lambda err: errors.append(str(err)))
    try:
        page.goto((ROOT/"diagnostic-envelope-assurance-lab.html").as_uri(),wait_until="domcontentloaded")
        assert page.locator("#decision").inner_text()=="CAN_REVIEW"
        assert "RELEASE HOLD" in page.locator("#summary").inner_text()
        for key,expected in [("markers","REJECT"),("schema","REJECT"),("write","REJECT"),("pii","REJECT"),("not-applicable","NOT_APPLICABLE"),("capped","INCOMPLETE"),("zero","REVIEW"),("sensitive","REJECT"),("no-groups","CAN_REVIEW"),("count-drift","INCOMPLETE"),("open-over-total","INCOMPLETE"),("payload-injection","REJECT"),("unsafe-result","REJECT"),("malformed-note","REJECT")]:
            page.locator("#scenario").select_option(key)
            assert page.locator("#decision").inner_text()==expected,(width,key)
            assert "DEV-VERIFIED 0" in page.locator("#summary").inner_text()
        for selector,rows in [("#download-examples",16),("#download-gates",9)]:
            with page.expect_download() as dl: page.locator(selector).click()
            candidate=Path(dl.value.path()).read_text(encoding="utf-8-sig")
            assert len(candidate.splitlines())==rows
            assert "HOLD" in candidate and "NOT RUN" in candidate
        assert page.evaluate("document.documentElement.scrollWidth <= innerWidth+2"),width
        assert not errors,errors
        print(f"PASS {width}px: scenario controls, HOLD CSV, no overflow")
    finally:
        page.close()
if __name__=="__main__":
    with sync_playwright() as playwright:
        browser=playwright.chromium.launch(headless=True)
        try:
            for width in (375,768,1024,1440):check(browser,width)
        finally: browser.close()

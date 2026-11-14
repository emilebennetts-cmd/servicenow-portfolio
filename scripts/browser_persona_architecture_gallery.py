#!/usr/bin/env python3
"""Accessible persona-tour/browser assurance. Website tests, not native ServiceNow verification."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / "workbench-architecture-gallery.html").read_text(encoding="utf-8")
URL = (ROOT / "workbench-architecture-gallery.html").as_uri()

def source_contract():
    for text in (
        'id="persona-tour"', 'role="tablist"', 'role="tabpanel"',
        'SOURCE-ONLY', 'MOCK-ONLY', "native_dev_verified:false",
        "production_verified:false", "screenshot_publication_approved:false",
        "review_state:'UNREVIEWED'", "verification_state:'NOT VERIFIED'",
        "release_state:'HOLD'", "30 September 2026",
        'id="persona-share-link"', 'id="persona-copy-link"', 'id="persona-share-url"',
        "Object.prototype.hasOwnProperty.call(data,requestedRole)",
    ):
        assert text in HTML, f"Missing required source boundary: {text}"
    assert HTML.count('data-role="') == 6, "Expected six fixed public personas"
    assert "<img" not in HTML.lower(), "Original image publication is not authorised"
    assert "fetch(" not in HTML and "XMLHttpRequest" not in HTML
    assert "localStorage" not in HTML and "sessionStorage" not in HTML
    assert "servicenow-portfolio-control" not in HTML

def run(browser, width):
    page=browser.new_page(
        viewport={"width":width,"height":900},accept_downloads=True,reduced_motion="reduce"
    )
    errors=[]
    page.on("pageerror",lambda e: errors.append(str(e)))
    try:
        page.goto(URL,wait_until="domcontentloaded")
        tabs=page.locator("#persona-tabs [role='tab']")
        assert tabs.count()==6
        assert page.locator("#persona-panel").get_attribute("aria-labelledby")=="role-presales"
        assert page.locator("#persona-name").inner_text()=="Presales: establish a governed engagement"
        assert page.evaluate("document.documentElement.scrollWidth <= innerWidth + 2"),width

        page.locator("#role-architect").click()
        assert "requirements" in page.locator("#persona-name").inner_text().lower()
        assert page.locator("#role-architect").get_attribute("aria-selected")=="true"
        assert page.locator("#role-presales").get_attribute("tabindex")=="-1"
        page.locator("#role-architect").press("ArrowRight")
        assert page.locator("#role-delivery").get_attribute("aria-selected")=="true"
        assert page.evaluate("document.activeElement.id")=="role-delivery"
        page.locator("#role-delivery").press("End")
        assert page.locator("#role-support").get_attribute("aria-selected")=="true"
        page.locator("#role-support").press("Home")
        assert page.locator("#role-presales").get_attribute("aria-selected")=="true"

        # A recruiter can open a version-neutral, public persona URL directly.
        page.goto(URL+"?role=architect#persona-tour",wait_until="domcontentloaded")
        assert page.locator("#role-architect").get_attribute("aria-selected")=="true"
        assert "requirements" in page.locator("#persona-name").inner_text().lower()
        assert page.locator("#persona-panel").get_attribute("aria-labelledby")=="role-architect"
        page.goto(URL+"?role=%3Cscript%3E#persona-tour",wait_until="domcontentloaded")
        assert page.locator("#role-presales").get_attribute("aria-selected")=="true"
        page.goto(URL+"?role=__proto__#persona-tour",wait_until="domcontentloaded")
        assert page.locator("#role-presales").get_attribute("aria-selected")=="true"
        page.locator("#role-deployer").click()
        assert "preview" in page.locator("#persona-gate").inner_text().lower()
        direct=page.locator("#persona-share-link").get_attribute("href")
        assert "?role=deployer#persona-tour" in direct
        assert "servicenow-portfolio-control" not in direct
        page.locator("#persona-copy-link").click()
        status=page.locator("#persona-share-status").inner_text().lower()
        assert ("copied" in status or "unavailable" in status),status
        if "unavailable" in status:
            assert page.locator("#persona-share-url").is_visible()
            assert page.locator("#persona-share-url").input_value()==direct
        assert page.evaluate("document.documentElement.scrollWidth <= innerWidth + 2"),width
        with page.expect_download() as download:
            page.locator("#persona-export").click()
        item=download.value
        assert item.suggested_filename=="workbench-persona-review-deployer.json"
        payload=json.loads(Path(item.path()).read_text(encoding="utf-8"))
        assert payload["persona"]=="deployer"
        assert payload["architecture_classification"]=="SOURCE-ONLY"
        assert payload["interaction_classification"]=="MOCK-ONLY"
        assert payload["review_state"]=="UNREVIEWED"
        assert payload["verification_state"]=="NOT VERIFIED"
        assert payload["release_state"]=="HOLD"
        for k in ("native_dev_verified","production_verified","screenshot_publication_approved"):
            assert payload[k] is False,k
        assert "dev438211" not in json.dumps(payload)
        assert "x_1577958" not in json.dumps(payload)
        assert "customer" not in json.dumps(payload).lower()
        assert not errors,errors
        print(f"PASS persona architecture {width}px: six roles, deep links, clipboard fallback, keyboard, conservative export")
    finally:
        page.close()

if __name__=="__main__":
    source_contract()
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True)
        try:
            for width in (390,768,1024,1440):
                run(browser,width)
        finally:
            browser.close()

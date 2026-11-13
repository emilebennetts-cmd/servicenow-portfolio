#!/usr/bin/env python3
"""Chromium mobile/desktop behaviour for offline-only portfolio explorer."""
from pathlib import Path
from playwright.sync_api import sync_playwright

URL = (Path(__file__).resolve().parents[1] / "portfolio-explorer.html").as_uri()

def verify(browser, width):
    page = browser.new_page(viewport={"width": width, "height": 900}, reduced_motion="reduce")
    errors = []
    page.on("pageerror", lambda err: errors.append(str(err)))
    requests = []
    page.on("request", lambda req: requests.append(req.url) if req.url.startswith(("http://","https://")) else None)
    try:
        page.goto(URL, wait_until="domcontentloaded", timeout=30000)
        assert not errors, errors
        assert page.locator(".result").count() >= 60
        registered = page.locator(".result:not([data-evidence=unregistered])").count()
        assert page.locator("#registered-pages").inner_text() == str(registered)
        assert page.locator(".result:visible").count() == 18
        assert page.locator("#more").is_visible()
        assert page.evaluate("() => document.documentElement.scrollWidth <= innerWidth + 2"), f"{width}px horizontal overflow"
        page.locator("#search").fill("CMDB")
        count = page.locator(".result:visible").count()
        assert count >= 2, f"{width}px CMDB search returned {count}"
        assert all("cmdb" in (x.get_attribute("data-search") or "").lower()
                   for x in page.locator(".result:visible").all())
        page.locator("#category").select_option(label="Labs & patterns")
        assert page.locator(".result:visible").count() >= 1
        page.locator("#category").select_option("All")
        page.locator("#search").fill("")
        page.locator("#evidence-status").select_option("mock-only")
        mock_rows = page.locator(".result:visible").all()
        assert len(mock_rows) >= 5, f"{width}px too few MOCK-ONLY pages"
        assert all(row.get_attribute("data-evidence") == "mock-only" for row in mock_rows)
        page.locator("#evidence-status").select_option("dev-reported")
        dev_rows = page.locator(".result:visible").all()
        assert len(dev_rows) >= 2
        assert all(row.get_attribute("data-evidence") == "dev-reported" for row in dev_rows)
        page.locator("#evidence-status").select_option("proposed")
        design_rows = page.locator(".result:visible").all()
        assert len(design_rows) >= 3, f"{width}px proposed reference designs missing"
        assert all(row.get_attribute("data-evidence") == "proposed" for row in design_rows)
        page.locator("#evidence-status").select_option("unregistered")
        assert page.locator(".result:visible").count() >= 1
        page.locator("#reset").click()
        assert page.locator("#search").input_value() == ""
        assert page.locator("#category").input_value() == "All"
        assert page.locator("#evidence-status").input_value() == "All"
        assert page.locator(".result:visible").count() == 18
        page.locator("#more").click()
        assert page.locator(".result:visible").count() == page.locator(".result").count()
        assert not requests, f"Network requests forbidden: {requests}"
        assert not errors, errors
        print(f"PASS {width}px: complete list, text/topic filters, reset, expand, viewport bounds and no network")
    finally:
        page.close()

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        try:
            for width in (390, 768, 1024, 1440):
                verify(browser, width)
        finally:
            browser.close()

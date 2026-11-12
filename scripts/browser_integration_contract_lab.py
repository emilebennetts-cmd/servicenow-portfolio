#!/usr/bin/env python3
"""Playwright browser checks for synthetic contract outcomes at four widths."""
from pathlib import Path
from playwright.sync_api import sync_playwright

URL = (Path(__file__).resolve().parents[1] / "integration-contract-lab.html").as_uri()

def run(browser, width):
    page = browser.new_page(viewport={"width": width, "height": 900},
                            reduced_motion="reduce")
    errors, remote = [], []
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.on("request", lambda r: remote.append(r.url)
            if r.url.startswith(("http://", "https://")) else None)
    try:
        page.goto(URL, wait_until="domcontentloaded", timeout=30000)
        assert page.locator("#status").inner_text() == "DRAFT · NOT RUN"
        assert "CREATE plan" in page.locator("#outcome").inner_text()
        assert page.evaluate("() => document.documentElement.scrollWidth <= innerWidth + 2"), width

        page.locator("#scenario").select_option("replay")
        assert page.locator("#status").inner_text() == "REPLAY · NOT RUN"
        assert "no-op" in page.locator("#outcome").inner_text()

        page.locator("#scenario").select_option("conflict")
        assert page.locator("#status").inner_text() == "REVIEW · NOT RUN"
        assert "Concurrent" in page.locator("#outcome").inner_text()

        page.locator("#scenario").select_option("inbound")
        assert page.locator("#status").inner_text() == "HOLD · NOT RUN"
        assert "Protected" in page.locator("#outcome").inner_text()

        page.locator("#scenario").select_option("missing")
        assert page.locator("#status").inner_text() == "HOLD · NOT RUN"
        assert "Connection approval missing" in page.locator("#outcome").inner_text()

        page.locator("#scenario").select_option("new")
        page.locator("#revision").fill("-1")
        page.locator("#evaluate").click()
        assert "Invalid revision" in page.locator("#outcome").inner_text()

        page.locator("#revision").fill("4")
        page.locator("#linked").check()
        page.locator("#direction").select_option("inbound")
        assert page.locator("#status").inner_text() == "DRAFT · NOT RUN"
        assert "REFRESH" in page.locator("#outcome").inner_text()
        assert not errors, errors
        assert not remote, remote
        print("PASS", width, "px: deterministic outcomes, invalid input, no network or overflow")
    finally:
        page.close()

if __name__ == "__main__":
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        try:
            for width in (390, 768, 1024, 1440):
                run(browser, width)
        finally:
            browser.close()

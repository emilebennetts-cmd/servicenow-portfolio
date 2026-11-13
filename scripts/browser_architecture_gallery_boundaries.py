#!/usr/bin/env python3
"""Verify the public architecture evidence gallery across four viewports.

This is browser/website assurance only, never a ServiceNow DEV or PROD test.
"""
from pathlib import Path

from playwright.sync_api import sync_playwright

URL = (Path(__file__).resolve().parents[1] / "workbench-architecture-gallery.html").as_uri()
WIDTHS = (390, 768, 1024, 1440)


def run(browser, width):
    page = browser.new_page(viewport={"width": width, "height": 900}, reduced_motion="reduce")
    try:
        page.goto(URL, wait_until="domcontentloaded")
        cards = page.locator("#baseline .baseline-card")
        assert cards.count() == 3
        assert cards.filter(has_text="4.6.1 source").count() == 1
        assert cards.filter(has_text="4.22.2 source").count() == 1
        assert cards.filter(has_text="4.22.8 demo").count() == 1
        assert cards.filter(has_text="NOT RUN").count() == 1
        assert page.get_by_role("link", name="Version evidence").count() == 1
        assert page.evaluate("document.documentElement.scrollWidth <= window.innerWidth + 2"), (
            f"Architecture gallery horizontal overflow at {width}px"
        )
        page.get_by_role("link", name="Version evidence").click()
        assert page.evaluate("location.hash") == "#baseline"
        assert page.locator("#verification dt").all_inner_texts() == [
            "SOURCE-ONLY", "DEV-REPORTED", "DEV-VERIFIED", "MOCK-ONLY", "PRODUCTION-VERIFIED"
        ]
        assert page.locator("img").count() == 0  # Diagram text is not an approved screenshot
        for card in cards.all():
            box = card.bounding_box()
            assert box and box["width"] <= width, f"Gallery card overflow at {width}px"
        print(f"PASS architecture gallery {width}px: 3 dated snapshots and no promoted runtime claim")
    finally:
        page.close()


if __name__ == "__main__":
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        try:
            for width in WIDTHS:
                run(browser, width)
        finally:
            browser.close()

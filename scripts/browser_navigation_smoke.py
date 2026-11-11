#!/usr/bin/env python3
"""Browser-level responsive navigation verification — no screenshot capture.

Execute only after `pip install playwright` and `playwright install chromium`.
The test serves local public HTML via file:// and never logs in to ServiceNow,
opens private source documents, or creates public image artifacts.
"""
from pathlib import Path
from playwright.sync_api import sync_playwright

INDEX_URL = (Path(__file__).resolve().parents[1] / "index.html").as_uri()
VIEWPORTS = (390, 768, 1024, 1440)


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def check_viewport(browser, width):
    page = browser.new_page(
        viewport={"width": width, "height": 900},
        device_scale_factor=1,
        reduced_motion="reduce",
    )
    try:
        page.goto(INDEX_URL, wait_until="domcontentloaded", timeout=30000)
        summary = page.locator(".mobile-directory > summary")
        primary = page.locator("nav.nav")
        directory = page.locator("nav.mobile-links")

        require(summary.is_visible(), f"{width}px: full-directory disclosure is hidden")
        require(primary.is_visible() == (width > 980),
                f"{width}px: primary nav visibility does not match breakpoint")
        require(
            page.evaluate(
                "() => document.querySelector('header.top').scrollWidth <= window.innerWidth + 2"
            ),
            f"{width}px: header content overflows the viewport",
        )

        summary.click()
        require(page.locator(".mobile-directory").evaluate("(el) => el.open"),
                f"{width}px: directory did not open")
        require(directory.is_visible(), f"{width}px: directory links are not visible")
        box = directory.bounding_box()
        require(box is not None, f"{width}px: directory has no visible bounds")
        require(
            box["x"] >= -1 and box["x"] + box["width"] <= width + 1,
            f"{width}px: directory extends outside screen: {box}",
        )

        # Native disclosure + existing Escape handler must be keyboard-operable.
        page.keyboard.press("Escape")
        require(not page.locator(".mobile-directory").evaluate("(el) => el.open"),
                f"{width}px: Escape did not close directory")
        require(summary.evaluate("(el) => document.activeElement === el"),
                f"{width}px: keyboard focus was not returned to menu trigger")

        summary.click()
        directory.locator('a[href="visual-evidence.html"]').click()
        page.wait_for_url("**/visual-evidence.html", timeout=12000)
        require("visual-evidence.html" in page.url,
                f"{width}px: public visual-evidence route could not be opened")
        print(f"PASS {width}px: responsive header, menu bounds, Escape/focus and evidence route")
    finally:
        page.close()


def main():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        try:
            for width in VIEWPORTS:
                check_viewport(browser, width)
        finally:
            browser.close()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Browser-level responsive navigation verification — no screenshot capture.

Execute only after `pip install playwright` and `playwright install chromium`.
The test serves local public HTML via file:// and never logs in to ServiceNow,
opens private source documents, or creates public image artifacts.
"""
from pathlib import Path
import json
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



CASE_STUDIES = (
    ("diagnostic-workbench-case-study.html", "implementation"),
    ("reusable-delivery-patterns-case-study.html", "build-map"),
    ("cmdb-ire-assurance.html", "metrics"),
)


def check_case_study(browser, filename, anchor, width):
    """Inspect the actual local HTML in Chromium; never ingest private captures."""
    url = (Path(__file__).resolve().parents[1] / filename).as_uri()
    page = browser.new_page(
        viewport={"width": width, "height": 900},
        device_scale_factor=1,
        reduced_motion="reduce",
    )
    try:
        page.goto(url, wait_until="domcontentloaded", timeout=30000)
        require(page.locator("h1").count() == 1, f"{filename}: expected one page title")
        require(page.locator("main").count() == 1, f"{filename}: expected one main landmark")
        require(
            page.evaluate("() => document.documentElement.scrollWidth <= window.innerWidth + 2"),
            f"{filename} at {width}px: horizontal document overflow",
        )
        text = page.locator("body").inner_text()
        for classification in ("SOURCE-ONLY", "DEV-VERIFIED", "MOCK-ONLY", "PRODUCTION-VERIFIED"):
            require(classification in text, f"{filename}: missing {classification} boundary")
        require(
            "not" in text.lower() and "screenshot" in text.lower(),
            f"{filename}: missing screenshot publication boundary",
        )
        page.locator(f'a[href="#{anchor}"]').click()
        require(page.url.endswith(f"#{anchor}"), f"{filename}: broken architecture anchor")
        require(page.locator(f"#{anchor}").count() == 1, f"{filename}: missing architecture section")
        require(
            page.locator(f"#{anchor}").evaluate("(el) => el.getBoundingClientRect().width > 0"),
            f"{filename}: architecture section is not rendered",
        )
        print(f"PASS {width}px: {filename} document bounds, provenance and architecture link")
    finally:
        page.close()


def check_cmdb_trust_lab(browser, width):
    """Exercise synthetic fixture decisions: no ServiceNow calls or captures."""
    url = (Path(__file__).resolve().parents[1] / "cmdb-diagnostic-trust-lab.html").as_uri()
    page = browser.new_page(
        viewport={"width": width, "height": 900},
        device_scale_factor=1,
        reduced_motion="reduce",
    )
    try:
        page.goto(url, wait_until="domcontentloaded", timeout=30000)
        require(page.locator("h1").count() == 1, f"{width}px: Trust Lab title absent")
        require(page.locator("main").count() == 1, f"{width}px: Trust Lab main absent")
        require(page.evaluate(
            "() => document.documentElement.scrollWidth <= window.innerWidth + 2"
        ), f"{width}px: Trust Lab horizontal overflow")
        require(page.locator("#overall-status").inner_text() == "PASS",
                f"{width}px: initial fixture should PASS")
        cases = (
            ("truncated", "PARTIAL", 0),
            ("unavailable", "NOT ASSESSED", None),
            ("overlap", "REVIEW", 7),
            ("ownership", "REVIEW", 0),
        )
        for key, expected, relation_count in cases:
            button = page.locator('[data-scenario="' + key + '"]')
            button.click()
            require(button.get_attribute("aria-pressed") == "true",
                    f"{width}px: {key} not selected")
            require(page.locator("#overall-status").inner_text() == expected,
                    f"{width}px: {key} status incorrect")
            receipt = json.loads(page.locator("#fixture-receipt").inner_text())
            require(receipt["fixture"] == key
                    and receipt["assessment_status"] == expected
                    and receipt["evidence_class"] == "MOCK-ONLY"
                    and receipt["service_now_instance"] == "none",
                    f"{width}px: {key} receipt invalid")
            require(receipt["distinct_incomplete_relationships"] == relation_count,
                    f"{width}px: {key} relationship union invalid")
        page.locator('[data-scenario="baseline"]').click()
        require(page.locator("#overall-status").inner_text() == "PASS",
                f"{width}px: baseline did not restore")
        print(f"PASS {width}px: CMDB Trust Lab fixture decisions and mobile bounds")
    finally:
        page.close()



def check_mim_design_lab(browser, width):
    """Test synthetic MIM gate decisions and receipt, never ServiceNow execution."""
    url = (Path(__file__).resolve().parents[1] / "major-incident-implementation-lab.html").as_uri()
    page = browser.new_page(viewport={"width": width, "height": 900}, reduced_motion="reduce")
    try:
        page.goto(url, wait_until="domcontentloaded", timeout=30000)
        require(page.locator("h1").count()==1 and page.locator("main").count()==1,
                f"{width}px: MIM page landmarks")
        require(page.evaluate("() => document.documentElement.scrollWidth <= window.innerWidth + 2"),
                f"{width}px: MIM page horizontal overflow")
        def check(expected):
            receipt=json.loads(page.locator("#readiness-receipt").inner_text())
            require(receipt["readiness_status"]==expected, f"{width}px: expected {expected}")
            require(receipt["evidence_class"]=="MOCK-ONLY"
                    and receipt["service_now_instance"] is None
                    and not receipt["platform_execution"] and not receipt["customer_approval"],
                    f"{width}px: MIM receipt unsafe classification")
            return receipt
        require(check("COMPLETE")["controls_completed"]==9,
                f"{width}px: initial MIM control count")
        page.locator('[data-fixture="authority"]').click()
        require(set(check("BLOCKED")["blocking_control_ids"])=={"declaration","roles"},
                f"{width}px: MIM authority blockers incorrect")
        page.locator('[data-fixture="integration"]').click()
        check("REVIEW")
        page.locator('[data-gate="entitlement"]').uncheck()
        check("BLOCKED")
        page.locator('[data-gate="entitlement"]').check()
        check("REVIEW")
        page.locator('[data-fixture="complete"]').click()
        check("COMPLETE")
        require(page.locator('[data-fixture="complete"]').get_attribute("aria-pressed")=="true",
                f"{width}px: MIM fixture not focus/selection accessible")
        print(f"PASS {width}px: MIM synthetic gates and receipt")
    finally:
        page.close()

def main():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        try:
            for width in VIEWPORTS:
                check_viewport(browser, width)
                for filename, anchor in CASE_STUDIES:
                    check_case_study(browser, filename, anchor, width)
                check_cmdb_trust_lab(browser, width)
                check_mim_design_lab(browser, width)
        finally:
            browser.close()


if __name__ == "__main__":
    main()

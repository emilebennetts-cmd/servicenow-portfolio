#!/usr/bin/env python3
"""Chromium contract for offline entitlement decisions, not native licensing validation."""
import json
from pathlib import Path

from playwright.sync_api import sync_playwright

URL = (Path(__file__).resolve().parents[1] / "operational-readiness-runbook.html").as_uri()


def verify(browser, width):
    page = browser.new_page(viewport={"width": width, "height": 900},
                            reduced_motion="reduce", accept_downloads=True)
    errors, external = [], []
    page.on("pageerror", lambda error: errors.append(str(error)))
    page.on("request", lambda req: external.append(req.url)
            if req.url.startswith(("https://", "http://")) else None)
    try:
        page.goto(URL, wait_until="domcontentloaded", timeout=30000)
        assert page.locator("#entitlement-cards .entitlement-card").count() == 10
        assert page.locator("#entitlement-count").inner_text() == "0 of 10 self-reported"
        assert not page.locator("#entitlement-export").is_disabled()
        assert page.evaluate("document.documentElement.scrollWidth <= window.innerWidth + 2"), width
        page.get_by_role("button", name="Additional product review").click()
        assert page.locator(".entitlement-card:visible").count() == 7
        page.get_by_role("button", name="All capabilities").click()
        page.locator("#entitlement-state-ENT-01").select_option("SELF_REPORTED_ENTITLED")
        assert page.locator("#entitlement-export").is_disabled()
        assert "ENT-01 requires" in page.locator("#entitlement-status").inner_text()
        alias = page.locator("#entitlement-alias-ENT-01")
        alias.fill("someone@example.com")
        assert page.locator("#entitlement-export").is_disabled()
        alias.fill("LIC_A01")
        assert not page.locator("#entitlement-export").is_disabled()
        page.get_by_role("button", name="Unresolved only").click()
        assert page.locator(".entitlement-card:visible").count() == 9
        with page.expect_download() as info:
            page.locator("#entitlement-export").click()
        item = info.value
        assert item.suggested_filename == "entitlement-review-HOLD.json"
        receipt = json.loads(Path(item.path()).read_text(encoding="utf-8"))
        assert receipt["schema"] == "entitlement-decision-draft-v1"
        for flag in ("contract_verified", "independent_approval", "dev_verified",
                     "production_verified", "installation_executed",
                     "licence_purchase_authorised", "requirement_level_reconciliation_complete"):
            assert receipt[flag] is False, flag
        assert receipt["publication_status"] == "HOLD"
        assert receipt["evidence_class"] == "MOCK-ONLY"
        assert receipt["source_basis"] == "SOURCE-ONLY"
        assert len(receipt["decisions"]) == 10
        assert receipt["decision_count"] == 1
        assert receipt["decisions"][0]["evidence_alias"] == "LIC_A01"
        page.locator("#entitlement-reset").click()
        assert page.locator("#entitlement-count").inner_text() == "0 of 10 self-reported"
        assert page.locator(".entitlement-card:visible").count() == 10
        assert not errors, errors
        assert not external, external
        print(f"PASS entitlement desk {width}px: 10 categories, alias validation, HOLD export, no network")
    finally:
        page.close()


if __name__ == "__main__":
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        try:
            for width in (390, 768, 1024, 1440):
                verify(browser, width)
        finally:
            browser.close()

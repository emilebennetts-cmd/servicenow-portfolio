#!/usr/bin/env python3
"""Browser regression for the public entitlement readiness worksheet.

These tests certify only a static website mock, never native ServiceNow runtime,
product licensing, customer acceptance, screenshot publication or Production.
"""
import json
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]

class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_args):
        pass

def check(browser, base, width):
    page = browser.new_page(viewport={"width": width, "height": 900},
                            accept_downloads=True, reduced_motion="reduce")
    errors = []
    remote = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    page.on("request", lambda r: remote.append(r.url) if not r.url.startswith(base + "/") else None)
    try:
        page.goto(base + "/entitlement-readiness.html", wait_until="load")
        cards = page.locator(".entitlement-card")
        assert cards.count() == 8
        assert page.locator(".entitlement-card:visible").count() == 8
        assert page.locator('[data-domain-filter="all"]').get_attribute("aria-pressed") == "true"
        assert "8 of 8" in page.locator("#filter-status").inner_text()
        page.locator(".entitlement-card details summary").first.click()
        assert page.locator(".entitlement-card details").first.get_attribute("open") is not None

        page.locator('[data-domain-filter="platform"]').click()
        assert page.locator(".entitlement-card:visible").count() == 2
        assert page.locator('[data-domain-filter="platform"]').get_attribute("aria-pressed") == "true"
        page.locator("#triage-WEB-001").select_option("evidence-requested")
        page.locator('[data-domain-filter="operations"]').click()
        assert page.locator(".entitlement-card:visible").count() == 3
        page.locator('[data-domain-filter="extension"]').click()
        assert page.locator(".entitlement-card:visible").count() == 3
        assert "3 of 8" in page.locator("#filter-status").inner_text()
        page.locator("#triage-INT-006").select_option("gap")
        page.locator("#triage-ANA-007").select_option("review-ready")
        assert "1 evidence requested" in page.locator("#triage-status").inner_text()
        assert "1 gaps" in page.locator("#triage-status").inner_text()
        assert "1 materials staged" in page.locator("#triage-status").inner_text()

        with page.expect_download() as pending:
            page.locator("#export-packet").click()
        payload = json.loads(Path(pending.value.path()).read_text(encoding="utf-8"))
        assert payload["source_classification"] == "SOURCE-ONLY"
        assert payload["interaction_classification"] == "MOCK-ONLY"
        assert payload["review_status"] == "UNREVIEWED"
        assert payload["verification_status"] == "NOT VERIFIED"
        assert payload["release_status"] == "HOLD"
        for key in ("native_dev_verified", "production_verified",
                    "screenshot_publication_approved", "licence_approval",
                    "target_instance_approved"):
            assert payload[key] is False, key
        assert [i["id"] for i in payload["items"]] == ["INT-006", "ANA-007", "ATF-008"]
        assert all(i["independent_native_test"] == "NOT RUN" for i in payload["items"])
        assert all(i["approval"] == "HOLD" for i in payload["items"])
        assert payload["reviewer_actions_only"] is True
        stages={i["id"]:i["reviewer_follow_up"] for i in payload["items"]}
        assert stages == {"INT-006":"GAP OR ENTITLEMENT DECISION NEEDED",
                          "ANA-007":"MATERIALS STAGED / REVIEW PENDING",
                          "ATF-008":"NOT ASSESSED"}
        assert all(i["suggested_review_owner"] for i in payload["items"])

        page.locator('[data-domain-filter="all"]').click()
        assert page.locator(".entitlement-card:visible").count() == 8
        assert page.locator("#triage-WEB-001").input_value() == "evidence-requested"
        page.locator("#reset-triage").click()
        assert page.locator("#triage-WEB-001").input_value() == "not-assessed"
        assert page.locator("#triage-INT-006").input_value() == "not-assessed"
        assert "8 not assessed" in page.locator("#triage-status").inner_text()
        assert not remote, remote
        assert not errors, errors
        # Bounding-box width is a conservative smoke check without injecting
        # client JavaScript into a page guarded by a strict CSP.
        assert page.locator("main").bounding_box()["width"] <= width + 2, width
        print("PASS", width, "px: filter, offline export, HOLD, browser privacy")
    finally:
        page.close()

if __name__ == "__main__":
    server = ThreadingHTTPServer(("127.0.0.1", 0),
                                 partial(QuietHandler, directory=str(ROOT)))
    Thread(target=server.serve_forever, daemon=True).start()
    base = "http://127.0.0.1:" + str(server.server_address[1])
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            try:
                for width in (390, 768, 1024, 1440):
                    check(browser, base, width)
            finally:
                browser.close()
    finally:
        server.shutdown()

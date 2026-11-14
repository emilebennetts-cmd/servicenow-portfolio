#!/usr/bin/env python3
"""Same-origin Chromium checks for dated lineage and full public claim catalogue."""
import json
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
REGISTER = json.loads((ROOT / "evidence/public-verification-register.json").read_text(encoding="utf-8"))
CLASS_COUNTS = {
    name: sum(item["classification"] == name for item in REGISTER["items"])
    for name in ("source-only", "DEV-reported", "mock-only", "proposed")
}

class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_args):
        pass

def check(browser, width, base):
    page = browser.new_page(viewport={"width": width, "height": 900}, reduced_motion="reduce", accept_downloads=True)
    errors = []
    page.on("pageerror", lambda error: errors.append(str(error)))
    try:
        page.goto(base + "/technical-evidence-register.html", wait_until="domcontentloaded")
        assert page.locator(".lineage-card").count() == 6
        assert page.locator(".lineage-card:visible").count() == 6
        assert page.evaluate("document.documentElement.scrollWidth <= innerWidth + 2"), width
        page.get_by_role("button", name="Source-only", exact=True).click()
        assert page.locator(".lineage-card:visible").count() == 3
        assert page.locator(".lineage-card[data-class='SOURCE-ONLY']:visible").count() == 3
        assert page.locator("#lineage-count").inner_text().startswith("Showing 3 of 6")
        page.get_by_role("button", name="Source-only", exact=True).get_attribute("aria-pressed") == "true"
        page.get_by_role("button", name="Historical DEV-reported").click()
        assert page.locator(".lineage-card:visible").count() == 3
        assert page.locator(".lineage-card[data-class='DEV-REPORTED']:visible").count() == 3
        page.get_by_role("button", name="All records").click()
        assert page.locator(".lineage-card:visible").count() == 6

        # Full catalogue is rendered from the current checked-in JSON, not a duplicated snapshot.
        page.locator("#claim-count").get_by_text("registered", exact=False).wait_for(timeout=10000)
        assert f"({len(REGISTER['items'])} registered)" in page.locator("#claim-count").inner_text()
        assert page.locator(".catalogue-entry").count() == 12
        page.locator("#claim-more").click()
        assert page.locator(".catalogue-entry").count() == 24
        page.locator("#claim-classification").select_option("DEV-reported")
        assert page.locator(".catalogue-entry").count() == CLASS_COUNTS["DEV-reported"]
        assert all(c == "DEV-reported" for c in page.locator(".catalogue-entry").evaluate_all(
            "(els) => els.map(e => e.dataset.class)"))
        page.locator("#claim-classification").select_option("all")
        page.locator("#claim-search").fill("COVERAGE2-20261113-TECHNICAL_EVIDENCE_REGISTER")
        assert page.locator(".catalogue-entry").count() == 1
        assert "Public technical evidence register" in page.locator(".catalogue-entry h3").inner_text()
        page.locator(".catalogue-entry summary").click()
        assert page.locator(".catalogue-entry dt").count() == 3
        page.locator("#claim-search").fill("NO-SUCH-PUBLIC-CLAIM-XXXXXXXXXXXXXXXXXX")
        assert page.locator(".catalogue-entry").count() == 0
        assert page.locator("#shortlist-export-json").is_disabled()
        assert page.locator("#shortlist-preview li").count() == 0
        assert "Showing 0 of 0 matching" in page.locator("#claim-count").inner_text()
        page.locator("#claim-search").fill("")
        page.locator("#claim-classification").select_option("source-only")
        assert page.locator(".catalogue-entry").count() == 12
        assert "of " + str(CLASS_COUNTS["source-only"]) in page.locator("#claim-count").inner_text()

        # Selection persists across filters and pagination but never becomes approval.
        assert page.locator("#shortlist-export-json").is_disabled()
        first_source_id = page.locator(".catalogue-entry .claim-id").first.inner_text()
        page.locator(".catalogue-entry .claim-choice input").first.check()
        assert "1 selected public claims" in page.locator("#shortlist-count").inner_text()
        page.locator("#claim-classification").select_option("DEV-reported")
        first_dev_id = page.locator(".catalogue-entry .claim-id").first.inner_text()
        page.locator(".catalogue-entry .claim-choice input").first.check()
        assert "2 selected public claims" in page.locator("#shortlist-count").inner_text()
        page.locator("#claim-classification").select_option("source-only")
        assert page.locator(".catalogue-entry .claim-choice input").first.is_checked()
        with page.expect_download() as artifact:
            page.locator("#shortlist-export-json").click()
        packet = json.loads(Path(artifact.value.path()).read_text(encoding="utf-8"))
        assert artifact.value.suggested_filename == "servicenow-public-evidence-briefing.json"
        assert packet["verification_state"] == "NOT VERIFIED"
        assert packet["review_state"] == "UNREVIEWED"
        assert packet["release_state"] == "HOLD"
        assert not packet["native_service_now_execution"]
        assert not packet["independent_review_approved"]
        assert not packet["screenshot_publication_approved"]
        assert [c["id"] for c in packet["claims"]] == [
            c["id"] for c in REGISTER["items"] if c["id"] in {first_source_id, first_dev_id}
        ]
        assert {c["classification"] for c in packet["claims"]} == {"source-only", "DEV-reported"}
        assert all(c["public_url"].startswith(
            "https://emilebennetts-cmd.github.io/servicenow-portfolio/"
        ) for c in packet["claims"])
        with page.expect_download() as document:
            page.locator("#shortlist-export-md").click()
        markdown = Path(document.value.path()).read_text(encoding="utf-8")
        assert "UNREVIEWED / NOT VERIFIED / HOLD" in markdown
        assert first_source_id in markdown and first_dev_id in markdown
        assert "not independently DEV-VERIFIED" in markdown
        page.locator("#shortlist-clear").click()
        assert page.locator("#shortlist-export-json").is_disabled()
        assert page.locator("#shortlist-preview li").count() == 0
        assert not page.locator(".catalogue-entry .claim-choice input").first.is_checked()
        assert page.evaluate("document.documentElement.scrollWidth <= innerWidth + 2"), width
        assert not errors, errors
        print(f"PASS evidence {width}px: lineage filters, {len(REGISTER['items'])} claims, query, pagination, safe rendering")
    finally:
        page.close()

def reject_bad_register(browser, base):
    page = browser.new_page()
    try:
        def poisoned(route):
            route.fulfill(status=200, content_type="application/json", body=json.dumps({
                "schema_version": "1.0",
                "items": [{"id": "BAD", "title": "<script>attack</script>",
                           "classification": "production-verified", "page": "javascript:alert(1)"}]
            }))
        page.route("**/evidence/public-verification-register.json", poisoned)
        page.goto(base + "/technical-evidence-register.html", wait_until="domcontentloaded")
        assert "unavailable" in page.locator("#claim-count").inner_text().lower()
        assert page.locator("#claim-fallback").is_visible()
        assert page.locator(".catalogue-entry").count() == 0
        assert page.locator("script[src='javascript:alert(1)']").count() == 0
        print("PASS evidence schema rejection: malicious record cannot render")
    finally:
        page.close()

if __name__ == "__main__":
    handler = partial(QuietHandler, directory=str(ROOT))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        base = "http://127.0.0.1:" + str(server.server_port)
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            try:
                for width in (390, 768, 1024, 1440):
                    check(browser, width, base)
                reject_bad_register(browser, base)
            finally:
                browser.close()
    finally:
        server.shutdown()
        server.server_close()

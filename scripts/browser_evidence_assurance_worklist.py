#!/usr/bin/env python3
"""Chromium source-only assurance board checks at four viewports and invalid input."""
import json
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
REGISTER = json.loads((ROOT / "evidence/public-verification-register.json").read_text(encoding="utf-8"))

class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_args):
        pass

def verify(browser, base, width):
    page = browser.new_page(viewport={"width": width, "height": 900},
                            reduced_motion="reduce", accept_downloads=True)
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    try:
        page.goto(base + "/evidence-assurance-worklist.html", wait_until="domcontentloaded")
        page.wait_for_function("document.querySelector('#total').textContent === '87'", timeout=10000)
        assert page.locator("#source-count").inner_text() == "54"
        assert page.locator("#mock-count").inner_text() == "20"
        assert page.locator("#reported-count").inner_text() == "4"
        assert page.locator("#proposal-count").inner_text() == "9"
        assert page.locator("#verified-count").inner_text() == "0"
        assert page.locator(".card[data-kind]").count() == 12
        assert page.evaluate("document.documentElement.scrollWidth <= innerWidth + 2"), width

        page.locator("#classification").select_option("DEV-reported")
        assert page.locator(".card[data-kind]").count() == 4
        assert page.locator(".card[data-kind='DEV-reported']").count() == 4
        page.locator("#action-filter").select_option("repeat")
        assert page.locator(".card[data-kind]").count() == 4
        page.locator("#search").fill("NO-MATCH-EXISTING-CLAIM")
        assert page.locator(".card[data-kind]").count() == 0
        assert page.locator("#download").is_disabled()
        page.locator("#clear").click()
        assert page.locator("#search").input_value() == ""
        assert page.locator(".card[data-kind]").count() == 12
        page.locator("#load-more").click()
        assert page.locator(".card[data-kind]").count() == 24

        page.locator("#classification").select_option("mock-only")
        assert page.locator("#status").inner_text().startswith("20 of 87")
        with page.expect_download() as pending:
            page.locator("#download").click()
        downloaded = pending.value
        data = json.loads(Path(downloaded.path()).read_text(encoding="utf-8"))
        assert data["review_state"] == "UNREVIEWED"
        assert data["verification_state"] == "NOT VERIFIED"
        assert data["release_state"] == "HOLD"
        assert data["independent_native_verification"] is False
        assert data["screenshot_publication_approved"] is False
        assert len(data["items"]) == 20
        assert all(entry["classification"] == "mock-only" for entry in data["items"])
        assert not errors, errors
        print(f"PASS {width}px: register totals, filtering, pagination, JSON export and no overflow")
    finally:
        page.close()

def verify_fails_closed(browser, base):
    page = browser.new_page(viewport={"width": 390, "height": 900})
    try:
        corrupt = dict(REGISTER)
        corrupt["items"] = [dict(REGISTER["items"][0]), dict(REGISTER["items"][0])]
        page.route("**/evidence/public-verification-register.json",
                   lambda route: route.fulfill(status=200, content_type="application/json",
                                               body=json.dumps(corrupt)))
        page.goto(base + "/evidence-assurance-worklist.html")
        page.locator("#failure:visible").wait_for(timeout=10000)
        assert page.locator("#download").is_disabled()
        assert page.locator(".card[data-kind]").count() == 0
        assert "no claims inferred" in page.locator("#status").inner_text()
        print("PASS fail-closed: duplicate public claim ID rejected")
    finally:
        page.close()

if __name__ == "__main__":
    server = ThreadingHTTPServer(("127.0.0.1", 0), partial(QuietHandler, directory=str(ROOT)))
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base = "http://127.0.0.1:" + str(server.server_address[1])
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            try:
                for width in (390, 768, 1024, 1440):
                    verify(browser, base, width)
                verify_fails_closed(browser, base)
            finally:
                browser.close()
    finally:
        server.shutdown()

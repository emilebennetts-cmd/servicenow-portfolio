#!/usr/bin/env python3
"""Chromium source-only assurance board checks at four viewports and invalid input."""
import csv
import io
import json
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from playwright.sync_api import sync_playwright, expect

ROOT = Path(__file__).resolve().parents[1]
REGISTER = json.loads((ROOT / "evidence/public-verification-register.json").read_text(encoding="utf-8"))
TOTAL = len(REGISTER["items"])
COUNTS = {kind: sum(item["classification"] == kind for item in REGISTER["items"])
          for kind in REGISTER["classification_definitions"]}

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
        expect(page.locator("#total")).to_have_text(str(TOTAL), timeout=10000)
        assert page.locator("#source-count").inner_text() == str(COUNTS["source-only"])
        assert page.locator("#mock-count").inner_text() == str(COUNTS["mock-only"])
        assert page.locator("#reported-count").inner_text() == str(COUNTS["DEV-reported"])
        assert page.locator("#proposal-count").inner_text() == str(COUNTS["proposed"])
        assert page.locator("#verified-count").inner_text() == str(COUNTS["DEV-verified"] + COUNTS["production-verified"])
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
        assert page.locator("#status").inner_text().startswith(f"{COUNTS['mock-only']} of {TOTAL}")
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
        with page.expect_download() as csv_pending:
            page.locator("#download-csv").click()
        csv_text = Path(csv_pending.value.path()).read_text(encoding="utf-8")
        rows = list(csv.DictReader(io.StringIO(csv_text)))
        assert len(rows) == 20
        assert all(row["classification"] == "mock-only" for row in rows)
        assert all(row["review_state"] == "UNREVIEWED" for row in rows)
        assert all(row["verification_state"] == "NOT VERIFIED" for row in rows)
        assert all(row["release_state"] == "HOLD" for row in rows)
        assert all(row["independent_native_verification"] == "FALSE" for row in rows)
        assert all(row["production_acceptance"] == "FALSE" for row in rows)
        assert all(row["screenshot_publication_approved"] == "FALSE" for row in rows)
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
        assert page.locator("#download-csv").is_disabled()
        assert page.locator(".card[data-kind]").count() == 0
        assert "no claims inferred" in page.locator("#status").inner_text()
        print("PASS fail-closed: duplicate public claim ID rejected")
    finally:
        page.close()


def verify_formula_neutralisation(browser, base):
    page = browser.new_page(viewport={"width": 390, "height": 900}, accept_downloads=True)
    try:
        poisoned = dict(REGISTER)
        poisoned["items"] = [dict(x) for x in REGISTER["items"]]
        poisoned["items"][0]["title"] = '=HYPERLINK("https://example.invalid", "bad")'
        poisoned["items"][1]["title"] = '  -SUM(1+1)'
        page.route("**/evidence/public-verification-register.json",
                   lambda route: route.fulfill(status=200, content_type="application/json",
                                               body=json.dumps(poisoned)))
        page.goto(base + "/evidence-assurance-worklist.html")
        expect(page.locator("#total")).to_have_text(str(TOTAL), timeout=10000)
        with page.expect_download() as pending:
            page.locator("#download-csv").click()
        csv_text = Path(pending.value.path()).read_text(encoding="utf-8")
        rows = list(csv.DictReader(io.StringIO(csv_text)))
        assert len(rows) == TOTAL
        assert rows[0]["title"].startswith("'=HYPERLINK("), rows[0]["title"]
        assert rows[1]["title"].startswith("'  -SUM("), rows[1]["title"]
        assert csv_text.count("\n") >= TOTAL + 1
        print("PASS CSV injection: leading formula and whitespace-prefixed formulas neutralised")
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
                verify_formula_neutralisation(browser, base)
            finally:
                browser.close()
    finally:
        server.shutdown()

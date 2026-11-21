#!/usr/bin/env python3
"""Offline Chromium acceptance of public document currency; never contacts ServiceNow."""
import csv
import io
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from threading import Thread
from urllib.parse import urlsplit
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]

class Quiet(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)
    def log_message(self, *args):
        return

def main():
    server = ThreadingHTTPServer(("127.0.0.1", 0), Quiet)
    Thread(target=server.serve_forever, daemon=True).start()
    base = f"http://127.0.0.1:{server.server_port}"
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            for width in (375, 768, 1024, 1440):
                context = browser.new_context(viewport={"width": width, "height": 850}, accept_downloads=True)
                page = context.new_page()
                errors, outside = [], []
                page.on("pageerror", lambda error: errors.append(str(error)))
                page.on("request", lambda req: outside.append(req.url) if urlsplit(req.url).netloc != urlsplit(base).netloc else None)
                response = page.goto(base + "/documentation-currency-gate.html", wait_until="networkidle")
                assert response and response.ok
                assert page.locator("#records article.doc").count() == 4
                assert page.locator("#matched").inner_text() == "1"
                assert page.locator("#drift").inner_text() == "2"
                assert page.locator("#holds").inner_text() == "4"
                assert "HOLD" in page.locator("#summary").inner_text()
                page.select_option("#target", "4.6.1")
                assert page.locator("#matched").inner_text() == "2"
                assert page.locator("#drift").inner_text() == "1"
                assert "UNVERSIONED / SHOWCASE" in page.locator("#records").inner_text()
                with page.expect_download() as info:
                    page.locator("#export").click()
                dl = info.value
                assert dl.suggested_filename == "documentation-currency-4.6.1-hold.csv"
                raw = Path(dl.path()).read_text("utf-8")
                rows = list(csv.reader(io.StringIO(raw)))
                assert len(rows) == 5 and len(rows[0]) == 9
                assert all(row[6:8] == ["NOT RUN", "HOLD"] for row in rows[1:])
                assert not any(term in raw.lower() for term in ("sys_id", "dev438211", "service-now.com", "drive.google.com"))
                assert page.evaluate("document.documentElement.scrollWidth <= window.innerWidth + 1"), f"Horizontal overflow {width}"
                assert not errors, (width, errors)
                assert not outside, (width, outside)
                context.close()
                print(f"PASS: {width}px, 4 controlled snapshots, stable HOLD CSV, no network egress")
            browser.close()
    finally:
        server.shutdown()
        server.server_close()

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Four-width local-browser contract for CSDM native acceptance preparation."""
import json
from pathlib import Path
from threading import Thread
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from functools import partial
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]

class Quiet(SimpleHTTPRequestHandler):
    def log_message(self, *args): pass

def run(browser, width, url):
    page = browser.new_page(viewport={"width":width,"height":900},accept_downloads=True,reduced_motion="reduce")
    errors = []
    remote = []
    page.on("pageerror",lambda e: errors.append(str(e)))
    page.on("request",lambda r: remote.append(r.url) if not r.url.startswith(url.split("/csdm-native")[0]) and not r.url.startswith("blob:") else None)
    try:
        page.goto(url,wait_until="load")
        assert page.locator(".gate[data-gate]").count() == 6
        assert page.locator("#count-open").inner_text() == "6"
        assert page.locator("#count-staged").inner_text() == "0"
        page.locator("#stage-target").select_option("staged")
        page.locator("#stage-ire").select_option("gap")
        assert page.locator("#count-staged").inner_text() == "1"
        assert page.locator("#count-gap").inner_text() == "1"
        page.locator("#scenario").select_option("identity")
        assert "Conflicting Discovery identities" in page.locator("#scenario-name").inner_text()
        assert page.locator("#count-open").inner_text() == "6"
        page.locator("#stage-health").select_option("requested")
        page.locator("#scenario").select_option("ownership")
        assert page.locator("#stage-target").input_value() == "staged"
        assert page.locator("#stage-ire").input_value() == "gap"
        with page.expect_download() as downloaded:
            page.locator("#export").click()
        packet=json.loads(Path(downloaded.value.path()).read_text(encoding="utf-8"))
        assert packet["schema_version"] == "csdm5-native-acceptance-preparation-v1"
        assert packet["scenario_id"] == "ownership"
        assert len(packet["gates"]) == 6
        assert packet["gates"][0]["stage"] == "staged"
        assert packet["gates"][1]["stage"] == "gap"
        assert packet["evidence_classification"] == "MOCK-ONLY"
        assert packet["native_execution_status"] == "NOT RUN"
        assert packet["native_verification_status"] == "NOT VERIFIED"
        assert packet["independent_review_approved"] is False
        assert packet["production_verified"] is False
        assert packet["publication_status"] == "HOLD"
        assert packet["approval_status"] == "UNREVIEWED"
        page.locator("#reset").click()
        assert page.locator("#count-open").inner_text() == "6"
        page.locator("#scenario").select_option("identity")
        assert page.locator("#stage-health").input_value() == "requested"
        assert page.evaluate("document.documentElement.scrollWidth <= window.innerWidth + 2"), width
        assert not errors,errors
        assert not remote,remote
        print(f"PASS CSDM acceptance {width}px: scenario memory, stages, HOLD JSON, reset, offline and layout")
    finally:
        page.close()

if __name__ == "__main__":
    server=ThreadingHTTPServer(("127.0.0.1",0),partial(Quiet,directory=str(ROOT)))
    thread=Thread(target=server.serve_forever,daemon=True)
    thread.start()
    try:
        with sync_playwright() as play:
            browser=play.chromium.launch(headless=True)
            try:
                for width in (390,768,1024,1440):
                    run(browser,width,"http://127.0.0.1:"+str(server.server_port)+"/csdm-native-acceptance.html")
            finally:
                browser.close()
    finally:
        server.shutdown()

#!/usr/bin/env python3
"""Source-only handoff contract: responsive interaction, export HOLD and no live calls."""
import json
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / "diagnostic-delivery-handoff-contract.html").read_text(encoding="utf-8")

class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, *_args):
        pass

def static_checks():
    assert 'SOURCE-ONLY' in HTML and 'MOCK-ONLY' in HTML
    assert "production_verified:false" in HTML
    assert "native_dev_verified:false" in HTML
    assert "screenshot_publication_approved:false" in HTML
    assert "review_state:'UNREVIEWED'" in HTML
    assert "verification_state:'NOT VERIFIED'" in HTML
    assert "release_state:'HOLD'" in HTML
    assert 'img-src &#39;none&#39;' not in HTML
    assert "img-src 'none'" in HTML
    assert '<iframe' not in HTML.lower()
    assert '<img' not in HTML.lower()
    assert 'localStorage' not in HTML
    assert 'fetch(' not in HTML and 'XMLHttpRequest' not in HTML
    assert 'http://' not in HTML and 'https://' not in HTML
    assert HTML.count('data-lane="') == 4

def run_browser(browser, base, width):
    page = browser.new_page(viewport={"width":width,"height":900},accept_downloads=True,reduced_motion="reduce")
    errors=[]
    page.on("pageerror",lambda e:errors.append(str(e)))
    page.on("request",lambda r: (_ for _ in ()).throw(AssertionError("external request: "+r.url)) if not r.url.startswith(base) else None)
    try:
        page.goto(base+"/diagnostic-delivery-handoff-contract.html")
        assert page.locator(".step").count()==6
        assert page.locator('[data-lane="tier0"]').get_attribute("aria-pressed")=="true"
        assert page.locator("#summary").inner_text().find("NOT VERIFIED")!=-1
        assert page.evaluate("document.documentElement.scrollWidth <= window.innerWidth + 2"),width

        page.locator('[data-lane="offline"]').click()
        assert page.locator(".step[data-state='blocked']").count()==2
        assert page.locator('[data-lane="offline"]').get_attribute("aria-pressed")=="true"
        page.locator('[data-lane="dev"]').click()
        assert page.locator(".step[data-state='required']").count()==6
        page.locator('[data-lane="production"]').click()
        assert page.locator(".step[data-state='blocked']").count()==1
        page.locator("#critical").check()
        assert page.locator(".step").count()==1
        assert page.locator(".step").first.get_attribute("data-state")=="blocked"
        with page.expect_download() as pending:
            page.locator("#export").click()
        payload=json.loads(Path(pending.value.path()).read_text(encoding="utf-8"))
        assert payload["boundary"]=="production"
        assert payload["interaction_classification"]=="MOCK-ONLY"
        assert payload["architecture_classification"]=="SOURCE-ONLY"
        assert payload["review_state"]=="UNREVIEWED"
        assert payload["verification_state"]=="NOT VERIFIED"
        assert payload["release_state"]=="HOLD"
        assert payload["native_dev_verified"] is False
        assert payload["production_verified"] is False
        assert payload["screenshot_publication_approved"] is False
        assert len(payload["records"])==6
        assert payload["records"][-1]["control_state"]=="blocked"
        assert not any("password" in str(x).lower() for x in payload["records"])
        page.locator("#reset").click()
        assert page.locator('[data-lane="tier0"]').get_attribute("aria-pressed")=="true"
        assert page.locator("#critical").is_checked() is False
        assert page.locator(".step").count()==6
        assert not errors,errors
        print("PASS",width,"px: lanes, privacy-bound export, reset, responsive layout")
    finally:
        page.close()

if __name__=="__main__":
    static_checks()
    server=ThreadingHTTPServer(("127.0.0.1",0),partial(QuietHandler,directory=str(ROOT)))
    Thread(target=server.serve_forever,daemon=True).start()
    base="http://127.0.0.1:"+str(server.server_address[1])
    try:
        with sync_playwright() as p:
            browser=p.chromium.launch(headless=True)
            try:
                for width in (390,768,1024,1440):
                    run_browser(browser,base,width)
            finally:
                browser.close()
    finally:
        server.shutdown()

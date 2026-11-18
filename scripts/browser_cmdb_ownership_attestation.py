#!/usr/bin/env python3
"""Browser acceptance for a synthetic CMDB ownership lab; no external network or native ServiceNow access."""
import csv
import io
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from threading import Thread
from urllib.parse import urlsplit
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
class Quiet(SimpleHTTPRequestHandler):
    def __init__(self,*a,**kw): super().__init__(*a,directory=str(ROOT),**kw)
    def log_message(self,*args): return

def main():
    server=ThreadingHTTPServer(("127.0.0.1",0),Quiet)
    thread=Thread(target=server.serve_forever,daemon=True);thread.start()
    base=f"http://127.0.0.1:{server.server_port}"
    try:
        with sync_playwright() as p:
            browser=p.chromium.launch(headless=True)
            for width in (375,768,1024,1440):
                context=browser.new_context(viewport={"width":width,"height":900},accept_downloads=True)
                page=context.new_page()
                errors=[]; external=[]
                page.on("pageerror",lambda err: errors.append(str(err)))
                page.on("request",lambda r: external.append(r.url) if urlsplit(r.url).netloc!=urlsplit(base).netloc else None)
                response=page.goto(base+"/cmdb-ownership-attestation-lab.html",wait_until="networkidle")
                assert response and response.ok, f"Failed page load at {width}"
                assert page.locator("tbody#gate-rows tr").count()==6
                assert page.locator("#outcome").inner_text()=="HOLD — REMEDIATE"
                assert page.locator("#gate-count").inner_text().startswith("3 / 6")
                for scenario,required in [
                    ("source-conflict","Authoritative source reconciliation"),
                    ("stale-attestation","Attestation currency"),
                    ("criticality-gap","Business criticality rationale"),
                    ("self-approval","Independent review boundary")
                ]:
                    page.locator('button[data-id="'+scenario+'"]').click()
                    assert "HOLD" in page.locator("#outcome").inner_text(),scenario
                    assert required in page.locator("#reason").inner_text(),scenario
                    assert page.locator("tbody#gate-rows tr").count()==6
                page.locator('button[data-id="ready-candidate"]').click()
                assert page.locator("#outcome").inner_text()=="CANDIDATE FOR NATIVE REVIEW"
                assert page.locator("#gate-count").inner_text().startswith("6 / 6")
                with page.expect_download() as download_info:
                    page.locator("#export").click()
                download=download_info.value
                assert "hold.csv" in download.suggested_filename
                data=Path(download.path()).read_text(encoding="utf-8-sig")
                rows=list(csv.reader(io.StringIO(data)))
                assert len(rows)==7 and all(r[-3:]==["MOCK-ONLY","NOT RUN","HOLD"] for r in rows[1:])
                assert not any(term in data.lower() for term in ("sys_id","token","credential","production-verified"))
                assert page.evaluate("document.documentElement.scrollWidth <= window.innerWidth + 1"),f"Horizontal overflow {width}"
                assert not errors,(width,errors)
                assert not external,(width,external)
                context.close()
                print(f"PASS: {width}px, 6 synthetic cases and HOLD-only CSV, no external requests")
            browser.close()
    finally:
        server.shutdown();server.server_close()

if __name__=="__main__": main()

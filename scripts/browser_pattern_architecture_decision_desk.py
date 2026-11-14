#!/usr/bin/env python3
"""Chromium browser assurance for local-only pattern architectural decisions.

Passing does not constitute native ServiceNow acceptance.
"""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
URL=(ROOT / "reusable-delivery-patterns-case-study.html").as_uri()

def verify(browser,width):
    page=browser.new_page(viewport={"width":width,"height":900},
                          reduced_motion="reduce",accept_downloads=True)
    failures, outbound=[], []
    page.on("pageerror",lambda e:failures.append(str(e)))
    page.on("request",lambda r:outbound.append(r.url)
            if r.url.startswith(("http://","https://")) else None)
    try:
        page.goto(URL,wait_until="domcontentloaded")
        assert page.locator("#pattern-fit-desk").is_visible()
        assert page.locator("#fit-status").inner_text()=="HOLD — 5 evidence gates open"
        assert page.evaluate("() => document.documentElement.scrollWidth <= innerWidth + 2"),width
        page.locator("#fit-scenario").select_option("cmdb")
        assert "IRE" in page.locator("#fit-context").inner_text()
        assert "Service Graph Connectors" in page.locator("#fit-ootb").inner_text()
        page.locator("#fit-approach").select_option("pattern")
        assert "6 evidence gates open" in page.locator("#fit-status").inner_text()
        for label in ("owner","baseline","entitlement","security","acceptance","exception"):
            page.locator(f'[data-fit-check="{label}"]').check()
        assert "PREPARED FOR INDEPENDENT REVIEW" in page.locator("#fit-status").inner_text()
        with page.expect_download() as event:
            page.locator("#fit-export").click()
        download=event.value
        assert download.suggested_filename=="pattern-architecture-decision-draft.json"
        packet=json.loads(Path(download.path()).read_text(encoding="utf-8"))
        assert packet["scenario"]=="cmdb"
        assert packet["proposed_approach"]=="pattern"
        assert packet["preparation_complete"] is True
        assert packet["open_gates"]==[]
        assert packet["classification"]=="mock-only"
        assert packet["review_state"]=="UNREVIEWED"
        assert packet["verification_state"]=="NOT VERIFIED"
        assert packet["release_state"]=="HOLD"
        for key in ("native_service_now_execution","independent_review_approved",
                    "production_verified","public_screenshot_approved"):
            assert packet[key] is False,key
        assert "dev438211" not in json.dumps(packet)
        # Offline roundtrip: a completed mock review can be resumed from its own
        # exported packet, without promoting any attestation flags.
        page.locator("#fit-reset").click()
        assert page.locator("#fit-scenario").input_value()=="mim"
        page.locator("#fit-import-file").set_input_files({
            "name":"review.json","mimeType":"application/json",
            "buffer":json.dumps(packet).encode("utf-8")})
        page.wait_for_function("document.querySelector('#fit-export-feedback').textContent.includes('Draft restored')")
        assert page.locator("#fit-scenario").input_value()=="cmdb"
        assert page.locator("#fit-approach").input_value()=="pattern"
        assert "PREPARED FOR INDEPENDENT REVIEW" in page.locator("#fit-status").inner_text()
        for label in ("owner","baseline","entitlement","security","acceptance","exception"):
            assert page.locator(f'[data-fit-check="{label}"]').is_checked()
        # Tampering, unknown selectors, extra fields, invalid JSON and oversize
        # files fail closed and leave previously selected controls untouched.
        invalid=[
            dict(packet,review_state="APPROVED"),
            dict(packet,production_verified=True),
            dict(packet,scenario="fake"),
            dict(packet,prepared_checks=["owner","owner"]),
            dict(packet,unexpected_private_field="unsafe"),
        ]
        for idx,entry in enumerate(invalid):
            page.locator("#fit-import-file").set_input_files({
                "name":f"tampered-{idx}.json","mimeType":"application/json",
                "buffer":json.dumps(entry).encode("utf-8")})
            page.wait_for_function("document.querySelector('#fit-export-feedback').textContent.includes('Import rejected')")
            assert page.locator("#fit-scenario").input_value()=="cmdb"
            assert page.locator("#fit-approach").input_value()=="pattern"
            assert "PREPARED FOR INDEPENDENT REVIEW" in page.locator("#fit-status").inner_text()
        for name,data in [("malformed.json",b"{bad json"),("oversize.json",b" "*16385)]:
            page.locator("#fit-import-file").set_input_files({
                "name":name,"mimeType":"application/json","buffer":data})
            page.wait_for_function("document.querySelector('#fit-export-feedback').textContent.includes('Import rejected')")
            assert page.locator("#fit-scenario").input_value()=="cmdb"
        page.locator('[data-fit-check="exception"]').uncheck()
        page.locator("#fit-approach").select_option("ootb")
        assert "PREPARED FOR INDEPENDENT REVIEW" in page.locator("#fit-status").inner_text()
        page.locator("#fit-approach").select_option("extension")
        assert "HOLD — 1 evidence gate open"==page.locator("#fit-status").inner_text()
        page.locator("#fit-reset").click()
        assert page.locator("#fit-scenario").input_value()=="mim"
        assert page.locator("#fit-approach").input_value()=="ootb"
        assert "HOLD — 5 evidence gates open"==page.locator("#fit-status").inner_text()
        assert page.evaluate("() => document.documentElement.scrollWidth <= innerWidth + 2"),width
        assert not failures,failures
        assert not outbound,outbound
        print(f"PASS pattern decision desk {width}px: 3 scenarios, 3 options, conservative HOLD export, tamper-resistant offline import, reset")
    finally:
        page.close()

if __name__=="__main__":
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True)
        try:
            for width in (390,768,1024,1440):
                verify(browser,width)
        finally:
            browser.close()

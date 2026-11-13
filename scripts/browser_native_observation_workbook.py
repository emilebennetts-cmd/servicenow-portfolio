#!/usr/bin/env python3
"""Exercise 29 candidate observation controls with Chromium; never test ServiceNow."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

URL = (Path(__file__).resolve().parents[1] / "incident-pack-native-pilot.html").as_uri()

def verify(browser, width):
    page = browser.new_page(viewport={"width":width,"height":900},accept_downloads=True,reduced_motion="reduce")
    errors=[]
    page.on("pageerror", lambda error:errors.append(str(error)))
    try:
        page.goto(URL,wait_until="domcontentloaded",timeout=30000)
        assert page.locator("#obs-cases .obs-card").count()==29
        assert page.locator("#obs-notrun").inner_text()=="29"
        assert page.evaluate("document.documentElement.scrollWidth <= innerWidth + 2"), width
        first=page.locator("#obs-cases .obs-card").first
        first.locator("select").select_option("OBSERVED PASS")
        assert page.locator("#obs-pass").inner_text()=="1"
        assert page.locator("#obs-missing").inner_text()=="1"
        assert first.locator("input").get_attribute("aria-invalid")=="true"
        first.locator("input").fill("EV-NV-001")
        assert page.locator("#obs-missing").inner_text()=="0"
        page.locator("#obs-environment").fill("DEV-LAB-01")
        page.locator("#obs-version").fill("4.22.8")
        page.locator("#obs-scope").fill("x_example_scope")
        page.locator("#obs-commit").fill("a"*40)
        second=page.locator("#obs-cases .obs-card").nth(1)
        second.locator("select").select_option("BLOCKED")
        assert page.locator("#obs-blocked").inner_text()=="1"
        with page.expect_download() as outcome:
            page.locator("#obs-export").click()
        download=outcome.value
        assert download.suggested_filename=="native-observation-candidate-UNREVIEWED-HOLD.json"
        packet=json.loads(Path(download.path()).read_text(encoding="utf-8"))
        assert len(packet["observations"])==29
        assert packet["native_verification_status"]=="NOT VERIFIED"
        assert packet["independent_review_approved"] is False
        assert packet["release_authorised"] is False
        assert packet["publication_status"]=="HOLD"
        assert packet["missing_evidence_aliases"]==["NV-002"]
        assert packet["context"]["source_commit_sha"]=="a"*40
        assert packet["observations"][0]["status"]=="OBSERVED PASS"
        assert packet["observations"][0]["evidence_alias"]=="EV-NV-001"
        assert packet["observations"][0]["dev_verified"] is False
        assert packet["observations"][1]["evidence_missing"] is True
        assert page.locator("#obs-notrun").inner_text()=="27"
        page.locator("#obs-reset").click()
        assert page.locator("#obs-notrun").inner_text()=="29"
        assert page.locator("#obs-pass").inner_text()=="0"
        assert page.locator("#obs-environment").input_value()==""
        # Import the packet exported above; a new session can resume offline without
        # confusing reported observations with verified native evidence.
        def upload(raw):
            if isinstance(raw, dict):
                raw=json.dumps(raw).encode("utf-8")
            page.locator("#obs-import-file").set_input_files({
                "name":"candidate.json", "mimeType":"application/json", "buffer":raw
            })
            page.wait_for_function("document.querySelector('#obs-import-status').textContent.includes('Restored') || document.querySelector('#obs-import-status').textContent.includes('rejected')")
        upload(packet)
        assert "Restored 29" in page.locator("#obs-import-status").inner_text()
        assert page.locator("#obs-notrun").inner_text()=="27"
        assert page.locator("#obs-pass").inner_text()=="1"
        assert page.locator("#obs-blocked").inner_text()=="1"
        assert page.locator("#obs-missing").inner_text()=="1"
        assert first.locator("input").input_value()=="EV-NV-001"
        assert page.locator("#obs-environment").input_value()=="DEV-LAB-01"
        assert page.locator("#obs-import-file").input_value()==""

        # Each rejected import must be atomic; preserve previously restored notes.
        import copy
        failures=[]
        forged=copy.deepcopy(packet)
        forged["native_verification_status"]="DEV-VERIFIED"
        failures.append(forged)
        forged=copy.deepcopy(packet)
        forged["release_authorised"]=True
        failures.append(forged)
        duplicate=copy.deepcopy(packet)
        duplicate["observations"][1]["case_id"]="NV-001"
        failures.append(duplicate)
        contaminated=copy.deepcopy(packet)
        contaminated["context"]["instance_url"]="https://private.example"
        failures.append(contaminated)
        contaminated=copy.deepcopy(packet)
        contaminated["observations"][0]["evidence_alias"]="https://private.example"
        failures.append(contaminated)
        inconsistent=copy.deepcopy(packet)
        inconsistent["missing_evidence_aliases"]=[]
        failures.append(inconsistent)
        failures.extend([b"{", b"x"*131073])
        for invalid in failures:
            # Clear the previous message before the change so each new result is observed.
            page.evaluate("document.querySelector('#obs-import-status').textContent='Checking packet…'")
            upload(invalid)
            assert "rejected" in page.locator("#obs-import-status").inner_text()
            assert page.locator("#obs-import-status").get_attribute("data-error")=="true"
            assert page.locator("#obs-pass").inner_text()=="1"
            assert page.locator("#obs-blocked").inner_text()=="1"
            assert page.locator("#obs-environment").input_value()=="DEV-LAB-01"
            assert first.locator("input").input_value()=="EV-NV-001"
        page.locator("#obs-reset").click()
        assert page.locator("#obs-notrun").inner_text()=="29"
        assert page.locator("#obs-environment").input_value()==""
        assert not errors,errors
        print(f"PASS native candidate workbook {width}px: 29 cases, validation, HOLD export, offline resume, malicious-file rejection, reset")
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

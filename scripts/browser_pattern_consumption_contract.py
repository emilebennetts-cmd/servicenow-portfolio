#!/usr/bin/env python3
"""Four-viewport offline Chromium verification of typed pattern consumption gates."""
import csv
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT=Path(__file__).resolve().parents[1]
URL=(ROOT/"pattern-library.html").as_uri()

def verify(browser,width):
    page=browser.new_page(viewport={"width":width,"height":880},accept_downloads=True,reduced_motion="reduce")
    errors,external=[],[]
    page.on("pageerror",lambda e:errors.append(str(e)))
    page.on("request",lambda req:external.append(req.url) if req.url.startswith(("http://","https://")) else None)
    try:
        page.goto(URL,wait_until="domcontentloaded")
        assert page.locator("#consumption-contract").is_visible()
        assert page.locator("#consumption-lanes .lane").count()==6
        assert "RELEASE HOLD" in page.locator("#consumption-summary").inner_text()
        assert "SOURCE ITEM MISSING" in page.locator("#consumption-lanes").inner_text()
        cases=[
            ("draft-pack","3 supplied source items","HOLD - REVIEW PREREQUISITES"),
            ("governed-draft","6 supplied source items","DRAFT ELIGIBLE - SYNTHETIC ONLY"),
            ("no-parent","6 supplied source items","BLOCKED - PARENT UNRESOLVED"),
            ("parent-only","0 supplied source items","BLOCKED - SOURCE ITEM MISSING"),
        ]
        for key,headline,disposition in cases:
            button=page.locator(f'[data-contract-example="{key}"]')
            button.click()
            assert button.get_attribute("aria-pressed")=="true",key
            assert headline in page.locator("#consumption-feedback").inner_text(),key
            assert disposition in page.locator("#consumption-lanes").inner_text(),key
            assert "RELEASE HOLD" in page.locator("#consumption-summary").inner_text(),key
        page.locator('[data-contract-example="governed-draft"]').click()
        with page.expect_download() as event:
            page.locator("#consumption-csv").click()
        download=event.value
        assert download.suggested_filename=="synthetic-pattern-consumption-governed-draft-hold.csv"
        text=Path(download.path()).read_text(encoding="utf-8-sig")
        rows=list(csv.DictReader(text.splitlines()))
        assert len(rows)==6
        assert len({row["source_type"] for row in rows})==6
        assert all(row["release"]=="HOLD" and row["native_execution"]=="NOT RUN" and row["evidence_class"]=="MOCK-ONLY" for row in rows)
        assert not any(token in text.lower() for token in ("sys_id","customer","instance_url","screenshot_url","credential"))
        assert page.evaluate("document.documentElement.scrollWidth <= window.innerWidth + 2"),width
        assert not errors,errors
        assert not external,external
        print(f"PASS pattern consumption {width}px: four synthetic cases, 6-row HOLD export, no overflow or network")
    finally:
        page.close()

if __name__=="__main__":
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True)
        try:
            for width in (375,768,1024,1440):verify(browser,width)
        finally:
            browser.close()

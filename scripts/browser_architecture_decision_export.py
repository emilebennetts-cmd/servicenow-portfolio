#!/usr/bin/env python3
"""Four-viewport browser acceptance of public source-only CSV, not native ServiceNow."""
import csv
from pathlib import Path
from playwright.sync_api import sync_playwright

URL=(Path(__file__).resolve().parents[1]/"architecture-decision-register.html").as_uri()

def verify(browser,width):
    page=browser.new_page(viewport={"width":width,"height":900},accept_downloads=True,reduced_motion="reduce")
    errors=[]; external=[]
    page.on("pageerror",lambda e:errors.append(str(e)))
    page.on("request",lambda r:external.append(r.url) if r.url.startswith(("http://","https://")) else None)
    try:
        page.goto(URL,wait_until="domcontentloaded")
        assert page.locator(".decision:visible").count()==8
        assert "8 of 8" in page.locator("#result-count").inner_text()
        assert page.evaluate("document.documentElement.scrollWidth <= innerWidth+2"),width
        def export():
            with page.expect_download() as event:page.locator("#export-review").click()
            item=event.value
            assert item.suggested_filename=="architecture-acceptance-HOLD.csv"
            with open(item.path(),newline="",encoding="utf-8-sig") as f:return list(csv.DictReader(f))
        rows=export()
        assert len(rows)==8
        assert [r["adr_id"] for r in rows]==[f"ADR-{n:02}" for n in range(1,9)]
        for r in rows:
            assert set(r)=={"adr_id","domain","decision","risk_controlled","native_acceptance_gate","source_classification","native_test_state","dev_verified","production_verified","publication_state"}
            assert r["risk_controlled"] and r["native_acceptance_gate"]
            assert r["source_classification"]=="SOURCE-ONLY"
            assert r["native_test_state"]=="NOT RUN"
            assert r["dev_verified"]=="false" and r["production_verified"]=="false"
            assert r["publication_state"]=="HOLD"
        page.locator('[data-filter="integration"]').click()
        found=page.locator(".decision:visible")
        expected=[found.nth(i).get_attribute("id").upper() for i in range(found.count())]
        assert 0<len(expected)<8
        assert [r["adr_id"] for r in export()]==expected
        page.locator("#decision-search").fill("no_matches_987")
        assert page.locator(".decision:visible").count()==0
        assert page.locator("#export-review").is_disabled()
        assert page.locator("#empty").is_visible()
        page.locator("#decision-search").fill("")
        page.locator('[data-filter="all"]').click()
        assert not page.locator("#export-review").is_disabled()
        assert len(export())==8
        assert not errors,errors
        assert not external,external
        print(f"PASS architecture review export {width}px: filtered CSV, HOLD gating, no network")
    finally:page.close()

if __name__=="__main__":
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True)
        try:
            for width in (390,768,1024,1440):verify(browser,width)
        finally:browser.close()

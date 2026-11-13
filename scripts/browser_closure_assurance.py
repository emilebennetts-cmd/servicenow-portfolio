#!/usr/bin/env python3
"""Chromium interactive closure exercise; never a native ServiceNow acceptance test."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

URL = (Path(__file__).resolve().parents[1] / 'delivery-case-study.html').as_uri()

def verify(browser,width):
    page=browser.new_page(viewport={'width':width,'height':900},accept_downloads=True,reduced_motion='reduce')
    errors=[]
    page.on('pageerror',lambda e:errors.append(str(e)))
    try:
        page.goto(URL,wait_until='domcontentloaded',timeout=30000)
        assert page.locator('#closure-checklist input[type=checkbox]').count()==9
        assert '0 of 9' in page.locator('#closure-count').inner_text()
        assert '9 preparation blockers' in page.locator('#closure-state').inner_text()
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth + 2'),width
        page.locator('#closure-scenario').select_option('documents')
        assert '6 preparation blockers' in page.locator('#closure-state').inner_text()
        page.locator('#closure-scenario').select_option('ready')
        assert 'Eligible to request independent review' in page.locator('#closure-state').inner_text()
        assert 'NOT APPROVED' in page.locator('#closure-state').inner_text()
        with page.expect_download() as info:
            page.locator('#closure-export').click()
        download=info.value
        assert download.suggested_filename=='handover-closure-preparation-HOLD.json'
        data=json.loads(Path(download.path()).read_text(encoding='utf-8'))
        assert data['synthetic_preparation_ready'] is True
        assert data['publication_status']=='HOLD' and data['native_test_status']=='NOT RUN'
        assert len(data['controls'])==9
        for flag in ('approval_request_submitted','independent_closure_approved',
                     'actual_document_issue_verified','actual_owner_acceptance_verified',
                     'dev_verified','production_verified'):
            assert data[flag] is False,flag
        page.locator('#closure-transition').uncheck()
        assert '1 preparation blocker' in page.locator('#closure-state').inner_text()
        assert page.locator('#closure-scenario').input_value()=='custom'
        page.locator('#closure-reset').click()
        assert '9 preparation blockers' in page.locator('#closure-state').inner_text()
        assert page.locator('#closure-scenario').input_value()=='draft'
        assert not errors,errors
        print(f'PASS closure assurance {width}px: nine gates, seven fixtures, HOLD-only receipt')
    finally:
        page.close()

if __name__=='__main__':
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True)
        try:
            for width in (390,768,1024,1440):verify(browser,width)
        finally:browser.close()

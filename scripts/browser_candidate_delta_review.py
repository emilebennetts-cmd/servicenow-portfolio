#!/usr/bin/env python3
"""Browser-local candidate delta contract regression; never connects to ServiceNow."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
WORKBOOK = (ROOT / "incident-pack-native-pilot.html").as_uri()
DELTA = (ROOT / "candidate-delta-review.html").as_uri()

def candidate(page, *, first="NOT RUN", second="NOT RUN", alias=""):
    page.goto(WORKBOOK, wait_until="domcontentloaded")
    assert page.locator("#obs-cases .obs-card").count() == 29
    first_card = page.locator("#obs-cases .obs-card").nth(0)
    second_card = page.locator("#obs-cases .obs-card").nth(1)
    first_card.locator("select").select_option(first)
    if alias:
        first_card.locator("input").fill(alias)
    second_card.locator("select").select_option(second)
    with page.expect_download() as saved:
        page.locator("#obs-export").click()
    packet = json.loads(Path(saved.value.path()).read_text(encoding="utf-8"))
    assert packet["publication_status"] == "HOLD"
    return packet

def upload(page, selector, packet):
    page.locator(selector).set_input_files({
        "name": "candidate.json", "mimeType": "application/json",
        "buffer": json.dumps(packet).encode("utf-8")
    })

def verify(browser, width):
    page = browser.new_page(viewport={"width": width, "height": 900},
                            accept_downloads=True, reduced_motion="reduce")
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    try:
        old = candidate(page, first="OBSERVED PASS", alias="EV-001")
        new = candidate(page, first="OBSERVED FAIL", second="BLOCKED")
        assert old["observations"][0]["status"] == "OBSERVED PASS"
        page.goto(DELTA, wait_until="domcontentloaded")
        assert page.evaluate("document.documentElement.scrollWidth <= innerWidth + 2"), width
        upload(page, "#baseline", old)
        upload(page, "#current", new)
        page.locator("#run").click()
        assert page.locator("#outcome").is_visible()
        assert page.locator("#total").inner_text() == "2"
        assert page.locator("#risk").inner_text() == "2"
        assert page.locator("#alias").inner_text() == "1"
        assert page.locator("#results li").count() == 29
        page.locator("#filter").select_option("changed")
        assert page.locator("#results li").count() == 2
        page.locator("#filter").select_option("attention")
        assert page.locator("#results li").count() == 2
        with page.expect_download() as saved:
            page.locator("#download").click()
        delta = json.loads(Path(saved.value.path()).read_text(encoding="utf-8"))
        assert delta["native_verification_status"] == "NOT VERIFIED"
        assert delta["independent_review_approved"] is False
        assert delta["production_verified"] is False
        assert delta["publication_status"] == "HOLD"
        assert delta["status_changes"] == 2
        assert not any("evidence_alias" in c for c in delta["cases"])
        # Forged candidate must fail closed and clear the rendered delta.
        forged = json.loads(json.dumps(new))
        forged["independent_review_approved"] = True
        upload(page, "#current", forged)
        page.locator("#run").click()
        assert page.locator("#outcome").is_hidden()
        assert page.locator("#download").is_disabled()
        assert "rejected" in page.locator("#status").inner_text().lower()
        # Content tampering must fail independently of approval flags.
        tampered = json.loads(json.dumps(new))
        tampered["observations"][0]["planned_control"] = "Forged control"
        upload(page, "#current", tampered)
        page.locator("#run").click()
        assert page.locator("#outcome").is_hidden()
        upload(page, "#current", new)
        page.locator("#run").click()
        assert page.locator("#outcome").is_visible()
        page.locator("#reset").click()
        assert page.locator("#outcome").is_hidden()
        assert page.locator("#download").is_disabled()
        assert page.locator("#baseline").input_value() == ""
        assert not errors, errors
        print(f"PASS delta review {width}px: 29-case alignment, filter, HOLD export, forged rejection, reset")
    finally:
        page.close()

if __name__ == "__main__":
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        try:
            for width in (390, 768, 1024, 1440):
                verify(browser, width)
        finally:
            browser.close()

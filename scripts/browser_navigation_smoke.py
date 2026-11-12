#!/usr/bin/env python3
"""Browser-level responsive navigation verification — no screenshot capture.

Execute only after `pip install playwright` and `playwright install chromium`.
The test serves local public HTML via file:// and never logs in to ServiceNow,
opens private source documents, or creates public image artifacts.
"""
from pathlib import Path
import json
from playwright.sync_api import sync_playwright

INDEX_URL = (Path(__file__).resolve().parents[1] / "index.html").as_uri()
VIEWPORTS = (390, 768, 1024, 1440)


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def check_viewport(browser, width):
    page = browser.new_page(
        viewport={"width": width, "height": 900},
        device_scale_factor=1,
        reduced_motion="reduce",
    )
    try:
        page.goto(INDEX_URL, wait_until="domcontentloaded", timeout=30000)
        summary = page.locator(".mobile-directory > summary")
        primary = page.locator("nav.nav")
        directory = page.locator("nav.mobile-links")

        require(summary.is_visible(), f"{width}px: full-directory disclosure is hidden")
        require(primary.is_visible() == (width > 980),
                f"{width}px: primary nav visibility does not match breakpoint")
        require(
            page.evaluate(
                "() => document.querySelector('header.top').scrollWidth <= window.innerWidth + 2"
            ),
            f"{width}px: header content overflows the viewport",
        )

        summary.click()
        require(page.locator(".mobile-directory").evaluate("(el) => el.open"),
                f"{width}px: directory did not open")
        require(directory.is_visible(), f"{width}px: directory links are not visible")
        box = directory.bounding_box()
        require(box is not None, f"{width}px: directory has no visible bounds")
        require(
            box["x"] >= -1 and box["x"] + box["width"] <= width + 1,
            f"{width}px: directory extends outside screen: {box}",
        )

        # Native disclosure + existing Escape handler must be keyboard-operable.
        page.keyboard.press("Escape")
        require(not page.locator(".mobile-directory").evaluate("(el) => el.open"),
                f"{width}px: Escape did not close directory")
        require(summary.evaluate("(el) => document.activeElement === el"),
                f"{width}px: keyboard focus was not returned to menu trigger")

        summary.click()
        directory.locator('a[href="visual-evidence.html"]').click()
        page.wait_for_url("**/visual-evidence.html", timeout=12000)
        require("visual-evidence.html" in page.url,
                f"{width}px: public visual-evidence route could not be opened")
        print(f"PASS {width}px: responsive header, menu bounds, Escape/focus and evidence route")
    finally:
        page.close()



CASE_STUDIES = (
    ("diagnostic-workbench-case-study.html", "implementation"),
    ("reusable-delivery-patterns-case-study.html", "build-map"),
    ("cmdb-ire-assurance.html", "metrics"),
)


def check_case_study(browser, filename, anchor, width):
    """Inspect the actual local HTML in Chromium; never ingest private captures."""
    url = (Path(__file__).resolve().parents[1] / filename).as_uri()
    page = browser.new_page(
        viewport={"width": width, "height": 900},
        device_scale_factor=1,
        reduced_motion="reduce",
    )
    try:
        page.goto(url, wait_until="domcontentloaded", timeout=30000)
        require(page.locator("h1").count() == 1, f"{filename}: expected one page title")
        require(page.locator("main").count() == 1, f"{filename}: expected one main landmark")
        require(
            page.evaluate("() => document.documentElement.scrollWidth <= window.innerWidth + 2"),
            f"{filename} at {width}px: horizontal document overflow",
        )
        text = page.locator("body").inner_text()
        for classification in ("SOURCE-ONLY", "DEV-VERIFIED", "MOCK-ONLY", "PRODUCTION-VERIFIED"):
            require(classification in text, f"{filename}: missing {classification} boundary")
        require(
            "not" in text.lower() and "screenshot" in text.lower(),
            f"{filename}: missing screenshot publication boundary",
        )
        page.locator(f'a[href="#{anchor}"]').click()
        require(page.url.endswith(f"#{anchor}"), f"{filename}: broken architecture anchor")
        require(page.locator(f"#{anchor}").count() == 1, f"{filename}: missing architecture section")
        require(
            page.locator(f"#{anchor}").evaluate("(el) => el.getBoundingClientRect().width > 0"),
            f"{filename}: architecture section is not rendered",
        )
        print(f"PASS {width}px: {filename} document bounds, provenance and architecture link")
    finally:
        page.close()


def check_cmdb_trust_lab(browser, width):
    """Exercise synthetic fixture decisions: no ServiceNow calls or captures."""
    url = (Path(__file__).resolve().parents[1] / "cmdb-diagnostic-trust-lab.html").as_uri()
    page = browser.new_page(
        viewport={"width": width, "height": 900},
        device_scale_factor=1,
        reduced_motion="reduce",
    )
    try:
        page.goto(url, wait_until="domcontentloaded", timeout=30000)
        require(page.locator("h1").count() == 1, f"{width}px: Trust Lab title absent")
        require(page.locator("main").count() == 1, f"{width}px: Trust Lab main absent")
        require(page.evaluate(
            "() => document.documentElement.scrollWidth <= window.innerWidth + 2"
        ), f"{width}px: Trust Lab horizontal overflow")
        require(page.locator("#overall-status").inner_text() == "PASS",
                f"{width}px: initial fixture should PASS")
        cases = (
            ("truncated", "PARTIAL", 0),
            ("unavailable", "NOT ASSESSED", None),
            ("overlap", "REVIEW", 7),
            ("ownership", "REVIEW", 0),
        )
        for key, expected, relation_count in cases:
            button = page.locator('[data-scenario="' + key + '"]')
            button.click()
            require(button.get_attribute("aria-pressed") == "true",
                    f"{width}px: {key} not selected")
            require(page.locator("#overall-status").inner_text() == expected,
                    f"{width}px: {key} status incorrect")
            receipt = json.loads(page.locator("#fixture-receipt").inner_text())
            require(receipt["fixture"] == key
                    and receipt["assessment_status"] == expected
                    and receipt["evidence_class"] == "MOCK-ONLY"
                    and receipt["service_now_instance"] == "none",
                    f"{width}px: {key} receipt invalid")
            require(receipt["distinct_incomplete_relationships"] == relation_count,
                    f"{width}px: {key} relationship union invalid")
        page.locator('[data-scenario="baseline"]').click()
        require(page.locator("#overall-status").inner_text() == "PASS",
                f"{width}px: baseline did not restore")
        print(f"PASS {width}px: CMDB Trust Lab fixture decisions and mobile bounds")
    finally:
        page.close()



def check_mim_design_lab(browser, width):
    """Test synthetic MIM gate decisions and receipt, never ServiceNow execution."""
    url = (Path(__file__).resolve().parents[1] / "major-incident-implementation-lab.html").as_uri()
    page = browser.new_page(viewport={"width": width, "height": 900}, reduced_motion="reduce")
    try:
        page.goto(url, wait_until="domcontentloaded", timeout=30000)
        require(page.locator("h1").count()==1 and page.locator("main").count()==1,
                f"{width}px: MIM page landmarks")
        require(page.evaluate("() => document.documentElement.scrollWidth <= window.innerWidth + 2"),
                f"{width}px: MIM page horizontal overflow")
        def check(expected):
            receipt=json.loads(page.locator("#readiness-receipt").inner_text())
            require(receipt["readiness_status"]==expected, f"{width}px: expected {expected}")
            require(receipt["evidence_class"]=="MOCK-ONLY"
                    and receipt["service_now_instance"] is None
                    and not receipt["platform_execution"] and not receipt["customer_approval"],
                    f"{width}px: MIM receipt unsafe classification")
            return receipt
        require(check("COMPLETE")["controls_completed"]==9,
                f"{width}px: initial MIM control count")
        page.locator('[data-fixture="authority"]').click()
        require(set(check("BLOCKED")["blocking_control_ids"])=={"declaration","roles"},
                f"{width}px: MIM authority blockers incorrect")
        page.locator('[data-fixture="integration"]').click()
        check("REVIEW")
        page.locator('[data-gate="entitlement"]').uncheck()
        check("BLOCKED")
        page.locator('[data-gate="entitlement"]').check()
        check("REVIEW")
        page.locator('[data-fixture="complete"]').click()
        check("COMPLETE")
        require(page.locator('[data-fixture="complete"]').get_attribute("aria-pressed")=="true",
                f"{width}px: MIM fixture not focus/selection accessible")
        print(f"PASS {width}px: MIM synthetic gates and receipt")
    finally:
        page.close()


def check_itsm_greenfield_sequencer(browser, width):
    """Exercise customer-neutral ITSM sequencing, blocking gates and honest receipts."""
    url = (Path(__file__).resolve().parents[1] / "itsm-greenfield-build-sequencer.html").as_uri()
    page = browser.new_page(viewport={"width": width, "height": 900}, reduced_motion="reduce")
    try:
        page.goto(url, wait_until="domcontentloaded", timeout=30000)
        require(page.locator("h1").count() == 1 and page.locator("main").count() == 1,
                f"{width}px: ITSM sequencer page landmarks")
        require(page.evaluate("() => document.documentElement.scrollWidth <= innerWidth + 2"),
                f"{width}px: ITSM sequencer document overflow")
        require(page.locator("#modules button").count() == 9,
                f"{width}px: ITSM sequencer capability count")
        require(page.locator("#gate-list input").count() == 8,
                f"{width}px: ITSM sequencer control count")
        def receipt(expected_status, expected_fixture):
            data = json.loads(page.locator("#readiness-receipt").inner_text())
            require(data["readiness_status"] == expected_status and
                    data["fixture"] == expected_fixture and
                    data["evidence_class"] == "MOCK-ONLY" and
                    data["service_now_instance"] is None and
                    not data["dev_execution_verified"] and
                    not data["customer_approval"] and
                    not data["production_deployment_verified"] and
                    not data["release_identity_verified"],
                    f"{width}px: ITSM receipt missing trust boundary: {data}")
            return data
        require(receipt("MODEL COMPLETE", "baseline")["checked_controls"] == 8,
                f"{width}px: ITSM initial fixture incomplete")
        page.locator('[data-fixture="access"]').click()
        require(set(receipt("BLOCKED", "access")["blocking_gates"]) ==
                {"baseline", "requirements"}, f"{width}px: access blockers")
        page.locator('[data-fixture="evidence"]').click()
        require(set(receipt("BLOCKED", "evidence")["blocking_gates"]) ==
                {"tests", "release"}, f"{width}px: execution blockers")
        page.locator('#gate-list input[data-gate="tests"]').check()
        page.locator('#gate-list input[data-gate="release"]').check()
        require(receipt("REVIEW", "custom")["review_gates"] == ["handover"],
                f"{width}px: review gate incorrect")
        page.locator("#modules button").nth(6).click()
        require(receipt("REVIEW", "custom")["capability"] == "MIM",
                f"{width}px: MIM selection did not propagate to receipt")
        page.locator('[data-fixture="baseline"]').click()
        receipt("MODEL COMPLETE", "baseline")
        print(f"PASS {width}px: ITSM sequencer selection, synthetic blockers and provenance")
    finally:
        page.close()


def verify_png_pixels(blob, inside, outside):
    """Inspect browser-exported PNG without image packages or retaining a file."""
    import struct
    import zlib

    require(blob[:8] == bytes([137,80,78,71,13,10,26,10]), "export must be a PNG")
    pos, rgba, size, compressed, chunks = 8, None, None, bytearray(), []
    while pos + 12 <= len(blob):
        length = struct.unpack(">I", blob[pos:pos + 4])[0]
        kind = blob[pos + 4:pos + 8]
        content = blob[pos + 8:pos + 8 + length]
        chunks.append(kind)
        if kind == b"IHDR":
            width, height, depth, colour, *_ = struct.unpack(">IIBBBBB", content)
            require(depth == 8 and colour in (2, 6), "unsupported export PNG colour mode")
            rgba = 4 if colour == 6 else 3
            size = (width, height)
        elif kind == b"IDAT":
            compressed.extend(content)
        pos += length + 12
        if kind == b"IEND":
            break
    require(size == (80, 50), "export dimensions changed from source")
    require(not any(kind in (b"tEXt", b"iTXt", b"zTXt", b"eXIf") for kind in chunks),
            "source metadata must not survive canvas raster re-encoding")
    require(b"PRIVATE-DO-NOT-PUBLISH" not in blob, "source metadata leaked")
    raw = zlib.decompress(bytes(compressed))
    stride = size[0] * rgba
    rows, previous, index = [], bytearray(stride), 0
    for _ in range(size[1]):
        f = raw[index]
        scan = raw[index + 1:index + stride + 1]
        index += stride + 1
        row = bytearray(stride)
        for i, value in enumerate(scan):
            left = row[i - rgba] if i >= rgba else 0
            above = previous[i]
            upper_left = previous[i - rgba] if i >= rgba else 0
            if f == 0: predictor = 0
            elif f == 1: predictor = left
            elif f == 2: predictor = above
            elif f == 3: predictor = (left + above) // 2
            elif f == 4:
                p = left + above - upper_left
                distances = (abs(p - left), abs(p - above), abs(p - upper_left))
                predictor = (left, above, upper_left)[distances.index(min(distances))]
            else: raise AssertionError("unsupported PNG filter")
            row[i] = (value + predictor) & 255
        rows.append(row)
        previous = row
    def rgb(pos):
        x, y = pos
        return tuple(rows[y][x * rgba:x * rgba + 3])
    require(rgb(inside) == (0, 0, 0), "redacted source pixels survived the PNG export")
    require(rgb(outside) == (230, 65, 65), "unredacted synthetic pixels were changed")


def check_local_redaction_desk(browser, width):
    """End-to-end synthetic image redaction and metadata stripping; no real files."""
    import base64
    import struct
    import zlib

    url = (Path(__file__).resolve().parents[1] / "screenshot-redaction-desk.html").as_uri()
    page = browser.new_page(viewport={"width": width, "height": 900},
                            reduced_motion="reduce", accept_downloads=True)
    remote = []
    page.on("request", lambda req: remote.append(req.url) if req.url.startswith(("http:", "https:")) else None)
    try:
        page.goto(url, wait_until="domcontentloaded", timeout=30000)
        require(page.locator("h1").count() == 1 and page.locator("main").count() == 1,
                f"{width}px: local redaction page landmarks")
        require(page.evaluate("() => document.documentElement.scrollWidth <= innerWidth + 2"),
                f"{width}px: redaction page horizontal overflow")
        require(page.locator("#export-png").is_disabled(), "export should start locked")
        fixture = page.evaluate("""() => {
            const c=document.createElement('canvas');c.width=80;c.height=50;
            const x=c.getContext('2d');x.fillStyle='#e64141';x.fillRect(0,0,80,50);
            return c.toDataURL('image/png').split(',')[1];
        }""")
        source = base64.b64decode(fixture)
        # Insert an explicit source-only PNG text chunk to prove it is excluded.
        payload = b"source" + bytes([0]) + b"PRIVATE-DO-NOT-PUBLISH"
        text_chunk = (struct.pack(">I",len(payload)) + b"tEXt" + payload
                      + struct.pack(">I",zlib.crc32(b"tEXt" + payload)))
        source = source[:33] + text_chunk + source[33:]
        page.locator("#source-file").set_input_files(
            {"name":"private-synthetic-fixture.png","mimeType":"image/png","buffer":source})
        page.wait_for_function("() => document.getElementById('image-size').textContent === '80 × 50'", timeout=10000)
        require(page.locator("#export-png").is_disabled(), "export without redactions permitted")
        page.locator("#rect-w").fill("50")
        page.locator("#rect-h").fill("50")
        page.locator("#add-rect").click()
        require(page.locator("#area-count").inner_text()=="1", "keyboard rectangle missing")
        require(page.locator("#export-png").is_disabled(), "export without visual acknowledgement permitted")
        page.locator("#reviewed").check()
        require(page.locator("#export-png").is_enabled(), "acknowledged export remains locked")
        page.locator("#undo-rect").click()
        require(page.locator("#reviewed").is_disabled() and page.locator("#export-png").is_disabled(),
                "undo did not revoke review")
        # Pointer interaction independently exercises pixel coordinates.
        page.evaluate("""() => { window.__redactionEvents=[]; const c=document.getElementById("preview"); ["pointerdown","pointermove","pointerup","pointercancel"].forEach(t=>c.addEventListener(t,e=>window.__redactionEvents.push(t+":"+e.button))); }""")
        page.locator("#preview").scroll_into_view_if_needed()
        bounds = page.locator("#preview").bounding_box()
        require(bounds is not None, "canvas is not visible")
        page.mouse.move(bounds["x"]+5,bounds["y"]+5)
        page.mouse.down()
        page.mouse.move(bounds["x"]+35,bounds["y"]+30,steps=5)
        page.mouse.up()
        require(page.locator("#area-count").inner_text()=="1", "pointer rectangle not registered: " + str(page.evaluate("() => ({events:window.__redactionEvents,status:document.getElementById('status').textContent,box:document.getElementById('preview').getBoundingClientRect().toJSON()})")) )
        page.locator("#reviewed").check()
        with page.expect_download(timeout=10000) as event:
            page.locator("#export-png").click()
        download=event.value
        require(download.suggested_filename=="workbench-redacted-review.png",
                "private input filename leaked into output")
        from pathlib import Path as _Path
        exported=_Path(download.path()).read_bytes()  # Chromium's temporary file, not repository.
        verify_png_pixels(exported,(10,10),(70,40))
        import hashlib
        digest=hashlib.sha256(exported).hexdigest()
        page.wait_for_function(
            "() => document.getElementById('export-receipt').disabled === false",
            timeout=10000
        )
        require(page.locator("#export-sha256").inner_text() == digest,
                f"{width}px: displayed SHA-256 does not match exported PNG bytes")
        with page.expect_download(timeout=10000) as receipt_event:
            page.locator("#export-receipt").click()
        receipt_download=receipt_event.value
        require(receipt_download.suggested_filename=="workbench-redacted-review.receipt.json",
                "unexpected redaction receipt download filename")
        receipt=json.loads(_Path(receipt_download.path()).read_text())
        require(receipt["sha256"]==digest and
                receipt["dimensions_px"]=={"width":80,"height":50} and
                receipt["redaction_area_count"]==1 and
                receipt["publication_status"]=="HOLD" and
                receipt["publication_approved"] is False and
                receipt["service_now_dev_verified"] is False and
                receipt["service_now_production_verified"] is False and
                receipt["independent_export_review"]=="REQUIRED",
                f"{width}px: receipt hash or publication guard invalid")
        require("private-synthetic-fixture" not in json.dumps(receipt) and
                "PRIVATE-DO-NOT-PUBLISH" not in json.dumps(receipt),
                f"{width}px: private source detail leaked into receipt")
        # Editing a mask invalidates the old digest and receipt.
        page.locator("#add-rect").click()
        require(page.locator("#export-receipt").is_disabled() and
                page.locator("#export-sha256").inner_text()=="Not generated" and
                page.locator("#reviewed").is_checked() is False,
                f"{width}px: old receipt remained valid after mask revision")
        require(not remote, f"{width}px: local tool made remote requests: {remote}")
        print(f"PASS {width}px: local image privacy, keyboard/pointer masking, export bytes and metadata")
    finally:
        page.close()

def check_screenshot_receipt_verifier(browser, width):
    """Verify PNG/receipt binding and publication HOLD with synthetic data only."""
    import base64
    import hashlib
    page = browser.new_page(viewport={"width": width, "height": 900}, reduced_motion="reduce")
    remote=[]
    page.on("request", lambda req: remote.append(req.url)
            if req.url.startswith(("http:", "https:")) else None)
    url=(Path(__file__).resolve().parents[1] / "screenshot-receipt-verifier.html").as_uri()
    try:
        page.goto(url, wait_until="domcontentloaded", timeout=30000)
        require(page.locator("h1").count()==1 and page.locator("main").count()==1,
                f"{width}px: receipt verifier landmarks")
        require(page.evaluate("() => document.documentElement.scrollWidth <= innerWidth + 2"),
                f"{width}px: receipt verifier horizontal overflow")
        require(page.locator("#verify").is_disabled(), "verification enabled without two files")
        b64=page.evaluate("""() => {
            const c=document.createElement('canvas');c.width=80;c.height=50;
            const ctx=c.getContext('2d');ctx.fillStyle='#000';ctx.fillRect(0,0,40,30);
            ctx.fillStyle='#72aacc';ctx.fillRect(40,0,40,50);
            return c.toDataURL('image/png').split(',')[1];
        }""")
        data=base64.b64decode(b64)
        receipt={
            "schema":"servicenow-portfolio-redacted-image-receipt/v1",
            "exported_file":"workbench-redacted-review.png",
            "sha256":hashlib.sha256(data).hexdigest(),
            "dimensions_px":{"width":80,"height":50},
            "redaction_area_count":1,
            "generated_utc":"2026-11-12T00:00:00.000Z",
            "evidence_class":"SOURCE-ONLY TOOL OUTPUT",
            "publication_status":"HOLD","publication_approved":False,
            "service_now_dev_verified":False,"service_now_production_verified":False,
            "independent_export_review":"REQUIRED"
        }
        page.locator("#png-file").set_input_files(
            {"name":"redacted-synthetic.png","mimeType":"image/png","buffer":data})
        require(page.locator("#verify").is_disabled(), "verification enabled without receipt")
        def load_receipt(record):
            page.locator("#receipt-file").set_input_files(
                {"name":"review.receipt.json","mimeType":"application/json",
                 "buffer":json.dumps(record).encode("utf-8")})
        load_receipt(receipt)
        page.locator("#verify").click()
        page.wait_for_function("""() => document.getElementById('status').dataset.kind !== 'pending'""")
        require(page.locator("#status").get_attribute("data-kind")=="match",
                f"{width}px: synthetic receipt did not match")
        require(page.locator("#actual-digest").inner_text()==receipt["sha256"],
                f"{width}px: verifier did not hash actual PNG bytes")
        require("HOLD" in page.locator("#publication-state").inner_text(),
                f"{width}px: publication HOLD not displayed")
        # A forged receipt can match altered image bytes: CRC must still catch corruption.
        import struct
        import zlib
        corrupted=bytearray(data)
        offset=8
        while offset+12<=len(corrupted):
            length=struct.unpack(">I",corrupted[offset:offset+4])[0]
            if corrupted[offset+4:offset+8]==b"IDAT":
                require(length>0, "synthetic fixture has no compressed image payload")
                corrupted[offset+8]^=1
                break
            offset+=length+12
        else:
            raise AssertionError("synthetic fixture missing IDAT")
        def load_image(blob):
            page.locator("#png-file").set_input_files(
                {"name":"local-synthetic.png","mimeType":"image/png","buffer":blob})
        load_image(bytes(corrupted))
        load_receipt({**receipt,"sha256":hashlib.sha256(corrupted).hexdigest()})
        page.locator("#verify").click()
        page.wait_for_function("""() => document.getElementById('status').dataset.kind !== 'pending'""")
        require(page.locator("#status").get_attribute("data-kind")=="fail"
                and "CRC mismatch" in page.locator("#explanation").inner_text(),
                f"{width}px: CRC-invalid PNG passed with matching receipt hash")
        # Inject a valid-CRC metadata chunk: must fail even with a matching digest.
        metadata=b"source\x00PRIVATE-DO-NOT-PUBLISH"
        ancillary=(struct.pack(">I",len(metadata))+b"tEXt"+metadata+
                   struct.pack(">I",zlib.crc32(b"tEXt"+metadata)))
        with_metadata=data[:33]+ancillary+data[33:]
        load_image(with_metadata)
        load_receipt({**receipt,"sha256":hashlib.sha256(with_metadata).hexdigest()})
        page.locator("#verify").click()
        page.wait_for_function("""() => document.getElementById('status').dataset.kind !== 'pending'""")
        require(page.locator("#status").get_attribute("data-kind")=="fail"
                and "Unexpected PNG metadata" in page.locator("#explanation").inner_text(),
                f"{width}px: embedded private metadata accepted")
        load_image(data)
        load_receipt(receipt)
        page.locator("#verify").click()
        page.wait_for_function("""() => document.getElementById('status').dataset.kind !== 'pending'""")
        require(page.locator("#status").get_attribute("data-kind")=="match",
                f"{width}px: restoring original PNG/receipt did not recover")
        forged={**receipt,"sha256":"0"*64}
        load_receipt(forged)
        require(page.locator("#actual-digest").inner_text()=="Not calculated",
                "changing receipt did not invalidate prior match")
        page.locator("#verify").click()
        page.wait_for_function("""() => document.getElementById('status').dataset.kind !== 'pending'""")
        require(page.locator("#status").get_attribute("data-kind")=="fail"
                and "mismatch" in page.locator("#explanation").inner_text().lower(),
                f"{width}px: altered hash incorrectly accepted")
        unsafe={**receipt,"publication_approved":True}
        load_receipt(unsafe)
        page.locator("#verify").click()
        page.wait_for_function("""() => document.getElementById('status').dataset.kind !== 'pending'""")
        require(page.locator("#status").get_attribute("data-kind")=="fail",
                f"{width}px: unsafe approval claim accepted")
        wrong={**receipt,"dimensions_px":{"width":81,"height":50}}
        load_receipt(wrong)
        page.locator("#verify").click()
        page.wait_for_function("""() => document.getElementById('status').dataset.kind !== 'pending'""")
        require(page.locator("#status").get_attribute("data-kind")=="fail",
                f"{width}px: incorrect dimensions accepted")
        require(not remote, f"{width}px: verifier made external requests: {remote}")
        print(f"PASS {width}px: local receipt CRC, safe chunks, SHA-256 binding, HOLD and dimensions")
    finally:
        page.close()



def check_reviewed_evidence_gallery(browser, width):
    """Review-source cards are safe, labelled and responsive without publishing image bytes."""
    url = (Path(__file__).resolve().parents[1] / "visual-evidence.html").as_uri()
    page = browser.new_page(viewport={"width": width, "height": 900}, reduced_motion="reduce")
    try:
        page.goto(url, wait_until="domcontentloaded", timeout=30000)
        require(page.locator('article[data-review-id]').count() == 6,
                f"{width}px: six inspected evidence records not visible")
        require(page.locator('article[data-evidence-id]').count() == 10,
                f"{width}px: ten separate candidate placeholders altered")
        require(page.locator("img").count() == 0,
                f"{width}px: private or unapproved image embedded")
        for record in ("RV-05", "RV-06"):
            card = page.locator(f'article[data-review-id="{record}"]')
            require(card.get_attribute("data-source-class") == "mock-only",
                    f"{width}px: {record} missing synthetic boundary")
            require("HOLD" in card.inner_text()
                    and "Not established" in card.inner_text(),
                    f"{width}px: {record} missing review and publication boundary")
        require(page.evaluate(
            "() => document.documentElement.scrollWidth <= window.innerWidth + 2"
        ), f"{width}px: evidence gallery overflows screen")
        # The inspected sample is a separate, usable review registry, not an image gallery.
        require(page.locator("#review-count").inner_text() == "6 of 6 inspected reviews shown",
                f"{width}px: reviewed sample initial count incorrect")
        page.locator('[data-review-filter="diagnostic"]').click()
        require(page.locator("#review-count").inner_text() == "2 of 6 inspected reviews shown",
                f"{width}px: Diagnostic filter incorrect")
        page.locator("#review-search").fill("MIM")
        require(page.locator("#review-count").inner_text() == "1 of 6 inspected reviews shown",
                f"{width}px: Diagnostic/MIM search incorrect")
        require(page.locator('article[data-review-id="RV-05"]').is_visible(),
                f"{width}px: inspected Diagnostic MIM record missing")
        require(not page.locator('article[data-review-id="RV-06"]').is_visible(),
                f"{width}px: Delivery review incorrectly returned in Diagnostic filter")
        with page.expect_download() as transfer:
            page.locator("#export-reviewed").click()
        csv = transfer.value.path().read_text(encoding="utf-8-sig")
        require("RV-05" in csv and "RV-06" not in csv and "publication_decision" in csv
                and "HOLD" in csv and "not_established" in csv,
                f"{width}px: exported reviewed register ignores filter or loses HOLD")
        require("drive.google.com" not in csv and "servicenow-portfolio-control" not in csv,
                f"{width}px: restricted material leaked into exported review CSV")
        page.evaluate("() => { window.print = () => { window.__reviewPrintMarked = document.body.classList.contains('review-print') } }")
        page.locator("#print-reviewed").click()
        require(page.evaluate("() => window.__reviewPrintMarked === true"),
                f"{width}px: reviewed print mode not activated")
        page.evaluate("() => window.dispatchEvent(new Event('afterprint'))")
        require(not page.locator("body").evaluate("(el) => el.classList.contains('review-print')"),
                f"{width}px: print-only state was not cleared")
        page.locator("#clear-reviews").click()
        require(page.locator("#review-count").inner_text() == "6 of 6 inspected reviews shown",
                f"{width}px: reviewed reset failed")
        page.goto(url + "?reviewGroup=delivery&reviewq=scope", wait_until="domcontentloaded")
        require(page.locator("#review-count").inner_text() == "1 of 6 inspected reviews shown"
                and page.locator('article[data-review-id="RV-06"]').is_visible(),
                f"{width}px: bookmarked reviewed search not restored")
        require(page.evaluate("() => document.documentElement.scrollWidth <= innerWidth + 2"),
                f"{width}px: reviewed filter controls create horizontal overflow")
        print(f"PASS {width}px: six evidence reviews, strict HOLD, no image publication")
    finally:
        page.close()



def check_verification_ledger(browser, width):
    """Browser-test the JSON-driven ledger via loopback HTTP (file:// fetch is blocked)."""
    from functools import partial
    from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
    from threading import Thread

    root = Path(__file__).resolve().parents[1]

    class QuietHandler(SimpleHTTPRequestHandler):
        def log_message(self, *_args):
            pass

    server = ThreadingHTTPServer(
        ("127.0.0.1", 0), partial(QuietHandler, directory=str(root))
    )
    worker = Thread(target=server.serve_forever, daemon=True)
    worker.start()
    page = browser.new_page(
        viewport={"width": width, "height": 900},
        reduced_motion="reduce",
    )
    try:
        url = f"http://127.0.0.1:{server.server_address[1]}/verification-ledger.html"
        page.goto(url, wait_until="domcontentloaded", timeout=30000)
        page.wait_for_function(
            "() => document.querySelectorAll('#records .card').length === 15",
            timeout=12000,
        )
        require(page.locator("#count").inner_text() == "15 of 15 evidence claims shown",
                f"{width}px: claim manifest did not hydrate")
        require(page.locator("#total").inner_text() == "15",
                f"{width}px: headline claim count out of sync")
        require(page.locator("#mock").inner_text() == "5",
                f"{width}px: synthetic classification count out of sync")
        require(page.locator("#load-error").is_hidden(),
                f"{width}px: ledger failed to load public JSON")
        page.locator('[data-filter="mock-only"]').click()
        require(page.locator("#count").inner_text() == "5 of 15 evidence claims shown",
                f"{width}px: mock filter is incorrect")
        page.locator("#reset").click()
        page.locator("#search").fill("CRC-32")
        require(page.locator("#count").inner_text() == "1 of 15 evidence claims shown",
                f"{width}px: evidence search did not isolate receipt verifier")
        require(page.locator("#claim-receipt-verifier").is_visible(),
                f"{width}px: expected verifier claim is not visible")
        page.locator("#reset").click()
        require(page.locator("#count").inner_text() == "15 of 15 evidence claims shown",
                f"{width}px: reset did not restore claims")
        require(page.evaluate("() => document.documentElement.scrollWidth <= innerWidth + 2"),
                f"{width}px: evidence ledger overflows the viewport")
        require(page.locator("img").count() == 0,
                f"{width}px: unapproved screenshot/image embedded in ledger")
        print(f"PASS {width}px: JSON evidence hydration, mock filter, search and privacy")
    finally:
        page.close()
        server.shutdown()
        server.server_close()
        worker.join(timeout=3)



def check_review_packet(browser, width):
    """Exercise privacy-preserving owner-side handoff; every export stays HOLD."""
    url = (Path(__file__).resolve().parents[1] / "screenshot-review-packet.html").as_uri()
    page = browser.new_page(
        viewport={"width": width, "height": 900},
        accept_downloads=True,
        reduced_motion="reduce",
    )
    try:
        page.goto(url, wait_until="domcontentloaded", timeout=30000)
        require(page.locator("#gate-count").inner_text() == "0 of 8 gates marked",
                f"{width}px: handoff should start with no affirmative controls")
        require("HOLD" in page.locator("#gate-status").inner_text(),
                f"{width}px: handoff must begin on HOLD")
        require(page.locator("img").count() == 0,
                f"{width}px: review packet must not expose private imagery")
        require(page.evaluate(
            "() => document.documentElement.scrollWidth <= innerWidth + 2"
        ), f"{width}px: review packet overflows viewport")
        page.locator("#review-id").select_option("RV-05")
        require("MOCK-ONLY" in page.locator("#review-class").inner_text(),
                f"{width}px: synthetic screenshot context was not classified")
        require(page.locator("#review-link").get_attribute("href").endswith("#review-rv-05"),
                f"{width}px: public cross-reference broken")
        gates = page.locator("input[data-gate]")
        require(gates.count() == 8, f"{width}px: missing publication controls")
        for i in range(8):
            gates.nth(i).check()
        require(page.locator("#gate-count").inner_text() == "8 of 8 gates marked",
                f"{width}px: checklist progress is inaccurate")
        require(page.locator("#gate-status").inner_text() == "REVIEW-READY · HOLD",
                f"{width}px: completion must never mean approved")
        preview = json.loads(page.locator("#packet-preview").text_content())
        require(preview["publication_status"] == "HOLD"
                and preview["public_release_authorised"] is False
                and preview["production_verified"] is False
                and preview["service_now_dev_verified"] is False
                and preview["public_review_id"] == "RV-05"
                and preview["completed_gates"] == 8,
                f"{width}px: review packet claims unsupported approval")
        with page.expect_download() as transfer:
            page.locator("#download-packet").click()
        exported = json.loads(transfer.value.path().read_text(encoding="utf-8"))
        require(exported["publication_status"] == "HOLD"
                and exported["public_release_authorised"] is False
                and exported["public_review_id"] == "RV-05",
                f"{width}px: downloaded packet bypasses hold policy")
        require(not any(k in exported for k in
                ("reviewer_name", "private_url", "original_hash", "image_bytes")),
                f"{width}px: downloaded packet contains private fields")
        page.locator("#review-id").select_option("RV-06")
        require(page.locator("#gate-count").inner_text() == "0 of 8 gates marked",
                f"{width}px: changing candidate must clear all prior checks")
        page.locator("input[data-gate=rights]").check()
        page.locator("#reset-packet").click()
        require(page.locator("#gate-count").inner_text() == "0 of 8 gates marked",
                f"{width}px: reset fails to clear rights attestation")
        print(f"PASS {width}px: review packet gates, HOLD-only export, candidate reset and privacy")
    finally:
        page.close()



def check_cmdb_source_onboarding_lab(browser, width):
    """Prove the synthetic CMDB ingestion design gate cannot assert native acceptance."""
    url = (Path(__file__).resolve().parents[1] / "cmdb-source-onboarding-lab.html").as_uri()
    page = browser.new_page(
        viewport={"width": width, "height": 900},
        accept_downloads=True,
        reduced_motion="reduce",
    )
    try:
        page.goto(url, wait_until="domcontentloaded", timeout=30000)
        require(page.locator("#gate-count").inner_text() == "0 of 6 reviews marked",
                f"{width}px: source review starts with a positive attestation")
        require("HOLD" in page.locator("#gate-status").inner_text(),
                f"{width}px: synthetic review starts as approved")
        require(page.locator("img").count() == 0,
                f"{width}px: unapproved Workbench capture published")
        require(page.evaluate("() => document.documentElement.scrollWidth <= innerWidth + 2"),
                f"{width}px: onboarding lab overflows viewport")

        checks = page.locator("input[data-gate]")
        require(checks.count() == 6, f"{width}px: six design controls not available")
        for i in range(6):
            checks.nth(i).check()
        require(page.locator("#gate-count").inner_text() == "6 of 6 reviews marked",
                f"{width}px: checklist count wrong")
        require("native simulation required" in page.locator("#gate-status").inner_text(),
                f"{width}px: design completion implies native acceptance")
        data = json.loads(page.locator("#receipt-preview").text_content())
        require(data["decision"] == "READY_FOR_NATIVE_SIMULATION_NOT_APPROVED"
                and data["approval_granted"] is False
                and data["servicenow_dev_verified"] is False
                and data["production_verified"] is False
                and data["actual_ire_response"] is None,
                f"{width}px: optimistic receipt claims unsupported execution")

        with page.expect_download() as transfer:
            page.locator("#download-receipt").click()
        exported = json.loads(transfer.value.path().read_text(encoding="utf-8"))
        require(exported == data and exported["assessment_classification"] == "MOCK-ONLY",
                f"{width}px: exported receipt diverges from safe preview")

        page.locator("#scenario-select").select_option("collision")
        require(page.locator("#gate-count").inner_text() == "0 of 6 reviews marked",
                f"{width}px: scenario change retained prior approvals")
        for i in range(6):
            checks.nth(i).check()
        require("BLOCK" in page.locator("#gate-status").inner_text()
                and json.loads(page.locator("#receipt-preview").text_content())["decision"]
                    == "BLOCKED_DESIGN_INPUT",
                f"{width}px: bad identity became accepted by checkbox completion")
        page.locator("#scenario-select").select_option("attributes")
        require(page.locator("#gate-count").inner_text() == "0 of 6 reviews marked",
                f"{width}px: attribute conflict inherited previous checks")
        page.locator("#reset-review").click()
        require("HOLD" not in page.locator("#gate-status").inner_text()
                or "BLOCK" in page.locator("#gate-status").inner_text(),
                f"{width}px: conflict scenario incorrectly promoted after reset")
        require(page.evaluate("() => document.documentElement.scrollWidth <= innerWidth + 2"),
                f"{width}px: scenario cards overflow mobile viewport")
        print(f"PASS {width}px: safe synthetic IRE readiness, conflict blocks, JSON receipt")
    finally:
        page.close()


def check_diagnostic_coverage_explorer(browser, width):
    """Verify local-only source catalogue filtering and HOLD receipt."""
    page = browser.new_page(viewport={"width": width, "height": 900}, accept_downloads=True, reduced_motion="reduce")
    try:
        page.goto((Path(__file__).resolve().parents[1]/"diagnostic-coverage-explorer.html").as_uri(),
                  wait_until="domcontentloaded", timeout=30000)
        require(page.locator(".record").count() == 20, f"{width}px: coverage not 20")
        require(page.evaluate("() => document.documentElement.scrollWidth <= innerWidth + 2"),
                f"{width}px: diagnostic page overflows")
        page.locator("#search").fill("duplicate")
        require(page.locator(".record:visible").count() >= 1, f"{width}px: no duplicate results")
        page.locator("#reset").click()
        page.locator("#domain").select_option("CMDB & CSDM")
        require(page.locator(".record:visible").count() == 6, f"{width}px: wrong CMDB coverage count")
        page.locator("#reset").click()
        page.locator("#scenario").select_option("absent")
        sample = json.loads(page.locator("#receipt").inner_text())
        require(sample["decision"] == "NOT_ASSESSED" and sample["servicenow_dev_verified"] is False,
                f"{width}px: missing metric claimed healthy")
        page.locator("#scenario").select_option("sensitive")
        require(page.locator("#decision").inner_text() == "REJECT_UNSAFE_PAYLOAD",
                f"{width}px: unsafe case accepted")
        with page.expect_download() as transfer:
            page.locator("#download").click()
        exported = json.loads(transfer.value.path().read_text(encoding="utf-8"))
        require(exported["publication_status"] == "HOLD"
                and exported["public_release_authorised"] is False
                and exported["production_verified"] is False
                and exported["classification"] == "MOCK-ONLY",
                f"{width}px: unsupported acceptance in exported example")
        print(f"PASS {width}px: diagnostic coverage/filter/unsafe-data/HOLD contract")
    finally:
        page.close()


def main():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        try:
            for width in VIEWPORTS:
                check_viewport(browser, width)
                check_reviewed_evidence_gallery(browser, width)
                check_verification_ledger(browser, width)
                check_review_packet(browser, width)
                check_cmdb_source_onboarding_lab(browser, width)
                check_diagnostic_coverage_explorer(browser, width)
                for filename, anchor in CASE_STUDIES:
                    check_case_study(browser, filename, anchor, width)
                check_cmdb_trust_lab(browser, width)
                check_mim_design_lab(browser, width)
                check_itsm_greenfield_sequencer(browser, width)
                check_local_redaction_desk(browser, width)
                check_screenshot_receipt_verifier(browser, width)
        finally:
            browser.close()


if __name__ == "__main__":
    main()

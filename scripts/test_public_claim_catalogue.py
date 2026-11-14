#!/usr/bin/env python3
"""Static contract for the same-origin, public-only evidence claim catalogue."""
import json
import re
import unittest
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "technical-evidence-register.html"
REGISTER = ROOT / "evidence/public-verification-register.json"

class IdParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            self.ids.append(attrs["id"])

class PublicClaimCatalogueContract(unittest.TestCase):
    def setUp(self):
        self.html = HTML.read_text(encoding="utf-8")
        self.data = json.loads(REGISTER.read_text(encoding="utf-8"))

    def test_reader_reuses_authoritative_public_register(self):
        self.assertIn("fetch(registerUrl,{cache:'no-store'})", self.html)
        self.assertIn("evidence/public-verification-register.json", self.html)
        self.assertIn("schema_version!=='1.0'", self.html)
        self.assertIn("const valid=new Set", self.html)
        self.assertIn("ids.has(c.id)", self.html)
        self.assertNotIn("innerHTML", self.html)
        self.assertIn("el.textContent=text", self.html)
        self.assertIn("host.replaceChildren()", self.html)
        self.assertIn("no claims inferred", self.html)

    def test_unique_controls_and_accessible_progress(self):
        parser = IdParser()
        parser.feed(self.html)
        self.assertEqual(len(parser.ids), len(set(parser.ids)))
        for ident in ("claim-catalogue", "claim-catalogue-title", "claim-search",
                      "claim-classification", "claim-count", "claim-results",
                      "claim-more", "claim-fallback"):
            self.assertIn(ident, parser.ids)
        self.assertIn('aria-live="polite"', self.html)
        self.assertIn('grid-template-columns:1fr', self.html)

    def test_public_register_never_promotes_historical_dev_claims(self):
        items = self.data["items"]
        self.assertGreaterEqual(len(items), 80)
        classes = {c["classification"] for c in items}
        self.assertTrue(classes <= {"source-only", "DEV-reported", "mock-only", "proposed"})
        self.assertFalse(any(c["classification"] in {"DEV-verified", "production-verified"} for c in items))
        for claim in items:
            with self.subTest(claim=claim["id"]):
                self.assertRegex(claim["page"], r"^[a-z0-9-]+\.html$")
                self.assertTrue((ROOT / claim["page"]).is_file())


    def test_selection_is_local_only_and_exports_cannot_certify_execution(self):
        for ident in ("claim-shortlist", "shortlist-count", "shortlist-export-md",
                      "shortlist-export-json", "shortlist-clear", "shortlist-preview"):
            self.assertIn(f'id="{ident}"', self.html)
        for snippet in ("const selected=new Set()", "function selectedClaims()", "function reviewPacket()",
                        "function publicUrl(c)", "function safeMarkdown(v)", "function reviewMarkdown(packet)",
                        "review_state:'UNREVIEWED'", "verification_state:'NOT VERIFIED'",
                        "release_state:'HOLD'", "native_service_now_execution:false",
                        "independent_review_approved:false", "screenshot_publication_approved:false",
                        "No browser storage, uploads", "check.checked=selected.has(claim.id)",
                        "selected.clear();render();updateSelection()", "URL.createObjectURL(blob)"):
            self.assertIn(snippet, self.html)
        self.assertNotIn("localStorage", self.html)
        self.assertNotIn("sessionStorage", self.html)
        self.assertNotIn("navigator.sendBeacon", self.html)
        self.assertIn("if(!selectedClaims().length)return", self.html)
        self.assertIn("selected.clear();updateSelection();", self.html)

    def test_public_review_permalink_is_bounded_and_never_certifies_claims(self):
        for ident in ("shortlist-share", "shortlist-link", "shortlist-copy",
                      "shortlist-open", "share-status"):
            self.assertIn(f'id="{ident}"', self.html)
        for marker in ("function parsePublicReviewLink()", "function restoreSharedSelection()",
                       "function publicReviewUrl()", "params.getAll('brief')",
                       "all.length!==1", "all[0].length>1300", "ids.length>12",
                       "new Set(ids).size!==ids.length", "shareInput.value=link||''",
                       "new URL(window.location.pathname,window.location.origin)",
                       "url.hash='claim-shortlist'", "sharedRequest.ids.every",
                       "navigator.clipboard.writeText(link)",
                       "UNREVIEWED / NOT VERIFIED / HOLD"):
            self.assertIn(marker, self.html)
        self.assertNotIn("history.pushState", self.html)
        self.assertNotIn("localStorage", self.html)
        self.assertNotIn("sessionStorage", self.html)
        self.assertEqual(len(self.data["items"]), 87)

if __name__ == "__main__":
    unittest.main()

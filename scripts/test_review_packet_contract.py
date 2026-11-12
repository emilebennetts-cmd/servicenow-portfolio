"""Contract checks for the local-only, HOLD-only screenshot review handoff.

Run with: python3 -m unittest discover -s scripts -p 'test_*.py'
These tests do not open or publish genuine evidence assets.
"""
from html.parser import HTMLParser
from pathlib import Path
import json
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "screenshot-review-packet.html"


class PacketMarkup(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.gates = []
        self.images = []
        self.external_resources = []
        self.meta = {}
        self.links = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get("id"):
            self.ids.append(a["id"])
        if tag == "input" and a.get("data-gate"):
            self.gates.append(a["data-gate"])
        if tag == "img":
            self.images.append(a)
        if tag == "meta" and a.get("http-equiv") == "Content-Security-Policy":
            self.meta["csp"] = a.get("content", "")
        if tag in ("script", "img", "iframe", "link") and a.get("src", a.get("href", "")).startswith(("http:", "https:", "//")):
            self.external_resources.append(a)
        if tag == "a":
            self.links.append(a.get("href", ""))


class ReviewPacketContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PAGE.read_text(encoding="utf-8")
        cls.markup = PacketMarkup()
        cls.markup.feed(cls.html)

    def test_accessible_mobile_and_unique_controls(self):
        self.assertEqual(len(self.markup.ids), len(set(self.markup.ids)))
        for expected in (
            "main", "review-id", "review-class", "review-description",
            "review-link", "gate-count", "gate-progress", "gate-status",
            "download-packet", "reset-packet", "packet-preview",
        ):
            with self.subTest(control=expected):
                self.assertIn(expected, self.markup.ids)
        self.assertIn('name="viewport"', self.html)
        self.assertIn("@media(max-width:800px)", self.html)
        self.assertIn("@media print", self.html)
        self.assertIn('aria-live="polite"', self.html)

    def test_all_governance_gates_are_explicit(self):
        expected = {
            "provenance", "rights", "runtime", "pixels",
            "sanitisation", "integrity", "editorial", "approval",
        }
        self.assertEqual(expected, set(self.markup.gates))
        self.assertEqual(8, len(self.markup.gates))
        for ident in range(1, 7):
            self.assertIn("RV-%02d" % ident, self.html)

    def test_never_grants_publication_or_runtime_attestation(self):
        for required in (
            'publication_status:"HOLD"',
            "public_release_authorised:false",
            "service_now_dev_verified:false",
            "production_verified:false",
            "READY_FOR_INDEPENDENT_REVIEW",
            "No ServiceNow licence",
            "MOCK-ONLY",
            "SOURCE-ONLY",
            "PRODUCTION-VERIFIED",
        ):
            self.assertIn(required, self.html)
        self.assertEqual([], self.markup.images)
        self.assertNotIn("servicenow-portfolio-control", self.html)
        self.assertNotIn("drive.google.com", self.html)

    def test_browser_only_and_no_private_data_collection(self):
        csp = self.markup.meta.get("csp", "")
        for directive in ("default-src 'none'", "connect-src 'none'", "img-src 'none'", "form-action 'none'"):
            self.assertIn(directive, csp)
        self.assertEqual([], self.markup.external_resources)
        for forbidden in ("fetch(", "XMLHttpRequest", "localStorage", "sessionStorage", "sendBeacon(", "innerHTML", "document.cookie"):
            self.assertNotIn(forbidden, self.html)
        # The export fields are strictly public-safe booleans and a public review ID.
        self.assertIn("Object.fromEntries(controls.map", self.html)
        self.assertIn('public_review_id:id', self.html)
        self.assertIn("new Blob([packet]", self.html)

    def test_public_links_only(self):
        for href in self.markup.links:
            if not href or href.startswith("#"):
                continue
            self.assertFalse(re.match(r"https?://|//", href))
            relative = href.split("#", 1)[0]
            if not relative or relative == "./":
                continue
            with self.subTest(href=href):
                self.assertTrue((ROOT / relative).exists(), "Missing " + href)


if __name__ == "__main__":
    unittest.main()

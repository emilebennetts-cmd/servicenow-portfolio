#!/usr/bin/env python3
"""Static contract for local-only, privacy-preserving screenshot redaction.

Runs in CI without private files, a browser, external libraries or network access.
Browser-level tests independently verify redacted exported PNG bytes.
"""
from html.parser import HTMLParser
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "screenshot-redaction-desk.html"

class Document(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.links, self.inputs = [], [], []
        self.h1 = self.main = 0
    def handle_starttag(self, tag, attrs):
        attr = dict(attrs)
        if "id" in attr: self.ids.append(attr["id"])
        if tag == "h1": self.h1 += 1
        if tag == "main": self.main += 1
        if tag == "a": self.links.append(attr.get("href", ""))
        if tag == "input": self.inputs.append(attr)

class LocalRedactionDeskContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PAGE.read_text(encoding="utf-8")
        cls.doc = Document()
        cls.doc.feed(cls.html)

    def test_semantics_navigation_and_responsive_view(self):
        self.assertEqual((self.doc.h1, self.doc.main), (1, 1))
        self.assertEqual(len(self.doc.ids), len(set(self.doc.ids)))
        for marker in ('lang="en"', 'href="#main"', 'width=device-width',
                       'aria-live="polite"', 'role="status"', 'touch-action:none',
                       '@media(max-width:900px)', '@media(max-width:520px)',
                       'prefers-reduced-motion:reduce'):
            self.assertIn(marker, self.html)
        for link in self.doc.links:
            self.assertFalse(link.startswith(("http:", "https:", "//")), link)
            path = link.split("#", 1)[0]
            if path:
                self.assertTrue((ROOT / (path if path != "./" else "index.html")).is_file(), link)

    def test_no_data_egress_or_external_dependencies(self):
        for forbidden in ('XMLHttpRequest', 'fetch(', 'sendBeacon', 'WebSocket',
                          'EventSource(', 'localStorage', 'sessionStorage',
                          'indexedDB', 'getUserMedia', 'serviceWorker',
                          'https://', 'http://', '<iframe', '<img ',
                          '<script src=', 'window.open(', 'postMessage(',
                          'github.com/emilebennetts-cmd/solution-lifecycle-studio',
                          'github.com/emilebennetts-cmd/servicenow-portfolio-control'):
            self.assertNotIn(forbidden, self.html)
        for directive in ("default-src 'none'", "connect-src 'none'",
                          "img-src blob: data:", "object-src 'none'",
                          "form-action 'none'", "base-uri 'none'"):
            self.assertIn(directive, self.html)

    def test_redaction_is_flattened_not_overlaid(self):
        required = ('id="source-file"', 'id="preview"', 'id="rect-x"',
                    'id="rect-y"', 'id="rect-w"', 'id="rect-h"',
                    'id="add-rect"', 'id="undo-rect"', 'id="clear-rect"',
                    'id="reviewed"', 'id="export-png"', 'id="rectangle-list"',
                    'const MAX_BYTES=15*1024*1024',
                    'MAX_PIXELS=16000000', 'decoded.width*decoded.height>MAX_PIXELS',
                    'URL.createObjectURL(f)', 'URL.revokeObjectURL(url)',
                    'target.fillStyle="#000000"', 'target.fillRect(r.x,r.y,r.w,r.h)',
                    'paint(out,false)', 'flattened.toBlob(function(blob)',
                    '"image/png"', 'workbench-redacted-review.png',
                    'reviewed.checked', 'exportBtn.disabled')
        for item in required:
            with self.subTest(item=item): self.assertIn(item, self.html)
        self.assertIn('["image/png","image/jpeg","image/webp"]', self.html)
        self.assertIn('canvas.addEventListener("pointercancel"', self.html)

    def test_honest_evidence_and_publication_hold(self):
        for marker in ('SOURCE-ONLY','MOCK-ONLY','DEV-VERIFIED','PRODUCTION-VERIFIED',
                       'HOLD','separate publication approval','no ServiceNow licence',
                       'manually review','Nothing is sent to GitHub'):
            self.assertIn(marker.lower(), self.html.lower())
        gallery = (ROOT / "visual-evidence.html").read_text(encoding="utf-8")
        home = (ROOT / "index.html").read_text(encoding="utf-8")
        sitemap = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
        for text in (gallery, home, sitemap):
            self.assertIn("screenshot-redaction-desk.html", text)
        self.assertNotIn('<img ', gallery)

if __name__ == "__main__":
    unittest.main()

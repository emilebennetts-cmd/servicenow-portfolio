#!/usr/bin/env python3
"""Static privacy and contract assertions for the client-only evidence receipt verifier."""
from html.parser import HTMLParser
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
PAGE=ROOT/"screenshot-receipt-verifier.html"

class Parse(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids=[]
        self.links=[]
        self.h1=0
        self.main=0
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if "id" in a:self.ids.append(a["id"])
        if tag=="a":self.links.append(a.get("href",""))
        if tag=="h1":self.h1+=1
        if tag=="main":self.main+=1

class Contract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html=PAGE.read_text(encoding="utf-8")
        cls.doc=Parse()
        cls.doc.feed(cls.html)
    def test_semantics_and_links(self):
        self.assertEqual((self.doc.h1,self.doc.main),(1,1))
        self.assertEqual(len(self.doc.ids),len(set(self.doc.ids)))
        for link in self.doc.links:
            self.assertFalse(link.startswith(("http:","https:","//")))
            if link and not link.startswith("#"):
                target=link.split("#",1)[0]
                self.assertTrue((ROOT/("index.html" if target=="./" else target)).is_file(),link)
        for marker in ("width=device-width","aria-live=\"polite\"","prefers-reduced-motion",
                       "@media(max-width:710px)","id=\"png-file\"","id=\"receipt-file\"",
                       "id=\"verify\"","id=\"status\""):
            self.assertIn(marker,self.html)
    def test_local_only(self):
        for forbidden in ("fetch(","XMLHttpRequest","sendBeacon","WebSocket","EventSource(",
                          "localStorage","sessionStorage","indexedDB","serviceWorker","<img ",
                          "<script src=","https://","http://","<iframe","window.open("):
            self.assertNotIn(forbidden,self.html)
        for marker in ("default-src 'none'","connect-src 'none'","form-action 'none'",
                       "img-src 'none'","object-src 'none'","base-uri 'none'"):
            self.assertIn(marker,self.html)
    def test_integrity_and_hold(self):
        for marker in ("crypto.subtle.digest(\"SHA-256\"","MAX_PNG_BYTES=64*1024*1024",
                       "MAX_RECEIPT_BYTES=64*1024","MAX_PIXELS=16000000",
                       "readPNG(bytes)","cursor===bytes.length","!hasMetadata",
                       "servicenow-portfolio-redacted-image-receipt/v1",
                       "r.publication_status===\"HOLD\"","r.publication_approved===false",
                       "r.independent_export_review===\"REQUIRED\"",
                       "r.service_now_dev_verified===false","r.service_now_production_verified===false",
                       "digest===r.sha256","token!==generation",
                       "SOURCE-ONLY","MOCK-ONLY","DEV-VERIFIED","PRODUCTION-VERIFIED",
                       "no ServiceNow licence"):
            self.assertIn(marker,self.html)
    def test_public_routes(self):
        for path in ("screenshot-redaction-desk.html","visual-evidence.html","index.html","sitemap.xml"):
            self.assertIn("screenshot-receipt-verifier.html",(ROOT/path).read_text(encoding="utf-8"))
if __name__=="__main__":
    unittest.main()

#!/usr/bin/env python3
"""Source-only and mock-only publication contract for the CMDB remediation desk."""
from html.parser import HTMLParser
from pathlib import Path
import json
import re
import unittest
ROOT=Path(__file__).resolve().parents[1]
class Tags(HTMLParser):
    def __init__(self):
        super().__init__();self.ids=set();self.dupes=set();self.buttons=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if a.get("id"):
            if a["id"] in self.ids:self.dupes.add(a["id"])
            self.ids.add(a["id"])
        if tag=="button" and a.get("data-fixture"):self.buttons.append(a["data-fixture"])
class Contract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text=(ROOT/"cmdb-remediation-decision-lab.html").read_text(encoding="utf-8")
        cls.tags=Tags();cls.tags.feed(cls.text)
    def test_four_source_informed_but_synthetic_fixtures(self):
        self.assertEqual(self.tags.buttons,["duplicate","relation","stale","ire"])
        self.assertFalse(self.tags.dupes)
        self.assertTrue({"main","decision-lab","evidence","owner","change","impact","decision","explanation","native","trace","export","reset"} <= self.tags.ids)
        for label in ("The client's pain","The ServiceNow solution","Architectural best practices","SOURCE-ONLY","MOCK-ONLY","CSP"):
            if label!="CSP":self.assertIn(label,self.text)
        self.assertIn("Content-Security-Policy",self.text)
    def test_decisions_fail_closed_and_receipt_never_grants_approval(self):
        for required in ('"EVIDENCE GAP"','"PARTIAL COVERAGE"','"OWNERSHIP REVIEW"','"IMPACT ASSESSMENT"','"CHANGE CONTROL"','"CONTROLLED REVIEW ONLY"','release_decision:"HOLD"','native_status:"NOT RUN"','dev_verified:false','production_verified:false','approval:false','screenshot_publication_approved:false'):
            self.assertIn(required,self.text)
        self.assertNotIn("fetch(",self.text)
        self.assertNotIn("XMLHttpRequest",self.text)
        self.assertNotIn("localStorage",self.text)
        self.assertNotIn("innerHTML",self.text)
        self.assertNotIn("<img",self.text)
        for sensitive in ("dev438211","service-now.com/","github.com/emilebennetts-cmd/Diagnostic-Workbench2","drive.google.com"):
            self.assertNotIn(sensitive,self.text)
    def test_public_evidence_claims_and_navigation(self):
        r=json.loads((ROOT/"evidence/public-verification-register.json").read_text())
        c=[v["classification"] for v in r["items"] if v["page"]=="cmdb-remediation-decision-lab.html"]
        self.assertEqual(sorted(c),["mock-only","source-only"])
        for file in ("portfolio-explorer.html","index.html","sitemap.xml"):
            self.assertIn("cmdb-remediation-decision-lab.html",(ROOT/file).read_text(),file)
if __name__=="__main__":unittest.main()

#!/usr/bin/env python3
"""Static, offline contract for the public Delivery Plan lab (not native DEV proof)."""
import re
import unittest
from pathlib import Path
from html.parser import HTMLParser

ROOT=Path(__file__).resolve().parents[1]
PAGE=ROOT/"delivery-case-study.html"

class Scanner(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids=set()
        self.duplicates=[]
        self.image_like=[]
        self.sections=0
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if a.get("id"):
            if a["id"] in self.ids:self.duplicates.append(a["id"])
            self.ids.add(a["id"])
        if tag in ("img","svg","picture","iframe","object","embed","video"):
            self.image_like.append(tag)
        if tag=="main":self.sections+=1

class DeliveryPlanContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html=PAGE.read_text(encoding="utf-8")
        cls.dom=Scanner()
        cls.dom.feed(cls.html)

    def test_layout_and_accessibility(self):
        self.assertEqual(self.dom.sections,1)
        self.assertEqual(self.dom.duplicates,[])
        self.assertIn('role="tablist"',self.html)
        self.assertIn('role="tabpanel"',self.html)
        self.assertIn('aria-live="polite"',self.html)
        self.assertIn('addEventListener("keydown"',self.html)
        self.assertIn('@media(max-width:680px)',self.html)
        self.assertIn("@media(prefers-reduced-motion:reduce)",self.html)
        for name in ("plan-tabs","plan-next","plan-prev","doc-type","doc-depth","doc-export","plan-gate"):
            self.assertIn(name,self.dom.ids)

    def test_synthetic_data_contract(self):
        views=re.search(r"const views=\[(.*?)\];\s*let current",self.html,re.S)
        self.assertIsNotNone(views)
        self.assertEqual(views.group(1).count('["'),8)
        docs=re.search(r"const types=\[(.*?)\];",self.html,re.S)
        self.assertIsNotNone(docs)
        self.assertEqual(docs.group(1).count('","')+1,8)
        self.assertIn('const depthNotes={Executive:',self.html)
        for phrase in ("MOCK-ONLY","SOURCE-ONLY","NOT RUN","HOLD","0", "native test","Jira", "Confluence","Notion"):
            self.assertIn(phrase.lower(),self.html.lower())
        self.assertIn('production_verified:false',self.html)
        self.assertIn('client_approved:false',self.html)
        self.assertIn('original_screenshots_approved:0',self.html)

    def test_privacy_and_publication(self):
        self.assertEqual(self.dom.image_like,[])
        for secret in ("drive.google.com","docs.google.com","servicenow-portfolio-control",
                       "dev438211","x_1577958","Bearer ","client_secret","token="):
            self.assertNotIn(secret,self.html)
        self.assertNotRegex(self.html,r"(?i)data:image|<script\s+src=|XMLHttpRequest|navigator\.sendBeacon")
        self.assertNotRegex(self.html,r"(?i)https?://")
        self.assertIn("no production",self.html.lower())

if __name__=="__main__":
    unittest.main()

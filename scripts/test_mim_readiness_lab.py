#!/usr/bin/env python3
"""Static contract for public, synthetic MIM readiness page. No private source."""
from html.parser import HTMLParser
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "major-incident-implementation-lab.html"

class Scan(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids=[]; self.h1=0; self.main=0; self.buttons=[]; self.links=[]
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if "id" in a: self.ids.append(a["id"])
        if tag=="h1": self.h1+=1
        if tag=="main": self.main+=1
        if tag=="button" and "data-fixture" in a: self.buttons.append(a)
        if tag=="a": self.links.append(a.get("href",""))

class MIMLabContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.content=PAGE.read_text(encoding="utf-8")
        cls.dom=Scan(); cls.dom.feed(cls.content)
    def test_semantics_and_mobile(self):
        self.assertEqual(self.dom.h1,1)
        self.assertEqual(self.dom.main,1)
        self.assertEqual(len(self.dom.ids),len(set(self.dom.ids)))
        for s in ('lang="en"','href="#main"','width=device-width','@media(max-width:600px)',
                  'prefers-reduced-motion:reduce','aria-live="polite"','input.type="checkbox"'):
            self.assertIn(s,self.content)
    def test_trust_boundaries_and_engine(self):
        self.assertEqual({x["data-fixture"] for x in self.dom.buttons},
                         {"complete","authority","integration"})
        for s in ('SOURCE-ONLY','MOCK-ONLY','DEV-VERIFIED','PRODUCTION-VERIFIED',
                  'service_now_instance:null','platform_execution:false',
                  'customer_approval:false','source_release_verified:false',
                  'critical:true','readiness_status:state','function evaluate()'):
            self.assertIn(s,self.content)
    def test_no_external_source_or_unapproved_media(self):
        forbidden=('github.com/emilebennetts-cmd/solution-lifecycle-studio',
                   'github.com/emilebennetts-cmd/Diagnostic-Workbench2',
                   'github.com/emilebennetts-cmd/servicenow-portfolio-control',
                   'fetch(', 'XMLHttpRequest','localStorage','sessionStorage',
                   '<img','<iframe','<video','https://dev')
        for token in forbidden:
            with self.subTest(token=token): self.assertNotIn(token,self.content)
        for link in self.dom.links:
            self.assertFalse(link.startswith(('http:','https:','//')))
            target=link.split('#')[0]
            if target:
                candidate=(ROOT/target).resolve()
                self.assertTrue(candidate.is_relative_to(ROOT.resolve()),link)
                if candidate.is_dir(): candidate=candidate/"index.html"
                self.assertTrue(candidate.is_file(),link)

if __name__=="__main__":
    unittest.main()

#!/usr/bin/env python3
"""Guard the public, evidence-first reviewer route (no ServiceNow runtime assumptions)."""
from html.parser import HTMLParser
from pathlib import Path
import re
import unittest

ROOT=Path(__file__).resolve().parents[1]
PAGE=ROOT/"engineering-case-studies.html"

class Audit(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links=[]
        self.buttons=[]
        self.sections=[]
        self.ids=set()
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if a.get("id"): self.ids.add(a["id"])
        if tag=="a" and a.get("href"): self.links.append(a["href"])
        if tag=="button" and a.get("data-route"): self.buttons.append((a["data-route"],a.get("aria-pressed")))
        if tag=="section": self.sections.append(a.get("id"))

class ReviewerRouteTests(unittest.TestCase):
    def setUp(self):
        self.html=PAGE.read_text(encoding="utf-8")
        self.audit=Audit()
        self.audit.feed(self.html)
    def test_three_accessible_review_tracks(self):
        self.assertIn("reviewer-route",self.audit.sections)
        self.assertEqual(self.audit.buttons,[("recruiter","true"),("architect","false"),("delivery","false")])
        self.assertIn('id="route-summary" aria-live="polite"',self.html)
        self.assertIn('role="status" aria-live="polite"',self.html)
        self.assertIn('event.key==="Home"',self.html)
        self.assertIn('event.key==="End"',self.html)
        self.assertIn("@media(max-width:480px)",self.html)
    def test_local_public_pages_only(self):
        for route in ("diagnostic-workbench-case-study.html","reusable-delivery-patterns-case-study.html",
            "verification-ledger.html","workbench-architecture.html","source-target-compatibility.html",
            "workbench-acceptance-playbook.html","diagnostic-gate-closure-lab.html",
            "pattern-library-audit-trail.html","finding-to-release-handoff.html"):
            with self.subTest(route=route):
                self.assertIn('"'+route+'"',self.html)
                self.assertTrue((ROOT/route).is_file())
        for forbidden in ("github.com/emilebennetts-cmd/solution-lifecycle-studio",
            "github.com/emilebennetts-cmd/Diagnostic-Workbench2",
            "github.com/emilebennetts-cmd/servicenow-portfolio-control",
            "<img ","<iframe ","fetch(","innerHTML="):
            self.assertNotIn(forbidden,self.html)
    def test_truthful_classification_and_non_authoritative_export(self):
        for text in ("SOURCE-ONLY","HOLD","4.22.2","4.20.0",
            "not native DEV or production execution","not an acceptance receipt",
            "not independently witnessed production outcomes"):
            self.assertIn(text.lower(),self.html.lower())
        self.assertIn('type:"text/plain;charset=utf-8"',self.html)

if __name__=="__main__":
    unittest.main()

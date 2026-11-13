#!/usr/bin/env python3
"""Source-backed closure preparation stays mock-only and never issues real approvals."""
from pathlib import Path
from html.parser import HTMLParser
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / 'delivery-case-study.html'

class Inspector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if attributes.get('id'):
            self.ids.append(attributes['id'])

class ClosureContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.page = PAGE.read_text(encoding='utf-8')
        cls.fragment = cls.page.split('<section id="closure-assurance"',1)[1].split('<section aria-labelledby="architecture"',1)[0]
        cls.parser = Inspector()
        cls.parser.feed(cls.page)

    def test_nav_and_accessible_scaffold(self):
        self.assertEqual(len(self.parser.ids),len(set(self.parser.ids)))
        self.assertIn('href="#closure-assurance"',self.page)
        for key in ('closure-scenario','closure-checklist','closure-count','closure-state',
                    'closure-blockers','closure-reset','closure-export'):
            self.assertIn(key,self.parser.ids)
        self.assertIn('aria-live="polite"',self.fragment)
        self.assertIn('@media(max-width:760px)',self.fragment)
        self.assertIn('<noscript>',self.fragment)

    def test_immutable_holds(self):
        for value in ("evidence_class:'MOCK-ONLY'","source_basis:'SOURCE-ONLY'",
                      "native_test_status:'NOT RUN'","publication_status:'HOLD'",
                      "approval_request_submitted:false","independent_closure_approved:false",
                      "actual_document_issue_verified:false","actual_owner_acceptance_verified:false",
                      "dev_verified:false","production_verified:false",
                      "original_screenshots_approved:0","handover-closure-preparation-HOLD.json"):
            self.assertIn(value,self.fragment)
        self.assertIn('Eligible to request independent review — NOT APPROVED',self.fragment)
        self.assertEqual(len(re.findall(r"^\['(?:transition|business|service|support|asbuilt|operations|report|objective|reviewer)'",self.fragment,re.M)),9)

    def test_source_pinned_three_documents_and_owners(self):
        for term in ('ART-AS-BUILT','ART-OPERATIONS-AND-SUPPORT',
                     'ART-PROJECT-CLOSURE-REPORT','Business owner','Service owner',
                     'Support owner','4.14.0','4.2.0','4.22.2',
                     'separate final approval','expiry-bounded waivers'):
            self.assertIn(term.lower(),self.fragment.lower())

    def test_no_private_source_images_or_transport(self):
        for value in ('drive.google.com','service-now.com','servicenow-portfolio-control',
                      'solution-lifecycle-studio','Diagnostic-Workbench2','<img','<iframe'):
            self.assertNotIn(value,self.fragment)
        self.assertNotRegex(self.fragment,r'\b(?:fetch|XMLHttpRequest|localStorage|sendBeacon)\s*\(')

if __name__ == '__main__':
    unittest.main()

#!/usr/bin/env python3
"""Static security, semantics and evidence-boundary contract for ITSM model."""
from html.parser import HTMLParser
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "itsm-greenfield-build-sequencer.html"

class Scan(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.h1 = 0
        self.main = 0
        self.links = []
        self.fixture_buttons = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if "id" in a:
            self.ids.append(a["id"])
        if tag == "h1":
            self.h1 += 1
        if tag == "main":
            self.main += 1
        if tag == "a":
            self.links.append(a.get("href", ""))
        if tag == "button" and "data-fixture" in a:
            self.fixture_buttons.append(a["data-fixture"])

class ITSMSequencerContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = PAGE.read_text(encoding="utf-8")
        cls.dom = Scan()
        cls.dom.feed(cls.text)

    def test_accessible_responsive_shell(self):
        self.assertEqual((self.dom.h1, self.dom.main), (1, 1))
        self.assertEqual(len(self.dom.ids), len(set(self.dom.ids)))
        for marker in ('lang="en"', 'href="#main"', 'width=device-width',
                       '@media(max-width:630px)', 'prefers-reduced-motion:reduce',
                       'aria-live="polite"', 'aria-pressed', 'role="group"'):
            self.assertIn(marker, self.text)

    def test_nine_capabilities_and_eight_controls(self):
        self.assertEqual(set(self.dom.fixture_buttons), {"baseline", "access", "evidence"})
        # Fixed, customer-neutral capability IDs are the only authorised models.
        for code in ('FND', 'INC', 'KM', 'REQ', 'CHG', 'PRB', 'MIM', 'SLA', 'CIM'):
            self.assertIn('id:"' + code + '"', self.text)
        for gate in ('baseline','discovery','requirements','design',
                     'build','tests','release','handover'):
            self.assertIn('id:"' + gate + '"', self.text)
        for marker in ('fixtures={baseline:[]', 'state=blocking.length?"BLOCKED"',
                       '"REVIEW":"MODEL COMPLETE"', 'function evaluate()'):
            self.assertIn(marker, self.text)

    def test_evidence_truthfulness_and_publication_hold(self):
        for marker in ('SOURCE-ONLY', 'MOCK-ONLY', 'DEV-VERIFIED',
                       'PRODUCTION-VERIFIED', 'service_now_instance:null',
                       'dev_execution_verified:false', 'customer_approval:false',
                       'production_deployment_verified:false',
                       'release_identity_verified:false', 'No genuine Workbench screenshot'):
            self.assertIn(marker, self.text)
        for prohibited in ('github.com/emilebennetts-cmd/solution-lifecycle-studio',
                           'github.com/emilebennetts-cmd/Diagnostic-Workbench2',
                           'github.com/emilebennetts-cmd/servicenow-portfolio-control',
                           'XMLHttpRequest', 'fetch(', 'localStorage', 'sessionStorage',
                           '<img', '<iframe', '<video', 'https://dev'):
            self.assertNotIn(prohibited, self.text)

    def test_all_references_are_public_local_files(self):
        for link in self.dom.links:
            self.assertFalse(link.startswith(("http:", "https:", "//")), link)
            target = link.split("#")[0]
            if not target:
                continue
            candidate = (ROOT / target).resolve()
            self.assertTrue(candidate.is_relative_to(ROOT.resolve()), link)
            if candidate.is_dir():
                candidate = candidate / "index.html"
            self.assertTrue(candidate.is_file(), link)

if __name__ == "__main__":
    unittest.main()

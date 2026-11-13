#!/usr/bin/env python3
"""Source, interaction and publication-safety contract for the Diagnostic operator guide."""
from html.parser import HTMLParser
from pathlib import Path
import re
import unittest

ROOT=Path(__file__).resolve().parents[1]
PAGE=(ROOT/"diagnostic-workbench-case-study.html").read_text(encoding="utf-8")
GUIDE=PAGE[PAGE.index('<section id="diagnostic-operator"'):PAGE.index('<section><h2>03 / Architectural best practices')]

class Reader(HTMLParser):
    def __init__(self):
        super().__init__()
        self.steps=[]
        self.marks=[]
        self.ids=[]
    def handle_starttag(self,tag,attributes):
        a=dict(attributes)
        if "id" in a:self.ids.append(a["id"])
        if tag=="article" and "diag-step" in a.get("class","").split():self.steps.append(a)
        if tag=="input" and "data-read" in a:self.marks.append(a)

class DiagnosticGuideContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.reader=Reader()
        cls.reader.feed(PAGE)

    def test_ten_source_grounded_distinct_steps(self):
        codes=["DW-01","DW-02","DW-03","DW-04","DW-05",
               "DW-06","DW-07","DW-08","KI-01","KI-02"]
        self.assertEqual([x["data-step"] for x in self.reader.steps], codes)
        self.assertEqual([x["data-read"] for x in self.reader.marks], codes)
        self.assertEqual(sum(x["data-lane"]=="core" for x in self.reader.steps),8)
        self.assertEqual(sum(x["data-lane"]=="ki" for x in self.reader.steps),2)

    def test_role_lane_filter_coverage(self):
        role_options=set(re.findall(r'<option value="([^"]+)">',GUIDE))
        self.assertEqual(role_options,{"all","core","ki","lead","analyst",
                                       "operator","reviewer","approver","architect"})
        for x in self.reader.steps:
            self.assertTrue(set(x["data-roles"].split()) <= role_options-{"all","core","ki"})
        self.assertIn("card.hidden=!(matchLane&&matchRole)",GUIDE)
        self.assertIn("lane.addEventListener('change',render)",PAGE)
        self.assertIn("role.addEventListener('change',render)",PAGE)

    def test_accessibility_and_small_screen_layout(self):
        self.assertEqual(len(self.reader.ids),len(set(self.reader.ids)))
        for token in ('id="diag-lane"','for="diag-lane"','id="diag-role"',
                      'for="diag-role"','id="diag-progress"','role="status"',
                      'aria-live="polite"','id="diag-reset"','id="diag-export"',
                      '.diag-step[hidden]{display:none}','@media(max-width:720px)'):
            self.assertIn(token,PAGE)
        self.assertEqual(GUIDE.count('class="diag-review"'),10)
        self.assertIn('No fresh DEV-VERIFIED or PRODUCTION-VERIFIED execution',GUIDE)

    def test_offline_export_is_permanently_not_run(self):
        for token in ("NOT RUN | HOLD","evidence_class=SOURCE-ONLY",
                      "runtime_verified=false","independent_dev_verified=false",
                      "production_verified=false","screenshot_approved=false",
                      "service_now_instance=none","client_approval=NOT GRANTED",
                      "READ ONLY","diagnostic-workbench-rehearsal-hold.txt"):
            self.assertIn(token,PAGE)
        self.assertIn("card.querySelector('[data-read]').checked=false",PAGE)

    def test_publication_and_version_boundary(self):
        for token in ("1 September 2026","30 September 2026","v0.0.1",
                      "KI 0.1.0","Knowledge Intelligence","separately deployed",
                      "Classic KI pages","read-only","Not assessed",
                      "historical","no original screenshots"):
            self.assertIn(token.lower(),GUIDE.lower())
        for prohibited in ("drive.google.com","docs.google.com",
                           "servicenow-portfolio-control","dev438211",
                           "private-user-images", "<img","<iframe","<svg",
                           "fetch(", "XMLHttpRequest", "localStorage", "sendBeacon"):
            self.assertNotIn(prohibited,GUIDE)

if __name__=="__main__":
    unittest.main()

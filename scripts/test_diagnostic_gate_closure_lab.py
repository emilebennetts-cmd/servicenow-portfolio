"""Publication and integrity contract for synthetic Diagnostic Gate Closure Lab."""
import unittest
from html.parser import HTMLParser
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PAGE=ROOT/"diagnostic-gate-closure-lab.html"

class Tags(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids=set()
        self.duplicates=set()
        self.embeds=[]
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        identifier=a.get("id")
        if identifier:
            if identifier in self.ids:
                self.duplicates.add(identifier)
            self.ids.add(identifier)
        if tag in ("img","iframe","video","source","picture","object","embed"):
            self.embeds.append(tag)

class GateClosureLabTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html=PAGE.read_text(encoding="utf-8")
        cls.parser=Tags()
        cls.parser.feed(cls.html)

    def test_accessible_self_contained_page(self):
        self.assertFalse(self.parser.duplicates)
        self.assertFalse(self.parser.embeds)
        self.assertTrue({"main","lab","scenario","reset","export","prepared",
                        "next","decision","gates","detail","tasks","queue","ticket-status"}<=self.parser.ids)
        for word in ("aria-live=\"polite\"","prefers-reduced-motion",
                     "connect-src 'none'","img-src 'none'","form-action 'none'",
                     "Skip to content","@media(max-width:500px)"):
            self.assertIn(word,self.html)

    def test_historical_boundary_and_provenance(self):
        for word in ("SOURCE-ONLY","MOCK-ONLY","DEV-REPORTED","DEV-VERIFIED",
                     "PRODUCTION-VERIFIED","NOT RUN","HOLD",
                     "DEMO PROD-SIM — NOT PRODUCTION","no ServiceNow licence",
                     "App Engine","G0","G6","D1","D11"):
            self.assertIn(word,self.html)
        for forbidden in ("dev438211","service-now.com/","drive.google.com",
                          "docs.google.com","github.com/emilebennetts-cmd/solution-lifecycle-studio",
                          "github.com/emilebennetts-cmd/Diagnostic-Workbench2",
                          "XMLHttpRequest","fetch(","localStorage","sessionStorage",
                          "indexedDB","innerHTML","<img","https://"):
            self.assertNotIn(forbidden,self.html)

    def test_false_approval_not_possible(self):
        self.assertEqual(self.html.count('id:"D'),11)
        self.assertEqual(self.html.count('id:0,title:'),1)
        for word in ('native_status:"NOT RUN"','approval:false','release:"HOLD"',
                     'dev_verified:false','production_verified:false',
                     'publication_approved:false','release_decision:"HOLD"',
                     'advisory_only:true','outcome(gate)','TASKS.filter(t=>!prepared.has(t.id))',
                     'selected=2'):
            self.assertIn(word,self.html)
        self.assertNotIn("approved:true",self.html)

    def test_public_navigation_includes_case_study(self):
        for path in ("index.html","portfolio-explorer.html","portfolio-review-guide.html","sitemap.xml"):
            self.assertIn(PAGE.name,(ROOT/path).read_text(encoding="utf-8"))

if __name__=="__main__":
    unittest.main()

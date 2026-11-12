"""Contract tests: public diagnostic coverage explorer; no private source or instance calls."""
import json
from html.parser import HTMLParser
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
HTML=(ROOT/"diagnostic-coverage-explorer.html").read_text(encoding="utf-8")
class Parser(HTMLParser):
    def __init__(self):super().__init__();self.ids=set();self.cards=[];self.scripts=0;self.media=0
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if a.get("id"):assert a["id"] not in self.ids;self.ids.add(a["id"])
        if tag=="article" and a.get("class")=="record":self.cards.append(a.get("data-domain"))
        if tag=="script":self.scripts+=1;assert not a.get("src")
        if tag in ("img","video","canvas","iframe","picture"):self.media+=1
class DiagnosticExplorerTests(unittest.TestCase):
    def test_coverage_and_navigation(self):
        p=Parser();p.feed(HTML)
        self.assertEqual(len(p.cards),20);self.assertEqual(len(set(p.cards)),10)
        self.assertEqual(p.scripts,1);self.assertEqual(p.media,0)
        for marker in ("search","domain","count","reset","records","scenario","decision","receipt","download"):
            self.assertIn(marker,p.ids)
        self.assertIn('href="diagnostic-coverage-explorer.html"',(ROOT/"index.html").read_text(encoding="utf-8"))
        self.assertIn("diagnostic-coverage-explorer.html",(ROOT/"sitemap.xml").read_text(encoding="utf-8"))
        manifest=json.loads((ROOT/"evidence/public-verification-register.json").read_text(encoding="utf-8"))
        item=next(i for i in manifest["items"] if i["id"]=="DIAGNOSTIC-COVERAGE")
        self.assertEqual(item["classification"],"source-only")
    def test_safety(self):
        for token in ("SOURCE-ONLY","MOCK-ONLY","DEV-VERIFIED","PRODUCTION-VERIFIED","NOT_ASSESSED","REJECT_UNSAFE_PAYLOAD","HOLD_COMPLETENESS","public_release_authorised:false","servicenow_dev_verified:false","production_verified:false","actual_collector_output:null","connect-src 'none'"):
            self.assertIn(token,HTML)
        for token in ("fetch(","XMLHttpRequest","localStorage","indexedDB","innerHTML","dev438211","drive.google.com","github.com/emilebennetts-cmd/Diagnostic-Workbench2","<img"):
            self.assertNotIn(token,HTML)
if __name__=="__main__":unittest.main()

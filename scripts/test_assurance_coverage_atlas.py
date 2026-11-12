"""Assurance atlas source populations and fail-closed publication contract."""
import json,re,unittest
from html.parser import HTMLParser
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PAGE=ROOT/"native-assurance-coverage-atlas.html"
class IDs(HTMLParser):
 def __init__(self):
  super().__init__();self.ids=set();self.duplicates=set()
 def handle_starttag(self,tag,attrs):
  ident=dict(attrs).get("id")
  if ident:
   if ident in self.ids:self.duplicates.add(ident)
   self.ids.add(ident)
class Contract(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.html=PAGE.read_text(encoding="utf-8")
  match=re.search(r'<script id="catalogue" type="application/json">([^<]+)</script>',cls.html)
  assert match
  cls.items=json.loads(match.group(1))
 def test_source_counts_and_unrun(self):
  self.assertEqual(len(self.items),43)
  self.assertEqual({x["id"] for x in self.items if x["track"]=="delivery"},{f"NV-{i:03d}" for i in range(1,30)})
  self.assertEqual({x["id"] for x in self.items if x["track"]=="diagnostic"},{f"DX-{i:02d}" for i in range(1,15)})
  self.assertEqual(len({x["id"] for x in self.items}),43)
  self.assertEqual({x["status"] for x in self.items},{"not_run"})
 def test_security_and_non_certification(self):
  doc=IDs();doc.feed(self.html);self.assertFalse(doc.duplicates)
  for token in ('id="search"','id="track"','id="risk"','id="cards"','id="export"',
                'publication_status:"HOLD"','independent_dev_verified:false','production_verified:false',
                'original_screenshots_approved:0','replaceChildren','textContent',
                "connect-src 'none'","img-src 'none'","SOURCE-ONLY","MOCK-ONLY","NOT RUN"):
   self.assertIn(token,self.html)
  for bad in ("innerHTML","localStorage","sessionStorage","fetch(","XMLHttpRequest",
              "<img","<iframe","sys_id=","x_eitsp_","x_1577958_","https://drive.google.com"):
   self.assertNotIn(bad,self.html)
 def test_navigation_and_manifest(self):
  for path in ("index.html","portfolio-review-guide.html","sitemap.xml"):
   self.assertIn(PAGE.name,(ROOT/path).read_text(encoding="utf-8"))
  items=json.loads((ROOT/"evidence/public-verification-register.json").read_text(encoding="utf-8"))["items"]
  entries=[x for x in items if x["id"]=="NATIVE-ASSURANCE-ATLAS"]
  self.assertEqual(len(entries),1)
  self.assertEqual(entries[0]["classification"],"source-only")
  self.assertEqual(entries[0]["page"],PAGE.name)
  self.assertIn("HOLD",entries[0]["public_screenshot_status"])
if __name__=="__main__":unittest.main()

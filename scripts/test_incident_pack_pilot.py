#!/usr/bin/env python3
"""Offline source/publication contract for the Incident pack native pilot.
Never accesses a ServiceNow instance or a private evidence file.
"""
import json
import re
import unittest
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "incident-pack-native-pilot.html"
REGISTER = ROOT / "evidence" / "public-verification-register.json"

class Scan(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.duplicates = set()
        self.tabs = []
        self.panels = []
        self.rows = []
        self.links = []
        self.images = 0
    def handle_starttag(self, tag, attr_list):
        a = dict(attr_list)
        if "id" in a:
            if a["id"] in self.ids:
                self.duplicates.add(a["id"])
            self.ids.add(a["id"])
        if a.get("role") == "tab":
            self.tabs.append(a)
        if a.get("role") == "tabpanel":
            self.panels.append(a)
        if tag == "tr" and "data-class" in a:
            self.rows.append(a["data-class"])
        if tag == "a":
            self.links.append(a.get("href",""))
        if tag in {"img","picture","svg","iframe","object","embed","video"}:
            self.images += 1

class PilotContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PAGE.read_text(encoding="utf-8")
        cls.scan = Scan()
        cls.scan.feed(cls.html)

    def test_mobile_accessibility_and_interaction_contract(self):
        self.assertFalse(self.scan.duplicates)
        self.assertEqual(len(self.scan.tabs),6)
        self.assertEqual(len(self.scan.panels),6)
        self.assertEqual(self.scan.rows.count("reported"),3)
        self.assertEqual(self.scan.rows.count("source"),1)
        self.assertEqual(self.scan.rows.count("pending"),2)
        self.assertEqual(sum(x.get("aria-selected")=="true" for x in self.scan.tabs),1)
        self.assertEqual(sum("hidden" not in x for x in self.scan.panels),1)
        for i, tab in enumerate(self.scan.tabs):
            self.assertEqual(tab["aria-controls"],f"step-{i}")
            self.assertEqual(self.scan.panels[i]["aria-labelledby"],tab["id"])
        self.assertIn("aria-live=\"polite\"",self.html)
        self.assertIn("@media(max-width:560px)",self.html)
        self.assertIn("@media(prefers-reduced-motion:reduce)",self.html)
        self.assertIn('addEventListener("keydown"',self.html)

    def test_provenance_gates(self):
        for phrase in ("SOURCE-ONLY","DEV-REPORTED","MOCK-ONLY",
                       "Production verification","83 / 83","36",
                       "29","unrun","21 October 2026","no ServiceNow licence"):
            self.assertIn(phrase.lower(),self.html.lower())
        self.assertNotIn("PRODUCTION-VERIFIED: passed",self.html)
        self.assertIn("No genuine approved screenshot",self.html)

    def test_no_private_or_remote_content(self):
        self.assertEqual(self.scan.images,0)
        for token in ("drive.google.com","servicenow-portfolio-control",
                      "dev438211","x_1577958","x_eitsp",
                      "2ca59f29718f","8cdc45578377",
                      "Epicon","DemoDev3","Bearer ","password="):
            self.assertNotIn(token,self.html)
        self.assertNotRegex(self.html,r"(?i)(?:https?://|data:image|<script\\s+src=|<link\\s+rel=[\"']stylesheet)")
        self.assertNotRegex(self.html,r"\\b(?:fetch|XMLHttpRequest|localStorage|sendBeacon)\\s*\\(")

    def test_page_links_and_manifest(self):
        for path in ("index.html","portfolio-review-guide.html","sitemap.xml"):
            self.assertIn(PAGE.name,(ROOT/path).read_text(encoding="utf-8"))
        for href in self.scan.links:
            if href.startswith("#"):
                self.assertIn(href[1:],self.scan.ids)
            else:
                self.assertTrue((ROOT / href.split("#",1)[0]).is_file(),href)
        register=json.loads(REGISTER.read_text(encoding="utf-8"))
        items=[x for x in register["items"] if x["id"]=="INCIDENT-PACK-PILOT"]
        self.assertEqual(len(items),1)
        record=items[0]
        self.assertEqual(record["classification"],"DEV-reported")
        self.assertEqual(record["page"],PAGE.name)
        self.assertIn("historical",record["runtime_verification"].lower())
        self.assertIn("hold",record["public_screenshot_status"].lower())

if __name__ == "__main__":
    unittest.main()

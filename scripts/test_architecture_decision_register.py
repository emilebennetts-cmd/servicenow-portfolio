#!/usr/bin/env python3
"""Public architecture decision case-study acceptance checks (offline)."""
from html.parser import HTMLParser
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "architecture-decision-register.html"
DOMAINS = {"evidence", "security", "delivery", "integration"}
REQUIRED = ("SOURCE-ONLY", "MOCK-ONLY", "DEV-VERIFIED", "PRODUCTION-VERIFIED")
PRIVATE = (
    "github.com/emilebennetts-cmd/solution-lifecycle-studio",
    "github.com/emilebennetts-cmd/Diagnostic-Workbench2",
    "github.com/emilebennetts-cmd/servicenow-portfolio-control",
)

class Inspection(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.duplicates = []
        self.cards = []
        self.buttons = []
        self.links = []
        self.media = []
        self.mains = 0
        self.h1s = 0
        self.lang = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "html":
            self.lang = a.get("lang")
        if a.get("id"):
            if a["id"] in self.ids:
                self.duplicates.append(a["id"])
            self.ids.add(a["id"])
        if tag == "main":
            self.mains += 1
        if tag == "h1":
            self.h1s += 1
        if tag == "article" and "decision" in a.get("class", "").split():
            self.cards.append(a)
        if tag == "button" and a.get("data-filter"):
            self.buttons.append(a)
        if tag == "a" and a.get("href"):
            self.links.append(a["href"])
        if tag in {"img", "picture", "iframe", "video", "canvas"}:
            self.media.append(tag)

class DecisionPageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PAGE.read_text(encoding="utf-8")
        cls.parser = Inspection()
        cls.parser.feed(cls.html)

    def test_semantic_mobile_and_security_contract(self):
        p = self.parser
        self.assertEqual(p.lang, "en")
        self.assertEqual(p.mains, 1)
        self.assertEqual(p.h1s, 1)
        self.assertFalse(p.duplicates)
        self.assertFalse(p.media)
        self.assertIn("name=\"viewport\"", self.html)
        self.assertIn("connect-src 'none'", self.html)
        self.assertIn("aria-live=\"polite\"", self.html)
        self.assertIn("prefers-reduced-motion", self.html)
        self.assertIn("@media print", self.html)

    def test_eight_distinct_decisions_and_filter_contract(self):
        p = self.parser
        self.assertEqual(len(p.cards), 8)
        self.assertEqual([x["id"] for x in p.cards], [f"adr-{n:02}" for n in range(1,9)])
        self.assertEqual({x["data-domain"] for x in p.cards}, DOMAINS)
        self.assertTrue(all(x.get("data-search") for x in p.cards))
        self.assertEqual({x["data-filter"] for x in p.buttons}, DOMAINS | {"all"})
        self.assertEqual(sum(x.get("aria-pressed") == "true" for x in p.buttons), 1)
        self.assertIn("card.hidden=!match", self.html)
        self.assertIn("empty.hidden=count!==0", self.html)

    def test_evidence_provenance_and_no_private_links(self):
        for label in REQUIRED:
            self.assertIn(label, self.html)
        for label in ("0. No confidential captures", "not newly DEV-VERIFIED",
                      "No PRODUCTION-VERIFIED claim", "SOURCE-DERIVED · NOT APPROVED"):
            self.assertIn(label, self.html)
        for restricted in PRIVATE:
            self.assertNotIn(restricted, self.html)
        self.assertNotIn("dev438211.service-now.com", self.html)
        for href in self.parser.links:
            if href.startswith("./"):
                self.assertTrue((ROOT / href[2:].split("#",1)[0]).is_file(), href)

    def test_navigation_and_discovery(self):
        self.assertIn("architecture-decision-register.html", (ROOT / "index.html").read_text(encoding="utf-8"))
        self.assertIn("architecture-decision-register.html", (ROOT / "architecture-atlas.html").read_text(encoding="utf-8"))
        self.assertIn("architecture-decision-register.html", (ROOT / "sitemap.xml").read_text(encoding="utf-8"))
        
if __name__ == "__main__":
    unittest.main()

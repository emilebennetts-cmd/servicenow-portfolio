"""Conservative contract for the public entitlement readiness review.

A public worksheet must never certify contractual rights, native ServiceNow
execution, or original screenshot publication. No customer information belongs here.
"""
from html.parser import HTMLParser
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "entitlement-readiness.html"
HOME = ROOT / "index.html"
EXPLORER = ROOT / "portfolio-explorer.html"
SITEMAP = ROOT / "sitemap.xml"
CANONICAL = "https://emilebennetts-cmd.github.io/servicenow-portfolio/entitlement-readiness.html"

class Audit(HTMLParser):
    def __init__(self):
        super().__init__()
        self.cards = []
        self.filters = []
        self.links = []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "article" and "entitlement-card" in attrs.get("class","").split():
            self.cards.append((attrs.get("data-id"),attrs.get("data-domain")))
        if tag == "button" and "data-domain-filter" in attrs:
            self.filters.append(attrs["data-domain-filter"])
        if tag == "a" and attrs.get("href"):
            self.links.append(attrs["href"])

class EntitlementReadinessTests(unittest.TestCase):
    def setUp(self):
        self.html = PAGE.read_text(encoding="utf-8")
        self.audit = Audit()
        self.audit.feed(self.html)

    def test_eight_unique_source_bounded_reviews(self):
        self.assertEqual(8,len(self.audit.cards))
        self.assertEqual(8,len({i for i,_ in self.audit.cards}))
        self.assertEqual({"all","platform","operations","extension"},set(self.audit.filters))
        self.assertTrue(all(domain in {"platform","operations","extension"} for _,domain in self.audit.cards))

    def test_export_never_certifies(self):
        for literal in ("review_status:'UNREVIEWED'","verification_status:'NOT VERIFIED'",
                        "release_status:'HOLD'","native_dev_verified:false",
                        "production_verified:false","screenshot_publication_approved:false",
                        "licence_approval:false","independent_native_test:'NOT RUN'",
                        "licence_entitlement_review:'REQUIRED'"):
            self.assertIn(literal,self.html)
        self.assertNotIn("localStorage",self.html)
        self.assertNotIn("sessionStorage",self.html)
        self.assertNotIn("fetch(",self.html)
        self.assertNotIn("XMLHttpRequest",self.html)
        self.assertNotIn("<img",self.html.lower())
        self.assertNotIn('og:image',self.html.lower())

    def test_web_csp_and_link_boundaries(self):
        self.assertIn("connect-src 'none'",self.html)
        self.assertIn("img-src 'none'",self.html)
        self.assertIn(CANONICAL,self.html)
        for href in self.audit.links:
            if href.startswith("https://"):
                self.assertTrue(href.startswith("https://www.servicenow.com/docs/"),href)
            else:
                self.assertTrue(href.endswith(".html") or href.endswith("#main") or href=="./",href)

    def test_navigation_is_discoverable(self):
        self.assertIn("entitlement-readiness.html",HOME.read_text(encoding="utf-8"))
        self.assertIn("entitlement-readiness.html",EXPLORER.read_text(encoding="utf-8"))
        self.assertEqual(1,SITEMAP.read_text(encoding="utf-8").count("<loc>"+CANONICAL+"</loc>"))

    def test_public_register_classifies_only_website_source(self):
        import json
        register = json.loads((ROOT / "evidence/public-verification-register.json").read_text(encoding="utf-8"))
        claims = register["items"]
        self.assertEqual(len(claims), len({c["id"] for c in claims}))
        own = [c for c in claims if c.get("page") == "entitlement-readiness.html"]
        self.assertEqual(1, len(own))
        self.assertEqual("source-only", own[0]["classification"])
        self.assertIn("NOT VERIFIED", own[0]["runtime_verification"])
        self.assertIn("No original", own[0]["public_screenshot_status"])

    def test_sitemap_and_directory_match_without_hardcoded_totals(self):
        paths = re.findall(r'/servicenow-portfolio/([a-z0-9-]+\\.html)</loc>', SITEMAP.read_text(encoding="utf-8"))
        catalog = re.findall(r'<li class="result"', EXPLORER.read_text(encoding="utf-8"))
        self.assertEqual(len(paths), len(set(paths)))
        self.assertEqual(paths, sorted(paths))
        self.assertEqual(len(paths), len(catalog))

if __name__ == "__main__":
    unittest.main()

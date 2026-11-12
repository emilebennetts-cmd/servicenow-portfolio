"""Fail-closed publication contract tests for browser-only integration simulation."""
import unittest
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "integration-contract-lab.html"

class Tags(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.duplicates = set()
        self.unsafe_embeds = []
        self.links = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get("id"):
            if a["id"] in self.ids:
                self.duplicates.add(a["id"])
            self.ids.add(a["id"])
        if tag in ("img", "iframe", "video", "picture", "object", "embed"):
            self.unsafe_embeds.append(tag)
        if tag == "a":
            self.links.append(a.get("href", ""))

class IntegrationContractLabTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PAGE.read_text(encoding="utf-8")
        cls.parser = Tags()
        cls.parser.feed(cls.html)

    def test_accessibility_and_navigation(self):
        self.assertFalse(self.parser.duplicates)
        self.assertFalse(self.parser.unsafe_embeds)
        self.assertTrue({"main", "scenario", "provider", "direction", "revision", "synced",
                         "remote", "known", "linked", "approved", "mapping", "protected",
                         "evaluate", "status", "outcome", "explain", "trace"} <= self.parser.ids)
        self.assertIn('aria-live="polite"', self.html)
        self.assertIn("prefers-reduced-motion", self.html)
        for index in ("index.html", "portfolio-explorer.html", "portfolio-review-guide.html", "sitemap.xml"):
            self.assertIn("integration-contract-lab.html", (ROOT / index).read_text(encoding="utf-8"))

    def test_security_and_truth_boundary(self):
        for expected in ("SOURCE-ONLY", "MOCK-ONLY", "DEV-REPORTED", "DEV-VERIFIED",
                         "PRODUCTION-VERIFIED", "NOT RUN", "HOLD", "connect-src 'none'",
                         "img-src 'none'", "no ServiceNow licence",
                         "Live provider sync: HOLD", "G07", "G03"):
            self.assertIn(expected, self.html)
        for unsafe in ("fetch(", "XMLHttpRequest", "localStorage", "sessionStorage",
                       "indexedDB", "innerHTML", "dev438211", "service-now.com/",
                       "github.com/emilebennetts-cmd/Diagnostic-Workbench2",
                       "github.com/emilebennetts-cmd/solution-lifecycle-studio",
                       "drive.google.com", "docs.google.com", "<img"):
            self.assertNotIn(unsafe, self.html)

    def test_all_contract_branches_remain_advisory(self):
        for token in ("revision<=synced", "remote>known", "direction===\"inbound\"",
                      "!linked", "!$(\"approved\").checked", "!$(\"mapping\").checked",
                      "Number.isSafeInteger", "trace.replaceChildren()", "state=\"DRAFT\"",
                      "state=\"REVIEW\"", "Result: manual reconciliation",
                      "not executed", "write action remains disabled"):
            self.assertIn(token, self.html)

if __name__ == "__main__":
    unittest.main()

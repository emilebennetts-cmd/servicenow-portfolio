"""Native protocol publication contract: preparatory only; never executed evidence."""
import json
import re
import unittest
from pathlib import Path
from html.parser import HTMLParser

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "native-assurance-coverage-atlas.html"

class IDs(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.duplicates = set()
    def handle_starttag(self, tag, attrs):
        ident = dict(attrs).get("id")
        if ident:
            if ident in self.ids:
                self.duplicates.add(ident)
            self.ids.add(ident)

class NativeProtocolContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.doc = PAGE.read_text(encoding="utf-8")
        match = re.search(r'<script id="protocol-data" type="application/json">([^<]+)</script>', cls.doc)
        assert match, "Protocol JSON is missing"
        cls.items = json.loads(match.group(1))

    def test_source_population_references(self):
        catalogue = json.loads(re.search(
            r'<script id="catalogue" type="application/json">([^<]+)</script>', self.doc
        ).group(1))
        ids = {item["id"] for item in catalogue}
        self.assertEqual(len(self.items), 9)
        self.assertEqual(len({p["id"] for p in self.items}), 9)
        self.assertTrue({p["id"] for p in self.items}.issubset(ids))
        self.assertEqual(sum(p["id"].startswith("DX-") for p in self.items), 3)

    def test_procedural_substance_and_safety(self):
        for item in self.items:
            with self.subTest(case=item["id"]):
                self.assertTrue(item["role"] and item["pre"] and item["expect"])
                self.assertGreaterEqual(len(item["steps"]), 3)
                self.assertTrue(all(len(step) > 30 for step in item["steps"]))
                self.assertIn("evidence", item)
                self.assertGreater(len(item["stop"]), 30)
        self.assertIn("isolated", self.doc.lower())
        self.assertIn("NOT RUN", self.doc)

    def test_non_certifying_receipt(self):
        for token in ('schema:"native-protocol-preparation-v1"', 'execution_status:"NOT RUN"',
                      'publication_status:"HOLD"', 'independent_dev_verified:false',
                      'production_verified:false', 'screenshot_publication_approved:false',
                      'actual_result:"NOT RECORDED"', 'approval:"NOT GRANTED"'):
            self.assertIn(token, self.doc)
        for forbidden in ("innerHTML", "fetch(", "XMLHttpRequest", "localStorage",
                          "sessionStorage", "<img", "sys_id=", "https://drive.google.com"):
            self.assertNotIn(forbidden, self.doc)

    def test_structure(self):
        html = IDs()
        html.feed(self.doc)
        self.assertFalse(html.duplicates)
        self.assertTrue({"execution-protocols", "protocol-data", "protocol-select",
                         "protocol-export", "protocol-detail", "protocol-status"}.issubset(html.ids))
        self.assertIn("connect-src 'none'", self.doc)
        self.assertIn("replaceChildren", self.doc)
        self.assertIn("textContent", self.doc)

if __name__ == "__main__":
    unittest.main()

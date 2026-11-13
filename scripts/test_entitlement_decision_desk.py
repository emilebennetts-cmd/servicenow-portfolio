#!/usr/bin/env python3
"""Offline entitlement desk: requirements must never become licence/DEV approval."""
from html.parser import HTMLParser
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "operational-readiness-runbook.html"


class Tags(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = []
        self.images = 0
        self.buttons = []
        self.links = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get("id"):
            self.ids.append(a["id"])
        if tag == "img":
            self.images += 1
        if tag == "button" and "data-entitlement-filter" in a:
            self.buttons.append((a["data-entitlement-filter"], a.get("aria-pressed")))
        if tag == "a":
            self.links.append(a.get("href", ""))


class EntitlementGateContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = PAGE.read_text(encoding="utf-8")
        cls.tags = Tags()
        cls.tags.feed(cls.html)

    def test_accessible_ten_category_review(self):
        self.assertEqual(len(self.tags.ids), len(set(self.tags.ids)))
        self.assertIn("entitlement-gate", self.tags.ids)
        for field in ("entitlement-cards", "entitlement-count", "entitlement-progress",
                      "entitlement-status", "entitlement-empty", "entitlement-export",
                      "entitlement-reset"):
            self.assertIn(field, self.tags.ids)
        ids = re.findall(r"\['(ENT-\d\d)','", self.html)
        self.assertEqual(ids, ["ENT-%02d" % n for n in range(1, 11)])
        self.assertEqual(set(self.tags.buttons),
                         {("all", "true"), ("unknown", "false"), ("optional", "false")})
        self.assertIn("aria-live=\"polite\"", self.html)
        self.assertIn("#entitlement-gate", self.tags.links)
        self.assertIn("@media(max-width:760px)", self.html)

    def test_all_outputs_stay_hold_and_synthetic(self):
        for item in ("schema:'entitlement-decision-draft-v1'",
                     "evidence_class:'MOCK-ONLY'", "source_basis:'SOURCE-ONLY'",
                     "publication_status:'HOLD'", "contract_verified:false",
                     "independent_approval:false", "dev_verified:false",
                     "production_verified:false", "installation_executed:false",
                     "licence_purchase_authorised:false",
                     "requirement_level_reconciliation_complete:false",
                     "entitlementProblems(decisions)", "entitlement-review-HOLD.json",
                     "does not", "unverified", "Self-reported"):
            self.assertIn(item.lower(), self.html.lower())
        self.assertIn("entitlementSafeAlias=/^[A-Za-z0-9]", self.html)
        self.assertIn("if(row.selection!=='UNKNOWN'&&!row.evidence_alias)", self.html)

    def test_distinguishes_runbook_from_generic_categories(self):
        for phrase in ("20 showcase requirements", "not the ten capability categories",
                       "client-neutral review prompts", "OOTB-first design",
                       "App Engine/custom-table", "Integration Hub",
                       "Service Graph", "Now Assist", "HRSD/CSM",
                       "Performance Analytics", "ITOM Visibility/Discovery"):
            self.assertIn(phrase.lower(), self.html.lower())

    def test_no_unauthorised_pixels_or_data_transport(self):
        self.assertEqual(self.tags.images, 0)
        self.assertIn("connect-src 'none'", self.html)
        self.assertIn("img-src 'none'", self.html)
        for forbidden in ("drive.google.com", "dev438211", "x_1577958",
                          "servicenow-portfolio-control", "api.github.com/repos"):
            self.assertNotIn(forbidden, self.html)
        self.assertNotRegex(self.html, r"\b(?:fetch|XMLHttpRequest|localStorage|sendBeacon)\s*\(")
        self.assertIn("www.servicenow.com/docs/", self.html)


if __name__ == "__main__":
    unittest.main()

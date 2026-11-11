#!/usr/bin/env python3
"""Keep reviewer paths public without changing source repository visibility."""
from html.parser import HTMLParser
from pathlib import Path
import unittest
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
ENTRYPOINTS = (
    "index.html",
    "workbench-evidence-ledger.html",
    "workbench-acceptance-playbook.html",
    "diagnostic-workbench-case-study.html",
    "reusable-delivery-patterns-case-study.html",
    "workbench-architecture-gallery.html",
    "engineering-case-studies.html",
)


class AnchorParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            href = dict(attrs).get("href")
            if href:
                self.links.append(href)


class PublicReviewAccessTests(unittest.TestCase):
    def test_reviewer_pages_do_not_link_to_access_restricted_repositories(self):
        for name in ENTRYPOINTS:
            with self.subTest(page=name):
                parser = AnchorParser()
                parser.feed((ROOT / name).read_text(encoding="utf-8"))
                restricted = [
                    url for url in parser.links
                    if urlsplit(url).netloc == "github.com"
                    and urlsplit(url).path.startswith("/emilebennetts-cmd/")
                    and not urlsplit(url).path.startswith("/emilebennetts-cmd/servicenow-portfolio")
                ]
                self.assertEqual(restricted, [], "Public reviewer links must resolve to a public-safe summary")

    def test_homepage_evidence_and_acceptance_routes_in_mobile_and_hero(self):
        page = (ROOT / "index.html").read_text(encoding="utf-8")
        for target in ("workbench-evidence-ledger.html", "workbench-acceptance-playbook.html"):
            with self.subTest(target=target):
                self.assertGreaterEqual(page.count('href="' + target + '"'), 2)
                self.assertTrue((ROOT / target).is_file())


if __name__ == "__main__":
    unittest.main()

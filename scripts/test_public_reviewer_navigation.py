#!/usr/bin/env python3
"""Public reviewer routes must not dead-end at private source repositories.

Static, offline, no credentials or private source required. CI discovers this
module as part of the Portfolio quality gate.
"""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import unittest

ROOT = Path(__file__).resolve().parents[1]
REVIEW_PAGES = (
    "visual-evidence.html",
    "visual-evidence-intake.html",
    "diagnostic-case-study.html",
    "delivery-case-study.html",
    "engineering-evidence.html",
    "workbench-experience.html",
    "workbench-architecture.html",
)
RESTRICTED = {
    "solution-lifecycle-studio",
    "Diagnostic-Workbench2",
    "servicenow-portfolio-control",
}


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hrefs = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            href = dict(attrs).get("href")
            if href:
                self.hrefs.append(href)


def is_restricted(href):
    url = urlsplit(href)
    if url.netloc.lower() not in ("github.com", "www.github.com"):
        return False
    parts = url.path.strip("/").split("/")
    return len(parts) >= 2 and parts[0].lower() == "emilebennetts-cmd" and parts[1] in RESTRICTED


class ReviewerNavigationTests(unittest.TestCase):
    def test_no_public_reviewer_links_into_private_repositories(self):
        for name in REVIEW_PAGES:
            with self.subTest(page=name):
                page = Links()
                page.feed((ROOT / name).read_text(encoding="utf-8"))
                self.assertEqual([], [url for url in page.hrefs if is_restricted(url)])

    def test_local_reviewer_links_resolve_to_public_pages(self):
        for name in REVIEW_PAGES:
            page = Links()
            page.feed((ROOT / name).read_text(encoding="utf-8"))
            for href in page.hrefs:
                url = urlsplit(href)
                if url.scheme or url.netloc or not url.path or url.path.startswith("/"):
                    continue
                target = (ROOT / name).parent / unquote(url.path)
                if target.suffix.lower() != ".html":
                    continue
                with self.subTest(page=name, href=href):
                    self.assertTrue(target.resolve().is_relative_to(ROOT.resolve()))
                    self.assertTrue(target.is_file())

    def test_source_link_labels_do_not_misstate_access(self):
        for name in ("visual-evidence-intake.html", "workbench-experience.html"):
            with self.subTest(page=name):
                body = (ROOT / name).read_text(encoding="utf-8")
                self.assertNotIn("Inspect public source</a>", body)
                self.assertNotIn("Inspect source overview", body)


if __name__ == "__main__":
    unittest.main()

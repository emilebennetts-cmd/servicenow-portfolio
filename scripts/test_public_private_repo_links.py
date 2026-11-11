#!/usr/bin/env python3
"""Guard all published top-level HTML pages against links to private repositories.

The audit is deliberately offline and tests public browser navigation rather
than private source availability. CI discovery includes this module.
"""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
import unittest

ROOT = Path(__file__).resolve().parents[1]
PRIVATE = {"solution-lifecycle-studio", "diagnostic-workbench2", "servicenow-portfolio-control"}
OWNER = "emilebennetts-cmd"


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.urls = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            href = dict(attrs).get("href")
            if href:
                self.urls.append(href)


def restricted(href):
    parsed = urlsplit(href)
    if parsed.netloc.lower() not in {"github.com", "www.github.com"}:
        return False
    parts = [segment.lower() for segment in parsed.path.strip("/").split("/")]
    return len(parts) > 1 and parts[0] == OWNER and parts[1] in PRIVATE


class PublicNavigationBoundaryTests(unittest.TestCase):
    def test_all_root_html_pages_have_no_links_into_private_repositories(self):
        pages = sorted(ROOT.glob("*.html"))
        self.assertGreaterEqual(len(pages), 50, "Unexpectedly reduced public HTML coverage")
        failures = []
        for page in pages:
            parser = Links()
            parser.feed(page.read_text(encoding="utf-8"))
            for href in parser.urls:
                if restricted(href):
                    failures.append((page.name, href))
        self.assertEqual([], failures, "Public visitors must receive public-safe evidence summaries")

    def test_private_url_detection_handles_case_and_protocol_relative(self):
        self.assertTrue(restricted("https://github.com/emilebennetts-cmd/Diagnostic-Workbench2"))
        self.assertTrue(restricted("//www.github.com/emilebennetts-cmd/solution-lifecycle-studio/blob/main/README.md"))
        self.assertTrue(restricted("https://github.com/emilebennetts-cmd/servicenow-portfolio-control"))
        self.assertFalse(restricted("https://github.com/emilebennetts-cmd/servicenow-portfolio"))
        self.assertFalse(restricted("./diagnostic-workbench-case-study.html"))
        self.assertFalse(restricted("https://github.com/someone-else/Diagnostic-Workbench2"))


if __name__ == "__main__":
    unittest.main()

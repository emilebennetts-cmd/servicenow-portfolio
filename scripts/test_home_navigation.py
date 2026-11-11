#!/usr/bin/env python3
"""Guard the responsive, public-safe homepage navigation.

Only standard-library dependencies. Discovered by the portfolio quality workflow.
"""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
HTML = (ROOT / "index.html").read_text(encoding="utf-8")


class NavigationLinks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hrefs = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            href = dict(attrs).get("href")
            if href:
                self.hrefs.append(href)


def nav(class_name):
    fragment = re.search(
        rf'<nav class="{re.escape(class_name)}"\s+aria-label="[^"]+"[^>]*>(.*?)</nav>',
        HTML,
        flags=re.DOTALL,
    )
    if not fragment:
        raise AssertionError(f"Missing {class_name} navigation")
    parser = NavigationLinks()
    parser.feed(fragment.group(1))
    return fragment.group(1), parser.hrefs


class ResponsiveNavigationTests(unittest.TestCase):
    def test_desktop_has_four_prioritised_links_not_an_overflowing_directory(self):
        _, links = nav("nav")
        self.assertEqual(
            links,
            [
                "engineering-case-studies.html",
                "workbench-architecture-gallery.html",
                "visual-evidence.html",
                "#contact",
            ],
        )

    def test_directory_remains_discoverable_on_desktop_and_mobile(self):
        fragment, links = nav("mobile-links")
        self.assertEqual(len(links), 18)
        self.assertEqual(fragment.count('class="directory-heading"'), 3)
        self.assertIn('class="mobile-directory"', HTML)
        self.assertIn('aria-label="Browse full portfolio directory"', HTML)
        self.assertIn('aria-label="Portfolio page directory"', HTML)
        for required in (
            "portfolio-review-guide.html",
            "delivery-case-study.html",
            "diagnostic-workbench-case-study.html",
            "reusable-delivery-patterns-case-study.html",
            "visual-evidence.html",
            "workbench-evidence-ledger.html",
            "workbench-acceptance-playbook.html",
            "finding-to-release-handoff.html",
        ):
            with self.subTest(required=required):
                self.assertIn(required, links)

    def test_all_header_destinations_exist_and_fragments_resolve(self):
        links = nav("nav")[1] + nav("mobile-links")[1]
        for link in links:
            with self.subTest(href=link):
                target = urlsplit(link)
                self.assertFalse(target.scheme or target.netloc)
                path = unquote(target.path)
                self.assertFalse(path.startswith("/"))
                destination = ROOT / path if path else ROOT / "index.html"
                self.assertTrue(destination.is_file(), f"Missing public page: {link}")
                if target.fragment and not path:
                    self.assertRegex(HTML, rf'\bid="{re.escape(unquote(target.fragment))}"')

    def test_responsive_breakpoints_and_keyboard_support(self):
        self.assertIn('<style id="reviewer-navigation-20261111">', HTML)
        css = HTML.split('<style id="reviewer-navigation-20261111">', 1)[1].split("</style>", 1)[0]
        self.assertIn("@media(max-width:820px)", css)
        self.assertIn("@media(max-width:540px)", css)
        self.assertIn("max-height:min(78vh,650px)", css)
        self.assertIn("overscroll-behavior:contain", css)
        self.assertIn("min-height:44px", css)
        self.assertIn("grid-template-columns:1fr", css)
        self.assertIn("event.key === 'Escape'", HTML)
        self.assertIn("summary?.focus()", HTML)
        self.assertIn(":focus-visible", HTML)


if __name__ == "__main__":
    unittest.main()

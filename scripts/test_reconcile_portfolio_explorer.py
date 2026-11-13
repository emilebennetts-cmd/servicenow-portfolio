"""Offline regression coverage for the curated portfolio explorer contract."""
from __future__ import annotations

import importlib.util
from pathlib import Path
import tempfile
import unittest

PATH = Path(__file__).with_name("reconcile_portfolio_explorer.py")
spec = importlib.util.spec_from_file_location("reconcile_portfolio_explorer", PATH)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def row(filename: str, category: str = "Start here") -> str:
    return (
        f'<li class="result" data-category="{category}" '
        f'data-search="{filename} {category}">'
        f'<span class="type">{category}</span>'
        f'<a href="{filename}">Example</a>'
        f'<span class="locator">{filename}</span></li>'
    )


def explorer(entries: str, count: int) -> str:
    return (
        '<html><body><strong id="total">' + str(count) + '</strong>'
        '<h2>Search ' + str(count) + ' published pages.</h2>'
        '<ul class="directory" id="results">' + entries + '</ul>'
        '</body></html>'
    )


class CatalogueTests(unittest.TestCase):
    def setUp(self):
        self.folder = tempfile.TemporaryDirectory()
        self.root = Path(self.folder.name)
        (self.root / "index.html").write_text("<title>Portfolio home</title>", encoding="utf-8")
        (self.root / "portfolio-explorer.html").write_text("<title>Explorer</title>", encoding="utf-8")

    def tearDown(self):
        self.folder.cleanup()

    def test_stale_counts_fail_closed(self):
        source = explorer(row("index.html"), 3)
        errors = module.problems(self.root, source)
        self.assertTrue(any("Heading count stale" in message for message in errors))
        self.assertTrue(any("Hero count stale" in message for message in errors))
        self.assertFalse(module.problems(self.root, module.reconcile(self.root, source)))

    def test_new_page_is_added_without_overwriting_curated_row(self):
        (self.root / "new-demo.html").write_text(
            "<title>Research &amp; Design | ServiceNow Showcase</title>", encoding="utf-8"
        )
        original = row("index.html")
        source = explorer(original, 1)
        refreshed = module.reconcile(self.root, source)
        self.assertIn(original, refreshed)
        self.assertIn('href="new-demo.html"', refreshed)
        self.assertIn("Research &amp; Design", refreshed)
        self.assertIn("Search 2 published pages.", refreshed)
        self.assertFalse(module.problems(self.root, refreshed))
        self.assertEqual(refreshed, module.reconcile(self.root, refreshed))

    def test_duplicate_and_unpublished_pages_are_rejected(self):
        source = explorer(row("index.html") * 2 + row("ghost.html"), 1)
        errors = module.problems(self.root, source)
        self.assertTrue(any("Duplicate result" in e for e in errors))
        self.assertTrue(any("Unknown/unpublished page: ghost.html" in e for e in errors))

    def test_symlinks_are_excluded(self):
        target = self.root / "private.html"
        target.write_text("<title>Private</title>", encoding="utf-8")
        (self.root / "linked.html").symlink_to(target)
        pages = module.public_pages(self.root)
        self.assertNotIn("linked.html", pages)
        self.assertIn("private.html", pages)

    def test_html_title_is_escaped_and_not_executable(self):
        (self.root / "example.html").write_text(
            "<title>Review < Risk &amp; Safety</title>", encoding="utf-8"
        )
        refreshed = module.reconcile(self.root, explorer(row("index.html"), 1))
        self.assertIn("Review &lt; Risk &amp; Safety", refreshed)
        self.assertFalse(module.problems(self.root, refreshed))


if __name__ == "__main__":
    unittest.main()

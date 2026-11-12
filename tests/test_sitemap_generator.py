#!/usr/bin/env python3
"""Sitemap generator acceptance: coverage, determinism and symlink boundaries."""
import sys
from pathlib import Path
import tempfile
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from generate_sitemap import public_pages, render, BASE


class SitemapGeneratorTests(unittest.TestCase):
    def test_all_current_published_pages_are_in_render(self):
        pages = public_pages()
        document = ET.fromstring(render())
        urls = [x.text for x in document.findall("{http://www.sitemaps.org/schemas/sitemap/0.9}url/{http://www.sitemaps.org/schemas/sitemap/0.9}loc")]
        expected = [BASE + ("" if p == "index.html" else p) for p in pages]
        self.assertEqual(urls, expected)
        self.assertEqual(len(urls), len(set(urls)))
        self.assertEqual(render(), render())

    def test_generator_excludes_nested_files_and_symlink(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "index.html").write_text("<html></html>")
            (root / "alpha.html").write_text("<html></html>")
            (root / "docs").mkdir()
            (root / "docs" / "private.html").write_text("<html></html>")
            outside = root / "docs" / "private.html"
            (root / "alias.html").symlink_to(outside)
            self.assertEqual(public_pages(root), ["index.html", "alpha.html"])
            output = render(root)
            self.assertNotIn("alias.html", output)
            self.assertNotIn("private.html", output)

    def test_missing_index_fails_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            (Path(directory) / "other.html").write_text("")
            with self.assertRaisesRegex(ValueError, "missing index.html"):
                public_pages(directory)


if __name__ == "__main__":
    unittest.main()

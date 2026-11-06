#!/usr/bin/env python3
"""Regression tests for the portfolio's dependency-free HTML quality gate."""
import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SCRIPT = Path(__file__).with_name("check_site.py")
spec = importlib.util.spec_from_file_location("check_site", SCRIPT)
site = importlib.util.module_from_spec(spec)
spec.loader.exec_module(site)

class QualityGateTests(unittest.TestCase):
    def test_parser_captures_links_ids_and_alt(self):
        p = site.Inspector()
        p.feed('<html lang="en"><head><title>Case study</title></head><body><a href="case.html#proof">Proof</a><img src="photo.png" alt=""><section id="proof"></section></body></html>')
        self.assertTrue(p.lang)
        self.assertTrue(p.title)
        self.assertIn("proof", p.ids)
        self.assertIn(("a", "case.html#proof"), p.links)
        self.assertEqual(p.images[0]["alt"], "")

    def test_missing_title_and_alt_fail(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "index.html").write_text('<html lang="en"><img src="a.png"></html>', encoding="utf-8")
            (root / "a.png").write_bytes(b"test")
            with patch.object(site, "ROOT", root):
                self.assertEqual(site.main(), 1)

    def test_valid_cross_page_anchor_passes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "index.html").write_text('<html lang="en"><title>Home</title><a href="case.html#proof">Case</a></html>', encoding="utf-8")
            (root / "case.html").write_text('<html lang="en"><title>Case</title><h1 id="proof">Proof</h1></html>', encoding="utf-8")
            with patch.object(site, "ROOT", root):
                self.assertEqual(site.main(), 0)

    def test_broken_fragment_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "index.html").write_text('<html lang="en"><title>Home</title><a href="#missing">Missing</a></html>', encoding="utf-8")
            with patch.object(site, "ROOT", root):
                self.assertEqual(site.main(), 1)

if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3
"""Security and document-integrity regression tests for the portfolio checker."""
import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

spec = importlib.util.spec_from_file_location("check_site", Path(__file__).with_name("check_site.py"))
site = importlib.util.module_from_spec(spec)
spec.loader.exec_module(site)

class IntegrityTests(unittest.TestCase):
    def test_duplicate_ids_fail(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "index.html").write_text('<html lang="en"><title>Test</title><div id="same"></div><p id="same"></p></html>')
            with patch.object(site, "ROOT", root):
                self.assertEqual(site.main(), 1)

    def test_parent_directory_escape_fails_even_if_file_exists(self):
        with tempfile.TemporaryDirectory() as folder:
            base = Path(folder)
            root = base / "site"
            root.mkdir()
            (base / "outside.html").write_text('<html lang="en"><title>Outside</title></html>')
            (root / "index.html").write_text('<html lang="en"><title>Test</title><a href="../outside.html">Outside</a></html>')
            with patch.object(site, "ROOT", root):
                self.assertEqual(site.main(), 1)

    def test_encoded_parent_directory_escape_fails(self):
        with tempfile.TemporaryDirectory() as folder:
            base = Path(folder)
            root = base / "site"
            root.mkdir()
            (base / "outside.html").write_text("private")
            (root / "index.html").write_text('<html lang="en"><title>Test</title><a href="%2e%2e/outside.html">Outside</a></html>')
            with patch.object(site, "ROOT", root):
                self.assertEqual(site.main(), 1)

    def test_unique_ids_and_internal_link_pass(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "index.html").write_text('<html lang="en"><title>Test</title><a href="#section">Section</a><section id="section"></section></html>')
            with patch.object(site, "ROOT", root):
                self.assertEqual(site.main(), 0)

if __name__ == "__main__":
    unittest.main()

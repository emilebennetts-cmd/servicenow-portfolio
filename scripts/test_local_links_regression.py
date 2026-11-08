#!/usr/bin/env python3
"""Regression tests for the portfolio's local-link publication gate.

Run: python3 -m unittest discover -s scripts -p 'test_local_links_regression.py'
No network access or third-party packages required.
"""
import tempfile
import unittest
from pathlib import Path
from check_local_links import audit


class LocalLinkRegression(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)

    def page(self, name, body):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text('<!doctype html><html><body>' + body + '</body></html>', encoding='utf-8')

    def test_local_file_and_fragment(self):
        self.page('index.html', '<a href="details.html#proof">Proof</a>')
        self.page('details.html', '<section id="proof">Verified anchor</section>')
        self.assertEqual(audit(self.root), [])

    def test_missing_local_file(self):
        self.page('index.html', '<a href="missing.html">Missing</a>')
        self.assertTrue(any('missing local target' in error for error in audit(self.root)))

    def test_missing_fragment(self):
        self.page('index.html', '<a href="details.html#unknown">Proof</a>')
        self.page('details.html', '<h2 id="known">Known</h2>')
        self.assertTrue(any('missing fragment' in error for error in audit(self.root)))

    def test_fragment_only(self):
        self.page('index.html', '<a href="#overview">Overview</a><h2 id="overview">Overview</h2>')
        self.assertEqual(audit(self.root), [])

    def test_external_urls_not_requested(self):
        self.page('index.html', '<a href="https://example.invalid/absent">External</a>'
                  '<a href="mailto:hello@example.invalid">Email</a>'
                  '<a href="//example.invalid/remote">Protocol relative</a>')
        self.assertEqual(audit(self.root), [])

    def test_parent_directory_escape_rejected(self):
        self.page('index.html', '<a href="../secret.txt">Outside</a>')
        self.assertTrue(any('escapes site root' in error for error in audit(self.root)))

    def test_percent_encoded_escape_rejected(self):
        self.page('index.html', '<a href="%2e%2e/secret.txt">Outside</a>')
        self.assertTrue(any('escapes site root' in error for error in audit(self.root)))

    def test_directory_index(self):
        self.page('index.html', '<a href="guide/">Guide</a>')
        self.page('guide/index.html', '<h1>Guide</h1>')
        self.assertEqual(audit(self.root), [])


if __name__ == '__main__':
    unittest.main()

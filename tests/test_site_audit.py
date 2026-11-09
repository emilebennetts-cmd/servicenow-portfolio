#!/usr/bin/env python3
"""Regression tests for the static portfolio auditor (no network or dependencies)."""
import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

MODULE = Path(__file__).with_name("audit_public_site.py")
spec = importlib.util.spec_from_file_location("portfolio_audit", MODULE)
audit_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit_module)

BASE = '<!doctype html><html><head><title>Case study</title><meta name="viewport" content="width=device-width"></head><body><main>{}</main></body></html>'


class PortfolioAuditTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.root_patch = patch.object(audit_module, "ROOT", self.root)
        self.root_patch.start()
        self.addCleanup(self.root_patch.stop)

    def page(self, path, body=""):
        dest = self.root / path
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(BASE.format(body), encoding="utf-8")

    def codes(self):
        return {finding["code"] for finding in audit_module.audit()["findings"]}

    def test_valid_cross_page_anchor(self):
        self.page("index.html", '<a href="cases/delivery.html#architecture">Architecture</a>')
        self.page("cases/delivery.html", '<section id="architecture"></section>')
        self.assertEqual(audit_module.audit()["finding_count"], 0)

    def test_missing_cross_page_anchor(self):
        self.page("index.html", '<a href="cases/delivery.html#absent">Architecture</a>')
        self.page("cases/delivery.html", '<section id="architecture"></section>')
        self.assertIn("missing-fragment", self.codes())

    def test_missing_relative_file(self):
        self.page("index.html", '<a href="missing.html">Missing</a>')
        self.assertIn("missing-local-target", self.codes())

    def test_duplicate_id_and_missing_alt(self):
        self.page("index.html", '<div id="same"></div><div id="same"></div><img src="example.png">')
        self.assertTrue({"duplicate-id", "missing-image-alt"}.issubset(self.codes()))

    def test_private_repository_reference_is_reported(self):
        self.page("index.html", '<p>servicenow-portfolio-control</p>')
        self.assertIn("private-reference", self.codes())

    def test_path_escape_is_reported(self):
        self.page("nested/index.html", '<a href="../../secret.html">Escape</a>')
        self.assertIn("path-escape", self.codes())

    def test_missing_main_landmark(self):
        (self.root / "index.html").write_text(BASE.replace("<main>", "<div>").replace("</main>", "</div>"))
        self.assertIn("main-landmark", self.codes())


if __name__ == "__main__":
    unittest.main()

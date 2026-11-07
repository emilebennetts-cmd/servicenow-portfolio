"""Regression tests for the portfolio local-link audit."""
import tempfile
import unittest
from pathlib import Path
from check_local_links import audit

class LinkAuditTests(unittest.TestCase):
    def test_valid_local_file_and_fragment(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "index.html").write_text('<a href="case.html#proof">Evidence</a>')
            (root / "case.html").write_text('<section id="proof"></section>')
            self.assertEqual(audit(root), [])
    def test_missing_target(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "index.html").write_text('<a href="missing.html">Missing</a>')
            self.assertTrue(any("missing local target" in e for e in audit(root)))
    def test_missing_fragment(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "index.html").write_text('<a href="#absent">Missing</a>')
            self.assertTrue(any("missing fragment" in e for e in audit(root)))
    def test_external_link_is_not_fetched(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "index.html").write_text('<a href="https://example.org/x#y">External</a>')
            self.assertEqual(audit(root), [])

if __name__ == "__main__":
    unittest.main()

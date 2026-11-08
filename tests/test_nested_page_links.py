"""Regression coverage for nested-page link auditing (source-only QA)."""
import importlib.util
from pathlib import Path
import tempfile
import unittest

MODULE = Path(__file__).resolve().parents[1] / "scripts" / "check_local_links.py"
spec = importlib.util.spec_from_file_location("portfolio_links", MODULE)
links = importlib.util.module_from_spec(spec)
spec.loader.exec_module(links)


class NestedPageLinkTests(unittest.TestCase):
    def test_nested_page_missing_target_is_detected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "index.html").write_text('<a href="docs/guide.html">Guide</a>')
            (root / "docs").mkdir()
            (root / "docs" / "guide.html").write_text('<a href="missing.html">Missing</a>')
            problems = links.audit(root)
            self.assertTrue(any("docs/guide.html" in item and "missing local target" in item for item in problems), problems)

    def test_nested_page_valid_relative_and_root_links(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "index.html").write_text('<h1 id="home">Home</h1>')
            (root / "docs").mkdir()
            (root / "docs" / "guide.html").write_text('<a href="../index.html#home">Home</a><a href="/index.html#home">Root</a>')
            self.assertEqual([], links.audit(root))


if __name__ == "__main__":
    unittest.main()

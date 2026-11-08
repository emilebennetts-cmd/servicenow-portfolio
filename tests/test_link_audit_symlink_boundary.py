"""Security regression checks for the static publication link auditor."""
import importlib.util
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check_local_links.py"
spec = importlib.util.spec_from_file_location("portfolio_link_audit", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class PublicationBoundaryTests(unittest.TestCase):
    def test_nested_missing_target_reports_relative_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            nested = root / "case-studies"
            nested.mkdir()
            (nested / "index.html").write_text('<a href="missing.html">Missing</a>', encoding="utf-8")
            errors = module.audit(root)
            self.assertEqual(len(errors), 1)
            self.assertIn("case-studies/index.html", errors[0])

    def test_external_html_symlink_is_not_read(self):
        with tempfile.TemporaryDirectory() as site, tempfile.TemporaryDirectory() as external:
            root = Path(site)
            outside = Path(external) / "private.html"
            outside.write_text('<a href="secret.html">Private</a>', encoding="utf-8")
            try:
                (root / "external.html").symlink_to(outside)
            except (OSError, NotImplementedError):
                self.skipTest("Symlinks unavailable on this platform")
            self.assertEqual(module.audit(root), [])


if __name__ == "__main__":
    unittest.main()

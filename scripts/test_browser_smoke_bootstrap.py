#!/usr/bin/env python3
"""Keep public portfolio browser CI deterministic and free of apt mirror access.

Regression for GitHub Actions 43048806716: Playwright's --with-deps
attempted to download optional fonts from the Ubuntu package mirrors and
failed before any of the actual responsive checks could run.
"""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "portfolio-responsive-smoke.yml"
BROWSER_TEST = ROOT / "scripts" / "browser_navigation_smoke.py"


class BrowserSmokeBootstrapContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.workflow = WORKFLOW.read_text(encoding="utf-8")
        cls.browser_test = BROWSER_TEST.read_text(encoding="utf-8")

    def test_pinned_browser_and_apt_free_install(self):
        self.assertRegex(self.workflow, r"pip install playwright==[0-9]+\.[0-9]+\.[0-9]+")
        run_lines = re.findall(r"^\s*run:\s*(.+)$", self.workflow, flags=re.MULTILINE)
        self.assertIn("python -m playwright install chromium --only-shell", run_lines)
        self.assertFalse(any("install --with-deps" in line for line in run_lines))
        self.assertFalse(any("apt-get" in line or "sudo apt" in line for line in run_lines))

    def test_actual_test_not_replaced_with_placeholder(self):
        self.assertIn("python scripts/browser_navigation_smoke.py", self.workflow)
        for token in ("390, 768, 1024, 1440", "check_cmdb_trust_lab",
                      "check_case_study", "check_viewport", "sync_playwright"):
            with self.subTest(token=token):
                self.assertIn(token, self.browser_test)

    def test_browser_test_does_not_capture_or_publish_images(self):
        for code in (".screenshot(", ".video(", "record_video_dir=",
                     "tracing.start(", "browser_type.connect("):
            with self.subTest(code=code):
                self.assertNotIn(code, self.browser_test)


if __name__ == "__main__":
    unittest.main()

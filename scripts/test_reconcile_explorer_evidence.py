"""Contract and regression tests for the public evidence-aware Portfolio Explorer."""
import importlib.util
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = Path(__file__).with_name("reconcile_explorer_evidence.py")
spec = importlib.util.spec_from_file_location("reconcile_explorer_evidence", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class ExplorerEvidenceTests(unittest.TestCase):
    def test_generator_matches_live_catalogue(self):
        source = (ROOT / "portfolio-explorer.html").read_text(encoding="utf-8")
        register = json.loads((ROOT / "evidence/public-verification-register.json").read_text(encoding="utf-8"))
        self.assertEqual(source, module.annotate(source, register))
        self.assertEqual(source.count('class="proof"'), len(module.ROW.findall(source)))
        self.assertIn('id="evidence-status"', source)
        self.assertIn('evidence.addEventListener("change"', source)
        self.assertIn('evidence.value="All"', source)
        self.assertIn('row.dataset.evidence===proof', source)
        self.assertIn("NOT REGISTERED", source)
        self.assertIn('<option value="proposed">PROPOSED</option>', source)
        self.assertIn('id="registered-pages"', source)
        self.assertIn('results.filter(row=>row.dataset.evidence!=="unregistered").length', source)
        self.assertNotIn("fetch(", source)

    def test_every_indexed_page_has_a_reviewed_claim(self):
        source = (ROOT / "portfolio-explorer.html").read_text(encoding="utf-8")
        register = json.loads((ROOT / "evidence/public-verification-register.json").read_text(encoding="utf-8"))
        self.assertEqual(module.unregistered_pages(source, register), [])
        self.assertNotIn('data-evidence="unregistered"', source)

    def test_new_unregistered_page_is_detected_before_publication(self):
        source = '<li class="result"><a href="new-page.html">New</a><span class="locator">new-page.html</span></li>'
        register = {"items": []}
        self.assertEqual(module.unregistered_pages(source, register), ["new-page.html"])
        preview = module.annotate(source, register)
        self.assertIn('data-evidence="unregistered"', preview)

    def test_mixed_pages_remain_mixed_not_promoted(self):
        source = (ROOT / "portfolio-explorer.html").read_text(encoding="utf-8")
        for page in ("index.html", "workbench-experience.html", "workbench-architecture.html"):
            with self.subTest(page=page):
                self.assertRegex(source, r'href="' + page + r'".*?<span class="proof">MIXED CLAIMS</span>')

    def test_unregistered_claim_cannot_be_promoted(self):
        source = '<li class="result" data-category="Start here" data-search="none"><span class="type">Start here</span><a href="unknown.html">A</a><span class="locator">unknown.html</span></li>'
        rendered = module.annotate(source, {"items": []})
        self.assertIn('data-evidence="unregistered"', rendered)
        self.assertIn("NOT REGISTERED", rendered)
        self.assertEqual(rendered, module.annotate(rendered, {"items": []}))

    def test_reference_design_classification_remains_proposed(self):
        page = '<li class="result"><a href="design.html">Design</a><span class="locator">design.html</span></li>'
        data = {"items": [{"page": "design.html", "classification": "proposed"}]}
        output = module.annotate(page, data)
        self.assertIn('data-evidence="proposed"', output)
        self.assertIn("PROPOSED", output)
        self.assertNotIn('data-evidence="dev-verified"', output)
        self.assertEqual(output, module.annotate(output, data))

    def test_mixed_claims_are_not_auto_promoted_to_verified(self):
        page = '<li class="result" data-category="Assurance"><a href="test.html">Test</a><span class="locator">test.html</span></li>'
        register = {"items": [{"page": "test.html", "classification": "DEV-verified"},
                              {"page": "test.html", "classification": "mock-only"}]}
        result = module.annotate(page, register)
        self.assertIn('data-evidence="mixed"', result)
        self.assertIn("MIXED CLAIMS", result)
        self.assertNotIn('data-evidence="dev-verified"', result)

    def test_claim_change_invalidates_stale_badge(self):
        page = '<li class="result"><a href="test.html">Test</a><span class="locator">test.html</span></li>'
        old = module.annotate(page, {"items": [{"page": "test.html", "classification": "source-only"}]})
        new = module.annotate(old, {"items": [{"page": "test.html", "classification": "mock-only"}]})
        self.assertIn('data-evidence="mock-only"', new)
        self.assertNotIn('data-evidence="source-only"', new)
        self.assertEqual(new, module.annotate(new, {"items": [{"page": "test.html", "classification": "mock-only"}]}))

    def test_rejects_unsafe_or_unknown_claims(self):
        for kind, page in [("production", "test.html"), ("source-only", "../private.html"),
                           ("mock-only", "https://example.test")]:
            with self.subTest(kind=kind, page=page):
                with self.assertRaises(ValueError):
                    module.claim_map({"items": [{"page": page, "classification": kind}]})


if __name__ == "__main__":
    unittest.main()

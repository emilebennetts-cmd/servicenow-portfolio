"""CI-discovered safety contract for the public visual-evidence intake.

Run by Portfolio quality gate: python -m unittest discover -s scripts.
The eight inspected files are private; this HTML must contain summary metadata only.
"""
from html.parser import HTMLParser
from pathlib import Path
import re
import unittest


GALLERY = Path(__file__).resolve().parents[1] / "visual-evidence.html"


class Tags(HTMLParser):
    def __init__(self):
        super().__init__()
        self.images = []
        self.anchors = []
        self.candidates = []
        self.reviewed = []
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get("id"):
            self.ids.add(a["id"])
        if tag == "img":
            self.images.append(a)
        if tag == "a":
            self.anchors.append(a.get("href", ""))
        if tag == "article" and a.get("data-evidence-id"):
            self.candidates.append(a["data-evidence-id"])
        if tag == "article" and a.get("data-review-id"):
            self.reviewed.append((a["data-review-id"], a.get("data-source-class", "")))


class VisualIntakeSafetyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = GALLERY.read_text(encoding="utf-8")
        cls.tags = Tags()
        cls.tags.feed(cls.html)

    def test_intake_summary_is_explicitly_not_a_gallery_approval(self):
        self.assertIn("triage-title", self.tags.ids)
        self.assertIn("independent intake sample", self.html)
        self.assertIn("0</strong><span>Images approved", self.html)
        self.assertIn("All eight files remain on HOLD", self.html)

    def test_source_document_and_synthetic_example_not_runtime_proof(self):
        self.assertIn("Overview document page, not a product screenshot", self.html)
        self.assertIn("MOCK-ONLY content", self.html)
        self.assertIn("installed release and execution unverified", self.html)

    def test_no_original_images_or_private_drive_links(self):
        self.assertEqual([], self.tags.images)
        self.assertFalse(any("drive.google.com" in a or "docs.google.com" in a
                             for a in self.tags.anchors))
        self.assertNotIn("servicenow-portfolio-control", self.html)

    def test_reviewed_source_sample_is_separate_and_classified(self):
        self.assertIn("reviewed-captures", self.tags.ids)
        self.assertEqual(
            [("RV-01", "source-only"), ("RV-02", "source-only"),
             ("RV-03", "mock-only"), ("RV-04", "source-document"),
             ("RV-05", "mock-only"), ("RV-06", "mock-only"),
             ("RV-07", "source-only"), ("RV-08", "source-document")],
            self.tags.reviewed,
        )
        self.assertEqual(8, len(set(x[0] for x in self.tags.reviewed)))
        self.assertIn("not a screenshot", self.html)
        self.assertIn("update-set metadata", self.html.lower())
        self.assertIn("requirements, not embedded runtime evidence", self.html)
        self.assertIn("MIM readiness example is explicitly labelled demo/synthetic", self.html)
        self.assertIn("live Jira/Notion synchronisation", self.html)
        self.assertIn("two sets can overlap", self.html)
        self.assertIn("None of these eight reviews is DEV-VERIFIED", self.html)
        self.assertIn("not a published screenshot gallery", self.html)
        self.assertEqual(8, self.html.count('class="hold">HOLD'))


    def test_inspected_review_controls_are_independent_and_safe(self):
        self.assertEqual(8, self.html.count('data-review-group='))
        for review_id in ("RV-01", "RV-02", "RV-03", "RV-04", "RV-05", "RV-06", "RV-07", "RV-08"):
            self.assertIn('id="review-' + review_id.lower() + '"', self.html)
        for identifier in ("review-search", "review-count", "review-empty", "clear-reviews",
                           "export-reviewed", "print-reviewed"):
            self.assertIn('id="' + identifier + '"', self.html)
        for group in ("all", "delivery", "diagnostic", "document"):
            self.assertIn('data-review-filter="' + group + '"', self.html)
        self.assertIn("'reviewGroup'", self.html)
        self.assertIn("'reviewq'", self.html)
        self.assertIn("workbench-inspected-review-register.csv", self.html)
        self.assertIn("'publication_decision'", self.html)
        self.assertIn("no original images, internal URLs, private file identifiers or source hashes", self.html)
        # The original ten-candidate controls must remain independently operable.
        self.assertIn('id="candidate-search"', self.html)
        self.assertIn('id="export-candidates"', self.html)

    def test_public_review_links_do_not_point_at_private_source(self):
        restricted = (
            "/emilebennetts-cmd/Diagnostic-Workbench2",
            "/emilebennetts-cmd/solution-lifecycle-studio",
            "/emilebennetts-cmd/servicenow-portfolio-control",
        )
        self.assertFalse(
            [(anchor, path) for anchor in self.tags.anchors for path in restricted
             if path in anchor],
            "Reviewer links must lead to public case studies, not restricted repositories",
        )
        for href in (
            "delivery-case-study.html",
            "diagnostic-workbench-case-study.html",
            "reusable-delivery-patterns-case-study.html",
            "workbench-architecture-gallery.html",
        ):
            self.assertIn(href, self.tags.anchors)
            self.assertTrue((GALLERY.parent / href).is_file())

    def test_existing_candidate_register_remains_intact(self):
        self.assertEqual(10, len(self.tags.candidates))
        self.assertEqual(10, len(set(self.tags.candidates)))
        self.assertTrue(all(re.fullmatch(r"(DW|VD)-IMG-\d{2}", i)
                            for i in self.tags.candidates))


if __name__ == "__main__":
    unittest.main()

"""Keep the screenshot-review UI wired to the fail-closed, byte-bound receipt model."""
from html.parser import HTMLParser
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

class Elements(HTMLParser):
    def __init__(self):
        super().__init__()
        self.inputs = {}
        self.scripts = []
    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        if tag == "input" and data.get("id"):
            self.inputs[data["id"]] = data
        if tag == "script" and data.get("src"):
            self.scripts.append(data["src"])

class ScreenshotReviewReceiptIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.page = (ROOT / "screenshot-publication-gate.html").read_text(encoding="utf-8")
        cls.model = (ROOT / "screenshot-review-safety.js").read_text(encoding="utf-8")
        cls.dom = Elements()
        cls.dom.feed(cls.page)

    def test_final_image_digest_is_required_for_review(self):
        self.assertIn("digest", self.dom.inputs)
        self.assertEqual(self.dom.inputs["digest"]["maxlength"], "64")
        self.assertIn("redacted_file_sha256", self.page)
        self.assertIn("screenshot-receipt-verifier.html", self.page)
        self.assertIn("validDigest(digest)", self.model)

    def test_actual_client_model_is_loaded_before_ui(self):
        self.assertIn("screenshot-review-safety.js", self.dom.scripts)
        self.assertIn("model.evaluate(", self.page)
        self.assertIn("q('#export').disabled = !result.export_safe", self.page)
        self.assertIn("'sensitive_notes'", self.model)
        self.assertNotIn("portfolio-screenshot-review-v1", self.page)

    def test_public_review_state_does_not_conflate_evidence_samples(self):
        self.assertIn("Ten historical candidate slots", self.page)
        self.assertIn("eight source-held images were visually inspected", self.page)
        self.assertIn("groups may overlap", self.page)
        self.assertIn("Public image approvals: zero.", self.page)
        self.assertIn("Inspection is not runtime certification", self.page)

    def test_no_private_image_pointers_or_exposed_originals(self):
        for marker in ("drive.google.com/file/d/", "servicenow-portfolio-control",
                       "DEV-MIM-delivery-home", "<img ", "<iframe "):
            self.assertNotIn(marker, self.page)
        self.assertIn("review_complete_not_auto_authorised", self.model)
        self.assertNotIn("publication_gate: 'approved'", self.model)

if __name__ == "__main__":
    unittest.main()

"""Prevent source image triage metadata becoming an unapproved public gallery."""
from html.parser import HTMLParser
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class IMG(HTMLParser):
    def __init__(self):
        super().__init__()
        self.images = []
    def handle_starttag(self, tag, attrs):
        if tag in ("img", "picture", "source"):
            self.images.append((tag, dict(attrs)))


class PrivateImageTriageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.page = (ROOT / "visual-evidence.html").read_text(encoding="utf-8")
        cls.library = (ROOT / "evidence.html").read_text(encoding="utf-8")
        cls.release = (ROOT / "releases" / "2026-11-19-private-image-triage.md").read_text(encoding="utf-8")

    def test_private_source_review_is_explicit_and_locatable(self):
        self.assertIn('id="nov19-review"', self.page)
        self.assertIn('aria-labelledby="nov19-review-title"', self.page)
        self.assertIn("Some candidates may overlap previous review samples", self.page)
        for marker in ("historical DEV-labelled", "MOCK-ONLY", "document pages",
                       "Security-configuration", "publication approvals"):
            self.assertIn(marker.lower(), self.page.lower())

    def test_no_image_embeds_or_private_identifiers(self):
        parser = IMG(); parser.feed(self.page)
        self.assertEqual(parser.images, [])
        for source in (self.page, self.library, self.release):
            for marker in ("drive.google.com/file/d/", "servicenow-portfolio-control",
                           "DEV-MIM-delivery-home-4.17.2-2026-10-05.jpg",
                           "IMG-03", "IMG-04", "IMG-05"):
                self.assertNotIn(marker, source)
        self.assertIn("No original images or redacted derivatives have been approved or published.", self.library)

    def test_evidence_counts_are_not_conflated_with_prior_sample(self):
        self.assertIn("eight inspected review records from 11–13 November", self.library)
        self.assertIn("eight further source-held candidates", self.library)
        self.assertIn("some may overlap earlier records", self.library)
        self.assertIn("0 approved public images", self.release.lower())

    def test_hold_and_no_native_certification(self):
        self.assertIn("Newly DEV-VERIFIED: **0**", self.release)
        self.assertIn("PRODUCTION-VERIFIED: **0**", self.release)
        self.assertIn("HOLD", self.page)


if __name__ == "__main__":
    unittest.main()

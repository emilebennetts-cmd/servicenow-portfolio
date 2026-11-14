"""Contract for safe, shareable public ServiceNow portfolio pages.

Text-only social previews are intentional: no private/original screenshot can enter
an Open Graph or Twitter preview before image-specific publication approval.
"""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
import unittest

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = "https://emilebennetts-cmd.github.io"
BASE = ORIGIN + "/servicenow-portfolio/"
PAGES = (
    "index.html",
    "delivery-case-study.html",
    "diagnostic-workbench-case-study.html",
    "reusable-delivery-patterns-case-study.html",
    "workbench-architecture-gallery.html",
    "technical-evidence-register.html",
)

class SocialHead(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.meta = {}
        self.canonicals = []
        self.in_title = False
        self.title = ""

    def handle_starttag(self, tag, attrs):
        props = dict(attrs)
        if tag == "title":
            self.in_title = True
        if tag == "link" and (props.get("rel") or "").lower() == "canonical":
            self.canonicals.append(props.get("href", ""))
        if tag == "meta":
            key = props.get("property") or props.get("name")
            if key:
                self.meta.setdefault(key.lower(), []).append(props.get("content", ""))

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title += data

def failures_for_html(html, expected_url):
    doc = SocialHead()
    doc.feed(html)
    errors = []
    if len(doc.canonicals) != 1 or doc.canonicals[0] != expected_url:
        errors.append("canonical must appear once and match the expected public URL")
    mandatory = (
        "description", "og:type", "og:site_name", "og:title",
        "og:description", "og:url", "twitter:card",
        "twitter:title", "twitter:description",
    )
    for key in mandatory:
        vals = doc.meta.get(key, [])
        if len(vals) != 1 or not vals[0].strip():
            errors.append(f"{key} must occur once and be nonempty")
    for key in ("og:title", "og:description", "twitter:title", "twitter:description"):
        val = (doc.meta.get(key) or [""])[0]
        if len(val) > (200 if "description" in key else 120):
            errors.append(f"{key} too long")
    if doc.meta.get("og:url") != [expected_url]:
        errors.append("og:url must match canonical")
    if doc.meta.get("og:type") != ["website"]:
        errors.append("og:type must be website")
    if doc.meta.get("twitter:card") != ["summary"]:
        errors.append("text-only Twitter summary card required")
    if any(k in doc.meta for k in ("og:image", "twitter:image", "og:image:url", "og:video")):
        errors.append("unreviewed media in social preview forbidden")
    for item in doc.canonicals:
        parts = urlsplit(item)
        if parts.scheme != "https" or parts.netloc != urlsplit(ORIGIN).netloc or parts.query or parts.fragment:
            errors.append("canonical must be an unparameterised HTTPS URL on the portfolio host")
    if not doc.title.strip():
        errors.append("browser title missing")
    return errors

class ShareMetadataTests(unittest.TestCase):
    def test_six_recruiter_entrances_are_shareable(self):
        for name in PAGES:
            with self.subTest(page=name):
                url = BASE + ("" if name == "index.html" else name)
                html = (ROOT / name).read_text(encoding="utf-8")
                self.assertEqual([], failures_for_html(html, url))

    def test_duplicate_metadata_fails(self):
        html = '<title>Example</title><link rel="canonical" href="' + BASE + '">' + (
            '<meta property="og:title" content="first"><meta property="og:title" content="second">'
        )
        errors = failures_for_html(html, BASE)
        self.assertTrue(any("og:title" in e for e in errors), errors)

    def test_private_media_previews_fail(self):
        html = '<title>Example</title><meta property="og:image" content="secret.png">'
        self.assertTrue(any("unreviewed media" in e for e in failures_for_html(html, BASE)))

    def test_noncanonical_external_and_query_urls_fail(self):
        html = '<title>Example</title><link rel="canonical" href="https://example.org/review?token=abc">'
        self.assertTrue(any("canonical" in e for e in failures_for_html(html, BASE)))

if __name__ == "__main__":
    unittest.main()

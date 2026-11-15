"""Security regressions for the public screenshot publication gate."""
import hashlib
import tempfile
import unittest
from pathlib import Path
from scripts.check_publication import check


class ScreenshotGateSecurityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "site"
        (self.root / "evidence").mkdir(parents=True)
        (self.root / "assets" / "screenshots").mkdir(parents=True)
        self.manifest = self.root / "evidence" / "approved-public-images.txt"

    def test_approved_matching_bytes(self):
        image = self.root / "assets" / "screenshots" / "approved.png"
        image.write_bytes(b"\x89PNG\r\n\x1a\nsynthetic-no-metadata")
        digest = hashlib.sha256(image.read_bytes()).hexdigest()
        self.manifest.write_text(f"assets/screenshots/approved.png {digest}\n")
        self.assertEqual(check(self.root, self.manifest), [])

    def test_rejects_unreviewed_active_embed(self):
        page = self.root / "embedded.html"
        page.write_text('<iframe src="https://example.invalid/secret-capture"></iframe>')
        self.assertTrue(any("active HTML embed" in x for x in check(self.root, self.manifest)))

    def test_rejects_inline_svg_filter_image(self):
        page = self.root / "case.html"
        page.write_text('<svg><filter><feImage href="local.png"/></filter></svg>')
        self.assertTrue(any("SVG filter image element" in x for x in check(self.root, self.manifest)))

    def test_rejects_remote_video_poster(self):
        page = self.root / "case.html"
        page.write_text('<video poster="https://example.invalid/capture.png"></video>')
        self.assertTrue(any("remote video poster" in x for x in check(self.root, self.manifest)))

    def test_rejects_remote_css_content_image(self):
        sheet = self.root / "style.css"
        sheet.write_text('.leak::before { content: url(https://example.invalid/capture.png); }')
        self.assertTrue(any("remote CSS image property" in x for x in check(self.root, self.manifest)))

    def test_plain_text_use_of_iframe_does_not_trigger_in_markdown(self):
        page = self.root / "notes.md"
        page.write_text('Example markup: <iframe src="https://example.invalid/">')
        self.assertFalse(any("active HTML embed" in x for x in check(self.root, self.manifest)))

    def test_rejects_traversal_manifest(self):
        self.manifest.write_text("assets/screenshots/../../secret.png " + "a" * 64 + "\n")
        self.assertTrue(any("unsafe image path" in x for x in check(self.root, self.manifest)))

    def test_rejects_absolute_manifest(self):
        self.manifest.write_text("/tmp/secret.png " + "a" * 64 + "\n")
        self.assertTrue(any("unsafe image path" in x for x in check(self.root, self.manifest)))

    def test_rejects_external_symlink(self):
        outside = Path(self.temp.name) / "private.png"
        outside.write_bytes(b"private bytes")
        link = self.root / "assets" / "screenshots" / "linked.png"
        link.symlink_to(outside)
        self.assertTrue(any("symlink escapes" in x for x in check(self.root, self.manifest)))

    def test_rejects_modified_approved_image(self):
        image = self.root / "assets" / "screenshots" / "approved.png"
        image.write_bytes(b"changed")
        self.manifest.write_text("assets/screenshots/approved.png " + "0" * 64 + "\n")
        self.assertTrue(any("image bytes changed" in x for x in check(self.root, self.manifest)))


    def test_blocks_remote_social_preview_even_without_image_element(self):
        page = self.root / "share.html"
        page.write_text('<meta content="https://other.invalid/private.png" property="og:image">')
        self.assertTrue(any("social preview image origin" in x for x in check(self.root, self.manifest)))

    def test_blocks_unapproved_twitter_and_schema_image(self):
        page = self.root / "share.html"
        page.write_text('<meta name="twitter:image" content="assets/screenshots/unknown.png">'
                        '<meta content="data:image/png;base64,AA==" itemprop="image">')
        issues = check(self.root, self.manifest)
        self.assertTrue(any("lacks byte-bound publication approval" in x for x in issues))
        self.assertTrue(any("social preview image origin" in x for x in issues))

    def test_approved_bytes_allow_same_origin_social_preview(self):
        image = self.root / "assets" / "screenshots" / "approved.png"
        image.write_bytes(b"\x89PNG\r\n\x1a\nsynthetic-no-metadata")
        digest = hashlib.sha256(image.read_bytes()).hexdigest()
        self.manifest.write_text(f"assets/screenshots/approved.png {digest}\n")
        page = self.root / "share.html"
        page.write_text(
            '<meta property="og:image" '
            'content="https://emilebennetts-cmd.github.io/servicenow-portfolio/assets/screenshots/approved.png">'
            '<meta name="twitter:image" content="assets/screenshots/approved.png">')
        self.assertEqual(check(self.root, self.manifest), [])

    def test_blocks_legacy_image_src_link_without_approval(self):
        page = self.root / "share.html"
        page.write_text('<link href="https://example.invalid/capture.png" rel="image_src">')
        self.assertTrue(any("social preview image origin" in x for x in check(self.root, self.manifest)))

    def test_blocks_alternate_port_and_query_on_approved_preview(self):
        image = self.root / "assets" / "screenshots" / "approved.png"
        image.write_bytes(b"\x89PNG\r\n\x1a\nsynthetic-no-metadata")
        self.manifest.write_text(
            "assets/screenshots/approved.png "
            + hashlib.sha256(image.read_bytes()).hexdigest() + "\n")
        page = self.root / "share.html"
        page.write_text(
            '<meta property="og:image" '
            'content="https://emilebennetts-cmd.github.io:8443/servicenow-portfolio/assets/screenshots/approved.png">'
            '<meta property="og:image:url" content="assets/screenshots/approved.png?token=test">')
        issues = check(self.root, self.manifest)
        self.assertTrue(any("social preview image origin" in x for x in issues))
        self.assertTrue(any("lacks byte-bound publication approval" in x for x in issues))


    def test_rejects_duplicate_social_metadata_attributes(self):
        page = self.root / "share.html"
        page.write_text('<meta property="og:image" property="og:title" '
                        'content="assets/screenshots/unreviewed.png">')
        self.assertTrue(any("ambiguous social preview" in x
                            for x in check(self.root, self.manifest)))

    def test_reports_malformed_social_preview_url(self):
        page = self.root / "share.html"
        page.write_text('<meta property="og:image" content="https://[bad-host/img.png">'
                        '<meta name="twitter:image" content="https://example.org:invalid/a.png">')
        issues = check(self.root, self.manifest)
        self.assertEqual(sum("malformed social preview" in x for x in issues), 2)


    def test_rejects_second_remote_srcset_candidate(self):
        page = self.root / "responsive.html"
        page.write_text('<picture><source srcset="assets/screenshots/ok.png 1x, https://other.invalid/private.png 2x"></picture>')
        self.assertTrue(any("unapproved responsive image origin" in x for x in check(self.root, self.manifest)))

    def test_rejects_unapproved_relative_img_src(self):
        (self.root / "case.html").write_text('<img src="assets/screenshots/private.png" alt="Example">')
        self.assertTrue(any("responsive image lacks byte-bound publication approval" in x for x in check(self.root, self.manifest)))

    def test_rejects_remote_image_preload_and_imagesrcset(self):
        (self.root / "case.html").write_text(
            '<link rel="preload" as="image" href="assets/screenshots/unknown.png" '
            'imagesrcset="assets/screenshots/unknown.png 1x, https://other.invalid/hidden.png 2x">')
        issues = check(self.root, self.manifest)
        self.assertTrue(any("lacks byte-bound publication approval" in x for x in issues))
        self.assertTrue(any("unapproved responsive image origin" in x for x in issues))

    def test_rejects_query_params_and_alternate_ports(self):
        (self.root / "case.html").write_text(
            '<img src="assets/screenshots/ok.png?token=accidental">'
            '<img src="https://emilebennetts-cmd.github.io:8443/servicenow-portfolio/assets/screenshots/ok.png">')
        issues = check(self.root, self.manifest)
        self.assertTrue(any("lacks byte-bound publication approval" in x for x in issues))
        self.assertTrue(any("unapproved responsive image origin" in x for x in issues))

    def test_rejects_duplicate_src_and_bad_srcset_descriptor(self):
        (self.root / "case.html").write_text(
            '<img src="a.png" src="b.png"><img srcset="assets/screenshots/ok.png 999q">')
        issues = check(self.root, self.manifest)
        self.assertTrue(any("ambiguous responsive image attribute" in x for x in issues))
        self.assertTrue(any("malformed responsive srcset candidate" in x for x in issues))

    def test_rejects_image_input_and_local_video_poster(self):
        (self.root / "case.html").write_text(
            '<input type="image" src="assets/screenshots/private.png">'
            '<video poster="assets/screenshots/private.png"></video>')
        issues = check(self.root, self.manifest)
        self.assertGreaterEqual(sum("responsive image lacks byte-bound" in x for x in issues), 2)

    def test_approved_srcset_and_preload_are_accepted(self):
        image = self.root / "assets" / "screenshots" / "approved.png"
        image.write_bytes(bytes([137, 80, 78, 71, 13, 10, 26, 10]) + b"synthetic-no-metadata")
        digest = hashlib.sha256(image.read_bytes()).hexdigest()
        self.manifest.write_text(f"assets/screenshots/approved.png {digest}\n")
        (self.root / "case.html").write_text(
            '<picture><source srcset="assets/screenshots/approved.png 1x, '
            'https://emilebennetts-cmd.github.io/servicenow-portfolio/assets/screenshots/approved.png 2x">'
            '<img src="assets/screenshots/approved.png"></picture>'
            '<link rel="preload" as="image" href="assets/screenshots/approved.png">')
        self.assertEqual(check(self.root, self.manifest), [])

    def test_rejects_data_url_in_srcset(self):
        (self.root / "case.html").write_text('<img srcset="data:image/png;base64,AA== 1x">')
        self.assertTrue(any("responsive image" in x for x in check(self.root, self.manifest)))


if __name__ == "__main__":
    unittest.main()

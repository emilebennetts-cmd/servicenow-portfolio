# Fail-closed embedded-media publication controls and enforceable regression suite

**Release:** 13 November 2026 · **Classification:** SOURCE-ONLY website and security engineering; synthetic tests are MOCK-ONLY. **Publication:** HOLD.

## 1. The client's pain and history

The existing image publication check required per-file SHA-256 approval and screened several image-embedding forms. A second audit found two operational gaps: unreviewed pixels could also be displayed through active HTML embed frames, SVG filter images, remote video poster artwork and less obvious CSS image properties; additionally, the GitHub quality workflow did not execute the broader `tests/` security suite. Its nominal approved-PNG fixture had invalid PNG bytes, masking whether that additional suite could run successfully.

## 2. The solution

- Extended `scripts/check_publication.py` to flag HTML `iframe`, `object` and `embed` elements; SVG `feImage`; remote `video[poster]`; and remote CSS `content`, `list-style-image`, `border-image-source` and `cursor` images. Existing data URL, direct image, CSS background/mask and external SVG checks remain in force.
- Corrected the synthetic approved-PNG fixture to carry the expected PNG signature and no metadata markers. Five additional negative/positive regression checks cover active embeds, filter images, remote video posters, CSS content images and Markdown textual examples.
- Enabled `python -m unittest discover -s tests -p 'test_*.py' -v` in the GitHub quality gate, in addition to the `scripts/` tests, provenance checks, local link audit and publication scan.
- Updated the public reviewer-facing [screenshot publication gate](../screenshot-publication-gate.html) to explain the extra safeguards. No external image, original capture, client artifact or hidden code was embedded in the website.

These controls are **heuristic, fail-closed checks**, not a formal Content Security Policy audit, exhaustive sanitizer, pixel inspection, approval, or independent native ServiceNow acceptance.

## 3. Architectural best practices and verification

- **SOURCE-ONLY:** Python publication guard, regression suite, site text and this release record.
- **MOCK-ONLY:** Test fixtures use invented hosts, synthetic image headers and synthetic markup.
- **DEV-REPORTED:** Only historical, version-specific source documentation; no new DEV installation or test has been asserted.
- **DEV-VERIFIED / PRODUCTION-VERIFIED:** No new independent native execution.
- **Screenshot release:** Original Workbench screen captures remain on HOLD; **0 approved for public display**.
- **Repository safety:** No private application source, customer records, original screenshot pixels, credentials or environment identifiers were published. Repository visibility was not changed.

**Licensing:** The static GitHub Pages site and its CI controls need no ServiceNow licence. Real native Workbench installation or testing requires validated App Engine/custom-application and table rights, relevant ACLs and personas, and feature-dependent ITSM, ITOM/Discovery, IntegrationHub, analytics, AI or external provider entitlements.

**Acceptance boundary:** Run the exact final commit's GitHub Actions checks and confirm Pages deployment independently. Image-by-image publication still requires owner/privacy approval and manual inspection of the final sanitized raster.
# 11 November 2026 — Visual evidence intake and screenshot metadata regression

**Release classification:** SOURCE-ONLY website and publication-control changes. No new ServiceNow DEV or production execution, and no new screenshot publication approval.

## 1. The client's pain & history

Public implementation portfolios can conflate illustrative screens, original UI captures, document pages, and verified product behaviour. An additional review risk was discovered in the screenshot publication validator: JPEG EXIF and GIF comment checks searched for *literal escaped characters* rather than the underlying binary marker bytes. A hash-approved asset could therefore bypass those two metadata heuristics. The test cases for these markers existed in the separate `tests/` folder but were not part of the normal `scripts/test_*.py` GitHub Actions discovery command.

## 2. The ServiceNow solution / delivered implementation

- Corrected the byte-matching expressions for JPEG EXIF (`Exif\x00\x00`) and GIF comment extensions (`0x21 0xFE`) in `scripts/check_publication.py`.
- Added seven binary-marker and end-to-end approval tests in `scripts/test_metadata_binary_markers.py`, which is discovered by the existing quality workflow.
- Added a responsive, accessible status panel to `visual-evidence.html` summarising a **separate, privately inspected four-file intake sample**: two application-interface captures without independently established runtime version/execution; one explicitly synthetic demonstration screen (MOCK-ONLY content); one overview-document page (not a Workbench UI screenshot). **Zero images are cleared for publication.** The sample must not be presented as verification of the existing ten gallery placeholders.
- Added `scripts/test_visual_intake_safety.py` to ensure the summary remains explicit about HOLD and avoids images or private Drive links.
- Recorded original retrieved-byte SHA-256 receipts and source-specific triage **in the private control repository only**. The public site contains no original images, source IDs, private URLs or client-specific content.

## 3. Architectural best practices, verification and scope

| Evidence tier | Outcome |
|---|---|
| SOURCE-ONLY | Code and status-panel commits recorded; HTML summary is based on private visual intake, not on a new runtime test |
| MOCK-ONLY | Synthetic demonstration screen explicitly classified |
| DEV-REPORTED | Historical release-specific records remain separate; not re-executed |
| DEV-VERIFIED | Not established in this release |
| PRODUCTION-VERIFIED | Not established |
| Publication-approved genuine screenshots | 0 |

**Commits:** `f03daf3` binary marker correction; `71ab36b` metadata regression coverage; `7529131` public review panel; `8dc86b4` review panel contract; `9876915` corrected contract ID regular expression.

**QA boundary:** The metadata detector remains heuristic. A clean marker scan, image signature and SHA-256 approval cannot establish irreversible redaction or publication permission. A human reviewer must inspect original and derivative pixels and explicitly approve each specific caption. GitHub Actions and live deployment results must be checked against the final release commit, not inherited from earlier runs.

**Licensing:** The public static page, Python tests and GitHub Actions require no ServiceNow licence. Running or validating the underlying ServiceNow applications may require App Engine/custom application rights and appropriate roles, plus ITSM/ITOM, IntegrationHub, Performance Analytics, Now Assist/AI or provider entitlements according to the exact capabilities exercised.

**Next evidence milestone:** Obtain image-owner publication authority and a version-specific witnessed DEV test receipt for one sanitised screenshot. Do not promote source-only or mock-only material to DEV-VERIFIED based on appearance.

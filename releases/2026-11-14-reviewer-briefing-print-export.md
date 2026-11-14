# Release — Reviewer-Specific Briefing and Print Export (14 November 2026)

## Client pain & history
The 90-second ServiceNow portfolio reviewer guide already had three context-sensitive paths for hiring managers, technical architects and assurance reviewers. A selected path could not be preserved as a reviewable file or professional print/PDF without screenshots or manual copy/paste. The source-observation overview also required clearer distinction between six captured UI observations and two document pages in the eight-file evidence sample.

## Implemented ServiceNow portfolio solution
- Extended `portfolio-review-guide.html` with **Export selected path (JSON)** and **Print selected path / Save PDF**.
- Exports include the current role, reviewer narrative, curated public first-party links and reasons to inspect them. A reviewer selection cannot modify the authoritative public evidence register.
- Uses explicit output boundaries: `claim_basis=SOURCE-ONLY`, `interaction_basis=MOCK-ONLY`, `native_dev_verified=false`, `production_verified=false`, `original_screenshots_approved=0` and immutable `UNREVIEWED / NOT VERIFIED / HOLD` states.
- Local-only browser Blob and print functionality; no data upload, calls to ServiceNow, external connectors, cloud storage or personal identifiers.
- Rejects non-public/invalid reviewer links before print/export. The printable design shows the active route only, preserves the claim warnings and allows browser-generated PDF.
- Clarifies the eight private source reviews: six captured UI observations plus two source documents, none approved for public image publication.

## Architecture and assurance
- Preserve source-first narrative and ITIL 4/OOTB-first design rationale without claiming that any source version is deployed or approved.
- New `scripts/browser_review_guide_briefings.py` validates all three reviewer paths at 390, 768, 1024 and 1440 px, downloaded JSON content, print media, network isolation and invalid URL fail-closed behaviour.
- Extended `scripts/test_review_guide.py` for HTML, CSP, source-classification, immutability and exclusion of original images.
- New `.github/workflows/reviewer-briefings-browser.yml` executes structural tests and pinned Playwright/Chromium on relevant changes.
- GitHub Pages build/CI and external live URL verification must be independently checked; repository commits alone are **SOURCE-ONLY**, not proof that the workflow has passed.
- Original screenshots, including any document excerpts, stay **HOLD** pending individual origin, redaction, legal/contractual permission and explicit reviewer approval.

## Licensing & entitlements
None required for the public static HTML, local JSON export or the browser's own print/PDF functionality. Native implementation of the Workbenches still requires contracted App Engine/custom table allocations, appropriate roles and ACLs and feature-specific ITSM/ITOM/Discovery/IntegrationHub/AI/analytics/ATF/third-party rights. No licensing compliance is certified by this page.

## Outstanding native verification
Independent current-version DEV read-back and role-negative tests; Production release/acceptance evidence; version mapping between historic runbooks, PDI application IDs and current source; genuine image publication approval.

## Related evidence
- [Reviewer guide](../portfolio-review-guide.html)
- [Eight restricted-source observations, public summaries only](../visual-evidence.html#reviewed-captures)
- [Source and runtime verification ledger](../verification-ledger.html)
- [Native acceptance playbook](../workbench-acceptance-playbook.html)

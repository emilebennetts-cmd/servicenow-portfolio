# Reviewed Workbench evidence cards and public-source navigation

**Date:** 11 November 2026  
**Scope:** Public portfolio evidence intake and publication boundary  
**Implementation tier:** SOURCE-ONLY  
**Image publication decision:** HOLD (0 new images approved)

## Problem and delivery
The prior visual evidence page reported four privately reviewed Workbench-related files only as totals. Reviewers could not distinguish the two interface captures from an explicitly synthetic demonstration and an architecture document page, and the page still linked to restricted Delivery/Diagnostic source repositories.

The public `visual-evidence.html` now contains four individually classified, responsive and accessible review cards, each stating what the source shows, what cannot be concluded and the next approval gate:

- `RV-01` Delivery Plan and milestones — SOURCE-ONLY interface capture.
- `RV-02` Diagnostic report/export — SOURCE-ONLY interface capture.
- `RV-03` Major Incident workshop demonstration — MOCK-ONLY synthetic example.
- `RV-04` Workbench overview page — SOURCE DOCUMENT, not an application screenshot.

The four reviewed records are **not** the ten existing unreviewed image candidates. Both sets remain withheld. The cards deliberately display no original pixels, filenames, hashes, internal IDs, private Drive paths or third-party branding. Links lead to public-safe case studies rather than private GitHub repositories.

## Acceptance and regression controls
- `scripts/test_visual_intake_safety.py` now checks the four review aliases and their evidence classes, publication-HOLD labels, unchanged ten-candidate inventory and absence of restricted GitHub links.
- Existing HTML, image approval, navigation and publication checks remain in force.
- A private alias-to-source register is maintained separately; its source identifiers are not mirrored into public assets.
- **Verification:** repository commits represent source-only changes. Automated CI, live Pages rendering and cross-device interaction require separate workflow/browser confirmation.

## Classification and entitlements
A screenshot establishes only that the captured pixels existed. It does not prove installed version, persistence, integration execution or operational acceptance. Historical Delivery DEV 4.20.0 claims do not validate later source versions, and no new independent DEV or production test was performed.

The static page uses HTML/CSS and requires no ServiceNow licence. For runtime verification, confirm custom application/App Engine rights and platform roles; ITSM, ITOM/Discovery, IntegrationHub, Performance Analytics, Now Assist/AI and external-provider entitlements are feature-specific and not assumed.

## Remaining gates
Confirm instance/capture provenance, publication rights and proposed captions; irreversibly redact and re-encode approved derivatives; inspect pixels and metadata; record cryptographic digests and image-specific approval; run CI and browser checks before publication. No public screenshot publication is authorised by this release.

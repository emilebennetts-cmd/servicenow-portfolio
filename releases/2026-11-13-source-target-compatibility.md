# Source-to-target compatibility assurance — 13 November 2026

## User-facing delivery
- New responsive `source-target-compatibility.html`: a dual-cohort technical case study and seven-gate, browser-only review worksheet.
- Linked the experience from the homepage, reviewer guide and bounded Incident native pilot; added it to the sitemap.
- Added `scripts/test_scope_compatibility.py` and a `SCOPE-COMPATIBILITY` source-only claim in the public verification register.
- Worksheet export is explicitly untrusted: `publication_status: HOLD`, no independent DEV/Production verification, historical scope-parity warning preserved.
- No customer, instance, sys_id, scope identifier, private documentation or original screenshot pixels published.

## Source and observation boundaries
The private programme records identify separate application generations: an October 2026 synthetic Incident pilot with historical DEV-reported metadata and draft replay, and a distinct source Workbench with an unrun 29-case native acceptance matrix. The 30 September As-Built is a controlled draft with an earlier source/DEV split. No cross-generation acceptance has been inferred.

## Acceptance outstanding
Validate exact source and target scope, installed version, update-set preview, licensing/table rights, role/ACL negative tests, stale-version/concurrent replay, recovery, operational sign-off, upgrade, native ATF/UAT and privacy review in an authorised environment. No current independent native execution or Production evidence. All genuine screenshot assets remain on individual HOLD.

## CI
`scripts/test_scope_compatibility.py` checks the seven UI controls, non-certifying receipt, source/version boundaries, public links and forbidden target identifiers. Final GitHub Actions run and external GitHub Pages availability require separate confirmation; committing a page alone is not deployment verification.

## Licensing
Public HTML needs no ServiceNow licence. Real delivery requires suitable App Engine/custom app/table rights and platform roles/ACLs; ITSM and optional IntegrationHub, AI, analytics or external services may require additional entitlements.

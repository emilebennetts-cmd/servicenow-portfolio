# Release record — 2026-11-08 — local link gate regression hardening

## Delivered
- Added `scripts/test_local_links_regression.py` with eight isolated `unittest` scenarios.
- Covers valid file links, missing files, missing fragments, fragment-only links, external URL exclusions, directory-index navigation, literal traversal and percent-encoded traversal.
- Uses only Python standard library and temporary fixture directories; does not access external systems.
- Source commit: `205785afcb47725486c9885ddb623758d9aa86ed`.

## Evidence boundaries
- **SOURCE-ONLY:** Test suite committed to public portfolio repository.
- **MOCK-ONLY:** Existing portfolio demonstrations remain illustrative.
- **DEV-VERIFIED:** No ServiceNow DEV execution in this release.
- **PRODUCTION-VERIFIED:** Not claimed.
- Test execution and GitHub Actions outcomes are not independently confirmed in this release.

## Publication and confidentiality
No application screenshots, credentials, customer records or private repository source were added. Genuine captures still require sanitisation, provenance and explicit approval before publication.

## Licensing
No ServiceNow licence required for static website checks. Underlying scoped applications require authorised instance access and applicable custom application entitlements; optional ITOM, IntegrationHub, Performance Analytics and AI features may require additional licensing.

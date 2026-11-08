# Release record — 2026-11-08 — recursive link audit

## Implemented
- Commit `6c01186`: link audit now traverses nested HTML pages, rather than only the site root. Diagnostics include relative page paths for actionable remediation.
- Commit `d29cacf`: added isolated regression scenarios for missing nested targets and valid parent/root-relative navigation.

## Evidence and limitations
- **SOURCE-ONLY:** Python changes and test specifications committed to the public portfolio repository.
- **MOCK-ONLY:** Existing illustrative portfolio UI remains mock-only.
- **DEV-VERIFIED:** No new authenticated ServiceNow DEV test performed.
- **PRODUCTION-VERIFIED:** No production claim or verification.
- CI execution, live GitHub Pages deployment, and browser rendering are not independently confirmed by this record.
- No customer records, screenshots, private repository contents or credentials were added.

## Follow-up
Review CI outcomes and resolve any newly exposed broken links. Continue provenance, sanitisation and explicit approval review before publishing real Workbench captures.

## Entitlements
Static site validation needs no ServiceNow licence. Workbench execution requires authorised instance access, roles and applicable custom app entitlements; optional ITOM, IntegrationHub, Performance Analytics and AI functions may require separate licensing.

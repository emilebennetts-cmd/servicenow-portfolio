# Local-link integrity CI integration — 8 November 2026

## Change
The existing GitHub Actions portfolio quality gate now executes `python scripts/check_local_links.py` on pushes to main, pull requests and manual dispatch. The validator checks local href/src destinations, HTML fragments and site-root escape attempts. It does not check remote URLs.

## Provenance
- Implementation: `.github/workflows/portfolio-quality.yml`
- Validator: `scripts/check_local_links.py`
- Source repositories: `solution-lifecycle-studio` and `Diagnostic-Workbench2` are unaffected by this website-only quality change.
- Private portfolio-control content was not copied or published.

## Evidence classification
- **SOURCE-ONLY:** CI workflow wiring and static validator source.
- **MOCK-ONLY:** Existing illustrative portfolio demonstrations remain illustrative.
- **DEV-VERIFIED:** No ServiceNow runtime tests executed in this change.
- **PRODUCTION-VERIFIED:** None claimed.

## Verification and next actions
GitHub accepted the workflow commit; successful Actions execution must be checked separately. Review failures before considering the gate green. This release does not validate remote links, visual layout, accessibility in a browser, or actual Workbench runtime behaviour.

Genuine screenshot publication remains blocked pending provenance, sanitisation and explicit approval of each derivative and digest.

## Entitlements
No ServiceNow licence is needed for GitHub Pages or this Python validation. Runtime use of scoped Workbenches requires authorised instance access and applicable custom-app entitlements; optional ITOM, IntegrationHub, Performance Analytics and AI capabilities may require additional subscriptions.

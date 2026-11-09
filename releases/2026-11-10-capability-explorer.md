# Capability Explorer release — 2026-11-10

## Delivery

- Added `capability-explorer.html`: responsive, keyboard-accessible two-filter comparison of Delivery and Diagnostic capabilities.
- Source provenance: public `solution-lifecycle-studio` README (v4.22.2 description); public `Diagnostic-Workbench2` README (scoped app and Knowledge Intelligence companion); private `servicenow-portfolio-control` README used for authority and acceptance boundaries, **not reproduced**.
- No screenshots, customer data, secrets, private code, live connectors, or runtime credentials were copied.

## Evidence classifications

- **SOURCE-ONLY:** capability statements about lifecycle gates, implementation presets, Knowledge Intelligence collectors and scoped app boundaries. Source describes historical DEV installation, not independently verified in this release.
- **MOCK-ONLY:** links to synthetic pattern lifecycle and finding-to-delivery walkthroughs.
- **DEV-VERIFIED:** none newly verified.
- **PRODUCTION-VERIFIED:** none.

## Quality and release limitations

- GitHub contents commit confirms source persistence; deployed GitHub Pages rendering, cross-browser behaviour, and CI checks require separate verification.
- Filter UI uses native selects and live status announcement; no third-party JavaScript dependencies.
- No change to private repository visibility or screenshot publication policy.
- Static page has no ServiceNow licensing dependency; actual scoped app deployment may require custom app/App Engine, ITSM, ITOM, IntegrationHub, Performance Analytics, AI and provider entitlements depending on features.

## Next

- Add contextual navigation from the homepage once its current markup is reviewed.
- Verify deployed page and accessibility, and curate genuine screenshots only after irreversible sanitisation and publication approval.

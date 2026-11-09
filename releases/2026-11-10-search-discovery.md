# Search discovery release — 2026-11-10

## Delivered
- Added `sitemap.xml` containing 12 curated public routes: homepage, engineering proof, two case studies, visual walkthroughs, architecture, evidence and methodology.
- Added `robots.txt` with a sitemap directive. Neither file changes ServiceNow code, access, or repository visibility.

## Provenance
- Public portfolio repository root and existing HTML route names inspected before writing.
- Source repositories inspected: `solution-lifecycle-studio` and `Diagnostic-Workbench2`.
- Private `servicenow-portfolio-control` repository root inspected for context; no private content copied.
- No Google Drive files or screenshots published.

## Verification boundaries
- **SOURCE-ONLY:** GitHub accepted commits `ab7be0cb70e800eeb3f9b9cff351ec23007b76de` and `5655853c1a0e747b399181c14e7a32c6e191afac`.
- **MOCK-ONLY:** Previously published illustrative walkthroughs remain illustrative; this release does not modify them.
- **DEV-VERIFIED:** No new ServiceNow instance testing performed.
- **PRODUCTION-VERIFIED:** None claimed.
- **Deployment:** GitHub Pages delivery, HTTP status, crawler indexing and search appearance require independent checks; a committed sitemap is not proof of indexing.

## Security and entitlement
- No secrets, private source, customer data, or unreviewed images included.
- Static sitemap and robots file require no ServiceNow entitlement. Underlying Workbench runtime may require App Engine/custom-app rights; ITSM, ITOM, IntegrationHub, Performance Analytics and AI entitlements are capability-dependent.

## Follow-up
Validate published sitemap and robots responses, audit canonical metadata, and prioritise reviewed real DEV evidence over additional synthetic visual pages.

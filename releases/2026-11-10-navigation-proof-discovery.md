# Portfolio release — engineering proof discovery (2026-11-10)

## Delivered

- Homepage desktop navigation now points to `engineering-proof.html` in place of the generic Approach anchor.
- Mobile portfolio directory now links to both `engineering-proof.html` and `capability-explorer.html`, allowing readers to discover two previously isolated pages.
- Source inspected: `solution-lifecycle-studio/README.md`, `Diagnostic-Workbench2/README.md`, private `servicenow-portfolio-control/README.md`, public homepage. Connected Drive search located `01-Universal-Delivery-Workbench-Solution-As-Built.pdf`; its contents were not reproduced or published.

## Verification and release boundaries

- **SOURCE-ONLY:** GitHub accepted the homepage HTML update; links are relative static routes. No local browser/CI or deployment test is claimed.
- **MOCK-ONLY:** Existing illustrative Workbench experiences remain synthetic, not ServiceNow screenshots.
- **DEV-VERIFIED:** Diagnostic README reports historical installation in dev438211; current runtime was not accessed or independently verified. Private control README reports prior access denial.
- **PRODUCTION-VERIFIED:** None asserted.
- **Sensitive evidence:** No screenshots, customer records, private control contents, tokens or credentials added to the public site.

## Next validation

Check GitHub Pages deployment, inspect desktop/mobile navigation in a browser, then curate only approved redacted instance captures for real-evidence galleries. Maintain provenance per screenshot and explicit approval before publication.

## Entitlements

Static GitHub Pages requires no ServiceNow entitlement. Runtime Workbench installation may require custom scoped-app/App Engine rights; ITSM, ITOM, IntegrationHub, Performance Analytics, AI and provider subscriptions depend on actual deployed modules and integrations. No licence is implied by these static demonstrations.

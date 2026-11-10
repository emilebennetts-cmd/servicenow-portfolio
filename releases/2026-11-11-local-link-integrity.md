# Release record — 2026-11-11 — Local-link quality gate

## Change
- Added `scripts/check-local-links.py`: standard-library HTMLParser audit of relative links, images, scripts, stylesheets and same-page/cross-page fragment identifiers.
- Added `.github/workflows/local-link-integrity.yml`: executes the audit on relevant pushes, pull requests and manual dispatch.
- Reports missing local files, broken fragments, and links escaping the site root. External links are intentionally excluded from this offline audit.

## Evidence / verification
- **SOURCE-ONLY:** Both files committed to the public repository.
- **DEV-VERIFIED:** No ServiceNow instance testing in this change.
- **MOCK-ONLY:** No new simulated runtime features.
- **PRODUCTION-VERIFIED:** No production verification asserted.
- **CI:** Workflow execution and pass/fail outcome not established at authoring time; inspect Actions results and remediate any pre-existing broken references.
- **Screenshots:** No screenshot assets reviewed or published.

## Risk and entitlement boundary
The audit checks repository-local references only; it cannot establish live GitHub Pages deployment, external URL reachability, WCAG compliance, or ServiceNow behaviour. Static HTML and Python require no ServiceNow entitlement. Deploying the underlying scoped workbenches may require App Engine/custom application entitlements and optional ITSM, ITOM, IntegrationHub, PA, AI and third-party subscriptions based on use.

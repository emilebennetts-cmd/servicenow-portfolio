# Workbench architecture gallery — reviewer inspection release

Date: 2026-11-11 (Australia/Sydney)
Scope: public static site; no ServiceNow runtime changes.

## Implemented
- Added four keyboard-accessible, native HTML disclosure panels to the existing Workbench architecture gallery, covering Diagnostic source inspection, Delivery pattern traceability, release evidence promotion, and screenshot publication checks.
- Added mobile single-column layout for inspection panels.
- Added a source-linked static-site release assurance statement and reviewer navigation.

## Verified source references
- Public gallery change: [commit 34b0a5e](https://github.com/emilebennetts-cmd/servicenow-portfolio/commit/34b0a5e87ba5a39cd7d6d7e18ce2a5e05609315d).
- Prior gallery baseline: [commit 234ff578](https://github.com/emilebennetts-cmd/servicenow-portfolio/commit/234ff578e8e1b0dafc8181705f54ef145090d082).
- Prior baseline GitHub Actions: [quality audit](https://github.com/emilebennetts-cmd/servicenow-portfolio/actions/runs/42904025954), [quality gate](https://github.com/emilebennetts-cmd/servicenow-portfolio/actions/runs/42904025948), [Pages deployment](https://github.com/emilebennetts-cmd/servicenow-portfolio/actions/runs/42904025768); all reported completed/success in the GitHub API at inspection time.
- The current change's CI outcome and live browser rendering were not established when this release note was authored.

## Verification boundary
- **SOURCE-ONLY:** current gallery markup and source repository references.
- **DEV-VERIFIED:** historical Delivery 4.5.1 read-back is document-reported; no fresh instance access or test.
- **MOCK-ONLY:** three conceptual architecture diagrams; not screenshots.
- **PRODUCTION-VERIFIED:** not established.
- **Screenshots:** none added; publication gate remains in force.

## Security
No private repository contents, instance identifiers, customer data, credentials, or unreviewed screenshots were copied into the public website.

## Entitlements
Static HTML requires no ServiceNow licence. Actual Workbench runtime features may depend on App Engine/custom app rights, ITSM/ITOM, IntegrationHub, Performance Analytics, AI and third-party subscriptions; validate against the customer contract.

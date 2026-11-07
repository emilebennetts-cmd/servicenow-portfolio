# Engineering case studies — 2026-11-08

## Change

Published `engineering-case-studies.html`, a mobile-responsive, accessible standalone page for Diagnostic Workbench 2 and Universal Delivery Workbench. Each case study includes client pain, ServiceNow solution, architectural best practices, a lifecycle diagram, source link and independently actionable verification checklist. No screenshots or private source were copied.

## Sources reviewed

- `emilebennetts-cmd/Diagnostic-Workbench2` public `README.md` (main)
- `emilebennetts-cmd/solution-lifecycle-studio` public `README.md` (main)
- `emilebennetts-cmd/servicenow-portfolio-control` private `README.md` (main), used for boundary checking only; no private content reproduced.
- Google Drive search for Diagnostic Workbench material returned client-neutral HTML references, but no assets were authorised for publication.

## Evidence classification

- SOURCE-ONLY: current architectural and capability narrative, tied to public repository documentation.
- HISTORICAL DEV-REPORTED: repository-reported prior instance read-back; no fresh validation performed.
- MOCK-ONLY: flow illustrations and portfolio interactions.
- DEV-VERIFIED: no fresh verification in this release.
- PRODUCTION-VERIFIED: none claimed.

## Validation and release limitations

- HTML is semantic and CSS responsive at 740px breakpoint; native details controls provide keyboard access.
- Commit receipt confirms GitHub write; deployment, live URL response, browser visual regression, accessibility audit and workflow success have not been verified.
- Public navigation to the new page from the homepage is not yet added.
- Screenshot publication remains blocked pending provenance, redaction and explicit approval; do not publish Drive HTML or screenshots without review.

## Licensing

Static GitHub Pages requires no ServiceNow entitlement. Runtime requires appropriate instance and custom-app entitlements. Optional ITOM, IntegrationHub, analytics, AI and provider connectors may require additional subscriptions.

# Homepage accessibility correction — 2026-11-10

## Scope and release receipt
- Homepage: `index.html`
- Implementation commit: `a020d10481de10739d748c72eade81f3cc575137`
- Change: removed the second, redundant keyboard skip-to-main link while retaining the existing visible-on-focus `skip-to-content` link targeting `<main id="main">`.
- Reason: two consecutive skip controls linked to the same target, creating unnecessary keyboard stops and an inconsistent screen-reader experience.

## Evidence and verification
- **SOURCE-ONLY:** GitHub contents read and update succeeded; the retained target `#main` and associated focus styling were checked in source.
- **DEV-VERIFIED:** No ServiceNow instance was accessed in this change.
- **MOCK-ONLY:** Existing synthetic demonstration content was not changed.
- **PRODUCTION-VERIFIED:** Not claimed; public GitHub Pages rendering and keyboard traversal have not been independently tested.
- **Screenshots:** None added, reviewed, or published.

## Security and licensing
No customer data, screenshots, private repository contents, credentials, or ServiceNow instance configuration were changed. This static-site accessibility correction has **no ServiceNow licensing or entitlement dependency**. Runtime Workbench capabilities remain subject to applicable App Engine, ITSM/ITOM, IntegrationHub, PA, AI and provider licensing, where used.

## Follow-up
Validate deployed homepage keyboard navigation, mobile viewport and Pages deployment status. Continue approved screenshot provenance and sanitisation review before any public gallery publication.

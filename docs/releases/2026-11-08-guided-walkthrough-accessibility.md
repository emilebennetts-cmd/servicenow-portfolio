# Portfolio release — 2026-11-08 — guided diagnostic walkthrough accessibility

## Implementation
- Commit `0d20752a9e261baf27815198fec4f57b93a4e474` adds a visible five-stage progress bar to the existing Diagnostic Workbench guided walkthrough.
- The stage transition now updates a screen-reader live status, announcing the illustrative nature, stage number and stage title.
- Motion is disabled under `prefers-reduced-motion`. Existing previous/next and direct stage controls are preserved.
- The update changes the existing homepage experience; it does not introduce another standalone public page.

## Evidence and publication boundary
- Walkthrough: **MOCK-ONLY**, informed by existing repository descriptions and historical evidence. It is not a live ServiceNow connection or genuine screenshot.
- Application source descriptions: **SOURCE-ONLY** unless separately verified.
- Historical DEV tests: **DEV-REPORTED**, not independently repeated during this release.
- Current **DEV-VERIFIED** and **PRODUCTION-VERIFIED** status: not established.
- No original screenshots, private source, credentials or customer data were published.

## Validation and remaining work
- Source replacement anchors and live-region/progress markup checked during commit creation.
- Automated browser accessibility testing and live GitHub Pages deployment confirmation remain outstanding.
- Original screenshot publication requires per-image provenance, sanitisation and approval. Until then, label reconstructions clearly.
- Public static website: no ServiceNow licence. Runtime scoped apps and assessed ITSM/ITOM/IntegrationHub/AI capabilities require appropriate instance access, roles and relevant product/spoke entitlements.

# Architecture gallery keyboard-access release — 2026-11-11

## Implemented
Added a visible-on-focus skip-to-main-content link to `workbench-architecture-gallery.html`, and an explicit focusable `main-content` target. This allows keyboard and assistive-technology users to bypass repeated page navigation.

## Evidence and verification
- **SOURCE-ONLY:** commit `3bcd39903cfa05343746a236f0c1849672964218` contains the HTML/CSS change.
- **DEV-VERIFIED:** no new ServiceNow instance test performed.
- **MOCK-ONLY:** existing conceptual architecture diagrams remain illustrative.
- **PRODUCTION-VERIFIED:** no production ServiceNow claim.
- **Browser/CI:** interactive keyboard and GitHub Pages deployment verification remain pending.

## Security and publication
No screenshot assets, private repository contents, customer data, credentials, or visibility settings were changed. The existing gallery's source links and verification labels remain intact.

## Licensing
The static accessibility change requires no ServiceNow licence. Deployment of the Workbenches may depend on App Engine/custom application entitlements and, by functionality, ITSM, ITOM, IntegrationHub, Performance Analytics, AI or third-party licences.

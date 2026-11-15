# Workbench source-to-DEV provenance gap board — 16 November 2026

## 1. Client pain & historical boundary
A controlled As-Built dated 30 September 2026 describes Delivery source 4.6.1 and historical DEV read-back 4.5.1. Later repository release records report an October 2026 DEV read-back at 4.20.0; current Delivery README declares 4.22.2. These observations are from **different dates and versions**, not proof that 4.22.2 is installed. Diagnostic Workbench 2 and companion KI 0.1.0 are a separate application identity, with 30 September historical DEV observations.

No customer outcome is attributed. The client story is representative.

## 2. ServiceNow solution shipped
- Responsive public [Workbench source-to-DEV gap board](../workbench-source-dev-gap-board.html), preserving four clearly dated provenance snapshots.
- Twelve acceptance controls: five Delivery, four Diagnostic and three cross-workbench, each visible with `NOT RUN · HOLD`.
- Keyboard-operable filter buttons with `aria-pressed`, visible filter count and reduced-motion / mobile layouts.
- All-control CSV export (13 columns) with **NOT RUN / HOLD / SOURCE-ONLY** and six blank private execution receipt columns: instance, version, executor role, UTC, evidence reference and independent reviewer.
- Local-only script, restrictive CSP, no image loading, no network access, no storage, no ServiceNow write capability.
- Homepage, Explorer, sitemap, architecture gallery, release log and automated test integration.

## 3. Architecture and evidence boundaries
- **SOURCE-ONLY**: current repository declarations and this authored HTML / JavaScript. No authenticated current DEV read-back.
- **DEV-REPORTED**: dated historical test and installation claims in the source documents. None was rerun for this release.
- **MOCK-ONLY**: browser-local controls and CSV simulation; not ServiceNow test execution.
- **DEV-VERIFIED / PRODUCTION-VERIFIED**: no new claims.
- **Screenshots**: no original ServiceNow screenshots, public screenshot approvals or private client records included.

Source review: private `solution-lifecycle-studio` README and HANDOVER, private `Diagnostic-Workbench2` README, README_BUILD and KI README, and Drive controlled `01-Universal-Delivery-Workbench-Solution-As-Built.pdf` dated 30 September 2026. The public page contains only a sanitised version-level narrative.

## 4. Verification gates
Local source preflight checked 12 unique IDs, offline classification, page canonical and accessible filter hooks. Added Node execution tests and Python structural/registration tests; these run in GitHub Actions `portfolio-quality.yml`. Final CI and live HTTP deployment results must be checked separately; a commit alone does not establish success.

## 5. Licensing / entitlement dependencies
Static HTML and CSV export require no ServiceNow licence. Native acceptance requires authorised DEV access and relevant App Engine/custom-table rights if applicable; verify ITSM, ITOM/Discovery, IntegrationHub, ATF, AI and analytics entitlements independently against the actual contract and target release. Neither a PDI nor a source build proves enterprise licensing.

## 6. Blockers
Current authenticated DEV scope/build read-back, synthetic transaction tests, negative-persona ACLs, independent reviewer receipt and specific screenshot approvals are outstanding. No repository visibility or screenshot HOLD status has been changed.

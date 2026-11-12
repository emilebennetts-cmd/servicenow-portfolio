# Release — Diagnostic baseline / rescan decision lab

**Date:** 13 November 2026 (Australia/Sydney)  
**Status:** Source implementation committed; CI and Pages acceptance to be independently verified against final SHA.  
**Classification:** SOURCE-ONLY engineering architecture; MOCK-ONLY calculations, synthetic fixture scenarios and downloadable receipts; historical DEV-REPORTED results have not been reproduced.  
**Screenshots:** 0 approved; all genuine Workbench captures HOLD.

## 1. The client's pain and history

An enterprise CMDB team can misread falling counts as a successful remediation when the number of discovered CIs increases, scope changes, metric fields are unavailable, or a new collector version changes the measurement. The source Diagnostic Workbench 2 design explicitly requires evidence-first validation and a Not assessed state for absent evidence.

## 2. Implemented ServiceNow-aligned solution

New [Diagnostic Baseline and Rescan Decision Lab](../diagnostic-rescan-decision-lab.html), purpose-built as a static, mobile-friendly demonstration:

- Four fully synthetic, anonymised aggregate-CI fixtures: improvement, missing collection, incompatible collector version and regression.
- A ratio/percentage-point comparator that uses per-snapshot denominators rather than raw count differences.
- Fail-closed comparability gates: scope, read-only declaration, data/privacy completeness, denominator, collector identity/version and independent approval.
- Adjustable decision threshold, contextual metric cards, gated reviewer interpretation and source-versus-runtime classification.
- Browser-local HOLD-only JSON export and print view. Receipts explicitly set `execution_status=NOT RUN`, `approval_status=HOLD`, `servicenow_dev_verified=false`, `production_verified=false` and `public_release_authorised=false`.
- No access to ServiceNow, private GitHub or Drive. No sample screenshots, customer data or collector script source.
- Linked from the homepage directory, 90-second guide, searchable explorer, sitemap and public verification manifest.

## 3. Architectural best practices

The concept favours native CMDB Health, IRE and platform controls before custom remediation; restricts collection to authorised non-production, read-only aggregate evidence; requires sign-off for diagnosis-to-delivery transfer; and preserves separate evidence lineages. Diagnostic Workbench 2's 20 collectors/42 rules/four correlations are **not** the Knowledge Intelligence add-on's separately defined 45 collectors. Historical source statements are not current instance acceptance.

### Quality / evidence state

- Source contract: `scripts/test_diagnostic_rescan_lab.py` (added to CI).
- Responsive Playwright: `scripts/browser_diagnostic_rescan_lab.py` at 390, 768, 1024 and 1440 px, including four fixture branches, threshold, reset, no-network gate and JSON HOLD export (added to workflow).
- All four input scenarios are synthetic; no customer records or secret fields embedded.
- Static / browser quality checks and GitHub Pages deployment **pending final CI verification** at log creation.
- No fresh DEV-VERIFIED or PRODUCTION-VERIFIED result, completed UAT, live collector execution or screenshot publication approval.

### Entitlement boundary

The public static page has **no ServiceNow licensing requirement**. Deploying any native Workbench capability requires target App Engine/custom app rights, custom table allowances, roles and ACLs. OOTB CMDB/ITOM Discovery, IntegrationHub, PA/AI and knowledge provider subscriptions vary with purchased entitlements and data-use permissions. Confirm per client.

### Public sources and provenance

Summarised source review: Diagnostic Workbench 2 `README.md`, `README_BUILD.md`, Knowledge Intelligence `README.md`, `docs/VERIFY.md`, `docs/GOVERNANCE.md`. Private source code and customer material are not replicated. Drive Architecture/As-Built and visual assets remain held in controlled locations.

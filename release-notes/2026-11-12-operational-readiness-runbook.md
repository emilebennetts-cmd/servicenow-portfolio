# Operational readiness & support runbook — 12 November 2026

## The client's pain and history
A delivered ServiceNow implementation is not automatically supportable: named service ownership, alert thresholds, privilege reviews, release read-backs, recovery rehearsals, consent validity, and privacy decisions may still be missing. The controlled September 2026 documentation identified exactly these gaps and an important source-versus-runtime release mismatch.

## ServiceNow solution delivered
- New [Operational Readiness & Support Runbook](../operational-readiness-runbook.html), mobile-friendly and client-neutral.
- Twelve source-derived operational checks: **3 daily, 2 weekly, 3 per release, 4 quarterly**. Search, accessible cadence filters, reset and print stylesheet require no login or network.
- Six safe failure-containment decisions: update-set preview, expired consent, invalid target schema/licensing, AI unavailable, missing role/ACL, and platform recovery.
- Clear handover contract: source/document reproduction, authorised DEV installation, security/privacy assurance, named support owners, recoverability/performance, change-controlled Production promotion.
- Connected public navigation, 90-second assurance route and sitemap; added static confidentiality contract and four-viewport Chromium interaction test, with CI trigger.

## Source provenance and evidence model
Controlled documents inspected through connected Google Drive:
1. **Universal Delivery Workbench Architecture**, 30 September 2026, sections 11–14 (quality attributes, ADRs, failure containment, unresolved decisions).
2. **Universal Delivery Workbench Solution As-Built**, 30 September 2026, sections 13 and 15–18 (operational cadence, release testing, gaps and handover).
3. **Universal Delivery Workbench User Guides and Training**, 30 September 2026, sections 5–8 (safe operating responses, roles, administration cadence and practical exercises).

The controlled source 4.6.1 baseline and historical DEV read-back 4.5.1 represent **different versions**. No new native ServiceNow DEV read-back, Production validation or independent owner sign-off was performed. **SOURCE-ONLY** describes this public page and documented runbook controls; browser interactions are illustrative only and do **not** verify ServiceNow. Historical **DEV-REPORTED** results are version/date-specific. **DEV-VERIFIED: none newly established. PRODUCTION-VERIFIED: none.** Original Workbench screenshots remain private on publication **HOLD**; **zero approved** public images. All controls are summarised and sanitised; original private documents are not redistributed.

## Architecture and acceptance guidance
Prefer OOTB platform ACLs, scoped roles, update-set preview and reconciliation, native logs/scheduled jobs, change control and incident/problem management. Keep consent, credentials, kill switches, deferred scope and independent approvals as gates. No unreviewed source/private captures, credentials, customer data, internal instance names or repository visibility changes were included.

## Licensing / entitlements
No ServiceNow licence is required for this static public page. Native use must confirm App Engine/custom application and table allowances, appropriate scoped roles/ACLs and installed release compatibility. Actual ITSM, ITOM/Discovery, IntegrationHub, analytics/AI, PDF and external provider functionality may carry separate contract, plugin and subscription dependencies.

## Release verification
Public source and test commits must be checked by GitHub CI and Pages. A passing browser smoke verifies only the public HTML tool; it is not a ServiceNow acceptance result. Host HTTP reachability and current installed runtime are separate evidence items.

## Linked evidence and repository continuity
- Public verification register now includes `OPERATIONS-READINESS` as the **19th source-classified claim**. Six separately classified synthetic/mock demonstrations remain MOCK-ONLY.
- The Delivery Workbench repository's `docs/portfolio/governed-delivery-showcase.html` links to the public runbook, maintaining a direct source-to-portfolio navigation route.
- Responsive browser expectations and the exact record count have been updated, but their hosted CI outcome was not independently confirmed during this release. No independent external HTTP check succeeded; treat the GitHub Pages URL as the configured publication destination until verified.

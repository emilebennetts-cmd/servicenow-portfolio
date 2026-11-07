# Evidence-first technical review — 7 November 2026

## Change
- Added an integrated, responsive 90-second technical review directly above the application explorer on the public homepage.
- Three accessible, high-contrast cards connect source-backed Diagnostic and Delivery mechanisms with explicit verification boundaries.
- Links remain within the same homepage; no external document navigation is required.
- No real client names, instance URLs, sys_ids, customer records, or unreviewed images added.

## Provenance and claim status
- Diagnostic counts (20 collector packs, 67 runbooks, 42 rules, four correlations): **SOURCE-ONLY**, documented in Diagnostic-Workbench2/README_BUILD.md. No fresh runtime measurement.
- Delivery lifecycle: **SOURCE-ONLY**, documented in solution-lifecycle-studio/README.md.
- Historical DEV activity: **DEV-REPORTED**, not independently re-tested in this change.
- Interactive demonstrations: **MOCK-ONLY** unless separately evidenced.
- **DEV-VERIFIED**: none newly established.
- **PRODUCTION-VERIFIED**: none claimed.

## Checks
- Verified all three homepage anchor targets exist in source.
- Verified the new block is present once.
- Reviewed newly added content for named clients and private instance/scope identifiers: none.
- Browser rendering, automated WCAG audit and GitHub Pages deployment remain **not independently verified**.

## Next work
- Replace illustrative application views with approved, sanitised DEV captures after publication review.
- Audit all public pages and assets for sensitive content.
- Run mobile, keyboard, contrast, and performance tests on deployed Pages.
- Validate current runtime independently before upgrading any DEV claim.

## Entitlements
Static portfolio: no ServiceNow entitlement. Workbench execution: appropriate ServiceNow platform/scoped app rights, instance roles and approvals. Optional ITOM, IntegrationHub/spokes, AI and analytics capabilities depend on purchased product entitlements and must be checked separately.

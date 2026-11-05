# Release — Diagnostic Workbench 2 technical case study

Date: 2026-11-06 (Australia/Sydney)

## Implemented

- Published `diagnostic-architecture.html` as a responsive, accessible technical case study.
- Linked the Diagnostic Workbench featured project on `index.html` to the new page.
- Included pain/history, solution, OOTB/architectural best practices, component boundaries, verification matrix, licensing caveats and Drive-provenance links.
- Explicitly separated the primary workspace's 20 embedded module-pack collectors from Knowledge Intelligence's 45 separately deployed collectors.
- Described source-recorded DEV testing and installation without implying independently reverified production state.

## Source evidence

- Private `emilebennetts-cmd/Diagnostic-Workbench2/README.md`: scope, DEV status, companion integration boundary.
- Private `emilebennetts-cmd/Diagnostic-Workbench2/README_BUILD.md`: 18-stage/six-phase assessment; 67 runbooks; 20 collectors; 42 rules + 4 correlations; 19 local view checks; 2026-09-01 DEV acceptance notes.
- Private `emilebennetts-cmd/Diagnostic-Workbench2/knowledge-intelligence/README.md`: 2026-09-30 DEV installation notes; 347 inserts; 45 collector lint checks; 16 packs and 38 solution patterns; DRAFT state.
- Drive: `DemoClient23_Diagnostic_Workbench_Completion_Runbook.pdf` (ID `1o60c9pSH9dO__ofazVvp12Qwxppkor-M`): fictional showcase, 45% baseline, G2–G6 outstanding.
- Drive screenshot candidates: `Workbench_dashboard.png` (`17QeSlLguEUu_F6BzrMHgSHGETGw4xo1q`), `Workbench_explorer_finding.png` (`1cW4QhLFgpmQDAbNLUFCe85RqalNUZyq-`), `Workbench_modules.png` (`1u_XlOxsOoreXAe461rwaAoKsxQtiGdzD`).

## Outstanding

- Inspect original screenshot pixels, verify they depict the intended application/version and redact all private/customer data before publishing image bytes.
- Independently verify public GitHub Pages response after deployment.
- Add feature-by-feature annotated real screenshot galleries after clearance.
- Cross-link Diagnostics → Delivery evidence handoff with source-specific schema and tests.

## Security and licensing

No private source, credentials or customer records published. Drive URLs may require sign-in. Static hosting does not require a ServiceNow licence; custom app, product and integration entitlements require target-instance validation.

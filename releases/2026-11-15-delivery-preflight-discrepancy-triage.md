# Delivery Release Identity Preflight — Discrepancy Triage Correction
**Date:** 15 November 2026  
**Status:** Public tool MOCK-ONLY / reviewed baseline SOURCE-ONLY / native acceptance HOLD

## 1. The client's pain & history
The Delivery source release is declared as 4.22.2 for technical scope `x_1577958_vdf`. Historical target reports include 4.20.0 and a separate `x_eitsp_vdf` demonstration identity. The original offline preflight used the same "divergent application identity" decision for *any* metadata mismatch. This conflated version drift within the same technical scope with scope divergence between different applications, and could send a reviewer down the wrong remediation path.

## 2. The ServiceNow solution — implemented
Updated the existing [release identity preflight](../delivery-release-evolution.html#release-identity-preflight), **not** a separate speculative application.

| Sanitised observation | Comparison result | Updated HOLD reasoning |
|---|---|---|
| Scope differs; version matches | Scope MISMATCH | Technical scope differs: verify approved mapping/target fork, application sys_id and package lineage |
| Scope matches; version differs | Version MISMATCH | Release version differs: review installed package/build, source-to-target compatibility, tested baseline |
| Both differ | Two MISMATCH results | Scope and version both differ: verify separate migration and release evidence |
| Either value invalid | INVALID INPUT | Reject invalid technical-scope or three-part numeric-version format |
| Both match | TEXT MATCH · NOT VERIFIED | Remain HOLD; labels cannot authenticate a package or native runtime |
| Missing value | UNAVAILABLE | Remain HOLD; insufficient target metadata |

Added a deterministic `discrepancy_category` to the existing redacted JSON worksheet using one of `scope`, `version`, `scope-and-version`, `invalid-format`, `insufficient-metadata`, `text-aligned-not-verified`. This field never contains input metadata, identifiers, customer records or screenshots. The worksheet schema remains backwards-compatible (`portfolio.release-identity-preflight.v1`).

Updated static contract checks and Chromium scenarios to exercise three distinct discrepancy decisions, unknown input, a positive text match that still fails native attestation, invalid values, and zero raw-value leakage in the exported worksheet. Browser checks cover 390, 768, 1024 and 1440px viewport widths.

## 3. Architectural best practices, controls and entitlements
The preflight is an **offline, unauthenticated, non-certifying reviewer aid**. The authoritative verification sequence is: establish intended target scope and app sys_id, record immutable source commit and package hash, review approved scope migration where relevant, perform authorised installed package/version read-back, execute role/ACL positive and negative cases, retain independently witnessed acceptance results and obtain release approval. A version mismatch alone does not prove a different scoped application.

**Evidence labels:** reviewed repository definitions SOURCE-ONLY; browser scenarios MOCK-ONLY; older document-provided DEV observations DEV-REPORTED (not independently re-performed); zero new DEV-VERIFIED or PRODUCTION-VERIFIED observations. Genuine original screenshots remain **0 approved / HOLD**.

**Security:** No live ServiceNow connectivity, network submissions, local persistence or browser analytics. Entered values stay in memory while the page is open and are not included in JSON downloads. No private source or customer information is published.

**Licensing:** Public static website and offline preflight: none. Any native deployment/acceptance requires authorised DEV instance access; ServiceNow custom scoped application/App Engine entitlements and relevant roles, ACLs and tables; contracted ITSM, ITOM, IRM, HRSD, CSM and other product subscriptions where patterns touch them; separate consideration of IntegrationHub, AI/analytics and external provider/spoke licences.

## Verification and blockers
- Source implementation: [commit 66bff1f](https://github.com/emilebennetts-cmd/servicenow-portfolio/commit/66bff1fe595c1486ca269b815603bfc2ac041286)
- Static and Chromium regression updates: `scripts/test_release_identity_preflight.py` and `scripts/browser_release_identity_preflight.py` on default branch.
- Browser/quality/Pages results must be confirmed against the **final repository head** separately from historical CI runs. GitHub Pages deployment does not constitute native DEV verification.
- Outstanding: current native DEV package/read-back and witnessed acceptance, actual production acceptance, contract-specific entitlements, individually approved sanitised screenshots and independent URL reachability.

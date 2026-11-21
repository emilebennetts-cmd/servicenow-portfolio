# 21 November 2026 — Documentation currency and training-readiness gate

**Release type:** Public SOURCE-ONLY portfolio experience and source-document crosswalk. **Runtime status:** Newly DEV-VERIFIED 0; PRODUCTION-VERIFIED 0; real screenshot publication approvals 0 / HOLD.

## 1. The client's pain & history

Four controlled source documents do not describe one homogeneous runtime baseline. The Universal Delivery Workbench As-Built and User Guides & Training were compiled on 30 September 2026 against source release **4.6.1**; their recorded DEV baseline was **4.5.1**. A subsequent Architecture record, with an evidence cutoff of **19 October 2026**, describes source **4.22.2** and an independently dated 6 October historical DEV read-back. The Diagnostic completion runbook is an expressly **fictional non-production showcase** and cannot be treated as certification of a live target. The Delivery repository main manifest also declared `4.22.2` when rechecked on 21 November; no live instance read-back occurred in this run.

Publishing a combined training story without reconciling the document version, target application, installed runtime and approval chain would risk false evidence assertions and outdated user instructions.

## 2. The ServiceNow solution implemented

- Added [Documentation Currency Gate](../documentation-currency-gate.html), a responsive, screen-reader-labelled public case study and interactive review with a four-document SOURCE-ONLY register. It compares only the exact historical **4.6.1** and **4.22.2** snapshots and makes no claim that either is a presently installed release.
- Added `documentation-currency-model.js` with four fixed, sanitized document descriptions, deterministic version-drift states, rejection of unknown targets, no live instance access and a **four-row HOLD-only CSV**. Exact matches indicate document alignment, **not** native acceptance, current DEV installation or publish clearance.
- Linked the review from the [homepage](../index.html) and [Evidence Library](../evidence.html) and indexed the new public route in [sitemap](../sitemap.xml).
- Added eight deterministic Node regressions and a required step in the existing public GitHub Actions portfolio-quality workflow. Tests check snapshot drift in both directions, fictional DIAG boundary, fail-closed invalid targets, export size and privacy, and immutable NOT RUN/HOLD states.
- No controlled document bytes, confidential instance URLs, screenshots, Drive file identifiers or private repository sources were copied into the public website.

## 3. Architectural best practices and follow-up acceptance

OOTB-first ServiceNow design, transparent source-to-target version mapping, role-based test execution, immutable evidence history, separation of duties and release-by-release documentation review are required before using controlled materials for live training. A native review must check the scoped package/version and hash, target roles/ACLs, current data and integrations, entitlements, role-specific procedures and independent approval. Historical source and DEV claims remain dated; no Production claim can be inferred.

The static site requires no ServiceNow licence. Native target operation and testing require authorised custom-scoped application permissions plus contractual entitlements for any invoked ITSM/CMDB, Discovery/ITOM, Service Graph, IntegrationHub/spokes, ATF, Performance Analytics, AI, SecOps, IRM, HRSD, CSM or ITAM capability.

**Source read-back:** Delivery private repository main at `af8605082439eb3bc94fe289cae191d888fc08a2` (read on 21 November; `app/package.json` version 4.22.2); Diagnostic private repository main at `b520fbb8a6485957a23c9c60791763b47b13f51d`. The four controlled Google Drive document originals were read in the connected user-owned store on 21 November. Private custody details are in the restricted control log; no originals redistributed.

**Release verification:** Node tests and GitHub Actions results are tracked separately from this commit and must not be represented as passed until observed. Website deployment, anonymous external HTTP accessibility, any DEV acceptance and all screenshot approvals remain independently checkable.

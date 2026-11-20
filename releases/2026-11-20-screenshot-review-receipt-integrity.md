# 20 November 2026 — Screenshot review receipt integrity and privacy containment

**Evidence class:** SOURCE-ONLY public website change. The browser-local control does not constitute authorised DEV execution, Production acceptance or permission to publish a screenshot.

## 1. The client's pain & history

The existing image publication checklist could mark nine human controls complete using an evidence alias alone. It did not bind the review draft to the exact bytes of the final flattened image, and user-entered review notes could be exported even when they included an instance URL, email, sys_id, IP address or credential-like value. A reviewer could also mistake the ten historical public candidate slots for the separate eight source files visually inspected on 19 November. These inventories may overlap.

Source review used the public publication workflow and 19 November [visual inspection release](2026-11-19-private-image-triage.md), as well as the controlled Delivery As-Built, Architecture and Training references and Diagnostic completion runbook. The controlled documents contain dated source/DEV descriptions, not new current installed-state verification.

## 2. The ServiceNow solution and delivered change

- Added `screenshot-review-safety.js` as a deterministic browser-only receipt model: safe evidence alias, 64-character SHA-256 of the **final redacted PNG**, fail-closed nine-control review, and suppression of suspicious notes.
- The updated [screenshot publication gate](../screenshot-publication-gate.html) links to the [local PNG receipt verifier](../screenshot-receipt-verifier.html). Draft export is disabled when the alias is unsafe or notes appear sensitive. A missing SHA-256 prevents a completed review, even with nine checkmarks.
- Exports use `portfolio-screenshot-review-v2`, omit invalid identities and digests, and retain an explicit `blocked` or `review_complete_not_auto_authorised` status. There is **no** `approved` or `publish` state. The heuristic notes checker cannot certify privacy.
- Reconciled the public notice: ten historical candidate slots and eight inspected private source images (possible overlap), zero public approvals. No image files, Drive IDs, controlled names, customer information or source code from the private repositories were published.
- Added ten Node regressions to the main quality workflow for identity, digests, missing review controls, suspicious notes and non-authorising exports.

## 3. Architectural best practices and verification

Least privilege, explicit release authority and byte-bound approval preserve a defensible evidence trail. SHA-256 validates byte identity only; it cannot establish actual runtime execution, redact pixels, validate consent or independently attest owner authority. Reviews therefore remain **HOLD** until verified final pixels, image rights and approval are recorded in a controlled register. Public draft JSON should be checked before sharing.

This release changes only GitHub Pages source code and tests. **New DEV-VERIFIED: 0. PRODUCTION-VERIFIED: 0. Public original screenshot approvals: 0.** The two historical Delivery screens remain dated DEV-labelled candidates, not fresh verification; the Diagnostic illustration remains MOCK-ONLY.

**Licensing and entitlements:** The offline gate and static website require no ServiceNow licence. Actual scoped Workbench operation requires appropriate application hosting rights, roles and ACLs; ITSM, ITOM/Discovery, Service Graph Connectors, IntegrationHub, SecOps, IRM, ITAM, AI and analytics must each be checked against the target instance and contracted capabilities when used.

**Remaining blockers:** Final image-specific owner/independent reviewer approval, pixel/metadata review, authorised current DEV read-back and native test evidence. CI and live-URL status must be confirmed separately from committed source.

**Implementation trail:** `screenshot-review-safety.js`, `screenshot-publication-gate.html`, `tests/screenshot-review-safety.test.cjs`, `.github/workflows/portfolio-quality.yml`.

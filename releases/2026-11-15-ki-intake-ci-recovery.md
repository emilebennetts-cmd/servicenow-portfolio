# Knowledge Intelligence CSV intake — quality-gate recovery

**Date:** 15 November 2026 (Australia/Sydney)  
**Public page:** https://emilebennetts-cmd.github.io/servicenow-portfolio/ki-matrix-intake.html  
**Evidence boundary:** MOCK-ONLY website review, SOURCE-ONLY KI taxonomy, PROPOSED acceptance cases; **NOT RUN / NOT VERIFIED / HOLD**.

## 1. The client's pain and history

The portfolio published a browser-based CSV intake feature, but the first read-back of GitHub Actions at the then-current head found three independent failures. A successful GitHub Pages deployment did **not** mean the page passed regression or quality gates:

- Portfolio quality audit reported **"Heading count stale (expected 78)"** and **"Hero count stale (expected 78)"** in the curated Explorer.
- Source quality gate reported an **unregistered** `ki-matrix-intake.html` claim and an annotation mismatch caused by the missing public register entry.
- Chromium intake regression reported status **"New file selected ... HOLD"** where the test expected completed **"Full plan structurally aligned: 180 cases"**. The test clicked and asserted before the async browser `File.text()` operation completed.

Evidence inspected: public GitHub Actions runs 43627075019, 43627074966, and 43627000412, plus public source and restricted Knowledge Intelligence README. The private README describes a **historical 30 September 2026 DEV-reported** installation/lint result, not newly witnessed acceptance. No client data or original images were used.

## 2. The ServiceNow-oriented solution

- Updated the curators' result count to **78**, excluding the Portfolio Explorer page itself from the 79 root HTML pages.
- Added `KI-MATRIX-INTAKE-STRUCTURAL-REVIEW-20261115` to the public evidence register as **MOCK-ONLY**, with explicit native execution and screenshot HOLD boundaries.
- Strengthened `tests/ki-matrix-intake.cjs` so all six CSV review actions wait for the browser's finished assessment rather than simply waiting for the click dispatch. Original full CSV (180 cases), BOM import, filtered subset, altered status, duplicate ID and invalid CSV remain covered at 390/768/1024/1440 widths.
- Preserved the existing local-only architecture, no browser storage/uploads or external calls, and the non-certifying JSON review receipt.

## 3. Architectural best practices and acceptance boundary

This release repairs website quality controls, not native ServiceNow capability. It cannot certify the 45 collectors, native target schema, roles/ACLs, any DEV or Production tests, client-specific entitlement rights, or image publication approvals. Historical DEV-REPORTED is never promoted to DEV-VERIFIED by GitHub CI.

**Required release checks:** GitHub Actions quality audit, source quality gate, new KI Chromium regression, link integrity, publication security and Pages deploy against the final commit. Treat outcomes as **pending until GitHub reports conclusion**.

**Entitlements:** The public HTML, CSV review and local JSON export require **no ServiceNow licence**. Native Knowledge Intelligence needs confirmed App Engine/custom-table and scoped application rights, `ki_admin`/`ki_user` (as appropriate), ACLs, licensed underlying ITSM/CMDB/ITOM/ITAM/SecOps/IRM/HRSD/CSM/SPM content, plus optional IntegrationHub, AI, ATF and third-party knowledge rights.

**Restricted evidence:** Existing sensitive source, customer details and genuine screenshots stay private; publication approval count is **zero / HOLD**. Independent native DEV and Production acceptance remain outstanding.

## Follow-up: narrow-screen overflow and variable catalogue tests

An initial browser regression read-back at 390px exposed a real page overflow (document 498px versus a 390px viewport). DOM inspection isolated the overlong slash-delimited licensing string inside a notice paragraph. Added `overflow-wrap:anywhere` to prose/list text so the entitlement explanation wraps within the mobile viewport rather than being clipped. The Worklist browser contract previously assumed exactly 20 MOCK-ONLY claims; with the newly registered intake claim, its JSON/CSV assertions now derive the expected number from the public register. Browser quality results remain pending a fresh final-head run.

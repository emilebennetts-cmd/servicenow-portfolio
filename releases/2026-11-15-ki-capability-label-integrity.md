# Knowledge Intelligence intake — canonical capability label integrity

**Date:** 15 November 2026 (Australia/Sydney)  
**Public tool:** https://emilebennetts-cmd.github.io/servicenow-portfolio/ki-matrix-intake.html  
**Scope:** Offline public planning CSV validation only. **SOURCE-ONLY / PROPOSED / MOCK-ONLY; NOT RUN / HOLD.**

## 1. The client's pain & history

The 180-test Knowledge Intelligence planning matrix is handed between architects, build engineers and reviewers. The prior structural gate checked that each capability description was non-empty, but did not ensure it belonged to its source module. An otherwise valid row could carry another module's label, or CSV text beginning with a spreadsheet formula. This was a defect in the *public CSV planning gate*, not evidence of a defect in the private native ServiceNow app.

## 2. The ServiceNow-oriented solution

- Pinned all 45 exact capability descriptions to the public module catalogue in `knowledge-intelligence-acceptance-matrix.html`.
- The offline intake now rejects any capability value that differs from its module's published description, including swapped descriptions, formula-like values and whitespace changes.
- The synthetic one-module demonstration uses the exact same canonical label and acceptance procedure as ordinary CSV imports.
- The exported review receipt includes `capability_label_check: true`; authenticity remains `cryptographic_authenticity_verified: false`, native tests remain `NOT RUN`, and authorisation remains `HOLD`.
- Existing exact case IDs, table/domain mapping, canonical test procedures, four-case coverage and duplicate/unsafe-flag checks remain enforced.
- No secrets, customer inputs, screenshot originals, server calls or browser storage were introduced. The site still processes files locally.

## 3. Architectural best practices and verification

This is a source-alignment control, not a cryptographically signed manifest, trust anchor, execution result, approval or entitlement check. Formula-like capability text is refused rather than merely escaped. The canonical labels were derived from the current public source module table (45 unique module codes), avoiding private-source redistribution.

Four-viewport Chromium regression `tests/ki-matrix-intake.cjs` exercises original 180-case CSV round-trip, 1-module filtered export, BOM, forged IDs, modified negative-test procedures, altered healthy result, formula injection, swapped capability label, whitespace tampering, malformed CSV, receipt HOLD and browser network isolation at 390/768/1024/1440px.

**Implementation commits:** [canonical label validation](https://github.com/emilebennetts-cmd/servicenow-portfolio/commit/725656b2edaa61342add0d3f9395c3eec6a1df2c), [negative browser tests](https://github.com/emilebennetts-cmd/servicenow-portfolio/commit/75e1ecdd9b3d5f599bc9f3e715d1f9f6453c82d1).

**Release rule:** GitHub Actions status must be confirmed separately for the latest functional code and final documentation head. In-progress checks are not PASS.

**Licensing:** Static page requires no ServiceNow licence. Native KI collectors require appropriate target rights for App Engine/custom tables, scope and ACLs, and the actual subscribed ServiceNow products whose data they access (ITSM, CMDB, ITOM, ITAM, SecOps, IRM, HRSD, CSM, SPM, Knowledge and others as applicable). IntegrationHub, ATF, AI and external knowledge-content entitlements are conditional.

**Unmet:** fresh independently witnessed DEV acceptance; production read-back; verified customer entitlements; independently validated original screenshots and publication authorisations (**0 approved, HOLD**). Private repositories and confidential material remain unpublished.

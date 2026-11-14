# Knowledge Intelligence intake — baseline integrity and negative-test safety

**Date:** 15 November 2026 (Australia/Sydney)  
**Public entry:** https://emilebennetts-cmd.github.io/servicenow-portfolio/ki-matrix-intake.html  
**Evidence:** SOURCE-ONLY catalogue; PROPOSED matrix; MOCK-ONLY structural checker. **NOT RUN / HOLD.**

## 1. The client's pain and history

The 180-case Knowledge Intelligence acceptance CSV is intended as a portable, non-certifying handoff. An inspection of the existing offline intake checker found that its supposed case-ID comparison did not compare the candidate ID at all: it assigned the result of a boolean equality test to `suffix`, then tested `!suffix`. A forged but non-empty, unique case ID could therefore be accepted as structurally aligned. In addition, an operator could modify a negative-test instruction or expected outcome without a corresponding baseline comparison, potentially removing the instruction never to delete real ServiceNow tables.

This is a defect in the **public portfolio's browser intake validator**, not a claim about the native ServiceNow Knowledge Intelligence package.

## 2. The ServiceNow-oriented solution

- Correctly construct the deterministic canonical ID `KI-{module_code}-{RUN|TABLE|FIELD|LINT}` and compare it **directly** with the incoming `test_id`, rejecting mismatches.
- Mirror the four published exporter procedures' exact preconditions, instructions and expected outcomes in the intake contract; reject changed baseline text. The contract was reconciled against the current public test matrix generator, including the isolated test-double instructions for missing tables, missing fields and read-only lint.
- Hold blank capability labels. Retain existing source-domain/table checks, four-case module completeness, row-count limit, non-certifying status flags, duplicate detection and malformed CSV quarantine.
- Update the synthetic built-in example to conform to the same procedure checks instead of bypassing them.
- Add structured, explicitly non-certifying receipt fields `exact_case_id_check`, `baseline_procedure_check` and `cryptographic_authenticity_verified: false`. The receipt carries no imported evidence or identifiers.

## 3. Architectural best practices and verification boundaries

The checker is a static, offline browser utility. No credentials, instance API requests, uploads, customer records or browser persistence are involved. A successful check confirms **only selected structural and prescribed-procedure fields**, not authenticity, completeness of manually editable capability descriptions, native test execution, entitlement possession, approved findings, or release authority.

Regression coverage in `tests/ki-matrix-intake.cjs` was extended to include:
- A unique forged RUN identifier that previously escaped detection.
- A TABLE scenario rewritten to remove the instruction not to delete real tables.
- An expected `table_unavailable` response rewritten to imply a healthy score.
- Existing full 180-case export/import, UTF-8 BOM, filtered coverage, changed flags, duplicates, malformed CSV, HOLD-only receipts, no network requests, and 390/768/1024/1440px viewports.

**GitHub implementation:**
- [Intake control fix](https://github.com/emilebennetts-cmd/servicenow-portfolio/commit/e9ca1bdd2bc6ed71d3856d9f63ed839cc6094a92).
- [Negative-test regressions](https://github.com/emilebennetts-cmd/servicenow-portfolio/commit/5b413b634f73186844c4f8a9b2e4ed7dcbb091a1).

**Verification requires checking GitHub Actions on the final documentation head.** Do not treat source-only or browser CI as DEV-VERIFIED or PRODUCTION-VERIFIED. Original screenshot publication approvals remain zero — HOLD. Private code and original imagery are not included.

**Licensing / entitlement boundary:** No ServiceNow subscription is required for this public static utility. Execution of the proposed native tests requires approved App Engine/custom-table rights where used, scope privileges/ACLs, relevant subscribed ITSM, ITOM, CMDB, SecOps, ITAM, HRSD, CSM, IRM, SPM and knowledge capabilities; IntegrationHub, ATF, AI and third-party entitlements are separately conditional. Target release and instance ownership must be independently confirmed.

**Remaining gates:** witnessed read-only DEV execution, separate production acceptance, contract-specific entitlements, technical sign-off, and individual sanitised screenshot publication approval.

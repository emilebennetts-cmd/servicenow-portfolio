# Knowledge Intelligence acceptance matrix intake gate

**Date:** 15 November 2026 (Australia/Sydney)  
**Public URL:** https://emilebennetts-cmd.github.io/servicenow-portfolio/ki-matrix-intake.html  
**Classification:** SOURCE-ONLY source taxonomy; PROPOSED test plans; MOCK-ONLY local review interface. **NOT RUN / HOLD** throughout. No independently DEV-VERIFIED or PRODUCTION-VERIFIED result.

## 1. The client's pain and history

Technical teams exchange acceptance CSVs between consultants, architects and reviewers. A filtered subset may be mistaken for the complete plan, IDs may be duplicated, or execution flags may be edited without authorised native acceptance. The prior public Knowledge Intelligence page generated 180 planned test rows but did not read them back to identify these structural problems.

## 2. Implemented ServiceNow-oriented handoff

Added `ki-matrix-intake.html`, a mobile-friendly offline intake validator. The page accepts only local CSV files up to 256 KB, validates the exact 19-column header, recognises the 45 source-defined module codes and their domain/table mappings, checks four required scenarios per represented module (RUN/TABLE/FIELD/LINT), detects duplicate or unknown IDs, and checks the baseline source classifications, NOT RUN status, HOLD approval, false DEV/Production flags and blank evidence references. It accepts the complete plan and intentionally filtered four-case module subsets.

Reviewers see domain coverage, omitted modules and structural exceptions. A downloadable JSON receipt contains only counts and non-certifying status, with no original CSV rows, instance details, customer content or evidence. A built-in synthetic example demonstrates one module without implying full coverage. All local file processing uses browser File APIs; no external fetch, storage, upload or ServiceNow access is implemented.

**Boundary:** This is a *structural*, not cryptographic, validator. It does not authenticate the file's author or validate runtime artefacts. Passing does not establish that test instructions are correct, that the ServiceNow instance is configured, or that any execution occurred. Do not import actual client information or proprietary scripts.

Navigation added from the original `knowledge-intelligence-acceptance-matrix.html`, the public homepage, Portfolio Explorer and sitemap. The 90 registered public evidence claims are not altered or promoted.

## 3. Architectural best practices and verification

Reviewed the committed private Diagnostic Workbench 2 `knowledge-intelligence/README.md` and `knowledge-intelligence/docs/VERIFY.md`, which identify 16 source tables, 45 collectors and a 30 September 2026 historical DEV installation/lint report **without independently reproducing it**. Reviewed the connected Universal Delivery Workbench 4.22.2 As-Built: source release and date-bound DEV read-back are distinct; this KI page does not claim a new deployment. Original evidence images and private source were not published.

Added `tests/ki-matrix-intake.cjs` and `.github/workflows/ki-matrix-intake-browser.yml` to exercise 390/768/1024/1440 px Chromium widths, original 180-case download and re-import, filtered subset, duplicate test IDs, tampered runtime flags, malformed CSV, JSON HOLD receipt, network isolation and horizontal overflow. **Workflow run result must be independently checked; presence of test source is not proof it passed.**

### Entitlement requirements

Public static HTML, CSV import and JSON structural receipt: **no ServiceNow licence**. Native verification of Knowledge Intelligence collectors requires authorised non-production access, scope/custom-table and App Engine rights as contracted, `ki_user`/`ki_admin` and least-privilege table ACLs, and the relevant underlying ITSM, CMDB/ITOM/Discovery, ITAM, SecOps, IRM, HRSD, CSM, SPM, WSD or other product rights. Optional IntegrationHub, AI, ATF and third-party knowledge licensing require independent checks.

### Outstanding release gates

- Confirm GitHub Actions browser regression and deployment results against the final public commit.
- Reproduce KI installation and collector behaviour on the current authorised DEV/PDI release with native test evidence.
- Verify customer-specific licensing, target schemas, roles and access, including known schema-sensitive collector fields.
- Independently review test evidence and production change/acceptance; neither is represented as complete.
- Review and permanently sanitise each genuine ServiceNow screenshot, followed by individual publication authorisation. Current approval count: **zero (HOLD)**.
- Independently confirm external GitHub Pages HTTPS reachability.

**Publication control:** The three scoped source/control repositories remain private. No change to repository visibility, proprietary code, customer data, secrets or unreviewed screenshots. No promotion of SOURCE-ONLY, MOCK-ONLY or historical DEV-REPORTED evidence.

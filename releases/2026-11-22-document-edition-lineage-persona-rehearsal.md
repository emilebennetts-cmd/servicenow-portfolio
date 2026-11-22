# Documentation edition lineage and persona rehearsal — 22 November 2026

**Release classification:** SOURCE-ONLY public implementation · MOCK-ONLY browser rehearsal · historical DEV-REPORTED context · native DEV **NOT RUN** · Production **NOT RUN** · original screenshot publication **HOLD**.

## 1. The client's pain & history
Different controlled file formats in the same Drive library share document titles but not baseline versions. Direct inspection confirmed the **30 September 2026 PDFs** for Delivery Solution As-Built and User Guides & Training each reference source **4.6.1**, while **19 October 2026 DOCX** versions of those two guides and Delivery Architecture reference source **4.22.2**. The prior public four-document matrix omitted the October editions of As-Built and Training, creating an incomplete edition inventory. The Diagnostic completion runbook is expressly fictional.

## 2. The ServiceNow solution
- Expanded the crosswalk from four family summaries to **six controlled editions**: two September PDFs, three October DOCX documents, and one unversioned fictional runbook.
- Preserved both editions of identically titled documents as separate records with distinct IDs, format, cutoff, version and required next evidence.
- Added a **five-persona training rehearsal** for presales/account, delivery lead, architect, test/release lead and platform owner. The interactive card shows focus, proof and target edition; it never stores actual execution or approval.
- Expanded CSV to six HOLD-only review rows, now including edition and format. All rows retain **NOT RUN / HOLD**; matching a source document does not certify DEV.
- Hardened this public page with restrictive CSP and same-origin-only assets. Updated the Evidence Library and browser regression checks.

## 3. Architectural best practices and acceptance
OOTB-first controls: exact scoped application identity, role-appropriate ACLs, segregation of duties, version-bound training material, independent test result and approved release change. Separate **source edition**, historical read-back and **current native verification**. Do not infer a current application install, UAT, customer entitlement, screenshot approval or Production deployment from Drive files or source CI.

Automated acceptance expectations: six unique editions; October target 3 matches, 2 drifts, 1 fictional; September target 2 matches, 3 drifts, 1 fictional; five persona cards always NOT RUN/HOLD; CSV six records and 11 columns; four-width browser test; no off-origin network requests. CI outcomes must be confirmed separately.

**Licensing / entitlements:** Static site and local demonstration require no ServiceNow subscription. Authorised native Workbench testing requires valid custom scoped-app rights, ACLs/roles and instance consent. Confirm target-specific ITSM/CMDB, ITOM/Discovery, IntegrationHub/spokes, ATF, Performance Analytics, AI, SecOps, IRM, CSM, HRSD and ITAM entitlements where a test invokes them.

## Controlled evidence policy
The source PDF/DOCX files were read via the connected private Drive account; no originals, links, screenshot bytes, customer records or private source code were copied into the public repository. All screenshot publication remains blocked pending image-specific permission, final redaction review and independent acceptance. The **date in each document** is the evidence cutoff, not proof of today's runtime state.

# CSDM 5 Native Acceptance Desk — preparation, not attestation

**Date:** 15 November 2026 (Sydney).  
**Public experience:** [CSDM 5 Native Acceptance Desk](../csdm-native-acceptance.html).  
**Evidence classification:** SOURCE-INFORMED architecture and MOCK-ONLY interactive review. No new DEV-VERIFIED or PRODUCTION-VERIFIED claim.

## 1. The client's pain & history
A representative enterprise CMDB may have service records without accountable owners, weak CI identifiers across discovery sources, and portfolio offerings that cannot be joined to independently confirmed operational dependencies. Static architecture pictures alone cannot resolve these governance gaps. The three cases in this release are fictional and do not assert customer outcomes.

## 2. The ServiceNow solution
Created a standalone, mobile-first browser-only CSDM 5 Native Acceptance Desk, linked from the [CMDB / IRE deep dive](../cmdb-ire-assurance.html#csdm-ownership) and homepage. It provides three synthetic investigations (ownership, IRE identity, and service offering) and six acceptance preparation gates (class/release metadata; IRE precedence; owner attestation; relationship provenance; bounded CMDB Health; and change/rollback/rescan). OOTB-first remediation routes refer to CSDM, CI Class Manager, IRE, CMDB Health and Service Portfolio Management. The reviewer may label a gate not assessed, evidence requested, gap, or materials staged; per-scenario states are maintained only in memory.

The **Export draft (JSON)** function writes a portable, non-certifying preparation record containing six fixed gate IDs and immutable MOCK-ONLY, NOT RUN, NOT VERIFIED, UNREVIEWED, HOLD and false approval / production-verification flags. Export is client-side only, with no external requests, upload, storage or native ServiceNow access. Reset is scoped to the selected scenario.

## 3. Architectural best practices, verification and licensing
- Public assets: csdm-native-acceptance.html and csdm-native-acceptance.js, with explicit CSP (connect-src none, img-src none, no embedded media).
- Publication contract: scripts/test_csdm_native_acceptance_desk.py; browser functional/accessibility regression: scripts/browser_csdm_native_acceptance_desk.py at 390, 768, 1024 and 1440 pixels via the [dedicated workflow](../.github/workflows/csdm-native-acceptance-browser.yml). These test website behaviour only.
- Navigation and provenance: homepage, CMDB deep dive, Portfolio Explorer, sitemap and authoritative public verification register updated in step with the new page. One explicit MOCK-ONLY claim was added; no existing historical DEV report was upgraded.
- Sources inspected: controlled Universal Delivery Workbench Architecture and User Guides and Training, private Delivery 4.22.2 README, private Diagnostic Workbench 2 README and a previously completed synthetic Diagnostic runbook. The documents remain restricted and are **not** reproduced, linked, or treated as independently verified current native execution.
- Acceptance still required: authorised target-version DEV testing and read-back, IRE preview/fixtures, valid ownership attestation, ACL and performance checks, ServiceNow build/change approval, independently reviewed receipts, and Production-specific authorisation. No current native execution was performed.
- Licensing: the static page and JSON export require **no ServiceNow licence**. Native work may require contract-specific CMDB/IRE and Health rights, Service Portfolio Management, ITOM Discovery/Service Mapping, Service Graph Connector/IntegrationHub, App Engine custom tables, ATF, appropriate user roles and third-party subscription rights. This artefact does not verify entitlement.
- Original ServiceNow screenshots: **zero approved, publication HOLD**. No image pixels, confidential code, customer records, secrets or private repository links were published.

**Status note:** CI and Pages deployment success should be confirmed against the final repository head after all documentation changes. Automated green checks are not DEV/Production certification.

# CMDB source-onboarding design and IRE acceptance lab

**Date:** 12 November 2026  
**Public release classification:** SOURCE-ONLY implementation / MOCK-ONLY synthetic scenarios  
**Production and new DEV verification:** Not established

## 1. Client pain and history

This is a representative enterprise situation, not a description of an identified customer. Several authoritative and non-authoritative feeds can supply overlapping host, endpoint or cloud-CI data; an import count is not proof of correct identification, attribute reconciliation or business ownership. Conflicting identifiers, uncontrolled field updates and unsupported conclusions from incomplete assessments create a need for a repeatable onboarding and acceptance design.

## 2. Implemented ServiceNow-oriented demonstrator

Added [CMDB Source Onboarding Lab](../cmdb-source-onboarding-lab.html), a responsive, self-contained static page with:

- Three labelled synthetic scenarios: stable server identity, ambiguous/reused hostname, and identified endpoint with unresolved attribute ownership.
- Six consultant review controls (class, identification, reconciliation, security, native tests, operational governance).
- Blocking input conditions that remain blocked even when a visitor selects all six controls.
- An accessible live status and missing-controls summary, scenario isolation/reset and a downloadable structured JSON receipt.
- Explicit negative evidence fields: servicenow_dev_verified = false, production_verified = false, approval_granted = false, actual_ire_response = null.
- Restrictive CSP; no file upload, remote calls, persistent browser storage or genuine images.
- Native acceptance matrix for positive/negative IRE payload tests, source-precedence conflict, refresh and null rules, denied-write access, CMDB Health and rollback.

**Important:** the application does not implement ServiceNow's IRE algorithm, run native Identification Simulation or calculate actual CI matches. A complete synthetic checklist only reaches READY_FOR_NATIVE_SIMULATION_NOT_APPROVED.

The homepage directory, CMDB case-study pathway and sitemap now link to this page. The public evidence ledger includes the new MOCK-ONLY claim, preserving separate runtime boundaries.

## 3. Architectural best practices, proof and dependencies

Use ServiceNow's supported identification/reconciliation, data source and dependent-identification rules, with target-release simulation and bounded load tests. Static and dynamic attribute reconciliation, source precedence, freshness and null rules require independent verification in an authorised non-production instance. A synthetically modelled source conflict is **not** a native IRE response.

**Repository source reviewed:** current private solution-lifecycle-studio documentation, Diagnostic-Workbench2 portfolio source, the prior private CMDB source-review release record and public cmdb-ire-assurance.html. Connected Google Drive was searched for the previously completed Universal Delivery Workbench As-Built and Diagnostic materials; these files were not republished or claimed as an IRE test. Public official Australia-release references:
- https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/configuring-ire.html
- https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/create-reconciliation-rule.html
- https://www.servicenow.com/docs/r/api-reference/rest-apis/c_IdentifyReconcileAPI.html

**Verification:** static contract regression in scripts/test_cmdb_source_onboarding_lab.py; responsive Chromium interaction assertions in scripts/browser_navigation_smoke.py at 390, 768, 1024 and 1440 px. Do not claim CI success until GitHub workflows for the release commit have returned completed/success.

**Evidence boundaries:** SOURCE-ONLY public implementation; MOCK-ONLY data and exported receipts; historical DEV source reports do not verify this new lab; new DEV-VERIFIED = none; PRODUCTION-VERIFIED = none. Original Workbench screenshots remain on HOLD (zero publicly approved).

**Entitlements:** the public lab requires no ServiceNow licence. Live CMDB/IRE operations require authorised access and applicable ServiceNow rights. Discovery, Service Graph Connectors, CMDB 360, ITOM Visibility, IntegrationHub spokes, analytics and external provider APIs may require separate licensing or subscriptions depending on the installed release and contractual entitlement.

## Outstanding controlled gates

1. Capture real target-run IRE simulation results from an authorised instance and independently confirm class, identification and reconciliation conditions.
2. Complete ACL/negative, volume, null/freshness, rollback and acceptance evidence before a DEV-VERIFIED label.
3. Obtain separate production authorisation before any production claims.
4. Retain original Workbench screenshots privately until image-specific rights, sanitisation, reviewer approval and provenance checks are complete.

## Verified CI receipt (final implementation head)

- Implementation and release-log head c0c19eed3b137340e13562afa278f4910347cffc: [Portfolio quality gate](https://github.com/emilebennetts-cmd/servicenow-portfolio/actions/runs/43148825572) completed/success; [quality audit](https://github.com/emilebennetts-cmd/servicenow-portfolio/actions/runs/43148825556) completed/success; [GitHub Pages](https://github.com/emilebennetts-cmd/servicenow-portfolio/actions/runs/43148825553) completed/success.
- Functional browser-test commit aa28f1f3df554739b3c919afe3a0c5a679c1b55a: [Chromium four-viewport run](https://github.com/emilebennetts-cmd/servicenow-portfolio/actions/runs/43148593813) completed/success including case switch reset, six review controls, blocked identity/authority conditions, receipt JSON export and viewport overflow checks. Later public commits only changed documentation and release notes.
- Independent external HTTP reading of the GitHub Pages URL was not available via the web reader; this does not negate the successful GitHub deployment workflow. No ServiceNow DEV or production execution occurred.

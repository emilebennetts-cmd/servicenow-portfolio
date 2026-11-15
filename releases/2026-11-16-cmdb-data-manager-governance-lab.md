# 2026-11-16 — CMDB Data Manager lifecycle governance lab

## 1. The client's pain & history
A fictional multi-source CMDB has stale server CIs, ambiguous ownership, service relationship dependencies and retention obligations. Spreadsheet-driven cleanup cannot reliably establish which CIs are safe to retire, archive, delete or attest. No customer incident, audit outcome or numerical saving is asserted.

## 2. ServiceNow solution implemented (public source only)
- Published [CMDB Data Manager governance lab](../cmdb-data-manager-governance-lab.html): responsive standalone HTML with accessible policy selection, four synthetic fixtures and a CSS-only **illustrative** policy console (not a native ServiceNow screenshot).
- Added the dependency-free [policy model](../cmdb-data-manager-policy-model.js) with conditional blockers for active class retirement definitions, retired state, legal hold, ownership, exclusion, dependent CIs, positive archive retention and source re-ingestion.
- Readiness is HOLD for retire (re-ingestion risk), delete (legal hold), attest (missing owner) and REVIEW REQUIRED for the archive example. REVIEW REQUIRED never means authorisation or native acceptance.
- Added 20 scenario-specific native DEV controls (5 each). Browser CSV exports for a selected policy or all 20 always use **NOT RUN / HOLD / MOCK-ONLY** and leave instance, version, executor, timestamp, private evidence and reviewer blank.
- No user-supplied data, credentials, API calls, native CI writes, client screenshots or browser persistence.
- Integrated page into homepage directory, Explorer, sitemap and classification register; added [Node regressions](../tests/cmdb_data_manager_policy.test.cjs) to CI.

## 3. Architecture and standards
Use OOTB CMDB Data Manager life-cycle policies, Workspace, active retirement definitions, task/approval separation, class-specific exclusions and dependent-CI controls. Native preview, negative-persona ACL testing, stale discovery-source assessment, retention authority, records-hold review and independent reconciliation are mandatory before activating a policy.

Official ServiceNow Australia-release sources verified **16 November 2026**:
- [Create Data Manager policy](https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/data-manager-create-policy-wrkspc.html) — updated 12 March 2026, retirement definition prerequisites, exclusion/target preview and 10,000-target task batching.
- [Retirement definitions](https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/data-manager-manage-ret-def-wrkspc.html) — class-based active definitions and administrative roles.
- [Dependent CI management](https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/manage-dependent-ci.html) — orphan prevention and exception handling.
- [CMDB Data Manager](https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/cmdb-data-management.html) — retire/archive/delete/attestation/certification concepts and approval paths.

## Evidence boundaries and provenance
- Reviewed private Delivery source README (declared 4.22.2) and Diagnostic Workbench README; neither establishes new current runtime state.
- Reviewed controlled Google Drive **01-Universal-Delivery-Workbench-Solution-As-Built.pdf**, revision 1.0, 30 September 2026: source 4.6.1, historical DEV 4.5.1, document not approved. Unrelated to current Data Manager native acceptance.
- Lab implementation: **SOURCE-ONLY**; interactions and scenarios: **MOCK-ONLY**. Historical Delivery observations: **DEV-REPORTED** and dated.
- Current Data Manager policy native execution: **0/20 NOT RUN / HOLD**; newly **DEV-VERIFIED 0**, **PRODUCTION-VERIFIED 0**.
- Genuine screenshots approved: **0 / HOLD**. Only CSS illustrations; no private images or sensitive source are published.

## Quality gate
Test suite asserts 20 unique control IDs, five controls per scenario, blockers, unapproved readiness states, immutable native statuses and blank private evidence fields. CI is configured to run it, but CI and deployment must be checked separately; source commit alone is not a passing CI receipt.

## Licensing/entitlements
The public static lab has no ServiceNow licensing requirement. Native CMDB Data Manager use requires appropriate installed platform/Workspace capabilities, authorised administration and policy roles (including documented sn_cmdb_admin and Data Manager roles) and entitlement checks on the target contract. Discovery/ITOM Visibility, Service Graph Connectors, CMDB 360, IntegrationHub, ATF, analytics and AI can require distinct licences, activation and privileges.

## Blockers / next release
Authorised instance/scope and version read-back, native synthetic policy preview, class retirement definition inspection, negative-role acceptance, dependency/restore behaviour, signed records-management approval, independent reviewer signoff and explicit per-image screenshot clearance. No production deployment or policy activation attempted.

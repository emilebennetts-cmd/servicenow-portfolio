# Change Management implementation rehearsal — 15 November 2026

## 1. The client's pain & history
A customer-neutral example describes the risk of treating Normal, Standard and Emergency changes as interchangeable: excessive CAB friction for standard work, incomplete emergency authorisation, weak CI/service impact and missing implementation/rollback evidence. No real customer problem or measured uplift is asserted.

## 2. The ServiceNow solution delivered in this public release
- Added `change-management-implementation-lab.html`, an independently authored, responsive Change Management case study.
- Implemented three separately navigable, OOTB-first synthetic models: **Normal**, **Standard** and **Emergency**, each with **seven** unique design/acceptance review controls (21 total).
- Selector resets reading marks to prevent accidental cross-model completion; reviewers can clear marks explicitly.
- Implemented browser-local CSV acceptance export with formula-prefix protection. Every row is **NOT RUN / HOLD / MOCK-ONLY** regardless of reading state.
- Added a three-layer evidence matrix and explicit source, DEV, release and Production acceptance boundaries.
- Added `tests/test_change_management_lab.py` for structural regression, evidence fail-closed controls, offline operation, responsive affordances and entitlements.
- Indexed the new route in `sitemap.xml`, `portfolio-explorer.html` and the homepage. Registered `CHANGE-MANAGEMENT-LAB` in `evidence/public-verification-register.json`.

### Reference basis and limits
The restricted `solution-lifecycle-studio` README documents source-defined Normal and Emergency change exemplars, platform-managed approvals and independent evidence review, but does not establish current native execution of this public feature. The September 2026 controlled Universal Delivery Workbench As-Built is a historical draft with an explicitly older DEV baseline. The Diagnostic Workbench 2 documentation was reviewed for read-only evidence and handover boundaries; it is not asserted to include a native Change Management workflow.

Public ServiceNow Australia-release documentation:
- [Change types](https://www.servicenow.com/docs/r/it-service-management/change-management/change-types.html)
- [Simplified Change Management](https://www.servicenow.com/docs/r/it-service-management/configuring-change-management-experience-in-it-service-management.html)
- [CSDM relationship mapping](https://www.servicenow.com/docs/r/it-service-management/change-management/itsm-change-use-case-product-view.html)
- [Create a change request / scheduling](https://www.servicenow.com/docs/r/it-service-management/change-management/t_CreateAChange.html)

The **classic** and **Simplified Change Management** models differ; approval and state policies must be read back from the selected target instance before a design is accepted.

## 3. Architectural best practices and verification
- Prefer native `change_request`, change models, standard template catalogue, approval policy, CAB, task records, risk and schedule/conflict facilities; avoid unnecessary customisation.
- Link `cmdb_ci`, `task_ci`, impacted services and `service_offering` where supported by the release and actual CSDM scope.
- Require role/ACL negative tests, separation of duties, emergency submitter restrictions, rollback tests, formal authorisation, record read-back and independent acceptance.
- This release is **MOCK-ONLY** for browser interactions, **SOURCE-ONLY** for documentation/implementation provenance. Existing historic DEV claims stay **DEV-REPORTED**.
- **No new DEV-VERIFIED or PRODUCTION-VERIFIED claim.** All 21 native acceptance tasks are **NOT RUN / HOLD**.
- Original genuine screenshots remain 0 approved; no image files, customer names, customer records, credentials or restricted source were added.
- Offline source and static tests are not browser integration or native ServiceNow acceptance. Final CI execution and external HTTPS retrieval must be recorded independently and must not be inferred from successful commits.

### Licensing and entitlement dependencies
The static web page, offline CSV and standard-library test require no ServiceNow licence. A target implementation requires the customer's ITSM/Change Management rights, licensed fulfiller access, roles/ACLs, selected change model configuration and approved instance access. CAB Workbench, IntegrationHub, Advanced Analytics/PA, ATF, Now Assist, ITOM/Discovery and external providers may have additional SKU, plugin and access dependencies; confirm the specific subscription before build or deployment.

## Release gates / unresolved
1. Obtain native non-production configuration and persona-test receipts for the actual installed change model.
2. Validate customer-specific approval policies, CAB/scheduling, CSDM data and operational ownership.
3. Secure change authority, production read-back, operational acceptance and per-image publication approvals before making stronger claims.

Public release contains no private repo paths beyond generic repository names and no original screenshot binary.

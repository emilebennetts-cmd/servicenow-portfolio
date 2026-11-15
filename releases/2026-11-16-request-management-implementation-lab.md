# Request Management implementation rehearsal — 16 November 2026

**Public capability: MOCK-ONLY interactive acceptance rehearsal. OOTB-first design informed by public ServiceNow Australia documentation (updated March 2026) and source review. No new native DEV or Production acceptance.**

## 1. The client's pain and history
Representative, fictional service operations relied on email requests, informal approvals, unlinked tasks and weak evidence trails. This is an illustrative consulting scenario, not a reported client incident.

## 2. The ServiceNow solution
A mobile-friendly Service Catalog case study presents the native catalog item / REQ / RITM / catalog task design, supported user criteria, conditional approval and Workflow Studio fulfilment. Three synthetic request examples (application access, hardware order, standard service) provide eight distinct test gates each (24 total). Buttons change the active scenario, checkboxes track reading only, and CSV export retains NOT RUN / HOLD / MOCK-ONLY for every row. No credentials, customer data, real record writes, uploads or browser persistence are involved.

Public documentation referenced:
- https://www.servicenow.com/docs/r/servicenow-platform/service-catalog/request-fulfillment.html
- https://www.servicenow.com/docs/r/build-workflows/workflow-studio/create-sc-flow.html
- https://www.servicenow.com/docs/r/build-workflows/workflow-studio/create-catalog-task-flow-designer.html
- https://www.servicenow.com/docs/r/servicenow-platform/service-catalog/c_LegcySrvcCatAccessCntrol.html

## 3. Architectural best practices
Use native Request Management records, user criteria for item eligibility, independently enforced ACLs for records, supported Service Catalog Flow triggers, accountable fulfilment ownership, negative-path impersonation and evidence-gated native promotion. Requirements differ by tenant and installed release.

### Verification and evidence
- Source/authoring: public HTML, browser-only JS and 24 synthetic controls. SOURCE-ONLY design, MOCK-ONLY page behaviour; tests cannot certify ServiceNow execution.
- Unit checks: Node contract tests for 24 unique test IDs, unknown input, fail-closed CSV and immutable acceptance states; Python static/privacy/accessibility tests.
- CI: workflow outcome must be checked against the precise commit; do not infer successful deployment until GitHub confirms it.
- Native DEV-VERIFIED added: **0**; PRODUCTION-VERIFIED added: **0**; original screenshots approved for publication: **0 / HOLD**.
- No private application source, confidential Drive documents, credentials, instance URLs, customer records or unapproved screenshots were copied.

### Entitlements and blockers
Static portfolio, local test logic and CSV: no ServiceNow licence. Native use requires applicable Service Catalog / Request Management subscription and assigned roles, Workflow Studio designer rights, licensed fulfiller access and verified tenant configuration. Separately confirm App Engine/custom table, HAM/SAM, IntegrationHub, ATF, analytics, AI and third-party subscriptions if used. Current native read-back, persona ACL acceptance, flow execution, production verification and screenshot-by-screenshot consent remain **blocked/not run**.

### Files
- request-management-implementation-lab.html
- request-management-implementation-lab.js
- tests/request_management_lab.test.cjs
- tests/test_request_management_lab.py
- evidence/public-verification-register.json (mock-only claim)
- homepage, explorer catalogue, sitemap, quality CI and release log

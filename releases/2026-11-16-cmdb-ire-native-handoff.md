# 2026-11-16 — CMDB source onboarding native IRE acceptance handoff

## 1. The client's pain & history
A multi-source CMDB can have technically successful imports and still create duplicate CIs or overwrite authoritative attributes. A source-onboarding design checklist alone is not an executable native test plan. The public onboarding lab previously exposed three synthetic design scenarios and a six-control JSON assessment, but lacked one portable, control-by-control handoff for authorised non-production IRE testing. No customer incident or production outcome is asserted.

## 2. The ServiceNow solution implemented
- Extended [the existing CMDB Source Onboarding Lab](../cmdb-source-onboarding-lab.html#native-handoff) with an accessible, responsive 18-case acceptance handoff.
- Created the offline, dependency-free [native acceptance model](../cmdb-source-acceptance.js): six concrete checks each for stable source identity, conflicting/reused hostnames, and attribute-authority conflicts.
- Added full 18-case and selected six-case CSV exports, safe for preparing privately executed DEV sessions.
- Every exported row is immutable **NOT RUN / HOLD / MOCK-ONLY**; instance, installed-scope version, executor, timestamp, evidence reference and reviewer remain empty. No CI IDs, credentials, customer data, network access or ServiceNow write functions are included.
- Retained original six-control design JSON export and made no change to native applications.
- Added Node regression suite and mandatory GitHub Actions quality gate.

## 3. Architectural best practices
Use OOTB Identification and Reconciliation Engine, supported ingestion APIs, dependent identification, class/attribute precedence and native data-source insert restrictions. The exported cases explicitly require actual rule traces, ACL denial tests, replay/idempotency, source-priority and null/refresh outcomes, and independent read-back in an authorised non-production environment. A browser report never grants release approval.

This source-informed lab is a *planning artefact*, not an IRE simulator and not a replacement for the installed CI schema, class rules or customer's governance process.

## Source/provenance boundary
- [Delivery Workbench source README](https://github.com/emilebennetts-cmd/solution-lifecycle-studio/blob/main/README.md): source version 4.22.2; historical DEV baselines explicitly distinct.
- [Diagnostic Workbench source README](https://github.com/emilebennetts-cmd/Diagnostic-Workbench2/blob/main/README.md): repository source and local test/build procedures, not proof of current production installation.
- Controlled Google Drive **01-Universal-Delivery-Workbench-Solution-As-Built.pdf**, revision 1.0, 30 September 2026: source 4.6.1 versus observed DEV 4.5.1. This is a historical controlled draft; no private content was published.
- All new scenarios and exports: **MOCK-ONLY**. New HTML/JS and test source: **SOURCE-ONLY**. Previously reported historical DEV observations: **DEV-REPORTED** (dated only). New **DEV-VERIFIED: 0** and **PRODUCTION-VERIFIED: 0**. Native tests executed: **0/18**. Screenshot approvals: **0 / HOLD**.

## Public verification
Node regression covers 18 unique IDs, six cases per path, immutable statuses and blank private fields, CSV structure, and mandatory offline disclosures. GitHub Actions workflow wired to run these tests; do not mark CI as passed until a successful run is independently observed. No external HTTPS delivery claim is made by this release document.

## Licensing / entitlement dependency
Static HTML, JS and CSV generation require no ServiceNow licence. Native IRE/configuration access requires target-platform roles and applicable CMDB feature entitlement; Service Graph Connectors, Discovery/ITOM Visibility, IntegrationHub, CMDB 360, Data Manager, ATF and external provider access can have additional activation, subscription, plugin, role or contract requirements. Confirm the contracted edition and tested instance before use.

## Remaining release gates
Authorised DEV environment/scope and version read-back; synthetic native execution of 18 checks; negative-persona ACL and source restrictions; signed stewardship/release decision; publication approval of individual customer-neutral screenshots. No private repository visibility change and no original screenshots published.

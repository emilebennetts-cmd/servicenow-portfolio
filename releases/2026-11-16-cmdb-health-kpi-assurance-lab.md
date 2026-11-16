# CMDB Health KPI Assurance Lab — 16 November 2026

## Scope and client scenario
Published an accessible, mobile-responsive, offline CMDB Health KPI Assurance Lab for a **fictional** legacy estate. The four governed investigations cover: disabled Completeness calculation, Correctness/IRE identity conflicts, Compliance scope drift, and Relationship-health coverage. Sample CI populations and percentages are synthetic UI illustrations, not native algorithm output or customer results.

## Source and architectural boundaries
- ServiceNow CMDB Health documentation: https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/overview-cmdb-health.html
- Health scheduled calculation configuration: https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/t_EnableCMDBHealthDashboardJob.html
- KPI definitions: https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/r_CMDBHealthMetrics.html
- Delivery repository README declares v4.22.2 source with a separately dated v4.20.0 pre-release DEV baseline; Diagnostic repository is a separate source provenance stream. These are **not** CMDB Health DEV acceptance evidence.
- The controlled Universal Delivery Workbench As-Built dated **30 September 2026** describes v4.6.1 source / v4.5.1 DEV and is a controlled draft, not a production sign-off. No material or screenshot from that restricted file was republished.

## Implementation
- `cmdb-health-assurance-lab.html`: static, mobile-responsive case study and accessible CSS-only illustrative console; explicit MOCK-ONLY captions, no original screenshots, no API requests.
- `cmdb-health-assurance-model.js`: four deterministic synthetic investigations, 24 unique native DEV acceptance checks; six per scenario.
- `tests/cmdb_health_assurance.test.cjs`: regression contract for immutable test status, missing evidence fields and complete scenario coverage.
- Navigation, evidence-aware Explorer index and sitemap integrated as separate commits.

## Acceptance classification
| Layer | Evidence class | Actual state |
| --- | --- | --- |
| Committed website, model and test source | SOURCE-ONLY | Implemented in GitHub |
| CSS console, synthetic numbers, CSV preparation | MOCK-ONLY | Offline simulation |
| Historical Workbench PDI read-back | DEV-REPORTED | Date/version bounded; unrelated to this lab |
| New CMDB Health native acceptance | DEV-VERIFIED | **0 / NOT RUN** |
| Production | PRODUCTION-VERIFIED | **0 / NOT RUN** |
| Original ServiceNow screenshots | Publication gate | **0 approved / HOLD** |

All 24 CSV rows intentionally contain `NOT RUN / HOLD / MOCK-ONLY`. Private instance, build, persona, time, receipt and reviewer columns are blank. No native writes, live credentials, customer data, repository visibility changes or original screenshot publication.

## Installation and licensing dependencies
Public static site needs no ServiceNow licence. Native job configuration requires `sn_cmdb_admin` or admin and relevant CMDB Health capability in the target release. Check feature/role entitlement for CMDB Workspace, Discovery/ITOM Visibility, Service Graph Connector, CMDB 360, IntegrationHub, ATF, Performance Analytics and AI separately where selected. Native execution remains blocked pending current DEV read-back, permissioned tester and independent reviewer.

## Release QA
Source and test commits are linked in GitHub history. CI/deployment outcomes are to be recorded after workflow completion, not inferred from a successful commit.

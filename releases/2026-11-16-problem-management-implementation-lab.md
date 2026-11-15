# 2026-11-16 · Problem Management OOTB-first acceptance lab

## Client's pain and history
A **fictional** organisation repeatedly restores service but does not govern investigation across incidents, CI context, RCA, known errors and changes. The story does not assert any real customer outcome.

## ServiceNow solution implemented in public portfolio
- Added a responsive offline HTML case study plus standalone JavaScript scenario model.
- Three synthetic user journeys: recurring incidents/Problem Tasks, workaround and known-error integration, permanent fix via Change and risk/reanalysis routes.
- Eight distinct acceptance controls per journey, 24 total. Each has expected native test and persona. Accessible selectors retain per-journey design reading marks only in current page memory.
- Exports eight or all 24 controls as CSV with fixed **NOT RUN / HOLD / MOCK-ONLY** native status and six blank private receipt columns. No browser storage, network requests, credentials, production data or ServiceNow script execution.
- Homepage, searchable explorer, deterministic sitemap, public evidence register, automated Node/Python regression suite and quality workflow updated.
- Illustration is authored HTML, **not** a screenshot from a running instance.

## Architectural best practices
- Native Problem/related Incident/Problem Task/Change/Knowledge before custom tables.
- Discover target instance Problem state model and version/migration history first; the older/newer state behaviour differs.
- Known error article integration/Primary Known Error reference is prerequisite-dependent; test user criteria and direct-link denial.
- Distinguish workaround publication, formal risk acceptance, successful change implementation and demonstrated root-cause correction.
- CMDB/CSDM context must be independently validated; do not infer service impact from duplicate or poorly identified CIs.

## Evidence and native acceptance
Public code: **SOURCE-ONLY**. Browser scenario: **MOCK-ONLY**. Existing historical Workbench notes: **DEV-REPORTED**, date-bounded. New **DEV-VERIFIED 0**, **PRODUCTION-VERIFIED 0** and approved original screenshots **0 / HOLD**. The 24 gates cannot be marked passed by the interactive UI. Target DEV identity, subscriptions, persona tests, actual Problem/Task/Change/KB records and independent reviewer receipt remain required.

## Licensing
Static website/CSV: no ServiceNow licence. Native implementation: appropriate ITSM/Problem entitlement, fulfiller roles/ACLs and installed state-model capabilities. Additional Knowledge integration, Service Operations Workspace, ATF, analytics, Now Assist, IntegrationHub and CMDB/ITOM features depend on the specific subscription and activation state.

## Authoritative references
- https://www.servicenow.com/docs/r/it-service-management/problem-management/exploring-problem-management.html
- https://www.servicenow.com/docs/r/it-service-management/problem-management/create-problem-task.html
- https://www.servicenow.com/docs/r/it-service-management/problem-management/investigate-root-cause.html
- https://www.servicenow.com/docs/r/it-service-management/problem-management/problem-form.html

CI and deployment evidence are tracked separately. CI success never establishes native ServiceNow execution.

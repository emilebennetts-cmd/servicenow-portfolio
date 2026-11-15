# 2026-11-16 — Incident Management end-to-end implementation lab

## 1. The client's pain and history
A strictly **fictional** client receives service interruptions through disconnected phone, self-service and email channels. Tickets are misclassified as requests, priority is guessed instead of derived from installed impact/urgency lookup, on-hold reasons are uncontrolled, work notes are confused with public comments and resolution closes without recovery assurance. No real customer outcome is asserted.

## 2. The ServiceNow solution implemented
- New mobile-friendly, standalone HTML/CSS case study plus separate browser-local JavaScript model, integrated into the homepage and searchable public Explorer.
- Three synthetic operator journeys: intake/priority, restore/communicate, close/improve.
- Three accessible illustrative screen reconstructions with no images or ServiceNow captures.
- 24 unique native DEV acceptance controls (8 each), including data lookup, permissions, task SLA pause/resume, communications, state model and independent receipt.
- Scenario-specific and full CSV export, fixed **NOT RUN / HOLD / MOCK-ONLY** status and six blank private receipt columns, regardless of reading marks. No browser persistence, network calls, ServiceNow authentication, or customer data.
- Regression tests in Python and Node, quality workflow, sitemap, public verification register, explorer and release log updated.

## 3. Architectural best practices
Native Incident [incident] and standard task model first; qualify versus Catalog request, preserve native Problem, Change and Major Incident governance boundaries. Validate installed state model, priority data lookup, SLA schedules and pause policies before customisation. Never infer service impact from unreliable CMDB/CSDM identifiers. Positive and denied personas require direct-link ACL checks. Target-specific integrations, workspace modules and subscriptions are prerequisites, not promises.

## Verification classification
Authored public source: **SOURCE-ONLY**. UI and CSV rehearsal: **MOCK-ONLY**. Prior Workbench histories: **DEV-REPORTED**, dated. New **DEV-VERIFIED: 0**, **PRODUCTION-VERIFIED: 0**, native controls executed: **0/24**, and approved original screenshots: **0 / HOLD**. Current native version, entitlement, permissions, record read-back and independent reviewer evidence are still required. Passing browser CI is not native execution.

## Licensing
Static portfolio and CSV: no ServiceNow licence. Native Incident execution: applicable ITSM/fulfiller entitlements and authorised incident roles. Service Operations Workspace, Major Incident Management, ITOM/Event, IntegrationHub, ATF, Virtual Agent, Now Assist and analytics are separately contingent on instance activation and contract.

## Public source references (ServiceNow Australia)
- https://www.servicenow.com/docs/r/it-service-management/incident-management/incident-management-process.html
- https://www.servicenow.com/docs/r/it-service-management/incident-management/create-an-incident.html
- https://www.servicenow.com/docs/r/it-service-management/service-operations-workspace/create-incident-sow.html

Prior Delivery and Diagnostic repository material and accessible Google Drive As-Built document titles were reviewed for claim-boundary context; no private source or unapproved Drive screenshot was exported to public site.

## Public deployment delivery assurance
The anonymous GitHub Pages smoke workflow now includes the exact Incident Management HTML route (14 routes total) and compares deployed UTF-8 bytes to the checked-out source SHA-256. Its result is delivery evidence only, not native DEV or production execution. External browser access remains a separate observation.

## Browser acceptance
Four-viewport (390, 768, 1024, 1440 px) Chromium test added for scenario switching, independent reading marks, responsive overflow, mock screen transitions, eight- and 24-gate CSV export and immutable NOT RUN/HOLD statuses. This is browser acceptance of the public synthetic UI, not native ServiceNow testing.

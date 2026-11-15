# Request Management complete native acceptance handoff — 16 November 2026

**Classification:** SOURCE-ONLY portfolio code and MOCK-ONLY browser rehearsal. **Native DEV: NOT RUN. Production: NOT RUN. Original screenshots: 0 approved / HOLD.**

## 1. The client's pain & history

The previously released Request Management lab contained three end-to-end representative journeys, but exported a separate eight-gate checklist only for the selected scenario. A technical consultant preparing a single native DEV test cycle needed a consistent complete pack across application access, hardware ordering and standard service requests. Combining independent CSVs by hand created omission and review-handoff risk. This is a synthetic process problem, not an assertion of a customer defect.

## 2. The ServiceNow solution

Extended the existing mobile-friendly, browser-local Request Management lab with **Download complete 24-gate DEV handoff CSV (HOLD)**. The original eight-gate scenario export remains available. The new export:

- Includes all 24 fixed, uniquely identified controls (ACC-01–08, HW-01–08, SRV-01–08), independent of which scenario is selected.
- Carries optional *read in rehearsal* marks from all three tabs without treating them as successful test execution.
- Includes blank, private reviewer-entry columns for instance alias, installed build/version, executor role, execution date, evidence receipt alias and independent reviewer.
- Forces **NOT RUN**, **HOLD** and **MOCK-ONLY** in each of the 24 generated rows.
- Runs entirely in the browser using an in-memory CSV/Blob download. No API requests, credentials, local storage, telemetry or ServiceNow writes.

Native execution observations and immutable evidence should be maintained in a **private** test register and reviewed separately; editing a downloaded spreadsheet does not itself establish DEV-VERIFIED or PRODUCTION-VERIFIED status.

## 3. Architectural best practices

Use native Service Catalog, request and task records (`sc_cat_item`, `sc_request`, `sc_req_item`, `sc_task`) where appropriate; separate item eligibility/user criteria from record ACLs and preserve source-to-instance baseline identity. Test supported Workflow Studio fulfilment, approval decisions, negative personas, cancellation and duplicate-task recovery before claiming native readiness. No custom tables are necessary for this offline portfolio export.

The underlying solution-lifecycle and Diagnostic Workbench source repositories were reviewed as provenance only. The Universal Delivery Workbench Solution As-Built (source release 4.22.2, evidence cutoff 19 October 2026) records date-bounded historical DEV observations; none authorise a new 16 November native acceptance claim.

### Implementation

- `request-management-implementation-lab.js`: `allAcceptanceRows` and `allAcceptanceCsv` public, testable contracts, and the all-scenario download handler.
- `request-management-implementation-lab.html`: new keyboard-accessible download control and reviewer guidance.
- `tests/request_management_lab.test.cjs`: unique 24-ID, status, CSV column and blank receipt-field regressions.
- `tests/test_request_management_lab.py`: new privacy, usability and fail-closed static assertions.
- Existing page and homepage link are unchanged; no new route, screenshot or third-party asset was added.

### Validation and promotion criteria

Source fetched back from the committed repository. Local isolated JavaScript contract checks passed: 24 records, 24 distinct IDs, scoped reading flags, 25 CSV lines, 24 fixed NOT RUN/HOLD/MOCK-ONLY values, blank private fields and expected column headers. Static checks confirmed the new control, tests, privacy restrictions and 24 gate identifiers. **GitHub Actions results must be verified on the final commit before claiming CI success.** An automatic workflow success does not establish ServiceNow native execution.

**Blocked:** authenticated target DEV app/version/scope read-back, real REQ/RITM/task and Workflow Studio execution, authorised positive and negative personas, independent review, licence verification and screenshot-by-screenshot publication consent. Do not copy real evidence or instance details into this public repository.

### Licensing and entitlements

This public static export needs **no ServiceNow licence**. The native scenario requires relevant Service Catalog/Request Management rights, fulfiller roles and Workflow Studio designer access. Assess ITSM tier, App Engine/custom-table, HAM/SAM, IntegrationHub, ATF, analytics, Now Assist/AI and third-party entitlements against the actual tenant only if those capabilities are in scope.

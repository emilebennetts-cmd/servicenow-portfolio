# Interactive governed Delivery Plan case study — 13 November 2026

## Client pain & history
Representative, client-neutral problem: discovery notes, requirements, pattern selections, phase gates, build specifications and support handover are commonly fragmented. Traceability and approval boundaries become difficult to inspect. This is a general architectural motivation, **not** a measured customer improvement.

## ServiceNow solution delivered in this website
Enhanced the existing public [Universal Delivery Workbench case study](../delivery-case-study.html#delivery-plan-lab) rather than creating an isolated microsite. Implemented:
- A keyboard-accessible eight-view Delivery Plan walkthrough with explicit source references, evidence required, blocked gate, and Next Best Action per view.
- A browser-local narrative explorer with eight source-described document families and Executive, Client and Technical depth: **24 mock-only combinations**.
- Conservative draft labels, source/DEV/version distinctions, SOW-approval safeguards and a synthetic JSON export that is always **NOT RUN / HOLD**.
- A homepage entry and a distinct MOCK-ONLY claim in the public verification register.
- Offline publication contract tests and four-viewport Chromium checks, wired into the existing responsive CI workflow. Execution status is tracked independently in GitHub Actions.

## Source evidence and limitations
Reviewed private Delivery Workbench source README (4.22.2) and its 4.22.0/4.22.2 release notes; Diagnostic Workbench 2 source boundary; connected Google Drive controlled **30 September 2026** Universal Delivery Workbench Solution As-Built (source 4.6.1; historical DEV 4.5.1); private portfolio-control release/evidence records.

The public walkthrough **does not** execute private source code, provide authentic instance imagery, or authenticate to a ServiceNow instance. Source 4.22.2 is **SOURCE-ONLY** here; browser actions and all document previews are **MOCK-ONLY**; historical DEV reporting cannot be inherited as current acceptance. No fresh **DEV-VERIFIED** or **PRODUCTION-VERIFIED** result is claimed.

All genuine screenshots remain withheld: **0 individually approved**. No customer identifiers, private source, instance addresses, tokens, Drive URLs or unreviewed image pixels were published. No repository visibility or Drive sharing changes.

## Acceptance and remaining gates
Repository quality tests and responsive Chromium runs must pass on the final commit. These tests prove public-page behaviour only. Native target acceptance needs version-pinned install/read-back, non-admin/negative access, replay, concurrency, document-source mapping, generated Word/HTML outputs, governance and rollback validation. Real captures need image-specific sanitisation and approval.

## Licensing
Public static HTML needs **no ServiceNow licence**. Native scoped implementation needs authorised platform roles and applicable App Engine/custom-app/custom-table entitlements. Native ITSM/ITOM features, IntegrationHub spokes, analytics, AI and external Jira/Confluence/Notion provider accounts/API rights require target-specific subscription and connection checks.

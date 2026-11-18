# CMDB ownership and criticality assurance — 18 November 2026

**Classification:** SOURCE-ONLY public implementation; MOCK-ONLY six scenarios; native ServiceNow verification NOT RUN; release HOLD.

## 1. The client's pain & history

Enterprise CMDB data can appear complete while business ownership is ambiguous, an integration source overrides a curated owner, or criticality is not attested. These conditions undermine incident routing, change impact and service accountability. A self-approved spreadsheet is not independently evidenced ownership. Fictional case; no named customer.

## 2. The ServiceNow solution illustrated

Published [CMDB Ownership & Criticality Assurance](../cmdb-ownership-attestation-lab.html), a responsive browser-local case study based on [the six-gate deterministic model](../cmdb-ownership-attestation-model.js). Fixed cases: unowned CI, source conflict, stale review, criticality gap, self-approval, reviewed candidate.

The six advisory controls are accountable business owner, support owner, criticality rationale, authoritative source, attestation recency and independent review. A 90-day illustrative review interval is NOT a ServiceNow OOTB default.

All-green status means candidate for native verification, never approved. The six-row offline CSV is permanently MOCK-ONLY / NOT RUN / HOLD, with no customer identifiers, private receipts or sensitive fields. The illustrated user interface is CSS and text, not a native ServiceNow screenshot.

## 3. Architectural best practices and entitlements

Prefer existing CMDB ownership fields, CSDM relationships, IRE reconciliation, assignment routing and native auditing to new custom tables. Keep source precedence and history explicit; use ACLs, separation of duties, a policy owner, attestation and a separately approved production release.

Static portfolio requires no ServiceNow licence. Native capabilities require appropriate CMDB/CSDM access. Discovery, Service Graph Connectors, Service Mapping, Data Manager, Performance Analytics and custom-app hosting may require additional subscriptions, plugins or roles; verify each target contract.

## Provenance reviewed

- Private Delivery source README (source releases, safe packaging and install boundary)
- Private Diagnostic Workbench 2 README (separate scope and KI companion)
- Controlled Google Drive Universal Delivery Workbench As-Built, Architecture and User Guides & Training dated 30 September 2026, each an unapproved draft distinguishing source 4.6.1 from historical DEV 4.5.1 read-back; no private Drive URLs or content reused in public UI
- Existing [CMDB Assurance Tower](../cmdb-assurance-control-tower.html) and [Evidence Library](../evidence.html)

## Native acceptance gates still outstanding

- [ ] Confirm installed target application, instance scope, plugin versions, roles and contractual entitlements
- [ ] Read owner, support group, criticality and source data under approved least-privilege access
- [ ] Inspect IRE precedence and preserve non-destructive conflict remediation
- [ ] Execute negative persona testing and capture dates/evidence with an independent reviewer
- [ ] Approve redacted screenshot publication individually
- [ ] Obtain change/operations acceptance before any production claim

**Evidence:** SOURCE-ONLY public code; MOCK-ONLY scenarios; newly DEV-VERIFIED 0; PRODUCTION-VERIFIED 0; original screenshot approvals 0 — HOLD. No private source, secrets or customer data published.

# Native Workbench acceptance worksheet — 12 November 2026

## 1. The client's pain & history

Source inspection, prior DEV read-backs, synthetic demonstrations and production acceptance were previously explained in the Workbench Acceptance Playbook but could not be recorded in a structured, downloadable local reviewer worksheet. This invites version drift and an unreviewed checklist being mistaken for native approval.

## 2. The ServiceNow solution

Extended [the existing acceptance playbook](../workbench-acceptance-playbook.html#native-execution-ledger) with a six-case browser-local test recording interface:

- A01: installation, scope and entitlement dependencies.
- A02: read-only Diagnostic collector safety and evidence lineage.
- A03: Delivery pattern regeneration, source identity and approval preservation.
- A04: role/ACL, release gates, audit and rollback.
- A05: optional external transport, correlation, retry, authority and failure handling.
- A06: responsive/keyboard accessibility and evidence.

The reviewer can record component, environment, installed version, source SHA, anonymised instance alias, role and execution date, then independently mark each case NOT_RUN, PASS, FAIL or BLOCKED with a private receipt alias. Downloaded JSON is a **manual handoff** only: it permanently states SOURCE-ONLY, publication HOLD, no independently verified DEV or Production execution and no publication authorisation. Six self-reported PASS states **cannot** promote the evidence class. Invalid URL-style receipt identifiers block export. The browser performs no external network calls or persistent storage.

The existing public site already links to this playbook; added a direct worksheet anchor and the route to the sitemap. The page now reconciles the historical DEV report to the 19 October 2026 Architecture document: 4.22.2 reported read-back on 6 October and a narrow UI Page read-back on 19 October. These dated source claims do not certify the current target.

## 3. Architectural best practices and evidence

- **SOURCE-ONLY:** HTML/JS worksheet implementation, supporting source documentation, static tests and architecture narrative.
- **MOCK-ONLY:** Browser test fixtures and synthetic data used by Chromium automation.
- **DEV-REPORTED:** 6 October and 19 October 2026 architecture-document statements, not newly reproduced.
- **DEV-VERIFIED:** No independent target-instance read-back in this release.
- **PRODUCTION-VERIFIED:** Not established.
- **Screenshot publication:** HOLD; no original or unreviewed image embedded. All six previously inspected source captures remain private.

Quality controls include source-level HTML/evidence assertions, existing full-site link/publication checks and browser end-to-end testing at 390, 768, 1024 and 1440 pixels. Browser tests cover six self-reported passes, HOLD-only JSON download, invalid receipt rejection and full reset without remote requests. Exact commit workflow statuses must be read separately; an automated browser passing does **not** prove a native ServiceNow execution.

### Licensing and entitlement boundary

Static GitHub Pages worksheet: **no ServiceNow licence**. Real deployments require authorised scoped-app usage, platform roles and ACLs; custom App Engine licences may apply. ITSM/MIM, ITOM/Discovery/Service Graph, IntegrationHub/third-party APIs, Performance Analytics, AI/Now Assist and Knowledge Intelligence product-table/content rights depend on the enabled features, subscription and negotiated entitlements. Never assume the entire matrix is licensed simply because the Workbench source has its capability definitions.

### Open release gates

- DEV scope, installed app/pack versions, source SHA, real role and ACL tests, functional verification, independent reviewer and dated receipts remain unproven in this run.
- Customer/proprietary screenshots remain on publication HOLD pending rights, redaction, pixel inspection and independent image approval.
- Public GitHub Pages reachability requires independent HTTP confirmation beyond GitHub workflow status.

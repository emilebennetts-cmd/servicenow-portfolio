# Integration contract decision lab — 13 November 2026

## 01 / The client's pain & history

Client-neutral scenario, not a customer outcome claim: multiple systems of record (ServiceNow delivery, Jira, Confluence and Notion) can duplicate tasks or overwrite approved content when retries, provider edits and version drift are not governed. Historical sync rows or a connected-looking UI do not prove a working service.

## 02 / The ServiceNow solution — public implementation

New [Integration Contract Decision Lab](../integration-contract-lab.html) implements a browser-local deterministic decision model:
- Five synthetic fixture presets: eligible proposed create, idempotent replay, remote concurrency conflict, protected inbound approval-field mutation, and missing connection approval.
- Selectable Jira/Notion/Confluence object profiles, outbound/inbound operations, linked/unlinked record state, bounded source/synchronised/external revisions, connection and mapping review flags.
- A fail-closed advisory receipt with decision trace. No API calls, persistence, ServiceNow writes, external links to restricted content or active provider credentials.
- A seven-gate native integration acceptance checklist covering source identity, authority, security, correlation, conflicts, recovery and release.
- Homepage/mobile navigation, 90-second reviewer link, searchable Explorer catalogue, canonical sitemap and mock-only public verification claim.
- Standalone source-contract assertions plus Chromium scenario coverage across 390/768/1024/1440px, enforced in responsive CI.

## 03 / Architectural best practices and source truth

Restricted Delivery source documentation reviewed: R1 independent 4.22.0 and 4.21.0 context/Plan specifications and current 4.22.2 README. The source describes destination-specific correlations, explicit field ownership, revision checks, replay, reviewed unlink and transport-free mock contracts. It explicitly withholds outbound actions until approved credentials, wire mapping, durable atomic operation ledger, persona/API verification and actual live replay acceptance are complete.

The public work is a separately authored educational representation, not a copy of private implementation files. Controlled Google Drive Solution As-Built resources were located in the connected index; no original screenshot pixels or confidential paragraphs were copied. Historical As-Built/DEV generations and the current source generation remain distinct.

### Classification

- **SOURCE-ONLY:** architecture/provenance, public authored HTML and static safety tests.
- **MOCK-ONLY:** all displayed outcomes and provider/event fixtures.
- **DEV-REPORTED:** only previously documented historical platform observations, not inherited as evidence of this connector.
- **DEV-VERIFIED:** none newly established.
- **PRODUCTION-VERIFIED:** none.
- **Public screenshots:** zero new approvals; image-specific publication gate remains HOLD.

## Remaining native acceptance

Real provider credentials and account rights, legal source-of-truth/field ownership signoff, target ServiceNow scope and version, authorised ACL-persona tests, atomic operation ledger, delayed/ambiguous creates, rate limits, concurrency, negative inbound authority, replay/recovery, rollback, monitoring and UAT remain NOT RUN. No client approval or production implementation is asserted.

## Licensing

Public website: no ServiceNow licence. Actual scoped implementation: App Engine/custom-app and table entitlements and appropriate roles/ACLs. External connection: target-approved REST/IntegrationHub and spoke licensing when used, provider API/subscription rights, connection aliases and privacy review. ITSM/ITOM rights as actually in scope.

## Publication controls

No unapproved imagery, private source, customer identifiers, original ServiceNow screenshots, instance addresses, credentials or data copied; no visibility/sharing changes. CI success establishes the public site, not native ServiceNow acceptance.

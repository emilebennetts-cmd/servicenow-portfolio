# ServiceNow Workbench verification matrix — 8 November 2026

This is a **public, sanitised acceptance specification**, not a test execution report. The implementation repositories are the source of architecture claims; no current production verification is asserted.

## Evidence vocabulary

| Label | Meaning | Publication rule |
| --- | --- | --- |
| SOURCE-ONLY | Repository or design artefact supports the claim; no runtime execution demonstrated | Link to specific source and commit |
| DEV-REPORTED | Historical development verification described in repository records | Include date, environment and limitations |
| DEV-VERIFIED | Current independent execution with reproducible read-back and reviewer | Require execution artefact and reviewer |
| MOCK-ONLY | Synthetic walkthrough or demonstration | Prominently identify as illustrative |
| PRODUCTION-VERIFIED | Authorised production execution with redacted evidence | Never infer from DEV or source |

## Acceptance tests (not yet executed for this portfolio release)

| ID | Workbench | Scenario and pass criterion | Evidence to retain | Current classification |
| --- | --- | --- | --- | --- |
| D-01 | Diagnostic | Read-only collector executes against an authorised non-production fixture without write operations | collector version, run ID, redacted query trace, read-only assertion | SOURCE-ONLY |
| D-02 | Diagnostic | Evidence envelope rejects missing required fields and preserves provenance on valid input | redacted fixture, validation result, schema version | SOURCE-ONLY |
| D-03 | Diagnostic | Same input and rule version produce identical findings and stable correlation references | fixture hash, rule version, output diff | SOURCE-ONLY |
| D-04 | Diagnostic | Role lacking required access cannot view restricted evidence or execute privileged collection | persona/role matrix, denied request, ACL result | NOT VERIFIED |
| D-05 | Diagnostic | Knowledge Intelligence companion installation and navigation are distinguished from the base Workbench UI | package version, installed modules, navigation read-back | NOT VERIFIED |
| L-01 | Delivery | Scope selection generates only missing draft artefacts; re-run preserves edited answers and approval states | before/after record snapshots, idempotency diff | SOURCE-ONLY |
| L-02 | Delivery | Candidate pattern is not represented as deployment-certified; review and approval gates remain enforced | pattern lifecycle states, role test, audit trail | SOURCE-ONLY |
| L-03 | Delivery | Requirements link to design, build, tests and handover; unrun tests remain explicitly unrun | redacted traceability export, lifecycle record IDs | SOURCE-ONLY |
| L-04 | Delivery | Document generation produces a controlled draft and does not imply customer approval | generated synthetic document, approval audit | SOURCE-ONLY |
| L-05 | Delivery | External Jira/Confluence/Notion adapters do not claim live sync without authorised connections | adapter configuration, connection test, outbound-write audit | MOCK-ONLY / NOT VERIFIED |
| X-01 | Cross-workbench | Reference-only diagnostic handoff cannot silently mutate Delivery approvals or source evidence | synthetic handoff payload, before/after audit | MOCK-ONLY |
| P-01 | Public portfolio | Every screenshot has source provenance, sanitisation review, explicit publication approval and matching SHA-256 | private approval receipt plus public hash manifest | NOT VERIFIED |
| P-02 | Public portfolio | Keyboard-only navigation, 320px layout, reduced motion, focus visibility and screen-reader announcements pass | dated browser/device and accessibility results | NOT VERIFIED |

**Execution rule:** Do not upgrade any row to DEV-VERIFIED or PRODUCTION-VERIFIED without dated, independently inspectable execution evidence. A passing source-level unit test is not an instance deployment test.

## Source boundaries and known blockers

- [Universal Delivery Workbench source](https://github.com/emilebennetts-cmd/solution-lifecycle-studio): README reports version 4.22.2 and historical DEV read-back for an earlier baseline. The documented demo7 target has a different application scope identity; no automatic equivalence is assumed.
- [Diagnostic Workbench 2 source](https://github.com/emilebennetts-cmd/Diagnostic-Workbench2): companion Knowledge Intelligence package is separately deployed, and its Classic modules are not yet integrated into the local-first Workbench navigation.
- The portfolio's illustrative process flows and pattern selector are MOCK-ONLY; they do not prove installed ServiceNow features.
- Screenshot publication remains gated by source ownership, confidentiality review, sanitisation, explicit approval and content-integrity verification. Do not publish images found in connected Drive merely because they are accessible.
- Client identities, instance hostnames, credentials, proprietary implementation files and unapproved screenshots must not enter public artefacts.

## Entitlement review

The static GitHub Pages portfolio needs **no ServiceNow licence**. Running the applications requires an authorised instance and applicable custom-app/App Engine entitlements. Verify subscription-specific rights for ITOM/Discovery, IntegrationHub spokes and transactions, Performance Analytics, AI/Now Assist and external provider APIs before claiming availability. Entitlements vary by contract and deployment; this matrix is not a licensing determination.

## Release record

- **Date:** 2026-11-08 (Australia/Sydney)
- **Change:** Added a public, source-traced acceptance matrix with explicit evidence promotion gates and known scope/version caveats.
- **Verification:** Markdown source committed; no ServiceNow instance, screenshot approval, browser automation or production test performed by this change.
- **Next:** Execute P-02 browser checks; privately review screenshot candidates and authorisation; attach redacted DEV execution receipts to applicable rows.

# 16 November 2026 — CMDB Assurance Five-Stage Evidence Triage

## 1. The client's pain & history

**Fictional governance scenario.** A field consultant returns a 117-row CMDB native-acceptance workpack with a mix of NOT RUN, PASS, FAIL and BLOCKED entries. The existing browser-local preflight can detect metadata and source mismatch, but does not clearly expose where remediation effort remains across the five dependency stages. A raw CSV or copied reviewer roster must never be published as evidence.

The implementation was informed by the current **public** 117-control source models and Control Tower, source-level Delivery and Diagnostic documentation (separate protected scopes and evidence boundaries), and the 30 September 2026 controlled Universal Delivery Workbench documentation completion report. That report distinguishes a historical 4.5.1 DEV read-back from its 4.6.1 document baseline; neither validates this CMDB feature.

## 2. The ServiceNow solution (implemented source-only)

Enhanced the [CMDB Assurance Control Tower](../cmdb-assurance-control-tower.html#native-receipt-preflight) in place. After a sanitised local CSV is imported, the five-stage reconciliation displays **only public stage titles and aggregate counts**: source-matched controls, reported NOT RUN / PASS / FAIL / BLOCKED, missing / changed source records and an immutable HOLD decision. The reviewer can export a separate **five-stage, six-line summary CSV**, which never includes imported instance aliases, receipts, timestamps, private evidence, performer identities or untrusted control IDs.

- Strict 117-record, 19-column CSV parsing and the original independent metadata audit remain unchanged in purpose.
- New `stageTriage` builds five summaries using current source-model review stages and checks exact expected source text and duplicate IDs.
- New `stageCsv` exports public names and aggregate numbers only; malformed, oversized or wrong-schema inputs cannot produce an export.
- The browser disables the aggregate download when a file has not been successfully parsed, clears previous summaries before new inspection and uses safe text nodes rather than importing raw HTML.
- Unknown input identifiers are now represented as generic row numbers in issue messages, never echoed from the CSV.
- Source-only regressions cover 18/25/24/30/20 source counts, mixed reported outcomes, missing/changed and unknown source IDs, restricted sentinel non-disclosure and fail-closed malformed uploads.
- Four-width responsive browser assertions were added for stage rendering, HOLD labels, summary download and invalid GO metadata.

**Evidence status:** The code and tests have been committed to public GitHub. Until GitHub Actions runs are independently inspected, automated CI and live public deployment remain **unconfirmed**. Nothing was executed on ServiceNow this cycle.

## 3. Architectural best practices and acceptance

Source reference remains the existing five public acceptance models, **not** a new parallel ServiceNow calculation engine. The tool never calls a ServiceNow API, reads network data, writes browser persistence or upgrades imported metadata into independently certified results. Even 117 operator-reported PASS values cannot make the output GO. Actual native acceptance requires a controlled target-instance read-back, test execution under positive and negative roles, evidence in approved private storage and independent reviewer sign-off.

**Classification:** public implementation SOURCE-ONLY; baseline exported workpacks MOCK-ONLY; edited candidate results, where provided, operator DEV-REPORTED at most; newly DEV-VERIFIED **0**, PRODUCTION-VERIFIED **0**. Original screenshots remain **HOLD; no approval or publication**.

**Licensing / entitlements:** Public static JavaScript/CSV features need **no ServiceNow licence**. Native testing depends on CMDB/IRE roles and relevant target activation. Check Discovery / ITOM Visibility, Service Graph Connectors, Service Mapping, Tag Governance, Data Manager, IntegrationHub, ATF, Performance Analytics and AI by installed application, target release and subscription before use. No entitlement is inferred from this website.

**Source and test paths:** `cmdb-assurance-receipt-preflight.js`, `cmdb-assurance-control-tower.html`, `tests/cmdb_assurance_receipt_preflight.test.cjs`, `scripts/browser_cmdb_assurance_control_tower.py`, `index.html`. Security and publication boundaries remain unchanged.

**Blockers:** No authorised current CMDB DEV read-back, 117 native execution receipts, independent reviewer signatures or image-specific publication approvals. Private application code, customer records, credentials and unapproved screenshots were not copied or published.

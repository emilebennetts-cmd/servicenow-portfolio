# 16 November 2026 — CMDB Assurance Offline Evidence Receipt Preflight

## 1. The client's pain & history

The public CMDB Assurance Control Tower already supplied a **117-control, five-stage native execution workpack**, but a field consultant could return an edited CSV with a missing IRE control, altered expected evidence, an unsupported `GO` decision, a missing execution timestamp or the same executor and reviewer. Without a consistency check, that worksheet could be mistaken for native acceptance. This is a **fictional governance scenario**, not a customer defect or measured production outcome.

## 2. The ServiceNow solution

Added a mobile-responsive **[local receipt preflight](../cmdb-assurance-control-tower.html#native-receipt-preflight)** to the existing Control Tower. The browser reads a *sanitised* 117-row CSV exported by the five-stage planner. It never uploads, persists, prints, emails, sends or stores the CSV and never connects to ServiceNow.

The preflight uses the **current five public source-model definitions** to check:

1. Exactly 117 unique, recognised control identities and the 19-column planned-workpack schema.
2. Unchanged stage assignments, source actions, dependencies and expected evidence.
3. Strict `NOT RUN`, `PASS`, `FAIL` or `BLOCKED` status, with `Release decision = HOLD` for **every** control.
4. `MOCK-ONLY` and empty private metadata for unrun controls; `DEV-REPORTED` for any manually populated candidate result. No result is relabelled `DEV-VERIFIED` by a CSV import.
5. Opaque non-URL private evidence receipt references, non-sensitive target aliases, installed-version text, syntactically valid UTC timestamps and separate executor/reviewer aliases.
6. Bounded 1 MiB input, correctly quoted CSV cells and rejection of malformed, duplicate, incomplete or altered data.

The rendered UI displays only aggregate counts and generic issue reasons by public control ID; it never echoes instance identifiers, reviewer names, receipt values or source text from the imported file. It **always returns HOLD**. Passing preflight means only that source/schema and metadata consistency checks passed, **not** that the underlying execution or approval is genuine.

Added `cmdb-assurance-receipt-preflight.js`, Node regression tests, a responsive Chromium acceptance extension and a mandatory GitHub quality-gate step. The original source-derived 117-control exports, hold statuses and existing site navigation remain intact.

## 3. Architectural best practices

Use ServiceNow's OOTB CMDB/IRE, applicable Health, relationship, Tag Governance and Data Manager components as the native systems of record. The website is a strictly read-only planning and preflight utility, not a replacement for ATF, platform audit, RBAC testing or an independent technical approver. Store actual DEV/Production evidence in approved restricted repositories; never provide a public static page with unredacted customer CSVs, tokens, instance URLs, screenshots or evidence artifacts.

**Evidence classification:** SOURCE-ONLY implementation; MOCK-ONLY synthetic default workpack; optionally DEV-REPORTED candidate metadata entered by an operator (not independently validated). New DEV-VERIFIED 0; PRODUCTION-VERIFIED 0. Original screenshot publication approvals 0 / HOLD. Historic Workbench DEV reports remain separately scoped and do not validate this module.

**Licensing and entitlements:** The static website, offline CSV parsing and export require **no ServiceNow licence**. Running the native 117 controls requires appropriate CMDB and IRE roles plus an authorised non-production instance. Entitlements/activation for Discovery, ITOM Visibility, Service Graph Connectors, Service Mapping, Tag Governance, Data Manager, IntegrationHub, ATF, Performance Analytics and optional AI must be established against the target release and contract.

**Source provenance:** Reviewed the latest public Control Tower code and its five source JavaScript acceptance models, private Delivery and Diagnostic repository documentation, private portfolio control boundaries and existing controlled workbench architecture/design documentation. Private source and original screenshots are not copied into the public site.

**Validation intent:** Node coverage includes pristine 117-row HOLD imports, one properly attributed DEV-REPORTED candidate, missing independent reviewer, missing timestamp/receipt/target, source drift, duplicate controls, changed header, forbidden release GO or DEV-VERIFIED, future timestamps, oversized files and malformed quoting. Responsive Chromium exercises synthetic HOLD import and tampered GO rejection at 375/768/1024/1440px.

**Release boundary:** Committed source and tests do not themselves establish GitHub Pages delivery, independently observed instance behaviour or native acceptance. CI and deployment outcomes must be read from their actual workflow receipts.

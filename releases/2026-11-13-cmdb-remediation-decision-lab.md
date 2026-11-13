# CMDB remediation decision lab — 13 November 2026

## Client pain and history

Large, multi-source CMDBs accumulate duplicate names or serials, stale discovery timestamps, conflicting IRE ownership and relationship gaps. Aggregate discovery and diagnostic signals must be treated as investigation candidates rather than authorisation to merge, retire or delete CIs. Data completeness can be obscured by unavailable source tables and bounded group collection.

## Implemented ServiceNow portfolio solution

Created a standalone, responsive, keyboard-accessible browser lab with four synthetic CMDB findings (duplicate, orphan relationship, stale lifecycle, identifier conflict). Four adjustable independent gates: aggregate evidence completeness, source/CI authority, simulated approval and rollback, and service/dependency impact. Decision algorithm follows strict precedence: unavailable → EVIDENCE GAP; capped → PARTIAL COVERAGE; unknown/conflicted owner → OWNERSHIP REVIEW; unknown impact → IMPACT ASSESSMENT; missing approval → CHANGE CONTROL; otherwise CONTROLLED REVIEW ONLY.

Every result is advisory. Downloaded JSON preparation receipts always encode HOLD, NOT RUN, not DEV-verified, not production-verified, not approved. Browser runtime has no external requests, credentials, stored client records, network APIs or original Workbench screen pixels.

## Source review / provenance boundary

- Private Diagnostic Workbench source: aggregate collector categories for duplicate CI analysis, identification/reconciliation, CI relationships, lifecycle/staleness.
- Controlled Google Drive: September 2026 Delivery Solution As-Built and training pack, version-bounded 4.6.1 source / 4.5.1 historical DEV; fictional Diagnostic completion runbook (not client or Production proof).
- Current Delivery repository source branch reviewed separately from those earlier installed baselines.
- Published text synthesises general architectural concerns, not private collector code, private file URLs, customer records or actual instance verification.

## Technical controls

- OOTB-first: ServiceNow IRE rules, CMDB Health, Data Manager, lifecycle governance, change control, CSDM impact and role/ACL review where licensed and applicable.
- Responsive styles with 390/768/1024/1440 px Chromium interaction/export checks.
- Offline public evidence and link/sitemap/explorer reconciliation, two evidence claims intentionally classified MIXED CLAIMS (source-informed narrative + synthetic decisions).
- No source-to-target compatibility, native DEV tests, change approvals, or screenshot publication is implied.

## Licensing

Public static website: no ServiceNow licence. Target-specific native implementation may require ITOM Visibility / Discovery / Service Graph Connectors, applicable CMDB Health and Data Manager features, ITSM Change, App Engine/custom table rights, IntegrationHub or third-party connector subscriptions, and authorised scope ACLs. Verify contract and plugins before native execution.

## Outstanding evidence

Real ServiceNow version-pinned DEV acceptance and genuinely approved/permanently sanitised screenshots remain unavailable. Original captured images remain HOLD / zero approved.

# Offline Evidence Assurance CSV Worksheet — 14 November 2026

**Classification:** SOURCE-ONLY browser implementation. **Native status:** NOT VERIFIED. **Review/release:** UNREVIEWED / HOLD.

## 1. The client's pain & history

ServiceNow delivery teams commonly reconcile As-Built inventories, historical DEV reports, synthetic demonstrations and design proposals during assurance and handover. A JSON-only evidence worklist is suitable for automation, but platform owners and independent reviewers often need a spreadsheet-friendly format for delegated verification planning. Copying source labels into an uncontrolled spreadsheet can accidentally drop important evidence boundaries or interpret malicious cell text as formulas.

The representative workflow is illustrative, not a customer-specific delivery assertion.

## 2. The ServiceNow solution — implemented website enhancement

Enhanced [Evidence Assurance Worklist](../evidence-assurance-worklist.html) with an **Export review worksheet (CSV)** action alongside the existing JSON export. Both operate on the same **current filters**, use the same authoritative public register and are unavailable when no valid matching items exist.

The UTF-8 CSV contains: claim ID, title, evidence classification, next gate, recommended action, public page, public register version timestamp, review status, verification status, release status, independent native verification, production acceptance and screenshot approval.

Every row has **UNREVIEWED / NOT VERIFIED / HOLD** and **FALSE** for the three approval/verification flags. No local tests, spreadsheet edits or imports can elevate a claim. The worksheet is generated in-browser without third-party calls, browser storage, a backend or additional ServiceNow permissions. It carries public content only, **not** customer material, private evidence aliases or original screenshots.

The public register remains at **87 claims** (54 SOURCE-ONLY, 20 MOCK-ONLY, 9 PROPOSED, four historical DEV-REPORTED, zero independently DEV-VERIFIED and zero PRODUCTION-VERIFIED). The existing SOURCE-ONLY worklist claim covers this incremental feature; it is not a new ServiceNow product capability.

## 3. Architectural best practices

- OOTB-first: use native records, roles, ACLs and the installed/licensed release where practical. Do not allow a spreadsheet to become a parallel approval engine or CMDB system of record.
- Export determinism: the CSV is derived from precisely the currently filtered public claim set; the independent JSON export remains unchanged.
- Formula-injection defence: every CSV value is quoted and escaped, control characters are replaced with spaces, and any formula-like first non-space character (`=`, `+`, `-`, `@`) is prefixed with a literal apostrophe.
- Strict schema: a corrupt or duplicate-ID register empties the view and disables both exports; unsafe page paths and unknown classification values are rejected.
- Browser/privacy boundary: no data upload, client instance connection, private URL, persistent local storage, screenshot publication, release authorisation or runtime promotion.
- Native DEV/production evidence: separate dated execution, target version, instance, witness, private receipt and acceptance remain mandatory.

### Verification

Automated static tests: `scripts/test_evidence_assurance_worklist.py` verifies safety and export boundaries.
Four-width Chromium suite: `scripts/browser_evidence_assurance_worklist.py` verifies JSON and CSV exports, all 20 MOCK-ONLY filtered rows, HOLD/false flags, mobile/no-overflow, no-result disabling, duplicate-ID fail-closed handling and spreadsheet-formula neutralisation.

Relevant CI: `.github/workflows/evidence-assurance-worklist.yml`, alongside existing site quality, publication audit and GitHub Pages workflows. **CI proves the static website only**, and completed final-commit workflows must be checked before asserting deployment.

### ServiceNow licensing and entitlement dependencies

The public static site, JSON export and CSV export require **no ServiceNow licence**. Actual native acceptance may require scoped App Engine/custom-table entitlements, authorised roles and ACLs, and feature-specific ITSM, ITOM/Discovery, IntegrationHub/spokes, ATF, analytics, AI and third-party subscriptions depending on the installed solution and customer contract.

### Release and security gates

- Native DEV/production acceptance: **NOT RUN** for this change.
- Screenshot rights and exact-derivative approval: **0 originals authorised; HOLD**.
- No repo visibility changes, restricted source, client data, secrets or unapproved pixels published.
- Original private documents and evidence remain at their controlled locations; only public claim metadata is exported.

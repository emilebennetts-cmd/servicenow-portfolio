# Native Acceptance Evidence — Offline Resume and Import Controls

**Date:** 14 November 2026 (Australia/Sydney)  
**Public experience:** [Incident Pack candidate evidence workbook](../incident-pack-native-pilot.html#native-observation-log)  
**Evidence boundary:** SOURCE-ONLY (implementation), SELF-REPORTED / UNREVIEWED (uploaded observations), historical DEV-REPORTED (separate pilot); **DEV-VERIFIED and PRODUCTION-VERIFIED are not established**.

## 1. The client's pain & history

The existing 29-case Incident Pack workbook could export a candidate evidence packet but could not restore it. A practitioner closing their browser lost temporary status and anonymous evidence-alias input, leading to unnecessary repeated preparation and increasing the risk that private evidence would be copied into unsuitable channels. A saved JSON packet must never be treated as a real native execution receipt or allowed to import forged approval flags.

The existing source-validation material (21 October 2026) is an **unexecuted** case matrix for a separate candidate. It has a blank execution record and unresolved native target, entitlement and independent witness requirements. The source is not a PROD acceptance record.

## 2. The ServiceNow solution

Added a visible, accessible **Resume an offline evidence candidate** panel within the live 29-case workbook. Reviewers may select a prior JSON export and restore all 29 self-reported status/alias pairs plus four anonymised environment identifiers, **replacing** the existing browser-local notes only if every record passes strict schema validation.

The import uses the local browser file API, does not upload files, stores no data, and never contacts ServiceNow, Drive or GitHub. Input is limited to 128 KiB; malformed JSON, arbitrary or duplicate case IDs, unknown fields, unsupported versions, invalid aliases, contaminated environment fields, mismatched workstreams/personas/titles, inconsistent missing-evidence indicators and any claims of verification, approval or publication are rejected **atomically**. Errors use fixed text rather than reflecting untrusted imported content into HTML.

Successful imports remain **NOT VERIFIED / UNREVIEWED / HOLD**. No import can grant an entitlement, prove an ACL test, authorise a deployment, approve a screenshot or close a ServiceNow release gate. Re-export produces the existing 1.0 candidate format.

## 3. Architectural best practices

- Treat evidence packets as **untrusted files**, even if their filename matches the expected export.
- Pin the known NV-001–NV-029 catalogue, its title, workstream and persona, so a compromised or stale source cannot silently redefine acceptance.
- Fail closed on false or elevated approval flags and malformed schema; preserve all local notes on failure.
- Retain original screenshots, target URLs, test-user identities and audit traces in independently controlled private systems; only short, safe evidence aliases belong in the public browser.
- Require ServiceNow native permission/ACL negative checks, metadata comparison, target build identity, before/after-state, ATF results, failure/replay and recovery evidence; owner approval and independent validation remain separate from this UI.
- Use native Incident and Change as systems of record. This is a public training/evidence candidate—not a replacement approval workflow.

## Source reconciliation and verification

- Source: `solution-lifecycle-studio/docs/native-validation/README.md` and `execution-record.json`, reviewed 14 November 2026 (private; not linked publicly)
- Distinct Diagnostic Workbench source boundary reviewed; its own scope and companion deployment do not inherit Incident Pack verification.
- Connected Drive Discovery and Delivery documentation inventory checked; no private file IDs, original screen pixels or client data included in the public page.
- Public changes: `incident-pack-native-pilot.html`, `scripts/test_native_observation_workbook.py`, `scripts/browser_native_observation_workbook.py`.
- Automated static contract tests cover no external uploads, schema allowlists, explicit HOLD flags and immutable publication boundaries.
- Chromium regression tests exercise JSON export/import, 29-case restoration, invalid/forged packet atomic rejection and reset at 390 / 768 / 1024 / 1440px. **Browser tests are not native ServiceNow execution.**
- GitHub Actions status and deployed site availability must be verified against the **final** commit, not assumed from code publication.

## Entitlements / HOLDs

The static GitHub Pages workbook requires **no ServiceNow licence**. Actual Delivery Workbench custom applications/tables require confirmation of App Engine/creator rights, custom table allocations, platform roles/ACLs, approval for a non-production instance and applicable ITSM/Change, ITOM/Discovery, ATF, IntegrationHub/spokes, analytics, AI or external provider entitlements based on the actual configuration. Entitlements are **not evidenced by the import**.

**HOLD:** 29/29 actual independently witnessed native cases are not established in this release; release and screenshot publication approvals remain outstanding. Original screenshots are held; private repositories remain private.

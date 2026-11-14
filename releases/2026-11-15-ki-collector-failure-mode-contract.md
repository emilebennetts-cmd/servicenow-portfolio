# Knowledge Intelligence collector failure-mode gallery

**Date:** 15 November 2026 (Australia/Sydney)  
**Page:** [Knowledge Intelligence acceptance matrix](../knowledge-intelligence-acceptance-matrix.html#collector-contract)  
**Evidence classes:** SOURCE-ONLY for source architecture; MOCK-ONLY for the four interactive fixtures; historical DEV-REPORTED remains dated and unverified independently. **No DEV-VERIFIED or PRODUCTION-VERIFIED claim.**

## 1. Client pain and history

A count of collectors or a successful static lint is not sufficient to certify a target instance. A collector that returns no observations can indicate an empty healthy dataset, a missing table, an unavailable field or a rejected script. Conflating these states can produce dangerously false green ratings. Human reviewers also need to inspect each rule/metric lineage before confirming findings.

## 2. Implemented public solution

Enhanced the existing 45-module Knowledge Intelligence acceptance matrix rather than creating a competing disconnected app:

- Built an accessible four-state interactive collector contract gallery with complete illustrative evidence, `table_unavailable`, `field_unavailable`, and mutating-script lint rejection.
- Added engineering explanations, target-specific negative test IDs `KI-COL-01`–`KI-COL-04`, expected handling and explicit evidence limitations for each fixture.
- Provided one-click download of a structured, explicitly synthetic JSON contract per fixture. All exports retain `MOCK-ONLY`, `NOT RUN`, `HOLD`, `review_approved=false`, `dev_verified=false` and `production_verified=false`; actual collector output and customer information remain null.
- Added an accessible navigation anchor and a deep link from the source-backed KI architecture case study.
- Kept the existing 16 unique source table objects, 45 module taxonomy, eight preparation controls and historic DEV status unchanged.

No remote API, input upload, browser storage, customer information, private source code or original Workbench image was introduced. All examples are independently authored synthetic user-interface fixtures, not source screenshots.

## 3. Architecture, provenance and acceptance

The restricted Diagnostic Workbench source describes KI companion version 0.1.0, 16 declared tables, 45 read-only collectors and source-reported 30 September 2026 DEV install/lint checks. Its PDI verification checklist still calls for current target scope/dictionary read-back, ACL negative tests, execution of each collector, `ki-evidence/1.0` envelope checks, safe unavailable-table/field handling, less-than-two-minute runs and reviewed rule/finding lineage. The gallery maps these source-defined safeguards to four fictional outcomes. It does not claim these checks were executed.

Controls:
- CSP `connect-src 'none'`, no outbound requests, images or iframe; no form submission.
- Fixed allowlisted fixture IDs, no free-text input, no evidence ingestion; text updates use `textContent`.
- Semantic group/buttons, `aria-pressed`, live status, keyboard activation and mobile single-column layout.
- Offline Python source/privacy tests plus real headless Chromium at widths 390, 768, 1024 and 1440px, including downloadable JSON and non-certifying metadata. CI execution should be checked for the final commit before declaring success.
- The 90-item public verification register is unchanged; existing `KI-ACCEPTANCE-MATRIX` stays MOCK-ONLY.

## Licensing and entitlements

The static website, JavaScript interactions and local JSON download require **no ServiceNow licence**. Native KI deployment requires confirmed App Engine/custom-table and role rights, target-scoped ACL permissions, access to relevant underlying ITSM, CMDB/ITOM, ITAM, SecOps, HRSD, CSM, IRM and other product data, and content rights for each external knowledge provider. IntegrationHub, AI/Now Assist, Discovery, performance analytics and ATF may require separate entitlements if a customer adopts those functions; no licence is granted or confirmed by the gallery.

## Open gates

Independent current-version DEV execution and acceptance; actual target scope, class and ACL verification; content licences; production change/acceptance; individually sanitised and approved original screenshots (**zero approved, publication HOLD**); independent external website retrieval. Successful GitHub/browser testing confirms static portfolio behaviour only.

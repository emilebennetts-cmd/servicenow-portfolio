# Pattern Library public-link containment and CI quality-gate repair — 13 November 2026

**Evidence classification:** SOURCE-ONLY public-site correction. No native ServiceNow DEV/Production activity or screenshot publication is claimed.

## 1. The client's pain & history

The Pattern Library source-lineage release made source inventory evidence easier to understand, but its public page linked directly to two repository paths classified as restricted by the portfolio's publication policy. An independent GitHub quality workflow exposed the failure: [quality run 43409563828](https://github.com/emilebennetts-cmd/servicenow-portfolio/actions/runs/43409563828), step `Test quality gate`. The page also exposed two controlled Google Drive document identifiers in its citation section. These links were not necessary to substantiate the public case study and could frustrate employers without source permissions.

## 2. The ServiceNow portfolio solution implemented

- Replaced both restricted-source GitHub navigation targets with internal, self-contained public evidence pages: `pattern-library-audit-trail.html` and `delivery-release-evolution.html`.
- Rewrote the controlled-source citation paragraph to retain dated source provenance without publishing restricted Google Drive IDs or direct document links. Added a public pattern-engineering case-study citation.
- Applied an explicit inline-only Content Security Policy: no external scripts, image loads, connections, object embedding or form submission.
- Hardened `scripts/test_pattern_catalogue_lineage.py`: all safe destinations must exist; private source/Drive URL patterns are forbidden; CSP must retain `connect-src 'none'`. Updated the superseded source release note and the front of `RELEASE_LOG.md`.
- No source Workbench code, customer records, access permissions, repository visibility or screenshots were changed.

## 3. Architectural best practices, evidence and limits

Treat publication navigation as a separate security boundary from the technical claims themselves. Source repository existence does not imply public access; keep raw controlled artefacts private and offer accessible, sanitised summaries to reviewers. The in-repository quality gate remains authoritative for future regressions. Native acceptance still requires a version-pinned installed-scope readback, authorised DEV execution and independent test receipts; no metadata or site check substitutes for those controls.

**Licensing:** The static portfolio and offline Python tests require no ServiceNow entitlements. Native Workbench use may require custom app/App Engine rights, licensed product scopes (ITSM/ITOM/CMDB/IRM/HRSD/CSM), IntegrationHub/spokes, analytics, AI and external-provider subscriptions, subject to the customer's contractual terms.

**Screenshot gate:** Zero original images newly approved. Individual provenance, irreversible sanitisation and owner approval remain required before any true ServiceNow interface capture can be published.

**Verification record:** A green post-correction workflow must be confirmed from GitHub Actions independently; a successful commit alone is not evidence of passing CI.

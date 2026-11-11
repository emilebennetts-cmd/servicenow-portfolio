# Technical case-study boundary release — 12 November 2026

**Scope:** Public, sanitized architecture explanation and regression coverage. No ServiceNow change, customer deployment, screenshot approval or repository visibility change.

## Implementation delivered

1. **Diagnostic case study:** differentiates the browser-local assessment Workbench from the separately deployed Knowledge Intelligence package. The map documents local evidence intake, non-executing UI, read-only collector controls, governed article provenance, source-reported seed counts and the absent automatic navigation integration. Adds a six-control requirement-to-acceptance table with explicit *not executed* caveat.
2. **Delivery case study:** adds an accessible eight-view Delivery Plan schematic (not a captured screen), five technical implementation boundaries and two version-specific evidence cards. Source 4.22.2 is not presented as certified by historical 4.20.0 DEV evidence. Jira/Confluence/Notion connectivity and writes remain explicitly unverified.
3. **Responsive/browser assurance:** expanded Chromium smoke script to open both case studies at 390px, 768px, 1024px and 1440px, check document overflow, review provenance labels and exercise architecture anchors. The workflow is configured to trigger when either case study changes.
4. **Source-only CI safety:** added a standard-library case-study integrity test covering semantic HTML, public navigation, no restricted repository links, no unapproved media, clear source/DEV/mock/production labels, and version boundaries.

## Factual provenance and limits

- Sources were read through authorised connected GitHub access from **private** Delivery and Diagnostic repositories; this public release contains no source files or private URLs. The Delivery README reports 4.22.2 source and older 4.20.0 DEV read-back; the separate Diagnostic README_BUILD and Knowledge Intelligence README report historical tests on 1 and 30 September 2026. Those historical reports have not been independently replayed.
- Earlier private Google Drive As-Built, Architecture, Training and candidate capture inventory were located via connected Drive and private control records. This release does **not** embed, transform, link or publish any of the held Drive screenshot candidates.
- `SOURCE-ONLY`: HTML, Python tests and CI configuration commits.
- `DEV-VERIFIED`: only **historical source-reported** receipts; no fresh DEV read-back.
- `MOCK-ONLY`: explanatory topology / tab drawings, synthetic demo references and provider mock contracts.
- `PRODUCTION-VERIFIED`: **not established**.
- Automated browser suite execution and hosted Pages deployment must be checked independently; the existence of a GitHub commit or workflow YAML does not prove a green run.

## Release acceptance checklist

| Check | State |
|---|---|
| Commit the two implementation maps | Done; source-only |
| Commit static provenance/integrity tests | Done; source-only |
| Trigger Chromium across four widths | Configured; result not attested here |
| Review live Pages render and accessibility | Pending independent check |
| Permission to publish real Workbench captures | **HOLD** |
| Execute authorised instance and negative ACL tests | Not run |
| Certify production capability | Not established |

## Entitlements and platform gates

The public website and static tests need **no ServiceNow licence**. Workbench runtime requires confirmation of scoped/custom-table/App Engine licensing, ACL roles and permitted instance access. Actual content import requires lawful article-copy rights. ITSM/ITOM, IntegrationHub spokes and transactions, Performance Analytics, AI functionality, and external Jira/Confluence/Notion subscriptions are conditional on actual feature use and platform contracts. No external connector was activated.

## Rollback

Revert the case-study content and browser workflow/test commits as normal public GitHub changes. No target-instance data, customer records, provider credentials, private repository permissions, or unreviewed screenshots were modified.

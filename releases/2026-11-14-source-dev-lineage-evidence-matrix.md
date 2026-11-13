# Workbench Source-to-DEV Lineage — Technical Evidence Register

**14 November 2026, Australia/Sydney** · Public path: [Technical Evidence Register](../technical-evidence-register.html#source-lineage)

**Claim boundary:** SOURCE-ONLY and historical DEV-REPORTED only. **No new DEV-VERIFIED, PRODUCTION-VERIFIED or original screenshot publication claims.** Existing public verification register remains at 86 records; this increment corrects and presents previously described evidence rather than inventing a new capability.

## 1. The client's pain & history

A common consulting evidence failure occurs when the latest repository version is placed beside an older DEV result, leading reviewers to infer that the latest build is installed and accepted. Here, the controlled September Delivery As-Built, an October source-reported DEV read-back and later Workbench source are materially different baselines. The original technical register mentioned the old 4.20.0 baseline without naming the later 4.22.2 source. The Diagnostic Workbench and Knowledge Intelligence companion also have separate deployment identities.

## 2. The ServiceNow solution

Expanded `technical-evidence-register.html` with six dated, individually classified source/runtime records and a three-state accessible filter (all, SOURCE-ONLY, historical DEV-REPORTED). Records cover:

| Record | Version/identity | Reported date | Classification |
| --- | --- | --- | --- |
| Delivery controlled As-Built source | 4.6.1 | 30 September 2026 | SOURCE-ONLY |
| Delivery As-Built historical DEV baseline | 4.5.1 | 30 September 2026 | DEV-REPORTED |
| Delivery repository historical DEV read-back | 4.20.0 | 5 October 2026 | DEV-REPORTED |
| Delivery repository latest declared source | 4.22.2 | Read 14 November 2026 | SOURCE-ONLY |
| Diagnostic Workbench 2 Now SDK | x_1577958_dw2 | Read 14 November 2026 | SOURCE-ONLY |
| Knowledge Intelligence companion 0.1.0 | 0.1.0 | 30 September 2026 | DEV-REPORTED |

Each row links to a public-safe review page rather than a private repository or Drive source. All version and classification qualifiers are visible without running JavaScript. The filter uses no storage, analytics, network APIs or external assets.

## 3. Architectural best practices

**Do not promote evidence classes.** A source build, a document-reported DEV result and a production release are separate objects. Current native installation requires a version-pinned read-back, authorisation, explicit test identities, expected and actual results, negative ACL/persona checks, and an independent reviewer. Current Diagnostic UI navigation or KI installation cannot be inferred from the other component. A historical screenshot cannot promote a later build.

**Testing:** `scripts/test_technical_evidence_lineage.py` verifies six distinct records, their classes and relevant links, unique IDs and the required disclaimer. `scripts/browser_technical_evidence_lineage.py` checks all three filters, focus-state accessible controls, JavaScript errors and horizontal overflow at 390/768/1024/1440 px. New path-scoped workflow `.github/workflows/technical-evidence-lineage.yml`; global `portfolio-quality.yml` will also pick up the static tests. CI results are not assumed before completion.

**Sources consulted:** Connected GitHub Delivery README (4.22.2 source; historical 4.20.0 DEV read-back), Diagnostic Workbench 2 README (separate scoped app), private evidence crosswalk, prior controlled 30 September Delivery As-Built documentation located through connected Google Drive, and prior public architecture gallery release reconciliation. These are editorial source facts, not a fresh authenticated instance inspection.

**Screenshot gate:** Original or reconstructed source image publication remains HOLD, including pre-reviewed Drive candidates. Zero image-specific approvals have been received. No screenshot pixels or private provenance identifiers were introduced.

**Licensing/entitlements:** Reading this GitHub Pages page requires no ServiceNow subscription. Installing or testing native Workbench functions requires authorised target access, App Engine/custom-application and custom-table entitlements where applicable, appropriate scoped roles/ACLs, plus ITSM/Change, ITOM/Discovery, IntegrationHub/spokes, Performance Analytics, AI, document generation and provider access if activated. Source presence is not contract evidence.

## Release controls

- Public implementation and static/Chromium tests are in GitHub, with version-claim check preventing unqualified promotion.
- No private repository visibility or Drive sharing changed.
- No new DEV/Production verification and no screenshots published.
- Final CI, deployment and external HTTP reachability to be assessed from actual GitHub Actions/HTTP results; no success is asserted by this document.

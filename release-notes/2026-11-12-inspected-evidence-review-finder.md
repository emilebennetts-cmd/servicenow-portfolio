# Workbench inspected-evidence review finder — 12 November 2026

## 1. The client's pain and history

The existing visual-evidence page contained six private-source image reviews and ten candidate placeholders. Although it safely withheld all original images, the six reviewed records were static and could not be searched, filtered, deep-linked, printed or exported separately. Reviewers were forced to scan every card or confuse screened source observations with uninspected candidate slots.

## 2. The ServiceNow solution and public implementation

Extended [Visual Evidence](../visual-evidence.html#reviewed-captures) in-place, preserving every previously recorded evidence classification and existing candidate filter.

- **Six separate reviewed records** now have stable, shareable `#review-rv-0x` anchors and clear group tags: Delivery (3), Diagnostic (2), source document (1).
- Accessible text search, product filters, live result counts, reset, empty state and independent bookmarkable `reviewGroup`/`reviewq` query parameters.
- Matching review rows can be exported as a quoted, spreadsheet-safe UTF-8 CSV with a publication-decision column fixed at **HOLD**. Export includes only visible public narrative observations, non-verification limitations, next steps and case-study relative links. No private asset URLs, SHA digests or original image bytes are available to the export.
- Separate print action prints matching inspected reviews without reclassifying or exposing original captures. Existing candidate-specific CSV, search, print and privacy controls remain intact.
- A synthetic/observational screen description is **not** evidence of a live integration, installed release or executed transaction. The ten candidate cards remain a distinct collection which can overlap the six reviews.

## 3. Architectural best practices and release acceptance

- **SOURCE-ONLY:** This static website implementation, source observations and regression code. The user interface is a reviewer utility, not native ServiceNow.
- **MOCK-ONLY:** MIM-related synthetic workshop and integration examples still explicitly tagged as such within RV-03, RV-05 and RV-06.
- **DEV-VERIFIED:** No newly authenticated ServiceNow DEV read-back. Earlier version-specific historical evidence must be independently reconciled before attaching it to a capture.
- **PRODUCTION-VERIFIED:** Not established.
- **Publication:** **HOLD for all images; zero original screenshots or derivatives published.** Per-image rights clearance, flattening/redaction, independent pixel inspection, exact caption approval and provenance/version matching remain mandatory.
- **Automated tests:** Public-safety contract and four-viewport Chromium interactions (390, 768, 1024 and 1440 pixels) exercise filters, CSV scoping and HOLD, print, URL restoration and page overflow.
- **Release validation:** Check GitHub Actions quality, audit, Chromium and Pages runs against the release source SHA; a successful earlier workflow does not prove a later commit. No ServiceNow instance or external provider was contacted.
- **Licensing:** Public static site, local CSV export and browser QA: no ServiceNow entitlement. Native custom Workbench execution requires the agreed App Engine/custom application rights and roles/ACLs. ITSM/MIM, CMDB/ITOM/Discovery, IntegrationHub, Performance Analytics, AI and Jira/Notion/other provider entitlements are contingent on target features and contracts.

## Rollback

Revert `visual-evidence.html` and associated test changes. No private image, customer record, ServiceNow configuration, connected provider or permission has been modified.

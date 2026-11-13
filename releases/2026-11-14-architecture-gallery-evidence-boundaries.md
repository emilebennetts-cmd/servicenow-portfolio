# Architecture Gallery — Version-Pinned Evidence Boundary Correction

**Date:** 14 November 2026 (Australia/Sydney)  
**Public page:** [Workbench Architecture Gallery](../workbench-architecture-gallery.html#baseline)  
**This website change:** SOURCE-ONLY. Diagrams remain explanatory/illustrative.  
**DEV-VERIFIED / PRODUCTION-VERIFIED:** no new claim. **Original images:** HOLD (0 approved).

## 1. The client's pain & history

The gallery retained an older September 2026 architecture paragraph and a status definition headed `DEV-VERIFIED` even though the cited historical DEV baseline was only document-reported to this run. It also used an 11 November website deployment check as a generic present-tense assurance statement. This wording could imply fresh native runtime verification or suggest the 4.6.1 source was installed.

## 2. ServiceNow solution implemented in the public portfolio

- Updated the gallery with **three dated visual baseline cards**:
  1. **30 September controlled draft:** Delivery 4.6.1 source vs historical 4.5.1 DEV-REPORTED baseline; neither document was approved.
  2. **October repository source:** Delivery README 4.22.2 source described; integration contracts are not live provider verification.
  3. **21 October separate demo:** 4.22.8 target-specific synthetic Incident pack pilot, reported metadata/draft replay only; original-source 29-case independent native matrix remains **NOT RUN**.
- Added the **application identity firewall**: an observed demo in a distinct application scope does not certify a separate source-generation baseline.
- Corrected the DEV-REPORTED and DEV-VERIFIED definitions in the gallery.
- Replaced obsolete site-deployment assurance with durable links to public quality and acceptance evidence; no current CI success is asserted in advance.
- Added accessible responsive layout, offline regression tests, and an anchor in the page's own navigation.

## 3. Architecture and evidence sources

Privately reviewed existing Delivery `README.md`, Diagnostic `README.md`, restricted 21 October Incident pilot control record, and the controlled 30 September Delivery As-Built and Architecture PDFs in Google Drive. Their approval and environment boundaries were not promoted. Only short, non-identifying fact summaries are public; internal scope identifiers, instance URLs, source code, original screenshots and controlled document links remain private.

The public page is now a clearer architecture diagram, **not an authenticated ServiceNow screenshot**. A future screenshot gallery requires individual image provenance, irreversible sanitisation and explicit approval. Native verification requires exact scope/build identity, relevant executed tests and independent review.

## 4. Verification and entitlements

`python -m unittest scripts.test_architecture_gallery_claim_boundaries -v` checks snapshot separation, accessible layout, restricted-data containment and the non-verified status. The repository's quality and publication workflows must be consulted after this commit; this release document does not assert their eventual success.

Static HTML/CSS and the offline tests require **no ServiceNow licence**. Native Workbench and implementation-pack execution depend on App Engine/custom-table rights, roles/ACLs and any applicable ITSM, ITOM/Discovery, IntegrationHub/spokes, analytics, AI-provider or other third-party entitlements, confirmed against each target contract.

**Remaining:** 29 independent native acceptance cases not run for the separate baseline; no new production validation; 0 genuine screenshots authorised.

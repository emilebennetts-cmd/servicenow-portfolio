# Public reviewer navigation reconciliation

**Date:** 11 November 2026  
**Evidence class:** SOURCE-ONLY code and site changes  
**Security decision:** No repository-visibility changes; no restricted source or unapproved images published

## Why this matters
A hiring manager without repository permissions should not encounter a private GitHub 404 after choosing a portfolio evidence link. A public-safe summary is a navigation aid, not independent proof of the private implementation and not a substitute for a runtime test receipt.

## Implementation
Replaced 18 access-restricted GitHub anchors across six public HTML pages with context-relevant public-safe portfolio routes and corrected misleading labels:
- `diagnostic-case-study.html` — public Diagnostic case study, Knowledge Intelligence and architecture.
- `delivery-case-study.html` — governed-delivery case study, public release evolution, catalogue overview and Diagnostic cross-reference.
- `visual-evidence-intake.html` — public case studies instead of links labelled "Inspect public source".
- `engineering-evidence.html` — public architecture, engineering and Knowledge Intelligence summaries, with the traceability column accurately labelled as a public source-based summary.
- `workbench-experience.html` — public architecture summaries.
- `workbench-architecture.html` — public deployment/version boundaries.

The visual-evidence gallery itself was corrected earlier in this same release sequence. The new offline `scripts/test_public_reviewer_navigation.py` regression test guards all seven corrected pages against future private-repository deep links and checks local HTML destinations resolve.

## Evidence and limits
Public summaries intentionally disclose no private code, customer/client information, credentials, source-file IDs or screenshots. The public documents describe SOURCE-ONLY engineering, dated historical DEV-reported results and MOCK-ONLY flows where appropriate. They **do not** establish current DEV-VERIFIED or PRODUCTION-VERIFIED execution. 0 screenshots have publication approval.

## Acceptance
- A reviewer can navigate from the targeted public pages to local public case studies.
- A static test rejects links to access-restricted repositories and missing local HTML targets within the targeted pages.
- The site quality and deployment workflows must pass against the final release commit; live browser/device rendering remains separately scoped.

## Licensing
Static portfolio HTML and Python checks: no ServiceNow entitlement. Workbench runtime: custom app/App Engine rights and authorised roles; ITSM, ITOM/Discovery, IntegrationHub, Performance Analytics, AI and third-party connectivity entitlements depend on implemented scope.

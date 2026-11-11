# Public reviewer source-link closure — 11 November 2026

## Client's pain and history
The public portfolio had gradually accumulated direct links to access-controlled implementation repositories. These links cannot serve anonymous hiring managers, even when the referenced source is legitimate. Earlier fixes addressed only seven review routes, leaving restricted destinations on other engineering, architecture and verification pages.

## ServiceNow solution / implemented change
- Audited all **53 top-level public HTML pages** for anchor links to three restricted source repositories.
- Replaced **72 inaccessible anchors across 25 additional pages** with context-specific public evidence summaries, including Delivery architecture/release history, Diagnostic engineering, Knowledge Intelligence, patterns and integration boundaries.
- Reworded link labels to say **public summary/case study** rather than claiming a reader can inspect inaccessible private code.
- Added `scripts/test_public_private_repo_links.py`, an offline unit test scanning **all top-level HTML pages**, with case-insensitive and scheme-relative URL checks.
- Kept previous private evidence provenance and image-intake records out of public markup. This release exposes no private source and publishes no new images.

## Architectural best practices and verification
- Classification: **SOURCE-ONLY** website navigation and regression checks.
- Previously reported DEV tests remain historical, release-specific and **not independently re-executed**. Synthetic demonstrations remain **MOCK-ONLY**; **PRODUCTION-VERIFIED** is not established.
- The repository-backed Delivery source is 4.22.2; the historical DEV report applies to 4.20.0, not automatically 4.22.2.
- 0 screenshots approved or added; visual evidence still requires individual source authority, redaction, metadata cleanup and explicit publication approval.
- No repository visibility changes. Root public HTML is covered by the new test; future additions must pass CI. CI/Pages completion must be checked against the final commit SHA.

## Licensing / entitlement boundary
This public static website and its Python CI tests need **no ServiceNow licence**. Runtime custom applications may need App Engine/custom-app rights and platform roles. ITSM, ITOM, IntegrationHub/selected spokes, Performance Analytics, AI and third-party provider subscriptions remain **conditional on actually activated capabilities**.

## Commit lineage
Navigation batches: `70c8e40`, `d70e941`, `3c15508`. Final batch extends the root-level navigation test to the verification ledger and completes the 25-page closure. No runtime installation or publishing authority is implied by these commits.

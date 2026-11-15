# Workbench interface storyboards — 16 November 2026

## 1. The client's pain & history
The Delivery and Diagnostic source repositories and controlled user/training and Diagnostic completion runbooks span multiple dated release baselines. Public reviewers need a clear visual explanation of the Workbench journeys, but currently authorised, independently reviewed ServiceNow screenshot assets are not available for publication. A reconstructed interface must never be confused with a running instance or promoted to DEV acceptance.

## 2. The ServiceNow solution shipped
Updated [Workbench Source-to-DEV Gap Board](../workbench-source-dev-gap-board.html#evidence-gallery) with three accessible, responsive HTML/CSS-only screen storyboards:
1. Delivery — discover, review reusable patterns, design, test and hand over; linked to DEL-04/05.
2. Diagnostic — read-only evidence, rule evaluation and held draft finding; linked to DIA-02/03.
3. Cross-workbench — reference-only Diagnostic-to-Delivery intake subject to reviewer decision and access checks; linked to XWB-01/02.

Every scene explicitly says **MOCK-ONLY**. No live screenshot, customer or synthetic instance record, API call, external image, external script or third-party tracking is used. The existing 12 native gates and five conflicting historical observations remain **NOT RUN / HOLD**. Gallery discoverability was added to the portfolio homepage and searchable Explorer.

## 3. Architectural best practices
The storyboards separate concerns by scope, preserve review and approval boundaries, and illustrate an OOTB-first ServiceNow delivery process without implying direct data synchronisation. An illustrative diagram is not an installation receipt; the native tests still require authorised target identity, technical scope, installed version, synthetic transaction trace, negative-persona ACL evidence and independent approval.

**Evidence classification:** SOURCE-ONLY basis (source design/documentation), MOCK-ONLY visual reconstruction; historical DEV-REPORTED observations unchanged. New DEV-VERIFIED: **0**; PRODUCTION-VERIFIED: **0**. Original screenshot assets approved/published: **0**.

## 4. Quality controls
Extended Python and executable Node regression files to enforce exactly three labelled reconstructions, links to six native acceptance controls, accessible scene descriptions, responsive layout, no screenshot-like image elements or remote scripts, and retention of the original fail-closed CSV export. GitHub Actions outcomes must be checked independently after the commits; this document makes no unexecuted test claim.

## 5. Entitlements / licensing
Static HTML/CSS storyboards and browser-local exports require no ServiceNow licence. Native Delivery/Diagnostic deployment or acceptance may require App Engine/custom-table entitlements, correct roles and ACLs, and release-specific ITSM/ITOM subscriptions. IntegrationHub, ATF, AI, analytics and third-party integrations require separate scope and contract verification. No entitlement is inferred from a PDI or source repository.

## 6. Open blockers
Current authenticated DEV inventory/read-back, approved source-target package fingerprints, synthetic native acceptance, negative persona checks, independent reviewer, customer/legal permission for each original image, and screenshot-level sanitisation/approval remain open. No repository visibility or publication control has been changed.

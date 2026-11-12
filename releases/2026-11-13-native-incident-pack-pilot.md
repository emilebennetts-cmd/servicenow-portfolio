# Portfolio release — governed Incident pack native pilot
**Date:** 13 November 2026  
**Public case study:** [Incident pack native pilot](../incident-pack-native-pilot.html)  
**Evidence type:** PUBLIC SOURCE SUMMARY + HISTORICAL DEV-REPORTED + MOCK-ONLY PRESENTATION.  
**Publication:** Source-controlled public HTML; independent hosted HTTP and latest CI checks are not asserted by this document.

## 1. Client pain and history
Consulting deliveries using disconnected requirements, implementation guidance, backlog stories and tests struggle to explain which pack generated what, who reviewed it and whether the output was actually tested. Replaying generators can create duplicate drafts. A successful metadata read-back must not be interpreted as end-to-end business acceptance.

## 2. ServiceNow solution delivered to the portfolio
A responsive public case study provides a six-stage, keyboard-accessible tabbed explanatory journey (scope, recommendation, pinned version, generation, replay, acceptance), six evidence rows with status filters, bounded outcome counts and source-versus-runtime disclosures. A homepage feature, reviewer-guide entry and sitemap route support discoverability. The public verification manifest adds INCIDENT-PACK-PILOT (historical DEV-reported) as a distinct claim. Note: the register ID is the ASCII string `INCIDENT-PACK-PILOT`.

Historical 21 October source-controlled reporting supports four additive pack-flow schemas, no DELETE actions, 83/83 target metadata read-back checks, and a synthetic admin-led creation/replay of 36 linked drafts (eight requirements, eight stories, 20 *unrun* test designs). It does not establish persona, concurrent/recovery, client UAT, current source-target equivalence, approval or production acceptance. A separate 29-case native matrix remains unexecuted.

## 3. Architectural best practices
OOTB Incident/Change record authority is preserved. Pattern content remains subject to review, pinned version and entitlement checks. Source-only, historical DEV-reported, browser mock-only and production-verified claims are different evidence classes. No current DEV read-back or production verification is asserted.

**Controls implemented:** `scripts/test_incident_pack_pilot.py` validates the offline publication contract and link integrity. `scripts/browser_navigation_smoke.py` exercises the six-stage keyboard journey and evidence filters at four screen widths; the responsive workflow is configured to run both. Pass/fail requires actual CI completion, not mere source presence.

**Image control:** No genuine screenshot was embedded or approved; original images remain on publication HOLD. No customer data, private source or secrets are present on this page.

**Entitlements:** Static HTML needs no ServiceNow licence. Native implementation requires custom app/table allowances, appropriate roles and ACLs; ITSM/MIM, IntegrationHub, analytics, AI and provider subscriptions depend on the licensed target configuration.

## Outstanding gates
Inspect latest CI for failures, confirm hosted HTTP access separately, obtain current DEV persona/functional/recovery/ATF acceptance and approve genuine screenshots image by image. Do not promote historical demo evidence to current or Production verification.

# Workbench DEV claim-conflict reconciliation — 16 November 2026

## 1. The client's pain & history
The original gap board described the older 30 September controlled As-Built (4.6.1 source / 4.5.1 DEV) and repository-reported 5 October 4.20.0 DEV observation. A later controlled As-Built, with a 19 October evidence cutoff, describes a 6 October read-back of Delivery 4.22.2 and Diagnostic 0.4.2. The same later document warns that Delivery source 4.22.2 is **not represented as installed**. These are contradictory document statements, not a licence to certify a build.

## 2. The ServiceNow solution shipped
- Updated the mobile-responsive [Workbench Source-to-DEV Gap Board](../workbench-source-dev-gap-board.html#asbuilt-conflict) with two clearly marked historical conflict cards and an accessible closure checklist.
- Added a new browser-only five-row reconciliation CSV including the September, 5 October, 6 October and 19 October snapshots.
- CSV leaves target scope, target version, role, observation UTC and reviewer blank. Every row remains NOT RUN / HOLD; classifications are SOURCE-ONLY or DEV-REPORTED.
- The existing twelve-gate DEV acceptance CSV remains unchanged.
- Extended source-level Python checks and executable Node browser-model tests for conflict completeness, export controls, classification and empty private receipt fields.

## 3. Architectural best practices
The correct closure is an authorised read-back of exact installed application identity, technical scope, sys_id, version, candidate package fingerprint and per-persona native execution. Package / instance alignment cannot be inferred from a document date or matching version string. No DEV-VERIFIED or PRODUCTION-VERIFIED capability is introduced. No original screenshot or private document is published.

## 4. Verification
Source-level tests are committed for GitHub Actions execution; action result must be checked separately. No ServiceNow network request, storage, third-party script, unsafe image or synthetic-to-native status promotion was introduced.

## 5. Licensing / entitlement dependencies
Static HTML and browser-local exports need no ServiceNow licence. Instance inspection needs platform-owner access. Installation and runtime testing may require App Engine/custom application and custom-table entitlements plus relevant scoped roles; ITSM, ITOM/Discovery, IntegrationHub, ATF, AI and analytics rights must be confirmed by capability and contract, not assumed.

## 6. Open blockers
Current authenticated DEV installed-scope/version read-back, conflicting As-Built statement resolution, separate Diagnostic read-back, role/ACL testing, independent reviewer, target contract/entitlement approval and screenshot-by-screenshot publication permission remain open.

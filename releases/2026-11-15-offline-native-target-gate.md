# Offline native DEV target compatibility gate — 15 November 2026

**PUBLIC ARCHITECTURE UPDATE + PRIVATE TOOLING IMPLEMENTED; NATIVE ACCEPTANCE HOLD.**

## The problem
A source package can build successfully while the installed DEV application has an incompatible application scope, missing prerequisites, a different payload or unverified metadata. Historical DEV reports are not current read-backs.

## Actual implementation
A private, offline Python gate in the portfolio-control repository enforces canonical DEV/TEST target naming, exact source/target scope equality, candidate source commit, installed application sys_id/version, independent package SHA-256 declarations, zero delete actions, full declared prerequisites/metadata checks, controlled PRECHECK_ONLY reference and distinct native acceptance cases with opaque evidence refs.

The public source-target-compatibility page now explains the real control, failure modes and limits at #native-preflight, with a three-part client problem, ServiceNow solution and architecture decision narrative. It contains no actual target identifiers, private code, credentials, client records or screenshots.

Private CI synthetic regression passed on commit 350ff251808b581f29103ea57d4cd583aeaccba8: https://github.com/emilebennetts-cmd/servicenow-portfolio-control/actions/runs/43709272204
Private control validation passed: https://github.com/emilebennetts-cmd/servicenow-portfolio-control/actions/runs/43709272081

## Provenance and release boundaries
Read-only reference inputs: solution-lifecycle-studio handover and native-validation README; Diagnostic-Workbench2 build README; connected Google Drive Universal Delivery Workbench As-Built listing; existing private portfolio control register. Original private documentation and images were not republished.

- Private code and public explanation: SOURCE-ONLY.
- Synthetic sample/CI fixtures: MOCK-ONLY.
- Prior DEV observations: DEV-REPORTED only.
- Newly DEV-VERIFIED / PRODUCTION-VERIFIED: zero.
- Genuine public screenshot approvals: zero; HOLD.
- No authenticated DEV session, SDK install, update-set apply or Production change executed.

Public site CI and GitHub Pages for the public explanatory change must be confirmed separately. A clean offline receipt is always REVIEW_REQUIRED, never native acceptance, entitlement confirmation or deployment authorisation.

## Licensing and blockers
The public site and offline Python tool require no ServiceNow licence. Native application work requires target-specific App Engine/custom app and custom table rights, subscribed ITSM/ITOM and other product capabilities, roles and ACLs, and separate IntegrationHub/ATF/Now Assist/analytics entitlement checks.

Open: authenticated DEV target and platform-owner permission, exact package/source identity, fresh instance read-back, non-admin ACL/negative testing, evidence-review sign-off and original screenshot publication approval.

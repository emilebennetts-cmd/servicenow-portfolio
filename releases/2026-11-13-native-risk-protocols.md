# Native acceptance protocols — risk-first verification preparation

**Date:** 13 November 2026  
**Classification:** SOURCE-ONLY documentation and browser implementation; MOCK-ONLY interaction; publication **HOLD**.  
**Execution:** NOT RUN. **DEV-VERIFIED:** no new execution. **PRODUCTION-VERIFIED:** none.

## Client pain and historical limitation

The 43-item cross-Workbench assurance catalogue made missing tests visible but did not tell a reviewer how to prepare an executable, non-admin acceptance exercise, what a safe stop should look like, or which proof to retain. The historical 21 October synthetic Incident pilot cannot be reused as acceptance for a different source/target application identity. The 29 Delivery native tests in the private source matrix all remain Not run; the 14 Diagnostic QA requirements are **not** 14 passed ATF tests.

## Delivered source-only implementation

Extended the existing [Native Assurance Coverage Atlas](../native-assurance-coverage-atlas.html#execution-protocols) with nine concrete, source-derived, human-readable execution protocols:

| ID | Test purpose |
| --- | --- |
| NV-001 | Exact target, scope, version and licence identity |
| NV-007 | Deny privileged record creation to pre-sales persona |
| NV-009 | Prove cross-engagement isolation with non-admin identities |
| NV-014 | Confirm pinned replay is idempotent and retains edits |
| NV-020 | Verify unique constraints under concurrent create |
| NV-021 | Recover from isolated interrupted writes without duplicates |
| DX-02 | Reject unsafe, truncated or overexposed diagnostic evidence |
| DX-09 | Preserve baseline/rescan measurement comparability |
| DX-14 | Block unknown or absent optional product entitlements |

Each protocol supplies a persona, isolated prerequisites, test actions, expected result, evidence to preserve privately and an explicit stop condition. The interactive selector renders text safely and downloads a narrowly scoped, **blank JSON preparation ticket**. The export hardcodes NOT RUN, HOLD, no DEV or production verification, no screenshot approval, no sign-off and unspecified target/executor.

The catalogue retains the full 29 + 14 source populations without implying that the nine examples replace execution of the other scenarios. Native instances are not contacted, no customer data or original screenshot pixels are handled, and no private source code is reproduced. Added a Python publication-contract test and responsive Chromium coverage at 390, 768, 1024 and 1440 px.

## Architecture and quality gates

- Prefer OOTB controls, service-owner-approved test fixtures, ACL and non-admin persona testing, and private retention of dated native evidence.
- Plan concurrency and interrupted-write fault injection **only in an explicitly approved disposable non-production fixture**. Never simulate destructive recovery on a customer/shared instance.
- Unknown licensing or application identity means BLOCKED, never implicit acceptance.
- A download is only a work instruction; recorded native execution, independent review and approved promotion remain distinct.
- The synthetic Incident pilot is historical DEV-REPORTED for its own version; it does not upgrade these protocols to DEV-VERIFIED.

**Quality:** Source and browser tests were committed. GitHub Actions results and independent hosted availability require separate post-commit confirmation; they are not assumed here.

## Licensing and ownership

The GitHub Pages protocol selector needs **no ServiceNow licence**. Actual native test execution requires validated scoped application/App Engine and custom-table rights, suitable non-admin test roles and ACLs, authorised target environments, and ITSM, ITOM/Discovery, IntegrationHub, analytics, AI, provider or external system subscriptions only where the tested capability depends on them.

All screenshot candidate reviews remain on publication HOLD; zero image-specific releases have been authorised. Private repository visibility is unchanged.

# Public evidence ledger quality-gate recovery — 13 November 2026

## Problem
The existing GitHub Actions quality gate failed on the current published source revision `c5bed055828d`, even while the responsive browser smoke, site audit and GitHub Pages deployment workflows succeeded. The failure was in `scripts/test_verification_ledger_manifest.py`: the test asserted exact equality between a fixed list of 19 baseline evidence IDs and a public register that had legitimately grown to 21 entries.

## Implemented correction
- Added `INCIDENT-PACK-PILOT` and `SCOPE-COMPATIBILITY` to the reviewed baseline contract.
- Enforced an append-friendly **required-subset** check instead of a fixed, brittle exact catalogue equality.
- Added explicit duplicate-ID rejection and preserved each claim's public-page existence and runtime/publication-status checks.
- Preserved the critical provenance split: `INCIDENT-PACK-PILOT` is **DEV-reported** (historical, synthetic workflow); `SCOPE-COMPATIBILITY` is **source-only**. Neither is current independent DEV-verified or production-verified evidence.
- The corrected source is pinned to commit `80305b99fbbfc219b880d13bfdbd235bf440eb10`.

## Verification
- [Corrected public quality gate — passed](https://github.com/emilebennetts-cmd/servicenow-portfolio/actions/runs/43257533767).
- [Corrected public quality audit — passed](https://github.com/emilebennetts-cmd/servicenow-portfolio/actions/runs/43257533330).
- [Previous failing quality gate](https://github.com/emilebennetts-cmd/servicenow-portfolio/actions/runs/43248512467) failed only on a stale expected-ID equality assertion; this was an automated quality-process defect, not proof of runtime functionality.
- [Previous version's responsive Chromium smoke — passed](https://github.com/emilebennetts-cmd/servicenow-portfolio/actions/runs/43248512671).
- GitHub Pages for the original source commit [succeeded](https://github.com/emilebennetts-cmd/servicenow-portfolio/actions/runs/43248510900); this release note does not assert an independent hosted HTTP check.

## Assurance boundaries
This is a SOURCE-ONLY CI assurance repair. No native ServiceNow execution, app installation, customer UAT, production verification, screenshot sanitisation approval or external integration transaction was performed. Genuine source screenshots remain on HOLD; no pixels, private source or customer data were added.

## Entitlements
The static GitHub Pages site and quality checks need no ServiceNow licence. Native Workbench implementation requires confirmation of the target's App Engine/custom-application and table rights, platform ACL/role permissions, and any applicable ITSM, ITOM/Discovery, IntegrationHub, analytics, AI or third-party entitlements.

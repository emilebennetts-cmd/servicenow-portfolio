# 2026-11-09 — Publication gate regression repair

## Observed failure
The existing `Portfolio quality gate` run 42572539280 failed at `Test quality gate`: two synthetic approval tests used `screen.png` at the repository root, although the actual publication policy permits approved image paths only beneath `assets/screenshots/`. This is a fixture mismatch, not grounds to relax the screenshot publication boundary.

## Change
Updated `scripts/test_check_publication.py` to create synthetic image fixtures beneath `assets/screenshots/`, to record matching canonical manifest paths and to add a regression case that rejects a root-level approval. The production gate implementation and all approval requirements remain unchanged.

## Evidence and verification
- GitHub Actions failed run: https://github.com/emilebennetts-cmd/servicenow-portfolio/actions/runs/42572539280
- Source commit: a017bc2eb8b0650ca9542e7cd05dfc68f7e366c2
- Classification: SOURCE-ONLY until a subsequent GitHub Actions run confirms the repaired tests.
- No DEV-VERIFIED or PRODUCTION-VERIFIED ServiceNow claims.
- No screenshots, credentials, private repository content or customer data added.

## Follow-up
Confirm the next `Portfolio quality gate` conclusion; investigate any remaining static-check failures without weakening confidentiality rules. The static website itself requires no ServiceNow entitlement; custom application deployments and optional ITSM, ITOM, IntegrationHub, Performance Analytics and AI features require separate licence review.

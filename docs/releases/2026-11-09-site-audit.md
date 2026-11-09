# Public portfolio site audit — 9 November 2026

**Commit:** f5334475f8061852b10065f6d4d3e2b2cbfa9981  
**Classification:** SOURCE-ONLY; no fresh DEV or production verification.

## Delivered
Added `tests/audit_public_site.py`, an offline, standard-library-only auditor covering all HTML files under the public website root. Checks include page title, mobile viewport, single main landmark, duplicate DOM IDs, missing image alt attributes, local relative links and cross-page fragments, paths escaping the repository, and private-reference markers.

## Operation
Run `python3 tests/audit_public_site.py` to generate a JSON report without failing the command. Run `python3 tests/audit_public_site.py --strict` as a release gate; findings cause a nonzero exit code. Root-absolute and external URLs are not network-checked; the script deliberately does not fetch private assets.

## Verification boundaries
GitHub accepted the source commit. This run did not execute the audit against a full checked-out repository, verify GitHub Pages deployment, inspect private screenshots, or perform ServiceNow instance testing. Any discovered findings must be reviewed before enforcing strict mode in CI. Existing screenshot candidates remain HOLD pending provenance, redaction and publication approval.

## Entitlements
Static HTML and Python auditing require no ServiceNow licences. Deploying either Workbench requires authorised instance access and applicable custom-app entitlements. ITSM/ITOM, IntegrationHub, Performance Analytics, AI and third-party provider entitlements are separately assessed per customer contract.

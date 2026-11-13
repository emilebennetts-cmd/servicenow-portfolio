# Portfolio Explorer catalogue drift guard — 13 November 2026

**Classification:** SOURCE-ONLY website engineering. No ServiceNow DEV or Production execution, no original screenshot publication, and no newly granted rights.

## The operational problem

The public portfolio already exposes 72 root HTML pages including the Explorer. Its manually curated catalogue correctly linked the other 71 pages, but the directory heading still announced **69**. Previously, neither the source-quality gate nor publication audit guaranteed that new pages would be indexed in the searchable directory.

## Delivered implementation

- Added `scripts/reconcile_portfolio_explorer.py` with `--check` (read-only, exit nonzero on drift) and `--write` (append missing root pages using HTML-escaped titles and inferred categories; preserve existing hand-curated entries and search terms; reconcile counts).
- Rejects missing, duplicate and orphaned listings; invalid topic labels, empty link names, missing searchable filenames and stale hero/heading counts. Excludes nested files and filesystem symlinks.
- Updated the visible heading to **Search 71 published pages** (the page is intentionally not listed inside itself).
- Added five offline regression scenarios for stale counts, safe/escaped additions, duplicates, unpublished entries and symlinks.
- Wired the contract into **both** Portfolio quality gate and Portfolio quality audit workflows.
- The site's navigation, private image assets, repository visibility and runtime claim categories were not changed.

## Safe maintenance procedure

Run `python scripts/reconcile_portfolio_explorer.py --check` before release. If a new public root HTML page is intentionally added, run `python scripts/reconcile_portfolio_explorer.py --write`, inspect the inferred categorisation/title for accuracy, then re-run the check and commit the reviewed update. The script makes no network calls.

## Verification and evidence limits

- Source revision: `dffa8da688a1fa066b13939e3f9b16594ef8d0f0` (workflow wiring prior to this documentation commit).
- [Quality gate passed](https://github.com/emilebennetts-cmd/servicenow-portfolio/actions/runs/43344236000) at that revision.
- [Publication audit passed](https://github.com/emilebennetts-cmd/servicenow-portfolio/actions/runs/43344236130) at that revision.
- [GitHub Pages workflow](https://github.com/emilebennetts-cmd/servicenow-portfolio/actions/runs/43344235950) was in progress when inspected; final deployment and independently accessible HTTP still require their own confirmation.
- Functional checks apply to static website files and test fixtures only. SOURCE-ONLY implementation; browser-local mock case studies remain MOCK-ONLY; historical DEV claims remain DEV-REPORTED; no independently new DEV-VERIFIED or PRODUCTION-VERIFIED claim.
- No original Workbench image was published. Six inspected originals and ten indexed candidate positions remain separate controlled inventories; individual approvals: **0**.

## ServiceNow licensing and permissions

No ServiceNow entitlement is required for static GitHub Pages index functionality. Native Workbench testing remains conditional on appropriate App Engine/scoped-app and custom-table rights, role and ACL permissions, applicable ITSM/CMDB/ITOM/Discovery capabilities, and separate IntegrationHub/spoke/analytics/AI/provider entitlements where those features are used.

## Next evidence gates

Independent version-pinned DEV tests and case-specific native read-back; screenshot-by-screenshot provenance, irreversible redaction, rights review and explicit release approval. Do not interpret site CI as ServiceNow runtime proof.

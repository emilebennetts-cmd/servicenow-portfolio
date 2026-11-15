# Public receipt integrity: full-route, canonical-HTTP assurance — 15 November 2026

## 1. The client's pain & history

External HTTPS verification now has a successful independent workflow on 15 November 2026, but the reporting layer still exposed an integrity gap. The underlying checker examined twelve routes; however, the `write_summary` function could independently set `verified_live_public_website: true` when a caller supplied `success=True` with only one passing route. The stronger byte-identity field already rejected this. An incomplete or fabricated receipt must never be presented as website assurance.

## 2. The ServiceNow portfolio solution

Hardened the summary generator so the **live website** claim itself now requires the exact twelve-route inventory, no duplicate route IDs, `PASS` for every route, HTTP 200 and each route's precise canonical HTTPS URL. The **exact byte** claim additionally requires positive byte-equality decisions and syntactically valid lowercase SHA-256 digests for all twelve. Local-only, partial, redirected, duplicated or stale/missing-digest claims fail closed. The workflow job summary uses the same certified predicate instead of its former standalone success argument.

Added an explicit, mobile-friendly public delivery-assurance panel to the [90-second reviewer guide](../portfolio-review-guide.html#public-delivery-assurance). It points to the successful **earlier** commit-specific [live workflow run](https://github.com/emilebennetts-cmd/servicenow-portfolio/actions/runs/43676497715) and [GitHub Pages release](https://github.com/emilebennetts-cmd/servicenow-portfolio/actions/runs/43676497584) without treating those historical checks as proof of later commits.

Added negative unit cases covering missing routes, duplicate identities, wrong HTTP status, redirected/wrong URLs, non-PASS results, false byte equality and malformed digest fields. No private source, credentials, customer images or screenshot bytes are introduced.

## 3. Architectural best practices, test boundaries and entitlements

This is an auditability and ITIL 4 change-enablement control for the **public portfolio**, not a native ServiceNow runtime function. The public case studies remain SOURCE-ONLY where based on source documents, MOCK-ONLY for synthetic interactions and DEV-REPORTED for historical un-witnessed instance observations. No new DEV-VERIFIED or PRODUCTION-VERIFIED claims are introduced. Original screen publication remains at **0 approved — HOLD**.

**Validation gate:** Unit tests and source/site quality workflow must pass after commit; repeat the live twelve-route check against the new source SHA and confirm GitHub Pages deployment. Until then, the dated run above is the only confirmed byte-equality evidence.

**Licensing:** No ServiceNow entitlement for the static website, Python standard-library verification or GitHub Actions. Native workbench installation and testing require authorised instance access, appropriate scoped custom-app/App Engine rights, roles/ACLs and any underlying ITSM/ITOM/CMDB, IntegrationHub, ATF, AI, analytics or third-party entitlements depending on the actual target design. Commercial terms and current native DEV/Production verification are not established.

**Privacy:** Private repositories and Drive originals remain restricted. No public screenshot was approved or published.

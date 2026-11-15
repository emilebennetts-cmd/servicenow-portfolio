# Public portfolio HTTPS delivery smoke — 15 November 2026

## 1. The client's pain & history

The portfolio has had multiple successful GitHub Pages deployment jobs, but those jobs alone did not independently prove an anonymous external reader could retrieve the main website or individual case studies. Available local and web checks could not resolve or retrieve the public Pages host. A successful source-quality check or an installed ServiceNow release is a separate kind of evidence.

## 2. The ServiceNow portfolio solution

Added an automated anonymous HTTPS smoke to the public CI:
- A unique, non-sensitive publication probe on the landing page distinguishes a deployed current source revision from a stale Pages copy.
- Four exact URLs are requested using a standards-based TLS client: portfolio root, Delivery release evolution, Diagnostic Workbench case study, and the visual-evidence gallery.
- Each response must be HTTP 200, HTML, served from the expected HTTPS host and path, and contain its page-specific marker.
- Retries allow for GitHub Pages propagation. The published workflow can be dispatched manually and runs on relevant main-branch commits.
- A machine-readable JSON receipt records only public URLs, route status, the source commit and an explicit verified-live-website boolean. It never captures HTML bodies, secrets, cookies, client data or screenshots.
- A failure is UNCONFIRMED, not proof of a native ServiceNow defect. The workflow is not a website uptime service.

## 3. Architectural best practices / test boundaries / entitlements

The Python verifier is standard-library-only; local regression tests cover strict origin/path/TLS checks, missing markers and fail-closed receipts. The local preflight is clearly LOCAL-ONLY. **GitHub workflow existence is not evidence of a passing live check**; use the workflow run and attached redacted receipt to confirm the real outcome. The live verification report must not be interpreted as DEV-VERIFIED or PRODUCTION-VERIFIED ServiceNow functionality.

All source architecture remains SOURCE-ONLY. Historical DEV documentation remains DEV-REPORTED pending native reconciliation. Existing demonstration interfaces remain MOCK-ONLY. Independent native DEV, Production acceptance, and original screenshot-publication approvals remain HOLD.

**Licensing:** The static GitHub Pages verification requires no ServiceNow licence. Live scoped-application deployment requires authorised App Engine/custom-app entitlements, roles/ACLs, relevant ITSM/ITOM/CMDB/other product subscriptions, and IntegrationHub, AI, analytics, ATF or third-party rights when features actually require them.

**Publication controls:** No change to private repository visibility; no confidential source, client information or unreviewed screenshot is included. The smoke is strictly browser-site delivery assurance, not a functional native instance verification.

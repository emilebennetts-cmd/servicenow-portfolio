# Public portfolio twelve-route deep-link assurance — 15 November 2026

## 1. The client's pain & history

A healthy GitHub Pages deployment and a four-route anonymous HTTPS smoke provided initial proof that the portfolio could be opened. They did not check important deep links for the Delivery case study, reusable pattern governance, Diagnostic-to-Delivery handoff, CMDB/IRE, greenfield ITSM, Knowledge Intelligence intake, evidence register or 90-second reviewer guide. An accessible homepage alone cannot guarantee a prospective client or hiring manager can reach the technical narrative they need. The earlier URL validator also compared the final hostname/path without explicitly rejecting unexpected port, URL credentials or query/fragment drift, and accepted Content-Type values merely containing the string `text/html`.

## 2. The ServiceNow portfolio solution

Extended the standard-library anonymous HTTPS release smoke from **4 to 12** source-backed pages, preserving the original four. Added eight exact, page-specific public-content markers across the end-to-end consulting story: governed Delivery Plan; reusable patterns; cross-workbench diagnostic handoff; CMDB/IRE; ITSM greenfield sequencer; 180-case KI matrix intake; technical evidence register; and 90-second reviewer route.

The probe now fails closed on noncanonical request URLs, unexpected redirect credentials/ports/query/fragment, incorrect MIME types, non-200 responses, failed TLS/host/path constraints and missing content markers. Existing propagation retries, bounded HTML reads, UTF-8 enforcement and redacted JSON evidence receipts remain unchanged. GitHub Actions automatically rechecks these paths when corresponding HTML files or the verifier change.

The offline contract now has four tests, including exact route-set coverage and negative URL cases; it cannot promote native ServiceNow evidence by design.

### Independent execution receipt

- Workflow: [Anonymous public portfolio HTTPS smoke — run 43672363794](https://github.com/emilebennetts-cmd/servicenow-portfolio/actions/runs/43672363794), source commit `9557768fca7ef4f0bc017b0111a28113bddab4e9`, completed successfully 15 November 2026 UTC.
- Local source marker preflight: **12/12 PASS**.
- GitHub-hosted anonymous live GET verification: **12/12 PASS**. Each route returned HTTPS HTTP 200, exact expected path and an expected public HTML marker. Four offline contract tests passed. The published JSON report explicitly reports `verified_live_public_website: true` and both native ServiceNow verification booleans false.
- Workflow artifact: `anonymous-public-https-receipt` (30-day retention), containing public URLs/status only. HTTP delivery assurance does not prove interactive control behaviour, accessibility, browser rendering, ServiceNow installation or production functionality.

## 3. Architectural best practices, safeguards and entitlements

Keep source-release claims, historical DEV statements, public static demonstrations, current native verification and production acceptance as **separate assurance domains**.

- **SOURCE-ONLY:** referenced Delivery/Diagnostic source architecture and technical capability declarations.
- **DEV-REPORTED:** historical release evidence, not independently reproduced by this verifier.
- **MOCK-ONLY:** interactive browser examples and illustrative flows.
- **LIVE WEBSITE DELIVERY VERIFIED:** all twelve selected public URLs on this specific GitHub-hosted run, distinct from functional browser and native evidence.
- **DEV-VERIFIED / PRODUCTION-VERIFIED:** no new claims; native execution is still HOLD.
- **Genuine screenshot publication:** no individual release approval is asserted; HOLD. No private source or image bytes were exported.

**Licensing:** The public static website, offline Python tests and GitHub-hosted HTTPS checks require no ServiceNow licence. Real target-instance validation requires approved custom scoped app/App Engine entitlements as applicable, roles and ACLs, the client's subscribed ITSM/ITOM/CMDB/ITAM/etc. capabilities, and separately evaluated IntegrationHub, ATF, AI, analytics and external-provider rights.

**Limitations:** This is a sampled twelve-route deep-link acceptance check, not a continuous uptime or exhaustive crawl. Stale pages can be served successfully if their stable markers remain; release identity is checked only for the versioned homepage probe. Original screenshot approval, independently witnessed DEV read-back and production acceptance are still required before any stronger claim.

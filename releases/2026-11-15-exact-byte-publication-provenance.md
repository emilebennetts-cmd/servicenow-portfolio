# Exact-byte publication provenance — 15 November 2026

## 1. The client's pain & history

The prior release independently reached twelve GitHub Pages URLs over HTTPS and inspected a page-specific marker in each response. A previously published version could nevertheless contain that same stable marker and be accepted as current. That is a **deployment freshness defect**, not a ServiceNow runtime defect: successful HTTP delivery did not prove that the website served the exact source files from the reviewed commit.

## 2. The ServiceNow portfolio solution

The anonymous HTTPS checker now reads each HTML target from the GitHub Actions checkout associated with `GITHUB_SHA`, computes its SHA-256 digest and compares it with the bytes returned by the published GitHub Pages route. It retains the existing HTTPS, origin, port, URL, HTTP status, HTML MIME, UTF-8 and page-marker controls.

The release fails closed if a published page has **the right marker but different bytes**. Propagation retries continue to handle ordinary publication delays. All twelve representative journeys are covered. Receipts contain only the public route, the public HTML digest, an exact-match boolean and outcome; they contain **no HTML bodies, cookies, credentials or private source**.

New receipt field `verified_exact_deployed_bytes` is true only when a successful **live** inspection covers the full twelve-route set and every route reports `bytes_match_checkout: true`. Offline checks and partial/synthetic passing records cannot set it. The existing `verified_live_public_website` flag continues to refer to anonymous URL delivery, a separate assurance level.

### Verification / change record

- Implementation: [SHA-256 equality gate](https://github.com/emilebennetts-cmd/servicenow-portfolio/commit/185e2478b9764839d41c5e7434dbbf0e6094ea51)
- Regression tests: [same-marker stale-page negative case, full-set receipt predicate and offline rejection](https://github.com/emilebennetts-cmd/servicenow-portfolio/commit/67828be55c595a54890c86f9de2360eafff3c354)
- GitHub workflow: [explicit byte-matching step](https://github.com/emilebennetts-cmd/servicenow-portfolio/commit/a61cc626797cdac8f4a7e170b497b6ab1db3a09b)
- Independent execution subsequently reviewed on **15 November 2026 at 04:22 UTC**: [exact-byte HTTPS workflow 43676497715](https://github.com/emilebennetts-cmd/servicenow-portfolio/actions/runs/43676497715) succeeded at source commit `828f17a33f526889204c353572dc01ebe816336a`; its anonymous-site job passed the offline, local and twelve-route SHA-256 comparison steps. [GitHub Pages deployment 43676497584](https://github.com/emilebennetts-cmd/servicenow-portfolio/actions/runs/43676497584) also succeeded for that commit. This is a dated website-delivery result, not native ServiceNow acceptance or proof that subsequent commits have deployed.
- Scope limitation: HTML bytes only, not independently re-fetched embedded CSS/JS/image dependencies, browser rendering, accessibility, interactive behaviour or hosting uptime. Source identity is tied to the workflow checkout and does not attest to a native ServiceNow package.

If GitHub Pages transforms an HTML file after checkout, the checker intentionally fails rather than silently accepting a semantically similar version. Investigate the publishing pipeline and document any canonicalisation before relaxing this control.

## 3. Architectural best practices, evidence and entitlements

This is a release control aligned with change enablement, configuration identification and traceable acceptance. It prevents a source-only page marker from being incorrectly presented as deploy-fresh proof.

- **SOURCE-ONLY:** the reviewed Delivery and Diagnostic Workbench source architecture; SHA-256 checker implementation and tests until independently executed.
- **MOCK-ONLY:** public illustrative Workbench journeys, interactive preflights and synthetic scenarios; unchanged.
- **DEV-REPORTED:** historical statements in private source/runbooks, not independently repeated here.
- **LIVE WEBSITE DELIVERY / BYTE IDENTITY:** only claim on the basis of a successful dated public workflow receipt.
- **DEV-VERIFIED / PRODUCTION-VERIFIED:** no new ServiceNow runtime execution. Both remain unverified.
- **Screenshot approval:** original images remain on HOLD; this change does not use, publish or approve any private screenshot.

**Licensing / entitlements:** The static portfolio, standard-library Python checker, GitHub Actions runner and public SHA-256 comparison need no ServiceNow licence. Native validation would require authorised instance access, appropriate custom scoped application/App Engine rights, roles and ACLs, relevant ITSM/ITOM/CMDB/IRM subscriptions, and any applicable IntegrationHub, ATF, AI, analytics or external-system entitlements. Confirm contractual terms against each target environment.

**Remaining gates:** Review actual workflow output; independently witnessed current DEV release read-back, production acceptance, customer-specific entitlements and image-by-image sanitisation, rights and publication decisions. Private repository visibility remains unchanged.

# Release — searchable ServiceNow portfolio explorer

**Date:** 13 November 2026  
**Classification:** SOURCE-ONLY site implementation; MOCK-ONLY browser interactions  
**Native ServiceNow DEV/Production acceptance:** Not performed  
**Genuine screenshot publication approvals:** 0 / HOLD

## Client pain and history

The portfolio had accumulated dozens of public case studies, labs, evidence controls and technical walkthroughs. A reviewer could open the 90-second route, but discovering a particular CMDB, ITSM, Diagnostic, architecture or assurance page required navigating a large homepage directory. Important technical evidence was easy to miss.

## Implemented solution

- New responsive [Portfolio Explorer](../portfolio-explorer.html), generated against the actual tracked public HTML file inventory before this release: **68 existing pages**.
- Four purpose-built reviewer pathways: hiring manager, technical architect, ServiceNow delivery and CMDB/diagnostics.
- Browser-local text search, topic filter, live matching count, 18-result initial limit, show-all control and reset. No network requests, ServiceNow login, local storage or analytics.
- Indexed links are actual public page paths, not links to private repositories or unapproved Drive attachments.
- Connected the homepage mobile directory, 90-second review and XML sitemap.
- Added standalone publication-contract and four-viewport Chromium interaction tests to the existing GitHub quality workflows.

## Architecture and verification boundaries

The index lists pages; it **does not** certify them. SOURCE-ONLY documents/code, MOCK-ONLY interactive demonstrations, historical DEV-REPORTED outcomes and required independently DEV-VERIFIED/PRODUCTION-VERIFIED evidence remain distinct. The visual gallery continues to withhold original captures pending case-by-case provenance, sanitisation and approval. Neither the website nor tests publish screenshots.

This is a static site: **no ServiceNow licence** required. Native Workbench deployment depends on App Engine/custom app and table entitlements, roles and ACLs, plus product-specific ITSM, ITOM/Discovery, ITAM, SecOps, IntegrationHub, AI, analytics and external-provider licences as applicable.

## Acceptance evidence and open gates

- Source commit and test implementation are recorded in GitHub history.
- CI and Pages verification must be checked at the final commit; do not treat committed workflow code as a passing run.
- No new native DEV run, production read-back, customer-specific data or approved screenshots.

## Source controls

Public GitHub repository directory listing was used to generate the catalogue; private Delivery and Diagnostic source documentation and connected Google Drive source inventory were reviewed for boundaries. No private files, source text, customer materials or Drive links were copied to the published directory.

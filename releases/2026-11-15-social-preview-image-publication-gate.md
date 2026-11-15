# Social-preview screenshot publication control — 15 November 2026

## 1. The client's pain & history
A static page can have no visible screenshots but still advertise a screenshot to social-media and link-preview crawlers using Open Graph, Twitter Card or legacy image metadata. Browser content security policy does not necessarily govern crawlers. The previous publication guard validated approved image bytes and blocked common visual embeds but did not inspect these specific metadata fields. This is a preventive control improvement, not evidence that an incident occurred.

## 2. The ServiceNow solution
Enhanced the portfolio's existing offline publication gate to parse social image declarations independent of attribute order. The gate accepts only repository image paths covered by the explicit SHA-256 approval manifest; absolute URLs must be HTTPS on the portfolio's canonical GitHub Pages origin and under the portfolio base path. It rejects unapproved image URLs, remote origins, data URLs, changed byte hashes, non-canonical ports, query strings and fragments.

The published screenshot checklist now explicitly describes the additional social-preview condition. Seven negative/positive regression scenarios test remote Open Graph, unapproved Twitter/structured image metadata, approved same-origin Open Graph/Twitter previews, legacy `image_src` links, alternate ports, query strings, duplicate attributes and malformed URLs. This change publishes **no screenshots** and does not modify repository visibility.

## 3. Architectural best practices & verification
A SHA-256 allowlist is a release safeguard, not an image reviewer. The actual screenshot's redacted pixels, capture authority, scope/version identity and publication rights still require independent human approval. The guard does not make a source artefact a DEV-VERIFIED or PRODUCTION-VERIFIED runtime result. Public source descriptions remain SOURCE-ONLY; demonstration interactions remain MOCK-ONLY; historical DEV statements remain DEV-REPORTED.

The guard is executed by the existing `portfolio-quality.yml` workflow through the full regression suite and `python scripts/check_publication.py`. CI and live deployment need their own completed receipts before claiming passed verification. No client-specific native ServiceNow testing occurred in this change.

## Licensing and entitlements
No ServiceNow licence is needed for the static page, social metadata inspection or CI. Actual Workbench installation and native acceptance require authorised target access, appropriate App Engine/custom scoped application entitlements, roles/ACLs, subscribed ITSM/ITOM/CMDB products and independently validated IntegrationHub, ATF, AI, analytics or other relevant integrations.

## Outstanding review gates
- Individual original image publication approval: **0 / HOLD**.
- Current DEV acceptance and independent production verification: not performed.
- Customer product subscription and feature entitlement verification: unresolved.

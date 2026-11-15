# Responsive image publication safeguard — 15 November 2026

## 1. Client pain and history
The public portfolio has a conservative screenshot approval gate. However, responsive image markup can select a second srcset candidate not visible from an ordinary img.src check. Image preload declarations, input-image elements and video posters are additional publication paths. These are preventive gaps, not evidence that customer images were exposed.

## 2. ServiceNow portfolio solution
The new HTMLParser-based ResponsiveImageInspector checks img src/srcset, source srcset, input type=image, video poster and image preloads (href and imagesrcset). Each reference must match a canonical, SHA-256-approved screenshot path. Remote third-party hosts, alternate ports, URL credentials, query/fragment variants, percent-encoded paths, malformed srcset descriptors and ambiguous duplicate attributes fail closed.

Eight positive/negative unit tests were added. Only synthetic test bytes were used; no private image was uploaded.

## 3. Architectural best practices and acceptance
- Publication approval stays scoped to the exact image bytes and URI. Existing separate controls inspect file signatures and known metadata markers.
- CI is a heuristic static guard, **not** screenshot redaction, exhaustive browser security analysis, native acceptance, or legal publication approval.
- Evidence class: SOURCE-ONLY code and tests; MOCK-ONLY synthetic fixtures. No current DEV-VERIFIED or PRODUCTION-VERIFIED assertion.
- New approval receipts: none. Original screenshot publication remains HOLD.
- Required verification: run the public quality and security workflows, inspect published HTML by HTTPS, then complete individual image/caption rights review before any image release.

## Licensing and entitlement dependencies
The static public site and standard-library Python validation require no ServiceNow licence. Delivery/Diagnostic Workbench native use remains subject to custom scoped-app/App Engine rights, permitted user roles and ACLs, and target-specific ITSM/ITOM/CMDB subscriptions. IntegrationHub, ATF, Now Assist/AI, analytics and third-party integrations require separate entitlement checks where applicable.

# Verification ledger reconciled to one public claim register — 12 November 2026

## 1. The client's pain and history

The public verification matrix was a hand-maintained nine-card snapshot last reviewed on 6 November, while the JSON verification manifest omitted newer interactive MIM and CMDB labs and screenshot utilities. This created claim drift: browser-tested public demonstration code might appear without a corresponding runtime-evidence boundary. This is a portfolio governance problem, not a customer-specific incident.

## 2. ServiceNow portfolio solution delivered

- Added five source-grounded records to `evidence/public-verification-register.json`: CMDB Trust Lab, MIM readiness lab, privately inspected Workbench observations, browser-local Screenshot Redaction Desk, and independent Screenshot Receipt Verifier. The register now contains **13 claims**, including **four MOCK-ONLY entries**.
- Rebuilt `verification-ledger.html` as a responsive, searchable public view of the JSON manifest. It uses safe DOM text nodes rather than HTML interpolation, explicit classification, runtime and screenshot boundaries, local public-page links, and a clear error state when the manifest cannot load.
- Added filters, record counts and keyboard-operable controls. Zero production-verified Workbench claims and zero approved genuine images remain explicit.
- Connected the Delivery and Diagnostic case studies and the Visual Evidence Gallery to the claim ledger, using statically resolvable links.
- Added standard-library CI assertions for manifest coverage and privacy posture, plus Chromium assertions at 390px, 768px, 1024px and 1440px using loopback HTTP to exercise real JSON loading.

**Not published:** customer records, restricted repository content, Google Drive identifiers, image bytes, captured private SHA-256 digests, instance credentials or screenshots on HOLD. Source-document DEV statements remain historical and are not promoted to newly DEV-VERIFIED.

## 3. Architectural best practices and acceptance boundary

The JSON manifest remains the authoritative non-sensitive claim catalogue; public HTML is a presentation layer. Static CI validates target local pages and evidence classes. Browser testing demonstrates website behaviour only. It does **not** establish live ServiceNow collectors, installed custom application releases, authenticated provider synchronisation, DEV acceptance or production deployment.

The change was based on a fresh review of the two private Workbench repository READMEs and the private evidence crosswalk, plus Google Drive metadata discovery of existing Universal Delivery As-Built, Architecture and related source holdings. No new original screenshot pixels were cleared or published.

### Evidence classification

| Asset | Classification | Boundary |
| --- | --- | --- |
| Public ledger, claim manifest, static and browser tests | SOURCE-ONLY / website browser-tested | No native ServiceNow runtime evidence |
| CMDB, MIM and ITSM interactive decision labs | MOCK-ONLY | Synthetic fixtures, not ServiceNow ATF or production outcomes |
| Historical Workbench instance reports | DEV-REPORTED | Dated source claims, not newly revalidated |
| Six privately inspected source captures | SOURCE observation, some MOCK-ONLY content | All publication HOLD; no image rights approval |
| Production-verified Workbench features | None | Requires authorised operational evidence |

### ServiceNow licensing / entitlements

No ServiceNow licence is needed for the static portfolio, public JSON or local browser tools. Real custom scoped Workbench deployment requires entitlement/role/ACL assessment. ITSM/MIM, App Engine, CMDB/ITOM Discovery, IntegrationHub, analytics, AI and third-party provider features require contract-specific validation. Screenshot publication permission is separate.

## Release verification

At implementation commit `9787a4790ec0d7406d2b9257aee6c1cd183056b6`, the portfolio quality gate, quality audit and four-viewport Chromium smoke suite passed. Subsequent case-study navigation links were refined after static local-link checks identified dynamically created fragment IDs as unsuitable for static target resolution; the final links use the public ledger page URL. CI and deployment must be confirmed against the **final main SHA**, rather than inherited from an earlier implementation commit.

No external-site HTTP response or live native ServiceNow verification is asserted.

# Entitlement and Deployment Readiness Gate — 14 November 2026

**Classification:** SOURCE-ONLY website implementation; MOCK-ONLY interactive review filtering and exported worksheet.
**Native DEV/Production:** NOT VERIFIED. **Publication:** UNREVIEWED / HOLD. **Original screenshots:** none approved.

## 1. The client's pain & history
ServiceNow consulting and platform teams can conflate an attractive source demonstration with installed modules, licensed users, custom-table rights and completed native acceptance. The two Workbench source applications and the separately observed demo7 target have different scope identities; neither website deployment nor historical DEV reports establish current target readiness. This is a generic consulting scenario, not an assertion about any client.

## 2. The ServiceNow solution implemented
Added a responsive public page [Entitlement & Deployment Readiness](../entitlement-readiness.html) with eight source-bounded review areas across core website, custom scoped applications, Diagnostic/Knowledge Intelligence, ITSM, CMDB/IRE/Discovery, IntegrationHub, analytics/AI, and ATF. Four filters separate platform, operations and extension reviews. An offline JSON export is generated entirely within the browser, from the currently visible public cards only, and always states UNREVIEWED / NOT VERIFIED / HOLD.

Updated public homepage directory, 90-second review, implementation-boundary page, Portfolio Explorer and XML sitemap to expose the page. Added static unit tests against the page, its security policy, eight unique review areas, export approval invariants and discoverability.

## 3. Architectural best practices
- Preserve the distinct source scopes `x_1577958_vdf` and `x_1577958_dw2` versus independently observed demo7 `x_eitsp_vdf`. Do not infer that 4.22.2 source was deployed merely because a historical DEV baseline exists.
- OOTB-first: use native ITSM, IRE, ACLs, Subscription Management and versioned approvals where appropriate, then add justified scoped extensions.
- Licensing: the static GitHub Pages portfolio needs no ServiceNow licence. Native components require contract-specific confirmation of custom-app and table entitlements, user roles, ITSM, ITOM/Discovery, IntegrationHub/spokes, analytics/AI, third-party products and any relevant ATF/feature rights.
- No contractual decision, product activation, ServiceNow connection, target deployment or independent native verification occurs on the website.
- No private source, customer inventory, credentials or unreviewed screenshots are embedded. Export is an unauthorised review prompt and cannot award sign-off.
- General custom-table guidance is drawn from current ServiceNow documentation:
  - https://www.servicenow.com/docs/r/platform-administration/table-administration-and-data-management/custom-tables.html
  - https://www.servicenow.com/docs/r/platform-administration/allocating-custom-tables-subscr-apps-v2.html
- Source context inspected: restricted Delivery and Diagnostic repository README files, private portfolio-control README and public evidence/implementation pages. Do not repeat restricted code in public.
- Website quality and deployment must be validated separately against GitHub Actions final release SHA. Native DEV acceptance and Production acceptance remain open.

**Open blockers:** Customer-specific licence/legal schedule validation, target-instance access and native testing, independent release acceptance, and individual screenshot approval.

## Release reconciliation and independent test boundary

- Final public register contains **89 classified claims**: 56 SOURCE-ONLY (including this site gate), 20 MOCK-ONLY, 9 PROPOSED and 4 historical DEV-REPORTED. Zero independent native DEV-VERIFIED or PRODUCTION-VERIFIED.
- **76 indexed HTML case-study pages** plus homepage appear in the uniquely sorted public sitemap; public Portfolio Explorer summary matches the index.
- `scripts/browser_entitlement_readiness.py` and `.github/workflows/entitlement-readiness-browser.yml` exercise four responsive widths, switching domains, browser-local JSON export, false approval flags and zero remote requests.
- Static unit tests also assert the single source-only claim and future-proof sitemap/index equality.
- Connector read-back and structural invariants passed; independent execution of the new Chromium workflow and final GitHub Pages HTTP retrieval could not be confirmed in this environment. Treat both as **NOT CONFIRMED**, not as a native or website release acceptance.

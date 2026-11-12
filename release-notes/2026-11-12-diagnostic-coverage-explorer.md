# Diagnostic collector coverage and evidence chain — 12 November 2026

**SOURCE-ONLY implementation; MOCK-ONLY synthetic cases. No new DEV or production verification.**

## 1. Client pain & history
Representative platform reviews mix absent modules, incomplete groupings and unreviewed aggregates. Without explicit applicability, missing values risk being treated as healthy systems.

## 2. ServiceNow solution
Implemented a responsive standalone coverage explorer with 20 source-summarised collector families and ten domain filters; acceptance questions; a six-stage evidence lifecycle; four safe synthetic decisions; and HOLD-only JSON examples. Original scripts, thresholds, customer values and screenshots were excluded. Source review of Diagnostic Workbench 2 catalogue on 12 November 2026 found 20 collectors, 42 rules, four correlations, 67 runbooks and ten packs. The separate wider knowledge catalogue is not additive. Navigation, sitemap, evidence register, static and four-viewport Chromium contracts are updated.

## 3. Architectural best practices and proof
Unknown/-1 values stay NOT_ASSESSED, truncated groups stay HOLD_COMPLETENESS and potentially sensitive data is REJECT_UNSAFE_PAYLOAD. Even a complete synthetic envelope is REVIEW_REQUIRED; no native collector execution. Historical 1 September DEV testing described in source is DEV-REPORTED only, not fresh DEV-VERIFIED. No production-verified results. Original screenshots remain publication HOLD.

Native assurance requires installed module/entitlement assessment; least privilege; negative ACL tests; bounded read-only aggregate collection; source window/denominator and truncation reconciliation; envelope/PII checks; analyst acceptance; and change authorisation. Compare with OOTB CMDB Health where applicable.

Public page: no ServiceNow licence. Native ITSM, ITOM/Discovery, SecOps, IRM, CSM, HRSD, HAM/SAM, IntegrationHub or external providers may require contractual entitlements, role and table access.

Official references: https://www.servicenow.com/docs/r/api-reference/server-api-reference/c_GlideAggregateAPI.html and https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/overview-cmdb-health.html .

Static quality and Chromium CI need exact-commit verification after release. No confidential source, customer information, private URLs or unapproved images were published.

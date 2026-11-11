# CMDB Diagnostic Trust Lab — public release record

**Release date:** 12 November 2026  
**Public entry:** [Interactive CMDB Trust Lab](../cmdb-diagnostic-trust-lab.html)  
**Related source review:** [CMDB & IRE Assurance](../cmdb-ire-assurance.html)  

## Client pain and history

A read-only CMDB collector may return superficially green results when it silently caps grouped enumeration, converts missing inputs into zero, or double-counts relationship gaps. A screenshot or static architecture diagram alone does not demonstrate safe handling of those conditions.

## ServiceNow solution and implementation

Added a standalone, accessible and mobile-responsive **synthetic fixture laboratory** with five deterministic scenarios:

1. Complete baseline (PASS within the fixture only).
2. Grouping limit reached (PARTIAL; observed counts are not population totals).
3. Source table unavailable (NOT ASSESSED; unknown must not become zero).
4. Overlapping parent/child gaps (REVIEW; union counts each row once).
5. Ownership and freshness gaps (REVIEW; human action is required).

The fixture receipt contains only code-embedded synthetic counts and scenario metadata; it performs no ServiceNow queries, API calls, credential handling, data storage or external export. The lab's logic mirrors the architectural concerns identified during the private collector source review without copying private implementation code.

**Files:** `cmdb-diagnostic-trust-lab.html`, `scripts/test_cmdb_trust_lab.py`, plus browser smoke test integration in `scripts/browser_navigation_smoke.py`, `index.html`, `cmdb-ire-assurance.html`, sitemap and CI workflow.

## Architectural best practices

The lab never claims to duplicate the actual ServiceNow collectors. Its arithmetic deliberately corrects overlapping relationship gaps using `missingParent + missingChild - bothMissing` and preserves source-unavailable and capped scan confidence states. In a real engagement, verify query compatibility and read rights on an authorised DEV instance; cross-check with OOTB CMDB Health, IRE, CI Class Manager and CSDM; attach release-specific execution receipts before asserting success.

## Verification and publication controls

- **SOURCE-ONLY:** Static website source, synthetic logic and regression tests committed.
- **MOCK-ONLY:** All fixture values and the interactive result interface.
- **DEV-VERIFIED:** None newly established. Historical source-reported DEV receipts do not apply to this lab.
- **PRODUCTION-VERIFIED:** Not established.
- **Screenshot status:** No screenshot content published or ingested; reviewed Google Drive screenshots remain on HOLD pending provenance, redaction and explicit approval.
- **Static tests:** Python unittest contract checks structure, confidentiality, categories and local targets.
- **Dynamic tests:** Chromium/Playwright exercises all five decisions at 390, 768, 1024 and 1440 px in GitHub Actions; record workflow result independently when complete.
- **Deployment:** GitHub Pages is the publication route; record actual successful deployment run separately from the source commit.

## Licensing

Static web content requires **no ServiceNow licence**. An actual collector requires authorised instance access and ACLs. CMDB Health, Discovery/ITOM Visibility, Service Graph connectors, custom App Engine applications, IntegrationHub/spokes and optional products must be assessed against the customer's relevant ServiceNow release and contracted entitlements.

## Rollback

Revert the new page and test, remove the homepage/source-case-study links and sitemap entry, and revert the browser-workflow trigger and smoke-test checks. No customer data or platform records are altered.

# Entitlement Readiness — Browser-Only Follow-up Triage

**Date:** 14 November 2026 · **Classifications:** SOURCE-ONLY (published page/code), MOCK-ONLY (reviewer interaction). **Native DEV / Production:** NOT VERIFIED. **Original screenshots:** 0 approved, HOLD.

## 1. The client's pain & history

A static licence-readiness checklist leaves platform leads with no quick way to separate unassessed dependencies from requested evidence, explicit entitlement gaps and material staged for independent review. A demo alone cannot establish purchased rights, available functionality or release approval. This is a representative consulting problem, not a statement about a particular customer.

## 2. The ServiceNow solution implemented

Extended [Entitlement & Deployment Readiness](../entitlement-readiness.html) with eight browser-only reviewer stages, each bound to a uniquely identified capability card and a **suggested** review role. Added cross-filter stage retention, a live accessible summary, reset, and explicit follow-up status/role in filtered JSON export. The original eight domains and the public evidence claim are unchanged; no new claims or images are necessary.

Allowed stages are **Not assessed**, **Evidence requested**, **Gap / entitlement decision needed**, and **Materials staged — independent review pending**. The last stage **does not mean accepted or verified**. No text input, browser storage, uploads, external network call or client data is involved. The controls reset on reload.

Every export continues to carry false native_DEV, Production, screenshot, licence and target-instance approval booleans; REQUIRED entitlement review; NOT RUN native test; and HOLD approval. The workflow is a review aid, not a contract or licence attestation.

## 3. Architectural best practices and testing

- **OOTB-first:** Use Subscription Management and contractual rights review, installed applications/scopes, platform ACLs and native non-production tests before designing custom replacement behaviour.
- **Source boundary:** Read restricted Delivery and Diagnostic source documentation and available connected As-Built/Architecture reference documents. Those sources identify scope and date-specific evidence, but do not establish a current target deployment or current purchased entitlements. Do not disclose restricted material publicly.
- **Security & accessibility:** Each visible review field is a labelled native `select`, supports keyboard access and mobile layouts, has a live summary, and runs entirely offline under the page's `connect-src 'none'` CSP. No free-text data to accidentally export.
- **Automated tests:** Extended `tests/test_entitlement_readiness.py` to assert eight labelled stages, conservative export flags and privacy. Extended `scripts/browser_entitlement_readiness.py` to exercise cross-filter retention, reviewer stages, exported values, reset and no external requests at 390, 768, 1024 and 1440px.
- **Verification:** Source update committed; final CI, browser tests and Pages should be checked against final branch commit before claiming a passed release. Public code tests do not establish native ServiceNow execution.
- **Licence dependencies:** None for static GitHub Pages. Native deployment requires contract-specific App Engine/custom-table and user rights; relevant ITSM, ITOM/Discovery, IntegrationHub/spoke, analytics, AI, ATF and third-party subscriptions and data rights must be checked individually.

**Outstanding:** Native DEV evidence, current target identity/role tests, customer entitlement agreement review, Production acceptance and individually approved sanitised images remain open.

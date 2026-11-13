# Entitlement & OOTB Decision Desk — SOURCE-ONLY Release

**Date:** 14 November 2026 (Australia/Sydney)  
**Public page:** [Operational Readiness — Entitlement Gate](../operational-readiness-runbook.html#entitlement-gate)  
**Evidence:** SOURCE-ONLY for public architecture descriptions; MOCK-ONLY for browser-local decisions and exports; historical DEV-REPORTED observations remain unrelated. **DEV-VERIFIED / PRODUCTION-VERIFIED:** no new claim. **Real screenshots:** zero approved, HOLD.

## 1. The client's pain & history

The controlled Diagnostic showcase completion runbook describes a G2 licensing blocker: 20 requirements need accountable, evidence-backed entitlement decisions before design approval. A status changed to "not required" without written basis does not resolve the blocker. At the same time, the Delivery Workbench source describes optional integrations and AI whose provider access and contractual rights have not been independently established. These unresolved dependencies could otherwise be mistaken for runnable features during a showcase.

The new page deliberately uses **10 generic capability categories**, **not** the 20 showcase requirement rows or a customer's actual licence inventory.

## 2. The ServiceNow solution implemented in the website

Added an accessible, responsive, offline Entitlement & OOTB Decision Desk to the existing Operational Readiness case study. Ten category cards cover scoped application/custom tables, ITSM, CMDB/CSDM, ITOM/Discovery, external integrations, reporting, asset management, customer/employee services, AI and document generation. Each card explains an OOTB-first path, an entitlement or deployment dependency to validate and an owner role.

Readers can filter all/unresolved/additional-product categories, select one of five explicitly **unverified** local decisions, add a strictly constrained anonymous evidence alias, reset the worksheet and export a JSON draft. Unresolved records remain visible and the export contains a complete ten-row snapshot. Missing/invalid aliases block export.

Every exported receipt is `HOLD`, `MOCK-ONLY` and `SOURCE-ONLY` in its respective fields, with `contract_verified`, `independent_approval`, `dev_verified`, `production_verified`, `installation_executed`, `licence_purchase_authorised` and `requirement_level_reconciliation_complete` hard-coded false. The widget has no network requests, client data, persistent browser storage, upload path or approved screenshot imagery.

## 3. Architectural best practices

- Prefer platform OOTB/standard workflow models before creating custom tables, collectors, additional integration layers or provider subscriptions. Record deviations, ongoing maintenance and the fallback route.
- Entitlement controls are **contract-specific**. ServiceNow [custom tables](https://www.servicenow.com/docs/r/platform-administration/table-administration-and-data-management/custom-tables.html) and [Integration Hub usage/subscriptions](https://www.servicenow.com/docs/r/integrate-applications/integration-hub/subscription-usage.html) documentation (updated 12 March 2026) establish the need to check actual custom-table and spoke rights. They do not prove any customer's ownership, product tier or usage allowance.
- Treat ITSM, ITOM Visibility/Discovery, Service Graph, HAM/SAM, HRSD/CSM, Performance Analytics, Now Assist, external providers and document-rendering services as **conditional** target-product checks, not universal purchases.
- Require the platform/licensing owner to reconcile **each** actual requirement to the signed subscription, instance plugin availability, technical design, usage model and independent approval. This educational website cannot clear that gate.
- Never confuse browser test success with native ServiceNow DEV/Production validation, customer sign-off or screenshot publication.

## 4. Reproducible verification

- `python -m unittest scripts.test_entitlement_decision_desk -v` enforces ten categories, accessible controls, no outbound transport, static aliases and non-promoted verification status.
- `python scripts/browser_entitlement_decision_desk.py` exercises the 390px, 768px, 1024px and 1440px layouts, filtering, validation, JSON export, reset and no network activity.
- GitHub Actions quality gate, responsive smoke test, publication audit and Pages deployment must be inspected against the **final commit**; a successful source commit alone is not deployed runtime proof.

## 5. Provenance and remaining HOLD items

Privately reviewed source basis: the connected Universal Delivery Workbench Solution As-Built (19 October 2026 source update), Diagnostic completion runbook (fictional showcase), Delivery and Diagnostic repository READMEs and the public Operational Readiness source. No private original, credential, source implementation or customer file was copied to the public site.

**Remaining:** 20 actual showcase requirements must be reconciled privately; no signed contract evidence, entitlement proof, independent G2 acceptance, native DEV replay, Production verification or authorised original screenshot is asserted. A public gallery of genuine Workbench captures remains blocked until image-specific rights, irreversible sanitisation and independent approval.

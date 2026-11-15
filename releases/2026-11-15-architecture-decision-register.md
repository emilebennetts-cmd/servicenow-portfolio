# Architecture decision review register — 15 November 2026

## 1. The client's pain & history

The public portfolio already covered individual source-only implementations and a conceptual architecture atlas. An engineering reviewer still had to infer the *decision record*: why the two Workbenches have different evidence authority, which shortcuts were rejected, and which native ServiceNow acceptance test would substantiate each choice. That can obscure ownership, technical debt and ITIL 4 governance boundaries. This is a generalised problem scenario, not a claim about a named customer.

## 2. The ServiceNow portfolio solution

Added [Architecture Decision Register](../architecture-decision-register.html), a mobile-friendly and print-friendly eight-record public case study. Each record explicitly identifies a source-derived design choice, rejected shortcut, risk controlled, necessary acceptance gate and a related **public** evidence page. The page includes accessible local search, four domain filters, count announcements, keyboard focus styling and a strict no-network content-security policy. All eight records are readable without JavaScript.

The register covers: single authority for findings, consent-based zero-footprint diagnostics, OOTB-first delivery, package/scope integrity, approved external writes, draft-not-approved document generation, human AI review and evidence-state segregation. These are *source-derived engineering rationales*, not signed ADRs or independently tested native implementations.

The new page is linked from the portfolio home and the architecture atlas and added to the sitemap. No customer names, instance URL, secrets, private repository links, source code or screenshot pixels were copied into the public document.

## 3. Architectural best practices, evidence and validation

- **Reviewed sources:** Restricted Delivery Workbench and Diagnostic Workbench 2 READMEs; controlled Delivery Workbench Architecture and Solution As-Built from connected Drive; public architecture and evidence pages. Private provenance is logged separately in portfolio-control.
- **Evidence:** SOURCE-ONLY for reviewed source rationale; MOCK-ONLY for browser filtering; previously documented DEV-REPORTED statements remain historical. No new DEV-VERIFIED or PRODUCTION-VERIFIED claims. Genuine screenshots remain **0 approved — HOLD**.
- **Security:** no external scripts, runtime network requests, browser storage, sensitive assets or private GitHub links; strict CSP with only local inline script/style; public links only.
- **Testing:** `scripts/test_architecture_decision_register.py` checks distinct ADR identities, source-only labels, no embedded visual media, no private links, accessible structure, interactive filter hooks, mobile/print support and home/atlas/sitemap discovery. Existing source, publication and local-link tests must also pass in CI.
- **Native acceptance required:** authorised DEV package read-back, correct technical scope, role/ACL and row security tests, approved integration consent, document sign-off, acceptable product entitlements, witnessed tests and current versioned evidence. No claim that a static page proves these controls.

**Licensing:** The public page is static and requires no ServiceNow subscription. Native apps may require rights for custom scoped apps/App Engine, relevant ITSM, ITOM and CMDB capabilities, and separately validated IntegrationHub spokes, AI/Now Assist, ATF, analytics or third-party provider subscriptions. Roles, ACLs and cross-scope privileges must be verified in the target environment; entitlement cannot be determined from repository presence.

**Publication gate:** This release does not authorise any original ServiceNow screenshot or confidential document for the public website. Source-to-DEV identity conflicts and independent Production assurance remain unresolved until witnessed and approved.

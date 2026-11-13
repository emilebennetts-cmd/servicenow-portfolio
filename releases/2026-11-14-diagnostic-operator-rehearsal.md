# Diagnostic Workbench — source-backed operator rehearsal

**Release date:** 14 November 2026 (Australia/Sydney)  
**Public implementation:** [Diagnostic technical case study](../diagnostic-workbench-case-study.html#diagnostic-operator)  
**Classification:** SOURCE-ONLY; historical DEV-REPORTED; no newly independent DEV-VERIFIED or PRODUCTION-VERIFIED result. All original screenshot publication remains HOLD.

## 1. The client's pain and history

Assessments can fail audit because runbooks, collectors, findings and remediation proposals are presented without a documented control path or independent judgement. The source-defined core Workbench and KI companion are different runtimes. Exporting a portfolio rehearsal is not proving either installation.

## 2. The ServiceNow solution delivered this release

- Implemented **10 accessible source-backed procedure cards**, eight for the core local-first Workbench and two for the separately deployed Knowledge Intelligence 0.1.0 companion. Both lanes can be filtered by six roles: lead, analyst, operator, reviewer, approver and architect.
- Each card explains the source-described action, the required artefact and the stop/go control. The flow moves from scope and guided runbooks to authorised read-only collection, DIAG evidence validation, draft rule/correlation findings, Not-assessed coverage, independent review and governed report/handover. KI cards cover licensing/ACL/update-set boundaries and evidence-to-finding lineage.
- Added a browser-only read checklist with reset and plain-text local export. Export is **NOT RUN | HOLD**, declares independent_dev_verified=false, runtime_verified=false, production_verified=false and screenshot_approved=false. Reading cards does not record native execution, customer approval or entitlement.
- Added offline Python structural/safety tests and four-width Chromium testing in the existing responsive smoke workflow (390, 768, 1024, 1440px).
- Updated the **existing** Diagnostic page-specific SOURCE-ONLY evidence claim rather than generating a redundant new claim; preserved deterministic Explorer coverage.

## 3. Source, architecture and verification

- Reviewed access-restricted `Diagnostic-Workbench2/README_BUILD.md` and `knowledge-intelligence/README.md`, plus its portfolio-safe diagnostic source dossier. Core readme documents a local-first 18-stage/six-phase assessment, 67 guided runbooks, 20 pack collectors, bounded DIAG-envelope intake, draft findings and pack health. The separate KI source documents 16 packs, 45 read-only collectors and a governed review chain. These are **source declarations**, not current customer runtime observations.
- Core v0.0.1 README_BUILD describes 1 September 2026 testing and historical DEV reports; KI 0.1.0 README describes a 30 September 2026 installation and lint. This implementation did not independently access or retest those environments.
- Connected Google Drive `DemoClient23_Diagnostic_Workbench_Completion_Runbook.docx` was reviewed: it explicitly labels its client/test data fictional and prohibits closing unproven approval gates. The controlled Delivery Workbench User Guides and Training was reviewed for the corresponding separate delivery governance boundary. No controlled document links or excerpts were published.
- The workbench **does not execute** collectors itself; an authorised operator executes separately in an approved non-production environment. KI Classic modules are not integrated into the local-first UI. No automatic source-to-delivery transaction was claimed.
- The website uses semantic labels, responsive card layout, no external assets or network I/O and can display all procedures with JavaScript disabled.

## 4. Entitlements, security and remaining gaps

Static portfolio website: **no ServiceNow licence**. An actual installation needs authorised non-production access, application/custom-table / App Engine rights as contracted, scope-specific KI roles and ACLs, update-set preview and change governance, and approved least-privilege collector execution. Optional ITSM, ITOM/Discovery, IntegrationHub, AI, Performance Analytics and third-party knowledge article/API rights require feature-specific approval.

No private repository visibility or production data was changed. No screenshot, password, instance endpoint, private source, Drive identifier or customer data was published. All screenshot candidates remain HOLD until individually reviewed and irreversibly sanitised. Fresh source-pinned native DEV acceptance, negative ACL checks and human-authorised image publication remain outstanding.

## Release files

- `diagnostic-workbench-case-study.html` — 10-card interactive guide
- `scripts/test_diagnostic_operator_guide.py` — offline publication/regression assertions
- `scripts/browser_navigation_smoke.py` — four-viewport functional test
- `evidence/public-verification-register.json` — existing claim updated
- `RELEASE_LOG.md` — dated audit entry
- Restricted provenance receipt maintained in the private control repository.

**CI status:** inspect final-commit workflow results; source-only website functionality is not native instance verification.

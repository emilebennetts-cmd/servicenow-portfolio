# Diagnostic Gate Closure Lab — source-controlled release (13 November 2026)

## 01 / The client's pain & history

A representative ServiceNow delivery programme can have diagnostics findings, an incomplete licence decision, open red RAID risks, missing peer review, incomplete SIT/ATF/PVT/UAT coverage and release records that do not align with the Delivery Workbench's engagement spine. A dashboard percentage cannot replace a version-pinned acceptance decision. This is a fictionalised business problem, not a current customer finding.

## 02 / The ServiceNow solution

Implemented [Diagnostic Gate Closure Lab](../diagnostic-gate-closure-lab.html), a responsive, local-only educational case study:

- Seven selectable G0–G6 stage cards and eleven D1–D11 evidence preparation work units, derived conceptually from the controlled fictional 30 September 2026 Diagnostic Workbench completion runbook.
- A comparison of the Diagnostic findings/assurance lens with the Delivery requirements, component, test, risk and release spine. Original historic identifiers, customer/demonstration names and private file content are absent.
- Four synthetic starting scenarios, independent toggling of evidence preparation, an outstanding-work queue and permanent `HOLD` release status.
- Downloadable JSON review ticket that always records `native_status=NOT RUN`, `approval=false`, `release=HOLD`, `dev_verified=false`, `production_verified=false` and `publication_approved=false` regardless of the selected scenario or self-reported preparation.
- No network calls, server storage, remote imagery, ServiceNow credentials or write operations.
- Homepage/mobile navigation, review guide, searchable Explorer, canonical sitemap, public evidence register and both restricted source-repository provenance records linked or updated.
- Static publication contract and Playwright behavioural coverage for 390/768/1024/1440px enforced by GitHub Actions workflow.

The diagram is an authored schematic, not an original ServiceNow screen or an installed integration. Self-marked preparation does not imply an independent test, an approved design, an actual CAB outcome or a Production release.

## 03 / Architectural best practices

Sources reviewed: the 30 September 2026 controlled Universal Delivery Workbench Solution As-Built, Architecture, User Guides/Training, and fictional Diagnostic completion runbook from connected Drive; Delivery and Diagnostic source repositories were reconciled. The historical Delivery 4.6.1 source / 4.5.1 DEV boundary is not interchangeable with the later separately maintained Delivery source generation (source 4.22.2) or demo7 environment. The current native 29-case acceptance matrix remains NOT RUN.

- **SOURCE-ONLY:** separately authored public HTML, governance model, scripts and source/Drive documentation.
- **MOCK-ONLY:** all four scenarios, preparatory checkmarks, gate summaries and exported ticket.
- **DEV-REPORTED:** historical non-production runbook observations only, dated and not independently repeated.
- **DEV-VERIFIED:** nothing newly established.
- **PRODUCTION-VERIFIED:** none.
- **Screenshots:** zero original Workbench images newly approved or published; HOLD still applies.

Critical native controls still pending: target release identity, signed entitlement/authority, non-admin persona ACLs and cross-engagement isolation, traceable finding-to-delivery links, actual tests, negative integration tests, true change/release approvals, safe rehearsal/rollback/PVT, recovery, independent UAT and operational acceptance. A safe DEMO PROD-SIM path is always explicitly NOT PRODUCTION.

Licensing: the public website needs no ServiceNow licence. Actual deployment requires authorised App Engine/custom-app/table rights, target roles/ACLs and applicable ITSM Change/ATF, ITOM/CMDB/Discovery, IntegrationHub/spoke/provider and optional AI/analytics entitlements. Verify each in the relevant instance.

No private repository source, original screenshots, client-identifying records, live instance addresses, keys or credential aliases were copied into the public site. Repository visibility and Drive sharing were unchanged. CI and Pages status must be read against their specific commit and must not be substituted for ServiceNow native acceptance.

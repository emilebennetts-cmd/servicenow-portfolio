# Source-backed persona review gallery — 14 November 2026

**Public page:** [Workbench Architecture Gallery](../workbench-architecture-gallery.html#persona-tour)
**Change classification:** SOURCE-ONLY historical design/training evidence, MOCK-ONLY browser walkthrough; NOT VERIFIED / HOLD.
**Scope of work:** public website only. No native ServiceNow application changes, production deployment, client data, screenshots, private source, secrets or approvals.

## 1. The client's pain & history

The architecture gallery correctly separated historical Delivery DEV 4.5.1, source 4.6.1 and later 4.22.x, but reviewers could not inspect how persona-specific procedures connect to delivery controls and evidence requirements. The 30 September 2026 controlled-draft User Guides and Training identifies role-based starts and a governed lifecycle, yet warns that source 4.6.1 was **not** installed/read back on the dated 4.5.1 DEV baseline.

The prior gallery had only static flow illustrations. Displaying restricted captures would breach the separate image-by-image approval gate; inventing screen pixels would blur MOCK-ONLY and native proof.

## 2. The ServiceNow solution — implemented on the public website

Added six accessible review journeys directly inside the existing architecture case study: presales, architect, delivery lead, developer/tester, deployer and platform support. Each changes an OOTB-aligned procedure, evidence requirement and explicit release blocker. Tabs support mouse, touch, Left/Right, Home/End keyboard navigation, roving tab focus and ARIA-labelled panel updates.

Added downloadable, local-only JSON preparation checklists. Every export is fixed to:
- architecture_classification: SOURCE-ONLY
- interaction_classification: MOCK-ONLY
- review_state: UNREVIEWED
- verification_state: NOT VERIFIED
- release_state: HOLD
- native_dev_verified: false
- production_verified: false
- screenshot_publication_approved: false

No external services, credentials, screenshot pixels, local storage or customer details are processed. The page's three version-specific baseline cards remain unchanged.

## 3. Architectural best practices, sources and assurance

- **Primary restricted reference:** connected Google Drive *03 — Universal Delivery Workbench — User Guides and Training*, controlled draft, evidence cutoff 30 September 2026, source 4.6.1. This private document is **not linked or republished**.
- **Corroborating restricted reference:** connected Google Drive *01 — Universal Delivery Workbench — Solution As-Built*, controlled draft 30 September 2026, 4.6.1 source and separate 4.5.1 DEV read-back. The draft remains unapproved.
- **Source repositories reviewed:** private `solution-lifecycle-studio` and `Diagnostic-Workbench2`, with `servicenow-portfolio-control` retaining restricted provenance. No private repository visibility or product source changed.
- **Public implementation:** `workbench-architecture-gallery.html`.
- **Regression test:** `scripts/test_architecture_gallery_claim_boundaries.py` now limits the original version-card assertions to the original baseline section.
- **Browser test:** `scripts/browser_persona_architecture_gallery.py` validates six roles, accessible selection, responsive layouts at 390/768/1024/1440px, conservative JSON export and image/network restrictions.
- **GitHub Actions:** `.github/workflows/portfolio-responsive-smoke.yml` runs the new browser test alongside existing gallery and site checks. Final run conclusions are separately checked after commit.

**No new DEV-VERIFIED or PRODUCTION-VERIFIED claim.** Historical DEV-REPORTED evidence does not transfer to later source or distinct application scopes. Genuine screenshots remain **0 approved / HOLD**. Automated browser/CI results verify only the public website.

**Licensing and entitlements:** No ServiceNow licence needed for this public HTML/JavaScript. Native scoped-app operation requires confirmation of App Engine/custom-table entitlements, roles, membership and ACLs. ITSM, ITOM/Discovery, IntegrationHub/spokes, ATF, Performance Analytics, AI and third-party rights depend on the approved target design; no entitlement is inferred from the reference documentation.

**Next evidence gates:** independently witnessed native DEV test with source SHA, installed version and app scope; recorded execution and reviewer; separate production change authorisation; individual screenshot ownership, irreversible sanitisation and publication approval.

## Verified CI receipts (14 November 2026)

- [Full responsive browser smoke](https://github.com/emilebennetts-cmd/servicenow-portfolio/actions/runs/43566131706) — **SUCCESS**, including new six-persona Playwright assertions at 390, 768, 1024 and 1440 px. Verified at source commit `de1a48679fb66c6bf40bbdf360ab654790e87bb3`.
- [Public source quality gate](https://github.com/emilebennetts-cmd/servicenow-portfolio/actions/runs/43566169260) — **SUCCESS** for release-documentation commit `6ea7d46553263c63f198125c7b34e0a3e3a54c03`.
- [Publication and evidence quality audit](https://github.com/emilebennetts-cmd/servicenow-portfolio/actions/runs/43566169287) — **SUCCESS** for the same source head.
- [GitHub Pages deployment](https://github.com/emilebennetts-cmd/servicenow-portfolio/actions/runs/43566169335) — **SUCCESS** for the same source head.

GitHub Actions completed successfully, but independent third-party HTTP retrieval of the public URL could not be established. These CI receipts apply to the public website only, **not** native ServiceNow DEV/PROD functionality or screenshot approval.

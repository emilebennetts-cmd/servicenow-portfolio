## 2026-11-11 — Visually inspected intake and binary metadata safety

- Corrected JPEG EXIF and GIF comment checks to match real binary bytes, not literal backslash escape characters. Added CI-discovered metadata regression tests and verified the publication gate still requires approved image bytes.
- Published a public-safe, responsive status panel at `visual-evidence.html` based on a **separate four-file private intake sample**: 2 UI captures without independently established runtime verification, 1 explicit synthetic example (MOCK-ONLY), 1 overview document page. All 4 remain HOLD; 0 approved images; they are **not** conflated with the existing ten placeholder IDs.
- Added a CI-discovered visual-intake safety contract; its candidate-ID regular expression was corrected after a failed initial quality-gate run.
- Maintained SHA-256 receipts and original source pointers privately. No image, private source or customer information was published.
- **Evidence tier:** SOURCE-ONLY implementation, mock-only demonstration, no new DEV-VERIFIED or PRODUCTION-VERIFIED claims.
- **Release details:** [Visual intake and metadata regression](releases/2026-11-11-visual-intake-metadata-regression.md). Verify final commit quality-gate and Pages results separately.
- **Licensing:** Static site and standard-library CI controls none; ServiceNow runtime App Engine/custom app, ITSM/ITOM, IntegrationHub, analytics, AI and provider entitlements conditional on scope.

## 2026-11-09 — Gallery DOM and navigation regression coverage

- Commit `36b252cb6442bf193f645d85401ee0e0f3108750` extends `tests/test_visual_evidence_contract.py` with duplicate DOM ID detection and local fragment-link integrity checks.
- These tests protect accessible label/target relationships and in-page navigation as the visual gallery evolves. No dependencies or confidential assets were introduced.
- **Verification:** SOURCE-ONLY; test execution and browser deployment have not been independently observed. Ten screenshot candidates remain HOLD; no new DEV-VERIFIED or PRODUCTION-VERIFIED claims.
- **Sources consulted:** Delivery and Diagnostic repository READMEs, existing gallery and tests, and Google Drive Diagnostic Workbench discovery. Drive image contents were not opened or published.
- **Next:** Run offline tests in CI, verify published mobile experience, and privately inspect/redact images before requesting explicit release clearance.
- **Entitlements:** Static checks require none. ServiceNow runtime requires authorised instance/custom app access; optional ITSM/ITOM, IntegrationHub, Performance Analytics and AI entitlements are feature-dependent.

## 2026-11-09 — Print review state and empty-result safeguards

- Implemented commit `447eaccc1cdee3c7a3035587a514ba0446f0bd81` in `visual-evidence.html`.
- Printing matching evidence records now expands details temporarily and restores each record's original disclosure state after the browser's `afterprint` event. Native Ctrl/Cmd+P also expands matching records using `beforeprint`.
- Print is disabled when filters return zero candidates, consistent with CSV export. A DOM observer tracks the existing result-count updates without changing filter behaviour.
- **Evidence classification:** SOURCE-ONLY; no browser execution, GitHub Pages propagation, DEV acceptance or production validation is claimed. Existing illustrative screens remain MOCK-ONLY; ten image candidates remain HOLD and CANDIDATE-ONLY.
- **Source review:** Public Delivery and Diagnostic READMEs, private portfolio-control README, existing gallery source, and Google Drive document discovery. Original image pixels were not inspected, sanitised or approved; no private Drive links or customer data were published.
- **Follow-up:** Browser-test print/cancel, empty-result filtering, and mobile layout; inspect original image assets privately and obtain explicit publication clearance before adding derivatives.
- **Entitlements:** Static website requires none; ServiceNow scoped app runtime and optional ITSM/ITOM, IntegrationHub, Performance Analytics and AI capabilities require relevant instance and product entitlements.

## 2026-11-09 — Filtered printable evidence review sheets

- Commit `f0e551c1cff8280fb6fdbc41b806faa509ea2313`: added a print action to the existing visual evidence gallery. The action expands the visible candidates' evidence records and prints a clean, paper-friendly reviewer sheet with the active search/product filters applied.
- Print CSS removes navigation, placeholder graphics and controls; excludes hidden cards; and keeps each evidence record together where supported by the browser.
- Verification: SOURCE-ONLY committed; print preview and live GitHub Pages deployment not independently tested. All ten candidate images remain HOLD; no DEV-VERIFIED or PRODUCTION-VERIFIED claims.
- Security: no original screenshots, private documents or customer data added. Licensing: static printing requires none; ServiceNow runtime verification and optional ITSM/ITOM, IntegrationHub, Performance Analytics and AI features depend on instance entitlements.

## 2026-11-09 — Gallery filter recovery and safe empty-state export

- Commit `e8e257725bff963de8f95f485753f389fda89cb5`: added an accessible Clear filters action that restores the full ten-candidate inventory, removes search and product query parameters and returns keyboard focus to search.
- Disabled CSV export when zero records match, avoiding misleading empty review registers; added disabled-state styling and accessible state.
- Verification: SOURCE-ONLY change committed; browser and live deployment not independently verified. Ten candidates remain HOLD; no new DEV-VERIFIED or PRODUCTION-VERIFIED evidence and no images published.
- Licensing: static website and CSV controls require no ServiceNow licence; scoped Workbench runtime and optional ITSM/ITOM, IntegrationHub, Performance Analytics and AI capabilities require applicable entitlements.

## 2026-11-09 — Downloadable screenshot review register

- Added a client-side CSV export to the existing visual evidence gallery. It exports only the currently filtered candidate records: evidence ID, product, screen, HOLD publication decision, CANDIDATE-ONLY verification status and reviewer guidance.
- Export is generated locally without external services or access to original Drive assets. UTF-8 BOM supports spreadsheet readers; CSV fields are quoted and formula-like prefixes escaped.
- Commit: 944aa1cb15e55bbf45d31986ccda9da72d3db032.
- Verification: SOURCE-ONLY; browser interaction and live Pages deployment not independently confirmed. Ten screenshot candidates remain HOLD, no DEV-VERIFIED or PRODUCTION-VERIFIED claims and no sensitive images published.
- Licensing: static CSV export needs no ServiceNow entitlement. Scoped application execution and optional ITSM/ITOM, IntegrationHub, Performance Analytics and AI features require instance-specific licence verification.

## 2026-11-09 — Screenshot publication gate security hardening

- Hardened `scripts/check_publication.py` to reject absolute, traversal and non-canonical approval paths; approvals are restricted to `assets/screenshots/`.
- Reject escaping symlinks before reading or hashing public assets, and verify resolved approval targets stay inside the repository.
- Added `tests/test_screenshot_gate_security.py` covering valid approved bytes, path traversal, absolute paths, external symlinks and post-approval image mutation.
- Evidence classification: **SOURCE-ONLY** for this gate implementation; tests committed but no new CI run independently verified in this release. No DEV-VERIFIED or PRODUCTION-VERIFIED ServiceNow claims.
- All ten screenshot candidates remain **HOLD** pending authorised human privacy review and publication approval. No new images published.
- Licensing: static publication gate requires no ServiceNow licence; runtime Workbench verification depends on authorised instance access, custom application entitlements and feature-specific ITSM/ITOM, IntegrationHub, Performance Analytics or AI subscriptions.


## 2026-11-09 — Screenshot review workspace
- Commit: aebe02c0e361fab700407abdb66bd659d9e993be
- Added a practical, accessible review checklist directly to the existing ten-candidate visual evidence register, with source links, digest requirements, confidentiality review and explicit HOLD status.
- Verification: SOURCE-ONLY website change; candidate screenshots remain unpublished. No new DEV-VERIFIED or PRODUCTION-VERIFIED claims. Browser deployment and CI outcome not independently verified for this commit.
- Security: no original screenshots, customer data or private control-repository content published. Licensing: static page none; runtime platform/custom-app and optional ITSM/ITOM, IntegrationHub, PA and AI entitlements depend on installed capabilities.

## 2026-11-08 — Capability traceability and verification boundaries

- Published `capability-traceability.html`: mobile-friendly, source-linked capability matrix for Diagnostic Workbench 2 and Universal Delivery Workbench, including Knowledge Intelligence's separately deployed companion status, delivery version drift, and mock-only provider integration boundaries.
- Linked the matrix from `visual-evidence-intake.html`.
- Evidence: public README and build documentation in `emilebennetts-cmd/Diagnostic-Workbench2` and `emilebennetts-cmd/solution-lifecycle-studio`; architecture boundaries in this site. No private control material or screenshots were published.
- Classification: **SOURCE-ONLY** for the new page and current application implementation claims; **MOCK-ONLY** for simulated external integrations; historical DEV installation statements remain repository-reported, not independently DEV-VERIFIED. No production verification claimed.
- Acceptance pending: CI and live deployment check, independent DEV execution, screenshot review and approval.
- Entitlements: static page none; runtime custom app, ITSM/ITOM, IntegrationHub, Performance Analytics, AI and provider entitlements subject to instance-specific review.

## 2026-11-08 — Job-level CI publication evidence

- Added `ci-job-evidence.html` with the independently retrieved GitHub Actions job ID 128637024742 for run 42450018822, including five named quality-gate steps each reporting success.
- Linked the job evidence from `publication-quality.html` for direct reviewer navigation.
- **Provenance:** GitHub Actions REST job collection for the named run, inspected 8 November 2026; job conclusion and step conclusions were observed, not independently re-executed.
- **Classification:** Website CI execution OBSERVED SUCCESS; application source remains SOURCE-ONLY or historically DEV-reported where applicable; interactive simulations MOCK-ONLY; no new DEV-VERIFIED or PRODUCTION-VERIFIED evidence.
- **Security:** No private repository material, customer information, credentials or unapproved screenshots included.
- **Outstanding:** Independent published-site/mobile-browser verification and approved original Workbench screenshots.
- **Entitlements:** No ServiceNow licence for static site CI; runtime scoped applications and optional ITOM/IntegrationHub/PA/AI may require entitlements.

## 2026-11-08 — Engineering evidence register and case-study navigation

- Published `engineering-evidence.html` with source-to-claim traceability, DEV/production verification boundaries, screenshot approval steps and licensing caveats.
- Linked the register from `engineering-case-studies.html`.
- Sources reviewed: public `solution-lifecycle-studio/README.md`, `Diagnostic-Workbench2/README.md`, and existing portfolio case-study content.
- **Evidence:** SOURCE-ONLY for documented capabilities; external sync and public walkthroughs MOCK-ONLY where indicated; historical DEV reports are not independently reproduced; no production verification claimed.
- **Security:** No screenshots, private source, credentials or client records published. Screenshot release still requires approved sanitised captures and digest verification.
- **Validation pending:** live Pages deployment, mobile browser/a11y testing and authorised DEV runtime checks.
- Commits: `abbd2c5` (new page), `aa98ee6` (navigation).

## 2026-11-07 — Source-traced proof paths (commit fc392b2)

- Added three responsive, keyboard-accessible engineering proof-path cards to the homepage, immediately before the 90-second review: diagnostic envelope intake and rules, governed implementation presets, and diagnostic-to-delivery evidence ownership.
- Each card explains the operational pain, repository-documented mechanism, evidence boundary and specific synthetic DEV acceptance test. Native `details/summary` provides progressive disclosure without a framework.
- Visual treatment: high-contrast light panel, single-column layout under 900px, visible focus indicators. This is an implementation, not an original ServiceNow screenshot gallery.
- Provenance: `Diagnostic-Workbench2/README_BUILD.md` and `solution-lifecycle-studio/README.md` (including implementation-preset release reference). Counts and capabilities remain **SOURCE-ONLY / historical DEV-reported**, not independently DEV-verified. Cross-workbench handoff remains **MOCK-ONLY**. No production verification claimed.
- Privacy: no client names, instance URLs, scope IDs, sys_ids, ticket identifiers, private code or unreviewed screenshots added in this change.
- Verification: checked successful GitHub contents update and expected three card insertions; no live-browser accessibility audit or GitHub Pages deployment confirmation in this run.
- Outstanding: approved sanitised real screenshot gallery; independent DEV read-back; site-wide privacy/accessibility/performance audit. Static website has no ServiceNow licensing requirement; scoped apps and optional ITOM/IntegrationHub/AI functions depend on appropriate roles and entitlements.


## 2026-11-07 — Inline diagnostic technical proof

- Added homepage section `#technical-proof`: evidence processing pipeline, 20 collector packs, 67 runbooks, 42 rules + 4 correlations, and five expandable implementation notes. All counts are repository-sourced catalogue counts, not new runtime observations.
- Source: `emilebennetts-cmd/Diagnostic-Workbench2/README_BUILD.md`, including historical 1 September 2026 local and DEV test claims.
- Verification: source-backed architecture and historical DEV-reported test results only. No current instance access, independent DEV read-back or production verification performed in this increment.
- Publication: no screenshots, instance URLs, client names, credentials, sys_ids or private repository contents added to the public page.
- Licensing: static site needs no ServiceNow entitlement; actual scoped application deployment and optional integrations require platform permissions and product entitlement assessment.
- Outstanding: sanitised original screenshot review and embedded image gallery; public deployment/browser checks.

## 2026-11-07 — Embedded Diagnostic operator walkthrough

- Commit `22862b059fa06a363a379c94edd80a80575b06bb`: replaced the homepage's external Google Drive screenshot call-to-action section with a self-contained, responsive five-stage Diagnostic Workbench operator walkthrough.
- Implemented five selectable stages, previous/next navigation, stage-specific expected outputs, keyboard-operable buttons, mobile horizontal stage selector, and expandable evidence/licensing disclosures.
- **Source:** visually inspected original client-neutral Diagnostic Command Centre capture from connected Drive; the five-step operator sequence and UI terminology are based on that capture. This implementation is a **source-informed reconstruction**, not a published original screenshot, live runtime or independently verified deployment.
- **Security:** no customer screenshot, private source, Google sharing link or unreviewed binary asset was embedded. The source capture stays private pending sanitisation and approval.
- **Verification:** GitHub contents update succeeded; automated browser rendering and latest GitHub Pages deployment were not independently confirmed in this change.
- **Licensing:** static in-page demo needs no ServiceNow licence; real instance execution requires applicable roles, instance permissions and relevant product entitlements.

## 2026-11-07 — Integrated interactive application explorer

- Commit `14b937425e0dc795c2ce7259b655028d765e51c2`: added a responsive, accessible, in-page application explorer to `index.html`, including Diagnostic Command Centre interface reconstruction, Delivery Workbench lifecycle board and functional five-stage governed-handoff walkthrough.
- Original Diagnostic Command Centre capture in connected Google Drive was visually inspected. The interface reconstruction uses its client-neutral navigation and historical metrics, clearly marked illustrative, not live telemetry or original screenshot.
- **Evidence status:** Diagnostic and Delivery application features are source-backed; historical DEV results are repository-reported; cross-workbench handoff is proposed/mock-only. No independently DEV-verified or production-verified claims added.
- **Publication boundary:** No original screenshot, confidential client material or private application source was copied to the public repository. Genuine embedded screenshot gallery remains pending image-by-image sanitisation and release review.
- **Licensing:** Public static explorer requires no ServiceNow entitlement. Underlying scoped apps, IntegrationHub and licensed workflow capabilities require instance access and applicable subscription entitlements.
- **Verification:** GitHub contents API accepted the homepage commit. Public GitHub Pages build and browser rendering remain to be independently confirmed.

## 2026-11-07 — Verification attestation hardening

- Commit `1e0f504`: tightened the public verification register validator: canonical in-repository HTML paths, ISO verification dates, future-date rejection, HTTPS evidence references and explicit production authorisation.
- Commit `02a2e92`: added four regression tests covering future dates, insecure evidence references, missing production authorisation and non-HTML page references.
- The quality workflow already executes this validator and discovers its regression tests; new workflow run result has not yet been independently checked.
- Drive metadata searched for Workbench assets. No original screenshots reviewed, redacted or approved; none published.
- Evidence classifications unchanged: source-only and DEV-reported are not independent runtime verification; mock-only and proposed are not deployed.
- No ServiceNow entitlement required for static validation; scoped apps, IntegrationHub, AI, analytics and product modules may require licensed entitlements.

## 2026-11-07 — Evidence register enforced in CI

- Commit `d43055b`: wired `scripts/check_verification_register.py` into the push/PR quality workflow, preventing unchecked evidence classifications from being merged without a failing check.
- Commit `70919e3`: added six unit tests covering valid register, duplicate claims, unsupported classification, unsupported production promotion, path traversal and missing case-study references.
- Previous revision `e074fb3` had successful quality and Pages workflow runs (42328400368 and 42328400318); the new revision's workflow outcome must be checked separately.
- No screenshot assets, customer data, private repository contents or secrets published. Static checks need no ServiceNow entitlements; underlying scoped apps and optional integrations still require target-instance licensing assessment.

## 2026-11-07 — Governed diagnostic-to-delivery handoff contract

- Commit `beba342`: added `governed-handoff-contract.html`, a mobile-friendly proposed versioned integration envelope with synthetic sample payload, five bounded workflow stages, replay/idempotency, conflict, authorisation and failure test criteria.
- Commit `42c9db2`: added homepage route from cross-workbench architecture to the contract.
- Sources reviewed: public `solution-lifecycle-studio/README.md` and `Diagnostic-Workbench2/README.md`. Google Drive search performed; no original screenshot pixels reviewed or approved.
- Classification: contract is **proposed/reference only**, source capabilities are **source-only**, historical DEV reports remain **repository-reported**, external connectors **mock-only**; no independent current DEV or production verification claimed.
- No private source, customer records, credentials or unreviewed screenshots published. GitHub commit acceptance confirmed; CI and browser deployment validation pending.
- Entitlements: static page none; scoped applications, IntegrationHub/spokes and underlying licensed modules subject to assessment.

## 2026-11-07 — Deployment assurance engineering case study

- Commit `ee3fb334`: added `deployment-assurance.html`, a responsive source-traced case study with five proposed release gates, verification matrix, architectural controls, licensing and primary public-source links.
- Compared the public Delivery and Diagnostic README files; distinguished Delivery 4.22.2 source declaration, historical 4.20.0 DEV report, mock-only external connectors, separately deployed Knowledge Intelligence companion and unverified production status.
- Google Drive As-Built candidate located; no Drive screenshot was inspected or published. No private source, customer data or credentials included.
- GitHub commit accepted; independent CI and public HTTP verification pending.

## 2026-11-07 — Knowledge Intelligence companion architecture case study

- Published `knowledge-intelligence.html` using the public `Diagnostic-Workbench2/knowledge-intelligence/README.md` as primary evidence; added a contextual route from `diagnostic-evidence-lifecycle.html`.
- Documented the separately deployed 0.1.0 companion, seed inventory, read-only collector controls, human review, installation boundaries and content-licensing obligations.
- The 30 September DEV acceptance (347 inserts, 45 collector lint checks) is **repository-reported**, not independently reproduced. No current DEV, production or cross-navigation integration is asserted.
- No screenshots, customer information, secrets or private repository material were published. Source commits confirmed; CI and public browser rendering await independent verification.
- Static website requires no ServiceNow licence; scoped-app deployment, underlying product modules and external content rights require entitlement review.

## 2026-11-07 — Evidence-first diagnostic lifecycle deep dive

- Commit `c721f9e`: published `diagnostic-evidence-lifecycle.html`, a responsive source-traced case study covering collector isolation, DIAG envelope intake, 42 rules / four correlations, 67 guided runbooks, pack-health controls and draft remediation.
- Commit `eee830f`: added mobile navigation entry from the homepage.
- Source: `Diagnostic-Workbench2/README_BUILD.md` and `README.md`. The 1 September 2026 local Playwright and DEV acceptance statements are **repository-reported historical results**, not independently reproduced tests.
- Knowledge Intelligence remains a separately deployed companion; no claim of connected navigation, production acceptance, or approved screenshot evidence.
- No customer data, private repository content, credentials or unreviewed imagery introduced.
- Verification: commits accepted by GitHub; CI and public browser rendering of this revision remain to be checked. Licensing depends on instance scoped-app entitlements and any licensed modules used by collectors.

## 2026-11-07 — Reusable pattern lifecycle engineering case study

- Commit `b5e6e03`: added responsive `pattern-lifecycle.html` with a six-stage candidate-pattern lifecycle, explicit review gates, evidence ledger, primary source links and licensing caveats.
- Commit `0f1c41b`: added a homepage route to the new case study.
- Source basis: public `solution-lifecycle-studio` README and linked implementation-presets/catalogue release analyses. Catalogue counts (11,000 issues, 2,234 candidate patterns), 4.22.2 version and historical DEV baseline are **repository assertions**, not independently audited runtime results.
- No customer-specific scenario presented as fact; no unreviewed screenshots, private repository content, secrets or production claims published.
- Verification: source commits accepted. CI, live public HTTP rendering and current DEV/production functionality **not independently verified in this increment**.
- Entitlements: static case study requires none; scoped-app deployment, licensed product modules and live integrations require instance-specific entitlement and API review.

## 2026-11-07 — Source-traced dual-workbench architecture case study

- Commit `0ebfc92`: published `workbench-architecture.html`, a responsive, accessible case study contrasting Diagnostic Workbench 2 (`x_1577958_dw2`) and Universal Delivery Workbench (`x_1577958_vdf`) using their public source README files.
- Commit `0ee34c2`: added a prominent homepage route to the new case study.
- Preserved distinctions: Delivery 4.22.2 is source-declared; DEV 4.20.0 baseline is repository-reported; external connectors and MIM demonstrations are mock-only; live cross-workbench integration, current DEV and production verification remain unconfirmed.
- No screenshot, private control material, customer data or credential published. Google Drive As-Built candidate located but not treated as public clearance.
- Licensing: static site needs no ServiceNow entitlement; scoped-app deployment and optional product modules, IntegrationHub/spokes, AI and analytics require target-instance review.
- Validation: commits accepted; independent CI result and public browser propagation for this revision not yet confirmed.

## 2026-11-07 — Independent GitHub Actions outcome reconciliation

- Queried the repository's GitHub Actions workflow-run API and confirmed **Portfolio quality gate** run [42260316927](https://github.com/emilebennetts-cmd/servicenow-portfolio/actions/runs/42260316927) completed **successfully** for commit `666cbd27dbbc7f3bb9183ea78529e90a69413a52`.
- Confirmed **pages build and deployment** run [42260315868](https://github.com/emilebennetts-cmd/servicenow-portfolio/actions/runs/42260315868) completed **successfully** for the same commit. This supersedes prior release-log statements that workflow completion was unconfirmed for that revision.
- Scope: GitHub-reported workflow conclusions, **not** independent end-user HTTP/browser verification, accessibility audit, image approval, ServiceNow DEV testing or production deployment. Successful Pages workflow does not by itself establish correct public rendering.
- No screenshot publication approval, customer data or ServiceNow instance verification was added. The static site and CI require no ServiceNow licence; application runtime and optional IntegrationHub/AI/analytics modules require target-instance entitlement assessment.

## 2026-11-07 — Screenshot provenance and publication workflow

- Commit `b4e5a0e`: added `evidence/SCREENSHOT_REVIEW_PROCEDURE.md` documenting source intake, private approval records, irreversible redaction, environment evidence classification, accessible gallery requirements and release validation.
- **Status: procedure committed; no original screenshots inspected, approved or published in this increment.** No new DEV or production verification claimed.
- Publication control: image allowlist remains empty unless a reviewer explicitly authorises an inspected sanitised derivative. Static gallery requires no ServiceNow entitlement; application reproduction may require scoped-app, module, IntegrationHub, AI and analytics entitlements.

## 2026-11-07 — Automated public publication safety gate

- Commits `a983175`, `b565270`, `045fd87`: implemented a dependency-free public asset scanner, six synthetic regression tests, and mandatory GitHub Actions execution.
- Gate scans public HTML/JS/CSS/JSON/SVG assets for selected credential patterns and blocks raster images without a path in `evidence/approved-public-images.txt`. An allowlist entry is an administrative record, **not proof of actual image review**; publication still requires human inspection and permission.
- Repository tree at implementation time contained **no raster screenshot assets**; no image was approved or published. Existing diagrams are HTML/CSS mock representations, not application screenshots.
- Classification: website quality-control **source implemented**; CI execution and live Pages propagation not independently confirmed. No new DEV or production verification.
- Limitations: heuristic patterns do not guarantee detection of all secrets, embedded SVG confidentiality, private data or screenshot suitability. Human review remains mandatory.
- Licensing: static checks require no ServiceNow entitlement. Scoped apps, IntegrationHub, AI and product-specific capabilities require target-instance entitlement assessment.

## 2026-11-07 — Static site link safety and document integrity

- Commit `d0b95d0`: reject local HTML links that resolve outside the site root (including percent-encoded parent paths) and detect duplicate element IDs. This closes a validation blind spot where an existing file outside the publishing tree could incorrectly satisfy a link.
- Commit `0f44b07`: add four regression tests for duplicate IDs, direct and encoded directory escapes, and valid local fragments. Existing GitHub Actions unittest discovery automatically includes the new test module; no workflow configuration change required.
- Verification: GitHub source commits confirmed; CI result and live Pages propagation not yet independently confirmed. These are static website checks, **not** ServiceNow DEV or production verification.
- Publication: no private repository contents, customer data, instance credentials or unreviewed screenshots included.
- Entitlements: static checker requires no ServiceNow licence; scoped applications and optional product modules, IntegrationHub and AI require target-instance entitlement review.

## 2026-11-07 — Quality gate regression tests

- Added `scripts/test_check_site.py` with four dependency-free regression tests covering parser semantics, missing metadata/alt failure, valid cross-page anchors and broken fragment failure (commit `ca62fa7`).
- Updated `.github/workflows/portfolio-quality.yml` to run `unittest` before static site validation (commit `cb3dd82`).
- Evidence: source-only implementation; CI execution and public Pages deployment are not independently confirmed in this change. Tests cover the checker, not application runtime or browser accessibility.
- Publication controls unchanged: no screenshots, private source, credentials or customer data added. Licensing: no ServiceNow entitlement for static checks; scoped-app and optional module/spoke entitlements require target-instance validation.

## 2026-11-07 — Automated portfolio quality gate

- Commit `cb671ca`: added `scripts/check_site.py`, a Python standard-library-only static checker for local links, same-page and cross-page fragment targets, HTML language/title presence and image alt attributes.
- Commit `bad7f36`: added `.github/workflows/portfolio-quality.yml` to run the checker on main pushes, pull requests and manual dispatch. The workflow uses read-only repository permissions and does not deploy or publish assets.
- Verification classification: **source-only** implementation of the checker and CI workflow. A passing GitHub Actions execution has not yet been confirmed; this is not ServiceNow DEV or production verification.
- Scope limits: does not verify external links, dynamic JavaScript behaviour, visual layout, screenshots, accessibility conformance or GitHub Pages propagation. Root-absolute links are deliberately skipped because their resolution depends on the hosting base path.
- Privacy: no screenshots, private code, customer data or secrets introduced.
- Licensing: static site checks require no ServiceNow entitlement; deployed scoped applications and optional IntegrationHub, AI or product-specific capabilities require target-instance entitlement review.

## 2026-11-06 — Interactive evidence-to-delivery walkthrough

- Commit `8dd5b40`: created `evidence-to-delivery.html`, an accessible five-stage, mobile-responsive synthetic walkthrough covering collection, validation, draft finding, reviewed delivery planning and assurance. Synthetic example IDs, counts and hypotheses are explicitly labelled. No customer data, screenshot or private code included.
- Commit `281eaa8`: linked the walkthrough from the public homepage.
- Source evidence reviewed: `solution-lifecycle-studio/README.md` (4.22.2 source-declared; reference-only diagnostic handoff and mock-only external sync) and `Diagnostic-Workbench2/README_BUILD.md` (read-only collectors, DIAG envelopes, 42 rules and historical repository-reported DEV verification).
- Classification: the walkthrough is **mock-only**; underlying architecture is **source-only**; historical DEV results are **repository-reported, not independently DEV-verified**; no production verification. This is not a live cross-workbench transfer.
- Security: no customer identifiers, instance URL, secrets, unpublished images or private source were copied into the public site.
- Validation: GitHub write operations confirmed; live GitHub Pages propagation, keyboard/mobile interaction and independent instance testing remain unverified.
- Entitlements: public static site none; scoped apps, licensed ServiceNow modules, IntegrationHub, AI and provider spokes require target-instance entitlement review.

## 2026-11-06 — Evidence assurance standards and claim acceptance matrix

- Created `evidence-standards.html` (commit `4cf99fc`) with an accessible, responsive evidence classification reference and acceptance matrix for source-only, mock-only, DEV-reported/verified and production-verified claims.
- Added a homepage entry point (commit `7bbd9c5`) and links to the verification ledger and screenshot register.
- Evidence boundary: governance documentation, not new ServiceNow runtime functionality. No original screenshots or private materials were published; no production claims were added.
- Verification: GitHub commits confirmed. Live Pages propagation and cross-device browser testing not independently verified.
- Outstanding: source-to-runtime testing, authorised image review and approval, release propagation checks.
- Licensing: static page none; ServiceNow scoped app, product-specific capabilities, IntegrationHub, AI, analytics and external API entitlements require target review.

## 2026-11-06 — Mobile navigation usability improvement

- Commit `36a8634826ff375685d8c32a16ffbb93a4624050`: replaced the small-screen hidden primary navigation with a native HTML `details`/ `summary` expandable directory. Provides direct mobile access to both flagship projects, engineering case studies, pattern library, verification ledger, visual evidence and contact. The desktop navigation remains unchanged.
- Evidence: existing public portfolio HTML and current Diagnostic Workbench repository README; searched connected Drive for diagnostic documents. No screenshot pixels or private material were published.
- Verification: GitHub write confirmed; live GitHub Pages deployment and mobile browser interaction not independently tested. This is a static-site usability improvement, not evidence of ServiceNow DEV or production functionality.
- Outstanding: inspect and approve actual screenshot pixels, perform mobile browser accessibility testing, independently verify Pages deployment, and test the application runtime in an authorised DEV instance.
- Licensing: public static navigation needs none; underlying ServiceNow custom apps and optional licensed modules, IntegrationHub, AI and third-party spokes require target-instance entitlement review.

## 2026-11-06 — Diagnostic Workbench 2 engineering case study

- Created `diagnostic-engineering.html` (commit `519cf97`) and linked it from the homepage (commit `ea7f559`).
- Evidence: public `Diagnostic-Workbench2/README_BUILD.md` and `knowledge-intelligence/README.md`, reviewed 6 November 2026. The historical source describes 18 stages / 6 phases, 67 runbooks, 20 collector packs, 42 rules and 4 correlations. Knowledge Intelligence 0.1.0 lists 16 packs, 45 collectors, 65 rules and 38 solution patterns.
- Verification boundary: source-backed architecture and historical repository-reported DEV acceptance; Knowledge Intelligence September 30 DEV installation is repository-reported, not independently revalidated. Companion navigation integration remains incomplete. No production claim.
- Security: no customer names, private instance hostnames, screenshots, secrets or private repository content published. Images remain gated pending review.
- Licensing: static page none; custom application, target modules, source KB licensing and optional integrations require entitlement checks.
- Outstanding: independent DEV read-back, cross-workbench handoff testing, screenshot sanitisation and public Pages propagation verification.

## 2026-11-06 — Delivery release case study homepage integration

- Linked the existing `delivery-release-evolution.html` case study from the portfolio homepage with a dedicated responsive section (commit `d64186012c87013c9ffcbc0c1ee0929b7f99732a`). Confirmed the target file exists in the public repository before linking.
- Source basis: `solution-lifecycle-studio` README declares 4.22.2 source; its 4.20.0 DEV read-back is repository-reported, not independently verified. Jira/Confluence/Notion remain mock-only for live provider operations. No production claim.
- Google Drive search located `01-Universal-Delivery-Workbench-Solution-As-Built.pdf`; no private document or screenshot contents were published. Image review and independent public URL verification remain open.
- Licensing: public HTML needs no ServiceNow licence; scoped-app deployment and product-specific patterns, IntegrationHub, AI and advanced analytics require entitlement review.

## 2026-11-06 — Screenshot publication assurance gate

- Created `screenshot-publication-gate.html` (commit `899afe3`), linked from homepage evidence library (commit `9de266e`). Responsive, accessible local-only review tool with nine mandatory controls, source/DEV/mock/production classifications, live blocking status, reset and JSON review-record export.
- Security boundaries: no image bytes fetched, embedded or published; no network submission, storage, analytics or automatic release. The ten screenshot candidates remain unverified and unpublished. A checked control is a self-declaration, not independently confirmed approval.
- Outstanding: open and inspect original images, verify provenance and capture versions, redact and independently review final pixels, obtain explicit publication approval, then add approved galleries. Check GitHub Pages propagation separately.
- Licensing: static review tool requires no ServiceNow entitlement; live scoped applications, platform products and optional integration/AI features require target-specific entitlement checks.

## 2026-11-06 — Source-led verification ledger

- Added `verification-ledger.html` (commit `6d7f9fb`), linked from the portfolio home (commit `c578383`). Nine searchable/filterable evidence records with responsive presentation, keyboard-accessible filters, source links, claim-graduation criteria and entitlement disclosures.
- Re-read current public Delivery Workbench and Diagnostic Workbench READMEs and the private portfolio-control README. Delivery source identifies v4.22.2; its Jira/Confluence/Notion contracts remain mock-only, and MIM showcase is synthetic. Diagnostic README asserts installation on dev438211, classified as **DEV-reported**, not independently DEV-verified. Knowledge Intelligence remains separately deployed and not integrated into local-first page navigation.
- No production-verified claims. The ten screenshot candidates remain unpublished pending pixel-level review and explicit sanitisation. No private source or screenshot bytes were copied into the public repository.
- Pending: independent runtime read-back, screenshot inspection/approval, current source reconciliation for the cross-workbench handoff, and public Pages propagation check.
- Licensing: static site needs no ServiceNow entitlement; scoped app, product modules, spokes, AI and external provider access require target-specific verification.

## 2026-11-06 — Interactive pattern readiness gate

- Added `pattern-readiness.html` (commit `e2af033`) and linked it from the Pattern Library Engineering case study (commit `3049a5a`).
- Delivered a working, mobile-responsive, browser-only 12-control evaluator with five mandatory blockers, remediation output, reset and print support. No backend, analytics, persistence or customer data collection.
- Evidence boundary: illustrative scoring and decision-support only; no claims of live ServiceNow integration, DEV verification, production readiness or formal certification. Current Delivery source README identifies v4.22.2; the September 2026 export assessment is an older historical baseline.
- Security: no private source, Drive screenshot pixels, credentials or client records published. Remaining: image-by-image sanitation and provenance review, current-source-to-historical baseline reconciliation and public deployment check.
- Licensing: static tool needs no ServiceNow entitlement; real scoped application operation and optional product/integration capabilities require applicable licences.


## 2026-11-06 — Pattern library assessment case study

- Published `pattern-library.html` (commit `5753735`) and linked it from the homepage (commit `01e81a6`).
- Evidence: Google Drive `02_existing_96_pattern_assessment.md`, a 28 September 2026 read-only export assessment of 96 solution patterns and 4,595 pattern items; and 5 November 2026 executive pattern-library talking points.
- Historical metrics, quality/completeness scores and the missing SLS pattern-item consumption pathway are explicitly scoped to the assessment baseline. No current DEV or production deployment is asserted.
- Publication: No private source, screenshot pixels, customer information or credentials copied. Source links may require Google Drive permissions.
- Follow-up: independently verify GitHub Pages deployment; inspect screenshot candidates before embedding; cross-check current repository implementation against the historical architecture gap.
- Entitlements: static website requires no ServiceNow licence; scoped apps, products and optional IntegrationHub/AI/analytics require environment-specific checks.
# Portfolio release log

## 2026-11-06 — Source-backed architecture case study

**Published:** `delivery-architecture.html`; linked from the Universal Delivery Workbench featured project card in `index.html`.

**Primary evidence:** Google Drive controlled drafts, all dated 30 September 2026:
- Universal Delivery Workbench Architecture (file ID `1jH9Nwx9iTuhb80XOX3vqA3BnAyjudIM1`)
- Universal Delivery Workbench Solution As-Built (file ID `1fuIlUUiZj_RP3G416RkEAv4vP8sgR1dQ`)
- Universal Delivery Workbench User Guides and Training (file ID `1gIf2j_hhsOT26e9uARpqXOGY6byS1U4-`)

**Source-backed technical facts:** Source release 4.6.1 at commit `c5ac4b5`; last documented DEV read-back 4.5.1; 68 scoped tables and 10 roles observed in DEV; source architecture reports 36 Script Includes, 50 UI actions, 8 jobs, 8 REST operations, 308 ACLs, 334 ACL-role links, 75 modules and 93 UI sections. Source verification reported 258 phase tests and 29 mock scenarios passing at the document cutoff. These are historical/documented figures, not fresh live verification.

**Security and publication:** No private code or raw screenshots published. External Drive originals are linked without changing access permissions. Customer-specific data, private DEV URL and synthetic engagement identifiers omitted. Screenshot version mismatch identified: September training guide explicitly requires fresh version-matched captures.

**Remaining:** Verify latest repo version and current DEV release separately; inspect image assets before sanitised publication; develop corresponding Diagnostic Workbench deep-dive and evidence gallery; validate public GitHub Pages deployment after publish.

## 2026-11-06 — Screenshot provenance and review records

**Commit:** `82ef68dc5386a743f9fdffe5875c3dcfe31aa6ad`

**Updated:** `visual-evidence.html` now has ten independently identified evidence records (DW-IMG-01–06 and VD-IMG-01–04), each with an accessible expandable reviewer record, product association, verification boundary, publication status and targeted inspection criteria.

**Source references:** Existing Google Drive image candidates previously discovered under Workbench dashboard, modules, finding explorer, script search, runs, report output, native workbench and overview pages 1–3. Private Google Drive file identifiers are not exposed on the public page. No screenshots or sensitive contents were copied to the public repository.

**Evidence classification:** All ten remain candidate/unverified and withheld. A filename alone does not establish DEV installation, screenshot provenance, production deployment or permission to publish.

**Next:** Inspect image pixels through an authorised source, redact confidential details, establish version/provenance and owner clearance, then add genuine annotated images. Check public Pages deployment after propagation.

**Entitlements:** Static GitHub Pages needs no ServiceNow entitlement. Scoped application execution and optional spokes/AI/analytics remain subject to platform licensing and permissions.

## 2026-11-06 — Source-to-runtime implementation assurance

- Added `implementation-boundaries.html`, a responsive, accessible technical case study with client problem framing, source-declared implementation details, verification matrix, OOTB-first controls, screenshot publication safeguards and licensing dependencies.
- Linked the new page from `index.html`.
- **Source evidence:** `solution-lifecycle-studio/README.md` declares Delivery Workbench 4.22.2, Delivery Plan, eight narrative document types and mock-only external integration tests; `Diagnostic-Workbench2/README.md` declares the DEV installation and separately deployed Knowledge Intelligence 0.1.0 companion. These are repository statements, not independently executed tests.
- **Status classification:** source-reported, DEV installation reported (not independently verified), mock-only, proposed architecture, and production not verified. No private source, screenshots, credentials or customer data published.
- **Outstanding:** visually inspect and sanitise the ten Drive screenshot candidates; obtain version/rights clearance; validate current DEV behaviour and production evidence; confirm live provider credentials and entitlements before integration claims.
- **Release check:** GitHub commit confirmed; public GitHub Pages propagation not independently confirmed.

## 2026-11-07 — Machine-readable verification governance

- Added `evidence/public-verification-register.json` with six individually classified public claims: Delivery source, historical Delivery DEV, Diagnostic source, Knowledge Intelligence historical DEV, mock external integrations, and proposed cross-workbench handoff.
- Added `scripts/check_verification_register.py`, a standard-library validator checking unique claim IDs, classification vocabulary, required claim provenance, local case-study targets and dated evidence for any future independently verified claims.
- **Evidence boundary:** No independent DEV or production verification performed; no screenshot publication approval inferred. Google Drive source candidates were searched, but no image pixels were inspected or released.
- **Validation:** Script committed; execution in GitHub Actions and Pages propagation not yet independently confirmed. To execute locally: `python3 scripts/check_verification_register.py`.
- **Licensing:** Static register and validator require no ServiceNow entitlement. Scoped applications and optional IntegrationHub, AI, analytics and licensed product modules require separate environment-specific assessment.

## 2026-11-08 — Case-study discoverability

- Homepage desktop navigation now links to `engineering-case-studies.html`.
- Mobile directory exposes the same page; proof-path section includes a prominent call to action.
- Implementation commit: `6c75508629961064e1dac0c340a13cd871165192`.
- Source provenance: existing engineering case-study page and public Delivery/Diagnostic Workbench repository READMEs. No new runtime testing or screenshot approval performed.
- Evidence status: website change SOURCE-ONLY pending GitHub Pages/browser confirmation; underlying architectural narratives SOURCE-ONLY; historical DEV observations remain historical; illustrative demos MOCK-ONLY; no current DEV-VERIFIED or PRODUCTION-VERIFIED claim.
- Next: review authentic screenshot provenance and approvals, check deployment and mobile browser navigation, and verify accessibility.
- Licensing: static website none; ServiceNow runtime/custom application and optional IntegrationHub, ITOM, AI/analytics or connector entitlements require separate assessment.


## 2026-11-10 — Cross-workbench evidence-to-delivery visual walkthrough

- Added `finding-to-delivery.html`: responsive, keyboard-operable five-stage synthetic finding lifecycle, with explicit Diagnostic ownership versus Delivery source-reference boundary and accessible live stage detail.
- Connected the existing pattern explorer to the new walkthrough.
- Source provenance reviewed: `solution-lifecycle-studio/README.md` and `Diagnostic-Workbench2/README.md`. Both contain historical development baseline statements; neither was independently runtime-tested during this change.
- Evidence classification: **MOCK-ONLY** for interactive synthetic walkthrough; **SOURCE-ONLY** for architectural repository descriptions and this website change. **DEV-VERIFIED: not newly established. PRODUCTION-VERIFIED: not established.**
- Safety: no private repository content, customer data, credentials, real screenshots, or live connectors included. No repository visibility changes.
- Entitlements: static page requires none; actual ServiceNow scoped app, ITSM/ITOM, IntegrationHub, PA, AI and provider integrations depend on contracted entitlements and deployment architecture.
- Commits: `7d968202eb56d09fc923e665eeb3471c725cdf91` (walkthrough), `da713491b1e80d69ed3b4ba912dcb919e6a024da` (navigation).
- Verification: GitHub commit acceptance confirmed; GitHub Pages deployment, browser rendering and CI completion not yet independently confirmed.

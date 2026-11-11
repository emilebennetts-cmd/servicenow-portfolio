# Public reviewer access and evidence boundaries — 11 November 2026

## 1. Client's pain & history

The public website linked hiring managers to source repositories that were actually **private**, including links labelled "Inspect public source". These produced a 404 or an authentication request for visitors. The homepage also lacked direct links to the newly published Evidence Ledger and Acceptance Playbook. A stale Diagnostic ledger record stated that an authenticated repository read had failed.

## 2. ServiceNow portfolio solution implemented

- Verified access using GitHub metadata: the public portfolio repository is **public**; the underlying Delivery, Diagnostic and portfolio-control repositories are **private**. No visibility settings were changed.
- Replaced inaccessible private-repository hyperlinks in seven reviewer pages with internal public case-study/evidence links.
- Corrected the Delivery and Diagnostic evidence descriptions: source was reviewed using authenticated access; it is not openly downloadable or independently public-inspectable.
- Refreshed the Diagnostic ledger following a successful authenticated README and Knowledge Intelligence 0.1.0 documentation read on 11 November 2026.
- Added direct homepage hero and mobile-navigation routes to the Evidence Ledger and Acceptance Playbook.
- Added an automated regression test under `scripts/`; the existing quality workflow discovers `test_*.py`.

## 3. Architectural best practices / verification and entitlements

| Layer | Classification | Current evidence |
| --- | --- | --- |
| Static HTML, links, reviewer access and test source | SOURCE-ONLY | Committed in the public website repository; CI for these commits must be checked separately |
| Workbench architecture and documented capabilities | SOURCE-ONLY | Private README review; only paraphrased public-safe summaries are published |
| Knowledge Intelligence DEV install on 30 September 2026 | Historical DEV-VERIFIED (repository-reported) | Not rerun; newer builds not automatically promoted to verified |
| Synthetic walkthroughs and diagrams | MOCK-ONLY | Explanatory only; not actual ServiceNow screen captures |
| Deployed integrated Workbenches | PRODUCTION-VERIFIED | Not established |
| Authentic screenshots | NOT PUBLISHED | Drive screenshot folders discovered; none cleared provenance, irreversible sanitisation and explicit publication approval during this release |

The previous baseline commit `5db703e7ff6f6688f7697fa77bb8b72da4c009b6` showed successful quality-gate, audit and Pages workflow runs on 11 November 2026. Results for these new commits require a separate check.

The static public site does **not** require a ServiceNow licence. Deployed Workbench custom applications may require App Engine/custom-app entitlements and appropriate roles. ITSM, ITOM/Discovery, IntegrationHub, Performance Analytics, Now Assist/AI and provider subscriptions are conditional and require a feature-specific licence review.

No private source, customer data, credentials, unapproved images or private control-repository material was added to the website. This portfolio is not a substitute for authorised target-instance validation.

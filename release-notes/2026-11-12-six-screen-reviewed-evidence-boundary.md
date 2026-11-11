# Six pixel-reviewed Workbench evidence records — 12 November 2026

## Client pain and history
Candidate screenshot titles and synthetic demonstration screens were being conflated with deployed, tested functionality. The portfolio carried ten placeholder slots and four independently inspected, privately retained evidence summaries. Two additional historic image files had been pixel-reviewed but were not yet represented in the public reviewer journey.

## ServiceNow solution / public artefact
The [Visual Evidence gallery](../visual-evidence.html#reviewed-captures) now includes six source-intake summaries, including two newly catalogued records:
- **RV-05 — Diagnostic discovery workshop and process packs:** Source UI capture shows investigation/discovery navigation and an explicitly synthetic MIM readiness example. A visible unanswered workshop count is not completion or acceptance evidence. **MOCK-ONLY content**, original image **HOLD**.
- **RV-06 — Delivery Scope & context:** Source UI capture shows a synthetic MIM foundation and demo-only integration indicators. A displayed 6/6 context-control count is not native workflow execution or live Jira/Notion sync. **MOCK-ONLY content**, original image **HOLD**.

These are text-only, source-observation cards. No pixels, private image URLs, record identifiers, repository contents, customer details or hashes of private originals have been moved to the public site. Source locations, original digests and reviewer caveats remain in private evidence-control records.

The existing ten gallery placeholders remain separate; counts must not be added together because collections can overlap. The source-intake statistics, dates and explicit zero-publication boundary were reconciled. Static assertions and Chromium responsive test coverage enforce six reviewed entries, ten candidate placeholders, explicit MOCK-ONLY/HOLD controls and absence of image tags.

## Architectural best practices
- **SOURCE-ONLY:** This public gallery implementation, tests and release note; source-observation captions do not establish application deployment.
- **MOCK-ONLY:** The synthetic MIM reference content and demo-only integration/status material pictured in RV-05 and RV-06.
- **DEV-VERIFIED:** Historical, version-scoped claims elsewhere in the private source documents. Neither new card has independent runtime read-back, dated acceptance outcome, or installation identity.
- **PRODUCTION-VERIFIED:** None from these images.
- **Publication:** HOLD. Manual sanitisation, derivative-byte verification, scope/version reconciliation and explicit image-plus-caption rights clearance are all still required.
- **Licensing:** Static page and browser tests: no ServiceNow licence. Native Workbench and associated ITSM/CMDB/ITOM, App Engine, IntegrationHub, analytics/AI or third-party provider capabilities require contract-specific entitlement, ACL and identity verification.

## Release acceptance
- Public file: `visual-evidence.html`.
- Automated checks: `scripts/test_visual_intake_safety.py`, `scripts/browser_navigation_smoke.py` across 390, 768, 1024 and 1440px.
- Verify each GitHub Actions run and GitHub Pages deployment against its specific commit. A committed test is not an executed test.
- Rollback: restore prior gallery and test revisions. No image assets or ServiceNow records need to be rolled back.

**Final-release CI, browser and hosting status is not asserted until GitHub Actions reports it.**

# Release — Searchable public evidence claim catalogue (14 November 2026)

**Scope:** Public portfolio presentation + publication regression controls; **no ServiceNow package or instance change**.

## Client pain and history

The technical evidence register explained six dated source/runtime baselines, while the authoritative public JSON register held 86 separately classified claims. A reviewer could not navigate all registered claims from the HTML evidence page, forcing manual inspection of a large JSON file. Duplication of a hand-curated second catalogue could introduce stale class labels.

## Delivered solution

- Added a responsive searchable catalogue at [Technical Evidence Register — complete claims](../technical-evidence-register.html#claim-catalogue).
- Dynamically loads the **version-controlled public-only JSON register** from the same website origin; renders titles, claim identifiers, classes, detailed basis, runtime boundaries and screenshot statuses, with links to the matching public case study.
- Text and classification filters, accessible live count and increments of 12 cards avoid overwhelming small screens. Empty result and inaccessible/corrupted JSON paths fail visibly rather than inferring or fabricating claims.
- Fail-closed client validation: expected schema 1.0, unique bounded IDs, supported classes, bounded textual fields and local-only `.html` path slugs. Every data value is rendered with `textContent` / DOM creation; **never `innerHTML`**.
- Existing six dated source-to-DEV evidence comparisons remain unchanged.
- Extended source regression tests and four-width Chromium workflow to cover real same-origin JSON loading, query, pagination, filtering, rejected malicious data, layout overflow and JavaScript exceptions.
- Preserved public verification claim count at **86**: 53 SOURCE-ONLY, 4 historical DEV-REPORTED, 20 MOCK-ONLY, 9 PROPOSED, **0 newly DEV-VERIFIED**, **0 PRODUCTION-VERIFIED**.
- Public code and test changes only; no private source, personally identifiable data, customer records, credentials, screenshot pixels or unapproved images.

## Architecture and validation

**Architecture:** GitHub Pages static HTML, offline-safe JavaScript and same-origin public JSON. No API credentials, external services, persistence or remote submission. This is a reader over an evidence register, not a native execution or an acceptance application.

**Verification:** The per-commit source and browser GitHub Actions results are authoritative. Static Python tests check DOM selectors and classification boundaries. Chromium tests cover 390, 768, 1024 and 1440 px. A successful CI run demonstrates this public presentation only; it does not prove any native ServiceNow deployment. The public webpage itself must be checked separately for external propagation.

**Genuine screenshots:** 0 approved; visual publication HOLD remains mandatory. Original screenshots require explicit rights, provenance, irreversible sanitisation, approved derivative digest and individual authorisation.

**Licensing:** Viewing the public catalogue needs no ServiceNow licence. Native App Engine/custom-application tables and ServiceNow ITSM, ITOM/Discovery, IntegrationHub, Performance Analytics, AI or third-party capabilities depend on actual customer subscriptions, assigned roles, licensed features and target environment. No implied entitlement transfer or purchase.

## Evidence / limitations

- Source evidence: `solution-lifecycle-studio` 4.22.2 source declaration; separately documented 4.20.0 historical DEV read-back; `Diagnostic-Workbench2` SDK and separately deployed companion; controlled historical Delivery As-Built and Diagnostic runbook.
- Runtime evidence: none newly obtained. Prior DEV-reported claims remain reported-only, separated from independently witnessed DEV-VERIFIED and Production-VERIFIED.
- No repository visibility changes. Restricted evidence provenance is recorded in the private control repository, without publishing its contents.

# Native Observation Capture Workbook — Release and Evidence Boundary

**Date:** 14 November 2026 (Australia/Sydney)  
**Public entry:** [Incident Pack — Native Observation Workbook](../incident-pack-native-pilot.html#native-observation-log)  
**Evidence:** SOURCE-ONLY frontend implementation and contract; browser-local user observations are **SELF-REPORTED / UNREVIEWED**, not independent DEV evidence. Historical pilot remains **DEV-REPORTED**, with separate mock demonstrations. No production verification, screenshot approval or live connection.

## 1. The client's pain & history

The controlled native acceptance catalogue contains 29 intentionally **NOT RUN** cases (NV-001–NV-029), spanning metadata, role-based authorisation, cross-engagement isolation, additive generation, idempotency, concurrency, recovery and formal approval. The 21 October synthetic pilot reports narrow metadata read-back and draft creation, but those observations do not independently certify the source candidate. The former public matrix allowed filtering and a static NOT RUN CSV, but gave a technician no client-neutral way to assemble candidate observations for private review.

## 2. The ServiceNow solution

Added a **browser-local observation capture workbook** alongside the original 29-case matrix. Each planned case retains its original ID, workstream and persona. A consultant may select NOT RUN, OBSERVED PASS, OBSERVED FAIL or BLOCKED and attach an anonymous private evidence alias. Missing or unsafe evidence aliases are flagged without requiring network calls or storing data. A constrained optional target identity captures an anonymous environment alias, installed version, application scope and exact Git commit SHA; invalid identifiers are excluded from export.

An export creates a deterministic 29-record JSON candidate with explicit evidence deficiencies, never silently promoting a result. **All exports contain publication_status = HOLD, native_verification_status = NOT VERIFIED, independent_review_approved = false, release_authorised = false, and dev_verified/production_verified = false for every case.** No JavaScript writes to ServiceNow, Google Drive or GitHub; all session state is in memory, not localStorage. Reset clears input. The existing NOT RUN CSV remains available.

This is an **evidence-intake tool**, not the execution environment or final evidence registry. The release does not claim that any of the 29 cases have been run in a target instance.

## 3. Architectural best practices

- Keep scoped application/version/commit/target identity explicit and separate from historic DEV reports.
- Use least-privilege personas and independent negative-access tests; a self-recorded PASS is never proof of ACL enforcement.
- Retain original, separately authorised ServiceNow/ATF evidence in approved private storage; use anonymous aliases in the public browser.
- A review candidate may help an independent reviewer find tests, but only a separate witnessed review and authoritative acceptance record can promote a claim to DEV-VERIFIED.
- No client data, instance URLs, credential fields, original screenshot pixels, write integrations or external dependencies are embedded in this static page.
- OOTB first: native Incident, Change, ACLs, ATF and platform approval mechanisms remain authoritative; a Workbench should orchestrate evidence rather than replace them.

## Verification and files

- Public page: incident-pack-native-pilot.html section #native-observation-log
- Unit contract tests: scripts/test_native_observation_workbook.py
- Chromium tests at 390, 768, 1024 and 1440 px: scripts/browser_native_observation_workbook.py
- Responsive workflow: .github/workflows/portfolio-responsive-smoke.yml
- Updated existing INCIDENT-PACK-NATIVE-MATRIX-20261114 evidence claim, without changing its SOURCE-ONLY classification or inflating the register count.
- Private release-control receipt records the boundary. CI and GitHub Pages must be checked against the **final** commit; browser tests are not native ServiceNow acceptance.

## Licensing and status

The public static page and browser-local JSON export require **no ServiceNow licence**. Actual Workbench deployment requires review of App Engine/custom-application and custom-table entitlements, role/ACL grants, and non-production instance rights; native Incident/Change, ATF, ITOM/Discovery, IntegrationHub/spokes, document generation and AI may add contract-specific dependencies if used. Do not assume an entitlement because a technical component exists.

**Remaining HOLDs:** authorised target access, version-pinned native execution of the 29 cases, independent review/sign-off, explicit screenshot-by-screenshot authorisation and irreversible sanitisation, and production acceptance. No private repository visibility or source publication was changed.

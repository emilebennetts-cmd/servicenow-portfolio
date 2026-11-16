# 16 November 2026 — Diagnostic Workbench ten-pack evidence coverage gate

**Public entry:** [Diagnostic Collector Coverage — coverage gate](../diagnostic-coverage-explorer.html#coverage-gate)  
**Publication classification:** SOURCE-ONLY implementation, MOCK-ONLY synthetic assessment inputs and outputs; NOT RUN / HOLD for native execution.

## 1. The client's pain and history

A representative brownfield ServiceNow assessment often combines incident, CI, Discovery, risk, case and integration data from products with uneven licensing, incomplete ACL access and inconsistent query limits. An empty result can mean a missing entitlement, a skipped table, an incorrect denominator or genuine zero findings. Treating all of these as healthy turns a demonstration dashboard into false assurance.

Historical provenance was reviewed in the access-restricted Diagnostic Workbench 2 source README and 1 September 2026 build documentation, together with controlled Universal Delivery Workbench As-Built and architecture material. These documents describe historical source and DEV states, **not** fresh runtime execution or a customer outcome.

## 2. The ServiceNow solution

Added a ten-category synthetic evidence coverage exercise to the existing [collector explorer](../diagnostic-coverage-explorer.html). The category names align to the existing public, source-informed inventory. The browser shows four deterministic hypothetical snapshots:

1. Ten unassessed packs.
2. Mixed outcomes including unknown entitlement, invalid envelope, capped denominator, independent review pending and proposed exclusion.
3. Nine synthetically reviewed packs with one capped denominator.
4. Ten synthetically reviewed packs which **still** do not establish any native verification.

The user can filter actionable versus synthetically reviewed categories and export ten canonical rows with immutable **MOCK-ONLY**, **NOT RUN**, **HOLD** and boolean false verification/publication fields. No names, accounts, target URLs, private evidence receipts or actual collector results are accepted.

Implementation:
- \`diagnostic-coverage-gate.js\`: isolated and deterministic evaluation, source-category mapping, private-data-free CSV export, canonical output validation and safe spreadsheet-field escaping.
- \`diagnostic-coverage-explorer.html\`: responsive, keyboard-accessible illustrative console with live announcements, all ten categories and source/entitlement boundaries.
- \`tests/diagnostic_coverage_gate.test.cjs\`: source-inventory agreement, all four states, unknown-identity fail-closed behaviour, denominator guard, all-reviewed-not-certified rule and export contract.
- \`.github/workflows/portfolio-quality.yml\`: automatic Node test on pushes and pull requests.
- \`index.html\`: direct navigation to the new exercise.

## 3. Architectural best practices

**OOTB-first:** Native evaluation should begin with product install/subscription, scope, ACL and supported service-specific reporting or health tools. Supplementary read-only collectors require explicit permission, privacy minimisation and safe scale constraints.

**Separation of duties:** The source-informed model demonstrates why a rule finding is a draft until independently confirmed; a proposed exclusion is not a healthy module, an aggregate with a capped denominator cannot certify completeness, and even a complete example remains on release HOLD.

**Source-to-runtime distinction:** The exercise is a local static website. It never calls ServiceNow, stores imported records, executes collectors, sends data to a third party, or treats synthetic review as an actual acceptance result. No genuine instance screenshots are published.

## Verification and blockers

At authoring: committed source and regression tests; GitHub Actions / browser / Pages results require their own completed receipts and are **not inferred** from a commit. New native DEV-VERIFIED: **0**. New PRODUCTION-VERIFIED: **0**. Screenshot approvals: **0**.

Native validation requires a permitted DEV test environment, target version and installed plugin read-back, ten applicability decisions, licensed module access, no-mutating-script review, bounded actual collector execution if approved, complete population reconciliation, negative ACL/persona checks, independent reviewer and publication sign-off.

**Licensing and entitlements:** No ServiceNow licence for public static training. ITSM, ITOM Visibility/Discovery, Security Operations, IRM, CSM, HRSD, ITAM/HAM/SAM, IntegrationHub, Performance Analytics or other product capabilities must be checked against target instance subscriptions, activation and role permissions before native assessment. Additional external provider licences apply to live integrations.

**Security:** No customer records, personal data, credentials, restricted source files, private screenshots or changes to repository visibility. Live execution and release decisions remain HOLD.

# 16 November 2026 — Diagnostic collector count-semantics correction and hostile-fixture guardrails

Public page: [DIAG Envelope Assurance Lab](../diagnostic-envelope-assurance-lab.html)
Classification: **SOURCE-ONLY** public implementation; **MOCK-ONLY** synthetic fixtures; **NOT RUN / HOLD** native checks; newly **DEV-VERIFIED 0**, **PRODUCTION-VERIFIED 0**, screenshot approvals **0**.

## 1. The client's pain & history
When an assessment mistakes a collector's `record_count` for the table denominator, it can falsely flag or accept output: the original Incident collector uses `record_count = envelope.results.length`, while `metrics.total` is a separate GlideAggregate count. A source-informed public demonstration had conflated these measures. This cycle resolves that provenance error before it could influence an acceptance story.

## 2. The ServiceNow solution
Corrected the public synthetic model and illustrative console to preserve the two separate quantities. Extended the nine fixed fixtures to **15**, adding a nonzero incident population with zero output groups, a group-count mismatch, an impossible open-to-total relationship, unexpected metadata, a disallowed result value and malformed notes. The evaluator now checks group count against result-array length, safely bounds the example group types/values and rejects unrecognised fixture fields, unexpected nested data and invalid metric shapes. All checks run entirely in-browser, with no user-submitted data or network access. The CSV now exports 15 synthetic dispositions and an unchanged eight-control NOT RUN / HOLD native worksheet.

## 3. Architectural best practices
The private source at `Diagnostic-Workbench2/tools/wb2_catalog.json` contains the `ITSM-INC-001` sourceText setting `envelope.record_count = envelope.results.length`; the same collector populates `metrics.total` through an `incident` GlideAggregate query. The public evaluator remains a **deliberately restricted teaching model**, not the private intake parser. Its small group-value allowlist is not a statement of permitted values for the real application. Do not use it on customer envelopes. Never treat zero returned groups as zero incident rows, or a shape check as reviewer approval. Preserve distinct Diagnostic and Knowledge Intelligence evidence contracts.

**Verification:** Regression assertions added for count semantics, malformed group records, privacy rejection, N/A, capped denominators, 15-row exports and immutable HOLD decisions. Chromium coverage expanded across four viewports; CI result must be checked separately after commit.

**Licensing:** Static site none. Native collection needs permission to execute read-only Scripts – Background queries, relevant ITSM product/table and role access, approved custom-app hosting rights where applicable and actual licence checks for any further ITOM, SecOps, IRM, CSM, HRSD, ITAM, IntegrationHub or analytics use. **Native DEV and Production validation NOT RUN**. No restricted code, real customer payloads, credentials or unapproved images published.

# Delivery Release Identity Preflight — 15 November 2026

## 1. The client's pain & history

The Delivery Workbench documentation contains unresolved version evidence: source README 4.22.2, historical 5 October DEV-reported 4.20.0, and a controlled 19 October As-Built / Architecture assertion of a 6 October DEV 4.22.2 read-back that conflicts with its own front-matter warning. A separate historical demo scope differs from the protected source scope. An attractive UI or matching display name cannot reconcile a scoped package or justify a production claim.

## 2. The ServiceNow solution

Added [Release Identity Preflight](../delivery-release-evolution.html#release-identity-preflight) directly to the existing evidence-led Delivery release case study. This is a working offline browser comparison, **not** a native ServiceNow integration or acceptance test.

- Pins the reviewed source **scope** `x_1577958_vdf` and **version declaration** `4.22.2`.
- Accepts user-entered, non-sensitive target technical scope and version; input shape is checked and compared as text, without fetching external sources.
- Includes four local synthetic examples: scope mismatch, prior version, aligned labels and unknown target.
- Outputs **MISMATCH**, **INVALID INPUT**, **UNAVAILABLE** or **TEXT MATCH · NOT VERIFIED** for each observed field. Every outcome maintains **release decision: HOLD**, including both labels matching.
- Downloads a versioned JSON worksheet containing only the comparison classes, source release declaration and outstanding acceptance gates; raw target values, customer identifiers and secrets are never serialized.
- Provides accessible status announcements, keyboard-operable controls, mobile layout and print-aware presentation.

The implementation is deliberately **MOCK-ONLY** as a client-side comparison and **SOURCE-ONLY** for the reviewed baseline. It cannot attest DEV or Production, validate source package hashes, perform ServiceNow reads or authorise screenshot publication.

## 3. Architectural best practices

OOTB-first release governance requires target installed application sys_id/scope/version, exact package and commit provenance, scoped UI Page read-back, role/ACL positive and negative tests, synthetic application acceptance, release and rollback approvals. A source version or local string comparison is never treated as installed evidence. Diagnostic Workbench remains the operational evidence owner; Delivery owns governed references.

**Security / privacy controls:** No external requests, localStorage, analytics, import of unreviewed screenshots or credentials. Comparison statuses only are exported. Input controls deliberately warn against real customer data, sys_ids, tokens and evidence content. The prior public original-screenshot publication gate stays **0 approved / HOLD**.

**Automated verification:**
- `python -m unittest scripts.test_release_identity_preflight -v` validates non-certifying export fields, source boundary, no private links or data-containing export.
- `python scripts/browser_release_identity_preflight.py` runs Chromium at **390 / 768 / 1024 / 1440px**, including keyboard-renderable layout, four presets, input validation, unchanged HOLD decision, input value redaction and download checks.
- Workflow: `.github/workflows/release-identity-preflight-browser.yml`. Only a completed successful Actions run on the functional code commit proves the public tool tests; never a native ServiceNow acceptance.

**Entitlements:** Public static website: **none**. Native tests or installation require authorised ServiceNow DEV access, appropriate App Engine/custom scoped application and table rights, role/ACL assignments, subscribed ITSM/ITOM/IRM/HRSD/CSM functionality where in scope, and any applicable IntegrationHub, AI/analytics, external vendor and third-party licences. Confirm target agreement, release and role model independently.

**Outstanding:** Resolve 4.20.0 versus 4.22.2 dated records with attributable installed package read-backs; verify target compatibility and scope; independently execute DEV and Production acceptance as separately authorised. No new DEV-VERIFIED or PRODUCTION-VERIFIED claims. Genuine original screenshot approvals remain **0 / HOLD**.

## Change trace

- Public feature implementation commit: `aca0755c2edca32e2519ea6f4eec509a3ea760ce`
- Browser workflow and tests introduced: `5d8bd387ede0191bbe088e0f89155027559b514a` (test workflow commit)
- Restricted document IDs, customer-level provenance and any future native receipts are retained only in the private control repository.

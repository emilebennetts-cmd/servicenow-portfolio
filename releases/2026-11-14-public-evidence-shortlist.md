# Release — Public Evidence Briefing Shortlist (14 November 2026)

**Status:** SOURCE-ONLY public website feature; `UNREVIEWED / NOT VERIFIED / HOLD` for every exported packet. **Scope:** presentation and client-only export, not a native ServiceNow deployment.

## 1. The client's pain and history

A technical reviewer previously had 86 public evidence claims to inspect, using keyword search, classification filters and 12-at-a-time paging. A hiring manager or technical architect needed to send a curated set of claims to a stakeholder, but copying raw JSON or screenshots could strip away the version-specific verification boundary or encourage the inadvertent disclosure of unapproved evidence.

The register mixes source-described functionality, synthetic demonstrations, proposals and four historical DEV-reported observations. None is independently DEV-VERIFIED or PRODUCTION-VERIFIED by the portfolio. Original Workbench screenshots remain individually unapproved.

## 2. The ServiceNow solution and delivered implementation

Extended [Technical Evidence Register](../technical-evidence-register.html#claim-shortlist) with a public-only briefing builder:

- Select any public claim with a keyboard-accessible checkbox, preserving selections when searching, changing classification or loading the next group of 12.
- Review selected IDs, titles and evidence classifications, remove individual selections, and clear all selections.
- Export a Markdown briefing suitable for offline review, or a structured JSON packet with schema version and immutable public website links.
- Exports carry explicit `review_state=UNREVIEWED`, `verification_state=NOT VERIFIED`, `release_state=HOLD`, and `false` for native execution, independent review and screenshot publication.
- Only fields from the validated same-origin public register are exported. No user-supplied notes, secrets, private source URLs, Drive links, customer instance URLs or screenshot pixels are accepted.
- No network submission, browser storage or ServiceNow API calls. Closing the tab discards selections.

The existing evidence claim `COVERAGE2-20261113-TECHNICAL_EVIDENCE_REGISTER` was expanded (still SOURCE-ONLY); the register remains at **86** claims without artificial claim inflation: 53 SOURCE-ONLY, 20 MOCK-ONLY, 9 PROPOSED and four historical DEV-REPORTED.

## 3. Architectural best practices and verification

The design reuses the public JSON schema rather than maintaining a duplicate list. Each claim is validated for unique ID, allowed classification, bounded descriptions and local-safe page slug before rendering. Data is inserted using DOM `textContent`, never HTML interpolation. Downloadable Markdown escapes formatting-sensitive text; the exported JSON has a stable explicit contract. Public links use a pinned canonical GitHub Pages origin. Buttons are disabled when there is no selection or valid register.

The existing [Workbench source lineage workflow](../.github/workflows/technical-evidence-lineage.yml) runs contract tests and Chromium checks. Its browser test now exercises cross-filter persistence, JSON and Markdown downloads, conservative verification flags, clear/reset, rejected poisoned input and layout at 390, 768, 1024 and 1440px. Actual CI results must be inspected against the resulting commits; source and browser tests **never** verify a native ServiceNow instance.

**Evidence provenance:** reviewed the public 86-claim register, the public claim catalogue tests and existing lineage comparison, the private Delivery source README, the separate Diagnostic SDK README and the connected Universal Delivery Workbench As-Built file inventory. The published release uses only pre-approved public claim fields. Private source and Drive documents are not republished.

**Screenshot governance:** zero genuine screenshots approved for publication. Images are still withheld until ownership, permanent redaction, derivative digest and individual authorisation have been recorded.

**Licensing / entitlements:** This static website and locally generated briefing require **no ServiceNow licence**. Validating native Delivery/Diagnostic features requires approved target-instance roles and ACLs, appropriate App Engine/custom-application table entitlements, and any actual ITSM, ITOM/Discovery, Service Graph, IntegrationHub, analytics, AI or third-party rights for the capability under test. An exported briefing cannot establish such entitlements.

**Unclosed acceptance:** independent native DEV execution, production verification, screenshot-specific approval and independent site retrieval remain distinct and unclaimed. No repository visibility has changed.

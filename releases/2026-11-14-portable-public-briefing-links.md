# Public evidence briefing — shareable review links (14 November 2026)

**Status:** SOURCE-ONLY static website improvement. All linked selections remain **UNREVIEWED / NOT VERIFIED / HOLD**. No new native ServiceNow verification.

## 1. The client's pain and history

The public technical register contains 86 evidence claims. Reviewers could select and download Markdown/JSON briefing packets, but there was no way to hand another reviewer a reusable link to the same curated claim selection. Manually copying claims risked missing their verification classifications and historical version boundaries.

## 2. The ServiceNow solution and completed implementation

The existing public-only briefing builder at `technical-evidence-register.html#claim-shortlist` now generates a portable review link containing **only up to 12 public claim IDs**. It never embeds claim bodies, evidence aliases, customer records, Drive URLs, private source or screenshots. A recipient opening the link sees the same claims after they are revalidated against the current same-origin public register, with the normal SOURCE-ONLY, MOCK-ONLY, PROPOSED or DEV-REPORTED badges.

The builder provides a read-only copyable URL field, a copy action with a manual fallback, and a working open-link anchor. It also supports existing downloadable Markdown/JSON packets for larger claim sets. No browser storage, remote submission or network destination is introduced. Links are deliberately non-certifying and do not grant approval.

## 3. Architectural best practices and verification

- Deep-link parsing validates exactly one `brief` parameter, 1–12 unique, bounded alphanumeric public claim IDs, and rejects unknown IDs after loading the authoritative public JSON.
- The target URL is generated from the same-origin current site path; all other query parameters are discarded, retaining the GitHub Pages project prefix.
- Invalid/forged/oversized/repeated links fail closed with an accessible status message and empty selection. No unsafe markup interpolation or private-file reads occur.
- Static contract tests cover bounded parsing and no browser persistence. Headless Chromium covers round-trip share/restore at 390/768/1024/1440 pixels and rejects malformed links.
- The existing public claim count remains **86**, with four historical DEV-REPORTED and zero newly DEV-VERIFIED / PRODUCTION-VERIFIED claims. All original ServiceNow screenshot candidates remain **HOLD (0 approved)**.
- CI or GitHub Pages success validates the public front end, **not** the underlying ServiceNow scoped apps, licences, ACLs, native execution, operational acceptance or customer runtime.

**Evidence provenance:** Existing public same-origin register and source-traced lineage. The private Delivery/Diagnostic source repository READMEs and controlled Drive As-Built and training files were located; none was republished or directly embedded. No private repository visibility changed.

**Entitlements:** No ServiceNow licence needed for the static site or browser deep link. Native implementations require target-specific confirmation of App Engine/custom-table rights, scoped roles/ACLs and any ITSM, ITOM/Discovery, IntegrationHub, Performance Analytics, AI, document-generation, provider or external service entitlements.

**Open gates:** Independently witnessed native DEV test evidence, production verification, individual irrevocably sanitised genuine screenshot approvals and separately verified public HTTP availability.

# Offline 29-case Candidate Delta Review — Evidence-Governed Release

**Release date:** 14 November 2026 (Australia/Sydney)  
**Public page:** [Candidate Delta Review](../candidate-delta-review.html)  
**Entry points:** [Incident Pack native workbook](../incident-pack-native-pilot.html#native-observation-log), [portfolio home](../index.html), [Portfolio Explorer](../portfolio-explorer.html)  
**Evidence:** SOURCE-ONLY public code; input candidates SELF-REPORTED / UNREVIEWED; native DEV-VERIFIED and PRODUCTION-VERIFIED **not established**.

## 1. The client's pain & history

A consultant using the 29-case offline Incident Pack workbook can prepare and export two candidate observation files across different non-production rehearsal sessions. Before this release, each candidate could be resumed but lacked a defensible change comparison. A status moving from OBSERVED PASS to OBSERVED FAIL, an evidence-alias being removed or a different source/target context could go unnoticed. These are representative delivery control risks, not a measured claim about a specific customer.

The source-of-truth for NV-001 through NV-029 is the existing public Incident Pack native acceptance catalogue. The programme source contains historical, bounded synthetic/DEV-reported pilots, but the 29-case acceptance execution remains unrun and unverified. Nothing in this change promotes those historical reports.

## 2. The ServiceNow solution

Added `candidate-delta-review.html`, a responsive, accessibility-aware **local-file-only** comparison tool:

- Compare two explicitly selected workbook 1.0 JSON candidate exports, each capped at 128 KiB.
- Validate all 29 pinned IDs, titles, workstreams and personas; reject missing or extra fields, unsupported statuses, mutated review or verification flags, unsafe aliases, invalid context identifiers, malformed evidence-missing lists and oversized files.
- Calculate status transitions, reported failure/blocker attention cases, evidence-alias **presence-only** changes and context-field mismatches. Offer all/changed/attention filters.
- Export a minimal JSON delta manifest with case statuses and alias-presence changes **without exporting underlying evidence aliases, private identifiers or input context values**.
- Reset both file inputs and in-memory candidate state. The page does not use network APIs, browser storage, analytics, forms, screenshots, credentials or ServiceNow access.
- Display permanent NOT VERIFIED / UNREVIEWED / HOLD disclosures even for apparently improving outcomes. Neither the inputs nor the downloaded comparison is an attestation.

The page is linked from the workbook, public home mobile directory and searchable Portfolio Explorer. Its source-only register entry is `INCIDENT-CANDIDATE-DELTA-20261114`, bringing the public register to 86 claims.

## 3. Architectural best practices

**Boundary:** File-format checking does not authenticate a file's author, real execution, timestamp, source commit or target installation. Identical candidate metadata is only a reported context match. Evidence missing/removed from a candidate must be reviewed privately; a positive status change is never an approval.

**Attack surface:** All candidate values are validated before comparison. Output DOM uses `textContent` or `createElement` rather than interpolating uploaded data into HTML. The page applies a restrictive CSP (`default-src 'none'; connect-src 'none'; img-src 'none'`), no external resources and no persistent storage. Rejected input clears rendered results and disables export rather than preserving potentially misleading stale comparison results.

**Testing:** `scripts/browser_candidate_delta_review.py` generates real 1.0 candidates by operating the original local workbook, compares them at 390, 768, 1024 and 1440 px, tests changed/attention filtering, exports HOLD JSON, and tests forged independent approval, altered planned-control identity and reset. Dedicated GitHub Actions workflow: `.github/workflows/candidate-delta-review.yml`. The release is not marked CI-PASSED until the workflow actually succeeds on the final commit.

**Sources reviewed:** `solution-lifecycle-studio/README.md` (source version 4.22.2), `Diagnostic-Workbench2/README.md` and KI companion README, 30 September 2026 controlled Delivery As-Built (source 4.6.1 / historical DEV 4.5.1), fictional Diagnostic completion runbook, and the existing Incident Pack workbook. Those separate application/version/source baselines are not conflated. No private URLs, code, screenshot content or customer data were published.

**Licensing:** Static GitHub Pages and local browser comparison have no ServiceNow licensing requirement. Native acceptance requires authorised non-production access, App Engine/custom application/table entitlements as applicable, appropriate roles/ACLs and product rights for ITSM, ATF, ITOM/Discovery, IntegrationHub/spokes, analytics, AI and third-party services when invoked. Contract evidence and installed product rights remain unresolved, not inferred.

## Verification and release control

| Item | Position |
|---|---|
| Source implementation | Committed to public portfolio |
| Syntax, 29-case alignment, local links and safety contract | Checked in source; Chromium CI to confirm |
| Browser acceptance tests | Authored; GitHub Actions outcome must be checked |
| Live website external HTTP reachability | Not independently confirmed |
| DEV / Production acceptance | Not run as part of this release |
| Native independent reviewer evidence | Not supplied; HOLD |
| Screenshot publication | Zero image-specific approvals; HOLD |
| Private repositories | Visibility unchanged |

**Publication decision:** safe to publish this static, non-sensitive, source-only comparison page. Do not promote any individual imported case to DEV-VERIFIED or PRODUCTION-VERIFIED until an independently witnessed native acceptance process records the attributable execution and original private evidence. Do not publish any captured ServiceNow screen without image-specific review and irreversible sanitisation.

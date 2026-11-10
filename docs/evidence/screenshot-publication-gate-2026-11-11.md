# Screenshot evidence intake and publication gate

Updated: 2026-11-11. Status: SOURCE-ONLY (process definition, not screenshot approval).

## Purpose
Publish real ServiceNow Workbench screens only after source provenance, sanitisation and explicit release approval. Do not substitute generated mockups for product evidence or infer DEV/PROD status from a filename.

## Intake record (one per candidate)
| Field | Required entry |
| --- | --- |
| Evidence ID | Stable non-identifying reference, e.g. DW-IMG-001 |
| Origin | Repository path or restricted Drive file ID; never a public customer link |
| Application and feature | Diagnostic / Delivery, screen and user journey |
| Capture date and environment | Date; DEV / TEST / PROD / unknown |
| Application version/build | Exact version or unknown |
| Operator / permission | Role used, without account identifiers |
| Verification | SOURCE-ONLY / DEV-VERIFIED / MOCK-ONLY / PRODUCTION-VERIFIED, with independent corroboration |
| Rights | Ownership and publication permission confirmed by named approver |
| Sensitive content check | Names, emails, sys_ids, instance URLs, hostnames, IPs, ticket numbers, financial or health data, customer branding, tokens |
| Redaction | Irreversible flattened image; original retained only in restricted storage |
| Reviewer | Reviewer, review date and decision |
| Public path | Only after approval, under assets/screenshots/ (the enforced allowlist path) |
| Caption | What is genuinely shown, version/environment and limitation |
| Source reference | Public safe design document or sanitized evidence reference |

## Release gate
1. Locate original in approved repositories or restricted Drive and establish provenance. A diagram, browser rendering, or synthetic dataset is not automatically a real instance screenshot.
2. Confirm rights to publish and that no customer contractual restriction applies. If uncertain, keep private.
3. Make a separate derivative and irreversibly redact all sensitive identifiers and contextual disclosures. Do not use CSS overlays or SVG text masking.
4. Review image at full resolution and inspect metadata/EXIF, filename, alt text and captions for leakage.
5. Obtain explicit approval of the **final derivative**, not merely the original screenshot.
6. Add descriptive alt text and a visible evidence classification; avoid asserting PROD without release-specific proof.
7. Run the portfolio link/sitemap quality gates and manually inspect mobile, zoom, keyboard navigation and image loading.
8. Record SHA-256 of the approved derivative, reviewer decision and commit in the release log. Retain originals only in authorised restricted locations.

## Evidence boundaries
- **SOURCE-ONLY:** code, documentation or page committed; does not prove a ServiceNow runtime.
- **DEV-VERIFIED:** attributable, dated, version-specific development-instance observation; never implies production.
- **MOCK-ONLY:** synthetic or illustrative visual; label it prominently.
- **PRODUCTION-VERIFIED:** only when attributable production release evidence and permission exist.

## Current inventory
No screenshot is approved for publication by this document. Existing illustrative HTML screens remain MOCK-ONLY. The historic Delivery DEV evidence is not proof that newer source releases are installed.

## Entitlements
This intake process and static gallery need no ServiceNow licence. Capturing and demonstrating runtime features depends on the instance and contractual entitlements, potentially App Engine, ITSM/ITOM, IntegrationHub, Performance Analytics and AI; confirm the actual product subscriptions before claiming deployability.

## 11 November 2026 — automated binary checks
The public CI publication gate now checks the magic-byte signature of each approved PNG, JPEG, WebP, GIF, BMP or TIFF against its extension, rejects approved files over 8 MiB, and still verifies the SHA-256 allowlist. Unit tests cover disguised files, mismatched bytes and oversized captures. These are **technical guardrails, not a content, EXIF, rights or sanitisation review**. Final human approval remains mandatory. Verification: SOURCE-ONLY until the corresponding GitHub Actions run passes. No new image was approved or published in this change.

# Release record — 2026-11-11 — sitemap integrity gate

## Delivered
- Added `tests/check_sitemap_integrity.py` to verify canonical GitHub Pages URLs, unique sitemap entries, safe local paths and existing HTML targets without network access.
- Wired the gate into `.github/workflows/portfolio-audit.yml` for push, pull request and manual dispatch.

## Evidence and verification
- SOURCE-ONLY: GitHub contents API accepted both commits, `ca9250860072e5d8ffd091afe92434bace6f87fc` and `ef9d4e8933c50c89092fc7e209b60a3ded49ea40`.
- DEV-VERIFIED: No ServiceNow instance testing performed.
- MOCK-ONLY: No new demonstration.
- PRODUCTION-VERIFIED: Not established.
- CI: Workflow execution and results not independently inspected in this release.
- Public deployment: No new HTML page or screenshot published.

## Controls
The test uses Python standard library only, accesses local checked-out files and makes no outbound requests. It does not disclose private repository content. A failure blocks the audit workflow until sitemap targets are repaired.

## Entitlements
Static GitHub Pages site and Python validation require no ServiceNow licence. ServiceNow runtime capabilities discussed elsewhere in the portfolio remain subject to App Engine, ITSM/ITOM, IntegrationHub, Performance Analytics, AI and external-provider entitlements as applicable.

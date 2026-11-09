# 2026-11-09 — External-link opener isolation audit

## Client pain and history
Public case studies link to external source evidence. Links opening new tabs without opener isolation can create an unnecessary browser trust boundary.

## Solution delivered
- Added `external-tab-opener` finding for HTTP(S) and protocol-relative links with `target="_blank"` lacking both `noopener` and `noreferrer`.
- Added regression fixtures for unsafe and safe new-tab links.
- Preserved reporting-only behaviour: findings are surfaced but not yet release-blocking.

## Evidence and verification
- SOURCE-ONLY: code and regression fixtures committed.
- CI-VERIFIED: pending successful GitHub Actions run for these commits.
- DEV-VERIFIED: no new instance testing.
- MOCK-ONLY: no new mock demonstrations.
- PRODUCTION-VERIFIED: none claimed.
- No screenshots, customer records, credentials or private repository content published.

## Follow-up
Review CI results and existing external links; add `rel="noopener noreferrer"` where required. Continue evidence approval separately.

## Licensing
Static audit and portfolio need no ServiceNow licence. Runtime Workbench custom applications may require App Engine entitlements; ITSM, ITOM, IntegrationHub, Performance Analytics and AI features depend on subscribed products and usage.

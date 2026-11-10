# Portfolio review guide — release record (2026-11-11)

## Scope
- New `portfolio-review-guide.html`: accessible, responsive 90-second review path linking two existing workbench case studies, the cross-workbench handoff, evidence registers and source-backed technical documents.
- Sitemap registration and homepage "Start here" navigation entry.

## Provenance and claim boundaries
- Source references: `Diagnostic-Workbench2/docs/portfolio/diagnostic-evidence-journey.html` and `solution-lifecycle-studio/docs/portfolio/delivery-workbench-verification-ledger.html`, plus existing public portfolio pages.
- SOURCE-ONLY: this page and its supporting source references are committed; no new runtime functionality was deployed.
- DEV-VERIFIED: historical, version-specific records may be linked; this release did not retest a ServiceNow instance.
- MOCK-ONLY: illustrative workflows remain conceptual, not proof of provider integrations.
- PRODUCTION-VERIFIED: not established.
- No genuine instance screenshots added; screenshot review, redaction and approval remain prerequisites for publication.

## Release assurance
- GitHub commits: `42b09045bfc366852195259f1a4bfb565b20e2ac` (page), `b96f3f554684764e965f66f409c6d1bb268e7f48` (sitemap), `678f8d43b4a23a975c0cd47c4aad6ae81b6673d6` (navigation).
- GitHub write operations succeeded; browser deployment, responsive screenshots and CI execution are not independently verified in this record.
- No repository visibility changes or private artefacts published.

## Entitlements
- Static site: no ServiceNow licence.
- Runtime: custom application/App Engine, ITSM/ITOM and other product entitlements, IntegrationHub, Performance Analytics, AI and third-party provider allowances depend on actual deployed scope and customer contract.

## Next checks
1. Verify GitHub Pages deployment and CI status.
2. Test keyboard/mobile navigation and local-link validator.
3. Review actual screenshots privately for provenance, identifiers, secrets and publication approval before adding a gallery.

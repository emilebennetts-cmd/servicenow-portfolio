# Portfolio site audit CI — 2026-11-09

## Change
Added `.github/workflows/portfolio-audit.yml` to execute the existing standard-library HTML audit on pushes to main, pull requests and manual dispatch. The workflow validates Python syntax, produces JSON findings, writes a concise Actions job summary and retains the JSON report for 30 days.

## Evidence and verification
- **SOURCE-ONLY:** Workflow YAML committed to the public portfolio repository; audit script previously present at `tests/audit_public_site.py`.
- **CI-VERIFIED:** Not claimed. A successful Actions execution and inspection of its report are required.
- **MOCK-ONLY:** Illustrative screens elsewhere on the site remain illustrative.
- **DEV-VERIFIED:** No new ServiceNow runtime validation.
- **PRODUCTION-VERIFIED:** No new ServiceNow runtime validation.

## Publication and release controls
No screenshots, private repository contents, customer records or credentials are included. The audit is initially nonblocking to avoid incorrectly asserting that legacy pages already satisfy every rule. Review JSON findings and remediate defects before changing the workflow to a strict release gate.

## Follow-up
1. Inspect the first workflow run and its JSON artifact.
2. Prioritise missing targets, accessibility issues and private-reference findings.
3. Enable strict mode only after the existing site passes the audit.
4. Separately validate GitHub Pages deployment, mobile rendering and approved screenshot provenance.

## Entitlements
Static GitHub Pages and this Python audit do not require ServiceNow licences. Deployment and execution of the underlying Workbenches require appropriate ServiceNow instance access and custom application entitlements; IntegrationHub, ITSM, ITOM, Performance Analytics and AI features require feature-specific assessment.

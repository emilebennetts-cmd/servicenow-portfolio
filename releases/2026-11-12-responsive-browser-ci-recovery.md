# Responsive Chromium verification recovery — 12 November 2026

## 1. The client's pain and history
The CMDB Diagnostic Trust Lab and both Workbench architecture case studies had static tests and a published GitHub Pages deployment, but their expanded responsive browser workflow **failed before running any browser assertions**. GitHub Actions run [43048806716](https://github.com/emilebennetts-cmd/servicenow-portfolio/actions/runs/43048806716) failed on Ubuntu package mirror DNS resolution during Playwright's optional `--with-deps` font installation. This was a CI bootstrap failure, **not** evidence of application behaviour passing or failing.

## 2. The ServiceNow portfolio solution
- Changed `.github/workflows/portfolio-responsive-smoke.yml` from `playwright install --with-deps chromium` to `playwright install chromium --only-shell`. GitHub's `ubuntu-latest` image already supplied the required browser runtime libraries for this successful run, so the unnecessary apt/font-download dependency was avoided.
- Added `scripts/test_browser_smoke_bootstrap.py` to the repository-wide standard-library CI suite. It checks the pinned Playwright version, shell-only bootstrap, prohibition on apt-based install commands, retention of actual Playwright cases and absence of screenshot-capture calls in the smoke harness.
- Reran the actual Chromium workflow. [Run 43057361014](https://github.com/emilebennetts-cmd/servicenow-portfolio/actions/runs/43057361014) **PASSED**, including all five synthetic CMDB scenarios and provenance/navigation checks across 390px, 768px, 1024px and 1440px (20 viewport/page combinations). This receipt is tied to the workflow-fix commit `75bf7915d01e9316ebf781d48079b5c135cf6e4e`. Subsequent commits must be evaluated against their own workflow runs.
- No ServiceNow credentials, customer data, private repository paths or held screenshot bytes were added to public assets.

## 3. Architectural best practices and acceptance boundary
**SOURCE-ONLY:** GitHub workflow and regression-test implementation. **BROWSER-VERIFIED:** Static public HTML runs locally in Chromium at four viewport widths, with deterministic synthetic fixtures. This is a web-QA receipt, **not a ServiceNow DEV receipt**. **MOCK-ONLY:** All values in the CMDB Diagnostic Trust Lab. **DEV-VERIFIED:** No new ServiceNow instance execution performed. **PRODUCTION-VERIFIED:** Not established. Original screenshot candidates remain **HOLD** until provenance, irreversible redaction and written publication approval.

### Follow-up release checks
1. Confirm standard-library tests and quality audit against the final source commit.
2. Confirm GitHub Pages deployment for the final release commit; do not conflate deployment with ServiceNow testing.
3. Retain provenance/version reconciliation privately rather than presenting a document's uncorroborated instance assertion as independently verified runtime evidence.

### Licensing and entitlements
The public static website, deterministic fixtures and Playwright verification require **no ServiceNow licence**. Runtime custom ServiceNow apps and evidence collectors require authorised ACLs/roles and review of App Engine, CMDB/ITOM, ITSM, IntegrationHub, analytics/AI, third-party connectors and knowledge licences as applicable.

### Rollback
Revert the workflow-install adjustment and its standard-library regression test if the runner contract changes. Avoid returning to `--with-deps` until repository/mirror availability is demonstrably reliable.

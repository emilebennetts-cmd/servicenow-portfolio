# 16 November 2026 — CMDB Health: denominator and rule-drift review

## 1. The client's pain & history
In a fictional multi-source CMDB, an apparently improving health headline can be caused by a smaller evaluated CI population, a revised metric rule or an incomplete scheduled run. The failure is not a low percentage; it is missing provenance for the percentage. This improvement extends the existing four-investigation CMDB Health lab rather than introducing another duplicated case-study page.

## 2. The ServiceNow solution
- Implemented a responsive synthetic before/after inspection directly inside [CMDB Health KPI Assurance Lab](../cmdb-health-assurance-lab.html#denominator-lab).
- Four distinct read-only examples: genuinely comparable **synthetic inputs** (700/1,000 to 820/1,000, +12.0 pp), excluded 200 synthetic CIs (700/1,000 to 700/800, +17.5 pp), changed rule revision (700/1,000 to 850/1,000, +15.0 pp) and incomplete second calculation.
- A deterministic browser-local model checks sample counts, denominator, cohort identity token, rule version, completed run and chronologically ordered timestamps. When any signal differs, it explicitly reports **NOT COMPARABLE / NATIVE HOLD**.
- Accessible case selector, textual results, two mobile-stacking comparative bars, reason list, a four-case offline CSV export and distinct labels separating example arithmetic from actual ServiceNow health algorithms.
- Preserved the original **24 native acceptance gates** untouched, fixed to **NOT RUN / HOLD / MOCK-ONLY**, with execution evidence fields blank.
- New Node tests cover all fixture verdicts, positive-looking but invalid trends, missing job receipts, download integrity and DOM provenance labels. CI workflow includes the new test.

**Important arithmetic boundary:** These values are fictional pass-count ratios, **not** native CMDB Health scores, and equality of synthetic cohort tokens is not a native CI membership verification. This visual does not fetch or submit any data.

## 3. Architectural best practices and acceptance
- Start with native CMDB Health metric definitions, scheduled job run evidence, CI class eligibility, actual population membership and source ownership. Use IRE and field/reconciliation rules rather than ad hoc changes or recalculating native scores in a custom app.
- Pin effective class/service filters, stable CI membership, metric rule revision, scheduled job completion and timestamps before comparing native results.
- Recompute only through authorised non-production execution; deny negative-persona modifications; independently review findings before any release decision.
- Never promote synthetic or repository-read evidence into DEV-VERIFIED or PRODUCTION-VERIFIED.

| Claim | Classification / outcome |
| --- | --- |
| Committed HTML, JS, test and CI source | SOURCE-ONLY |
| Four diagrams, before/after figures and CSV | MOCK-ONLY |
| Source repositories' past PDI observations | DEV-REPORTED, historical only |
| New CMDB Health DEV native execution | 0/24, NOT RUN / HOLD |
| New production native execution | 0/24, NOT RUN / HOLD |
| Original ServiceNow screenshot publication | 0 approved / HOLD |
| Public/private repository visibility changes | None |

## Source boundaries
- Delivery repository `emilebennetts-cmd/solution-lifecycle-studio` README currently declares 4.22.2 source while separately preserving an older, date-bound DEV release.
- Diagnostic repository `emilebennetts-cmd/Diagnostic-Workbench2` README describes a scoped application and KI companion; not a source of new CMDB Health runtime findings.
- Controlled Drive file `01-Universal-Delivery-Workbench-Solution-As-Built.pdf` is a 30 September 2026 unapproved draft with source 4.6.1 and historical DEV 4.5.1; no screenshots, private identifiers or source reproduced.
- ServiceNow documentation: [CMDB Health overview](https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/overview-cmdb-health.html), [Health job configuration](https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/t_EnableCMDBHealthDashboardJob.html).

## Implementation receipts
- Deterministic model: [commit 14d59b3](https://github.com/emilebennetts-cmd/servicenow-portfolio/commit/14d59b3216486dbfdade925937b5fe0068943d42).
- Responsive interactive section: [commit af8bc56](https://github.com/emilebennetts-cmd/servicenow-portfolio/commit/af8bc568765f346bf0a753cec35e01d4e5eeaacb).
- Regression tests: [commit 75eff88](https://github.com/emilebennetts-cmd/servicenow-portfolio/commit/75eff882875a8af1949648c064072784a4eca7c6).
- Quality workflow enforcement: [commit c5f04a3](https://github.com/emilebennetts-cmd/servicenow-portfolio/commit/c5f04a35c472468781b3bdadc7e358889bb6770d).
- Final CI, Pages and external HTTP verification are recorded separately and must not be assumed from source commits alone.

## Licensing / entitlement dependencies
Public HTML, local computation and CSV download need no ServiceNow licence or API token. Real native assurance requires licensed/activated CMDB Health capabilities, correct admin or `sn_cmdb_admin` roles for jobs, and authorised CI access. Discovery and ITOM Visibility, Service Graph Connectors, CMDB 360, IntegrationHub, ATF, Performance Analytics and AI capabilities may require additional licensing or subscription-specific rights depending on usage. Validate entitlements on the target instance before selecting an implementation path.

## Blockers
No authenticated current DEV read-back, no actual 24-gate execution, no independent reviewer sign-off, no production acceptance and no screenshot publication approval. No production writes or private repository publication were performed.

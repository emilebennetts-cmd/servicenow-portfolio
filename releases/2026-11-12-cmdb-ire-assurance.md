# CMDB / IRE assurance evidence release — 12 November 2026

## Change delivered
- Published `cmdb-ire-assurance.html`, a customer-neutral, source-reviewed technical deep dive for CMDB Inventory, IRE configuration, duplicate indicators, relationship quality and server lifecycle.
- Added discovery links in the homepage's Workbench directory and the Diagnostic case-study header; registered the page in `sitemap.xml`.
- Added `scripts/test_cmdb_assurance_contract.py`: semantic/mobile baseline, local-link and fragment checks, four evidence classes, collector coverage and prohibited-media/private-link assertions.
- The schematic is **MOCK-ONLY**, not a captured user interface. No screenshot candidate was released.

## Material source-review findings
1. Source-described read-only collectors can still emit grouped display values, including CI names and hardware serial numbers. An aggregate-only posture or a metadata flag is not sufficient to approve export.
2. Group enumeration has a finite cap; duplicate-population metrics can be partial rather than exact.
3. Unavailable tables can propagate missing/zero values into computed metrics, requiring a NOT ASSESSED / PARTIAL state rather than a healthy score.
4. Parent-empty and child-empty relationship counts can overlap; source implementation does not by itself establish duplicate-edge or self-reference detection.

These are design/assurance observations from authorised source inspection, not production defects demonstrated against a customer instance. Public text is a sanitised architectural assessment; no private source code, internal links, instance identity, customer record or raw screenshot was copied.

## Status and acceptance
| Gate | State |
|---|---|
| SOURCE-ONLY | Public HTML, navigation, sitemap and test code committed |
| DEV-VERIFIED | No new direct DEV run; historical unrelated receipts are not inherited |
| MOCK-ONLY | Flow illustration only |
| PRODUCTION-VERIFIED | Not established |
| Publication permission for genuine images | HOLD, unchanged |
| Browser rendering / GitHub Pages deploy | Must be observed separately, not inferred from commit |

The page describes a proposed acceptance suite; these acceptance checks are **not executed**. Read-only scripts are not run and no CI data is exported.

## ServiceNow licence / entitlement boundary
The static website requires no ServiceNow licence. Live execution needs authorised platform roles and access. CMDB/IRE, CMDB Health, ITOM Visibility/Discovery, Service Graph connectors, custom App Engine tables, and optional IntegrationHub/automation entitlements must be checked against the target customer's subscriptions and release before deployment. No licensing rights are implied by this case study.

## Reversion
Revert the new page, its test, navigation updates and sitemap entry by commit as ordinary static website changes. No ServiceNow configuration or data was changed.

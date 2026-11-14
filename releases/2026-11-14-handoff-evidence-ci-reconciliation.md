# Handoff evidence register reconciliation and failed quality-gate recovery — 14 November 2026

**Public case study:** [Diagnostic-to-Delivery Handoff Contract](../diagnostic-delivery-handoff-contract.html)  
**Evidence position:** SOURCE-ONLY architecture, MOCK-ONLY browser controls; no native DEV/Production verification or customer instance access.  
**Publication:** zero genuine screenshots approved; HOLD; no private repository source or external credentials published.

## 1. The client's pain and history

The previous handoff case-study release was source-backed, accessible and independently browser-tested. However the page was indexed in the public Portfolio Explorer **before its corresponding evidence claim was registered**. The Explorer correctly annotated it SOURCE-ONLY in markup, while the authoritative public verification register had no matching record. Both cross-register quality gates therefore failed. A successful GitHub Pages deployment alone was insufficient to assert a healthy release.

**Observed failure on previous head `ff56227b50e1cfb6e413b54745c3037cd089169f`:**
- [Portfolio quality gate — failed](https://github.com/emilebennetts-cmd/servicenow-portfolio/actions/runs/43556411908): `test_every_indexed_page_has_a_reviewed_claim` and `test_generator_matches_live_catalogue`.
- [Publication audit — failed](https://github.com/emilebennetts-cmd/servicenow-portfolio/actions/runs/43556411793): `reconcile_explorer_evidence.py --check`, reporting `diagnostic-delivery-handoff-contract.html` unregistered.
- [Handoff browser checks — passed](https://github.com/emilebennetts-cmd/servicenow-portfolio/actions/runs/43556411876).
- [GitHub Pages deployment — succeeded](https://github.com/emilebennetts-cmd/servicenow-portfolio/actions/runs/43556412152).

## 2. ServiceNow solution evidence repair — implemented

- Registered `DIAGNOSTIC-DELIVERY-HANDOFF-CONTRACT-SOURCE-20261114` in the canonical public verification register, with a single page mapping and explicit SOURCE-ONLY/MOCK-ONLY boundaries.
- Kept the already correct Explorer badge; the deterministic generator will now compute its SOURCE-ONLY status directly from the register rather than producing `NOT REGISTERED`.
- Added a regression test requiring exactly one matching claim, conservative runtime wording, native NOT RUN state and screenshot HOLD.
- Preserved the separation between Diagnostic operational evidence ownership and Delivery's reference-only reviewed handoff; no live cross-app data flow is asserted.
- Did not amend original controlled As-Built, User Guides, training, or any native ServiceNow packages. No repository visibility or screenshot approval state changes.

## 3. Architectural best practices and verification

One public evidence register remains authoritative for website classifications; a new page is not release-ready unless it has a registered, validated claim. Browser tests and Pages deployment establish website behaviour, **not** target ServiceNow installation or execution. Historical DEV-reported read-backs remain version- and scope-bound.

**Expected source gate commands:**
```bash
python scripts/check_verification_register.py
python scripts/reconcile_explorer_evidence.py --check
python -m unittest discover -s scripts -p 'test_reconcile_explorer_evidence.py' -v
```
Final GitHub Actions conclusions must be inspected for the exact commit before this repair is called green.

**Entitlements:** Public HTML, evidence JSON and CI require no ServiceNow licence. Native scoped application deployment requires applicable App Engine/custom-table rights and ACL/role coverage. ITSM, ITOM/Discovery, IntegrationHub/spokes, ATF, Performance Analytics, AI and third-party provider subscriptions depend on the implementation and actual customer contract.

**Blockers remain:** independent DEV acceptance with source SHA, target app/scope/version, dated executed tests, reviewer identity and private receipts; separate production/change authority; image-by-image irreversible redaction and express publication permission. **No DEV-VERIFIED / PRODUCTION-VERIFIED promotion.**

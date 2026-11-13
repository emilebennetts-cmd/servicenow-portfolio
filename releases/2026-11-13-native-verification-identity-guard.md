# Native verified-claim metadata guard — 13 November 2026

**Release type:** SOURCE-ONLY website/publication control  
**Scope:** public evidence-register validator, negative regression tests, acceptance playbook, reviewer field guide  
**Native Workbench execution:** NOT PERFORMED · **Screenshot publication:** HOLD (0 approved)

## 1. The client's pain & history

With all 71 Explorer entries now classified, the next risk is incorrectly promoting a historical or synthetic statement into **DEV-VERIFIED** or **PRODUCTION-VERIFIED**. Previously, the register validator required dates, HTTPS evidence references and production authorisation, but it did not require the tested source revision, installed version, application scope, target environment or executed test set. An unrelated old receipt could therefore be described using a stronger classification without identifying the version mismatch.

## 2. The ServiceNow solution

Expanded `scripts/check_verification_register.py` to require complete, safe metadata before either native verified label can appear. Every such future claim must include a full 40/64-character lowercase source SHA, installed app version, scoped-app identifier, DEV-versus-PROD environment, anonymised environment alias, unique executed test IDs, sanitised private receipt alias and an independent-review approval flag. Existing date, HTTPS and production-authorisation controls remain.

Added four additional regression tests with a complete synthetic example and failure cases for absent build identity, wrong environment, unsafe aliases, duplicate test IDs, short SHAs and absent production authorisation. Wrote a reviewer-facing field guide at `evidence/native-verification-claim-contract.md` and linked it from `workbench-acceptance-playbook.html#promotion-contract`.

All **79 existing public claims** retain their existing evidence class: this is a fail-closed future publication boundary, **not** proof that the named metadata, reviewer or ServiceNow execution actually exists. A Boolean approval marker is a declared value and still requires independent validation of the private receipt.

## 3. Architectural best practices

Prefer OOTB platform app/version/scope read-back, ACL and role checks, sanctioned ATF/UAT records, explicit rollout/change authority and immutable source traceability. An installer screen or a pretty mock is not an acceptance record. Never include instance URLs, customer identifiers, full screenshots or secrets in the public manifest; keep supporting evidence in the restricted control system.

The controlled Drive Delivery As-Built/Architecture/Training filenames and Diagnostic fictional runbook were located; repository readme/source boundaries remain separated. Historical Delivery source/DEV baselines and current source declarations are **not interchangeable**. No source application deployment was attempted.

### Local/CI checks

- `python scripts/check_verification_register.py`
- `python -m unittest scripts/test_verification_register.py`
- Repository Portfolio quality gate / publication audit / local-link integrity workflows

See GitHub Actions for final commit statuses; a successful repository commit is not in itself external website availability or native runtime verification.

## Licensing and entitlement boundary

Static GitHub Pages and Python validation: **none**. Native testing depends on approved instance roles and ACLs, applicable App Engine/custom-table licensing, available ATF functionality, and contracted ITSM, CMDB/ITOM Discovery, Service Graph, IntegrationHub/spokes, analytics/AI and external-provider rights per target application.

## Unresolved acceptance

- Native DEV/UAT read-back against exact source and app version: **NOT RUN**
- Independent observed production execution and release authorisation: **NOT ESTABLISHED**
- Screenshot provenance, permanent sanitisation and publication approval: **HOLD — zero original images approved**
- Custom non-GitHub domain: not configured; requires a domain and DNS authorisation

**No changes were made to the visibility of any source or private repository.**

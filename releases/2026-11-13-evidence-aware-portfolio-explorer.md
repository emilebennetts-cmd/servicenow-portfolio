# Evidence-aware Portfolio Explorer — 13 November 2026

## 1. Client pain and history
The growing 71-entry public directory listed pages by topic alone, even though its public verification ledger held 27 separately classified claims. A reviewer could not distinguish an illustrative lab from a source-supported implementation or historical DEV report without opening multiple pages. Page-level inference could also accidentally overstate validation.

## 2. Implemented solution
The Portfolio Explorer now exposes a second filter, **Registered evidence**, alongside keyword and topic filtering. Every result displays a badge derived deterministically from the PUBLIC `evidence/public-verification-register.json`. It shows SOURCE-ONLY, MOCK-ONLY, DEV-REPORTED, MIXED CLAIMS or NOT REGISTERED. Mixed statuses are never elevated to a single verified status; unregistered pages never receive a made-up verification claim.

The browser remains strictly offline: no fetch(), local storage, connections, credentials or image assets. Result badges are compiled into static HTML. Reset clears all three filters. The source-controlled generator supports `--write` and `--check`, with a fail-closed drift check in BOTH publication workflows, offline negative-case tests and mobile Chromium interaction tests.

The public register gains the source-only PORTFOLIO-EXPLORER-PROOF-FILTER claim. Its own page is omitted from the directory by design.

## 3. Architecture and assurance
Source baselines reviewed: Delivery source repository, Diagnostic source repository, 30 September controlled Delivery As-Built (source 4.6.1 distinct from historical DEV 4.5.1), Delivery training guide and Diagnostic completion runbook. No restricted content, client information, original screenshot or private source was copied to the public HTML. Existing eight screenshot observations remain under publication HOLD.

**Classification:** SOURCE-ONLY website implementation; existing MOCK-ONLY browser demonstrations and historical DEV-REPORTED statements retain their original boundaries. This release does not establish DEV-VERIFIED or PRODUCTION-VERIFIED Workbench functionality, user UAT or real integration.

**Licensing:** No ServiceNow licence for this public static feature. Native Workbench replication requires validated App Engine/custom table entitlements, roles and ACLs; ITSM, CMDB/ITOM Discovery, IntegrationHub, analytics, AI or external-provider rights depend on enabled scope and target contract.

**Open:** Independently test current target application/version, approve screenshots individually after permanent sanitisation and rights checks, and verify public HTTP reachability separately from a successful Pages workflow.

## Verification
Run `python scripts/reconcile_explorer_evidence.py --check`, `python -m unittest discover -s scripts -p 'test_*.py'`, `python scripts/check_publication.py` and responsive Chromium checks. GitHub CI result should be checked against the committed SHA, not inferred from source success.

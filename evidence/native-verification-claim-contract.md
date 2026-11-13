# Native ServiceNow verification: version-pinned claim contract

**Release:** 13 November 2026  
**Evidence class:** SOURCE-ONLY publication-policy code and tests  
**Status:** PREPARATION / HOLD. No native ServiceNow execution was performed to create this document.

## 1. The client's pain and history

A source-based portfolio can easily accumulate attractive statements such as “works in DEV,” while the accompanying test receipt belongs to an earlier installed version, different application scope or one isolated route. A browser demonstration is sometimes incorrectly treated as platform acceptance. Without immutable identifiers, the same evidence can accidentally be reused to certify a later implementation.

The public verification register currently describes historical observations and synthetic browser labs but does not contain any independently established DEV-VERIFIED or PRODUCTION-VERIFIED Workbench claim.

## 2. The ServiceNow solution: a fail-closed promotion contract

The public register validator now refuses the **DEV-verified** and **production-verified** classifications unless the claimed record includes the following *non-sensitive metadata*. The fields are **necessary but never sufficient** for verification.

| Field | Requirement | Reason |
| --- | --- | --- |
| `verification_date` | Actual ISO date, not in the future | Anchors the observation |
| `verification_reference` | HTTPS reference, no URL-embedded credentials | Points to evidence reviewed separately |
| `source_commit_sha` | Full 40- or 64-character lowercase Git SHA | Binds source lineage |
| `installed_version` | Explicit version label | Prevents implicit promotion between releases |
| `application_scope` | Valid scoped-app ID or `global` | Binds platform application identity |
| `execution_environment` | `DEV` for DEV-verified, `PROD` for production-verified | Prevents environment confusion |
| `environment_alias` | Uppercase alphanumeric alias, hyphen/underscore permitted | Avoids publishing instance URLs |
| `executed_test_ids` | Unique, nonempty, constrained list | Requires an identifiable test set |
| `evidence_receipt_alias` | Sanitised reference only; no paths or URLs | Keeps private receipts private |
| `independent_review_approved` | Boolean true | Records claimed independent approval, not proof of it |
| `production_authorisation` | Required in addition for production | Separates production change authority |

The CI validator confirms only the **shape of the public claim**. It cannot inspect ServiceNow, confirm that a reviewer signed anything, determine whether a private receipt is authentic, or authorise a screenshot. Approval remains a separate human-controlled release gate.

### Minimum private evidence bundle

Retain the actual redacted ServiceNow app/version/scope read-back, executed test steps and expected/actual results, actor role and ACL denial checks, timestamp, supporting defect records, immutable source reference, independent reviewer sign-off and any production change authority **only in an approved private evidence system**. Keep aliases, not private URLs, in public JSON.

A new source commit or installed version requires explicit impact review and appropriate retesting; it does not inherit the earlier version's DEV acceptance. Historical 4.6.1 / 4.5.1 documentation and later 4.22.2 source materials are not interchangeable test baselines.

## 3. Architectural best practices

- Prefer OOTB **sys_scope**, installed application metadata, update-set/application deployment records, ACL/role read-back, IRE/CMDB Health diagnostics and native ATF/UAT acceptance where applicable.
- Test positive and negative paths, particularly least-privilege failure, idempotent reruns, blocked releases, rollback and source identification.
- Never infer installed native behaviour from a static website, a synthetic simulator, or an archived update-set screen labelled Complete.
- Publish original ServiceNow screenshots **only** after ownership, permanent sanitisation and individual approval have been verified. The publication status remains HOLD, with zero originals approved.
- Do not place customer names, environment hostnames, sys_ids, access tokens, credentials or private evidence URLs in the public repository.

### Regression protection

`python -m unittest scripts/test_verification_register.py` exercises complete synthetic metadata, missing fields, wrong DEV/PROD environment, invalid receipt aliases, duplicate test identifiers, shortened Git SHAs, missing production authorisation and existing register validation. The repository's quality gate also runs the primary register validator.

## Licensing and entitlements

The public portfolio, metadata validator and documentation do **not** require a ServiceNow licence. Reproducing native test results depends on approved instance access and roles, App Engine/custom-table rights when applicable, native ATF entitlement/availability, and separately contracted ITSM, ITOM/Discovery, Service Graph, IntegrationHub/spokes, analytics/AI and third-party connector rights according to the capability under test. Never assume an entitlement from a public screenshot or repository.

**Authoritative public classification for this release:** SOURCE-ONLY. No new DEV-VERIFIED or PRODUCTION-VERIFIED claim or screenshot publication was created.

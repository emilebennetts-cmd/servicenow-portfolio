# Native candidate-byte preflight — public architecture release (15 November 2026)

**SOURCE-ONLY tooling, MOCK-ONLY tests; DEV and Production acceptance HOLD.**

## 1. Client pain and history
The existing offline source-to-target gate checked two equal SHA-256 values provided by an operator. Equal text is not independently verified package bytes. It also needed to reject unexpected receipt fields that could be used to smuggle unsupported claims or misplaced confidential values. This is a preventive data-integrity improvement, not evidence of a disclosed secret.

## 2. The ServiceNow solution
Implemented **optional local candidate-file verification** inside the private preflight: stream the local candidate file, calculate SHA-256, compare against both expected and observed declarations, reject missing/unreadable files and mismatches, refuse symlink inputs. Added strict allowlists for all receipt sections, generic non-echoing errors, version bounds and a test-matrix size limit.

The source-to-target architecture case study now clearly differentiates self-declared hash agreement from actual local byte verification. No network/API connection, installation, change, source-package publication or screenshot upload was made.

## 3. Architecture, verification and licensing
- Private regression: **26/26 synthetic tests passed** on code commit `edd7a25ce704235f97910407e1ce2171d11654bb`, [GitHub Actions run 43714117768](https://github.com/emilebennetts-cmd/servicenow-portfolio-control/actions/runs/43714117768).
- Even when the local bytes match, the maximum result is REVIEW_REQUIRED. Native DEV functionality, installed package identity, source authenticity, roles/ACLs and licensed entitlements are NOT independently established.
- Evidence: SOURCE-ONLY code and architectural narrative; MOCK-ONLY synthetic tests; DEV-REPORTED historical observations; newly DEV-VERIFIED **0** and PRODUCTION-VERIFIED **0**.
- Genuine original screenshot publication: **0 approved — HOLD**. No private file, customer identifier, instance URL, token, screenshot or private source material published.
- No ServiceNow licence required for static website/offline Python; target native implementation needs relevant App Engine/custom-app/table rights, ITSM/ITOM subscriptions as applicable, authorised roles and ACLs, plus separate IntegrationHub, ATF, Now Assist/AI, analytics and other connector entitlements.

## Current blockers
Authenticated and authorised DEV target read-back, actual source/installed app scope alignment, native positive and negative-persona acceptance, customer entitlement confirmation and screenshot-by-screenshot review/approval.

Referenced privately (not reproduced publicly): Delivery and Diagnostic source repositories and connected Google Drive Universal Delivery Workbench As-Built/Architecture and Diagnostic runbooks. Public [source-to-target case study](../source-target-compatibility.html#native-preflight).

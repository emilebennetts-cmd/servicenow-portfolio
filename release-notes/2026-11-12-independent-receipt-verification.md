# Independent redacted-image receipt verification — 12 November 2026

**Classification:** SOURCE-ONLY application implementation. **Screenshot publication:** HOLD. **Runtime:** no new ServiceNow DEV or production execution.

## 1. The client's pain and history
The prior browser-local Redaction Desk could generate a flattened PNG and a SHA-256 JSON receipt, but reviewers still needed a separate, reliable way to compare the downloaded PNG with the recorded digest. Relying on a displayed hash or matching filenames is unsafe, especially when the PNG is transferred, renamed or regenerated.

## 2. The solution implemented
Added [Screenshot Evidence Receipt Verifier](../screenshot-receipt-verifier.html), a self-contained, static, responsive HTML/JavaScript tool. It accepts an exported PNG and v1 receipt, bounds input size (PNG 64 MB; JSON 64 KB), checks PNG signature, IHDR dimensions, internal chunk bounds, IDAT/IEND presence and unwanted tEXt/iTXt/zTXt/eXIf chunks. It validates the receipt's exact schema, redaction count, timestamp, dimensions, evidence class and mandatory HOLD/no-approval/no-DEV/no-production fields. It computes **SHA-256 from the selected PNG bytes** and rejects a mismatch. Changing either file invalidates the previous result, including an in-flight check.

All processing occurs in the browser. A restrictive Content Security Policy blocks connect and forms; no script dependency, image upload, persistence, telemetry or private GitHub assets are used. Linked from the homepage, redaction desk and held-image inventory, and included in the sitemap.

## 3. Architectural best practices, trust boundary and testing
- The matched digest proves byte correspondence to this *user-provided receipt*. It does **not** authenticate the receipt's issuer, prove a safe redaction, establish ServiceNow execution, or grant publication rights. Any person able to modify both files can create another matching pair.
- The PNG parser inspects basic structure and metadata markers; it does not fully decode or validate all image content/CRC. **Separate full-resolution human inspection is mandatory.**
- Static scripts/test_screenshot_receipt_verifier.py covers privacy rules, semantic structure, controls and site links. The Chromium smoke script uses a **MOCK-ONLY synthetic PNG**, generates a valid receipt, and asserts positive match, tampered hash rejection, unsafe approval rejection and dimension mismatch at 390/768/1024/1440 px. No real images are consumed by tests.
- Updated the existing redaction desk test to reflect its actual asynchronous toBlob callback (async function). This is test-contract alignment, not a change to the redaction algorithm.
- **SOURCE-ONLY:** HTML/JS implementation and automated test source.
- **MOCK-ONLY:** synthetic browser PNG fixture.
- **DEV-VERIFIED:** no new platform read-back; historical, version-scoped records remain distinct.
- **PRODUCTION-VERIFIED:** not established.
- **Visual evidence:** all real screenshot candidates remain HOLD until redaction, individual owner/rights approval, safe caption and source provenance are reviewed.

## Release verification and rollback
GitHub Actions (quality gate, audit, Chromium, Pages) must be checked against the final branch head before declaring this release deployed or browser-verified. Rollback: revert the public verifier, navigation, regression and release-log commits; original screenshots remain untouched and in private storage.

## Licensing and entitlements
Static website, Web Crypto and browser testing require **no ServiceNow licence**. Real Delivery/Diagnostic Workbench executions need instance-level ACL/roles and contract-specific custom app/App Engine entitlements; ITSM, ITOM/CMDB/Discovery, IntegrationHub, analytics, AI, content and external-provider licences only where relevant. Publishing images additionally requires rights and explicit approval, independent of ServiceNow licensing.

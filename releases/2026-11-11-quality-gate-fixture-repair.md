# Quality gate repair — 2026-11-11

## Observed failure
GitHub Actions run 42930390880 failed during `Test quality gate`: `test_allowlisted_image_is_accepted` wrote literal `b"fake"` to a PNG filename, contradicting the newly enforced image-signature rule. The failure was in a stale test fixture, not evidence that a genuine screenshot was approved.

## Change
Replaced only the positive approval fixture with a synthetic minimal PNG byte sequence and recalculated its SHA-256 from those bytes. The rejection tests retain deliberately invalid content. The image is a test fixture, not a Workbench screenshot and is not published in `assets/screenshots/`.

## Verification and classification
- **SOURCE-ONLY:** GitHub commit `1b9c4bf9acd8253440bec6b32b982576ed7da985` contains the regression-fixture repair.
- **CI:** prior run 42930390880 failed; rerun status must be checked before asserting success.
- **DEV-VERIFIED:** no new ServiceNow instance verification.
- **MOCK-ONLY:** the synthetic PNG fixture is not runtime evidence.
- **PRODUCTION-VERIFIED:** none established.

## Publication boundary
No screenshots, customer data, private source, credentials or repository visibility settings changed. Real screenshots still require origin records, sanitisation, checksum approval and human publication authorisation.

## Licensing
The Python CI gate and GitHub Pages website do not require ServiceNow entitlements. Runtime demonstrations may depend on App Engine/custom application licensing, ITSM, ITOM/CMDB, IntegrationHub, Performance Analytics, AI features or third-party subscriptions depending on the exact features used.

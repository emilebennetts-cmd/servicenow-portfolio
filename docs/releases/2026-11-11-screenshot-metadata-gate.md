# Release record — 2026-11-11 — screenshot metadata guardrail

## Change
- Commit `75d978494ba7bcb917143b67429fe6070c489c8b`: detect common embedded PNG text/EXIF, JPEG EXIF/XMP/Photoshop, WebP EXIF/XMP and GIF comments in approved screenshot assets; fail the publication gate on detection.
- Commit `e9bd03370d120245036a012a5ec95dd5e4fab0b6`: add focused regression tests for metadata markers.

## Verification boundary
**SOURCE-ONLY:** GitHub commits persisted. Tests were committed but have not been executed or independently verified in CI in this release. The marker check is deliberately conservative and can produce false positives; it is not a full image parser, metadata scrubber or content review. A clean result does **not** imply rights clearance, sanitisation, DEV verification or production verification.

**DEV-VERIFIED:** No new runtime evidence. **MOCK-ONLY:** Existing illustrative diagrams remain conceptual. **PRODUCTION-VERIFIED:** Not established. No screenshots were approved or published.

## Follow-up
Verify CI execution, check any false-positive reports, and only publish final derivatives after provenance, irreversible redaction and explicit human approval. Do not publish original restricted screenshots or private repository material.

## Entitlements
The static publication gate requires no ServiceNow licence. Workbench demonstrations may depend on App Engine, ITSM, ITOM, IntegrationHub, Performance Analytics, AI or third-party entitlements, subject to contract and actual feature use.

# Local screenshot evidence — SHA-256 export receipt (12 November 2026)

**Classification:** SOURCE-ONLY browser utility; browser QA must be independently confirmed. **Publication state:** HOLD. No real customer screenshot or redacted derivative is published in this release.

## Delivered

The existing [Screenshot Redaction Desk](../screenshot-redaction-desk.html) now produces a separate JSON review receipt **after** exporting a flattened PNG. The receipt cryptographically binds its SHA-256 value to the exact PNG bytes generated in the same operation. It contains the export filename, width, height, number of solid redaction areas, UTC generation time and explicit publication/verification restrictions. The UI displays the digest so the reviewer can independently recompute it against the downloaded PNG.

A source image or mask edit invalidates the previous receipt. A pending export is cancelled if its source token, image object, mask geometry or acknowledgement changes while image conversion or hashing is in progress. Source filename, original pixels, original metadata, unredacted regions and mask coordinates are **not** copied into the receipt.

Both PNG and JSON downloads remain local to the browser. The page does not call ServiceNow, Google Drive, GitHub or another remote endpoint. The utility needs a secure browser context to compute SHA-256 and fails closed rather than exporting an unbound file if hashing is unavailable.

## Review boundaries

- A hash verifies byte identity, **not** successful redaction, confidentiality, authorised publication, visual fidelity or ServiceNow execution.
- The receipt status is **HOLD**, with `publication_approved: false`, `independent_export_review: REQUIRED`, and both DEV and production verification set to false. Approval and source provenance must be recorded independently.
- Screenshots indexed privately remain under the pre-existing image-specific approval gate. **Zero new genuine Workbench screenshots were published.**
- Browser tests use MOCK-ONLY synthetic pixels and embedded source-text metadata to prove redacted pixels are opaque and metadata is absent. They independently check the downloaded receipt's hash against the actual exported PNG bytes at 390, 768, 1024 and 1440 px.
- Static code, privacy contracts and this note are SOURCE-ONLY. Existing historical DEV claims remain scoped to their original source versions; there is no new DEV or production read-back.

## Quality and release boundaries

Static tests and GitHub Actions are the authority for release outcome; check runs against the final source commit before declaring browser verification or successful deployment. Revert the commits adding the receipt UI and tests to roll back without touching any private images.

## Entitlements

This static HTML/Canvas/Web Crypto workflow requires **no ServiceNow licence**. Capturing actual Workbench function in ServiceNow requires appropriate application roles/ACLs and contract-specific App Engine/custom app/table entitlements. ITSM, CMDB/ITOM, IntegrationHub, analytics/AI, external integrations and third-party content rights must be verified when present. Image publication permissions are separate from product licences.

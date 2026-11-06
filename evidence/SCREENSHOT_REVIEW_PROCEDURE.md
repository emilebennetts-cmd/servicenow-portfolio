# Screenshot evidence intake and publication procedure

**Status:** Internal publication procedure; this document is not evidence that any screenshot has been reviewed or approved. Updated 2026-11-07.

## 1. Source intake (private workspace only)
For each candidate from the Universal Delivery Workbench or Diagnostic Workbench, record a private evidence ID, source repository or Drive document, original file name, capture date if known, source owner, target instance/environment, application/version and the exact UI claim the image could support. Never copy original customer screenshots into the public repository. Keep original and redacted files in access-controlled storage. Do not place customer-specific identifiers, instance addresses, email addresses or private Drive URLs in public metadata.

## 2. Verification classification
- **Source-only:** UI or functionality is documented in code or design artefacts, but not independently executed.
- **Mock-only:** Synthetic rendering or illustrative demo; never label as an application screenshot.
- **DEV-reported:** A source document says it ran in DEV, but the portfolio author has not independently reproduced the result.
- **DEV-verified:** Authorised reviewer independently observes the running feature in DEV and records environment, date, steps and outcome.
- **Production-verified:** Authorised reviewer observes an approved production deployment and records change/reference, date and outcome without publishing restricted identifiers.

An image alone proves a rendered UI state, not an integration, transaction, deployment or business outcome.

## 3. Mandatory image review
A reviewer with publication authority must inspect the original and the final redacted derivative at full resolution. Check visible text, tables, browser address bar, breadcrumbs, navigation, tooltips, notifications, usernames, tenant names, customer identifiers, financial amounts, API keys, tokens, email addresses, record sys_ids, QR codes and embedded metadata. Crop or permanently rasterise redactions; do not rely on translucent overlays or CSS masks. Remove EXIF and other metadata. Re-open the exported image to verify redactions are irreversible and the UI remains truthful.

## 4. Public release record
Before adding any image to `evidence/approved-public-images.txt`, retain a private approval record containing: evidence ID, original SHA-256, sanitised SHA-256, reviewer, approval date, permitted public caption, environment classification, and explicit publication authorisation. The public repository may contain only the approved derivative and a caption that does not overclaim. The allowlist is a CI control, **not** proof of consent, legal permission or technical verification.

## 5. Gallery presentation
Use accessible `figure`/`figcaption` elements, descriptive `alt` text, lazy loading, explicit environment labels and links to source-backed case-study claims. Do not publish a gallery with fabricated screenshots merely to fill gaps. Until review completes, retain the existing clearly labelled mock UI and explain that genuine images are pending.

## 6. Release checks
Run `python3 -m unittest discover -s scripts -p 'test_*.py'`, `python3 scripts/check_site.py`, and `python3 scripts/check_publication.py`. Confirm the GitHub Actions run succeeds, then inspect the public Pages URL on mobile and desktop. Check links, captions, contrast, image scaling and that no restricted information is visible. Record the commit, run URL, deployment timestamp and verification result in the release log.

## 7. Entitlements
The public static gallery needs no ServiceNow licence. Reproducing screens in a ServiceNow instance may require scoped-app entitlements, appropriate roles and licensed products such as ITSM, ITOM, ITAM, SecOps, IRM, HRSD or CSM; IntegrationHub spokes, AI and advanced analytics may require additional subscriptions. Verify against the target instance contract before asserting availability.

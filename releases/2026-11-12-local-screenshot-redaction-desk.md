# 12 November 2026 — Local Screenshot Redaction Desk

## Why

The public Workbench gallery contains **held screenshot candidates**, not approved source captures. Existing intake records distinguish UI captures, synthetic workshop demonstrations and architectural documents. Publishing any original is prohibited until rights, provenance, image-specific sanitisation and permission are established. This release adds a practical **owner-side preparation tool**, not a publication shortcut.

## Delivered

- New public-static `screenshot-redaction-desk.html` with **local-only** PNG/JPEG/WebP selection, 15 MiB and 16 megapixel bounds, no image uploads, no network API and no browser persistence.
- Accessible percentage-coordinate rectangle input and pointer/touch solid-redaction drawing; undo and clear revoke prior review acknowledgement.
- Black areas are **painted into an opaque, full-resolution canvas** and re-encoded into a new PNG using `toBlob("image/png")`. Neither the source filename nor its embedded metadata is reused.
- Exports remain disabled without a loaded image, at least one solid area and an explicit manual-inspection acknowledgement.
- A restrictive in-document Content Security Policy (`default-src 'none'; connect-src 'none'`) limits accidental connections. This is defence in depth, not a security audit of the viewer's own browser.
- Linked from the held-source visual evidence gallery and homepage full directory; included in sitemap.
- New standard-library static test for privacy, metadata, publication boundaries, responsive semantics and link destinations.
- New Chromium test uses an **in-memory synthetic red image** with an injected private marker in a PNG `tEXt` chunk. It drives keyboard and pointer masking at 390/768/1024/1440px, downloads to the runner's temporary area and **inspects PNG pixels and metadata** without publishing screenshots or source captures. The test checks that marked pixels are black, unmarked pixels retain expected RGB values and source metadata is absent.

## Verification and classification

- **SOURCE-ONLY:** Public tool HTML/JS, integration, tests and this release note are GitHub changes. Static checks/Chromium and Pages deployment must be evaluated against the actual final commit; a commit alone does not establish a passing run.
- **MOCK-ONLY:** Browser-test fixture is an in-memory, entirely synthetic image. No actual ServiceNow screenshots are used in tests.
- **DEV-VERIFIED:** No new ServiceNow installation, UI access, API read-back or instance execution.
- **PRODUCTION-VERIFIED:** Not established.
- **Visual evidence:** All genuine screenshot candidates remain **HOLD**. The tool never grants publication rights and never pushes images to public GitHub.

## Limitations and acceptance controls

A black rectangle only protects the area covered. No automatic confidential-data detection, facial/brand analysis or OCR is performed. Text may remain in cropped browser chrome, tooltips, watermark layers or other regions. Manually review and reopen the exported PNG, confirm release identity and obtain authorisation for each proposed image *and* caption before committing any pixels. Images too large to decode within the bounds are rejected.

Browser tests cover the utility, not correctness of underlying Workbench implementation. No private repository access or external connector is required for the static page.

## Licensing and entitlement boundary

The static HTML site and client-side image processing require **no ServiceNow licence**. Captured runtime features may require App Engine/custom application entitlements, ServiceNow product licences (e.g. ITSM, CMDB/ITOM/Discovery), IntegrationHub/spoke subscriptions and provider rights. Publication rights are a separate legal and information-security decision.

## Rollback

Remove the new HTML page, its gallery/homepage/sitemap navigation and associated tests/workflow entry. Do not relax the screenshot publication gate or repository privacy.

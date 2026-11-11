# 12 November 2026 — PNG receipt structural validation hardening

**Evidence classification:** SOURCE-ONLY implementation; MOCK-ONLY test images; no new ServiceNow DEV verification and no production verification. All authentic Workbench screenshots remain on **HOLD**.

## 1. The client's pain and history

A matching SHA-256 value only binds a PNG to the supplied receipt. The initial verifier checked the PNG signature, chunk bounds, dimension fields, IDAT/IEND markers and a small set of metadata chunk names, but did not validate per-chunk PNG CRCs, accepted unexpected ancillary chunks and did not enforce strict canvas-export colour modes. A synthetic or corrupted PNG and a newly computed matching receipt could therefore pass preliminary structural checks. This is separate from any unproven claim of image authenticity.

## 2. The solution implemented

- Hardened the **browser-local** [Screenshot Receipt Verifier](../screenshot-receipt-verifier.html) to validate CRC-32 on each PNG chunk, from exact type and payload bytes; reject truncated or tampered chunk contents even when the supplied SHA-256 matches those altered bytes.
- Enforced non-interlaced 8-bit truecolour/truecolour-with-alpha canvas PNG headers, contiguous IDAT chunks, a single initial IHDR and a correctly positioned IEND with no trailing bytes.
- Restricted allowed ancillary chunks to normal non-identifying canvas colour/physical-format headers (`sRGB`, `gAMA`, `cHRM`, `pHYs`) with required lengths. Reject all text/EXIF, unrecognised, palette, profile and post-image ancillary chunks. An unexpected capture must be re-flattened locally; never loosen the public intake gate to accommodate an original.
- Updated on-page explanations and the static contract. Extended Chromium regression testing at 390, 768, 1024 and 1440px with two negative fixtures: IDAT corruption **with a matching freshly forged receipt digest**, and an embedded `tEXt` chunk with a valid CRC **and matching digest**. Both must fail; the unmodified synthetic fixture must still pass.
- Input files stay entirely in the browser. No remote APIs, persistent storage, real customer captures, screenshot publishing or private source transfers were added.

## 3. Architectural best practices, acceptance and limitations

- CRC-32 provides PNG **chunk integrity**, not authenticity, cryptographic signing or a full image decode. The SHA-256 receipt is still user-supplied and unauthenticated; a malicious actor can construct a different valid image/receipt pair. This verifier does **not** establish visual sanitisation, security clearance, ownership, release identity, DEV execution or permission to publish.
- The acceptance boundary is a canvas-flattened PNG from the Redaction Desk, not arbitrary original PNGs. This narrow policy deliberately fails closed when metadata or unusual colour formats appear.
- Browser testing uses synthetic fixtures only. Static source tests and CI results must be confirmed for the final commit; browser testing is not a native ServiceNow ATF, integration, acceptance or production test.
- **SOURCE-ONLY:** source and tests committed. **MOCK-ONLY:** fixture images. **DEV-VERIFIED:** only historical, scope/version-specific evidence already on record. **PRODUCTION-VERIFIED:** not established. Real image admission remains **HOLD** pending independent full-resolution inspection and rights approval.
- **Licensing:** static website, browser-side CRC/SHA and Playwright: none. Real Workbench installations may require App Engine/custom app rights, platform ACL roles, ITSM, CMDB/ITOM/Discovery, IntegrationHub, analytics/AI and external-provider entitlements according to scope.

**Rollback:** revert this page parser change, regression-test changes and release documentation, keeping the independent image-approval gate unchanged.

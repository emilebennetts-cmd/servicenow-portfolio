# Package fingerprint preparation gate — 15 November 2026

**Public URL:** https://emilebennetts-cmd.github.io/servicenow-portfolio/delivery-release-evolution.html#package-fingerprint  
**Classification:** Public browser feature = MOCK-ONLY / preparation, Delivery repository declaration = SOURCE-ONLY, historical DEV assertions = DEV-REPORTED. **Native DEV/PROD acceptance = NOT RUN. Release decision = HOLD.**

## 1. The client's pain & history

The source README currently declares Delivery Workbench 4.22.2; earlier documentation makes conflicting historical DEV deployment claims. A target scope and version text match cannot demonstrate that the package bytes match an authorised build. Without a digest comparison against an independent release manifest, an incorrect or altered package could be misinterpreted as the correct release. This is a representative engineering risk, not a claim of a customer incident.

## 2. The ServiceNow solution — actual public implementation

Added a functioning browser-local SHA-256 comparison to the existing release-identity preflight rather than another simulated native screen. Select a local release artefact (maximum 25 MiB), optionally provide a trusted 64-character SHA-256 reference, and compute the file digest through WebCrypto. The control explicitly distinguishes a computed digest without reference, invalid reference, matching digest, mismatch, missing file, oversized file and read failure. Editing or clearing either input invalidates the previous result; late async file-read responses are ignored.

- No file content, filename, entered SHA-256 or computed digest is exported or sent over the network.
- A local "Copy computed SHA-256" action supports owner-side comparison without uploading the artefact.
- The existing JSON worksheet exports only the categorical review status and negative privacy/acceptance flags. `target_package_hash_verified`, independent DEV, production, screenshot approval and release decision remain **false / HOLD**, including when digest text matches.
- A matching digest supports byte equality **only to the supplied reference**. Authenticity of that reference, source commit, installed app, scope, UI Page, roles, ACLs and authorised deployment still require independent evidence.

## 3. Architectural best practices / tests / entitlements

**Architecture:** Static HTML and browser WebCrypto; no backend, credentials, files persisted, browser storage, API calls, analytics or ServiceNow scripts. 25 MiB memory bound; input validation and stale-result invalidation; accessible live status; responsive layout.

**Regression controls:** `scripts/test_package_fingerprint_preflight.py`, `scripts/browser_package_fingerprint_preflight.py` and `.github/workflows/package-fingerprint-preflight-browser.yml`. Browser assertions cover four widths (390/768/1024/1440px), matching/mismatching test fixture, invalid reference, reset, exported JSON redaction and absence of HTTP requests. CI receipt must be checked independently: a committed workflow does not itself prove a passed run.

**Native next steps:** 1) obtain approved build manifest from a trusted source; 2) compare package hash; 3) capture installed app sys_id, scope, version and UI Page; 4) independently witness positive/negative ACL tests; 5) assess target-specific entitlements; 6) obtain change approval and screenshot-by-screenshot publication clearance if necessary.

**Licensing:** Public fingerprint page requires no ServiceNow licence. Target-native scoped app needs the customer's applicable App Engine/custom-app entitlements, administrator-controlled roles/ACLs and product subscriptions; IntegrationHub spokes, external providers, analytics, AI/Now Assist and ATF may need separate rights where actually used.

**Publication controls:** No private source copied to public pages; no customer metadata, secrets, photos or original screenshots embedded; underlying source repositories retain existing visibility. This is not a production deployment or certified build.

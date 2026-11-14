# Recruiter-friendly canonical and social sharing metadata

**Release date:** 14 November 2026 · **Classification:** SOURCE-ONLY (website implementation); no native ServiceNow acceptance.

## 1. The client's pain and history
The public portfolio contains in-depth ServiceNow engineering evidence, but six primary entry pages previously exposed only browser titles and description metadata. Sharing those long URLs with recruiters or architecture reviewers could produce incomplete social previews, duplicated URL identities or inconsistent page labels. Introducing real screenshot thumbnails would have violated the outstanding approval HOLD.

## 2. The ServiceNow portfolio solution
Added absolute, unparameterised HTTPS canonical URLs, Open Graph text metadata and Twitter summary-card text metadata to the home page and five critical recruiter entry points:
- Home / portfolio overview
- Universal Delivery Workbench case study
- Diagnostic Workbench 2 case study
- Reusable Delivery Patterns case study
- Workbench Architecture Gallery (including six role-based walkthroughs)
- Searchable Technical Evidence Register

All six preview descriptions expressly describe source-backed capabilities or verification boundaries. There is deliberately **no** Open Graph/Twitter image: existing private original screenshots remain unapproved. The canonical domain is the existing GitHub Pages address, not a purchased custom domain.

## 3. Architectural best practices and quality controls
- New `tests/test_social_share_metadata.py` verifies canonical, OG and Twitter metadata on all six pages; it rejects duplicate or missing keys, external/parameterised canonicals and unapproved social-preview media.
- Existing Delivery Plan privacy test now distinguishes the specifically allowlisted static same-origin canonical/OG URL from prohibited remote references or browser-network activity. This repairs the false-positive regression created by adding legitimate canonical URLs without weakening the protection against new remote URLs.
- Metadata is version-controlled static text with no scripts, client tracking, third-party screenshot assets or private evidence.
- Search engines and preview clients may refresh cached metadata on their own schedules; metadata in source does not guarantee how any particular platform renders a link.
- Publication quality checks and successful GitHub Pages deployment verify **the website only**, not a native ServiceNow application or customer delivery.

### Evidence and entitlement boundaries
- **SOURCE-ONLY:** six website files and automated quality tests.
- **MOCK-ONLY:** existing illustrative UI demonstrations remain unchanged.
- **DEV-REPORTED:** historical, version-pinned observations remain separately labelled.
- **DEV-VERIFIED:** no new native execution established by this release.
- **PRODUCTION-VERIFIED:** none established.
- **Screenshot publication:** 0 approved; HOLD unchanged.
- **ServiceNow licence:** none for the public static site. Native Delivery/Diagnostic applications require appropriate custom-app/App Engine and custom-table entitlements, roles/ACLs, plus relevant ITSM, ITOM/Discovery, IntegrationHub/spokes, ATF, analytics/AI and external provider licences, depending on tested features.

### Review route
[Portfolio](https://emilebennetts-cmd.github.io/servicenow-portfolio/) · [Delivery case study](https://emilebennetts-cmd.github.io/servicenow-portfolio/delivery-case-study.html) · [Diagnostic case study](https://emilebennetts-cmd.github.io/servicenow-portfolio/diagnostic-workbench-case-study.html) · [Architecture gallery](https://emilebennetts-cmd.github.io/servicenow-portfolio/workbench-architecture-gallery.html) · [Evidence register](https://emilebennetts-cmd.github.io/servicenow-portfolio/technical-evidence-register.html)

**Deployment caveat:** GitHub Actions receipts must be recorded against the final release commit. External link-preview appearance and independent public HTTP reachability are distinct checks. No repository visibility change, customer data export or screenshot publication occurred.

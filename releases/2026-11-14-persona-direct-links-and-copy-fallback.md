# Role-specific portfolio permalinks — 14 November 2026

**Change scope:** Public static portfolio only. `workbench-architecture-gallery.html#persona-tour`.
**Evidence classifications:** SOURCE-ONLY (historical controlled-draft role descriptions) and MOCK-ONLY (interactive website behaviour). No DEV-VERIFIED or PRODUCTION-VERIFIED promotion.
**Change state:** Source committed. Final CI/deployment are tracked independently in GitHub Actions; never infer ServiceNow runtime evidence from browser tests.

## 1. The client's pain & history
The public Workbench Architecture Gallery contained six source-informed consulting journeys, but recipients always opened on the presales tab. Recruiters and technical reviewers could not link an architect directly to requirements/design controls, a deployer to release authority, or support engineers to operational-readiness gates. Sharing screenshots would be an inappropriate workaround while genuine Workbench captures remain unapproved.

## 2. The ServiceNow solution — public website increment
- Added fixed allowlisted deep links using `?role=<presales|architect|delivery|tester|deployer|support>#persona-tour`; navigation restores the matching accessible role tab.
- Added an obvious **Open direct link to this role** anchor and a **Copy role link** action. Clipboard failures reveal a selectable, read-only URL field; no action silently claims a successful copy.
- Switching roles updates the prepared link while retaining keyboard, touch and pointer navigation. URLs include only a public role key; arbitrary query parameters are removed from generated links.
- Malformed, unrecognised and prototype-like role values fall back to presales without executing or interpolating untrusted content.
- Original source-only architectural narratives and all release gates remain unchanged. No data is sent to an external endpoint; nothing is persisted in browser storage.

## 3. Architectural best practices, tests and evidence limitations
- Browser regression: `scripts/browser_persona_architecture_gallery.py`, covering inbound architect link, rejected malicious/unknown role values, copy success/fallback, role-specific JSON export, accessible tab state, responsive overflow and four widths: 390/768/1024/1440 px.
- Existing site QA and publication audit continue checking links, class boundaries, source/private segregation and absence of new screenshot assets.
- SOURCE-ONLY source reference: 30 September 2026 controlled-draft Universal Delivery Workbench User Guides and Training (source 4.6.1). Historical 4.5.1 DEV report is not transferred to 4.6.1, later source 4.22.x or a distinct demo app.
- No fresh native instance test, independent DEV acceptance, production change authorisation, licence verification or customer record review was performed.
- **Screenshot status:** 0 individually publication-approved genuine Workbench images. No original pixels, customer artefacts, credentials or private source introduced.

## ServiceNow licence / entitlement boundary
The public HTML, browser clipboard and deep links need **no ServiceNow subscription**. Native Workbench execution remains dependent on relevant App Engine/custom-table subscription allocations, application roles and ACLs; ITSM/ITOM Discovery, IntegrationHub/spokes, ATF, analytics, AI and third-party connectors require contract- and instance-specific entitlement checks. Refer to the public Entitlement & Deployment Readiness page; none is presumed granted.

## Reviewers
Open the gallery at `workbench-architecture-gallery.html?role=architect#persona-tour` or choose any of the six named roles in the page. Its exports remain **UNREVIEWED / NOT VERIFIED / HOLD** and never constitute acceptance or deployment authority.

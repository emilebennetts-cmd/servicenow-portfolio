# Public evidence register — reviewed coverage wave 1
Date: 13 November 2026  
Status: **SOURCE-ONLY publication update; no new ServiceNow execution**

## 1. The client's pain and history
The published explorer indexed 71 pages but only 26 had a dedicated page-level verification classification; 45 showed NOT REGISTERED. This was a metadata gap, not proof of defective or unverified implementation. It made it harder for reviewers to separate documentary architecture, historical DEV reports, synthetic interactions and unimplemented reference designs.

## 2. The ServiceNow solution
Reviewed 25 previously unregistered public pages against their displayed purpose, repository source descriptions and controlled historical documentation; wrote one narrowly scoped entry per page into `evidence/public-verification-register.json`. Each new entry states its documentary basis, native acceptance boundary and screenshot HOLD. No claim was promoted to DEV-VERIFIED or PRODUCTION-VERIFIED.

The public Portfolio Explorer now offers a **PROPOSED** filter, a distinct visible status for reference designs, and a browser-computed count of pages carrying registered evidence metadata. The other filters still combine keyword, subject and evidence classifications. The count is derived from the catalogue rather than a manually maintained number.

### Scope and resulting public register
- **53** classified claims across **51** of the **71** indexed public pages.
- **20** pages remain explicitly **NOT REGISTERED** for subsequent source review.
- Page-level categories: 31 SOURCE-ONLY, 11 MOCK-ONLY, 4 DEV-REPORTED, 4 PROPOSED, 1 MIXED CLAIMS, 20 NOT REGISTERED.
- The two additional claims are separately classified assertions on already-registered pages. Claim counts must not be confused with page counts.
- This pass added 25 reviewed page-level claims; it does **not** attest to 25 completed ServiceNow builds.

Reviewed pages: architecture-atlas, architecture-boundaries, capability-explorer, capability-traceability, ci-job-evidence, delivery-release-evolution, deployment-identity-gates, diagnostic-architecture, diagnostic-case-study, diagnostic-engineering, diagnostic-to-delivery-journey, diagnostic-workbench-case-study, diagnostics-to-delivery, engineering-case-studies, engineering-evidence, engineering-proof, evidence-led-delivery, evidence-methodology, evidence-standards, evidence-to-delivery, evidence-to-release-journey, evidence-verification, evidence, finding-to-delivery, and finding-to-release-handoff (all `.html`).

### Source history and release identity
The linked Universal Delivery Workbench documents stored in Drive are **controlled drafts dated 30 September 2026**. Their source snapshot was **4.6.1**, while the Delivery repository README now describes **4.22.2** source. These are different time-stamped reference points. Neither establishes that 4.22.2 is installed or accepted on any target instance. The Diagnostic completion runbook is also explicitly a fictional, non-production showcase; gate-completion instructions are **not** approvals.

## 3. Architectural best practices
- Register classification applies to the **specific claim**, not every sentence or feature on the page. PROPOSED means design intent; MOCK-ONLY means an invented browser scenario; DEV-REPORTED is historical and needs current independent reproduction.
- A synthetic example and a proposed design must not be combined to produce a stronger claim. Mixed classification is retained whenever multiple claim types coexist on one page.
- Existing controlled screenshots remain **HOLD**: zero original images approved for public embedding. Redaction alone is not publication permission.
- The browser catalogue uses static HTML, locally executed filtering, no ServiceNow credentials and no runtime data access.
- The updated Python reconciliation test rejects stale labels. Added tests cover PROPOSED, metadata coverage, filter behaviour and mobile/desktop interaction without promoting any native verification claim.

## Acceptance / release boundaries
- **SOURCE-ONLY:** public HTML, classifier changes, code-level checks, repository/document provenance.
- **MOCK-ONLY:** existing synthetic browser demonstrations; unchanged native status.
- **DEV-REPORTED:** historical observations as dated in sources; no new read-back.
- **DEV-VERIFIED / PRODUCTION-VERIFIED:** no new evidence recorded.
- **Screenshots:** originals withheld; no new image approved or published.
- **Independent public-domain HTTP reachability:** to be separately checked; GitHub Pages workflow success is not independently observed retrieval.

### Licensing and entitlements
No ServiceNow licence is required to browse the public static website. Native application installation/acceptance requires appropriate App Engine/custom application and table rights, scopes, ACLs and user roles, plus the relevant ITSM, ITOM/Discovery, IntegrationHub, Performance Analytics, AI, and external-provider entitlements when those features are actually used. Verify against the specific licensed target.

## Remaining work
Review 20 unregistered pages individually; document source-specific support before registering them. Secure native, version-pinned DEV acceptance and image-specific owner/publication approvals independently. Do not move any existing private repository to public visibility.

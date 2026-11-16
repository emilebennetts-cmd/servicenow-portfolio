# 16 November 2026 — Diagnostic catalogue lineage boundary and acceptance crosswalk

**Public entry:** [Diagnostic catalogue lineage review](../diagnostic-coverage-explorer.html#lineage-review)  
**Change type:** Existing responsive Diagnostic Explorer enhancement, canonical browser-local source model, Node tests and homepage navigation.  
**Release status:** SOURCE-ONLY implementation; illustrative interface MOCK-ONLY; 12 native gates NOT RUN / HOLD. New DEV-VERIFIED: 0; new PRODUCTION-VERIFIED: 0; approved original screenshots: 0.

## 1. The client's pain and history

A ServiceNow discovery team can confuse similar-looking catalogue counts or treat an older DEV build statement as a current installed capability. The original Diagnostic Workbench module-pack catalogue and the Knowledge Intelligence companion are intentionally different inventories with different evidence payloads, users and governance. Combining their collectors, findings and acceptance outcomes creates a false claim about the current deployed estate. The client story on this page is a representative consulting risk, not a claim of a named customer incident.

## 2. The ServiceNow solution

Added a readable, mobile-friendly comparison directly to the existing Diagnostic Collector Explorer:

- **Base Diagnostic Workbench 2:** source-declared 20 module-pack collectors across ten pack categories, 42 rules, four correlations and 67 runbooks. This catalogue declares the DIAG envelope and an evidence-led, local-first workflow. Source reference: Diagnostic-Workbench2/README_BUILD.md, historical 1 September 2026 verification statement.
- **Knowledge Intelligence 0.1.0 companion:** distinct source-declared 16 knowledge packs, 45 read-only collectors (81 metrics), 65 rule/finding templates and 38 solution patterns. It uses KI-EVIDENCE markers, KI roles and a separately installed companion update set. Source reference: Diagnostic-Workbench2/knowledge-intelligence/README.md, historical 30 September 2026 DEV statement.
- An interactive selector shows either source family or a side-by-side comparison without summing incompatible inventories.
- Twelve canonical review gates (six per catalogue) address installed version, entitlement, least privilege, script authority, envelope/payload completeness and independent finding approval.
- A browser-local downloadable, formula-safe CSV keeps every control SOURCE-ONLY, NOT RUN, UNREVIEWED and HOLD. No imported instance data, customer IDs, screenshots or credentials are used.
- The existing ten-pack coverage gate and its CSV remain unchanged.

Implementation paths: diagnostic-lineage-review.js, diagnostic-coverage-explorer.html, tests/diagnostic_lineage_review.test.cjs, .github/workflows/portfolio-quality.yml, and index.html.

## 3. Architectural best practices

**OOTB-first and ITIL 4 alignment:** Validate native product entitlement, installed release and roles before an optional read-only diagnostic assessment. Never authorise scripts implicitly from this showcase. Correctness of an aggregate depends on source authority, full denominators, query limits and privacy minimisation; human-controlled diagnosis and continual improvement remain distinct from native change implementation.

**Compatibility boundary:** DIAG and KI envelope wrappers are not interchangeable. There is no public claim of a deployed DIAG-to-KI adapter or independently observed runtime interoperability. Source tests and synthetic UI behaviour do not prove a native ServiceNow outcome.

**Security and change control:** Customer records, authentication tokens, instance outputs, private application code and unapproved screenshot files remain outside the static publication. Any actual background-script operation requires designated platform approval and the least-privileged permitted execution route. Preserve the original evidence in authorised private custody and approve only a sanitised derivative for public publication.

## Validation and acceptance requirements

The deterministic Node suite tests exact catalogue counts, envelope separation, twelve unique gate IDs, immutable statuses, source-integrity rejection, limited CSV fields and HTML accessibility anchors. GitHub CI and Pages deployment must be observed separately; a successful file commit alone is not a completed runtime check.

**Native DEV gates still open:** Obtain authorised instance access; read back app scope, version and installed KI update set; inventory subscriptions and scoped roles; run negative-access tests; independently validate each envelope on bounded, privacy-safe test data; reconcile denominator and import safety; review resulting findings separately; record time-bounded approval and evidence. Production is not evaluated.

**Licensing and entitlements:** The static portfolio needs no ServiceNow licence. Running a custom scoped app or companion may require App Engine or other contractual rights depending on the hosting arrangements. ITSM, ITOM Visibility/Discovery, SecOps, IRM, CSM, HRSD, HAM/SAM, IntegrationHub, analytics and knowledge-article reuse require product, role, subscription and external licence checks for each target. No entitlement is inferred from source file presence.

**Original screenshots:** 0 approved; no original images published. Existing [visual evidence review](../visual-evidence.html) continues to withhold publication without image-specific provenance, sanitisation and reviewer authorisation.

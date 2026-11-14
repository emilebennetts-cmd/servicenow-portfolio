# Knowledge Intelligence — 180-case native acceptance handoff

**Release date:** 15 November 2026 (Australia/Sydney)  
**Public entry point:** [Knowledge Intelligence test matrix](../knowledge-intelligence-acceptance-matrix.html#ki-test-matrix)  
**Evidence boundary:** SOURCE-ONLY module taxonomy, PROPOSED native test procedures, NOT RUN / HOLD execution; historical DEV-REPORTED remains separate. **No independently DEV-VERIFIED or PRODUCTION-VERIFIED assertion.**

## 1. The client's pain and history

A 45-collector code catalogue and a historical lint-success report are not a usable, module-by-module acceptance schedule. An architect needs explicit positive and negative test objectives, provenance, and entitlement checks before accepting client-facing diagnostic findings. A missing product table must not be interpreted as zero defects or a passing health score.

## 2. Implemented ServiceNow-oriented handoff

Extended the existing [Knowledge Intelligence acceptance page](../knowledge-intelligence-acceptance-matrix.html), without adding a second mock application. **Two new offline exports:**

- Complete UTF-8 CSV with **180 PROPOSED procedures** for **45 SOURCE-ONLY modules**, using the current source-informed taxonomy already rendered on the page.
- Filtered CSV containing only modules currently visible after product-domain and text filtering. A zero-match selection yields no download and an accessible status message.

Four unique scenarios are generated for every module: **RUN** (read-only evidence envelope, metrics and reviewer lineage), **TABLE** (safe `table_unavailable` handling), **FIELD** (safe `field_unavailable` handling), and **LINT** (offline mutating-collector rejection). Each proposed case includes the source module, representative table, precondition, plan-only instructions, expected result, `ki-evidence/1.0` contract, nominal two-minute time limit, human review and unfilled execution/evidence slots.

**Every export explicitly carries** `SOURCE-ONLY` / `PROPOSED` / `NOT RUN` / `HOLD`, false DEV/production flags, no execution date and no actual evidence reference. CSV cells are quoted and formula-like leading characters are neutralised. All source data come from fixed DOM taxonomy; no customer files, actual collector scripts, remote calls, local storage or credentials are used.

Safety requirements: check product availability, contractual licence and least-privilege ACL access first; simulate missing fields/tables using authorised isolated PDI fixtures; **never delete real instance tables, alter deployed dictionary entries or run a mutating script**. The worksheet is not a native ATF suite or a certificate.

## 3. Architectural best practices and release verification

Source reviewed: private Diagnostic Workbench 2 `knowledge-intelligence/README.md` and `knowledge-intelligence/docs/VERIFY.md` (companion 0.1.0, 16 source tables, 45 declared collectors, historical DEV install/lint on 30 September 2026, wider acceptance still open). The connected Universal Delivery Workbench As-Built and Architecture drafts distinguish source release from independently observed runtime baselines. No restricted document, client identifier or original image was copied to this public document.

Implementation: enhanced accessible section in the existing page; keyboard-operable export buttons; mobile CSS and focus styling; CSP `connect-src 'none'`, no external services. Added offline Python assertions and real Chromium CSV-content regression at **390 / 768 / 1024 / 1440 px**, including 180 unique IDs, four scenario types, filtered count, empty state, CSV classification flags, and network isolation.

### Licences and entitlements

No ServiceNow licence for this public static exporter. Running the tests in a real target requires authorisation for a non-production instance, scoped App Engine/custom-table capacity as contracted, KI role and table ACLs, and subscriptions/plugins for underlying products (ITSM, CMDB/ITOM/Discovery, ITAM, SecOps, IRM, HRSD, CSM, SPM, WSD and optional AI / IntegrationHub). Approved knowledge-content rights and optional ATF rights are separate checks. Absence of any dependency blocks the relevant test; never mark it passed.

### Outstanding gates

- Independent current-version DEV/PDI package, dictionary, role and ACL read-back.
- Controlled execution and evidence for each proposed test with independent review.
- Authorised production change/acceptance and entitlement verification.
- Individually sanitised and approved screenshot derivatives (**zero original screenshots authorised to publish — HOLD**).
- Independent external link reachability check; GitHub Pages CI is not proof of worldwide access.

**Publication:** No private repository visibility, source, screenshots or customer data changed or disclosed.

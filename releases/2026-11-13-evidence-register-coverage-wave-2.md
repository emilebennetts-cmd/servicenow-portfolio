# Evidence coverage wave 2 — Complete 71-page catalogue classification
Date: 13 November 2026
Release class: **SOURCE-ONLY website and evidence-register maintenance**
Publication posture: **No original screenshots approved; no new native DEV or Production verification**

## 1. The client's pain & history

The public Portfolio Explorer indexed 71 pages but 20 pages still showed `NOT REGISTERED`. These were mostly high-visibility pages: the homepage, the Workbench experience, source architecture, reusable patterns and several evidence/acceptance guides. A reviewer could mistake a missing metadata label for absent functionality or assume the polished synthetic UI represented an authenticated instance. The 51 previously classified catalogue pages did not make that ambiguity disappear.

## 2. The ServiceNow solution

Reviewed the remaining 20 pages individually against their public assertions, the Delivery and Diagnostic repository READMEs and the controlled 30 September Delivery As-Built/Architecture/Training and fictional Diagnostic completion runbook. Recorded **26 narrowly scoped new claims** because six of the pages contain distinct evidence classes that must be displayed as `MIXED CLAIMS`.

The public manifest now contains **79 claims** spanning **72 unique HTML pages**: the 71 indexed catalogue pages plus the Portfolio Explorer itself. The Explorer now has **71/71 entries classified, 0 NOT REGISTERED**. This is full **metadata** coverage, not 100% runtime acceptance.

| Explorer label | Pages |
| --- | ---: |
| SOURCE-ONLY | 42 |
| MOCK-ONLY | 13 |
| DEV-REPORTED | 4 |
| PROPOSED | 5 |
| MIXED CLAIMS | 7 |
| NOT REGISTERED | 0 |
| **Total indexed pages** | **71** |

The extra SOURCE-ONLY page in the register (43, rather than 42) is the Explorer itself, which is excluded from its own catalogue.

### All 20 newly reviewed pages

| Page | Evidence status | Claim boundary |
| --- | --- | --- |
| `implementation-boundaries.html` | SOURCE-ONLY | Versioned source interpretation |
| `index.html` | MIXED CLAIMS | Implemented navigation and linked synthetic examples |
| `pattern-library-experience.html` | MOCK-ONLY | Synthetic lifecycle selector |
| `pattern-library.html` | MIXED CLAIMS | Historical export assessment and undeployed target design |
| `pattern-lifecycle.html` | SOURCE-ONLY | Repository-described lifecycle |
| `pattern-readiness.html` | MOCK-ONLY | Illustrative local readiness rubric |
| `portfolio-review-guide.html` | SOURCE-ONLY | Review navigation and evidence policy |
| `publication-quality.html` | SOURCE-ONLY | Historical website CI, not ServiceNow acceptance |
| `reusable-delivery-patterns-case-study.html` | SOURCE-ONLY | Source-grounded engineering case study |
| `reusable-delivery-patterns.html` | SOURCE-ONLY | Source-described selection and reconciliation |
| `technical-evidence-register.html` | SOURCE-ONLY | Public source evidence pointers |
| `technical-reviewer-walkthrough.html` | SOURCE-ONLY | Reviewer guide and open native evidence |
| `verification-ledger.html` | SOURCE-ONLY | Public claim-manifest browser interface |
| `verification-playbook.html` | PROPOSED | Test protocol not yet executed |
| `visual-evidence-intake.html` | SOURCE-ONLY | Image intake and publication controls |
| `workbench-acceptance-playbook.html` | MIXED CLAIMS | Documented protocols and illustrative worksheet |
| `workbench-architecture-gallery.html` | MIXED CLAIMS | Source diagrams and proposed cross-workbench handoff |
| `workbench-architecture.html` | MIXED CLAIMS | Source boundary and proposed integration |
| `workbench-evidence-ledger.html` | SOURCE-ONLY | Source and historical assertion review |
| `workbench-experience.html` | MIXED CLAIMS | Source architecture and synthetic UI compositions |

### Implemented prevention of drift

- `scripts/reconcile_explorer_evidence.py --check` now **fails closed** if a new indexed page is missing a public evidence claim, rather than merely regenerating a `NOT REGISTERED` badge.
- Added regression tests for complete coverage, deliberate detection of new unregistered pages, and explicit non-promotion of mixed claims.
- Updated the Chromium four-width test to assert zero existing unregistered pages and the correct empty state when that filter is selected. The filter remains available to surface future metadata gaps.
- Reconciled the reviewer guide's inspected evidence count from six to eight; removed the ledger's stale fixed navigation count and static manifest update timestamp.

## 3. Architectural best practices / audit boundary

**SOURCE-ONLY:** The new register entries, Python checks, public documentation, source version interpretation and browser code. CI or website operation is not an authenticated ServiceNow acceptance test.

**MOCK-ONLY:** Pattern-readiness and stage selectors, browser worksheets and Workbench UI reconstructions. None submits a native ServiceNow transaction or external provider request.

**DEV-REPORTED:** Older, explicitly dated records remain separate. The controlled 30 September Delivery docs describe source **4.6.1**, a historically reported DEV **4.5.1** read-back and a still-pending newer installation; the current Delivery README describes later **4.22.2 source**. They are not interchangeable. Diagnostic SDK source is also not a fresh runtime read-back.

**DEV-VERIFIED and PRODUCTION-VERIFIED:** No new independent execution, release approval or production claim was obtained. Genuine screenshot approvals remain **zero (HOLD)**. No private PDFs, screenshots, hashes, customer records, ServiceNow instance URLs or private source were copied to the public repository.

**Tests:** Repository quality and browser CI are separate from ServiceNow execution and need to be confirmed against the final commit. GitHub Pages deployment and independent external reachability are separate checks.

### Licensing and entitlements

No ServiceNow entitlement is required for this static public website. For a native implementation, confirm application ownership, App Engine/custom-app and custom-table rights, roles and ACLs, and scope-specific ITSM/ITOM/Discovery/ITAM, IntegrationHub/spokes, Performance Analytics, AI and third-party licences in the target environment.

## Remaining gates

Obtain independently reproducible, version-pinned native DEV acceptance. For real screenshots require capture ownership, exact version and role, irreversible redaction, reviewer sign-off and individual publication approval before embedding. Keep controlled source and private repositories restricted.

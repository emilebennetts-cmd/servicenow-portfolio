# 16 November 2026 — CMDB Tag Governance and key-value assurance lab

## 1. The client's pain & history
A fictional, multi-cloud CMDB uses several provider feeds with mismatched `Env`, `env` and `Environment` tag conventions, incomplete owner/cost-centre keys, and a manual workaround that Discovery would overwrite. These can compromise chargeback reporting, exception accountability and tag-driven application service populations. No real customer counts, records or measured performance improvements are claimed.

## 2. The ServiceNow solution
- Delivered [CMDB Tag Governance Lab](../cmdb-tag-governance-lab.html): five mobile-responsive investigations using a visual, CSS-generated **illustrative** policy console. There are **no original instance screenshots**.
- Implemented deterministic, browser-local, network-free scenarios for key aliases, a missing cost-centre tag, colliding values, re-ingestion after a manual change, and an apparently clean case.
- The clean case correctly returns **REVIEW — NOT APPROVED**, not a native policy pass. Blocking cases say **HOLD — REMEDIATION BLOCKED**. No browser action can assert real DEV acceptance.
- Exports a five-gate CSV per case and a complete **25-gate native DEV acceptance worksheet**, with immutable `NOT RUN`, `HOLD`, `MOCK-ONLY` columns and blank instance, installed plugin/version, executor, timestamp, private evidence and independent-review fields.
- Added Node contract tests and four-viewport browser workflow (375, 768, 1024 and 1440 pixels), indexed homepage/Explorer entry, sitemap and public verification-register classification.
- No remote API calls, credentials, customer identifiers, private code, automatically approved screenshots, or mutation of native platform records.

## 3. Architectural best practices
1. **OOTB-first:** Check installed Tag Governance capabilities and effective Tag Count, Tag Presence and Tag Key & Value policy definitions before considering custom bulk scripts.
2. **Source correction:** Inspect `cmdb_key_value`, authorised CI associations, provider reconciliation and discovered timestamps. A local manual fix can be overwritten by the next discovery cycle; correct upstream where possible.
3. **Governance:** Owner approval, time-boxed exceptions, task assignment, ACL-denied persona, and independent remediation review precede any destructive changes.
4. **Downstream effect:** Tag-based Service Mapping may change service membership. Check category/key rules and candidate populations in authorised non-production acceptance.
5. **Release fail-closed:** No static/demo/browser result may become DEV-VERIFIED or PRODUCTION-VERIFIED. Native evidence must be dated, source-pinned and reviewed separately.

## Source evidence and limitations
- ServiceNow [Tag Governance](https://www.servicenow.com/docs/r/washingtondc/it-operations-management/itom-visibility/tag-governance.html) documents key-value cloud tags, policies and remediation tasks.
- ServiceNow [tag-based service mapping preparation](https://www.servicenow.com/docs/r/it-operations-management/service-mapping/prepare-map-service-tag.html) and [application-service tag population](https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/populate-app-service-tags.html) describe `cmdb_key_value`, tag categories and tag-driven service membership.
- Private Delivery `solution-lifecycle-studio` README declared source 4.22.2 and a separate older DEV baseline. Private Diagnostic `Diagnostic-Workbench2` README confirms app scope and explicitly differentiates source from deployment. Those readmes provide provenance discipline, **not** Tag Governance test results.
- Controlled 30 September 2026 Google Drive `01-Universal-Delivery-Workbench-Solution-As-Built.pdf` records a draft Delivery source 4.6.1 and historical DEV 4.5.1. It is not an approved Tag Governance As-Built and does not establish current native installation. No restricted content has been reproduced.

| Boundary | Current position |
| --- | --- |
| Public HTML, JS and tests | SOURCE-ONLY implementation |
| Illustrative screen, examples, policy findings, CSV | MOCK-ONLY |
| Historical Workbench source claims | DEV-REPORTED only if source explicitly says so; no promotion |
| New Tag Governance native DEV acceptance | 0 / 25 run; NOT RUN / HOLD |
| New Tag Governance production verification | 0 / 25; NOT RUN / HOLD |
| Original ServiceNow screenshot publication | 0 individually approved; HOLD |
| Public site licence | None |
| Native licensing | Target-specific Tag Governance / ITOM Visibility, Discovery or Service Graph Connectors, Service Mapping, CMDB roles and applicable integration spokes as used; verify purchased rights, installed application, release and permissions. |

## Deliverables
- [Responsive case study](../cmdb-tag-governance-lab.html)
- [Deterministic policy model](../cmdb-tag-governance-model.js)
- [Source regression suite](../tests/cmdb_tag_governance.test.cjs)
- [Four-width browser test](../scripts/browser_cmdb_tag_governance.py)
- [Public verification register](../evidence/public-verification-register.json)

## Remaining approval gates
Access to an authorised DEV instance and its plugin/version/role read-back, actual native audit and remediation tests, denied-persona verification, independent reviewer sign-off, and image-specific sanitisation/publication approval. These are blockers for stronger verification labels, not for this source-only static training release.

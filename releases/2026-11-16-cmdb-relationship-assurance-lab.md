# 16 November 2026 — CMDB Relationship Integrity Assurance Lab

## 1. The client's pain & history
In a **fictional** enterprise CMDB, discovery, cloud import and manual updates produce ambiguous service dependencies. Duplicate or orphan `cmdb_rel_ci` rows, stale CI endpoints and incompatible direction policies can make a topology look plausible while making change impact and incident routing unreliable. No customer counts, outcomes or measured improvements are claimed.

## 2. The ServiceNow solution
- Added [CMDB Relationship Integrity Assurance Lab](../cmdb-relationship-assurance-lab.html), a mobile-responsive, accessible static page with five fixture-driven investigations: duplicate, orphan, stale, invalid direction and clean-looking baseline.
- Created deterministic JavaScript evaluation for exact parent/child/type/port duplicates, nonexistent endpoints, synthetic stale nodes and a **fictional** class-direction policy. This code is a training example and does **not** reproduce native CMDB Health calculations, CI Class Manager inheritance or processor behaviour.
- Added a CSS/text illustrative relationship review console, **not a real screenshot**, and a safe offline CSV export for six selected or all **30** immutable native acceptance gates. Every gate is NOT RUN / HOLD / MOCK-ONLY; instance, version, executor, timestamp, receipt and reviewer fields remain blank.
- Added automated Node regression coverage, portfolio-quality workflow invocation, and updated homepage, Explorer (89 pages), sitemap, verification register and release log.

## 3. Architectural best practices
- OOTB-first: use relationship records, CI Class Manager effective suggested/dependent rules and native Relationship Health reports.
- Relationship Health Dashboard requires an effective processor job. ServiceNow cautions that enabling the relationship processor can affect performance; scope and schedule under change control.
- Use native effective inheritance and approved class pairs, not the lab's hard-coded illustration; confirm actual `cmdb_rel_ci` relationship source/identity and compare ingestion replay.
- Treat graph anomalies as investigation triggers, not deletion orders; preserve upstream ownership, negative-persona ACL evidence, CSDM service-impact checks and independent approval.
- Keep the static-site release separate from DEV installation and Production acceptance. No new native results were observed.

## Source boundaries
- [ServiceNow Australia: relationship governance rules](https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/relationship-governance.html), updated 12 March 2026; defines class/direction governance and inheritance.
- [ServiceNow Australia: Relationship Health Dashboard](https://www.servicenow.com/docs/r/servicenow-platform/configuration-management-database-cmdb/t_ViewRelationshipsHealth.html), updated 12 March 2026; covers duplicate/orphan/stale relationships, compliance and processor caution.
- Read Delivery `solution-lifecycle-studio` and Diagnostic `Diagnostic-Workbench2` repository READMEs, and the 30 September 2026 controlled, unapproved Google Drive Universal Delivery Workbench As-Built. These establish portfolio/provenance context only, not CMDB relationship testing or a customer implementation.
- Source/MOCK distinctions: new HTML and JS are SOURCE-ONLY; synthetic decisions and visual console are MOCK-ONLY; historical workbench DEV is DEV-REPORTED where documented; native DEV-VERIFIED 0; PRODUCTION-VERIFIED 0; approved original screenshots 0/HOLD.

## Entitlement dependency
Static site: no ServiceNow licence. In-instance CMDB review and health configuration: applicable CMDB capabilities, installed jobs and required read/administration roles. Discovery / ITOM Visibility, Service Mapping, Service Graph Connectors, IntegrationHub, ATF or analytics must be separately verified under the target licence, installed plugins and contract. No entitlement is inferred from a mock.

## Remaining acceptance
Authorised non-production instance/version and processor read-back; actual execution of the 30 tests; sample population and source lineage; permitted and denied ACL personas; independent reviewer and image-specific publication approval. No source secrets, customer data, or private source published.

# Pattern item-consumption integrity contract — 17 November 2026

**Status:** SOURCE-ONLY site implementation; MOCK-ONLY fixed scenarios; NOT RUN native acceptance; independent release decision HOLD.

## 1. The client's pain & history

The 28 September historical read-only pattern assessment recorded 96 parent patterns and 4,595 linked export items. The current Delivery repository explicitly states that its 96 mined references are *parent-only* there because the historical child records are not present in GitHub. A visual library can appear complete while an engagement generator cannot safely consume missing typed child items. The 30 September Universal Delivery Workbench controlled As-Built and Architecture are unapproved drafts, with a historical 4.5.1 DEV read-back separate from later source releases. No records have been imported from those private documents into the public site.

## 2. The ServiceNow solution illustrated

Implemented a no-network, mobile-friendly **six-lane pattern item-consumption contract** in [the existing pattern-library case study](../pattern-library.html#consumption-contract). Four immutable fictional input cases show (a) parent-only source gaps, (b) partial unapproved drafts, (c) design-reviewed synthetic candidates and (d) unresolved parent identity. Mapping lanes: workshop questions, requirements, decisions, build guidance, tests and handover. Missing linked items are explicitly blocked rather than filled with fabricated data. Complete hypothetical governance only makes **synthetic engagement drafts** eligible; tests remain NOT RUN and approval HOLD. A six-row CSV export is local, formula-safe and contains no target instance or private evidence fields.

Added a deterministic UMD model, seven Node regression tests, a new quality-gate step and homepage navigation. The existing historic/export evidence claims were not promoted to current DEV verification.

## 3. Architectural best practices

OOTB-first evaluation of existing ServiceNow workflows and data model precedes customisation. Pin both pattern and engagement versions; validate roles/ACLs and target licences/plugins; use idempotent create-missing-only draft mappings; preserve edited requirements and approvals; derive tests as **unrun**; obtain actual native evidence and independent change authority before release. The browser demonstrator does **not** perform ServiceNow API calls or native application writes.

**Provenance reviewed:** Delivery source README v4.22.2 (current source declaration), private `patterns/MIM-FOUNDATION-001/provenance.json` indicating a draft, and controlled Google Drive As-Built/Architecture dated 30 September 2026 (unapproved; historical DEV 4.5.1). The public page exposes only generic source-safe findings, not private source contents or document identifiers.

**Licensing:** Public case study needs none. Native implementation may need custom scoped-app rights plus relevant ServiceNow product subscriptions (ITSM/ITOM/CMDB/ITAM/IRM/HRSD/CSM as applicable), approved integration spokes/IntegrationHub, ATF/test permissions and licensed provider APIs. Confirm in the target environment; licence identifiers in source metadata are not entitlement evidence.

**Outstanding gates:** authorise current DEV read-back, execute source-to-draft native tests, independently review against the installed version, approve individual screenshot releases. No new DEV-VERIFIED or PRODUCTION-VERIFIED claims, original screenshots, secrets, customer records or private application code were published.

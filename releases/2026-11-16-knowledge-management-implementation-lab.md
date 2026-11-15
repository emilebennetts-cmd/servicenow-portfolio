# 2026-11-16 · Knowledge Management OOTB-first implementation lab

## Purpose
Extend the ITSM consulting portfolio with Knowledge Management, distinct from the separate Diagnostic Workbench Knowledge Intelligence companion. The client-history story is explicitly representative and synthetic, not a real customer assertion.

## Implemented
- Added responsive, keyboard-accessible Knowledge Management HTML case study and isolated JavaScript model.
- Built three switchable scenarios: contributor authoring/approval, positive and negative reader access, and versioning-aware review/retirement. Each contains eight stable native DEV acceptance controls (24 total).
- Per-scenario review markings have no browser persistence. Offline CSV exports contain only authored test descriptions, fixed native **NOT RUN**, release **HOLD**, and **MOCK-ONLY** labels, with blank private receipt fields.
- Linked homepage, searchable Explorer, deterministic sitemap and public verification register.
- Added Node behavioural and Python static regression coverage; Node test is invoked by the existing quality workflow.
- No ServiceNow API, live auth, ServiceNow screenshot, private source or customer data is embedded.

## Architecture and evidence
- OOTB Knowledge base and kb_knowledge before custom tables. Configure Can Read / Can Contribute and ownership on a per-base basis, test both authorised and excluded personas, and select the supported base-specific publish and retire lifecycle.
- Knowledge Management Advanced versioning, state handling and ownership-related capabilities require prerequisite checks. Do not treat a synthetic workflow as the installed ServiceNow configuration.
- Classification: authored code **SOURCE-ONLY**, interaction/testing fixtures **MOCK-ONLY**, historical instance evidence **DEV-REPORTED** only. Newly **DEV-VERIFIED 0** and **PRODUCTION-VERIFIED 0**. Original screenshot approvals **0 / HOLD**.
- Follow-up: authenticate to authorised DEV; confirm target release/plugin state/entitlements; run and peer-review the 24 positive, negative and governance tests; keep evidence private; approve each screenshot separately.

## Licensing
No ServiceNow licence for the public static lab and offline CSV. Native platform use depends on the target subscription, role ACLs, installed Knowledge capabilities and base ownership. Validate Knowledge Management Advanced/related enhancements, ATF, Now Assist, analytics, IntegrationHub and associated entitlements independently.

## References
- https://www.servicenow.com/docs/r/servicenow-platform/knowledge-management/create-knowledge-article.html
- https://www.servicenow.com/docs/r/servicenow-platform/knowledge-management/create-a-knowledgebase.html
- https://www.servicenow.com/docs/r/servicenow-platform/knowledge-management/knowledge-article-states.html
- https://www.servicenow.com/docs/r/servicenow-platform/knowledge-management/r_KnowledgeWorkflows.html

Release verification status: GitHub CI/PAGES to be recorded separately. A successful public website test is **not** a native ServiceNow DEV or Production test.

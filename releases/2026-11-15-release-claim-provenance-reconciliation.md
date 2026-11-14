# Release-claim provenance reconciliation — 15 November 2026

## 1. The client's pain & history
The public case study cited a dated README with a 4.20.0 DEV-reported baseline and 4.22.2 source declaration. A separate 19 October controlled As-Built / Architecture pair reports a 6 October DEV read-back of 4.22.2 yet contains front-matter warning that source 4.22.2 is not represented as installed. Choosing either claim without a version-matched target receipt could mislead recruiters, architects or client reviewers. The Diagnostic case study also incorrectly labelled historical source-reported receipts as "DEV-VERIFIED".

## 2. The ServiceNow-oriented solution
- Added a responsive, self-contained, four-card source-vs-DEV evidence review to `delivery-release-evolution.html#release-evidence-reconciliation`. It preserves 4.22.2 SOURCE-ONLY, README 4.20.0 DEV-REPORTED (5 Oct), As-Built 4.22.2 DEV-REPORTED (6 Oct, evidence cutoff 19 Oct), and restricted later UI-only read-back, explicitly marking the discrepancy HOLD.
- Provided two expandable native-acceptance and image-clearance checklists, linking to existing public assurance resources. No private Drive links, IDs or original contents were published.
- Corrected `diagnostic-workbench-case-study.html` heading from the misleading DEV-VERIFIED historical-source wording to **DEV-REPORTED**, preserving the reported 1 September core and 30 September KI historical observations without upgrading their proof grade.
- Added an offline regression to guard the contradictory label, current/older version distinction, absolute screenshot HOLD and no private references. Existing public claim register classifications were not escalated.

## 3. Architectural best practices and verification
Source code, claimed historical instance read-backs, independent target testing and production validation are four different evidence layers. An authorised ServiceNow owner must inspect installed app scope/version, package identity and source hash; separately verify UI endpoints, protected data, roles, ACL negatives, upgrade-safe changes, and release approvals before certifying current DEV. Production claims require their own authorised change/read-back. Jira/Confluence/Notion adapters remain mock-only unless authenticated operation is independently tested.

**Test:** `python -m unittest scripts.test_release_evidence_conflicts -v` (also discovered by the portfolio quality workflow). After publishing check source quality, audit and Pages run against the final GitHub head; a pending workflow is not a pass.

**Evidence status:** SOURCE-ONLY + conflicting historical DEV-REPORTED; no fresh DEV-VERIFIED, no PRODUCTION-VERIFIED, no genuine screenshot publication approval (0 / HOLD).

**Licensing:** The public website uses no ServiceNow licence. Native acceptance requires authorised custom-app/App Engine and role/ACL rights, relevant subscribed ITSM/ITOM/IRM/HRSD/CSM features, and conditional IntegrationHub, AI, analytics and third-party connectors; customer contract and instance release must be checked.

**Restricted provenance:** Exact document IDs and reviewer receipts belong in the private control repository. This release does not change private visibility or publish sensitive artefacts.

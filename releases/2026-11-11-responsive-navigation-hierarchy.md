# 2026-11-11 — Responsive portfolio navigation hierarchy

## The client's pain & history

The public homepage had accumulated 18 separate desktop-header links. On narrow laptop and tablet viewports, those links competed for horizontal space while the compact `Explore` directory was hidden at every viewport wider than 560px. The result was an overfilled primary navigation bar that obscured the highest-value case studies and verification material. This change corrects an observable source-level information architecture defect; no unmeasured usability outcome is asserted.

## ServiceNow portfolio solution

- Replaced the 18-link primary header with four high-priority destinations: engineering case studies, architecture gallery, visual evidence and contact.
- Kept a native HTML `details/summary` directory available on **all** viewport widths, rather than only on small phones.
- Arranged 18 secondary links into three descriptive groups: Start here, Workbench solutions, and Evidence & assurance.
- Included the most important proof boundaries: screenshot candidate review (HOLD), evidence ledger, acceptance playbook and verification classifications.
- Made the directory responsive at 820px and 540px, with vertical scrolling, a 44px summary target and an accessible heading hierarchy.
- Retained the existing Escape-to-close, outside-click and close-on-selection behaviour. No new JavaScript dependency, remote script or private asset was introduced.
- Added a dependency-free Python regression test at `scripts/test_home_navigation.py` checking priorities, 18 directory links, public target existence, fragment targets, accessible labelling and responsive CSS.

## Architectural best practices

**OOTB-first / upgradeability:** The site uses semantic `nav` and native `details` rather than a third-party menu widget. It changes the public presentation only; ServiceNow scoped-app source, instance state and repository permissions are untouched.

**Accessibility:** Keyboard users can reach the directory via `summary`, navigate normal anchors and close via Escape. Native disclosure state is conveyed by the browser. Responsive changes intentionally avoid horizontal navigation overflow at common laptop and tablet widths. Actual device and assistive-technology validation remains a separate acceptance task.

**Evidence tiers:**
- **SOURCE-ONLY:** HTML/CSS and offline regression test committed; browser/layout validation and quality-gate status to be checked against the final commit.
- **DEV-VERIFIED:** No new ServiceNow DEV test performed; historical evidence stays version-specific and source-reported.
- **MOCK-ONLY:** Existing illustrative Workbench interfaces and synthetic demonstrations remain labelled as such.
- **PRODUCTION-VERIFIED:** Not established. Static GitHub Pages deployment is not ServiceNow production verification.

**Publication:** No screenshot or original source document was published. The existing 4 reviewed evidence records remain HOLD, and the independent ten-candidate inventory remains separate. No customer-specific content, tokens or private repository URLs were added.

## Acceptance / follow-up

1. Confirm quality workflow, HTML audits, local link checks and GitHub Pages deployment for the final release commit.
2. Test navigation using narrow laptop (e.g. 1024px), tablet (768px) and phone (390px) browser viewports, plus keyboard-only/assistive-technology review; CI unit tests alone do not establish a visual layout pass.
3. Resume authorised screenshot provenance/sanitisation/approval workflow without weakening the publication gate.

## Licensing and entitlements

- GitHub Pages static navigation, CSS and standard-library Python regression test: **no ServiceNow licensing required**.
- Runtime Workbench deployment: verify custom-app/App Engine entitlements, platform access and roles, plus optional ITSM, ITOM, IntegrationHub selected spokes, Performance Analytics, AI and third-party vendor licences according to actual functionality. None is implied by this website change.

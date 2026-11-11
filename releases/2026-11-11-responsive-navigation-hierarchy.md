# 2026-11-11 — Responsive portfolio navigation hierarchy

## The client's pain & history

The public homepage had accumulated 18 separate desktop-header links. On narrow laptop and tablet viewports, those links competed for horizontal space while the compact `Explore` directory was hidden at every viewport wider than 560px. The result was an overfilled primary navigation bar that obscured the highest-value case studies and verification material. This change corrects an observable source-level information architecture defect; no unmeasured usability outcome is asserted.

## ServiceNow portfolio solution

- Replaced the 18-link primary header with four high-priority destinations: engineering case studies, architecture gallery, visual evidence and contact.
- Kept a native HTML `details/summary` directory available on **all** viewport widths, rather than only on small phones.
- Arranged 18 secondary links into three descriptive groups: Start here, Workbench solutions, and Evidence & assurance.
- Included the most important proof boundaries: screenshot candidate review (HOLD), evidence ledger, acceptance playbook and verification classifications.
- Made the directory responsive at 980px and 540px, with vertical scrolling, a 44px summary target and an accessible heading hierarchy.
- Retained the existing Escape-to-close, outside-click and close-on-selection behaviour. No new JavaScript dependency, remote script or private asset was introduced.
- Added a dependency-free Python regression test at `scripts/test_home_navigation.py` checking priorities, 18 directory links, public target existence, fragment targets, accessible labelling and responsive CSS.
- Added a Chromium browser smoke at `scripts/browser_navigation_smoke.py` and GitHub Actions workflow `portfolio-responsive-smoke.yml`. The browser test navigates real HTML at 390px, 768px, 1024px and 1440px, checks header overflow, menu bounds, Escape/focus and an actual link to the public evidence page. It captures **no** screenshots.

## Architectural best practices

**OOTB-first / upgradeability:** The site uses semantic `nav` and native `details` rather than a third-party menu widget. It changes the public presentation only; ServiceNow scoped-app source, instance state and repository permissions are untouched.

**Accessibility:** Keyboard users can reach the directory via `summary`, navigate normal anchors and close via Escape. Native disclosure state is conveyed by the browser. Responsive changes intentionally avoid horizontal navigation overflow at common laptop and tablet widths. Actual device and assistive-technology validation remains a separate acceptance task.

**Evidence tiers:**
- **SOURCE-ONLY:** HTML/CSS, offline regression test and browser CI scripts committed. Chromium exercised the local public site successfully at four widths on commit `ae7fcfed0615ecb01e0bfa933213c733a518d944`; this is real browser verification of the static site, not a ServiceNow DEV or production runtime test.
- **DEV-VERIFIED:** No new ServiceNow DEV test performed; historical evidence stays version-specific and source-reported.
- **MOCK-ONLY:** Existing illustrative Workbench interfaces and synthetic demonstrations remain labelled as such.
- **PRODUCTION-VERIFIED:** Not established. Static GitHub Pages deployment is not ServiceNow production verification.

**Publication:** No screenshot or original source document was published. The existing 4 reviewed evidence records remain HOLD, and the independent ten-candidate inventory remains separate. No customer-specific content, tokens or private repository URLs were added.

## Acceptance / follow-up

1. GitHub Actions quality gate, portfolio audit, Chromium responsive browser smoke and Pages build all **passed** at `ae7fcfed0615ecb01e0bfa933213c733a518d944`:
   - [Chromium 390/768/1024/1440 browser checks](https://github.com/emilebennetts-cmd/servicenow-portfolio/actions/runs/43020752139)
   - [Quality gate](https://github.com/emilebennetts-cmd/servicenow-portfolio/actions/runs/43020752195)
   - [Portfolio audit](https://github.com/emilebennetts-cmd/servicenow-portfolio/actions/runs/43020752046)
   - [GitHub Pages deployment](https://github.com/emilebennetts-cmd/servicenow-portfolio/actions/runs/43020751749)
   - [Local-link integrity on the navigation source change](https://github.com/emilebennetts-cmd/servicenow-portfolio/actions/runs/43020607606).
   Live-device assistive-technology testing and independent rendering of the hosted Pages URL remain outstanding.
2. Chromium smoke passed for the four specified viewports and keyboard Escape/focus; continue with manual real-device and assistive-technology review. Automated geometry checks do not prove visual polish on every browser.
3. Resume authorised screenshot provenance/sanitisation/approval workflow without weakening the publication gate.

## Licensing and entitlements

- GitHub Pages static navigation, CSS and standard-library Python regression test: **no ServiceNow licensing required**.
- Runtime Workbench deployment: verify custom-app/App Engine entitlements, platform access and roles, plus optional ITSM, ITOM, IntegrationHub selected spokes, Performance Analytics, AI and third-party vendor licences according to actual functionality. None is implied by this website change.

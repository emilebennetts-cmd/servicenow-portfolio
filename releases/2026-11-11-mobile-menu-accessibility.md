# Release record — 2026-11-11 — Mobile navigation interaction

## Change
Updated `index.html` to close the compact `details.mobile-directory` navigation when the visitor presses Escape, taps outside the menu, or follows one of its links. Escape returns focus to the summary control. Existing disclosure semantics and desktop navigation remain unchanged.

## Provenance
Source change: commit `da2a9ca6d22831fcb491222e8a8ac26fd39d33fd`.
Before this change, the compact menu was implemented as a native details element, with no explicit outside-click or Escape close behaviour in the homepage JavaScript.

## Verification
- **SOURCE-ONLY:** GitHub accepted the homepage change; source inspection confirmed the event handlers.
- **DEV-VERIFIED:** No new ServiceNow instance testing; not applicable to website navigation.
- **MOCK-ONLY:** Existing illustrative Workbench interfaces remain mock-only.
- **PRODUCTION-VERIFIED:** No ServiceNow production validation is claimed.
- **WEBSITE:** Before this change, GitHub Actions pages deployment and portfolio quality checks both reported success in runs 42863935888 and 42863933857 (10 Nov 2026 UTC). These results do not verify this new commit. Post-change keyboard, mobile browser, and deployment verification remain outstanding.

## Publication controls and dependencies
No screenshot, private source, customer data, or credentials were introduced. This static navigation change requires no ServiceNow licence. Runtime Workbench deployments may separately require App Engine/custom application rights, relevant ITSM/ITOM products, IntegrationHub, Performance Analytics or AI entitlements depending on installed features and contract.

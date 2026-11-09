# Release — 2026-11-10 — Interactive pattern lifecycle experience

## Scope
- Added `pattern-library-experience.html`: responsive, keyboard-operable five-stage pattern lifecycle explorer with live region announcements and no external JavaScript dependencies.
- Linked the explorer from `workbench-experience.html`.
- Source basis: `solution-lifecycle-studio/patterns/MIM-FOUNDATION-001` and existing public delivery architecture. Illustrative copy is not asserted as an exact representation of an installed application.

## Evidence classification
- **SOURCE-ONLY:** the new HTML/JS and source-directory link are committed.
- **MOCK-ONLY:** stage selections and the example MIM engagement are synthetic; they do not execute ServiceNow actions.
- **DEV-VERIFIED:** none in this release.
- **PRODUCTION-VERIFIED:** none in this release.
- **Screenshot status:** no screenshots added or published.

## Controls
- No private repository content, secrets, credentials, customer records, or unapproved images included.
- Static page uses local scripts only and textContent for dynamic DOM updates.
- Licensing: public static site requires none. Runtime MIM depends on ITSM entitlement; custom workbench functions may require App Engine rights; external integration may require IntegrationHub and third-party subscriptions.

## Verification pending
- Confirm CI and GitHub Pages deployment for this commit.
- Perform browser keyboard, responsive and link checks.
- Future genuine DEV evidence requires sanitisation, provenance, and explicit approval.

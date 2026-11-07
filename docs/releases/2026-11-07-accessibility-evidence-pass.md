# Accessibility and evidence-integrity pass — 7 November 2026

## Release
Homepage commit: `ba94f984eb9c9f41fd5945d3d2e6cd58b2423914`.

## Changes
- Added keyboard-accessible skip-to-content link to main landmark.
- Strengthened visible keyboard focus across links, buttons, tabs and disclosure controls.
- Honoured reduced-motion preference, including smooth scrolling.
- Improved small-screen padding, button wrapping and overflow resilience.
- Renamed misleading screenshot navigation to guided demonstration.
- Added prominent evidence-status disclosure before main portfolio content.

## Evidence boundaries
- **Source-only:** Application feature descriptions grounded in source repositories; not runtime verification.
- **DEV-reported:** Historical testing documented by source repositories; not independently re-run during this release.
- **Mock-only:** Interactive workbench reconstructions and simulated handoff.
- **DEV-verified:** No new independent runtime verification.
- **Production-verified:** None claimed.

## Checks and blockers
Source file read and GitHub update succeeded. Browser, axe/WCAG and live GitHub Pages checks were not executed in this run; WCAG 2.2 AA compliance is **not certified**. Original screenshots are withheld pending individual privacy and release approval. No private source, instance identifiers, customer records or unreviewed images were introduced.

## Next
Run automated accessibility and responsive browser tests; inspect all public routes and assets for confidential identifiers; secure approved sanitised real application captures; build in-page visual gallery.

## Entitlements
Static GitHub Pages portfolio: none from ServiceNow. Running underlying scoped ServiceNow applications: appropriate platform access and app entitlements; ITOM, IntegrationHub spokes, analytics or AI may require additional subscriptions depending on features.

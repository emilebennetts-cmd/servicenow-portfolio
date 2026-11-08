# Publication link-audit boundary hardening — 2026-11-08

## Change
- Skip recursively discovered HTML symlinks resolving outside the publication root before opening their contents.
- Include the source page's site-relative path in missing-target and missing-fragment diagnostics.
- Add isolated regression tests for external symlink exclusion and nested-page diagnostic context.

## Provenance
- Public repository: `emilebennetts-cmd/servicenow-portfolio`.
- Source context reviewed: `emilebennetts-cmd/solution-lifecycle-studio` README and `emilebennetts-cmd/Diagnostic-Workbench2` README.
- Drive search returned client-neutral Diagnostic Workbench interactive HTML; no images or content from that private Drive material were published.

## Evidence status
- **SOURCE-ONLY**: Website validator changes and tests committed; execution in CI not confirmed in this run.
- **MOCK-ONLY**: Existing public demonstrations are illustrative.
- **DEV-VERIFIED**: No new independent ServiceNow DEV execution.
- **PRODUCTION-VERIFIED**: None claimed.

## Publication and entitlements
No customer data, private repository source, credentials, or unreviewed screenshots are included. Static GitHub Pages validation requires no ServiceNow entitlement. Runtime scoped apps require authorised instance access and relevant custom-app entitlements; ITOM, IntegrationHub, Performance Analytics, AI and external integration features may require additional subscriptions.

## Follow-up
Confirm CI run, inspect public deployment, and obtain explicit screenshot sanitisation and publication approval before exposing original application captures.

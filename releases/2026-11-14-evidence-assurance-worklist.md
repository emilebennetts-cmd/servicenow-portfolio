# Evidence Assurance Worklist — public-source release (14 November 2026)

**Release status:** SOURCE-ONLY website implementation. Native execution **NOT VERIFIED**; approval **HOLD**. This document is a provenance and engineering-release note, not a ServiceNow acceptance certificate.

## 1. The client's pain & history

A representative enterprise ServiceNow programme inherits versioned As-Built and architecture statements alongside newer source, historical DEV-reported observations, mock integration demonstrations and reference designs. A searchable evidence catalogue is valuable, but reviewers also need to see **what remains to be verified**. A historical document-reported DEV result does not validate the newer build. The scenario is illustrative; no customer-specific outcome is asserted.

## 2. The ServiceNow solution — implemented public evidence worklist

New route: [Evidence Assurance Worklist](../evidence-assurance-worklist.html).

Implemented a static, responsive, same-origin evidence review UI, reading the public verification register as its sole authoritative content source. It exposes derived register counts and next-control actions across six classifications: SOURCE-ONLY, DEV-REPORTED, MOCK-ONLY, PROPOSED, DEV-VERIFIED and PRODUCTION-VERIFIED.

Reviewers can search, filter by classification and engineering gate, page through twelve-at-a-time cards, expand source/runtime/screenshot boundaries, follow public-safe case study links and export filtered worklists as **browser-local JSON**. Every export is **UNREVIEWED / NOT VERIFIED / HOLD**, with independent native verification, production acceptance and screenshot publication approval explicitly set to false.

The register now contains **87** claims: **54 SOURCE-ONLY, 20 MOCK-ONLY, 9 PROPOSED, 4 historical DEV-REPORTED, 0 DEV-VERIFIED and 0 PRODUCTION-VERIFIED**. The new claim PUBLIC-EVIDENCE-ASSURANCE-WORKLIST-20261114 covers the source implementation and does **not** assert native runtime behaviour.

Navigation has been added to the homepage evidence directory, portfolio explorer and canonical sitemap. No images, customer material, original documents, controlled Drive URLs or private source were embedded.

## 3. Architectural best practices and testing

- OOTB-first gate: establish target release, licensing, roles/ACLs and native capabilities before proposing custom development.
- Native verification must separately identify application scope, build/version, tested instance, dated protocol, operator, witness and restricted evidence alias.
- Source-only and historical DEV-reported claims never auto-promote. Mock-only cases require approved nonproduction provider tests before any live-integration claim.
- Public JSON is checked for schema version, duplicate IDs, classification allowlist, bounded text and safe same-directory HTML paths. The UI uses textContent/DOM nodes rather than interpolating untrusted markup. Failure clears the worklist.
- Content Security Policy permits only same-origin register fetch and local inline resources. No browser storage, third-party scripts or server-side upload.
- Browser acceptance covers four viewport widths (390, 768, 1024, 1440 px), classification counts, filtering, pagination, local JSON export and corrupt-register fail-closed behaviour.
- Dedicated static test: scripts/test_evidence_assurance_worklist.py; browser test: scripts/browser_evidence_assurance_worklist.py; CI workflow: .github/workflows/evidence-assurance-worklist.yml.
- CI and Pages outcomes must be checked against the final commit; do not assume success from source creation alone.

## Licensing and entitlements

The GitHub Pages worklist requires **no ServiceNow licence**. Native tests or future implementation require authorised access and applicable App Engine/custom-application/table rights, scoped roles and ACLs; feature-specific ITSM, ITOM/Discovery, IntegrationHub, ATF, analytics, AI and third-party subscriptions may also apply. Actual entitlement rights must be checked for the target customer contract and release.

## Gates remaining open

1. Independently execute version-specific native DEV acceptance and attach dated, reviewer-attributable evidence. Prior historical read-backs remain DEV-REPORTED.
2. Establish separate change/release, UAT, operational acceptance and production evidence before any production-verification status.
3. Approve each real ServiceNow screenshot derivative individually after ownership, rights review, irreversible redaction and exact-hash approval; **0 approved originals** remain on HOLD.
4. Confirm final GitHub Actions/Pages deployment and an external GET of the live route when DNS is available.

**Security:** No repository visibility changes; no private source or sensitive screenshots published.

# Release — Offline architecture decision draft resume

**Date:** 15 November 2026 (Australia/Sydney)  
**Public page:** [Reusable Delivery Patterns — Architecture Decision Desk](../reusable-delivery-patterns-case-study.html#pattern-fit-desk)  
**Evidence classification:** website code SOURCE-ONLY; example scenario decisions MOCK-ONLY; native DEV / Production **NOT VERIFIED**.

## 1. The client's pain and history

Architecture decision workshops may span several sessions and reviewers. Previously, the desk exported JSON but could not restore its own drafts, forcing manual re-entry and increasing the risk of unchecked evidence gates. No actual client baseline or efficiency improvement is asserted.

## 2. The ServiceNow solution and public implementation

The existing three-scenario design desk now accepts its own exported JSON as a **local file**. A consultant can resume the selected Major Incident, CMDB onboarding or service-request scenario, its OOTB-first / governed pattern / scoped extension choice, and six preparation checkboxes. The recalculated status always remains a preparation state, never native or independently approved acceptance.

The import rejects malformed files, unknown or duplicate checks, unknown scenarios or approaches, extra properties, files over **16 KiB**, forged review/verification/production approval fields and modified derived status/gate counts. All fields are recomputed against the same source-controlled decision model before any UI state is changed. Invalid imports leave the existing review intact.

Accessibility and portability: visible labelled file input, descriptive live status, keyboard operability, small-screen layout, browser-local file handling. No localStorage, network requests, private Drive references or external JavaScript.

## 3. Architectural best practices and evidence boundaries

- **OOTB-first:** assess native ITSM Major Incident Management, Service Catalog/Flow Designer and CMDB IRE/Service Graph patterns before adopting a custom extension; deployment requires target-specific licensing, ACL and negative-test review.
- **Integrity:** an imported file is never attestation. Canonical fields remain `classification=mock-only`, `review_state=UNREVIEWED`, `verification_state=NOT VERIFIED`, `release_state=HOLD`; all native execution, approval, Production and screenshot assertions remain `false`.
- **Source provenance:** reviewed private Delivery and Diagnostic repositories, Delivery As-Built, Architecture and User Guides in connected Drive and a Diagnostic completion runbook. Original documents remain private. The As-Built and training documents explicitly distinguish source release 4.22.2 from installed DEV/Production proof.
- **Test coverage:** extended static structure checks and existing Playwright Chromium suite at 390, 768, 1024 and 1440 px. Roundtrip, tamper, invalid JSON, oversized file, preserved state, no external requests and false approval flags are exercised. CI and Pages status require independent read-back.
- **Publication:** no customer data, secrets, raw private application source, original screenshots or internal Drive URLs copied; screenshot release stays **0 approved / HOLD**. Public claim register stays at the prior **89** claims.

## Entitlement dependencies

Static website and browser file import need no ServiceNow subscription. Native implementation still requires licensed App Engine/custom tables where applicable, correct roles/ACLs, target ITSM/MIM and Request capability, ITOM/CMDB/IRE/Discovery or Service Graph Connectors if implemented, IntegrationHub/spoke transactions, and feature-specific ATF, Performance Analytics, AI and third-party content/connector rights, according to the customer's contract.

## Remaining acceptance

Independently witness current-version authorised DEV execution, confirm installed plugins and product rights, retain negative test and authorised release receipts, review each sanitised original image and obtain publication approval before showing real screenshots. No page interaction can close those native gates.

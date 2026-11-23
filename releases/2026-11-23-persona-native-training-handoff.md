# 23 November 2026 — Persona native training acceptance handoff

**Release classification:** SOURCE-ONLY implementation and source-based test designs; browser interactions MOCK-ONLY.  
**Native execution:** NOT RUN. **Independent UAT/role sign-off:** HOLD. **Production verified:** No. **Original screenshot publication approval:** None.

## 1. The client's pain and history

The September 2026 Training PDF references Universal Delivery Workbench source 4.6.1, whereas the controlled October DOCX Training, As-Built and Architecture editions reference source 4.22.2. Previous public comparison established edition drift and introduced five role summaries, but did not provide native positive/negative acceptance cases per persona. A matching training edition is not proof of installed scope, granted roles or completed training.

## 2. The ServiceNow solution

Extended the existing [Documentation Currency & Training Readiness Gate](../documentation-currency-gate.html#native-training-controls) rather than creating another disconnected microsite.

- **15 immutable acceptance designs**, three each for presales/account, delivery, solution architecture, test/release and platform-owner roles.
- Each design identifies expected observed behaviour, negative-path denial, a public-safe source-section crosswalk, and the relevant permission or optional product entitlement to check.
- Browser-local filter displays the selected role or the full 15-control matrix. All views are usable by keyboard and on narrow screens.
- Downloadable formula-protected CSV includes the selected historical release (4.6.1 or 4.22.2), source basis, negative-path test and five immutable status columns: SOURCE-ONLY, NOT RUN, HOLD, NOT VERIFIED and NOT AUTHORISED.
- No ServiceNow API calls, secrets, account data, unapproved screenshots or private document links are included.

## 3. Architectural best practices

Use OOTB roles, ACLs, approval separation and auditing before considering custom workarounds. Confirm the exact scoped app, installed version, generated metadata and permitted test accounts before executing a role's case. Record negative cases as explicitly as positive ones. A script CI pass or a synthetic browser demonstration is not native DEV execution, a client sign-off or production readiness.

**Controlled source classes reviewed:** October Delivery As-Built, Architecture and User Guides & Training; September Training edition; Delivery source repository; Diagnostic repository; private evidence control. Sources are not redistributed. Diagnostic sample-runbook approvals are fictional examples, not live acceptance.

### Licensing and entitlements

The public page, filters, CSV and CI require **no ServiceNow licence**. Native protocols require authorised scoped app hosting and appropriate role/ACL test identities. ITSM, CMDB, ITOM/Discovery/Service Graph, IntegrationHub/spokes, Now Assist/AI, ATF, analytics and any SecOps, IRM, CSM, HRSD or ITAM components require contractual and installed-instance checks **only where a protocol invokes that capability**. Neither source availability nor a named product automatically establishes entitlement.

### Regression and release controls

- Node contract tests cover unique IDs, five-persona allocation, immutable status, fail-closed release/persona selections, and sensitive-reference exclusion.
- Four-width Chromium test covers persona switching, 15-row HOLD CSV, negative controls, horizontal overflow and network isolation.
- Both quality and documentation-specific browser workflows explicitly run the new model tests.
- The public publication-security audit and screenshot approval gate remain unchanged.

**Release decisions remain HOLD** pending current authorised DEV package/read-back, executed role/ACL and document-output cases, independent reviewer sign-off, contractual entitlements and separate permission for each source image. No original or provisional redaction image has been published.

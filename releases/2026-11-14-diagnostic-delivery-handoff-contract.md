# Diagnostic-to-Delivery Handoff Contract — 14 November 2026

**Public page:** [Diagnostic-to-Delivery Handoff Contract](../diagnostic-delivery-handoff-contract.html)
**Architecture evidence:** SOURCE-ONLY. **Interactions:** MOCK-ONLY.
**Native current-target verification:** NOT RUN / NOT VERIFIED. **Production:** NOT VERIFIED.
**Release and screenshot status:** UNREVIEWED / HOLD.

## 1. The client's pain & history

A representative enterprise ServiceNow delivery creates operational diagnostic evidence, draft remediation findings, delivery plans and handover documents in separate contexts. Without an explicit ownership contract, a Delivery planning tool may become an unauthorised second writable finding store. Staff can then confuse an assessment proposal, source code, an older DEV test report or a mock demonstration with current target-instance acceptance.

This is an illustrative delivery risk, not a representation of a named customer's confidential operational state.

## 2. The ServiceNow solution — implemented public educational artefact

A new static, responsive architecture experience explains six contractual controls: assessment scope and permission; read-only collection and minimisation; evidence envelope validation; human-reviewed, metric-linked finding; reference-only Delivery handoff; target identity and independent release assurance.

Four interactive execution boundaries show different obligations: Tier 0 zero footprint, approved offline collection, native DEV verification, and production release. The browser-local JSON export is an unreviewed architecture checklist with mandatory false values for native_dev_verified, production_verified, screenshot_publication_approved; verification_state = NOT VERIFIED; and release_state = HOLD. Switching lanes does not execute collectors, move evidence, connect to ServiceNow or promote a claim.

This educational page is cross-linked from the Diagnostic and Delivery case studies, indexed on the homepage and added to the canonical sitemap.

## 3. Architectural best practices, evidence and tests

- **Source basis:** The Diagnostic Workbench 2 README and Knowledge Intelligence 0.1.0 README, the Universal Delivery Workbench README (4.22.2 source), and private controlled portfolio baseline read during preparation. The source describes Diagnostic ownership of operational investigation/findings and Delivery's reference-only handoff. It also documents the KI companion as separately packaged, with a historical 30 September 2026 DEV report. This is not fresh independent runtime evidence.
- **Version/identity firewall:** Original source scopes and later demo generations must not be conflated. A native acceptance receipt must name actual instance, installed app identity, scope, version, actor, test date, outcome and independent witness.
- **Privacy / publication:** Source references only; no customer records, original image pixels, tokens, endpoints, real hostnames, screenshot reuse rights or private repository code are published. The CSP forbids images, remote connections, forms, embedded objects and frames; no local persistence.
- **Testing:** scripts/browser_diagnostic_handoff_contract.py checks four viewports (390, 768, 1024, 1440 pixels), four boundary lanes, conservative classification and status, JSON flags, reset, horizontal overflow and browser errors. CI workflow: .github/workflows/diagnostic-handoff-contract.yml. Static assertions require conservative labels and no image elements, storage or network fetches. CI success is website acceptance only.
- **No evidence promotion:** The canonical public claim register remains at 87 entries. Neither architecture nor synthetic controls create a new independently DEV-VERIFIED or PRODUCTION-VERIFIED record. Screenshot approvals remain at zero.

### Licensing and entitlements

The public website requires no ServiceNow licence. Actual native implementation requires App Engine/custom-app/custom-table rights and scope permissions, plus roles and ACLs. Feature use may require ITSM, ITOM/Discovery, IntegrationHub/spokes, ATF, analytics, AI or third-party content/provider subscriptions. Collectors may require approved non-production access and security/change authorisation. Nothing here implies that base subscriptions include optional features.

### Approval and verification gates still open

- Authorised current-target native DEV execution and negative tests
- Independently reviewed operational findings, versioned references and target identity
- Customer business, technical and support sign-off and production change approval
- Explicit image-by-image rights review, irreversible redaction and approval of the exact final derivative

**Release statement:** Static source-backed portfolio implementation only. Check CI workflow and GitHub Pages against final commit before asserting live delivery.

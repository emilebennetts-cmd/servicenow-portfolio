# Screenshot render-path ambiguity guard — 16 November 2026

**Public security control: SOURCE-ONLY implementation; MOCK-ONLY regression fixtures. No native ServiceNow DEV/Production verification. Screenshot approvals remain HOLD (zero).**

## 1. Client pain and history
The public portfolio already required byte-bound approval for conventional screenshots, responsive images, social previews and image preloads. Two additional HTML/CSS constructs remained ambiguous: browser CSS image-source selection could reference image pixels through a quoted value without a conventional URL function; duplicate image-control attributes could be resolved differently by an HTML parser and a browser. Neither observation is evidence that confidential images were disclosed.

## 2. ServiceNow solution
The publication checker now denies CSS image-source selection constructs until an explicit approved-image-aware implementation exists. It also inspects **all original type/rel/as attributes** on image-type inputs and preloaded image links instead of collapsing them into a dictionary, and blocks conflicting duplicate attributes.

Five new synthetic regression cases exercise both CSS forms, ambiguous image inputs, ambiguous preload links, and ordinary gradients/text inputs that must still pass. The public Screenshot Publication Gate describes the added controls.

## 3. Architectural best practice, evidence and licensing
- No customer source, screenshots, raw private documents, credentials, or instance identifiers were included.
- This is a fail-closed heuristic publication guard, not pixel-level sanitisation or owner approval.
- SOURCE-ONLY: publication checker and public explanation. MOCK-ONLY: synthetic test fixtures.
- Historical instance claims remain DEV-REPORTED. **New DEV-VERIFIED = 0; PRODUCTION-VERIFIED = 0; actual screenshot approvals = 0.**
- Publication requires separate provenance, redaction, derivative hash and publication-rights confirmation for every candidate.
- No ServiceNow licence is necessary for static GitHub Pages or this Python checker. Native Workbench deployment and acceptance depend on target custom scoped-application/App Engine and table entitlements, roles/ACLs, applicable ITSM/ITOM subscriptions and separately confirmed IntegrationHub, ATF, AI, analytics and provider-specific rights.

## Verification
New regressions are committed into the existing source-quality CI suite. Workflow outcome must be checked for the exact commit; a passing test cannot establish native acceptance or external HTTPS availability.

## Source boundaries
The Delivery and Diagnostic private repositories and connected Drive As-Built and Diagnostic documents were searched for context only. No private text or image was replicated to the public website.

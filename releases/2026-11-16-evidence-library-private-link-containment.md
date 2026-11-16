# Public evidence library — private-link containment and version boundary

**Date:** 16 November 2026  
**Area:** Public evidence library, review navigation and controlled source traceability  
**Classification:** SOURCE-ONLY website change; MOCK-ONLY illustrated walkthroughs; all native acceptance HOLD  
**Publication:** No images added, no private repository settings changed

## 1. Client pain and history

The public `evidence.html` source index linked directly to controlled Google Drive PDFs and screenshot candidates. An anonymous visitor could not reliably use those destinations, and even a sign-in prompt created a confusing experience. It also conflated source documentation with the current operational state and provided no clear summary of what historical DEV observations could prove.

## 2. ServiceNow portfolio solution

Rebuilt `evidence.html` as an accessible, responsive source-summary hub with no external Drive, restricted GitHub or instance links. It contains:

- Three source-document summaries: As-Built, Architecture, User Guides & Training (all controlled draft dated 30 September 2026).
- Separate Diagnostic base collector and Knowledge Intelligence companion boundaries, with public case-study navigation.
- A dated Delivery baseline sequence: documented DEV 4.5.1 on 30 September, later DEV 4.20.0 reported in source README on 5 October, and current README source version 4.22.2 on 16 November.
- Explicit SOURCE-ONLY, historical DEV-reported/verified, MOCK-ONLY and PRODUCTION-VERIFIED claim interpretation; no later source inherits earlier DEV validation.
- A four-step native acceptance pathway and visual-evidence reviewer guidance. All original screenshots remain withheld.
- No JavaScript, raw image assets, credential requests or browser storage.

The existing `visual-evidence.html` contains the reviewed text-only visual cards and is reused rather than duplicating or publishing unapproved captures.

## 3. Architecture and control evidence

The control is deliberately platform-agnostic HTML/CSS with zero external runtime dependencies. Root navigation is supported at narrow mobile widths, reduced-motion users and keyboard-only use.

`scripts/test_evidence_library_public_boundary.py` is discovered by the existing Python quality workflow and checks relative link targets, local fragments, evidence tiers, explicit screenshot holds and absence of private routes and media elements.

### Source reconciliation

- Connected Drive: `01-Universal-Delivery-Workbench-Solution-As-Built.pdf`, `02-Universal-Delivery-Workbench-Architecture.pdf`, `03-Universal-Delivery-Workbench-User-Guides-and-Training.pdf` (all dated 30 September 2026, controlled drafts).
- Private Delivery source repository README: source version 4.22.2; historical 4.20.0 DEV report retained with its date.
- Private Diagnostic repository README: separate `x_1577958_dw2` source and KI companion boundaries.
- The public visual gallery and screenshot approval manifest remain authoritative for release gating.

**Verification at authoring:** Source files committed through GitHub; automated CI and live public Pages confirmation must be checked separately. No native instance login, installed-version read-back or test execution was performed in this release. Production verification 0. Genuine screenshot approvals 0.

## Licence and entitlement boundaries

Static GitHub Pages content requires no ServiceNow licence. Native delivery/diagnostics need approved scoped-app hosting rights, platform permissions, segregation-of-duties review and contract-specific checks for applicable ITSM, ITOM/Discovery, Service Graph Connectors, Service Mapping, SecOps, IRM, CSM, HRSD, ITAM, IntegrationHub, analytics, AI and external provider services.

## Pending authority

Only an authorised DEV read-back can establish currently installed runtime functionality. Private originals and screenshot derivatives require independent source, privacy and image-specific publication approval before public release.

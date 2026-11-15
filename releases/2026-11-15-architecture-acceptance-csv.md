# Architecture decisions — offline acceptance CSV (15 November 2026)

## 1. The client's pain & history
Source-backed architecture trade-offs lacked a directly reusable worklist. Manual transcription could omit a native gate or confuse a source-only design with accepted ServiceNow functionality.

## 2. The ServiceNow solution
Implemented **Export visible acceptance gates (CSV)** on `architecture-decision-register.html`. The browser exports only the decisions currently matching domain/search filters to Excel-compatible UTF-8 CSV. It preserves decision ID, domain, rationale, risk and native acceptance gate and adds immutable evidence boundary fields.

Every output row is `SOURCE-ONLY / NOT RUN / dev_verified=false / production_verified=false / HOLD`. The CSV contains no search terms, private repository paths, instance identity or user values. It uses quote escaping and spreadsheet formula-prefix neutralisation and never calls the network or browser storage.

## 3. Architectural best practices & verification
The export is a review preparation tool and cannot approve architecture or establish a DEV/Production verification state. The Diagnostic finding boundary, Delivery execution boundary, OOTB-first architecture and role/ACL acceptance requirements still require authorised native tests.

Added source-level contract tests and a Playwright regression script at 390/768/1024/1440 pixels, covering eight rows, filtered rows, no-match disable, secure hold fields, download correctness and zero external requests. Focused GitHub Actions workflow: `.github/workflows/architecture-decision-export-browser.yml`. Record outcomes only after workflow completion.

Reviewed Delivery and Diagnostic source repositories and private provenance. Located controlled Drive As-Built, Architecture, Training and completion runbooks; content is not reproduced into the public asset. No customer data or original screenshots published. Original screenshot approvals: **0 / HOLD**.

## Licensing and open gates
Static publication and offline worksheet: **no ServiceNow licence**. Native deployment and testing may require authorised ServiceNow instance access, custom app/App Engine rights, roles/ACLs and subscribed ITSM/ITOM/CMDB features; assess IntegrationHub, ATF, analytics, Now Assist/AI and third-party API entitlements separately. No customer-specific commercial licence was verified.

Independent DEV acceptance, Production approval, signed ADR review, trusted package manifest and per-image screenshot approvals remain outstanding.

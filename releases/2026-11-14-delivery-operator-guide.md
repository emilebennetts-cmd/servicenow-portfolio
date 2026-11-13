# Delivery Workbench — source-traced persona operations guide

**Release date:** 14 November 2026 (Australia/Sydney)  
**Public implementation:** [Delivery case study](../delivery-case-study.html#persona-operations)  
**Evidence status:** SOURCE-ONLY (documented operating procedures) and pre-existing MOCK-ONLY (Delivery Plan simulator). No current DEV-VERIFIED or PRODUCTION-VERIFIED claims.

## Client pain and history

Training artefacts, source releases and historical DEV read-back can appear interchangeable during architectural review. A successful build or synthetic demonstration can be mistaken for evidence of a functioning installed application. A controlled 19 October 2026 training pack expressly requires fresh instance read-back and screenshot review.

## Delivered solution

- Implemented twelve role-filterable, accessible **read-only** procedure cards corresponding to the controlled Universal Delivery Workbench User Guides and Training sections 4.1–4.12. Nine practitioner role filters expose role-specific prerequisites, expected evidence, and governing controls, including consent and read-only scanning, AI decisions, separation of duties, native release preview and operational acceptance.
- Added in-browser *read* checkmarks, clearing controls and local plain-text rehearsal export. The export permanently declares `NOT RUN | HOLD`, `production_verified=false`, `screenshot_approved=false`. It is **not** an approval, test result, deployment, or ServiceNow-generated record.
- Retained the existing eight-view synthetic Delivery Plan lab and its MOCK-ONLY status. Page now legitimately carries **MIXED CLAIMS** across distinct source-only and synthetic parts, reconciled in the public evidence register and Portfolio Explorer.
- Added six offline Python source/publication contracts; extended four-width Playwright browser checks to verify role filtering, checkmarks, clearing, export status and no network calls. Existing CI includes both the quality suite and browser script.

## Source and claim lineage

- Controlled Delivery User Guides & Training: **19 October 2026 evidence cutoff**, source-described release **4.22.2**; 12 procedures are paraphrased, not reproduced.
- Controlled Delivery As-Built: 4.22.2 source identity recorded separately from historical 6 October Delivery 4.22.2/Diagnostic 0.4.2 DEV read-back. **DEV-REPORTED** status is not new independent runtime validation.
- Private Delivery and Diagnostic repositories were read to confirm product boundaries. The current repository HEAD or a later branch must not be silently equated with the historical training snapshot.
- Fictional DemoClient23 Diagnostic closure runbook was reviewed only for safe workflow boundaries; it is showcase planning, not customer approval or Production execution.
- No private Drive URL, source content, table dump, credentials, customer-specific identity or screenshot pixel was copied into the public site.

## OOTB-first and licensing

The public static page requires **no ServiceNow licence**. Native implementation may require App Engine/custom-table rights, scoped roles and engagement ACL/membership, approved ITSM/Change capabilities, ITOM or integration collection rights, IntegrationHub/connection aliases, licensing for AI-provider functionality and platform-generated documents, and permitted target-instance access. Contracted rights, roles and spokes must be checked independently. Native update-set preview, read-back, ATF/role tests, security/privacy review, support acceptance and production change authorisation remain gates.

## Verification and publication gates

This release establishes a source-backed website interaction only. A passing browser test certifies no ServiceNow functionality. A live demonstration requires an authorised instance with pinned source/version, read-back, least-privilege persona tests, visual reinspection and independently attributable receipts. Genuine Workbench screenshots remain **HOLD — none approved**. No private repository visibility changed.

## Files and quality gates

- `delivery-case-study.html` — twelve static accessible procedure cards, role filtering and local receipt generation.
- `scripts/test_persona_operating_guide.py` — six offline structural and safety tests.
- `scripts/browser_delivery_plan_lab.py` — four-width interactive regression including new role filter and HOLD export.
- `evidence/public-verification-register.json` — one additional source-only claim.
- `portfolio-explorer.html` — mixed evidence classification.
- `RELEASE_LOG.md` — auditable dated entry.

**CI status:** Check workflow runs for the final release commit; no DEV/Production native execution or external live-site retrieval is implied.

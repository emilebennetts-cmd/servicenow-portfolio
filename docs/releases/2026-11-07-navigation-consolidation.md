# Portfolio navigation and privacy consolidation — 7 November 2026

## Implemented
- Replaced the homepage's evidence navigation with its in-page evidence library anchor.
- Redirected mobile menu entries for release history, diagnostic engineering, evidence lifecycle, patterns, verification and screenshot evidence to existing homepage sections.
- Replaced the homepage's cross-page synthetic walkthrough CTA with its in-page connected-delivery section.
- Removed outbound Google Drive screenshot buttons from the homepage. Original screenshots are not public and must not be published without review.
- Removed publicly rendered application scope identifiers from the homepage.

## Verification boundary
Source-only change committed to the public repository. GitHub Pages deployment, browser operation and WCAG compliance have not been independently re-tested in this increment. The visual demonstration remains illustrative/mock-only. No new DEV or production verification is claimed.

## Remaining gaps
1. Audit every other public HTML file for private instance identifiers, names and externally linked evidence.
2. Create a first-party gallery using only approved, sanitised screenshots or labelled synthetic screens.
3. Consolidate duplicated homepage content and perform mobile, keyboard and performance checks.
4. Verify GitHub Pages deployment and fix any broken section anchors.

## Licensing
Static HTML/CSS/JavaScript portfolio: no ServiceNow licence. Running the ServiceNow scoped applications requires authorised instance access and relevant application/platform entitlements. IntegrationHub spokes, ITOM and optional AI/analytics products may require separate subscriptions.

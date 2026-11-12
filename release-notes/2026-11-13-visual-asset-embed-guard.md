# Visual-asset embed bypass protection — 13 November 2026

**Change type:** Public CI publication safety; SOURCE-ONLY. **Runtime status:** Not a ServiceNow instance test.

## Why this exists
The existing public asset gate required SHA-256 approval for individual raster files, but a screenshot could bypass that control if placed inside an HTML/CSS/JS/SVG data URL, a remote image element, or an SVG image/foreignObject. This release closes those common publication paths. A vector illustration is allowed only if it does not use these prohibited payloads. Review of what a vector diagram depicts is still a human responsibility.

## Implemented
- Reject common raster image data URLs in checked public HTML, Markdown, SVG, JS, JSON and styles.
- Reject remote HTML image/picture sources, remote CSS background images, inline SVG external references and SVG image elements, foreignObject, scripts and remote references.
- Preserve existing approval-by-hash rules for actual screenshot files.
- Add nine regression cases, including safe vector diagrams and external web-font stylesheets.
- Keep original screenshot candidates on HOLD. This release publishes **no** screenshot bytes and changes no repository visibility.

## Scope and limits
Static matching cannot detect deliberately obfuscated JavaScript, third-party content at runtime, or all sensitive content inside vector paths. A passing CI gate is not evidence of image approval, native DEV execution, ServiceNow deployment or production validation. The final redacted image still requires individual visual inspection and explicit owner approval with a private evidence record.

## Entitlements
This static security gate and public portfolio require **no ServiceNow licence**. Native scoped application verification requires authorised App Engine/custom table rights and roles; ITSM, ITOM/Discovery, IntegrationHub, AI and other product entitlements depend on what is installed.

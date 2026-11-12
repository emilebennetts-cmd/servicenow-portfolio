# Release: Complete public sitemap coverage and drift gate

**Date:** 13 November 2026 (Australia/Sydney)  
**Public classification:** SOURCE-ONLY infrastructure improvement  
**Runtime claim:** No newly DEV-VERIFIED or PRODUCTION-VERIFIED ServiceNow execution  
**Original screenshot publication:** 0 approved; existing publication HOLD unchanged

## 1. The client's pain and history

The website's searchable Portfolio Explorer covered 69 case-study/reference pages in addition to the Explorer itself (70 root HTML files), but the published `sitemap.xml` listed only 36 URLs. This created discoverability inconsistency and a recurring manual maintenance risk whenever the growing portfolio gained a new page. The existing sitemap validator checked whether declared targets existed but not whether *all* published pages were declared.

## 2. Implemented solution

- Rebuilt the public `sitemap.xml` with 70 canonical project-site URLs: homepage + all 69 other existing root HTML pages. **34 already-published pages were missing** before this repair.
- Added dependency-free `scripts/generate_sitemap.py` with `--write` authoring and `--check` CI modes.
- Enforced a deterministic alphabetic listing with the homepage first and no network, credentials, private-source discovery or screenshots.
- Excluded non-root files and symlinks from the page inventory; nested documentation files and restricted evidence are not traversed.
- Added `tests/test_sitemap_generator.py` for completeness, stable ordering, duplicate resistance, symlink exclusion and missing-index failure.
- Enforced `--check` in the source quality gate and site-audit workflows, so the next public HTML addition cannot silently leave the sitemap stale.

## 3. Architectural and publication best practices

The generator indexes **only files already publicly published** at the root of the static site. It is not a ServiceNow runtime integration, screenshot-publishing tool or permission authority. The HTML source and browser-local laboratories retain their existing evidence classifications; success of sitemap tests does not promote any claim to independently DEV-VERIFIED or PRODUCTION-VERIFIED.

No ServiceNow licence is needed for GitHub Pages, XML sitemaps or offline Python checks. Native Workbench functionality independently depends on appropriate App Engine/custom application and table rights, roles/ACLs, ITSM/ITOM/IntegrationHub/AI/analytics and any third-party provider entitlements where applicable.

## Quality receipts

- Root HTML inventory observed: **70**.
- Old sitemap URL count: **36**.
- Newly included existing public pages: **34**.
- New coverage test and both CI workflow checks committed; confirm final quality/deployment run receipts against the exact release SHA before marking green.
- Original images, private Drive pointers, customer content and source-only repositories were not made public.

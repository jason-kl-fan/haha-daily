# Learnings

Append structured entries:
- LRN-YYYYMMDD-XXX for corrections / best practices / knowledge gaps
- Include summary, details, suggested action, metadata, and status


## [LRN-20260315-001] best_practice

**Logged**: 2026-03-15T16:46:04.008Z
**Priority**: medium
**Status**: pending
**Area**: docs

### Summary
For plain static GitHub Pages sites on legacy builds, adding .nojekyll can avoid opaque Page build failures.

### Details
Observed a GitHub Pages repo serving static HTML with Pages status=errored and generic 'Page build failed.' No Jekyll config was needed; adding .nojekyll is a minimal, design-preserving fix to bypass Jekyll processing.

### Suggested Action
When a static Pages site shows generic build failures under legacy build_type, check for and add .nojekyll before attempting broader changes.

### Metadata
- Source: memory-lancedb-pro/self_improvement_log
---


## [LRN-20260317-001] best_practice

**Logged**: 2026-03-17T16:40:39.108Z
**Priority**: high
**Status**: pending
**Area**: docs

### Summary
首頁入口曾誤指向單一主題頁，需把每日首頁日期同步列為固定檢查

### Details
使用者指出首頁入口仍停在舊日期。檢查後發現根目錄 index.html 與 2026-03-17/index.html 都被寫成單一主題頁，而不是當日總覽頁。已修正首頁與日期頁，並記錄規則。

### Suggested Action
每日發布後固定檢查：根目錄首頁日期、當日日期頁、主題捷徑是否都同步到同一天且指向總覽頁。

### Metadata
- Source: memory-lancedb-pro/self_improvement_log
---


## [LRN-20260318-001] best_practice

**Logged**: 2026-03-18T21:16:57.191Z
**Priority**: high
**Status**: pending
**Area**: docs

### Summary
Live-site verification and Pages build status are mandatory parts of publishing the news site.

### Details
A successful local rebuild is insufficient for a GitHub Pages-backed site. Publishing completion must include live URL checks and workflow/build confirmation. Broken gitlinks/submodule entries can silently block Pages deployment even when local files are correct.

### Suggested Action
Add a publish checklist to workspace rules: rebuild, commit, push, verify Pages run success, verify live homepage date, live today page, live broken page, and live saved page before reporting success.

### Metadata
- Source: memory-lancedb-pro/self_improvement_log
---

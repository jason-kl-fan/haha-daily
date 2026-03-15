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

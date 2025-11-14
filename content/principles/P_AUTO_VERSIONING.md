---
id: P_AUTO_VERSIONING
title: Automated Semantic Versioning
category: project-specific
severity: medium
weight: 9
enforcement: "RECOMMENDED - Team-dependent (solo: auto, teams: PR-based, large org: manual)"
applicability:
  project_types: ['library', 'api_backend', 'cli_tool', 'framework']
  languages: ['all']
---

# P_AUTO_VERSIONING: Automated Semantic Versioning 🟡

**Severity**: Medium

Automatically bump version based on conventional commit type following Semantic Versioning (SemVer). Version bumps are determined by commit message prefix: feat: → MINOR, fix: → PATCH, feat!/BREAKING CHANGE: → MAJOR.

**Why**: Eliminates manual versioning errors and ensures consistent version history aligned with actual changes

**Enforcement**: RECOMMENDED - Team-dependent (solo: auto, teams: PR-based, large org: manual)

**Project Types**: library, api_backend, cli_tool, framework
**Languages**: all

**Rules**:
- **Commit Type To Version Mapping**: feat: commits bump MINOR version (1.2.0 → 1.3.0), fix: commits bump PATCH (1.2.0 → 1.2.1), feat!/BREAKING CHANGE: bump MAJOR (1.2.0 → 2.0.0)
- **Version File Update**: Automatically update version in all relevant files (pyproject.toml, package.json, __init__.py, etc.)
- **Git Tag Creation**: Optionally create git tag (v1.2.3) for new version
- **Team Awareness**: Strategy varies by team: solo dev (auto on commit), small team (PR approval), large org (manual release)

**❌ Bad**:
```
# Inconsistent versioning
1.2.0 → 1.2.5 (random jump)
1.2.5 → 1.4.0 (skipped 1.3.x)
1.4.0 → 2.0.0 (no BREAKING CHANGE marker)
# Wrong bump type
feat(api): add field → 1.2.0 → 1.2.1 (should be MINOR)
fix(bug): patch → 1.2.0 → 1.3.0 (should be PATCH)
```

**✅ Good**:
```
# Solo dev - automatic
git commit -m "feat(api): add user registration"
→ Version auto-bumps: 1.2.0 → 1.3.0
→ pyproject.toml updated
→ Git tag v1.3.0 created
# Small team - PR-based
PR: feat(auth): add JWT refresh tokens
→ Reviewer confirms MINOR bump
→ On merge: version bumps 1.2.0 → 1.3.0
# Large org - manual
Release manager reviews sprint commits
→ Manually bumps version for release
→ Creates release branch
→ Merges to main with tag
```

**Related**: P047, U_ATOMIC_COMMITS, U_CONCISE_COMMITS

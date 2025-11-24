---
name: cco-skill-versioning-semver-changelog-compat
description: Versioning, releases, changelogs, backward compatibility
keywords: [versioning, semver, version, major, minor, patch, release, breaking changes, changelog, deprecation, git, releases, conventional commits]
category: infrastructure
related_commands:
  action_types: [audit, fix, generate]
  categories: [infrastructure]
pain_points: [5]
---

# Skill: Versioning - SemVer, Changelog & Backward Compatibility

## Purpose

Prevent breaking changes through semantic versioning and deprecation.

**Solves**: Breaking changes without warning (40%+ outages), SemVer violations, missing changelogs

**Impact**: High
---

## Standard Structure

**This skill follows [STANDARDS_SKILLS.md](../STANDARDS_SKILLS.md):**

- **Standard sections** - Domain, Purpose, Core Techniques, Anti-Patterns, Checklist
- **Code example format** - Bad/Good pattern with specific examples
- **Detection pattern format** - Python functions with Finding objects
- **Checklist format** - Specific, verifiable items

**See STANDARDS_SKILLS.md for format details. Only skill-specific content is documented below.**

---

## Principles

- **P_SEMANTIC_VERSIONING** - MAJOR.MINOR.PATCH compatibility
- **P_CHANGELOG_MAINTENANCE** - Keep a Changelog format
- **P_NO_BACKWARD_COMPAT_DEBT** - 6mo+ deprecation periods
- **P_AUTO_VERSIONING** - Conventional commits → auto version
- **P_GIT_COMMIT_QUALITY** - @content/principles/P_GIT_COMMIT_QUALITY.md

## Activation

**Keywords**: version, release, changelog, semver, breaking, deprecation
**Files**: VERSION, CHANGELOG.md, .releaserc.json

## Command Discovery Protocol

When this skill is active, find relevant commands by searching `~/.claude/commands/` metadata:

```yaml
# Search criteria for this skill's domain
action_types: [audit, fix, generate]
keywords: [versioning, semver, changelog, git, releases, breaking changes, deprecation]
category: infrastructure
pain_points: [5]
```

**How Claude finds commands:**
1. Grep command files for `keywords:.*version|changelog|semver` in frontmatter
2. Match `category: infrastructure`
3. Present matching commands with their parameters

This ensures commands are always current even when renamed or updated.

## Related Skills

- **cco-skill-cicd-gates-deployment-automation**
- **cco-skill-git-branching-pr-review**
- **cco-skill-api-rest-versioning-security**

---

## Examples

### SemVer Rules
```
1.0.0 → 1.0.1  # PATCH (bug fix)
1.0.1 → 1.1.0  # MINOR (new feature)
1.1.0 → 2.0.0  # MAJOR (breaking)
```

### Changelog (Keep a Changelog)
```markdown
## [Unreleased]
### Added
- OAuth2 support

## [2.0.0] - 2025-01-15
### Changed
- **BREAKING:** Renamed `getUserById` → `fetchUser`
### Deprecated
- `old_api()` removed in v3.0.0
```

### Backward Compat (Alias)
```python
def fetch_user(user_id: int) -> User:
    return db.query(User).get(user_id)

def getUserById(user_id: int) -> User:
    """DEPRECATED: Use fetch_user(). v3.0.0"""
    warnings.warn("getUserById deprecated", DeprecationWarning)
    return fetch_user(user_id)
```

### Conventional Commits
```
feat: → MINOR | fix: → PATCH | BREAKING: → MAJOR
```

### Deprecation
```python
# v2.0: Deprecate
@deprecated(version="2.0.0")
def old_fn():
    warnings.warn("old_fn deprecated", DeprecationWarning)
    return new_fn()
# v3.0: Remove (6mo later)
```

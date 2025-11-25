---
name: cco-skill-versioning
description: Versioning, releases, changelogs, backward compatibility
keywords: [versioning, semver, version, major, minor, patch, release, breaking changes, changelog, deprecation, git, releases, conventional commits]
category: infrastructure
related_commands:
  action_types: [audit, fix, generate]
  categories: [infrastructure]
pain_points: [5]
---

# Skill: Versioning - SemVer, Changelog & Backward Compatibility

> **Standards:** Format defined in [cco-standards.md](../cco-standards.md)  
> **Discovery:** See [cco-standards.md](../cco-standards.md#18-command-discovery-protocol)


## Purpose

Prevent breaking changes through semantic versioning and deprecation.

**Solves**: Breaking changes without warning (40%+ outages), SemVer violations, missing changelogs

**Impact**: High
---

---

## Guidance Areas

- **Semantic Versioning** - MAJOR.MINOR.PATCH compatibility
- **Changelog Maintenance** - Keep a Changelog format
- **Backward Compatibility** - 6mo+ deprecation periods
- **Auto Versioning** - Conventional commits → auto version
- **Git Commit Quality** - Quality commits enable deployment tracking

## Activation

**Keywords**: version, release, changelog, semver, breaking, deprecation
**Files**: VERSION, CHANGELOG.md, .releaserc.json

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

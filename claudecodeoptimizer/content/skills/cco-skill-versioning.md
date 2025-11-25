---
name: cco-skill-versioning
description: Versioning, releases, changelogs, backward compatibility
keywords: [versioning, semver, version, major, minor, patch, release, breaking changes, changelog, deprecation, git, releases, conventional commits]
category: infrastructure
related_commands:
  action_types: [audit, fix, generate]
  categories: [infrastructure]
pain_points: [6]
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

---

## Breaking Change Detection

### What Constitutes a Breaking Change?

| Change Type | Breaking? | SemVer |
|-------------|-----------|--------|
| Remove public function | ✅ Yes | MAJOR |
| Change function signature | ✅ Yes | MAJOR |
| Change return type | ✅ Yes | MAJOR |
| Add required parameter | ✅ Yes | MAJOR |
| Rename public method | ✅ Yes | MAJOR |
| Add optional parameter | ❌ No | MINOR |
| Add new function | ❌ No | MINOR |
| Fix bug | ❌ No | PATCH |
| Performance improvement | ❌ No | PATCH |

### Automated Detection

```bash
# Python: API changes via ast-grep or semgrep
semgrep --config p/python-breaking-changes .

# TypeScript: API extractor
api-extractor run --local

# Go: go-apidiff
go-apidiff -base main -head HEAD
```

### Safe Migration Pattern

```python
# v1.0: Original API
def get_user(id: int) -> User:
    return db.get(id)

# v2.0: Add optional parameter (non-breaking)
def get_user(id: int, include_deleted: bool = False) -> User:
    query = db.query(User).filter(User.id == id)
    if not include_deleted:
        query = query.filter(User.deleted == False)
    return query.first()

# v3.0: Breaking change - use new function + deprecate old
def get_user_by_id(id: int, options: GetUserOptions = None) -> User:
    """New API with options object."""
    ...

@deprecated("Use get_user_by_id(). Removed in v4.0")
def get_user(id: int, include_deleted: bool = False) -> User:
    """DEPRECATED: Use get_user_by_id instead."""
    return get_user_by_id(id, GetUserOptions(include_deleted=include_deleted))
```

---

## Changelog Automation

### Conventional Commits → Changelog

```bash
# Install standard-version (Node.js)
npm install -g standard-version

# Generate changelog and bump version
standard-version

# Or specific bump
standard-version --release-as minor
```

**Generated CHANGELOG.md:**
```markdown
# Changelog

## [2.1.0] - 2025-01-20

### Features
* add OAuth2 support ([#123](link))
* implement rate limiting

### Bug Fixes
* fix null pointer in user service ([#456](link))

### BREAKING CHANGES
* renamed `getUserById` to `fetchUser`
```

### Python: commitizen

```bash
# Install
pip install commitizen

# Interactive commit
cz commit

# Bump version + changelog
cz bump --changelog
```

### Git Tags

```bash
# Create annotated tag
git tag -a v2.1.0 -m "Release v2.1.0: OAuth2 support"

# Push tag
git push origin v2.1.0

# List tags
git tag -l "v2.*"
```

---

## Deprecation Lifecycle

```
v1.0 ──────────────────────────────────────────────
       │
v2.0   ├─ DEPRECATE: Add warnings, document migration
       │  - @deprecated decorator
       │  - Runtime warnings
       │  - Documentation update
       │  - Migration guide
       │
       │  (Minimum 6 months, 2 major versions)
       │
v3.0   └─ REMOVE: Delete deprecated code
          - Remove from codebase
          - Update documentation
          - Release notes
```

### Deprecation Decorator

```python
import warnings
from functools import wraps

def deprecated(version: str, alternative: str = None):
    """Mark function as deprecated."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            msg = f"{func.__name__} is deprecated since v{version}."
            if alternative:
                msg += f" Use {alternative} instead."
            warnings.warn(msg, DeprecationWarning, stacklevel=2)
            return func(*args, **kwargs)
        return wrapper
    return decorator

# Usage
@deprecated(version="2.0.0", alternative="fetch_user()")
def get_user_by_id(user_id: int):
    return fetch_user(user_id)
```

### TypeScript Deprecation

```typescript
/**
 * @deprecated Use `fetchUser()` instead. Will be removed in v3.0.
 */
function getUserById(id: number): User {
    console.warn('getUserById is deprecated. Use fetchUser().');
    return fetchUser(id);
}
```

---

## API Versioning Strategies

### URL Path Versioning

```
/api/v1/users
/api/v2/users
```

**Pros**: Clear, easy routing
**Cons**: URL changes, cache invalidation

### Header Versioning

```http
GET /api/users
Accept: application/vnd.myapi.v2+json
```

**Pros**: Clean URLs
**Cons**: Less discoverable

### Query Parameter

```
/api/users?version=2
```

**Pros**: Simple implementation
**Cons**: Can be accidentally omitted

### Recommendation

**Start with URL versioning** (most common, easiest):

```python
# FastAPI example
from fastapi import APIRouter

v1_router = APIRouter(prefix="/api/v1")
v2_router = APIRouter(prefix="/api/v2")

@v1_router.get("/users/{id}")
def get_user_v1(id: int):
    return {"id": id, "name": "Alice"}  # v1 format

@v2_router.get("/users/{id}")
def get_user_v2(id: int):
    return {"user": {"id": id, "name": "Alice"}}  # v2 format
```

---

## Anti-Patterns

### ❌ Version in Filename

```python
# ❌ BAD: version in filename
from utils_v2 import helper
from models_v3 import User

# ✅ GOOD: Use package versions
from myapp.utils import helper  # Package version controls API
```

### ❌ No Deprecation Period

```python
# ❌ BAD: Remove without warning
# v1.0: def get_user(id) exists
# v2.0: get_user() deleted, breaks all consumers!

# ✅ GOOD: Deprecation period
# v1.0: get_user() works
# v2.0: get_user() deprecated with warnings
# v3.0: get_user() removed (6+ months later)
```

### ❌ Breaking Changes in PATCH

```python
# ❌ BAD: Breaking change in patch version
# 1.2.3 → 1.2.4 (removed required parameter)

# ✅ GOOD: Breaking changes = MAJOR
# 1.2.3 → 2.0.0 (removed required parameter)
```

### ❌ Silent Breaking Changes

```python
# ❌ BAD: Behavior change without version bump
def calculate_tax(amount):
    return amount * 0.10  # Was 0.08, changed silently!

# ✅ GOOD: Document and version
# CHANGELOG: v2.0.0 - BREAKING: Tax rate changed from 8% to 10%
def calculate_tax(amount, rate=0.10):
    return amount * rate
```

---

## Checklist

### Before Release
- [ ] Version follows SemVer (MAJOR.MINOR.PATCH)
- [ ] CHANGELOG.md updated
- [ ] Breaking changes documented
- [ ] Deprecations have warnings + docs
- [ ] Migration guide for breaking changes

### Deprecation
- [ ] @deprecated decorator applied
- [ ] Runtime warning emitted
- [ ] Alternative documented
- [ ] Minimum 6 months / 2 major versions before removal
- [ ] Removal date announced

### Release
- [ ] Git tag created (v2.1.0)
- [ ] Release notes published
- [ ] Package published (PyPI, npm, etc.)
- [ ] Documentation updated

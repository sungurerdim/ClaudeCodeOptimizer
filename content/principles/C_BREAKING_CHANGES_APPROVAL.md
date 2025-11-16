---
id: C_BREAKING_CHANGES_APPROVAL
title: Breaking Changes Need Approval
category: claude-guidelines
severity: critical
weight: 10
applicability:
  project_types: ['all']
  languages: ['all']
---

# C_BREAKING_CHANGES_APPROVAL: Breaking Changes Need Approval 🔴

**Severity**: Critical

Never make breaking changes without explicit user approval. Always identify, document, and propose breaking changes with migration path before implementation. Breaking changes affect existing functionality and require careful coordination.

**Enforcement**: MUST

**Project Types**: all
**Languages**: all

---

## Why

### The Problem

**Breaking changes without approval create system-wide failures:**

- **Production Outages** - Breaking changes can immediately crash production systems relying on existing APIs
- **Cascade Failures** - One breaking change can break multiple dependent systems downstream
- **Data Loss Risk** - Schema changes or format modifications can corrupt or lose existing data
- **Team Disruption** - Breaks other developers' work without warning or coordination
- **Rollback Complexity** - Breaking changes are hard to roll back cleanly once deployed
- **Trust Erosion** - Unannounced breaking changes erode team trust in AI assistance
- **Time Waste** - Teams spend hours debugging failures from unexpected breaking changes

### Core Techniques

**1. Detect Breaking Changes Before Implementation**

```python
# Before making any changes, analyze impact:

# ❌ BAD: Change signature without checking usage
Edit("src/api.py",
     old_string="def process_data(data, format='json'):",
     new_string="def process_data(data):")  # BREAKING!

# ✅ GOOD: Check usage first, then propose
Grep("process_data", output_mode="files_with_matches")
# Found in: api.py, handlers.py, tests.py, integration.py, workers.py

Grep("process_data", output_mode="content", "-C": 2)
# 5 files call with format parameter
# → This is a BREAKING CHANGE

# Propose to user:
"""
BREAKING CHANGE DETECTED:

Change: Remove 'format' parameter from process_data()
Reason: Only JSON supported; parameter is vestigial

Impact:
- 5 files affected (api.py, handlers.py, tests.py, integration.py, workers.py)
- All call sites use format='json' explicitly
- Breaking: yes

Migration:
1. Remove format parameter (unused in practice)
2. Update 5 call sites to remove format='json' argument
3. Update tests

Should I proceed with this breaking change?
"""
```

**2. Always Propose with Full Context**

```python
# ❌ BAD: Vague proposal
"I want to rename the User class. OK?"

# ✅ GOOD: Comprehensive proposal
"""
BREAKING CHANGE PROPOSAL:

**Change**: Rename User class → Account
**Reason**: 'Account' better reflects business domain (supports orgs + users)

**Impact Analysis:**
- 23 files reference User class
- 45 function signatures use User type hints
- 12 database queries reference User model
- 3 API endpoints return User objects (/users, /user/:id, /profile)

**Breaking for:**
- Internal code: yes (23 files)
- External API: yes (3 endpoints return 'user' field)
- Database: no (table name unchanged)

**Migration Path:**
1. Rename User → Account internally
2. Add 'user' alias field to API responses for 6 months (backward compat)
3. Update API docs with deprecation notice
4. Remove alias after 6 months

**Timeline:**
- Implementation: 2 hours
- Testing: 1 hour
- Migration period: 6 months

Proceed with this breaking change?
"""
```

**3. Propose Alternatives for Non-Breaking Solutions**

```python
# ✅ GOOD: Offer non-breaking alternatives

"""
You want to change database field 'email_addr' → 'email'.

OPTION 1: Breaking Change
- Rename column directly
- Breaking: yes
- Requires database migration + downtime
- All code must update simultaneously

OPTION 2: Non-Breaking (Recommended)
- Add 'email' column alongside 'email_addr'
- Sync values in both columns
- Gradually migrate code to use 'email'
- Remove 'email_addr' after full migration
- Breaking: no
- Zero downtime

Which approach do you prefer?
"""
```

**4. Document Breaking Changes in Proposal**

```markdown
# ✅ GOOD: Clear breaking change documentation

BREAKING CHANGE: API v2.0.0

## Removed
- `GET /api/users` (deprecated since v1.8.0, 6 months ago)
- `format` parameter in `process_data()` (unused)

## Changed
- `User.email_address` → `User.email` (migration: use new field)
- Authentication now requires Bearer token (was: Basic auth)

## Migration Guide
1. Update `GET /api/users` → `GET /api/v2/users`
2. Change `User.email_address` → `User.email` in all code
3. Update auth headers: `Authorization: Bearer <token>`

## Backward Compatibility
- `/api/v1/users` still works until 2025-12-31
- `email_address` field aliased to `email` until 2025-12-31

Approve this breaking change?
```

**5. Wait for Explicit Approval**

```python
# ❌ BAD: Assume silence means approval
# Propose breaking change
# ...wait 10 seconds...
# Proceed with implementation  # WRONG!

# ✅ GOOD: Wait for explicit "yes"
# Propose breaking change
# Wait for user response
# User: "Yes, go ahead"
# → NOW implement

# User: "No" or "Wait" or silence
# → DON'T implement
```

**6. Implement with Safety Checks**

```python
# ✅ GOOD: After approval, implement with safety

# User approved breaking change: rename get_user() → fetch_account()

# Step 1: Update definition
Edit("src/models.py",
     old_string="def get_user(user_id):",
     new_string="def fetch_account(user_id):")

# Step 2: Update all call sites (found from grep earlier)
for file in ["api.py", "handlers.py", "tests.py"]:
    Edit(file,
         old_string="get_user(",
         new_string="fetch_account(",
         replace_all=True)

# Step 3: Verify no old references remain
Grep("get_user", output_mode="content")
# → Ensure zero matches

# Report completion
"""
Breaking change complete:
- Renamed get_user() → fetch_account()
- Updated 3 files: api.py, handlers.py, tests.py
- Verified no remaining references to get_user()

Tests recommended before committing.
"""
```

---

### Implementation Patterns

#### ✅ Good: Detect + Propose + Wait for Approval

```python
# User: "Simplify the authentication API"

# Step 1: Understand current API
Read("src/auth.py")
# Current: authenticate(username, password, mfa_code=None, device_id=None)

# Step 2: Check usage
Grep("authenticate\\(", output_mode="content", "-C": 2)
# 8 call sites found
# 3 use mfa_code parameter
# 5 use device_id parameter

# Step 3: Propose breaking change
"""
BREAKING CHANGE PROPOSAL:

**Simplification**: Remove `mfa_code` and `device_id` parameters from authenticate()

**Current**:
```python
authenticate(username, password, mfa_code=None, device_id=None)
```

**Proposed**:
```python
authenticate(username, password)
# MFA and device handled separately
```

**Impact**:
- 8 call sites affected
- 3 use mfa_code (login.py, api.py, tests.py)
- 5 use device_id (all mobile endpoints)
- Breaking: YES

**Migration**:
1. Create new mfa_verify(code) function
2. Create new device_register(device_id) function
3. Update 8 call sites to use new flow:
   - authenticate(username, password)
   - mfa_verify(code) if needed
   - device_register(device_id) if needed

**Benefits**:
- Cleaner separation of concerns
- Each function does one thing
- Easier to test

**Drawbacks**:
- Requires code changes in 8 locations
- More complex flow (3 calls instead of 1)

Proceed with this breaking change? (yes/no)
"""

# Wait for explicit user approval before implementing
```

---

#### ✅ Good: Offer Non-Breaking Alternative

```python
# User: "Change the config format from JSON to YAML"

# ❌ Could do breaking change: replace JSON with YAML
# ✅ Better: Offer non-breaking alternative

"""
BREAKING vs NON-BREAKING OPTIONS:

**OPTION 1: Breaking Change**
- Replace config.json with config.yaml
- Breaking: YES
- All users must convert their config files
- Deployment requires manual intervention

**OPTION 2: Non-Breaking (Recommended)**
- Support both config.json AND config.yaml
- Load yaml if present, else load json
- Breaking: NO
- Users migrate at their own pace
- Old deployments keep working

Code implementation (Option 2):
```python
def load_config():
    if os.path.exists('config.yaml'):
        return yaml.safe_load(open('config.yaml'))
    elif os.path.exists('config.json'):
        return json.load(open('config.json'))
    else:
        raise ConfigNotFound()
```

Which option do you prefer?
"""
```

---

#### ✅ Good: Gradual Deprecation Path

```python
# User approved removing old API endpoint

# ✅ GOOD: Implement deprecation first

Edit("src/api.py",
     old_string="""@app.route('/api/users')
def get_users():
    return jsonify(fetch_users())""",
     new_string="""@app.route('/api/users')
def get_users():
    # DEPRECATED: Use /api/v2/users instead. Will be removed in v3.0.0
    warnings.warn(
        "GET /api/users is deprecated. Use /api/v2/users",
        DeprecationWarning
    )
    logger.warning("Deprecated endpoint /api/users called")
    return jsonify(fetch_users()), 200, {
        'X-Deprecation-Warning': 'Use /api/v2/users. Removal: v3.0.0'
    }""")

# Add new endpoint
Edit("src/api.py",
     old_string="# API Routes",
     new_string="""# API Routes

@app.route('/api/v2/users')
def get_users_v2():
    return jsonify(fetch_users())""")

"""
Breaking change mitigated with deprecation:
1. Old endpoint /api/users still works but logs warnings
2. New endpoint /api/v2/users added
3. Deprecation header added to old endpoint
4. Can remove old endpoint in v3.0.0 (after migration period)

This gives users time to migrate without immediate breakage.
"""
```

---

#### ❌ Bad: Silent Breaking Change

```python
# ❌ BAD: Rename function without proposal

# User: "Improve naming in auth module"

# Immediately rename without checking impact
Edit("src/auth.py",
     old_string="def verify_credentials(username, password):",
     new_string="def authenticate_user(username, password):")

# Problems:
# - Didn't check how many files call verify_credentials()
# - Didn't propose the breaking change
# - Didn't wait for approval
# - Broke all existing call sites
# - No migration plan
```

---

#### ❌ Bad: Vague Breaking Change Proposal

```python
# ❌ BAD: Incomplete proposal

"""
I'm going to rename some stuff in the database to be clearer. OK?
"""

# Problems:
# - No details on what's being renamed
# - No impact analysis
# - No migration path
# - User can't make informed decision
```

---

#### ❌ Bad: Assuming Silence = Approval

```python
# ❌ BAD: Don't wait for explicit approval

Propose breaking change to user
# ...no response for 30 seconds...
# "I'll take that as a yes"
Implement breaking change  # WRONG!

# ✅ GOOD: Wait for explicit "yes"
Propose breaking change
# Wait indefinitely until user responds
# Only proceed if user explicitly approves
```

---

## Anti-Patterns

### ❌ Anti-Pattern 1: "It's Just a Rename"

**Problem**: Assuming renames are safe because they "just change names."

```python
# ❌ BAD: Rename without approval

# User: "Make variable names clearer"

Edit("src/models.py",
     old_string="class User:",
     new_string="class Account:",
     replace_all=True)

Edit("src/models.py",
     old_string="def get_user(",
     new_string="def get_account(",
     replace_all=True)

# Problems:
# - Class rename breaks all imports: from models import User
# - Function rename breaks all call sites
# - May break external API if User class is serialized
# - No impact analysis
# - No approval requested
```

**Impact:**
- Breaks all code importing or using renamed items
- May break external consumers of API
- Difficult to roll back partial renames
- Hours of debugging for team

---

### ❌ Anti-Pattern 2: Breaking Changes in "Improvements"

**Problem**: Hiding breaking changes in "improvements" or "refactoring."

```python
# ❌ BAD: Breaking change disguised as improvement

# User: "Improve error handling"

# Change exception types without asking
Edit("src/service.py",
     old_string="raise ValueError('Invalid input')",
     new_string="raise InvalidInputError('Invalid input')")

# Problems:
# - Changed exception type (ValueError → InvalidInputError)
# - Breaks all code catching ValueError
# - Disguised as "improvement"
# - No breaking change proposal
```

**Impact:**
- Exception handlers no longer catch the error
- Crashes propagate to production
- Team doesn't know why their try/except blocks stopped working

---

### ❌ Anti-Pattern 3: Database Schema Changes Without Migration Plan

**Problem**: Changing database schema without migration or rollback strategy.

```python
# ❌ BAD: Change schema without approval/migration

# User: "Add user roles feature"

# Directly modify schema
Edit("models.py",
     old_string="email = Column(String)",
     new_string="email = Column(String, unique=True)")  # BREAKING!

# Problems:
# - Added unique constraint without checking for duplicates
# - No migration script to clean existing data
# - Will fail on deployment if duplicates exist
# - No rollback plan if deployment fails
```

**Impact:**
- Deployment failure if duplicate emails exist
- Data migration required but not planned
- Production downtime during emergency fix
- Potential data loss

---

## Implementation Checklist

### Before Making Any Changes

- [ ] **Analyze impact** - Use Grep to find all references to code being changed
- [ ] **Identify breaking changes** - Does this change function signatures, remove functions, change data formats, or modify APIs?
- [ ] **Check dependencies** - What code depends on the current behavior?
- [ ] **Consider alternatives** - Is there a non-breaking way to achieve the goal?

### Breaking Change Detection

A change is BREAKING if it:

- [ ] **Removes** public functions, classes, or APIs
- [ ] **Renames** public functions, classes, parameters, or fields
- [ ] **Changes signatures** - adds required parameters, removes parameters, changes parameter types
- [ ] **Changes return types** - different type or structure returned
- [ ] **Changes data formats** - JSON → YAML, XML schema changes, API response structure
- [ ] **Changes database schema** - column renames, type changes, constraints
- [ ] **Changes configuration** - config file format or structure changes
- [ ] **Changes behavior** - same signature but different behavior that breaks assumptions
- [ ] **Changes exceptions** - different exception types raised

### Proposal Format (Use This Template)

```markdown
BREAKING CHANGE PROPOSAL:

**Change**: [What are you changing?]
**Reason**: [Why is this change necessary?]

**Impact Analysis**:
- [X] files affected
- [X] functions need updates
- [X] API endpoints changed
- [X] database migrations required

**Breaking for:**
- Internal code: [yes/no]
- External API: [yes/no]
- Database: [yes/no]
- Configuration: [yes/no]

**Migration Path**:
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Alternatives** (non-breaking):
- [Alternative 1]
- [Alternative 2]

**Timeline**:
- Implementation: [X hours]
- Testing: [X hours]
- Migration period: [X days/months]

Proceed with this breaking change? (yes/no)
```

### After Approval

- [ ] **Implement carefully** - Make exact changes proposed, nothing more
- [ ] **Update all references** - Use grep results to update all call sites
- [ ] **Verify completeness** - Grep again to ensure no old references remain
- [ ] **Update documentation** - API docs, README, changelogs
- [ ] **Add migration guide** - If needed for users/team
- [ ] **Recommend testing** - Suggest running tests to verify breaking change

---

## Summary

**Breaking Changes Need Approval** means never removing functions, changing signatures, modifying data formats, or altering APIs without explicit user approval. Always detect, propose with full context, and wait for "yes" before implementing.

**Core Rules:**

- **Detect first** - Use Grep to analyze impact before proposing changes
- **Always propose** - Never implement breaking changes without user knowledge
- **Full context** - Proposal must include impact, migration path, alternatives
- **Wait for "yes"** - Explicit approval required; silence ≠ approval
- **Offer alternatives** - Suggest non-breaking approaches when possible
- **Gradual deprecation** - Prefer deprecation periods over immediate removal

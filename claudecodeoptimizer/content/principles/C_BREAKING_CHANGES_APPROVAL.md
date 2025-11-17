# C_BREAKING_CHANGES_APPROVAL: Breaking Changes Need Approval

**Severity**: Critical

Never make breaking changes without explicit user approval. Identify, document, propose with migration path before implementation.

---

## Why

Breaking changes without approval create production outages, cascade failures, data loss risk, team disruption, and erode trust.

---

## Workflow

### 1. Detect Before Implementation

```python
# Check usage first
Grep("process_data", output_mode="files_with_matches")
# Found: api.py, handlers.py, tests.py, integration.py, workers.py

Grep("process_data", output_mode="content", "-C": 2)
# 5 files call with format parameter → BREAKING

# Propose:
"""
BREAKING CHANGE DETECTED:
Change: Remove 'format' parameter from process_data()
Impact: 5 files affected
Migration:
1. Remove parameter
2. Update 5 call sites
3. Update tests
Proceed?
"""
```

### 2. Propose with Full Context

```plaintext
BREAKING CHANGE PROPOSAL:
**Change**: Rename User → Account
**Reason**: Better reflects domain (supports orgs + users)
**Impact**: 23 files, 45 signatures, 12 queries, 3 API endpoints
**Breaking for**: Internal (yes), External API (yes), Database (no)
**Migration Path**:
1. Rename internally
2. Add 'user' alias for 6 months (backward compat)
3. Update docs with deprecation
4. Remove alias after 6 months
**Timeline**: 2h implementation, 6mo migration
Proceed?
```

### 3. Offer Non-Breaking Alternatives

```plaintext
OPTION 1: Breaking (rename column, downtime)
OPTION 2: Non-Breaking (add new column, sync, gradual migration, zero downtime)
Which approach?
```

---

## Breaking Change Detection

A change is BREAKING if:
- [ ] Removes public functions/classes/APIs
- [ ] Renames public items
- [ ] Changes signatures (add required params, remove params, change types)
- [ ] Changes return types/structures
- [ ] Changes data formats (JSON→YAML, schema changes)
- [ ] Changes database schema
- [ ] Changes configuration format
- [ ] Changes behavior (same signature, different outcome)
- [ ] Changes exceptions raised

---

## Examples

### ✅ Good: Detect + Propose + Wait
```python
# User: "Simplify authentication API"
Read("src/auth.py")
# Current: authenticate(username, password, mfa_code=None, device_id=None)

Grep("authenticate\\(", output_mode="content", "-C": 2)
# 8 call sites, 3 use mfa_code, 5 use device_id

"""
BREAKING CHANGE PROPOSAL:
**Simplification**: Remove mfa_code and device_id params
**Impact**: 8 call sites
**Migration**: Create mfa_verify() and device_register() functions
Proceed? (yes/no)
"""
# WAIT for explicit approval
```

### ✅ Good: Gradual Deprecation
```python
@app.route('/api/users')
def get_users():
    # DEPRECATED: Use /api/v2/users. Removal: v3.0.0
    logger.warning("Deprecated endpoint called")
    return jsonify(fetch_users()), 200, {
        'X-Deprecation-Warning': 'Use /api/v2/users. Removal: v3.0.0'
    }
```

---

## Checklist

### Before Changes
- [ ] Analyze impact (grep all references)
- [ ] Identify breaking changes
- [ ] Check dependencies
- [ ] Consider non-breaking alternatives

### After Approval
- [ ] Implement exact proposed changes
- [ ] Update all references (grep-verified)
- [ ] Verify no old references remain
- [ ] Update documentation
- [ ] Recommend testing

# U_CHANGE_VERIFICATION: Change Verification Protocol

**Severity**: Critical

Verify all changes BEFORE claiming completion. No "should work" - only verified facts.

---

## Why

Prevents partial completion, missed references, and integration failures through systematic verification.

---

## Protocol

### 1. Pre-Flight Analysis

**Find ALL affected points:**
```bash
# Direct references
grep -r "old_name" .

# Deep analysis (Explore agent)
Task({
  subagent_type: "Explore",
  model: "haiku",
  prompt: "Find ALL dependencies for 'old_name': definitions, calls, imports, types, config, docs"
})
```

**Categorize & order:**
1. DEFINITIONS (first)
2. TYPE HINTS (second)
3. CALLERS (third)
4. IMPORTERS (fourth)
5. CONFIG/TESTS/DOCS (last)

**Create TODOs:**
```javascript
TodoWrite([
  {content: "Update DEFINITION in api/users.py:45", status: "pending"},
  {content: "Update CALLERS in services/auth.py:123,156,189", status: "pending"},
  {content: "Final verification: grep old name (must be 0)", status: "pending"}
])
```

### 2. Implementation

```
For each TODO:
├─ Make change
├─ ✅ VERIFY:
│  ├─ Grep old name in THIS file (0 results)
│  ├─ Grep new name in THIS file (exists)
│  └─ Check imports/calls
└─ Mark complete ONLY after verification
```

### 3. Post-Flight Check

```bash
# Old names GONE (0 results)
grep -r "old_name" .

# New names PRESENT
grep -r "new_name" .
```

---

## Verification Without Tests

**Structural:**
- Syntax: `python -m py_compile file.py`
- Imports: Grep import statements
- Types: `mypy file.py` (if available)

**Semantic:**
Present critical change points to user for manual verification.

---

## Examples

### ❌ Wrong
```
"Renamed getUserData to fetchUserData in all files."
[Missed 2 files, didn't verify]
```

### ✅ Right
```
1. Grep found 12 files
2. Created 12 TODOs
3. Updated each, verified (0 old refs)
4. Final: grep -r "getUserData" src/ → 0 results ✓
```

---

## Thoroughness Levels

- **Quick** (< 1min): 1 file, grep this file only
- **Medium** (1-2min): 2-4 files, grep affected dir
- **Comprehensive** (2-5min): 5+ files, Explore agent + full analysis

**Never skip verification** - adjust thoroughness to scope.

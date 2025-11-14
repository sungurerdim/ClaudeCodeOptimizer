---
id: U_CHANGE_VERIFICATION
title: Change Verification Protocol
category: universal
severity: critical
weight: 10
applicability:
  project_types: ['all']
  languages: ['all']
---

# U_CHANGE_VERIFICATION: Change Verification Protocol 🔴

**Severity**: Critical

AI must verify changes BEFORE claiming completion. No "should work" or "looks complete" - only verified facts.

**Why**: Prevents partial completion, missed references, and integration failures in ALL code changes.

**Applies to**: EVERY code change - from single-line edits to large refactorings.

**Thoroughness Levels**:
- **Quick** (1 file, simple edit): Grep this file only
- **Medium** (2-4 files): Grep all affected files
- **Comprehensive** (5+ files, API changes, renames): Full dependency analysis with Explore agent

**Philosophy**: Even a single function name change requires checking ALL callers. The scope determines thoroughness, not whether to verify.

---

## Protocol

### 1. Pre-Flight: Comprehensive Dependency Analysis (1-2 minutes)

**Goal**: Find EVERY affected point BEFORE making any changes. Prevention > Reaction.

**Step 1: Direct References**
```bash
# Find all direct uses
grep -r "old_name" .
# or
Grep("old_name", output_mode="content", -C=2)
```

**Step 2: Indirect Dependencies (Use Explore Agent)**
```javascript
// Launch Explore agent for deep analysis
Task({
  subagent_type: "Explore",
  model: "haiku",
  description: "Find all dependencies for X",
  prompt: `Analyze ALL dependencies for changing 'old_name':

  1. Direct references:
     - Function/class definitions
     - Function calls
     - Import statements
     - Type annotations

  2. Indirect dependencies:
     - Modules that import modules using old_name
     - Config files referencing this
     - Environment variables
     - Documentation/comments

  3. Dependency graph:
     - What depends ON this? (callers, importers)
     - What does this depend ON? (callees, imports)
     - Tests that exercise this

  Return: Complete list with file:line for EACH occurrence.
  Thoroughness: very thorough`
})
```

**Step 3: Categorize & Order**
```
From Explore results, create ordered categories:

1. DEFINITIONS (change first)
   - The actual function/class being renamed

2. TYPE HINTS (change second)
   - Return types, parameter types

3. CALLERS (change third, depends on 1-2)
   - Direct function calls
   - Group by file for efficiency

4. IMPORTERS (change fourth)
   - Modules importing this
   - Update import statements

5. CONFIG/TESTS (change fifth)
   - Config files
   - Test files

6. DOCS (change last, optional)
   - Comments, docstrings, README
```

**Step 4: Create Smart TODOs**
```javascript
// Generate specific, ordered TODOs
TodoWrite([
  {
    content: "Update DEFINITION in api/users.py:45 (rename getUserData → fetchUserProfile)",
    activeForm: "Updating function definition",
    status: "pending"
  },
  {
    content: "Update RETURN TYPE in api/users.py:47 (if signature changed)",
    activeForm: "Updating type hints",
    status: "pending"
  },
  {
    content: "Update CALLERS in services/auth.py:123, :156, :189",
    activeForm: "Updating auth.py callers",
    status: "pending"
  },
  {
    content: "Update CALLERS in api/routes.py:67, :89",
    activeForm: "Updating routes.py callers",
    status: "pending"
  },
  {
    content: "Update IMPORTS in services/__init__.py:12",
    activeForm: "Updating imports",
    status: "pending"
  },
  {
    content: "Update TESTS in tests/test_users.py:34, :67",
    activeForm: "Updating tests",
    status: "pending"
  },
  {
    content: "Final verification: grep for old name (must be 0 results)",
    activeForm: "Running final verification",
    status: "pending"
  }
])
```

**Output**: Comprehensive, ordered TODO list with NO surprises during implementation.

---

### 2. Implementation: Verify-Then-Complete (per TODO)
```
For each TODO:
├─ Make the change
├─ ✅ VERIFY before marking complete:
│  ├─ Grep for old name in THIS file (should be 0)
│  ├─ Grep for new name in THIS file (should exist)
│  └─ Check imports/calls related to this change
└─ Mark TODO as completed ONLY after verification
```

**Critical**: Never mark TODO complete without verification evidence.

---

### 3. Post-Flight: Final Check (30 seconds)
```bash
# Old names should be GONE (0 results)
grep -r "old_name" .

# New names should be PRESENT (in expected files)
grep -r "new_name" .

# Integration points check
grep -r "from.*old_module" .  # Old imports?
```

**Pass criteria**:
- Zero results for old names
- New names present in all expected locations
- Imports/calls updated

---

## Verification Without Tests

When test suite is minimal/absent:

**Structural Verification** (automatic):
- Syntax check: `python -m py_compile file.py` or `node --check file.js`
- Import check: Grep for import statements
- Type check: `mypy file.py` or `tsc --noEmit` (if available)

**Semantic Verification** (manual checkpoint):
- Present user with **critical change points**:
  ```
  ⚠️ Manual Verification Needed:

  1. auth.py:45 - API signature changed, check callers:
     - api/routes.py:123
     - services/user.py:89

  2. config.py:12 - Renamed config key, check usage:
     - Grep shows 3 files reference this
  ```

**User validates critical paths**, AI handles mechanical checks.

---

## Examples

### ❌ Wrong Way (Optimistic Completion)
```
Assistant: "Renamed `getUserData` to `fetchUserData` in all files."
[Actually missed 2 files, didn't verify]
```

### ✅ Right Way (Verified Completion)
```
Assistant:
1. Grep found 12 files using `getUserData`
2. Created 12 TODOs for each file
3. Updated file 1/12... [verified with grep - 0 old refs]
4. Updated file 2/12... [verified with grep - 0 old refs]
...
12. All files updated.
13. Final verification:
    $ grep -r "getUserData" src/
    [0 results - verified ✓]
```

---

## Integration with Existing Tools

**Use with**:
- U_EVIDENCE_BASED (Evidence-Based Verification) - grep output is evidence
- U_ROOT_CAUSE_ANALYSIS (Root Cause Analysis) - trace changes to source
- U_INTEGRATION_CHECK (Complete Integration Check) - no orphaned code

**TodoWrite pattern**:
```javascript
{
  "content": "Update auth.py:45 to use new fetchUserData signature",
  "status": "in_progress",
  "activeForm": "Updating auth.py"
}
// Mark complete ONLY after grep verification
```

---

## Token Efficiency

**Smart grep usage**:
```bash
# ✅ Efficient: Target specific patterns
grep -r "class OldName" src/
grep -r "from.*old_module import" .

# ❌ Wasteful: Reading entire files
Read every file to search manually
```

**Parallel verification**: When checking multiple independent changes, run grep commands in parallel.

---

## Thoroughness Scaling

**ALL changes use this protocol, but thoroughness scales with scope:**

### Quick Verification (< 1 minute)
- **When**: Single file, < 3 locations affected
- **Method**: `grep old_name this_file.py` (check this file only)
- **Example**: Rename helper function used 2x in same file

### Medium Verification (1-2 minutes)
- **When**: 2-4 files affected, local changes
- **Method**: `grep -r old_name affected_dir/`
- **Example**: Update function used in 3 related files

### Comprehensive Verification (2-5 minutes)
- **When**: 5+ files, API changes, structural refactoring
- **Method**: Explore agent + full dependency analysis
- **Example**: Rename public API used across codebase

**Never skip verification** - adjust thoroughness to match scope.

---

## Related Skill

For detailed workflow with sub-agent orchestration, see:
- **comprehensive-refactoring** skill (`.claude/skills/comprehensive-refactoring.md`)

This principle defines WHAT to verify, the skill shows HOW to execute it efficiently.

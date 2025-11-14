# Principle Categorization Update Plan

**Date:** 2025-01-14
**Purpose:** Migrate 8 project-specific principles to universal category and remove 2 duplicate principles
**Impact:** Critical - affects core principle loading, categorization, and all documentation

---

## Executive Summary

**Principles to Move (P → U):** 8 principles
**Principles to Delete:** 2 duplicates (U005, U006)
**Total Changes:** 10 principles, 50+ files affected
**Estimated Time:** 2-3 hours
**Risk Level:** HIGH (affects core categorization logic)

---

## Table of Contents

1. [Pre-Migration Checklist](#pre-migration-checklist)
2. [Number Field Handling Strategy](#number-field-handling-strategy)
3. [Critical Bugs to Fix First](#critical-bugs-to-fix-first)
4. [Principle-by-Principle Migration](#principle-by-principle-migration)
5. [Duplicate Deletion Strategy](#duplicate-deletion-strategy)
6. [Post-Migration Validation](#post-migration-validation)
7. [Rollback Plan](#rollback-plan)

---

## Pre-Migration Checklist

### ✅ Before Starting

- [ ] Create backup branch: `git checkout -b principle-categorization-update`
- [ ] Run full test suite: `pytest tests/ -v`
- [ ] Verify current principle count: `ls content/principles/*.md | wc -l` (should be 95)
- [ ] Document current state: `git log --oneline -5 > pre-migration-state.txt`
- [ ] Check for uncommitted changes: `git status --short`

### ⚠️ Critical Understanding

**Why This Migration?**
These principles were incorrectly categorized as project-specific when they should be universal:
- **Universal** = Applies to ALL projects, ALL languages, CRITICAL/HIGH severity
- **Project-Specific** = Conditional based on project type, language, or team size

**What Changes?**
- File names: `P001.md` → `U015.md` (8 files)
- Principle IDs: `id: P001` → `id: U015` (in frontmatter)
- Categories: `category: code_quality` → `category: universal`
- Documentation: All references updated

**What Stays Same?**
- File content (except frontmatter)
- Principle logic and rules
- Severity levels

---

## Number Field Handling Strategy

### 🔍 Critical Analysis: The "number" Field

**Background:**
Each principle has a `number` field in frontmatter:
```yaml
id: P001
number: 1     # ← What is this?
title: DRY Enforcement
category: code_quality
```

### What is the Number Field?

**Definition:** The `number` field stores the numeric portion of the principle ID.

- `P001` → `number: 1`
- `U014` → `number: 14`
- `P045` → `number: 45`

**It is NOT category-relative ordering.** Each ID series (U, P, C) has its own numbering starting from 1.

### Current Numbering State

| Series | Range | Number Values | Status |
|--------|-------|--------------|--------|
| **U-series** | U001-U014 | 1-14 (sequential) | ✅ Complete |
| **P-series** | P001-P069 | 1-69 (sequential) | ✅ Complete |
| **C-series** | C001-C012 | **None** (omitted) | ✅ Works fine |

**Critical Finding:** All 12 C-series principles have **no `number` field** and the system handles this gracefully!

### Where is Number Field Used?

**Comprehensive code analysis reveals:**

#### ✅ Where Number is READ:
1. `principle_md_loader.py:40` - `"number": post.get("number")` → Returns `None` if missing
2. `principles.py:101` - `number=principle_data["number"]` → Assigns to dataclass
3. `principles.py:353` - Returns in `get_principle_summary()` → **Method never called anywhere!**

#### ❌ Where Number is NEVER Used:
- **Sorting**: All code sorts by `p["id"]` (string) or severity, NOT `number`
  - `claude_md_generator.py:643`: `sorted(principles, key=lambda x: x["id"])`
  - `claude_md_generator.py:782`: `sorted(claude_principles, key=lambda x: x["id"])`
  - `principle_selector.py:334`: `sorted(..., key=lambda p: (severity_order[p.severity], p.id))`

- **Display**: CLAUDE.md shows `{principle['id']}`, not `{principle['number']}`
- **Filtering**: No code filters by number
- **Business Logic**: No decisions based on number value

**Conclusion:** The `number` field is **vestigial metadata** - never used for any functional purpose.

### Impact of P→U Migration on Numbering

**Question:** When P001 (number: 1) becomes U015, what happens to numbering?

**Three Scenarios:**

#### Scenario A: Keep P001's number=1 in U015
```yaml
# U015.md (migrated from P001)
id: U015
number: 1    # ← Original P001's number
category: universal
```
**Problem:** U015 with number=1 contradicts the pattern (U001=1, U014=14, U015=1?)

#### Scenario B: Assign U015 number=15
```yaml
# U015.md (migrated from P001)
id: U015
number: 15   # ← Sequential continuation
category: universal
```
**Problem:** Then P002-P069 need renumbering to 1-68 (68 files to edit!)

#### Scenario C: Omit number field entirely
```yaml
# U015.md (migrated from P001)
id: U015
# number: (omitted) ← Follow C-series precedent
category: universal
```
**Benefit:** C-series already proves this works perfectly!

### 🎯 Recommended Strategy: Option C (No Number Field)

**Decision:** **Omit `number` field from all new universal principles (U015-U022)**

**Rationale:**
1. ✅ **Proven precedent:** C001-C012 already work without `number` field
2. ✅ **Zero functional impact:** Field never used in code
3. ✅ **Minimal touch:** Don't need to edit 68 P-series files
4. ✅ **Type safety:** `Optional[int]` already in dataclass
5. ✅ **Future-proof:** Can clean up later if needed

**Implementation:**

For each P→U migration (P001→U015, P002→U016, etc.):

```yaml
# BEFORE (P001.md)
---
id: P001
number: 1
title: DRY Enforcement & Single Source of Truth
category: code_quality
---

# AFTER (U015.md)
---
id: U015
# number: (omit this field entirely)
title: DRY Enforcement & Single Source of Truth
category: universal
---
```

**Update commands in migration steps:**

```bash
# When editing frontmatter, DELETE the number line
sed -i '/^number:/d' content/principles/P001.md

# Then update ID and category
   # number field deleted above
sed -i 's/^id: P001$/id: U015/' content/principles/P001.md
sed -i 's/^category: code_quality$/category: universal/' content/principles/P001.md
```

### Alternative Options (Not Recommended)

#### Option A: Full Renumbering (High Risk, No Benefit)

**Action:**
- P001→U015: Set `number: 15`
- P002→P069: Renumber all to `number: 1-68`

**Impact:**
- ❌ Requires editing 69 files (error-prone)
- ❌ Zero functional benefit (number unused)
- ❌ Risk of introducing bugs
- ❌ Violates minimal touch principle

#### Option B: Keep Original Numbers (Inconsistent)

**Action:**
- P001→U015: Keep `number: 1` from P001

**Impact:**
- ❌ U015 (number: 1) looks wrong after U014 (number: 14)
- ❌ Confusing for humans
- ❌ No functional issue but semantically odd

### Validation After Migration

Check that omitted `number` field causes no issues:

```bash
# Test principle loading
python -c "
from pathlib import Path
from claudecodeoptimizer.core.principle_md_loader import load_all_principles

principles = load_all_principles(Path('content/principles'))

# Find principles without number field
no_number = [p for p in principles if p.get('number') is None]
print(f'Principles without number: {len(no_number)}')

# Should include C001-C012 (12) + U015-U022 (8) = 20 total
expected_ids = [f'C{i:03d}' for i in range(1, 13)] + [f'U{i:03d}' for i in range(15, 23)]
actual_ids = [p['id'] for p in no_number]
print(f'Expected: {len(expected_ids)}, Actual: {len(actual_ids)}')
print(f'Match: {set(actual_ids) == set(expected_ids)}')
"
```

**Expected result:**
```
Principles without number: 20
Expected: 20, Actual: 20
Match: True
```

### Documentation Update

Add note to principle contribution guide:

```markdown
## Principle Frontmatter Fields

- **id** (required): Principle identifier (U001, P001, C001)
- **title** (required): Human-readable title
- **category** (required): universal, code_quality, security_privacy, etc.
- **severity** (required): critical, high, medium, low
- **weight** (required): 1-10 importance score
- **number** (optional): **DEPRECATED** - Omit for new principles
  - Legacy field from earlier versions
  - Not used in any code logic
  - Can be omitted (see C-series precedent)
```

### Summary: Number Field Strategy

| Aspect | Decision | Reason |
|--------|----------|--------|
| **U015-U022 number field** | **Omit entirely** | Follow C-series precedent |
| **P002-P069 renumbering** | **No changes** | Avoid unnecessary edits |
| **Code changes needed** | **Zero** | Field already optional |
| **Validation needed** | **Yes** | Verify None handling works |
| **Documentation** | **Update contrib guide** | Mark field as deprecated |

**Action Items:**
- ✅ Add `sed -i '/^number:/d'` to each migration step
- ✅ Update validation section to check `number: None` handling
- ✅ Document that number field is deprecated

---

## Critical Bugs to Fix First

### 🐛 BUG #1: Incorrect P002 References (HIGH PRIORITY)

**Problem:** Multiple files reference "P002 (DRY Enforcement)" but P002 is actually "Complete Integration Check". The correct principle for DRY is P001.

**Affected Files:**

1. **claudecodeoptimizer/core/constants.py**
   - Line 5: `# Follows P002 (DRY Enforcement) - single source of truth`
   - Line 18: `# Display Limits (P002 - DRY Enforcement)`
   - Line 58: `# Detection Confidence Thresholds (P002 - DRY Enforcement)`

   **Fix:** Change all `P002` → `P001` in these comments

2. **claudecodeoptimizer/core/utils.py**
   - Line 3: `# Common helper functions to reduce code duplication (P002 - DRY Enforcement)`

   **Fix:** Change `P002` → `P001`

**Commands to Fix:**
```bash
# Fix constants.py
sed -i 's/P002 (DRY Enforcement)/P001 (DRY Enforcement)/g' claudecodeoptimizer/core/constants.py
sed -i 's/P002 - DRY Enforcement/P001 - DRY Enforcement/g' claudecodeoptimizer/core/constants.py

# Fix utils.py
sed -i 's/P002 - DRY Enforcement/P001 - DRY Enforcement/g' claudecodeoptimizer/core/utils.py

# Verify
grep -n "P002.*DRY" claudecodeoptimizer/core/*.py
# Should return 0 results
```

**Commit:**
```bash
git add claudecodeoptimizer/core/constants.py claudecodeoptimizer/core/utils.py
git commit -m "fix(principles): correct P002→P001 references in comments

Fixed incorrect principle ID references. P001 is DRY Enforcement,
not P002. These comments were copy-paste errors.

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

## Principle-by-Principle Migration

### Migration Template

For each principle, follow this exact sequence:

1. **Update Frontmatter** (in principle file)
2. **Rename File** (P001.md → U015.md)
3. **Update Code References** (Python files)
4. **Update Documentation** (Markdown files)
5. **Verify** (grep for old ID)
6. **Commit** (atomic commit per principle)

---

### P001 → U015: DRY Enforcement & Single Source of Truth

**Current State:**
- File: `content/principles/P001.md`
- ID: `P001`
- Category: `code_quality`
- Severity: `high`

**Target State:**
- File: `content/principles/U015.md`
- ID: `U015`
- Category: `universal`
- Severity: `critical` (upgrade from high)

#### Step 1: Update Frontmatter

**File:** `content/principles/P001.md`

```bash
# Edit frontmatter
# BEFORE:
# id: P001
# category: code_quality
# severity: high

# AFTER:
# id: U015
# category: universal
# severity: critical
```

**Command:**
```bash
# Update frontmatter (including number field deletion)
sed -i '/^number:/d' content/principles/P001.md
   # number field deleted above
sed -i 's/^id: P001$/id: U015/' content/principles/P001.md
sed -i 's/^category: code_quality$/category: universal/' content/principles/P001.md
sed -i 's/^severity: high$/severity: critical/' content/principles/P001.md

# Verify
head -15 content/principles/P001.md | grep -E "^(id|category|severity):"
# Should NOT show 'number:' line
```

#### Step 2: Rename File

```bash
git mv content/principles/P001.md content/principles/U015.md
```

#### Step 3: Update Code References

**File: `claudecodeoptimizer/core/principles.py:93`**

```python
# BEFORE:
"minimal": {"include": ["U001", "U002", "U003", "P001"]}

# AFTER:
"minimal": {"include": ["U001", "U002", "U003", "U015"]}
```

**Command:**
```bash
sed -i 's/"P001"/"U015"/g' claudecodeoptimizer/core/principles.py

# Verify
grep -n "U015" claudecodeoptimizer/core/principles.py
```

**Files with Example Comments (update for consistency):**
- `claudecodeoptimizer/core/principle_loader.py:183,190` - Update examples
- `claudecodeoptimizer/core/principle_loader.py:252,259` - Update examples
- `claudecodeoptimizer/core/principle_md_loader.py:86` - Update examples

```bash
# Update all P001 example references to U015
sed -i 's/"P001"/"U015"/g' claudecodeoptimizer/core/principle_loader.py
sed -i 's/"P001"/"U015"/g' claudecodeoptimizer/core/principle_md_loader.py
```

#### Step 4: Update Documentation

**Files to Update:**

1. **CLAUDE.md:32**
   ```bash
   sed -i 's/P001: DRY Enforcement/U015: DRY Enforcement/g' CLAUDE.md
   sed -i "s/'\.claude\/principles\/P001\.md'/'\.claude\/principles\/U015\.md'/g" CLAUDE.md
   ```

2. **content/agents/audit-agent.md:72**
   ```bash
   sed -i 's/P001:/U015:/g' content/agents/audit-agent.md
   sed -i 's/P001\.md/U015\.md/g' content/agents/audit-agent.md
   ```

3. **content/agents/fix-agent.md:64**
   ```bash
   sed -i 's/P001:/U015:/g' content/agents/fix-agent.md
   sed -i 's/P001\.md/U015\.md/g' content/agents/fix-agent.md
   ```

4. **content/commands/fix.md:5** (frontmatter list)
   ```bash
   sed -i "s/'P001'/'U015'/g" content/commands/fix.md
   ```

5. **content/commands/init.md:756** (example)
   ```bash
   sed -i "s/'P001'/'U015'/g" content/commands/init.md
   ```

6. **docs/architecture.md** (all references)
   ```bash
   sed -i 's/P001/U015/g' docs/architecture.md
   ```

#### Step 5: Verify

```bash
# Search for any remaining P001 references
grep -r "P001" --include="*.py" --include="*.md" . | grep -v ".git"

# Should only find:
# - This plan file (PRINCIPLE_UPDATE_PLAN.md)
# - Old git history
```

#### Step 6: Commit

```bash
git add -A
git commit -m "refactor(principles): migrate P001 to U015 (universal)

Moved DRY Enforcement & Single Source of Truth from code_quality to
universal category. This principle applies to all projects and languages.

Changes:
- Renamed: content/principles/P001.md → U015.md
- Updated: ID, category (universal), severity (critical)
- Updated: All code references in principles.py, loaders
- Updated: All documentation (CLAUDE.md, agents, commands, docs/)

Breaking: Principle ID changed P001→U015
Impact: Projects referencing P001 need update

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

### P002 → U016: Complete Integration Check

**Current State:**
- File: `content/principles/P002.md`
- ID: `P002`
- Category: `code_quality`

**Target State:**
- File: `content/principles/U016.md`
- ID: `U016`
- Category: `universal`

#### Steps:

1. **Update Frontmatter:**
   ```bash
   sed -i '/^number:/d' content/principles/P002.md
   sed -i 's/^id: P002$/id: U016/' content/principles/P002.md
   sed -i 's/^category: code_quality$/category: universal/' content/principles/P002.md
   ```

2. **Rename File:**
   ```bash
   git mv content/principles/P002.md content/principles/U016.md
   ```

3. **Update Code References:**
   ```bash
   # No hardcoded P002 references in Python code found
   # Only in comments (which were already fixed in Bug #1)
   ```

4. **Update Documentation:**
   ```bash
   sed -i 's/P002: Complete Integration Check/U016: Complete Integration Check/g' CLAUDE.md
   sed -i 's/P002\.md/U016\.md/g' CLAUDE.md
   sed -i 's/P002:/U016:/g' content/agents/audit-agent.md
   sed -i 's/P002\.md/U016\.md/g' content/agents/audit-agent.md
   sed -i 's/P002:/U016:/g' content/agents/fix-agent.md
   sed -i 's/P002\.md/U016\.md/g' content/agents/fix-agent.md
   sed -i "s/'P002'/'U016'/g" content/commands/fix.md
   sed -i "s/'P002'/'U016'/g" content/commands/init.md
   sed -i 's/P002/U016/g' content/principles/U013.md
   ```

5. **Verify:**
   ```bash
   grep -r "P002" --include="*.py" --include="*.md" . | grep -v ".git" | grep -v "PRINCIPLE_UPDATE_PLAN.md"
   ```

6. **Commit:**
   ```bash
   git add -A
   git commit -m "refactor(principles): migrate P002 to U016 (universal)

   Moved Complete Integration Check from code_quality to universal
   category. Zero orphaned code applies to all projects.

   Changes:
   - Renamed: content/principles/P002.md → U016.md
   - Updated: ID, category (universal)
   - Updated: All documentation references
   - Fixed: Cross-reference in U013.md

   Co-Authored-By: Claude <noreply@anthropic.com>"
   ```

---

### P003 → U017: No Backward Compatibility Debt

**Current State:**
- File: `content/principles/P003.md`
- ID: `P003`
- Category: `code_quality`

**Target State:**
- File: `content/principles/U017.md`
- ID: `U017`
- Category: `universal`

#### Steps:

1. **Update Frontmatter:**
   ```bash
   sed -i '/^number:/d' content/principles/P003.md
   sed -i 's/^id: P003$/id: U017/' content/principles/P003.md
   sed -i 's/^category: code_quality$/category: universal/' content/principles/P003.md
   ```

2. **Rename File:**
   ```bash
   git mv content/principles/P003.md content/principles/U017.md
   ```

3. **Update Documentation:**
   ```bash
   sed -i 's/P003/U017/g' content/commands/audit.md
   sed -i 's/P003/U017/g' content/commands/generate.md
   sed -i "s/'P003'/'U017'/g" content/commands/fix.md
   ```

4. **Verify:**
   ```bash
   grep -r "P003" --include="*.py" --include="*.md" . | grep -v ".git" | grep -v "PRINCIPLE_UPDATE_PLAN.md"
   ```

5. **Commit:**
   ```bash
   git add -A
   git commit -m "refactor(principles): migrate P003 to U017 (universal)

   Moved No Backward Compatibility Debt from code_quality to universal.
   Clean migration applies to all projects.

   Co-Authored-By: Claude <noreply@anthropic.com>"
   ```

---

### P007 → U018: Linting & SAST Enforcement

**Current State:**
- File: `content/principles/P007.md`
- ID: `P007`
- Category: `code_quality`

**Target State:**
- File: `content/principles/U018.md`
- ID: `U018`
- Category: `universal`

#### Steps:

1. **Update Frontmatter:**
   ```bash
   sed -i '/^number:/d' content/principles/P007.md
   sed -i 's/^id: P007$/id: U018/' content/principles/P007.md
   sed -i 's/^category: code_quality$/category: universal/' content/principles/P007.md
   ```

2. **Rename File:**
   ```bash
   git mv content/principles/P007.md content/principles/U018.md
   ```

3. **Update Documentation:**
   ```bash
   sed -i 's/P007: Linting/U018: Linting/g' CLAUDE.md
   sed -i 's/P007\.md/U018\.md/g' CLAUDE.md
   sed -i 's/P007:/U018:/g' content/agents/audit-agent.md
   sed -i 's/P007\.md/U018\.md/g' content/agents/audit-agent.md
   sed -i 's/P007:/U018:/g' content/agents/fix-agent.md
   sed -i 's/P007\.md/U018\.md/g' content/agents/fix-agent.md
   sed -i 's/P007/U018/g' content/agents/generate-agent.md
   sed -i 's/P007/U018/g' content/commands/init.md
   sed -i 's/P007/U018/g' content/commands/audit.md
   sed -i 's/P007/U018/g' content/commands/generate.md
   sed -i "s/'P007'/'U018'/g" content/commands/fix.md
   ```

4. **Verify:**
   ```bash
   grep -r "P007" --include="*.py" --include="*.md" . | grep -v ".git" | grep -v "PRINCIPLE_UPDATE_PLAN.md"
   ```

5. **Commit:**
   ```bash
   git add -A
   git commit -m "refactor(principles): migrate P007 to U018 (universal)

   Moved Linting & SAST Enforcement from code_quality to universal.
   Security scanning applies to all projects.

   Co-Authored-By: Claude <noreply@anthropic.com>"
   ```

---

### P028 → U019: SQL Injection Prevention

**Current State:**
- File: `content/principles/P028.md`
- ID: `P028`
- Category: `security_privacy`
- Severity: `critical`

**Target State:**
- File: `content/principles/U019.md`
- ID: `U019`
- Category: `universal`
- Severity: `critical` (keep)

#### Steps:

1. **Update Frontmatter:**
   ```bash
   sed -i '/^number:/d' content/principles/P028.md
   sed -i 's/^id: P028$/id: U019/' content/principles/P028.md
   sed -i 's/^category: security_privacy$/category: universal/' content/principles/P028.md
   ```

2. **Rename File:**
   ```bash
   git mv content/principles/P028.md content/principles/U019.md
   ```

3. **Update Documentation:**
   ```bash
   sed -i 's/P028: SQL Injection/U019: SQL Injection/g' CLAUDE.md
   sed -i 's/P028\.md/U019\.md/g' CLAUDE.md
   sed -i 's/P028:/U019:/g' content/agents/audit-agent.md
   sed -i 's/P028\.md/U019\.md/g' content/agents/audit-agent.md
   sed -i 's/P028/U019/g' content/agents/fix-agent.md
   sed -i 's/P028/U019/g' content/commands/init.md
   sed -i 's/P028/U019/g' content/commands/audit.md
   sed -i "s/'P028'/'U019'/g" content/commands/fix.md
   sed -i 's/P028/U019/g' content/guides/security-response.md
   ```

4. **Verify:**
   ```bash
   grep -r "P028" --include="*.py" --include="*.md" . | grep -v ".git" | grep -v "PRINCIPLE_UPDATE_PLAN.md"
   ```

5. **Commit:**
   ```bash
   git add -A
   git commit -m "refactor(principles): migrate P028 to U019 (universal)

   Moved SQL Injection Prevention from security_privacy to universal.
   Parameterized queries are mandatory for all DB access.

   Co-Authored-By: Claude <noreply@anthropic.com>"
   ```

---

### P029 → U020: Secret Management with Rotation

**Current State:**
- File: `content/principles/P029.md`
- ID: `P029`
- Category: `security_privacy`
- Severity: `critical`

**Target State:**
- File: `content/principles/U020.md`
- ID: `U020`
- Category: `universal`
- Severity: `critical` (keep)

#### Steps:

1. **Update Frontmatter:**
   ```bash
   sed -i '/^number:/d' content/principles/P029.md
   sed -i 's/^id: P029$/id: U020/' content/principles/P029.md
   sed -i 's/^category: security_privacy$/category: universal/' content/principles/P029.md
   ```

2. **Rename File:**
   ```bash
   git mv content/principles/P029.md content/principles/U020.md
   ```

3. **Update Documentation:**
   ```bash
   sed -i 's/P029: Secret Management/U020: Secret Management/g' CLAUDE.md
   sed -i 's/P029\.md/U020\.md/g' CLAUDE.md
   sed -i 's/P029:/U020:/g' content/agents/audit-agent.md
   sed -i 's/P029\.md/U020\.md/g' content/agents/audit-agent.md
   sed -i 's/P029/U020/g' content/agents/fix-agent.md
   sed -i 's/P029/U020/g' content/commands/init.md
   sed -i 's/P029/U020/g' content/commands/audit.md
   sed -i "s/'P029'/'U020'/g" content/commands/fix.md
   sed -i 's/P029/U020/g' content/guides/security-response.md
   sed -i 's/P029/U020/g' content/skills/incremental-improvement.md
   sed -i 's/P029/U020/g' content/skills/security-emergency-response.md
   sed -i 's/P029/U020/g' .github/workflows/security.yml.disabled
   ```

4. **Verify:**
   ```bash
   grep -r "P029" --include="*.py" --include="*.md" --include="*.yml" . | grep -v ".git" | grep -v "PRINCIPLE_UPDATE_PLAN.md"
   ```

5. **Commit:**
   ```bash
   git add -A
   git commit -m "refactor(principles): migrate P029 to U020 (universal)

   Moved Secret Management from security_privacy to universal.
   No hardcoded secrets applies to all projects.

   Co-Authored-By: Claude <noreply@anthropic.com>"
   ```

---

### P040 → U021: Dependency Management

**Current State:**
- File: `content/principles/P040.md`
- ID: `P040`
- Category: `security_privacy`

**Target State:**
- File: `content/principles/U021.md`
- ID: `U021`
- Category: `universal`

#### Steps:

1. **Update Frontmatter:**
   ```bash
   sed -i '/^number:/d' content/principles/P040.md
   sed -i 's/^id: P040$/id: U021/' content/principles/P040.md
   sed -i 's/^category: security_privacy$/category: universal/' content/principles/P040.md
   ```

2. **Rename File:**
   ```bash
   git mv content/principles/P040.md content/principles/U021.md
   ```

3. **Update Documentation:**
   ```bash
   sed -i 's/P040: Dependency Management/U021: Dependency Management/g' CLAUDE.md
   sed -i 's/P040\.md/U021\.md/g' CLAUDE.md
   sed -i 's/P040:/U021:/g' content/agents/audit-agent.md
   sed -i 's/P040\.md/U021\.md/g' content/agents/audit-agent.md
   sed -i 's/P040/U021/g' content/commands/audit.md
   sed -i "s/'P040'/'U021'/g" content/commands/fix.md
   sed -i 's/P040/U021/g' content/commands/optimize-deps.md
   sed -i 's/P040/U021/g' content/commands/analyze.md
   sed -i 's/P040/U021/g' content/guides/security-response.md
   sed -i 's/P040/U021/g' .github/workflows/security.yml.disabled
   ```

4. **Verify:**
   ```bash
   grep -r "P040" --include="*.py" --include="*.md" --include="*.yml" . | grep -v ".git" | grep -v "PRINCIPLE_UPDATE_PLAN.md"
   ```

5. **Commit:**
   ```bash
   git add -A
   git commit -m "refactor(principles): migrate P040 to U021 (universal)

   Moved Dependency Management from security_privacy to universal.
   Vulnerability scanning applies to all projects.

   Co-Authored-By: Claude <noreply@anthropic.com>"
   ```

---

### P045 → U022: CI Gates

**Current State:**
- File: `content/principles/P045.md`
- ID: `P045`
- Category: `testing`

**Target State:**
- File: `content/principles/U022.md`
- ID: `U022`
- Category: `universal`

#### Steps:

1. **Update Frontmatter:**
   ```bash
   sed -i '/^number:/d' content/principles/P045.md
   sed -i 's/^id: P045$/id: U022/' content/principles/P045.md
   sed -i 's/^category: testing$/category: universal/' content/principles/P045.md
   ```

2. **Rename File:**
   ```bash
   git mv content/principles/P045.md content/principles/U022.md
   ```

3. **Update Documentation:**
   ```bash
   sed -i 's/P045: CI Gates/U022: CI Gates/g' CLAUDE.md
   sed -i 's/P045\.md/U022\.md/g' CLAUDE.md
   sed -i 's/P045:/U022:/g' content/agents/audit-agent.md
   sed -i 's/P045\.md/U022\.md/g' content/agents/audit-agent.md
   sed -i 's/P045/U022/g' content/agents/generate-agent.md
   sed -i 's/P045/U022/g' content/commands/audit.md
   ```

4. **Verify:**
   ```bash
   grep -r "P045" --include="*.py" --include="*.md" . | grep -v ".git" | grep -v "PRINCIPLE_UPDATE_PLAN.md"
   ```

5. **Commit:**
   ```bash
   git add -A
   git commit -m "refactor(principles): migrate P045 to U022 (universal)

   Moved CI Gates from testing to universal category.
   CI/CD quality gates apply to all modern projects.

   Co-Authored-By: Claude <noreply@anthropic.com>"
   ```

---

## Duplicate Deletion Strategy

### U005 → DELETE (Duplicate of C004: Minimal Touch Policy)

**Analysis:**
- **U005:** Minimal stub (25 lines) - category `universal`
- **C004:** Full detailed version (48 lines, with examples) - category `claude_guidelines`
- **Decision:** Keep C004 (more detailed), delete U005

**Issue:** Category mismatch - C004 is `claude_guidelines` not `universal`

**Two Options:**

#### Option A: Delete U005, Keep C004 as Claude Guideline (RECOMMENDED)

**Rationale:**
- "Minimal Touch Policy" is Claude-specific behavior guidance
- Not a software engineering principle, but AI behavior rule
- Should stay in `claude_guidelines` category
- Universal principles auto-load for all projects
- Claude guidelines loaded differently (for Claude Code behavior)

**Steps:**

1. **Delete U005:**
   ```bash
   git rm content/principles/U005.md
   ```

2. **Update CLAUDE.md:**
   ```bash
   # Move reference from Universal Principles section to Claude Guidelines section
   # Line 18: Remove U005 from universal list
   # Add to Claude Guidelines section instead

   # Manually edit CLAUDE.md:
   # Remove line 18: "- **U005**: Minimal Touch Policy..."
   # Verify C004 is already in Claude Guidelines section
   ```

3. **Update Documentation:**
   ```bash
   # Update references from U005 to C004
   sed -i 's/U005/C004/g' content/commands/init.md
   sed -i 's/U005/C004/g' content/agents/fix-agent.md
   ```

4. **Verify:**
   ```bash
   grep -r "U005" --include="*.py" --include="*.md" . | grep -v ".git" | grep -v "PRINCIPLE_UPDATE_PLAN.md"
   ```

5. **Commit:**
   ```bash
   git add -A
   git commit -m "refactor(principles): remove duplicate U005, keep C004

   Removed U005 (Minimal Touch Policy) as duplicate of C004.
   C004 is more detailed and belongs in claude_guidelines category.

   Rationale:
   - Minimal Touch is AI behavior guidance, not software principle
   - Keep in claude_guidelines (not universal)
   - Updated all references U005→C004

   Co-Authored-By: Claude <noreply@anthropic.com>"
   ```

#### Option B: Delete U005, Move C004 to Universal (ALTERNATIVE)

**Only use if:** Minimal Touch Policy should be universal principle

**Steps:**
1. Delete U005
2. Rename C004→U005
3. Change C004 category to `universal`
4. Update all C004 references to U005

**Not recommended** - This is truly Claude-specific behavior

---

### U006 → DELETE (Duplicate of C011: Model Selection Strategy)

**Analysis:**
- **U006:** Minimal stub (25 lines) - category `universal`
- **C011:** Full detailed version (46 lines, with model types) - category `claude_guidelines`
- **Decision:** Keep C011 (more detailed), delete U006

**Rationale:**
- Model selection is Claude Code specific (Haiku/Sonnet/Opus)
- Not a universal software principle
- Should stay in `claude_guidelines` category

**Steps:**

1. **Delete U006:**
   ```bash
   git rm content/principles/U006.md
   ```

2. **Update CLAUDE.md:**
   ```bash
   # Line 19: Remove U006 from universal list
   # Verify C011 is in Claude Guidelines section
   ```

3. **Update Documentation:**
   ```bash
   sed -i 's/U006/C011/g' docs/features.md
   ```

4. **Verify:**
   ```bash
   grep -r "U006" --include="*.py" --include="*.md" . | grep -v ".git" | grep -v "PRINCIPLE_UPDATE_PLAN.md"
   ```

5. **Commit:**
   ```bash
   git add -A
   git commit -m "refactor(principles): remove duplicate U006, keep C011

   Removed U006 (Model Selection Strategy) as duplicate of C011.
   C011 is more detailed and belongs in claude_guidelines category.

   Rationale:
   - Model selection (Haiku/Sonnet/Opus) is Claude Code specific
   - Keep in claude_guidelines (not universal)
   - Updated all references U006→C011

   Co-Authored-By: Claude <noreply@anthropic.com>"
   ```

---

## Global Documentation Updates

After all principle migrations, update count references:

### Update Universal Principle Count: 14 → 22

**Files with hardcoded "14 Universal" or "U001-U014":**

1. **README.md**
   ```bash
   sed -i 's/14 Universal/22 Universal/g' README.md
   sed -i 's/U001-U014/U001-U022/g' README.md
   ```

2. **docs/features.md**
   ```bash
   sed -i 's/U001-U014/U001-U022/g' docs/features.md
   ```

3. **docs/architecture.md**
   ```bash
   sed -i 's/U001-U014/U001-U022/g' docs/architecture.md
   ```

4. **docs/installation.md**
   ```bash
   sed -i 's/U001-U014/U001-U022/g' docs/installation.md
   ```

5. **docs/tutorial.md**
   ```bash
   sed -i 's/U001-U014/U001-U022/g' docs/tutorial.md
   ```

6. **docs/roadmap.md**
   ```bash
   sed -i 's/U001-U014/U001-U022/g' docs/roadmap.md
   ```

7. **docs/project-structure.md**
   ```bash
   sed -i 's/U001-U014/U001-U022/g' docs/project-structure.md
   sed -i 's/14 universal/22 universal/g' docs/project-structure.md
   sed -i 's/69 project-specific/61 project-specific/g' docs/project-structure.md
   # Note: Total stays 95, but 61 P-series (not 69) after moving 8 to U-series
   ```

8. **claudecodeoptimizer/core/hybrid_claude_md_generator.py**
   ```bash
   sed -i 's/U001-U014/U001-U022/g' claudecodeoptimizer/core/hybrid_claude_md_generator.py
   ```

9. **claudecodeoptimizer/core/principle_md_loader.py:73** (comment)
   ```bash
   sed -i 's/U001-U012/U001-U022/g' claudecodeoptimizer/core/principle_md_loader.py
   ```

10. **content/commands/remove.md:27**
    ```bash
    sed -i 's/U001-U012/U001-U022/g' content/commands/remove.md
    ```

**Commit:**
```bash
git add -A
git commit -m "docs: update universal principle count (14→22)

Updated all references to universal principle count and range
after migration of 8 principles from P-series to U-series.

Changes:
- Universal principles: 14 → 22
- Project-specific principles: 69 → 61
- Total remains: 95 (83 + 12 Claude guidelines)
- Range: U001-U014 → U001-U022

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

## Post-Migration Validation

### ✅ Validation Checklist

Run these checks **in order** after all migrations:

#### 1. File System Checks

```bash
# Check principle count (should be 95)
ls content/principles/*.md | wc -l

# Check U-series count (should be 22)
ls content/principles/U*.md | wc -l

# Check P-series count (should be 61)
ls content/principles/P*.md | wc -l

# Check C-series count (should be 12)
ls content/principles/C*.md | wc -l

# Verify new files exist
ls -la content/principles/{U015,U016,U017,U018,U019,U020,U021,U022}.md

# Verify old files deleted
ls content/principles/{P001,P002,P003,P007,P028,P029,P040,P045,U005,U006}.md 2>&1
# Should show "No such file or directory" for all
```

#### 2. Principle Loading Test

```bash
# Test principle loader
python -c "
from pathlib import Path
from claudecodeoptimizer.core.principle_md_loader import load_all_principles

principles_dir = Path('content/principles')
principles = load_all_principles(principles_dir)

# Count by category
universal = [p for p in principles if p['category'] == 'universal']
code_quality = [p for p in principles if p['category'] == 'code_quality']
claude = [p for p in principles if p['category'] == 'claude_guidelines']

print(f'Total principles: {len(principles)}')
print(f'Universal: {len(universal)} (expected: 22)')
print(f'Code Quality: {len(code_quality)} (expected: reduced)')
print(f'Claude Guidelines: {len(claude)} (expected: 12)')

# Verify new IDs exist
new_ids = ['U015', 'U016', 'U017', 'U018', 'U019', 'U020', 'U021', 'U022']
found_ids = [p['id'] for p in principles if p['id'] in new_ids]
print(f'New IDs found: {len(found_ids)}/8')
print(f'IDs: {found_ids}')

# Verify old IDs deleted
old_ids = ['P001', 'P002', 'P003', 'P007', 'P028', 'P029', 'P040', 'P045', 'U005', 'U006']
remaining = [p['id'] for p in principles if p['id'] in old_ids]
print(f'Old IDs remaining: {len(remaining)} (expected: 0)')
if remaining:
    print(f'ERROR: Found old IDs: {remaining}')
"
```

#### 3. Category Filter Test

```bash
# Test category-based filtering
python -c "
from pathlib import Path
from claudecodeoptimizer.core.principle_md_loader import load_all_principles

principles_dir = Path('content/principles')
principles = load_all_principles(principles_dir)

# Test that new universal principles are in universal category
universal = [p for p in principles if p['category'] == 'universal']
new_universal_ids = ['U015', 'U016', 'U017', 'U018', 'U019', 'U020', 'U021', 'U022']

for uid in new_universal_ids:
    found = any(p['id'] == uid for p in universal)
    print(f'{uid} in universal: {found}')
    if not found:
        print(f'ERROR: {uid} not found in universal category!')
"
```

#### 4. Principle Selector Test

```bash
# Test principle selector logic
python -c "
from claudecodeoptimizer.core.principle_selector import PrincipleSelector
from claudecodeoptimizer.schemas.preferences import CCOPreferences
from pathlib import Path

# Create test preferences
prefs = CCOPreferences(
    project_identity={
        'name': 'test',
        'types': ['backend'],
        'primary_language': 'python',
        'team_trajectory': 'solo',
        'project_maturity': 'production'
    },
    code_quality={'linting_strictness': 'strict'},
    testing={'strategy': 'balanced'},
    security={'stance': 'high'}
)

selector = PrincipleSelector(Path('content/principles'), prefs)
selected = selector.select_principles()

# Check that new universal principles are included
new_ids = ['U015', 'U016', 'U017', 'U018', 'U019', 'U020', 'U021', 'U022']
for uid in new_ids:
    if uid in selected:
        print(f'✓ {uid} selected')
    else:
        print(f'✗ {uid} NOT selected (ERROR!)')
"
```

#### 5. CLAUDE.md Generation Test

```bash
# Test CLAUDE.md generation
python -c "
from pathlib import Path
from claudecodeoptimizer.core.claude_md_generator import ClaudeMdGenerator

prefs = {
    'project_identity': {'name': 'test', 'team_trajectory': 'solo'},
    'code_quality': {'linting_strictness': 'strict'},
    'testing': {'strategy': 'balanced'},
    'selected_principle_ids': ['U015', 'U016', 'U017', 'U018', 'U019', 'U020', 'U021', 'U022']
}

generator = ClaudeMdGenerator(prefs)
output = Path('test_CLAUDE.md')
result = generator.generate(output)

# Verify file was created
if output.exists():
    content = output.read_text()

    # Check for new IDs
    for uid in ['U015', 'U016', 'U017', 'U018', 'U019', 'U020', 'U021', 'U022']:
        if uid in content:
            print(f'✓ {uid} in CLAUDE.md')
        else:
            print(f'✗ {uid} NOT in CLAUDE.md (ERROR!)')

    # Cleanup
    output.unlink()
else:
    print('ERROR: CLAUDE.md not generated')
"
```

#### 6. Search for Orphaned References

```bash
# Final comprehensive search for old IDs
echo "Searching for orphaned old IDs..."
for old_id in P001 P002 P003 P007 P028 P029 P040 P045 U005 U006; do
    echo "Checking $old_id..."
    matches=$(grep -r "$old_id" --include="*.py" --include="*.md" --include="*.json" --include="*.yml" . | grep -v ".git" | grep -v "PRINCIPLE_UPDATE_PLAN.md" | grep -v "pre-migration-state.txt" | wc -l)
    if [ $matches -gt 0 ]; then
        echo "⚠️  Found $matches references to $old_id:"
        grep -r "$old_id" --include="*.py" --include="*.md" --include="*.json" --include="*.yml" . | grep -v ".git" | grep -v "PRINCIPLE_UPDATE_PLAN.md" | grep -v "pre-migration-state.txt"
    else
        echo "✓ No references to $old_id"
    fi
done
```

#### 7. Git Status Check

```bash
# Verify all changes committed
git status --short
# Should be empty (no uncommitted changes)

# Verify commit count
git log --oneline origin/main..HEAD
# Should show ~12 commits (1 bug fix + 8 migrations + 2 deletions + 1 docs update)
```

#### 8. Run Full Test Suite

```bash
# Run all tests
pytest tests/ -v

# Check for any failures
echo $?
# Should be 0 (success)
```

---

## Rollback Plan

If migration fails or causes issues:

### Immediate Rollback

```bash
# Option 1: Revert to pre-migration state
git reset --hard <commit-before-migration>

# Option 2: Revert individual commits
git revert <commit-hash>...

# Option 3: Delete branch and start over
git checkout main
git branch -D principle-categorization-update
```

### Partial Rollback (Individual Principles)

If only one principle causes issues:

```bash
# Example: Rollback U015 (P001) only
git revert <U015-commit-hash>

# Manually fix:
# 1. Rename U015.md back to P001.md
# 2. Update frontmatter (ID, category)
# 3. Update all references back to P001
```

### Recovery Checklist

After rollback:

- [ ] Verify principle count: `ls content/principles/*.md | wc -l` (95)
- [ ] Verify principle loading works
- [ ] Run tests: `pytest tests/`
- [ ] Check CLAUDE.md generation
- [ ] Document what went wrong in GitHub issue

---

## Critical Warnings

### ⚠️ DO NOT:

1. **Don't skip bug fixes** - Fix P002 comment errors FIRST before migration
2. **Don't batch commits** - Commit each principle migration separately (atomic)
3. **Don't forget documentation** - Every code change needs doc update
4. **Don't ignore validation** - Run ALL validation checks before pushing
5. **Don't force push to main** - Use feature branch: `principle-categorization-update`

### ⚠️ BREAKING CHANGES:

This migration introduces **BREAKING CHANGES**:

- **Principle IDs change:** P001→U015, etc.
- **File paths change:** `principles/P001.md` → `principles/U015.md`
- **Categories change:** `code_quality` → `universal`

**Impact on existing projects:**
- Projects using CCO will need to regenerate CLAUDE.md
- Symlinks to old IDs will break
- Custom references to P001, P002, etc. need manual update

**Mitigation:**
- Document breaking changes in CHANGELOG.md
- Add migration guide for users
- Consider version bump: v0.x.y → v0.(x+1).0

---

## Timeline Estimate

**Total Time:** 2-3 hours

- **Bug Fixes:** 15 minutes
- **P→U Migrations:** 90 minutes (8 principles × ~11 minutes each)
- **Duplicate Deletions:** 20 minutes (2 principles × 10 minutes each)
- **Global Docs Update:** 15 minutes
- **Validation:** 30 minutes
- **Buffer:** 30 minutes

**Recommended Schedule:**
1. **Session 1 (1 hour):** Bug fixes + First 4 migrations (P001→U015 through P007→U018)
2. **Session 2 (1 hour):** Next 4 migrations (P028→U019 through P045→U022)
3. **Session 3 (45 min):** Duplicate deletions + Global docs
4. **Session 4 (30 min):** Validation + push

---

## Success Criteria

Migration is successful when:

- ✅ All 8 P-series principles moved to U015-U022
- ✅ All 2 duplicate principles deleted (U005, U006)
- ✅ File count: 95 principles (22 U + 61 P + 12 C)
- ✅ No references to old IDs (P001, P002, etc.)
- ✅ All validation tests pass
- ✅ CLAUDE.md generation includes new universal principles
- ✅ Category filtering works correctly
- ✅ Documentation updated (14→22 universal)
- ✅ All commits atomic and clean
- ✅ Git history clean (no WIP commits)
- ✅ Tests pass: `pytest tests/`

---

## Post-Migration Tasks

After successful migration:

1. **Update CHANGELOG.md:**
   ```markdown
   ## [Unreleased]

   ### Changed (BREAKING)
   - Migrated 8 principles from project-specific to universal category
   - Principle IDs changed: P001→U015, P002→U016, P003→U017, P007→U018,
     P028→U019, P029→U020, P040→U021, P045→U022
   - Universal principle count increased: 14→22
   - Removed duplicate principles: U005, U006

   ### Migration Guide
   Projects using CCO need to regenerate CLAUDE.md:
   - Run: `/cco-init` or `python -m claudecodeoptimizer init`
   - Update any custom references to old principle IDs
   ```

2. **Create Migration Guide:**
   - `docs/migration-guide-v0.x.md`
   - Document ID changes
   - Provide sed commands for bulk updates
   - Examples of affected workflows

3. **Version Bump:**
   ```bash
   # Update version (breaking change = minor bump in 0.x)
   # 0.9.0 → 0.10.0
   python -m claudecodeoptimizer.core.version_manager bump minor
   ```

4. **Create GitHub Release:**
   - Tag: `v0.10.0`
   - Title: "Principle Categorization Refactor"
   - Notes: Link to CHANGELOG and migration guide

5. **Notify Users:**
   - GitHub Discussions post
   - Update README.md with migration note
   - Consider deprecation warning in next release

---

## Contact & Support

**Questions during migration?**
- Review this plan thoroughly before starting
- Check validation outputs at each step
- Use `git status` frequently
- Commit atomically (one principle per commit)
- Test after each migration

**If issues occur:**
- Don't panic - use rollback plan
- Document the issue in GitHub
- Check validation section for troubleshooting

---

## Appendix A: Quick Reference Commands

### Complete Migration Script (All-in-One)

**⚠️ USE WITH CAUTION** - Better to run step-by-step!

```bash
#!/bin/bash
set -e  # Exit on error

echo "Starting principle migration..."

# Bug fixes first
echo "Fixing P002 comment bugs..."
sed -i 's/P002 (DRY Enforcement)/P001 (DRY Enforcement)/g' claudecodeoptimizer/core/constants.py
sed -i 's/P002 - DRY Enforcement/P001 - DRY Enforcement/g' claudecodeoptimizer/core/constants.py
sed -i 's/P002 - DRY Enforcement/P001 - DRY Enforcement/g' claudecodeoptimizer/core/utils.py
git add claudecodeoptimizer/core/constants.py claudecodeoptimizer/core/utils.py
git commit -m "fix(principles): correct P002→P001 references in comments"

# Migrate each principle (example for P001→U015)
migrate_principle() {
    local OLD_ID=$1
    local NEW_ID=$2
    local OLD_FILE="content/principles/${OLD_ID}.md"
    local NEW_FILE="content/principles/${NEW_ID}.md"

    echo "Migrating ${OLD_ID} → ${NEW_ID}..."

    # Update frontmatter
    sed -i "s/^id: ${OLD_ID}$/id: ${NEW_ID}/" "$OLD_FILE"
    sed -i 's/^category: [a-z_]*$/category: universal/' "$OLD_FILE"

    # Rename file
    git mv "$OLD_FILE" "$NEW_FILE"

    # Update references (simplified)
    find . -type f \( -name "*.py" -o -name "*.md" \) -exec sed -i "s/${OLD_ID}/${NEW_ID}/g" {} +

    # Commit
    git add -A
    git commit -m "refactor(principles): migrate ${OLD_ID} to ${NEW_ID} (universal)"
}

# Run migrations
migrate_principle "P001" "U015"
migrate_principle "P002" "U016"
migrate_principle "P003" "U017"
migrate_principle "P007" "U018"
migrate_principle "P028" "U019"
migrate_principle "P029" "U020"
migrate_principle "P040" "U021"
migrate_principle "P045" "U022"

# Delete duplicates
git rm content/principles/U005.md
git rm content/principles/U006.md
git add -A
git commit -m "refactor(principles): remove duplicates U005, U006"

# Update global docs
find . -type f -name "*.md" -exec sed -i 's/U001-U014/U001-U022/g' {} +
find . -type f -name "*.md" -exec sed -i 's/14 Universal/22 Universal/g' {} +
git add -A
git commit -m "docs: update universal principle count (14→22)"

echo "Migration complete! Run validation checks."
```

---

## Appendix B: Regex Patterns for Finding References

### Search Patterns

```bash
# Find all principle ID references
grep -rE "\b[PUC][0-9]{3}\b" --include="*.py" --include="*.md" .

# Find principle file paths
grep -r "principles/P[0-9]*.md" --include="*.py" --include="*.md" .

# Find category filters
grep -r "category.*==.*['\"]code_quality['\"]" --include="*.py" .
grep -r "category.*==.*['\"]security_privacy['\"]" --include="*.py" .
grep -r "category.*==.*['\"]testing['\"]" --include="*.py" .

# Find principle counts
grep -rE "[0-9]+ (universal|Universal)" --include="*.md" .
grep -r "U001-U014" --include="*.py" --include="*.md" .
```

---

## Appendix C: File Modification Summary

**Total Files Affected:** ~50 files

### Python Files (Code Logic)
- `claudecodeoptimizer/core/constants.py` - Bug fix + no P001 refs
- `claudecodeoptimizer/core/utils.py` - Bug fix + no P001 refs
- `claudecodeoptimizer/core/principles.py` - Update P001→U015
- `claudecodeoptimizer/core/principle_loader.py` - Update examples
- `claudecodeoptimizer/core/principle_md_loader.py` - Update examples, comments
- `claudecodeoptimizer/core/hybrid_claude_md_generator.py` - Update U001-U014→U001-U022

### Markdown Files (Documentation)
- `CLAUDE.md` - Update all 8 principle references + counts
- `README.md` - Update universal count
- `docs/features.md` - Update U001-U014→U001-U022
- `docs/architecture.md` - Update all refs
- `docs/installation.md` - Update range
- `docs/tutorial.md` - Update range
- `docs/roadmap.md` - Update range
- `docs/project-structure.md` - Update counts
- `content/agents/audit-agent.md` - Update all principle refs
- `content/agents/fix-agent.md` - Update all principle refs
- `content/agents/generate-agent.md` - Update P007→U018
- `content/commands/*.md` - Update refs in all command files
- `content/guides/security-response.md` - Update security principle refs
- `content/skills/*.md` - Update refs in relevant skills
- `content/principles/U013.md` - Cross-reference P002→U016

### Configuration Files
- `.github/workflows/security.yml.disabled` - Update P029→U020, P040→U021

### Principle Files (Renamed)
- `content/principles/P001.md` → `U015.md`
- `content/principles/P002.md` → `U016.md`
- `content/principles/P003.md` → `U017.md`
- `content/principles/P007.md` → `U018.md`
- `content/principles/P028.md` → `U019.md`
- `content/principles/P029.md` → `U020.md`
- `content/principles/P040.md` → `U021.md`
- `content/principles/P045.md` → `U022.md`

### Principle Files (Deleted)
- `content/principles/U005.md` ❌
- `content/principles/U006.md` ❌

---

**END OF PLAN**

---

*This plan is comprehensive and ready for execution in a future session. Follow steps sequentially, commit atomically, and validate continuously.*

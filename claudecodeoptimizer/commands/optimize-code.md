---
id: cco-cleanup-dead-code
description: Remove unused code, imports, and deprecated markers
category: quality
priority: medium
---

# Cleanup Dead Code

You are removing unused code from **${PROJECT_NAME}**.

**Project Type:** ${PROJECT_TYPE}
**Primary Language:** ${PRIMARY_LANGUAGE}

## Objective

Detect and remove dead code:
1. Unused functions/classes
2. Orphaned imports
3. Unreachable code
4. @deprecated markers
5. TODO/FIXME markers (production-ready code only)

**Output:** Clean codebase with git backup for safety.

---

## Step 1: Git Backup

**CRITICAL:** Create backup before any deletions!

```bash
git stash push -m "CCO cleanup dead code backup $(date +%Y%m%d_%H%M%S)"
```

---

## Step 2: Remove Unused Imports

**Python:**
```bash
# Use ruff to detect and remove
ruff check --select F401 --fix .

# Show what was removed
git diff --stat
```

**JavaScript/TypeScript:**
```bash
# Use eslint
npx eslint --fix --rule 'no-unused-vars: error' .
```

---

## Step 3: Find Unused Functions/Classes

**Python (using vulture):**
```bash
# Install if needed
pip install vulture

# Find dead code
vulture . --min-confidence 80

# Review and manually delete
```

**Manual Detection:**
```bash
# Find functions that are never called
# 1. List all function definitions
Grep("^def \\w+\\(", glob="**/*.py", output_mode="content")

# 2. For each function, search if it's called anywhere
# If no matches found (except definition), it's unused
```

---

## Step 4: Remove Unreachable Code

Detect unreachable code after return/raise:

```bash
Grep("return\\s*.*\\n\\s+[^#]|raise\\s*.*\\n\\s+[^#]", glob="**/*.py", output_mode="content", multiline=true, -A=5)
```

**Example:**
```python
# BAD - Unreachable code
def process():
    return result
    print("This will never execute")  # Dead code

# GOOD
def process():
    return result
```

Use Edit tool to remove unreachable lines.

---

## Step 5: Remove @deprecated Markers

Find and remove deprecated code:

```bash
Grep("@deprecated|@Deprecated|# DEPRECATED", output_mode="content", -C=10)
```

**For each deprecated item:**
1. Verify no other code references it
2. If unused, delete entire function/class
3. If used, keep and warn user

---

## Step 6: Remove TODO/FIXME Markers

**Only for production code!** Development code may keep TODOs.

```bash
Grep("TODO:|FIXME:|XXX:|HACK:", output_mode="content", -C=3)
```

**For each TODO:**
- If trivial, fix it immediately
- If complex, create GitHub issue and remove TODO
- If outdated, just remove

**Example:**
```python
# BAD - Production code
def process():
    # TODO: Add error handling
    return result

# GOOD
def process():
    # Proper implementation without TODOs
    try:
        return result
    except Exception as e:
        logger.error(f"Failed: {e}")
        raise
```

---

## Step 7: Remove Debug/Print Statements

Find debugging code that shouldn't be in production:

```bash
# Python
Grep("print\\(|pprint\\(|pp\\(|console\\.log\\(", output_mode="content", -C=2)

# Filter out legitimate logging
# Look for patterns like: print(f"DEBUG: ...")
```

**Remove:**
- `print("debug:", ...)`
- `console.log("test")`
- `pprint(obj)` for debugging

**Keep:**
- Proper logging: `logger.info(...)`
- CLI output: `print(result)` in CLI tools

---

## Step 8: Clean Up Empty Files/Classes

Find empty or near-empty files:

```bash
# Find files with < 5 lines (likely empty)
find . -name "*.py" -exec wc -l {} \; | awk '$1 < 5 {print $2}'

# Find empty classes
Grep("^class \\w+.*:\\s*pass\\s*$", glob="**/*.py", output_mode="content", multiline=true)
```

**For each empty item:**
- If truly empty, delete file
- If has pass statement only, delete class
- Update imports that referenced deleted code

---

## Step 9: Verification

Run tests to ensure nothing broke:

```bash
# Run test suite
pytest

# If tests fail, rollback
if [ $? -ne 0 ]; then
    echo "Tests failed! Rolling back..."
    git reset --hard HEAD
    git stash pop
    exit 1
fi
```

---

## Step 10: Summary Report

```
=== Dead Code Cleanup Summary ===

Project: ${PROJECT_NAME}

Removed:
- Unused imports: 23 imports
- Unused functions: 5 functions
- Unreachable code: 8 blocks
- Deprecated code: 3 functions
- TODO markers: 12 markers
- Debug prints: 15 statements
- Empty files: 2 files

Files Modified: 34
Lines Deleted: 456

Verification:
✓ Tests passed
✓ Git backup: stash@{0}

Next Steps:
1. Review changes: git diff
2. Commit: git commit -m "Clean up dead code"
3. Rollback if needed: git reset --hard HEAD && git stash pop
```

---

## Safety Guidelines

✅ **Safe to remove:**
- Unused imports (auto-detected by tools)
- Unreachable code after return/raise
- Empty files with no references
- Debug print statements

⚠️ **Verify before removing:**
- Functions (may be called dynamically)
- Classes (may be used via reflection)
- TODOs (may indicate incomplete work)

❌ **Never remove:**
- Code referenced from other files
- Public API functions (even if unused internally)
- Code that may be called externally

---

## Anti-Patterns

❌ **Deleting without backup** - Always git stash first

❌ **Removing public APIs** - May break external users

❌ **Bulk deletion** - Review each item individually

❌ **Skipping tests** - Must verify nothing broke

---

## Output Example

```
=== Dead Code Cleanup ===

Project: safescribe
Language: python

Creating backup...
✓ Git stash: stash@{0}

[1/7] Removing unused imports...
  ruff check --select F401 --fix .
  ✓ 23 imports removed

[2/7] Finding unused functions...
  vulture . --min-confidence 80
  Found 5 unused functions:
  - shared/legacy.py:old_process_audio (unused)
  - services/worker/deprecated.py:old_transcribe (unused)
  ✓ 5 functions deleted

[3/7] Removing unreachable code...
  ✓ 8 blocks removed

[4/7] Removing deprecated code...
  ✓ 3 @deprecated functions deleted

[5/7] Removing TODO markers...
  ✓ 12 TODOs removed or fixed

[6/7] Removing debug prints...
  ✓ 15 print statements removed

[7/7] Removing empty files...
  ✓ 2 empty files deleted

Verification...
  pytest -q
  ✓ 127 passed in 11.2s

Summary:
- 34 files modified
- 456 lines deleted
- 0 tests broken

Review: git diff
Commit: git commit -m "Clean up dead code: imports, functions, TODOs, debug prints"
```

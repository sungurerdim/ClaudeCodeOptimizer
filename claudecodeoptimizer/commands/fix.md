---
description: Auto-fix issues (code, security, docs, tests)
category: quality
cost: 4
---

# CCO Fix Commands

Automatically fix issues found in audits: code quality, security vulnerabilities, documentation, and flaky tests.

## Prerequisites: Load Required Context

**CRITICAL**: Before running any fix, load and verify required documents.

```python
from pathlib import Path

print("📚 Loading CCO Context for Fixes...\n")

# Load core documents
loaded_docs = []

# CLAUDE.md
claude_md = Path("CLAUDE.md")
if claude_md.exists():
    tokens = len(claude_md.read_text(encoding="utf-8")) // 4
    loaded_docs.append(("CLAUDE.md", tokens))
    print(f"✓ Loaded CLAUDE.md (~{tokens:,} tokens)")

# PRINCIPLES.md
principles_md = Path("PRINCIPLES.md")
if principles_md.exists():
    tokens = len(principles_md.read_text(encoding="utf-8")) // 4
    loaded_docs.append(("PRINCIPLES.md", tokens))
    print(f"✓ Loaded PRINCIPLES.md (~{tokens:,} tokens)")

total_tokens = sum(t for _, t in loaded_docs)
print(f"\n📊 Core context: ~{total_tokens:,} tokens\n")
```

---

## Step 1: Select Fix Types

**Use AskUserQuestion tool** to ask which fixes to apply:

```json
{
  "questions": [{
    "question": "Which fixes would you like to apply?",
    "header": "Fix Selection",
    "multiSelect": true,
    "options": [
      {"label": "Code Quality", "description": "Auto-fix formatting, linting, type errors (black, ruff, prettier, etc.)"},
      {"label": "Security", "description": "Fix security vulnerabilities and remove hardcoded secrets"},
      {"label": "Documentation", "description": "Update outdated docs, add missing docstrings"},
      {"label": "Flaky Tests", "description": "Fix non-deterministic tests and race conditions"}
    ]
  }]
}
```

**All options selected by default.**

---

## Step 2: Run Selected Fixes

**⚠️ CRITICAL: Safe Fix Workflow**

All fixes follow this pattern:
1. **Git Backup**: Create safety branch
2. **Apply Fixes**: Run auto-fix tools
3. **Verify**: Run tests
4. **Rollback**: If tests fail, revert changes

---

## Fix: Code Quality

**Auto-fix formatting, linting, and type errors**

### Safety Backup

```bash
git stash
git checkout -b cco-fix-code-backup-$(date +%s)
git stash pop
```

### Run Auto-Fixes

**Python:**
```bash
black .
ruff check --fix .
```

**JavaScript/TypeScript:**
```bash
prettier --write .
eslint --fix .
```

**Go:**
```bash
gofmt -w .
goimports -w .
```

**Rust:**
```bash
rustfmt --edition 2021 .
```

### Verify Changes

```bash
# Run tests
pytest  # or npm test, go test, cargo test

# Check if tests pass
if [ $? -eq 0 ]; then
  echo "✓ Tests passed - fixes applied successfully"
else
  echo "✗ Tests failed - rolling back"
  git checkout main
  git branch -D cco-fix-code-backup-*
fi
```

### Output

- Files modified count
- Issues fixed count
- Test results
- Rollback status if needed

---

## Fix: Security

**Fix security vulnerabilities and remove secrets**

### Safety Backup

```bash
git checkout -b cco-fix-security-backup-$(date +%s)
```

### Fix Types

1. **Remove Hardcoded Secrets**
   - Scan for API keys, passwords, tokens
   - Move to environment variables
   - Update .gitignore

2. **Fix SQL Injection**
   - Replace string concatenation with parameterized queries
   - Example: `f"SELECT * FROM users WHERE id={user_id}"` → `cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))`

3. **Add Input Validation**
   - Validate user inputs
   - Sanitize HTML/SQL
   - Add length/type checks

4. **Fix XSS Vulnerabilities**
   - Escape user-generated content
   - Use safe rendering methods

5. **Implement HTTPS**
   - Update URLs from http:// to https://
   - Add security headers

### Implementation

**Use Task tool with explicit model selection:**

**Security Fix Agent:**
```
Subagent Type: Plan
Model: sonnet
Description: Fix security vulnerabilities

MUST LOAD FIRST:
1. @CLAUDE.md (Security section)
2. @~/.cco/knowledge/guides/security-response.md
3. @docs/cco/principles/security.md
4. Print: "✓ Loaded 3 docs (~3,500 tokens)"

Task: Fix security vulnerabilities systematically

Steps:
1. Load audit findings (if available from /cco-audit security)
2. Categorize vulnerabilities by type:
   - Hardcoded secrets → Move to environment variables
   - SQL injection → Use parameterized queries
   - XSS → Add output escaping
   - Missing HTTPS → Update config
3. Apply fixes category by category (not one-by-one)
4. Verify each fix doesn't break functionality:
   - Run relevant tests after each category
   - Check that code still compiles/runs
5. Run security audit again to confirm fixes

Why Sonnet:
- Complex security fixes require reasoning
- Need to understand attack vectors
- Must preserve functionality while hardening
- Requires careful testing strategy
```

### Verify

```bash
# Re-run security audit
/cco-audit security

# Run tests
pytest

# If tests fail → rollback
```

---

## Fix: Documentation

**Update outdated docs and add missing docstrings**

### Safety Backup

```bash
git checkout -b cco-fix-docs-backup-$(date +%s)
```

### Fix Types

1. **Update README**
   - Update installation steps
   - Fix broken links
   - Add missing sections

2. **Add Missing Docstrings**
   - Python: Add Google-style docstrings
   - JavaScript: Add JSDoc comments
   - Go: Add Go doc comments

3. **Fix Outdated API Docs**
   - Update parameter descriptions
   - Fix return type documentation
   - Update examples

4. **Sync Code with Docs**
   - Update docs to match current code behavior
   - Remove deprecated API references

### Implementation

**Use Task tool with model selection:**

**Documentation Fix Agent:**
```
Subagent Type: Plan
Model: haiku
Description: Fix documentation issues

MUST LOAD FIRST:
1. @CLAUDE.md (Documentation section)
2. @docs/cco/principles/code-quality.md (Docstring principles)
3. Print: "✓ Loaded 2 docs (~2,100 tokens)"

Task: Fix documentation issues systematically

For each doc issue found in audit:
1. Read current documentation (README, docstrings, API docs)
2. Read corresponding code implementation
3. Update documentation to match actual code behavior
4. Verify code examples work (run them if possible)
5. Check all links are valid (no 404s)
6. Update outdated version references
7. Fix formatting issues

Why Haiku:
- Documentation fixes are straightforward
- Mostly reading and writing text
- No complex reasoning required
- Faster and cheaper for simple edits
```

### Verify

```bash
# Build docs (if applicable)
mkdocs build  # or sphinx-build, etc.

# Run tests (examples in docs)
pytest --doctest-modules
```

---

## Fix: Flaky Tests

**Fix non-deterministic and unreliable tests**

### Safety Backup

```bash
git checkout -b cco-fix-tests-backup-$(date +%s)
```

### Common Flaky Test Causes

1. **Race Conditions**
   - Add proper synchronization
   - Use await/locks/mutexes

2. **Time-Dependent Tests**
   - Mock time/dates
   - Use fixed timestamps

3. **Random Data**
   - Seed random generators
   - Use deterministic test data

4. **External Dependencies**
   - Mock external APIs
   - Use test fixtures

5. **Order Dependencies**
   - Make tests independent
   - Clean up state between tests

### Implementation

**Use Task tool with model selection:**

**Flaky Test Fix Agent:**
```
Subagent Type: Explore
Model: sonnet
Description: Fix flaky tests

MUST LOAD FIRST:
1. @CLAUDE.md (Testing section)
2. @docs/cco/principles/testing.md
3. Print: "✓ Loaded 2 docs (~1,900 tokens)"

Task: Fix flaky tests systematically

For each flaky test (from audit):
1. Identify root cause by analyzing test code:
   - Timing issues: Missing waits, race conditions
   - Randomness: Unseeded random generators
   - External dependencies: APIs, databases, filesystem
   - State leakage: Shared mutable state between tests
   - Order dependencies: Tests passing in one order, failing in another

2. Apply appropriate fix pattern:
   - Timing: Add explicit waits, use async/await properly
   - Randomness: Seed random generators with fixed values
   - External: Mock external dependencies
   - State: Isolate tests, proper teardown
   - Order: Make tests independent

3. Verify fix by running test 20 times:
   - Must pass all 20 runs
   - If fails even once, fix is incomplete

4. Document fix in test comments:
   - Explain what was flaky
   - Why the fix works
   - How to avoid similar issues

Why Sonnet:
- Requires deep understanding of test behavior
- Root cause analysis needs reasoning
- Must design appropriate fix pattern
- Complex debugging involved
```

### Verify

```bash
# Run flaky tests 20 times
for i in {1..20}; do
  pytest path/to/flaky_test.py
  if [ $? -ne 0 ]; then
    echo "✗ Still flaky after $i runs"
    exit 1
  fi
done

echo "✓ Test stable across 20 runs"
```

---

## Step 3: Final Summary

After all selected fixes:

```
============================================================
FIX SUMMARY
Project: ${PROJECT_NAME}
============================================================

Fixes Applied:
✓ Code Quality:    15 issues fixed
✓ Security:        3 vulnerabilities patched
✓ Documentation:   8 docs updated
✓ Tests:           2 flaky tests fixed

Tests Status:      ✓ All passing
Git Status:        ✓ Changes committed to fix branch

Next Steps:
1. Review changes: git diff main
2. Merge if satisfied: git checkout main && git merge cco-fix-*
3. Run full audit: /cco-audit all
============================================================
```

---

## Rollback Procedure

If anything goes wrong:

```bash
# Return to main branch
git checkout main

# Delete fix branch
git branch -D cco-fix-*-backup-*

echo "✓ Rolled back to clean state"
```

---

## Error Handling

- **Tests fail after fix**: Automatic rollback
- **Tool not found**: Skip that fix, note in report
- **Git not available**: Refuse to run (no safety backup)
- **Uncommitted changes**: Stash before starting

---

## Related Commands

- `/cco-audit` - Run audits to find issues
- `/cco-generate tests` - Generate missing tests
- `/cco-config` - Configure auto-fix preferences

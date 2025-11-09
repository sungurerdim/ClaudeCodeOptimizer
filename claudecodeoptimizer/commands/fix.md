---
description: Auto-fix issues (code, security, docs, tests)
category: quality
cost: 3
---

# CCO Fix Commands

Automatically fix issues found in audits: code quality, security vulnerabilities, documentation, and flaky tests.

---

## Architecture & Model Selection

**Hybrid approach for optimal speed + quality**

**Data Gathering**: Haiku (Explore agent, quick)
- Fast file scanning, pattern detection
- Identify issues to fix across codebase
- Cost-effective for repetitive operations

**Analysis & Reasoning**: Sonnet (Plan agent)
- Complex analysis for security fixes
- Reasoning required for flaky test fixes
- Synthesis of findings and fix strategies

**Direct Tools**: Bash (instant)
- Code quality fixes (black, ruff, prettier) - no AI needed
- Deterministic linting/formatting operations

**Execution Pattern**:
1. Scan codebase with Haiku agents (parallel)
2. Apply bash tools for code quality (instant)
3. Use Sonnet for security and test fixes (reasoning)
4. Aggregate results and generate report

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
      {"label": "Code Quality", "description": "Auto-fix formatting, linting, type errors (bash tools - instant)"},
      {"label": "Security", "description": "Fix security vulnerabilities and remove hardcoded secrets (Sonnet - reasoning)"},
      {"label": "Documentation", "description": "Update outdated docs, add missing docstrings (Haiku - fast)"},
      {"label": "Flaky Tests", "description": "Fix non-deterministic tests and race conditions (Sonnet - analysis)"}
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

**Method:** Bash tools (no AI agents - instant execution)

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

**Why Bash Tools:** Code quality fixes are deterministic transformations. No AI reasoning needed - use native tools for instant execution.

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

**Method:** Sonnet Plan agent (reasoning required for security decisions)

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

Use Task tool (Sonnet Plan agent):

```
Task: Fix security vulnerabilities
Agent: Plan
Model: sonnet
Thoroughness: high

1. Scan for vulnerabilities (use audit-security results)
2. Apply fixes category by category
3. Verify each fix doesn't break functionality
4. Run security audit again to confirm fixes

Reasoning required:
- Identify appropriate fix for each vulnerability type
- Ensure fixes don't break existing functionality
- Design secure alternatives (env vars, parameterized queries)
- Balance security improvements with code maintainability
- Understand attack vectors and proper mitigations
```

**Why Sonnet:** Security fixes require understanding vulnerabilities, attack vectors, and secure coding patterns. Wrong fixes can introduce new vulnerabilities or break functionality.

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

**Method:** Haiku Explore agent (fast data updates)

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

Use Task tool (Haiku Explore agent):

```
Task: Fix documentation issues
Agent: Explore
Model: haiku
Thoroughness: quick

For each doc issue found in audit:
1. Read current documentation
2. Read corresponding code
3. Update documentation to match code
4. Verify examples work
5. Check links are valid
```

**Why Haiku:** Documentation fixes are mostly data updates - read code, update docs to match. No complex reasoning required, fast execution for many doc updates.

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

**Method:** Sonnet Explore agent (root cause analysis required)

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

Use Task tool (Sonnet Explore agent):

```
Task: Fix flaky tests
Agent: Explore
Model: sonnet
Thoroughness: high

For each flaky test (from audit):
1. Identify root cause (timing, randomness, state, etc.)
2. Apply appropriate fix pattern
3. Run test 10 times to verify stability
4. Document fix in test comments

Reasoning required:
- Analyze test failures to identify root cause
- Understand timing/synchronization issues
- Design proper mocking strategy
- Ensure fix doesn't mask real bugs
- Verify test still validates intended behavior
```

**Why Sonnet:** Flaky test fixes require deep analysis of root causes (race conditions, timing issues, state management). Wrong fixes can mask real bugs or create false positives.

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
✓ Code Quality:    15 issues fixed [Bash tools - instant]
✓ Security:        3 vulnerabilities patched [Sonnet - reasoning]
✓ Documentation:   8 docs updated [Haiku - fast]
✓ Tests:           2 flaky tests fixed [Sonnet - analysis]

Tests Status:      ✓ All passing
Git Status:        ✓ Changes committed to fix branch

Performance:
- Code quality: Instant (bash tools)
- Documentation: 2-3x faster (Haiku vs Sonnet)
- Security/Tests: High quality reasoning (Sonnet)

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

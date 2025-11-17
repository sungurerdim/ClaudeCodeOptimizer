# cco-fix

**Automated issue resolution with safe/risky categorization and auto-audit dependency.**

---

## Purpose

Automatically fix issues found by audits. Runs audit first if no recent audit exists. Categorizes fixes into safe (auto-apply) and risky (require approval).

---

## 17 Fix Categories (Same as Audit)

All categories from `/cco-audit`:
- --security, --tech-debt, --ai-security (🔴 Critical)
- --tests, --integration (🟡 High)
- --code-quality, --docs, --database, --observability, --monitoring, --cicd, --containers, --supply-chain, --migrations, --performance, --architecture, --git (🟢 Medium)

Each category uses same skills as corresponding audit category.

---

## Safe vs Risky Fixes

### Safe Fixes (✓ Auto-Applied)

Fixes that are low-risk and reversible:
- Parameterize SQL queries (SQL injection fix)
- Remove unused imports
- Remove dead code (unreachable, unused functions)
- Fix typos in comments/docstrings
- Add missing type hints
- Format code with Black/Prettier
- Fix linting issues
- Move secrets to environment variables
- Add input validation
- Fix simple logic bugs (obvious off-by-one)
- Update outdated dependencies (patch versions only)
- Add missing docstrings
- Add .gitignore entries
- Fix AI prompt injection (add sanitization)

### Risky Fixes (⚠️ Require Approval)

Fixes that could break functionality:
- Add CSRF protection (modifies forms, sessions)
- Change authentication (JWT, OAuth)
- Refactor complex functions
- Database schema changes
- Add caching layer (Redis, Memcached)
- Change API contracts
- Major dependency updates (minor/major versions)
- Architectural changes
- Add monitoring/logging (if changes code flow)
- Add rate limiting (could affect users)
- Implement circuit breakers
- Migration scripts

---

## Auto-Audit Dependency

**Before fixing, check for recent audit:**

```python
def fix(category):
    # Check if audit results exist and are recent (<10 min old)
    if not has_recent_audit(category, max_age=600):
        print(f"No recent {category} audit found.")
        print(f"Running /cco-audit --{category} first...\n")

        # Run audit
        run_audit(category)

    # Get audit results
    issues = get_audit_results(category)

    if not issues:
        print(f"No issues found in {category} audit.")
        print("Nothing to fix! ✓")
        return

    # Categorize fixes
    safe_fixes, risky_fixes = categorize_fixes(issues)

    # Present and apply
    present_and_apply(safe_fixes, risky_fixes)
```

---

## Execution Protocol

### Step 1: Check for Recent Audit

```markdown
Checking for recent [category] audit...
```

If no recent audit (< 10 minutes):
```markdown
No recent audit found.
Running /cco-audit --[category] first...

[Audit runs and presents results]
```

If recent audit exists:
```markdown
Found recent audit results (5 minutes ago)
Using existing results...
```

### Step 2: Categorize Fixes

Analyze each issue and categorize:

```python
safe = []
risky = []

for issue in issues:
    if is_safe_fix(issue):
        safe.append(issue)
    else:
        risky.append(issue)
```

### Step 3: Present Fix Plan

```markdown
[Category] Fix Plan:

I can fix automatically:

Safe Fixes (✓ will auto-apply):
1. Parameterize SQL in api/users.py:45
   Issue: String concatenation in query
   Fix: cur.execute("SELECT * FROM users WHERE id = %s", (id,))
   Skill: cco-skill-security-owasp

2. Move API_KEY to environment (config.py:12)
   Issue: Hardcoded secret
   Fix: Load from os.environ['API_KEY']
   Skill: cco-skill-security-owasp

3. Fix AI prompt injection (api/chat.py:67)
   Issue: Direct user input to LLM
   Fix: Add sanitization + output validation
   Skill: cco-skill-ai-security-promptinjection

4-6. [More safe fixes...]

Risky Fixes (⚠️ need individual approval):
7. Add CSRF protection to forms (modifies 10 files)
   Issue: No CSRF tokens
   Impact: Adds dependency, modifies all forms
   Risk: Could break existing form submissions

8. Update authentication to JWT (breaks sessions)
   Issue: Session-based auth not scalable
   Impact: Breaking change for active sessions
   Risk: All users logged out, integration changes

Apply [6] safe fixes automatically? (yes/no/customize)
```

### Step 4: Apply Safe Fixes

If user confirms:

1. **Use TodoWrite** to track fixes
2. **Launch Task with cco-agent-fix**:

```python
Task({
  subagent_type: "general-purpose",
  model: "sonnet",  # Use Sonnet for accuracy
  prompt: """
  Apply these safe security fixes:

  1. api/users.py:45 - Parameterize SQL query
  2. config.py:12 - Move API_KEY to environment
  3. api/chat.py:67 - Add AI input sanitization

  For each fix:
  - Read the file
  - Apply the fix using Edit tool
  - Verify the fix (grep for old pattern = 0 results)
  - Report completion with file:line reference

  Use these skills:
  - cco-skill-security-owasp-xss-sqli-csrf
  - cco-skill-ai-security-promptinjection-models

  Follow U_CHANGE_VERIFICATION protocol.
  """
})
```

3. **Report completion:**

```markdown
Applied 6 safe fixes:
✓ api/users.py:45 (SQL parameterization)
✓ api/posts.py:23 (SQL parameterization)
✓ config.py:12 + .env.example (externalized API_KEY)
✓ auth.py:5 (externalized PASSWORD)
✓ api/register.py:30 (added input validation)
✓ api/chat.py:67 (AI security fix)

Verification:
✓ grep -r "execute.*%" . → 0 results (no more string interpolation)
✓ grep -r "API_KEY.*=" config.py → 0 results (no hardcoded key)
✓ All changes follow U_CHANGE_VERIFICATION protocol
```

### Step 5: Handle Risky Fixes Individually

For each risky fix:

```markdown
Risky Fix #7: Add CSRF Protection

What will change:
- Add 'flask-wtf' to requirements.txt
- Add SECRET_KEY to config (environment variable)
- Modify 10 template files (add csrf_token)
- Modify 5 form handlers (validate csrf)
- Update tests (8 test files)

Impact:
- BREAKING CHANGE: Existing form submissions will fail
- Migration: Frontend must include CSRF tokens
- Benefit: Prevents Cross-Site Request Forgery attacks

This addresses Pain #1 (51% security concern).

Time to apply: ~5 minutes
Risk level: MEDIUM (can be reverted)

Proceed with this fix? (yes/no/details)
```

If yes:
- Apply fix using cco-agent-fix
- Verify changes
- Report completion
- Recommend testing

If no:
- Skip to next risky fix
- Note skipped fix for user reference

### Step 6: Impact Summary

```markdown
Fix Summary:

Applied:
✓ 6 safe fixes (auto-applied)
✓ 2 risky fixes (user approved)
✗ 1 risky fix (user skipped)

Results:
- Security score: 45 → 85 (+40 points)
- Vulnerabilities: 20 → 3 (85% reduction)
- Files modified: 15
- Lines changed: +234 / -89

Pain Point Impact:
✓ Addresses Pain #1 (51% security concern)
✓ Risk reduced: 85%
✓ Compliance improved: 40 points

Remaining Issues:
- 3 vulnerabilities require manual review
- 1 risky fix skipped (CSRF protection)

Next Steps:
1. Test changes: pytest tests/
2. Review git diff before committing
3. Address remaining issues manually
4. Run /cco-audit --security to verify

Recommended:
/cco-commit (generates semantic commit messages)
```

---

## Agent Usage

**Agent:** `cco-agent-fix` (Sonnet for code changes)

**Why Sonnet:**
- Higher accuracy for code modifications
- Better contextual understanding
- Safer refactoring and fixes
- Worth the extra cost for correctness

**Parallel Execution Pattern:**
```python
# Example: Fixing multiple independent issues in parallel

# Safe fixes that can run in parallel (independent files)
Task({
  subagent_type: "general-purpose",
  model: "sonnet",
  description: "Fix SQL injection in api/users.py",
  prompt: "Parameterize SQL query at api/users.py:45..."
})
Task({
  subagent_type: "general-purpose",
  model: "sonnet",
  description: "Fix SQL injection in api/posts.py",
  prompt: "Parameterize SQL query at api/posts.py:23..."
})
Task({
  subagent_type: "general-purpose",
  model: "sonnet",
  description: "Externalize secrets from config.py",
  prompt: "Move API_KEY and PASSWORD to environment variables..."
})

# All run in parallel since they modify different files
# Total time: ~10s (vs 30s sequential)
# No cost savings (all Sonnet), but 3x faster

# Sequential execution needed when files depend on each other:
# 1. Update interface definition first
# 2. Then update all implementations
# 3. Then update tests
```

---

## Skills Usage

Each fix category uses same skills as corresponding audit:
- `--security` → 3 security skills
- `--tech-debt` → 2 code quality skills
- `--database` → 2 database skills
- etc.

Skills are referenced in agent prompt for context.

---

## Smart Detection

Before applying fixes:
- **Verify component exists** (no DB fixes if no database)
- **Check dependencies** (can we add flask-wtf?)
- **Test environment** (are tests runnable?)
- **Git status** (uncommitted changes?)

Warn user if:
- Uncommitted changes exist (recommend commit first)
- Tests don't pass before fixes (risky to apply)
- Dependencies can't be installed

---

## Success Criteria

- [OK] Recent audit exists or was run automatically
- [OK] Issues categorized into safe/risky
- [OK] Safe fixes explained and user confirmed
- [OK] Safe fixes applied using cco-agent-fix
- [OK] Changes verified (U_CHANGE_VERIFICATION)
- [OK] Risky fixes presented individually
- [OK] User chose to apply/skip each risky fix
- [OK] Risky fixes applied if approved
- [OK] Impact summary presented
- [OK] Next steps recommended
- [OK] Pain-point impact communicated

---

## Example Usage

```bash
# Fix security issues (runs audit if needed)
/cco-fix --security

# Fix multiple categories
/cco-fix --security --tech-debt --tests

# Fix everything found in recent audit
/cco-fix --all
```

---

## Integration with Other Commands

- **After /cco-audit**: Natural next step
- **Before /cco-commit**: Good to fix before committing
- **After /cco-overview**: Follow action plan
- **With /cco-generate**: Fix existing, generate missing

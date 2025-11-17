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

### Step 0: Introduction and Confirmation (ALWAYS FIRST)

**Before doing ANYTHING, present this introduction and get user confirmation:**

```markdown
# Fix Command

**What I do:**
I automatically fix issues found by audits. I categorize fixes into safe (low-risk, auto-applicable) and risky (could break functionality, need approval).

**How it works:**
1. Check if recent audit exists (if not, run audit first)
2. Categorize all issues into safe and risky fixes
3. You select which fixes to apply (individual steps or groups)
4. I apply selected fixes and verify changes
5. I report what was fixed with before/after verification

**What you'll get:**
- Safe fixes applied automatically (SQL injection, dead code, etc.)
- Risky fixes with individual approval (CSRF protection, architecture changes, etc.)
- Complete verification of all changes (grep verification, test runs)
- Impact summary (vulnerabilities reduced, files modified, etc.)

**Time estimate:** 5-30 minutes depending on number of fixes

**Changes WILL be made to your code** - all changes are verified and can be reviewed with git diff before committing.
```

**Then ask for confirmation using AskUserQuestion:**

```python
AskUserQuestion({
  questions: [{
    question: "Do you want to start fixing issues?",
    header: "Start Fix",
    multiSelect: false,
    options: [
      {
        label: "Yes, start fixing",
        description: "Begin fixing issues (will run audit first if needed)"
      },
      {
        label: "No, cancel",
        description: "Exit without making any changes"
      }
    ]
  }]
})
```

**CRITICAL:**
- If user selects "No, cancel" → EXIT immediately, do NOT proceed
- If user selects "Yes, start fixing" → Continue to Step 1

---

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

### Step 3: Present Fix Plan with AskUserQuestion

**IMPORTANT:** The fixes listed in options below are EXAMPLES. You MUST:
- Use actual issues from the audit results
- For simple fixes (single file/change): List as one option
- For complex fixes (multiple files/changes): Break down into individual steps with category in parentheses
- List REAL file paths and line numbers (e.g., api/users.py:45)
- Include actual issue descriptions from the audit
- Replace example fixes with REAL project-specific fixes

First, present safe fixes using multiselect (simple fixes can be single options, complex fixes should be broken down):

```python
AskUserQuestion({
  questions: [{
    question: "Which SAFE fixes should I apply? (These are low-risk and reversible):",
    header: "Safe Fixes",
    multiSelect: true,
    options: [
      {
        label: "SQL injection fix - api/users.py:45",
        description: "Parameterize query: cur.execute('SELECT * FROM users WHERE id = %s', (id,)) | Skill: cco-skill-security-owasp"
      },
      {
        label: "Externalize API_KEY - config.py:12",
        description: "Move to environment variable: os.environ['API_KEY'] | Skill: cco-skill-security-owasp"
      },
      {
        label: "AI prompt injection fix - api/chat.py:67",
        description: "Add input sanitization + output validation | Skill: cco-skill-ai-security-promptinjection"
      },
      {
        label: "Remove unused imports - 15 files",
        description: "Clean up 200+ unused imports across codebase | Skill: cco-skill-code-quality"
      },
      {
        label: "Fix type hints - services/auth.py",
        description: "Add missing type hints for 8 functions | Skill: cco-skill-code-quality"
      },
      {
        label: "Add input validation - api/register.py:30",
        description: "Validate email and username formats | Skill: cco-skill-security-owasp"
      },
      {
        label: "All Safe Fixes",
        description: "✅ Apply all 6 safe fixes automatically (recommended)"
      }
    ]
  }]
})
```

**IMPORTANT:** If user selects "All Safe Fixes", ignore other selections and apply all safe fixes.

Then, present risky fixes using multiselect (break down complex fixes into individual steps):

```python
AskUserQuestion({
  questions: [{
    question: "Which RISKY fix steps should I apply? (These could break functionality - select carefully):",
    header: "Risky Fixes",
    multiSelect: true,
    options: [
      # CSRF Protection - Broken down into steps (if this fix involves multiple files)
      {
        label: "Add flask-wtf dependency",
        description: "(CSRF Protection, 1 min) Add to requirements.txt | ⚠️ LOW RISK"
      },
      {
        label: "Add SECRET_KEY to config",
        description: "(CSRF Protection, 1 min) Add SECRET_KEY env variable | ⚠️ LOW RISK"
      },
      {
        label: "Update all 10 templates with csrf_token",
        description: "(CSRF Protection, 3 min) Add {{ csrf_token }} to forms | ⚠️ MEDIUM RISK - Forms will break without this"
      },
      {
        label: "Add CSRF validation to 5 form handlers",
        description: "(CSRF Protection, 2 min) Validate CSRF in POST handlers | ⚠️ MEDIUM RISK"
      },
      {
        label: "Update 8 test files for CSRF",
        description: "(CSRF Protection, 3 min) Add CSRF tokens to test requests | ⚠️ LOW RISK"
      },
      {
        label: "All CSRF Protection Steps",
        description: "✅ Apply all 5 CSRF steps above (complete CSRF protection)"
      },

      # JWT Migration - Broken down into steps (if complex migration)
      {
        label: "Install PyJWT dependency",
        description: "(JWT Migration, 1 min) Add pyjwt to requirements.txt | ⚠️ LOW RISK"
      },
      {
        label: "Create JWT service (services/jwt.py)",
        description: "(JWT Migration, 3 min) Token creation/validation logic | ⚠️ LOW RISK - New file"
      },
      {
        label: "Replace session auth in /api/auth/login",
        description: "(JWT Migration, 2 min) Return JWT instead of session | ⚠️ BREAKING - Old clients break"
      },
      {
        label: "Replace session auth in middleware",
        description: "(JWT Migration, 2 min) Validate JWT instead of session | ⚠️ BREAKING - All users logged out"
      },
      {
        label: "Update all protected endpoints (15 endpoints)",
        description: "(JWT Migration, 5 min) Use JWT auth decorator | ⚠️ BREAKING"
      },
      {
        label: "Update all tests for JWT auth",
        description: "(JWT Migration, 4 min) Update 20 test files | ⚠️ MEDIUM RISK"
      },
      {
        label: "All JWT Migration Steps",
        description: "⚠️ Apply all 6 JWT steps above (complete migration, BREAKING CHANGE)"
      },

      # Redis Caching - Simpler, might not need breakdown (example of simple fix)
      {
        label: "Add Redis caching for popular products",
        description: "(Redis, 10 min) Add redis-py, implement caching | ⚠️ MEDIUM RISK - Requires Redis server | Impact: 90% faster"
      },

      # Payment Refactoring - Broken down if complex
      {
        label: "Extract payment validation logic",
        description: "(Payment Refactor, 5 min) services/payment.py:validate_payment() | ⚠️ MEDIUM RISK"
      },
      {
        label: "Extract payment processing logic",
        description: "(Payment Refactor, 5 min) services/payment.py:process_payment() | ⚠️ MEDIUM RISK"
      },
      {
        label: "Update payment API to use new services",
        description: "(Payment Refactor, 3 min) api/payments.py - use extracted services | ⚠️ HIGH RISK"
      },
      {
        label: "Update payment tests",
        description: "(Payment Refactor, 7 min) Refactor 12 payment tests | ⚠️ MEDIUM RISK"
      },
      {
        label: "All Payment Refactoring Steps",
        description: "⚠️ Apply all 4 payment refactoring steps above"
      },

      # Group options
      {
        label: "All Risky Fix Steps",
        description: "⚠️ Apply ALL risky fix steps above - Only select if you understand ALL risks and have backups"
      },
      {
        label: "Skip all risky fixes",
        description: "✅ SAFE CHOICE: Skip all risky fixes for now (you can review them manually later)"
      }
    ]
  }]
})
```

**IMPORTANT:**
- If user selects "All Risky Fix Steps", ignore other selections and apply all risky fix steps
- If user selects "All [Fix Name] Steps", apply all steps for that specific fix
- If user selects "Skip all risky fixes", ignore other selections and skip all risky fixes
- Otherwise, apply ONLY the individually selected steps
- Break down complex fixes (affecting multiple files) into individual steps
- Keep simple fixes (single file/change) as single options

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

3. **Launch Task with cco-agent-fix** for selected risky fixes:

```python
Task({
  subagent_type: "general-purpose",
  model: "sonnet",  # Use Sonnet for accuracy on risky changes
  prompt: """
  Apply these risky fixes (user approved):

  [List only the risky fixes user selected]

  For each fix:
  - Explain what will change
  - Apply the fix using Edit/Write tools
  - Run tests to verify functionality
  - Verify the fix (grep for patterns)
  - Report completion with file:line references
  - Warn if tests fail

  Use these skills:
  - [skills for selected risky fixes]

  Follow U_CHANGE_VERIFICATION protocol.
  Follow C_BREAKING_CHANGES_APPROVAL (user already approved).
  """
})
```

### Step 5: Impact Summary

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

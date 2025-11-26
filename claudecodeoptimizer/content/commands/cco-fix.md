---
name: cco-fix
description: Automated issue resolution with safe/risky categorization
action_type: fix
note: Uses same categories as cco-audit - search cco-audit metadata for parameter details
parameters:
  security:
    keywords: [security fix, owasp fix, xss fix, sqli fix, csrf protection, secrets externalize]
    category: security
    pain_points: [1]
  tech-debt:
    keywords: [tech debt fix, remove dead code, reduce complexity, fix duplication]
    category: quality
    pain_points: [2]
  ai-security:
    keywords: [ai security fix, prompt injection fix, sanitization, output validation]
    category: security
    pain_points: [3]
  tests:
    keywords: [fix tests, improve coverage, fix test isolation, add edge cases]
    category: testing
    pain_points: [4]
  integration:
    keywords: [fix integration, resolve dependencies, fix imports, resolve conflicts]
    category: infrastructure
    pain_points: [6]
  code-quality:
    keywords: [fix syntax, fix logic bugs, add type hints, improve error handling]
    category: quality
    pain_points: [2]
  docs:
    keywords: [fix documentation, add docstrings, update readme, create adr]
    category: docs
    pain_points: [7]
  database:
    keywords: [fix n+1, add indexes, fix connection pooling, optimize queries]
    category: database
    pain_points: [5]
  observability:
    keywords: [add logging, structured logging, add correlation ids, add metrics]
    category: observability
    pain_points: [5]
  monitoring:
    keywords: [add dashboards, configure alerts, setup prometheus, setup grafana]
    category: observability
    pain_points: [5]
  cicd:
    keywords: [fix pipeline, add quality gates, fix deployment, improve cicd]
    category: infrastructure
    pain_points: [6]
  containers:
    keywords: [fix dockerfile, optimize container, fix k8s config, container security]
    category: infrastructure
    pain_points: [6]
  supply-chain:
    keywords: [update dependencies, fix vulnerabilities, update licenses, generate sbom]
    category: security
    pain_points: [1]
  migrations:
    keywords: [fix migration, add rollback, fix schema, data migration fix]
    category: database
    pain_points: [5]
  performance:
    keywords: [fix performance, add caching, reduce bundle, optimize response]
    category: performance
    pain_points: [5]
  architecture:
    keywords: [fix architecture, reduce coupling, apply patterns, improve design]
    category: architecture
    pain_points: [5]
  git:
    keywords: [fix git, improve commits, fix branching, improve pr process]
    category: infrastructure
    pain_points: [5]
  ai-quality:
    keywords: [fix ai quality, fix hallucination, fix api errors, fix code bloat, fix vibe coding]
    category: quality
    pain_points: [3, 8, 9]
  ai-debt:
    keywords: [fix ai debt, fix ai generated code, refactor ai code, fix ai technical debt]
    category: quality
    pain_points: [2, 3]
  ai:
    keywords: [fix ai issues, comprehensive ai fix, ai security and quality fix]
    category: meta
    pain_points: [2, 3, 8, 9]
    meta_flags: [ai-quality, ai-debt, ai-security]
  critical:
    keywords: [fix critical, essential fixes, must-fix, high priority fix]
    category: meta
    pain_points: [1, 3, 4, 5]
    meta_flags: [security, ai-security, database, tests]
  production-ready:
    keywords: [production fixes, deploy readiness fix, pre-deploy fixes]
    category: meta
    pain_points: [1, 4, 5, 7]
    meta_flags: [security, performance, database, tests, docs]
  code-health:
    keywords: [code health fix, quality improvements, maintainability fix]
    category: meta
    pain_points: [2, 4, 7]
    meta_flags: [tech-debt, code-quality, tests, docs]
  team-metrics:
    keywords: [team metrics fix, collaboration fix, platform improvements]
    category: meta
    pain_points: [6, 10, 11, 12]
    meta_flags: [code-review, platform, cicd]
---

# CCO Fix Command

**Automated issue resolution with safe/risky categorization and auto-audit dependency.**

---


## Execution Guarantee

**This command WILL execute fully without requiring user presence during processing.**

**What Happens:**
1. **Step 0**: Introduction and confirmation (user input required)
2. **Context Check**: Check for calling command context (automated)
3. **Audit** (if no context): Run audit to discover issues (automated)
4. **Selection**: Select fixes to apply (user input or automated)
5. **Pre-Flight**: Summary and confirmation (user input required)
6. **Execution**: Apply fixes with verification (fully automated)
7. **Final Report**: Results with accounting (automated)

**User Interaction Points:**
- Initial confirmation
- Fix selection (if manual mode)
- Pre-flight confirmation
- Risky fix approval (if risky fixes detected)

**Automation:**
- All audits run without interruption
- Fix agents apply changes in parallel
- Complete accounting enforced (total = applied + skipped + failed)
- Verification runs automatically

**Time Estimate:**
- Quick fixes (1-5): 2-5 minutes
- Moderate (6-20): 5-15 minutes
- Comprehensive (21+): 15-30 minutes

**Verification:**
- Every fix verified before acceptance
- Accounting formula: `total = applied + skipped + failed`

---

## Design Standards

- UX/DX standards (transparency, progressive disclosure, zero surprises)
- Honesty & accurate reporting (no false positives/negatives)
- No hardcoded examples (use placeholders: `{FILE_PATH}`, `{LINE_NUMBER}`)

---

## Purpose

Automatically fix issues found by audits. Runs audit first if no recent audit exists. Categorizes fixes into safe (auto-apply) and risky (require approval).

---

## CRITICAL: Check for Context from Calling Command

**BEFORE running audit, check conversation for "CONTEXT FOR /cco-fix:"**

✓ **If found**: Use provided issue list, skip audit, fix specified issues only
✗ **If not found**: Run audit first, then fix discovered issues

**Why**: Eliminates duplicate audit - previous command already analyzed.


---

## Fix Outcome Categories

```python
# Accurate categorization - no false claims
OUTCOMES = {
    "fixed": "Applied and verified",
    "needs_decision": "Multiple valid approaches - user must choose",
    "needs_review": "Complex change - requires human verification",
    "requires_migration": "Database change - needs migration script",
    "requires_config": "External system configuration needed",
    "impossible_external": "Issue in third-party code",
    "impossible_design": "Requires architectural change",
}
```

---

## Fix Categories (Same as Audit)

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

## Execution Protocol

### Step 0: Introduction and Confirmation

**Pattern:** Pattern 1 (Step 0 Introduction)

**Command-Specific Details:**

**What I do:** Automatically fix issues found by audits. Safe fixes auto-applied, risky fixes require approval.

**Process:** Check for recent audit → Categorize fixes (safe/risky) → You select → I apply and verify → Report results

**Output:** Complete verification of all changes, impact summary (vulnerabilities reduced, files modified, etc.)

**Time:** 2-30 minutes depending on fix count

**Changes WILL be made** - all verified and reviewable with git diff

```python
AskUserQuestion({
  questions: [{
    question: "Do you want to start fixing issues?",
    header: "Start Fix",
    multiSelect: false,
    options: [
      {label: "Yes, start fixing", description: "Begin fixing issues (will run audit first if needed)"},
      {label: "No, cancel", description: "Exit without making any changes"}
    ]
  }]
})
```

**If Cancel:** Exit immediately, do NOT proceed
**If Start:** Continue to Project Context Discovery

---

### Step 0.5: Project Context Discovery

**Pattern:** Pattern 2 (Multi-Select with "All")

**Command-Specific Details:**

**Benefits for /cco-fix:** Fixes follow project conventions (naming style, ORM usage, test patterns)

**Context Used:** Project naming conventions, testing framework, formatting style applied to all fixes

---

### Step 0.6: Tech Stack Detection & Applicability Filtering

**Pattern:** Pattern 10 (Tech Stack Detection & Context Sharing)

**Purpose:** Filter fixes to show only applicable options

```markdown
Detecting tech stack for fix applicability...

════════════════════════════════════════════════════════════════
TECH STACK DETECTED:

Languages: {DETECTED_LANGUAGES}
Frameworks: {DETECTED_FRAMEWORKS}
Databases: {DETECTED_DATABASES}
Testing: {DETECTED_TESTING}

Detection time: {DURATION}s
════════════════════════════════════════════════════════════════

Applicable fixes: {APPLICABLE_COUNT}
Filtered: {FILTERED_COUNT} fixes (not applicable to this project)

ℹ️  Filtered:
  - {FILTERED_FIX_CATEGORY_1} ({REASON_1})
  - {FILTERED_FIX_CATEGORY_2} ({REASON_2})
  - {FILTERED_FIX_CATEGORY_3} ({REASON_3})
```

---

### Step 1: Check for Recent Audit

```markdown
Checking for recent [category] audit...
```

If no recent audit:
```markdown
No recent audit found.
Running /cco-audit --[category] first...

[Audit runs and presents results]
```

If recent audit exists:
```markdown
Found recent audit results
Using existing results...
```

---

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

---

### Step 3: Present Fix Plan with Category Selection

**Pattern:** Pattern 3 (Progress Reporting)

**Command-Specific Details:**

**Tab-based selection (single submit):**
- Tab 1: Safe fix categories (✅ low-risk, reversible)
- Tab 2: Risky fix categories (⚠️ require confirmation)

**Dynamic generation:** All options generated from REAL audit results (no hardcoded examples)

**Category grouping:** Fixes grouped by category (Security, Quality, Database, etc.) to ensure ALL fixes shown regardless of count

```python
# Generate safe fix category counts
safe_security_count = len([f for f in safe_fixes if f.category == "security"])
safe_quality_count = len([f for f in safe_fixes if f.category == "quality"])
# ... etc

AskUserQuestion({
  questions: [
    {
      question: "Select SAFE fix categories (low-risk, reversible):",
      header: "✅ Safe",
      multiSelect: true,
      options: [
        {label: "All Safe Fixes", description: f"Apply all {total_safe_count} safe fixes (recommended)"},
        {label: f"Security ({safe_security_count} fixes)", description: "Parameterize queries, externalize secrets"},
        {label: f"Code Quality ({safe_quality_count} fixes)", description: "Remove dead code, fix imports"},
        # ... dynamic categories
      ]
    },
    {
      question: "Select RISKY fix categories (require confirmation):",
      header: "⚠️ Risky",
      multiSelect: true,
      options: [
        {label: "All Risky Fixes", description: f"⚠️ Select all {total_risky_count} risky fixes"},
        {label: f"Security ({risky_security_count} fixes)", description: "Auth changes, CSRF protection"},
        {label: f"Database ({risky_db_count} fixes)", description: "Schema changes, migrations"},
        # ... dynamic categories
      ]
    }
  ]
})
```

**Selection Processing:**

After user submits:
```markdown
## Fix Selection Summary

**Your selections:**
- ✅ Safe: [categories] → {SELECTED_COUNT} fixes
- ⚠️ Risky: [categories] → {SELECTED_COUNT} fixes

**Total: {TOTAL_SELECTED} fixes selected**

⚠️ Only selected categories will be applied.
Categories NOT selected will be skipped entirely.
```

---


---

### Step 4: Apply Fixes

**Pattern:** Pattern 4 (Complete Accounting)


**Command-Specific Details:**

**Agent:** `fix-agent` (model selected in Step 3.5, defaults to Sonnet)

**Model Selection:** Let Claude Code decide based on task complexity

**Parallel Execution:** Agent automatically parallelizes independent fixes (different files)

**TodoWrite tracking:** All fixes tracked in real-time

**Fix Application:**

```python
Task({
  subagent_type: "fix-agent",
  model: "sonnet",
  prompt: """
  Apply these safe security fixes (from audit results):

  [For each issue selected by user:]
  {N}. {FILE_PATH}:{LINE_NUMBER} - {FIX_DESCRIPTION}

  For each fix:
  - Read the file
  - Apply the fix using Edit tool
  - Verify the fix (grep for old pattern = 0 results)
  - Report completion with file:line reference

  Use these skills:
  - {MATCHED_SECURITY_SKILL}
  - {MATCHED_AI_SECURITY_SKILL}

  Follow U_CHANGE_VERIFICATION protocol.
  """
})
```

**Report ACTUAL changes made:**

```markdown
Applied {ACTUAL_COUNT} safe fixes:
[For each fix actually applied:]
✓ {FILE_PATH}:{LINE_NUMBER} ({SPECIFIC_CHANGE})

Verification:
✓ {ACTUAL_VERIFICATION_COMMAND} → {ACTUAL_RESULT}
✓ All changes follow U_CHANGE_VERIFICATION protocol
```

**For risky fixes:** Same process, but with individual confirmation for each fix before applying.

---

### Step 5: Impact Summary


**Command-Specific Details:**

**Accounting formula enforced:** `total = applied + skipped + failed`

**Real metrics (no placeholders):**

```markdown
Fix Summary:

Applied:
✓ {ACTUAL_SAFE_COUNT} safe fixes (auto-applied)
✓ {ACTUAL_RISKY_COUNT} risky fixes (user approved)
✗ {SKIPPED_COUNT} fixes (user skipped)

Results:
- Security score: {BEFORE_SCORE} → {AFTER_SCORE} (+{DELTA} points)
- Vulnerabilities: {BEFORE_COUNT} → {AFTER_COUNT} ({PERCENTAGE}% reduction)
- Files modified: {ACTUAL_FILE_COUNT}
- Lines changed: +{ADDED} / -{REMOVED}

Pain Point Impact:
✓ Addresses Pain #{X} ({PAIN_DESCRIPTION})
✓ Risk reduced: {ACTUAL_PERCENTAGE}%

Remaining Issues:
- {REAL_REMAINING_ISSUE_1}
- {REAL_REMAINING_ISSUE_2}

Next Steps:
1. Test changes: {PROJECT_SPECIFIC_TEST_COMMAND}
2. Review git diff before committing
3. Address remaining issues manually
4. Run /cco-audit --{CATEGORY} to verify

Recommended:
/cco-commit (generates semantic commit messages)
```

---

## Agent Usage

- Parallel execution patterns (fan-out, pipeline, hierarchical)
- Model selection (Haiku for mechanical, auto for complex)
- Error handling protocols
- Agent communication patterns

**Command-Specific Agent Configuration:**

**Agent:** fix-agent (Sonnet)
**Pattern:** Automatic parallelization (independent fixes in parallel)
**Skills:** Same skills as corresponding audit category

---

## Agent Error Handling

**Pattern:** Pattern 5 (Error Handling)

**Command-Specific Handling:**

Options: Retry | Retry with different model | Manual fix | Skip this fix | Cancel

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
- [OK] Safe fixes applied using fix-agent
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

# With additional context (optional prompt)
/cco-fix --security "Prioritize authentication fixes"
/cco-fix --tech-debt "Focus on high-complexity functions"
/cco-fix --all "Apply conservative fixes only"
```

**Optional Prompt Support:**
Any text after the flags is treated as additional context for the fix process. The AI will:
- Prioritize fixes based on your guidance
- Apply domain-specific conventions
- Adjust risk assessment based on your context
- Follow specific fix preferences you mention

---

## Integration with Other Commands

- **After /cco-audit**: Natural next step
- **Before /cco-commit**: Good to fix before committing
- **After /cco-audit --quick**: Follow action plan
- **With /cco-generate**: Fix existing, generate missing

---

## Next Steps: Calling Other Commands


**Command-Specific Context:**

### If Tests/Docs Needed After Fixes

When fixes are applied but tests or documentation are missing:

**ALWAYS provide context before calling /cco-generate:**

```markdown
CONTEXT FOR /cco-generate:
Fix applied to {COUNT} files: {FILE_LIST}. These changes need:
- Tests: {TEST_DESCRIPTION} ({AFFECTED_FUNCTIONS})
- Docs: {DOC_DESCRIPTION} ({AFFECTED_APIs})
Pattern: {EXISTING_PATTERN_REFERENCE}

[Then immediately call SlashCommand]
```

**Example:**

```markdown
CONTEXT FOR /cco-generate:
Fixed SQL injection in {COUNT} files ({FILE_PATH}, {FILE_PATH}, etc.) by adding parameterized queries. These changes need integration tests to verify: db query functions ({FUNCTION_NAME}, {FUNCTION_NAME}, etc.) and API endpoints ({API_ENDPOINT}, {API_ENDPOINT}). Existing test pattern in {TEST_FILE} uses pytest with database fixtures.

SlashCommand({command: "/cco-generate tests"})
```

**Why This Matters:**
- `/cco-generate` knows exactly what was fixed
- Can generate tests specifically for fixed code
- No need to re-analyze the codebase

---

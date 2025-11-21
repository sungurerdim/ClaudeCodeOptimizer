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

# cco-fix

**Automated issue resolution with safe/risky categorization and auto-audit dependency.**

---

## Purpose

Automatically fix issues found by audits. Runs audit first if no recent audit exists. Categorizes fixes into safe (auto-apply) and risky (require approval).

---

## Critical UX Principles (Same as Audit)

1. **100% Honesty** - Never claim "fixed" unless verified, never say "impossible" if technically possible
2. **Complete Accounting** - Every issue must be accounted: fixed + skipped + cannot-fix = total
3. **No Hardcoded Examples** - All examples use `{PLACEHOLDERS}`, never fake data
4. **Phase Tracking** - Explicit start/end for each phase with timestamps
5. **Consistent Counts** - Same numbers shown everywhere (single source of truth)

**See `/cco-audit` for detailed implementation of:**
- Component 6: State Management & Count Tracking
- Component 9: Honesty & Accurate Reporting
- Component 10: Fix Integration Accounting

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

## Auto-Audit Dependency

**Before fixing, check for recent audit in conversation context:**

```python
def fix(category):
    # Check if audit results exist in current conversation
    # (Zero pollution: no files, only conversation memory)
    if not has_audit_in_context(category):
        print(f"No recent {category} audit found in conversation.")
        print(f"Running /cco-audit --{category} first...\n")

        # Run audit (results go to conversation context)
        run_audit(category)

    # Get audit results from conversation context
    issues = get_audit_from_context(category)

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

**PHASES TRACKING:**
```python
PHASES = {
    1: "Introduction & Confirmation",
    2: "Project Context Discovery",
    3: "Fix Categorization & Selection",
    4: "Apply Fixes & Report Results"
}

# Before each phase, announce:
print("───────────────────────────────────────────────────────")
print(f"### Phase {N}/4: {PHASES[N]} ▶ STARTED")
print("───────────────────────────────────────────────────────")
# After phase completes:
print(f"### Phase {N}/4: {PHASES[N]} ✓ COMPLETE")
```

### Step 0: Introduction and Confirmation (ALWAYS FIRST)
**[Phase 1/4: Introduction & Confirmation]**

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
- If user selects "Yes, start fixing" → Continue to Step 0.5

---

### Step 0.5: Project Context Discovery (Optional)
**[Phase 2/4: Project Context Discovery]**

**Ask user if they want project documentation analyzed for better fix alignment.**

```python
AskUserQuestion({
  questions: [{
    question: "Extract context from project documentation?",
    header: "Project Context",
    multiSelect: false,
    options: [
      {
        label: "Yes (recommended)",
        description: "Extract project conventions from README/CONTRIBUTING, fixes align with project style"
      },
      {
        label: "No",
        description: "Code fixes only (faster)"
      }
    ]
  }]
})
```

**If "Yes" selected:**

```python
# Extract project context via Haiku sub-agent
context_result = Task({
    subagent_type: "Explore",
    model: "haiku",
    prompt: """
    Extract project context summary (MAX 200 tokens).
    Focus on: naming conventions, testing framework, formatting style.

    Files to check: README.md, CONTRIBUTING.md, ARCHITECTURE.md

    Return: Purpose, Tech Stack, Conventions (naming, testing, formatting)
    """
})

# Use context when applying fixes
project_context = context_result
```

**Benefits:** Fixes follow project conventions (naming style, ORM usage, test patterns).

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
**[Phase 3/4: Fix Categorization & Selection]**

**IMPORTANT - Dynamic Fix Generation Protocol:**
You MUST generate fix options from ACTUAL audit results:
1. Read audit results to get REAL issues found
2. Categorize each issue as safe or risky using the criteria below
3. For simple fixes (one file, one change): Create single option
4. For complex fixes (multiple files/changes): Break into individual steps
5. Use ACTUAL file paths and line numbers from audit (e.g., <real-file>:<real-line>)
6. Include REAL issue descriptions from audit findings
7. Reference ACTUAL skills used in detection

**Example template for generating options (DO NOT use verbatim):**
```python
# From audit results:
for issue in audit_results:
    if is_safe_fix(issue):
        option = {
            label: f"{issue.fix_type} - {issue.file}:{issue.line}",
            description: f"{issue.fix_description} | Skill: {issue.skill}"
        }
```

**IMPORTANT - Tab-Based Selection (Single Submit):**
Present safe and risky fixes together in a single AskUserQuestion with multiple tabs:

```python
# Generate options dynamically from REAL audit results
safe_fix_options = []
for safe_fix in safe_fixes:
    safe_fix_options.append({
        label: f"{safe_fix.type} - {safe_fix.file}:{safe_fix.line}",
        description: f"{safe_fix.description} | Skill: {safe_fix.skill}"
    })

# Add group option for safe fixes
safe_fix_options.append({
    label: "All Safe Fixes",
    description: f"✅ Apply all safe fixes automatically (recommended)"
})

# Tab-based selection - group by category to ensure ALL fixes are shown
# Since fix counts are dynamic (from audit), group by category for scalability

AskUserQuestion({
  questions: [
    {
      question: "Select SAFE fix categories (low-risk, reversible):",
      header: "✅ Safe",
      multiSelect: true,
      options: [
        {
          label: f"Security ({safe_security_count} fixes)",
          description: "Parameterize queries, externalize secrets, add headers"
        },
        {
          label: f"Code Quality ({safe_quality_count} fixes)",
          description: "Remove dead code, fix imports, add error handling"
        },
        {
          label: f"Other Safe ({safe_other_count} fixes)",
          description: "Formatting, linting, documentation updates"
        },
        {
          label: "All Safe Fixes",
          description: f"Apply all {total_safe_count} safe fixes (recommended)"
        }
      ]
    },
    {
      question: "Select RISKY fix categories (require confirmation):",
      header: "⚠️ Risky",
      multiSelect: true,
      options: [
        {
          label: "All Risky Fixes",
          description: f"⚠️ Select all {total_risky_count} risky fixes (each will need confirmation)"
        },
        {
          label: f"Security ({risky_security_count} fixes)",
          description: "Auth changes, CSRF protection, encryption"
        },
        {
          label: f"Database ({risky_db_count} fixes)",
          description: "Schema changes, migrations, indexes"
        },
        {
          label: f"Architecture ({risky_arch_count} fixes)",
          description: "Refactoring, pattern changes, API updates"
        }
      ]
    }
  ]
})
```

### Selection Processing

**After user submits, calculate and display selection summary:**

```markdown
## Fix Selection Summary

**Your selections:**
- ✅ Safe: [list selected categories] → [total fix count] fixes
- ⚠️ Risky: [list selected categories] → [total fix count] fixes

**Total: {{SELECTED_COUNT}} fixes selected**

⚠️ Only selected fix categories will be applied.
Categories NOT selected will be skipped entirely.
```

**IMPORTANT:**
- Group fixes by category to ensure ALL fixes are visible regardless of count
- If user selects "All Safe Fixes", apply all safe fixes in all categories
- For risky fixes, always show individual confirmation before applying each fix

For detailed fix selection within a category:

```python
# Generate risky fix options dynamically from REAL audit results
risky_fix_options = []

# For each risky fix, determine if it needs breakdown
for risky_fix in risky_fixes:
    if risky_fix.is_complex():  # Multiple files or steps
        # Break down into individual steps
        for step in risky_fix.steps:
            risky_fix_options.append({
                label: f"{step.action}",
                description: f"({risky_fix.name}, {step.time_estimate}) {step.description} | ⚠️ {step.risk_level}"
            })
        # Add group option for this fix
        risky_fix_options.append({
            label: f"All {risky_fix.name} Steps",
            description: f"⚠️ Apply all {len(risky_fix.steps)} {risky_fix.name} steps above"
        })
    else:  # Simple risky fix
        risky_fix_options.append({
            label: f"{risky_fix.name}",
            description: f"({risky_fix.category}, {risky_fix.time_estimate}) {risky_fix.description} | ⚠️ {risky_fix.risk_level} | Impact: {risky_fix.impact}"
        })

# Add master group options
risky_fix_options.extend([
    {
        label: "All Risky Fix Steps",
        description: f"⚠️ Apply ALL {sum(len(f.steps) if f.is_complex() else 1 for f in risky_fixes)} risky fix steps above - Only if you understand ALL risks and have backups"
    },
    {
        label: "Skip all risky fixes",
        description: "✅ SAFE CHOICE: Skip all risky fixes for now (review manually later)"
    }
])

AskUserQuestion({
  questions: [{
    question: "Which RISKY fix steps should I apply? (These could break functionality - select carefully):",
    header: "Risky Fixes",
    multiSelect: true,
    options: risky_fix_options
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
**[Phase 4/4: Apply Fixes & Report Results]**

If user confirms:

1. **Use TodoWrite** to track fixes
2. **Launch Task with cco-agent-fix**:

```python
Task({
  subagent_type: "general-purpose",
  model: "sonnet",  # Use Sonnet for accuracy
  prompt: """
  Apply these safe security fixes (from audit results):

  [For each issue selected by user:]
  [N]. <file>:<line> - [Fix description from audit]

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

3. **Report completion with REAL results:**

**IMPORTANT - Dynamic Results Reporting:**
Report ACTUAL changes made, not examples. Use this template:

```markdown
Applied [ACTUAL_COUNT] safe fixes:
[For each fix actually applied:]
✓ <real-file>:<real-line> ([specific change made])

Verification:
[For each verification run:]
✓ [actual verification command] → [actual result]
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

**IMPORTANT - Dynamic Impact Reporting:**
Generate summary from ACTUAL changes made. Use this template with REAL metrics:

```markdown
Fix Summary:

Applied:
✓ [ACTUAL_SAFE_COUNT] safe fixes (auto-applied)
✓ [ACTUAL_RISKY_COUNT] risky fixes (user approved)
✗ [SKIPPED_COUNT] fixes (user skipped)

Results:
- Security score: [BEFORE_SCORE] → [AFTER_SCORE] (+[DELTA] points)
- Vulnerabilities: [BEFORE_COUNT] → [AFTER_COUNT] ([PERCENTAGE]% reduction)
- Files modified: [ACTUAL_FILE_COUNT]
- Lines changed: +[ADDED] / -[REMOVED]

Pain Point Impact:
✓ Addresses Pain #[X] ([PAIN_DESCRIPTION])
✓ Risk reduced: [ACTUAL_PERCENTAGE]%
✓ [Other actual improvements]

Remaining Issues:
- [List REAL remaining issues]
- [List REAL skipped fixes]

Next Steps:
1. Test changes: [actual test command for this project]
2. Review git diff before committing
3. Address remaining issues manually
4. Run /cco-audit --[category] to verify

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
  description: "Fix [issue type] in <file1>",
  prompt: "[Fix description] at <file1>:<line>..."
})
Task({
  subagent_type: "general-purpose",
  model: "sonnet",
  description: "Fix [issue type] in <file2>",
  prompt: "[Fix description] at <file2>:<line>..."
})
Task({
  subagent_type: "general-purpose",
  model: "sonnet",
  description: "Fix [issue type] in <file3>",
  prompt: "[Fix description] at <file3>:<line>..."
})

# All run in parallel since they modify different files
# Total time: significantly faster than sequential
# No cost savings (all Sonnet), but much faster

# Sequential execution needed when files depend on each other:
# 1. Update interface definition first
# 2. Then update all implementations
# 3. Then update tests
```

---

## Skills Usage

Each fix category uses same skills as corresponding audit:
- `--security` → 3 security skills (cco-skill-security-owasp-xss-sqli-csrf, cco-skill-privacy-gdpr-compliance-encryption, cco-skill-supply-chain-dependencies-sast)
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

## Agent Error Handling

**If fix agent execution fails:**

AskUserQuestion({
  questions: [{
    question: "fix-agent (Sonnet) failed: {error_message}. How to proceed?",
    header: "fix-agent (Sonnet) Error",
    multiSelect: false,
    options: [
      {label: "Retry", description: "Run agent again with same parameters"},
      {label: "Retry with different model", description: "Try Sonnet/Haiku/Opus"},
      {label: "Manual fix", description: "Guide manual fix process"},
      {label: "Skip this fix", description: "Continue with next fix"},
      {label: "Cancel", description: "Stop entire command"}
    ]
  }]
})

**Model selection if user chooses "Retry with different model":**

AskUserQuestion({
  questions: [{
    question: "Which model to try?",
    header: "Model Selection",
    multiSelect: false,
    options: [
      {label: "Sonnet", description: "Balanced performance and cost (recommended)"},
      {label: "Haiku", description: "Faster, more affordable"},
      {label: "Opus", description: "Most capable, higher cost"}
    ]
  }]
})

---
title: Root Cause Analysis Skill
category: analysis
description: Analyze WHY violations exist, not just WHERE
metadata:
  name: "Root Cause Analysis"
  activation_keywords: ["root cause", "why violations", "pattern analysis", "systemic fix"]
  category: "analysis"
principles: ['U_ROOT_CAUSE_ANALYSIS', 'U_EVIDENCE_BASED', 'U_FAIL_FAST', 'U_DRY', 'U_COMPLETE_REPORTING', 'U_CHANGE_VERIFICATION']
use_cases:
  development_philosophy: [quality_first, balanced]
  project_maturity: [active-dev, production, legacy]
---

# Root Cause Analysis

Fix the pattern, not individual instances. Understand WHY violations exist to prevent recurrence.

<!-- INSTRUCTIONS: Load when activated -->
## Detailed Instructions

### When This Skill Activates

This skill activates AFTER audit aggregation, BEFORE reporting:
- `/cco-audit-principles` aggregates violations
- `/cco-audit-security` aggregates security issues
- `/cco-audit-tests` aggregates coverage gaps

**Trigger:** Command finds 3+ violations of same type

### The Core Principle

**Don't just fix symptoms. Find and fix the root cause.**

Example:
- Don't fix 15 bare except clauses individually
- Understand WHY they exist, create systemic fix

### Analysis Dimensions

#### 1. Temporal Patterns - When were violations introduced?

```bash
for file in <violation_files>; do
    git log -1 --format="%ai %an" -- $file
done
```

Categories:
- **LEGACY** (>1 year old): Before team adopted principle
- **RECENT** (<1 month old): New code, training issue
- **GRADUAL** (3-12 months): Slow drift, enforcement gaps

#### 2. Authorship Patterns - Who introduced violations?

```bash
for file in <violation_files>; do
    git log --format="%an" -- $file | sort | uniq -c
done
```

Categories:
- **SINGLE AUTHOR**: Training/knowledge issue for one person
- **MULTIPLE AUTHORS**: Team-wide knowledge gap
- **EXTERNAL**: Third-party code, dependencies

#### 3. Structural Patterns - Where do violations cluster?

```bash
# Group by directory
for violation in <violations>; do
    dirname $violation
done | sort | uniq -c
```

Categories:
- **SERVICE-SPECIFIC**: Only in services/worker/
- **CROSS-CUTTING**: In shared/ (affects all services)
- **COPY-PASTE**: Identical code in multiple files

#### 4. Code Age Patterns - How old is the violating code?

```bash
git log --follow --format="%ai" -- <file> | tail -1
```

Categories:
- **ANCIENT** (>2 years): Original implementation, never refactored
- **OLD** (6-24 months): Pre-dates current standards
- **NEW** (<6 months): Recent addition, should comply

### Root Cause Classification

#### Type 1: Legacy Code

**Signature:** Old files (>1 year), before principle adopted

**Example:**
```
15 bare except clauses found
Analysis:
- 12/15 in files >1 year old
- 0/15 in files <6 months old
- Pattern: All added before 2024-01-01 (U_FAIL_FAST adoption date)

Root Cause: LEGACY CODE (pre-principle)
```

**Systemic Fix:**
```
1. Create migration script: /cco-migrate-legacy --principle=U_FAIL_FAST
2. Auto-fix all legacy violations in one pass
3. Add pre-commit hook to prevent new violations
4. Schedule: Migrate legacy code in next sprint
```

#### Type 2: Training Gap

**Signature:** Same author, recent code, multiple violations

**Example:**
```
8 DRY violations found (duplicate functions)
Analysis:
- 6/8 authored by alice@company.com
- All in last 3 months
- Alice joined team 4 months ago

Root Cause: TRAINING GAP (new team member)
```

**Systemic Fix:**
```
1. Schedule 1-on-1 with Alice
2. Share DRY principle (U_FAIL_FAST) documentation
3. Code review: Show how to extract to shared module
4. Provide IDE snippet for common patterns
5. Pair programming: Refactor together
```

#### Type 3: Copy-Paste Pattern

**Signature:** Identical code in multiple locations

**Example:**
```
5 duplicate encrypt_aes_gcm() functions
Analysis:
- Identical implementation in 5 files
- All by different authors
- First instance: shared/crypto.py (18 months ago)
- Copies: 3-12 months ago

Root Cause: COPY-PASTE (developers copied instead of importing)
```

**Systemic Fix:**
```
1. Delete duplicates: Keep only shared/crypto.py
2. Update imports in all 4 locations
3. Add docstring: "CANONICAL IMPLEMENTATION - import, don't copy"
4. Add test: Verify only one implementation exists
5. Document in team wiki: "Common Crypto Functions"
```

#### Type 4: Missing Template

**Signature:** Same violation in multiple services, boilerplate code

**Example:**
```
12 API endpoints without rate limiting
Analysis:
- All in services/*/routes.py
- All by different authors over 8 months
- No shared rate limit decorator exists

Root Cause: MISSING TEMPLATE (no reusable component)
```

**Systemic Fix:**
```
1. Create rate_limit decorator in shared/api.py
2. Update all 12 endpoints to use decorator
3. Add to project template/cookiecutter
4. Document in API development guide
5. Add linter rule: Flag @app.route without @rate_limit
```

#### Type 5: Incomplete Migration

**Signature:** Mix of old and new patterns

**Example:**
```
23 files use dataclasses, 18 files use manual __init__
Analysis:
- dataclass migration started 6 months ago
- Not completed
- Some files migrated, others forgotten

Root Cause: INCOMPLETE MIGRATION
```

**Systemic Fix:**
```
1. Identify all files with manual __init__ (grep)
2. Create migration script: /cco-migrate-to-dataclasses
3. Run script, convert all at once
4. Test thoroughly
5. Commit: "refactor: complete dataclass migration"
```

### Analysis Report Format

```markdown
=== Root Cause Analysis ===

Violation Type: <Principle ID or Security Issue>
Total Count: <N violations>

ANALYSIS:

Temporal Distribution:
- LEGACY (>1yr): 12 violations (80%)
- OLD (6-12mo): 2 violations (13%)
- RECENT (<6mo): 1 violation (7%)

Authorship Distribution:
- alice@company.com: 6 violations (40%)
- bob@company.com: 3 violations (20%)
- Multiple authors: 6 violations (40%)

Structural Distribution:
- services/worker/: 8 violations (53%)
- shared/: 4 violations (27%)
- services/api/: 3 violations (20%)

ROOT CAUSES:

1. PRIMARY: Legacy Code (80% of violations)
   - Files last modified >1 year ago
   - Before team adopted U_FAIL_FAST principle
   - Evidence: git log shows all files from 2023

2. SECONDARY: Training Gap (20% of violations)
   - Alice (new team member, joined 4 months ago)
   - Recent code (<6 months)
   - Evidence: All by same author in last 3 months

SYSTEMIC FIXES:

Priority 1 (Legacy Code):
[ ] Create migration script: /cco-migrate-legacy --principle=U_FAIL_FAST
[ ] Run script in next sprint
[ ] Auto-fix 12 legacy violations
[ ] Estimated time: 2 hours

Priority 2 (Training Gap):
[ ] Schedule 1-on-1 with Alice
[ ] Share U_FAIL_FAST documentation
[ ] Code review session
[ ] Estimated time: 1 hour

PREVENTIVE MEASURES:

1. Add pre-commit hook: Block new bare except clauses
2. Add IDE snippet: Proper exception handling template
3. Update onboarding docs: Include U_FAIL_FAST principle
4. Schedule quarterly principle refresher training

TIMELINE:

Week 1: Implement preventive measures (hooks, snippets)
Week 2: Fix legacy code (migration script)
Week 3: Training session with Alice
Week 4: Verify no new violations
```

<!-- RESOURCES: Load on explicit request -->
## Examples & Resources

### Example: Security Issue Root Cause

15 hardcoded secrets found → Analysis reveals:
- 53% in .env.backup files (forgotten backups, missing .gitignore)
- 33% legacy config (>1yr old, pre-env-variables)
- 13% test fixtures (false positives, safe to ignore)

Systemic fix: Add .gitignore, migrate legacy, whitelist tests, add pre-commit hook

### Example: Test Coverage Root Cause

36 untested functions → Analysis reveals:
- 50% private helpers (team belief: don't test private)
- 67% legacy code (pre-test mandate)
- 56% in worker service (async code, harder to test)

Systemic fix: Team discussion on test philosophy, test critical functions first, async testing training

### Integration with Commands

#### audit-principles.md
Add after Phase 3 (Aggregation), before Phase 4 (Reporting):

```markdown
## Phase 3.5: Root Cause Analysis

After aggregating violations, activate root-cause-analysis:

Use Skill tool:
Skill("root-cause-analysis")

The skill analyzes:
1. When violations were introduced (temporal)
2. Who introduced them (authorship)
3. Where they cluster (structural)
4. Why they exist (root cause)

Returns systemic fixes, not just individual remediation.
```

### Anti-Patterns to Prevent

❌ WRONG: Fix 15 bare except clauses individually, next week 10 new ones appear

✅ RIGHT: Analyze root cause (legacy code → migration script, new dev → training), add pre-commit hook to prevent recurrence

### Success Metrics

Before: 60% recurrence, 2-3 hour fixes
After: 10% recurrence, 30 min fixes with prevention

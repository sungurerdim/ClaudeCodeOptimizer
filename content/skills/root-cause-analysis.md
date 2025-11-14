---
metadata:
  name: "Root Cause Analysis"
  activation_keywords: ["root cause", "why violations", "pattern analysis", "systemic fix"]
  category: "analysis"
principles: ['U_ROOT_CAUSE_ANALYSIS', 'U_EVIDENCE_BASED', 'U_FAIL_FAST', 'U_DRY', 'U_COMPLETE_REPORTING', 'U_CHANGE_VERIFICATION']
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

### Example 1: Security Issue Root Cause

```
User runs: /cco-audit-security
Output: "15 hardcoded secrets found"

Skill activates:
"Analyzing patterns in 15 secret violations..."

=== Root Cause Analysis ===

Violation Type: Hardcoded Secrets (P_PRIVACY_FIRST)
Total Count: 15 violations

ANALYSIS:

Temporal Distribution:
- LEGACY (>1yr): 11 violations (73%)
- OLD (6-12mo): 3 violations (20%)
- RECENT (<6mo): 1 violation (7%)

File Types:
- .env.backup files: 8 violations (53%)
- config.py files: 5 violations (33%)
- test fixtures: 2 violations (13%)

ROOT CAUSES:

1. PRIMARY: .env.backup Files (53%)
   - Developers created backups with "cp .env .env.backup"
   - Forgot to add to .gitignore
   - Evidence: All .env.backup files in git history

2. SECONDARY: Legacy Config (33%)
   - Before we used environment variables
   - Hardcoded in config.py
   - Evidence: All files >1 year old

3. TERTIARY: Test Fixtures (13%)
   - NOT real secrets (password123, test_api_key)
   - False positives

SYSTEMIC FIXES:

Priority 1 (Backup Files):
[ ] Add .env.backup to .gitignore
[ ] Run: git rm --cached **/.env.backup
[ ] Add pre-commit hook: Block .env.backup files
[ ] Documentation: "Never commit .env backups"

Priority 2 (Legacy Config):
[ ] Run: /cco-migrate-secrets-to-env
[ ] Create .env.example templates
[ ] Update deployment docs

Priority 3 (Test Fixtures):
[ ] Whitelist test_*/ directories in secret scanner
[ ] Add comment: # nosec (tell scanner to ignore)

PREVENTIVE MEASURES:

1. Pre-commit hook: Scan for new secrets
2. .gitignore template: Include common secret patterns
3. Team training: Secret management best practices
4. CI/CD: Fail build if secrets detected

TIMELINE:

Day 1: Add .gitignore entries + pre-commit hook
Day 2: Migrate legacy secrets to .env
Day 3: Update test fixtures (whitelist)
Day 4: Team training session
```

### Example 2: Test Coverage Root Cause

```
User runs: /cco-audit-tests
Output: "36 functions untested"

Skill activates:
"Analyzing patterns in 36 untested functions..."

=== Root Cause Analysis ===

Violation Type: Untested Functions
Total Count: 36 violations

ANALYSIS:

Function Types:
- Private helpers (_helper_func): 18 functions (50%)
- Public API: 12 functions (33%)
- Internal utilities: 6 functions (17%)

Service Distribution:
- services/worker/: 20 functions (56%)
- shared/: 10 functions (28%)
- services/api/: 6 functions (17%)

Code Age:
- LEGACY (>1yr): 24 functions (67%)
- RECENT (<6mo): 12 functions (33%)

ROOT CAUSES:

1. PRIMARY: Private Helpers (50%)
   - Team doesn't test private functions
   - Belief: "Only test public API"
   - Evidence: 0 tests for any _* function

2. SECONDARY: Legacy Untested Code (67%)
   - Old code before test requirements
   - Never retroactively tested
   - Evidence: Created before 2024 test mandate

3. TERTIARY: Worker Service Focus (56%)
   - Most untested code in worker service
   - Complex async code, hard to test
   - Evidence: worker/ has 45% coverage, api/ has 85%

SYSTEMIC FIXES:

Priority 1 (Testing Philosophy):
[Challenge team belief: "We should test private functions if complex"]
[ ] Team discussion: When to test private vs public
[ ] Document decision in TESTING.md
[ ] Update coverage rules: Include private if >10 lines

Priority 2 (Legacy Code):
[ ] Identify CRITICAL untested functions (payment, auth)
[ ] Write tests for critical functions first (5 functions)
[ ] Then high-value functions (15 functions)
[ ] Then remaining (16 functions)

Priority 3 (Worker Service):
[ ] Training: Testing async/celery tasks
[ ] Add test utilities: mock_celery, async_test decorator
[ ] Pair programming: Test 3 worker functions together

PREVENTIVE MEASURES:

1. Pre-commit hook: Block new functions without tests
2. Code review checklist: "Tests added?" required
3. CI/CD: Fail if coverage drops below 80%
4. Team training: Async testing patterns

TIMELINE:

Week 1: Team discussion + testing guidelines
Week 2: Test 5 critical functions
Week 3: Test 15 high-value functions
Week 4: Test remaining 16 functions
```

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

#### WRONG: Fix Symptoms Only

```
User: "15 bare except clauses found. I'll fix them."
<Spends 3 hours editing 15 files>
<Commits>

Next week:
"10 new bare except clauses found"
User: "Why do these keep appearing?!"
```

#### RIGHT: Fix Root Cause

```
Skill: "15 bare except clauses found. Analyzing root cause..."
Skill: "80% are legacy code (>1 year old). Fix with migration script?"
User: "Yes"
Skill: "Running /cco-migrate-legacy --principle=U_FAIL_FAST..."
Skill: "✓ 12 legacy violations fixed in 30 seconds"
Skill: "Remaining 3 are recent. Analyzing authorship..."
Skill: "All by alice@company.com (new team member). Schedule training?"
User: "Yes"
Skill: "✓ Scheduled 1-on-1 with Alice for next week"
Skill: "Adding pre-commit hook to prevent new violations..."
Skill: "✓ Pre-commit hook added"

Next week:
"0 new bare except clauses" (pre-commit hook blocks them)
Alice: "My code was blocked by pre-commit. Found U_FAIL_FAST docs, using specific exceptions now ✓"
```

### Success Metrics

**Before (without skill):**
- Recurrence rate: 60% (violations return)
- Fix time: 2-3 hours (individual fixes)
- Learning: None (same mistakes repeat)

**After (with skill):**
- Recurrence rate: 10% (systemic fixes prevent)
- Fix time: 30 minutes (scripts + automation)
- Learning: High (team understands WHY)

### When to Skip This Skill

Skip root cause analysis if:
- <3 violations of same type (not enough data)
- Violations are unrelated (no pattern)
- User explicitly requests: `/cco-audit-principles --no-root-cause`

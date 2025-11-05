---
name: incremental-improvement
description: Break overwhelming tasks into achievable milestones
version: 1.0.0
category: planning
applies_to:
  - audit-tests
  - generate-tests
  - audit-principles
activation: after_large_gap_detected
---

# Incremental Improvement Protocol

**Purpose:** Transform overwhelming goals into achievable milestones. Prevent paralysis from "too much to fix".

---

## When This Skill Activates

This skill activates when audit shows LARGE gap:
- `/cco-audit-tests` finds 20+ untested functions
- `/cco-audit-principles` finds 30+ violations
- Any audit shows "this will take days" amount of work

**Trigger:** Gap > threshold (configurable, default: 20 items)

---

## The Core Principle

**Don't try to fix everything at once. Break into weekly sprints with celebration milestones.**

Why?
- Overwhelming tasks lead to procrastination
- All-or-nothing approach often becomes nothing
- Progress > Perfection

---

## The Protocol

### Step 1: PRIORITIZE by Impact

**For test coverage:**
```
Priority 0 (CRITICAL): Functions that handle money, auth, data validation
Priority 1 (HIGH): Business logic, workflows, integrations
Priority 2 (MEDIUM): Utilities, helpers
Priority 3 (LOW): Internal plumbing, getters/setters
```

**For principle violations:**
```
Priority 0 (CRITICAL): Security, privacy, data loss risks
Priority 1 (HIGH): DRY, architecture, type safety
Priority 2 (MEDIUM): Code quality, testing
Priority 3 (LOW): Style, optimization
```

### Step 2: SET Weekly Milestones

**Formula:**
```
Week 1: P0 → 100% (ship-blocking issues)
Week 2: P1 → 80% (high-value improvements)
Week 3: P2 → 80% (remaining gap)
Week 4: Polish + buffer
```

### Step 3: TRACK Progress

Save state in `.cco/state/{PROJECT}/incremental-progress.json`:
```json
{
  "goal": "Reach 80% test coverage",
  "current": "64%",
  "target": "80%",
  "weeks": [
    {
      "week": 1,
      "milestone": "Critical paths to 100%",
      "functions": ["process_payment", "validate_auth", "encrypt_data"],
      "status": "completed",
      "coverage_delta": "+8%"
    },
    {
      "week": 2,
      "milestone": "High-value to 80%",
      "functions": ["create_user", "send_email", "..."],
      "status": "in_progress",
      "coverage_delta": "+6%"
    }
  ]
}
```

### Step 4: CELEBRATE Milestones

After each week:
```
"🎉 Week 1 Complete!"
"Critical paths at 100%"
"Coverage: 64% → 72% (+8%)"
"Ship-blocking issues resolved ✓"
"Ready for Week 2?"
```

---

## Examples

### Example 1: Test Coverage Gap

**Scenario:**
```
User runs: /cco-audit-tests
Output: "36 untested functions, 64% coverage (goal: 80%)"
```

**Without skill (overwhelming):**
```
User: "I need to write 36 tests?! That's days of work..."
<Procrastinates>
<Never starts>
```

**With skill (achievable):**
```
Skill activates:
"36 untested functions detected. That's a lot! Let's break it down."

Analyzing function criticality...

=== Incremental Improvement Plan ===

Current: 64% coverage
Target: 80% coverage
Gap: 36 functions

WEEK 1: Critical Paths (MUST-HAVE)
Goal: 100% coverage for payment, auth, data validation
Functions to test:
  [ ] process_payment()           - services/payment/stripe.py:45
  [ ] validate_auth_token()        - shared/auth.py:67
  [ ] sanitize_user_input()        - shared/validators.py:23
  [ ] encrypt_sensitive_data()     - shared/crypto.py:89
  [ ] execute_database_query()     - shared/db.py:112

Impact: Coverage 64% → 72% (+8%)
Estimated effort: 3 hours
Priority: CRITICAL (ship-blockers)

Start Week 1? (y/n)
```

**User:** y

```
Generating tests for Week 1 functions...

✓ test_process_payment.py created (5 test cases)
✓ test_validate_auth_token.py created (8 test cases)
✓ test_sanitize_user_input.py created (6 test cases)
✓ test_encrypt_sensitive_data.py created (4 test cases)
✓ test_execute_database_query.py created (7 test cases)

Running tests...
✓ 30/30 tests pass

Running coverage...
Coverage: 64% → 72%

🎉 WEEK 1 COMPLETE!

Critical paths at 100% ✓
Coverage increased 8% ✓
Ship-blocking issues resolved ✓

Ready for Week 2? (y/n)
```

**User:** y

```
WEEK 2: High-Value Functions
Goal: 80% coverage for business logic
Functions to test (12 total):
  [ ] create_user()
  [ ] send_email_notification()
  [ ] generate_report()
  [ ] sync_to_external_api()
  ... (8 more)

Impact: Coverage 72% → 78% (+6%)
Estimated effort: 4 hours
Priority: HIGH

Start Week 2? (y/n)
```

### Example 2: Principle Violations

**Scenario:**
```
User runs: /cco-audit-principles
Output: "47 violations found across 8 principles"
```

**With skill:**
```
"47 violations detected. Let's prioritize by severity."

=== Incremental Improvement Plan ===

Current: 47 violations
Target: 0 violations
Categories: 8 principles

WEEK 1: Critical Security Issues (P0)
Principles: P019 (Secrets), P021 (Encryption), P022 (Zero Disk)
Violations to fix:
  [ ] P019: 3 hardcoded secrets
  [ ] P021: 5 missing encryption
  [ ] P022: 2 disk writes with sensitive data

Total: 10 violations
Impact: All P0 CRITICAL resolved
Estimated effort: 2 hours
Priority: BLOCKING DEPLOYMENT

WEEK 2: High-Impact Quality (P1)
Principles: P001 (Fail-Fast), P002 (DRY), P023 (Type Safety)
Violations to fix:
  [ ] P001: 8 bare except clauses
  [ ] P002: 6 duplicate functions
  [ ] P023: 12 missing type hints

Total: 26 violations
Impact: All P1 HIGH resolved
Estimated effort: 4 hours

WEEK 3: Code Quality (P2)
Principles: P003 (Integration), P006 (Precision)
Violations to fix:
  [ ] P003: 7 integration tests missing
  [ ] P006: 4 float comparison issues

Total: 11 violations
Impact: All P2 MEDIUM resolved
Estimated effort: 2 hours

Timeline:
Week 1 → 47 violations → 37 violations (21% reduction)
Week 2 → 37 violations → 11 violations (55% reduction)
Week 3 → 11 violations → 0 violations (100% compliance)

Total effort: 8 hours over 3 weeks

Start Week 1? (y/n)
```

### Example 3: Mid-Sprint Progress Check

**User runs:** `/cco-status`

```
Incremental Improvement Status:

Goal: 80% test coverage
Started: 2025-01-08
Current: Week 2, Day 3

Progress:
✓ Week 1: Critical Paths (COMPLETED)
  - 5/5 functions tested
  - Coverage: 64% → 72% (+8%)
  - Completed: 2025-01-12

→ Week 2: High-Value Functions (IN PROGRESS)
  - 8/12 functions tested (67%)
  - Coverage: 72% → 76% (+4% so far)
  - Remaining: 4 functions
  - Estimated completion: 2025-01-19

  Pending functions:
  [ ] sync_to_external_api()    - services/api/sync.py:45
  [ ] batch_process_records()   - services/worker/batch.py:89
  [ ] validate_schema()         - shared/validation.py:123
  [ ] transform_data()          - shared/transforms.py:67

  Week 2 on track ✓

□ Week 3: Remaining Functions (NOT STARTED)
  - 16 functions queued
  - Estimated effort: 3 hours
  - Start date: 2025-01-22

Overall Progress: 13/36 functions tested (36%)
Coverage: 64% → 76% (+12% / +16% target)
ETA: 2025-01-29 (19 days remaining)

Continue Week 2? (y/n)
```

---

## Milestone Celebration Examples

### Week 1 Complete
```
┌─────────────────────────────────────┐
│  🎉 WEEK 1 MILESTONE ACHIEVED! 🎉  │
└─────────────────────────────────────┘

Critical Paths: 100% Tested ✓

Before: 64% coverage (ship-blocking risk)
After:  72% coverage (safe to deploy)
Delta:  +8%

Functions Protected:
  ✓ process_payment()        (handles money)
  ✓ validate_auth_token()    (security)
  ✓ sanitize_user_input()    (prevents injection)
  ✓ encrypt_sensitive_data() (privacy)
  ✓ execute_database_query() (data integrity)

Impact:
  • No more payment bugs slipping through
  • Auth vulnerabilities caught by tests
  • SQL injection attacks prevented
  • Encryption always validated

Team morale: 📈
Deployment confidence: 📈📈

Next: Week 2 - High-value functions
Ready? (y/n)
```

### Week 2 Complete
```
┌─────────────────────────────────────┐
│  🎉 WEEK 2 MILESTONE ACHIEVED! 🎉  │
└─────────────────────────────────────┘

High-Value Functions: 80% Tested ✓

Before: 72% coverage
After:  78% coverage
Delta:  +6%

Functions Protected (12 total):
  ✓ create_user()
  ✓ send_email_notification()
  ✓ generate_report()
  ✓ sync_to_external_api()
  ... (8 more)

Progress:
  Week 1: Critical paths ✓
  Week 2: High-value logic ✓
  Week 3: Remaining functions (in progress)

Total coverage improvement: 64% → 78%
We're 12% away from 80% goal!

Almost there! One more week!
```

### Final Goal Achieved
```
┌──────────────────────────────────────┐
│  🎊 80% COVERAGE ACHIEVED! 🎊        │
│  PROJECT GOAL REACHED! 🏆            │
└──────────────────────────────────────┘

Journey:
  Start:  64% (36 untested functions)
  Week 1: 72% (+8%) - Critical paths
  Week 2: 78% (+6%) - High-value
  Week 3: 82% (+4%) - Remaining
  Final:  82% coverage ✓

Total functions tested: 38
Total test cases written: 147
Time invested: 9 hours (3 weeks)

Impact:
  • 100% critical paths covered
  • 92% business logic covered
  • 78% utilities covered
  • Deployment confidence: VERY HIGH

What changed:
  Before: Fear of refactoring
  After:  Confidence to ship

Team learned:
  • Incremental > All-at-once
  • Progress > Perfection
  • Celebrate milestones

Next goals:
  • Maintain 80%+ coverage
  • Add mutation testing
  • Improve test quality

Congratulations! 🎉
```

---

## Integration with Commands

### audit-tests.md
Add after reporting, if gap > 20 functions:

```markdown
## Phase 5: Incremental Improvement Planning (if large gap)

If 20+ untested functions, activate incremental-improvement:

Use Skill tool:
Skill("incremental-improvement")

The skill will:
1. Prioritize functions by criticality
2. Create weekly milestones
3. Track progress
4. Celebrate achievements
```

### audit-principles.md
Add after reporting, if violations > 30:

```markdown
## Phase 5: Incremental Fix Planning (if many violations)

If 30+ violations, activate incremental-improvement:

Use Skill tool:
Skill("incremental-improvement")

Break fixes into manageable weekly sprints.
```

---

## State Management

Track progress in `.cco/state/{PROJECT}/incremental-progress.json`:

```json
{
  "goal_type": "test_coverage",
  "goal_target": 80,
  "baseline": 64,
  "current": 76,
  "start_date": "2025-01-08",
  "weeks": [
    {
      "week_number": 1,
      "milestone": "Critical Paths",
      "target_coverage": 72,
      "actual_coverage": 72,
      "status": "completed",
      "completion_date": "2025-01-12",
      "functions_tested": [
        "process_payment",
        "validate_auth_token",
        "sanitize_user_input",
        "encrypt_sensitive_data",
        "execute_database_query"
      ]
    },
    {
      "week_number": 2,
      "milestone": "High-Value Functions",
      "target_coverage": 78,
      "actual_coverage": 76,
      "status": "in_progress",
      "functions_tested": [
        "create_user",
        "send_email",
        "generate_report",
        "sync_api"
      ],
      "functions_pending": [
        "batch_process",
        "validate_schema",
        "transform_data"
      ]
    }
  ],
  "total_items": 36,
  "completed_items": 13,
  "completion_percentage": 36
}
```

**Resume command:**
```bash
/cco-continue-improvement
```

---

## Anti-Patterns to Prevent

### ❌ WRONG: All-or-Nothing

```
User: "36 functions to test. I'll do it all this weekend."
<Works Saturday and Sunday>
<Gets 20/36 done, exhausted>
<Gives up>
Result: 20 tests but no systematic approach
```

### ✅ RIGHT: Incremental Progress

```
Skill: "36 functions. Let's do 5 critical ones this week."
User: <Works 3 hours, finishes 5>
Skill: "🎉 Week 1 done! Coverage +8%! Ship-blockers resolved!"
User: <Feels accomplished>
Week 2: <Does 12 more>
Week 3: <Does remaining 16>
Result: All 36 tested with sustainable pace
```

---

## Success Metrics

**Before (without skill):**
- Completion rate: 30% (give up when overwhelmed)
- Time to complete: Never (or 6 months)
- Team morale: Low (failure feels bad)

**After (with skill):**
- Completion rate: 85% (milestones achievable)
- Time to complete: 3-4 weeks (systematic)
- Team morale: High (celebrate every week)

---

## When to Skip This Skill

Skip incremental planning if:
- Gap is small (<20 items)
- User has time to fix all at once
- User explicitly requests: `/cco-audit-tests --no-incremental`

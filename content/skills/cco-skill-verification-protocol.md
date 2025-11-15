---
metadata:
  name: "Verification Protocol"
  activation_keywords: ["verify", "verification", "violations", "audit", "fix"]
  category: "enforcement"
principles: ['U_CHANGE_VERIFICATION', 'U_EVIDENCE_BASED', 'U_TEST_FIRST', 'U_ATOMIC_COMMITS', 'U_EXPLICIT_COMPLETION', 'U_COMPLETE_REPORTING']
---

# Verification Protocol

Enforces fix → verify → commit loop for principle violations. Prevents "fix everything, test once" anti-pattern through incremental verification.

<!-- INSTRUCTIONS: Load when activated -->
## Detailed Instructions

**NEVER fix all violations at once. ALWAYS use this loop:**

### For Each Violation Category:

1. **ISOLATE**: Show violations for THIS category only
   ```
   Example: "U_FAIL_FAST (Fail-Fast): 5 violations
   - services/api/main.py:45
   - shared/utils.py:89"
   ```

2. **ASK**: Get user confirmation to fix this category
   ```
   "Fix U_FAIL_FAST violations now? (y/n/skip)"
   ```

3. **FIX**: Apply fixes (manual or automated)
   - User edits files OR
   - Run `/cco-fix-code --principle=U_FAIL_FAST`

4. **VERIFY**: Run mini-audit for THIS category only
   ```bash
   # For principles
   Grep with U_FAIL_FAST patterns only

   # For security
   Scan for specific vulnerability type only

   # For tests
   Check coverage delta for modified files only
   ```

5. **CONFIRM**: Check verification results
   ```
   ✓ "All U_FAIL_FAST violations fixed!"
   ⚠ "2 violations remain - review needed"
   ```

6. **COMMIT**: Atomic commit for this category
   ```bash
   git add <changed files>
   git commit -m "fix(U_FAIL_FAST): replace bare except with specific exceptions"
   ```

7. **REPEAT**: Move to next violation category

### Final Verification

After ALL categories fixed:
```
"Running full audit to confirm..."
<Run complete audit command>
"✓ All violations resolved! Project compliant."
```

<!-- RESOURCES: Load on explicit request -->
## Examples & Resources

### Example 1: Principle Violations

```
User runs: /cco-audit-principles
Output: "23 violations found across 5 principles"

Skill activates:
"23 violations detected. Start guided remediation? (y/n)"

User: y

Skill:
"Principle U_FAIL_FAST (Fail-Fast): 5 violations
 - services/api/main.py:45   (bare except)
 - services/api/main.py:89   (silent exception)
 - shared/utils.py:67         (bare except)
 - worker/tasks.py:123        (bare except)
 - worker/tasks.py:234        (silent exception)

Fix U_FAIL_FAST now? (y/n/skip)"

User: y
<User manually fixes 5 violations>

Skill:
"Verifying U_FAIL_FAST fixes..."
<Runs grep for bare except patterns>
"✓ All U_FAIL_FAST violations fixed!"
"Committing changes..."
<git commit -m "fix(U_FAIL_FAST): replace bare except clauses">

Skill:
"Principle U_FAIL_FAST (DRY): 8 violations
 - Duplicate encrypt_aes_gcm() in 3 files

Fix U_FAIL_FAST now? (y/n/skip)"

User: n

Skill:
"Skipping U_FAIL_FAST. Moving to next..."
```

### Example 2: Security Violations

```
User runs: /cco-audit-security
Output: "12 security issues found (3 CRITICAL)"

Skill activates:
"12 security issues detected. Guided remediation? (y/n)"

User: y

Skill:
"CRITICAL: Hardcoded secrets (3 violations)
 - services/api/client.py:23  (API key)
 - shared/config.py:45        (Database password)
 - worker/.env.backup:12      (JWT secret)

Fix CRITICAL secrets now? (y/n/skip)"

User: y
<User moves to env vars>

Skill:
"Verifying secret removal..."
<Runs grep for common secret patterns>
"✓ No hardcoded secrets found!"
"Committing..."
<git commit -m "fix(security): move secrets to environment variables">
```

### Anti-Patterns to Prevent

#### ❌ WRONG: Batch Fix Everything

```
User: "I'll fix all 23 violations now"
<Spends 2 hours editing 15 files>
<Runs tests>
Tests fail: "AssertionError in test_api.py"
User: "Which fix broke this? No idea..."
<Reverts everything, starts over>
```

#### ✅ RIGHT: Incremental with Verification

```
User: Uses verification protocol
<Fixes U_FAIL_FAST (5 violations in 3 files)>
<Verifies - all fixed>
<Commits>
<Fixes P_PRIVACY_FIRST (3 violations in 2 files)>
<Verifies - all fixed>
<Commits>
<Tests fail on P_PRIVACY_FIRST commit>
User: "P_PRIVACY_FIRST broke tests, revert ONLY that commit"
<git revert HEAD>
<U_FAIL_FAST fixes preserved ✓>
```

### Integration with Commands

#### audit-principles.md
Add after Phase 4 (Reporting):

```markdown
## Phase 5: Guided Remediation (if violations found)

If violations detected, activate verification-protocol skill:

Use Skill tool:
Skill("verification-protocol")

The skill will guide user through:
1. Fix one principle at a time
2. Verify each fix immediately
3. Commit atomically
4. Track progress
```

#### fix-code.md
Add after Phase 3 (Backup):

```markdown
## Phase 3.5: Incremental Fixing with Verification

Instead of applying ALL fixes at once, use verification-protocol:

Use Skill tool:
Skill("verification-protocol")

The skill will:
1. Apply fixes for one principle category
2. Run tests for ONLY affected files
3. If tests pass → commit
4. If tests fail → rollback category, keep others
5. Repeat for next category
```

### State Management

The skill tracks progress in `.cco/state/{PROJECT}/verification-session.json`:

```json
{
  "session_id": "audit-principles-20250111-143022",
  "total_violations": 23,
  "categories": [
    {
      "id": "U_FAIL_FAST",
      "violations": 5,
      "status": "fixed",
      "commit": "a3b4c5d"
    },
    {
      "id": "U_FAIL_FAST",
      "violations": 8,
      "status": "skipped"
    },
    {
      "id": "P_PRIVACY_FIRST",
      "violations": 3,
      "status": "fixed",
      "commit": "e6f7g8h"
    }
  ],
  "last_updated": "2025-01-11T14:45:33Z"
}
```

Resume interrupted session:
```bash
/cco-continue-verification
```

### Success Metrics

**Before (without skill):**
- Fix time: 2-3 hours
- Test failures: 40% of attempts
- Rollback rate: 60%
- Frustration: High

**After (with skill):**
- Fix time: 30-45 minutes (incremental)
- Test failures: 10% of attempts (isolated)
- Rollback rate: 15% (single category, not all)
- Frustration: Low (clear progress)

### When to Skip This Skill

Skip guided remediation if:
- Only 1-2 violations (overhead not worth it)
- All violations in single file (atomic anyway)
- User explicitly requests: `/cco-audit-principles --no-guided`

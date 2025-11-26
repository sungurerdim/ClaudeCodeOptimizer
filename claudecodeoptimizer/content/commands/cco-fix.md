---
name: cco-fix
description: Auto-fix issues with safe/risky categorization
categories: same as cco-audit
---

# /cco-fix

**Auto-fix detected issues**

---

## Flow: Confirm → Review → Apply → Verify

### Confirm
Check for context from `/cco-audit`. If none, run audit first.

### Review
Categorize fixes:
- **Safe** (auto-apply): Parameterize queries, remove dead code, externalize secrets
- **Risky** (approval needed): Auth changes, DB schema, API contracts

Present fix plan. User selects what to apply.

### Apply
1. Apply safe fixes automatically
2. Present risky fixes one by one
3. Track progress with TodoWrite

### Verify
1. Read file after each change
2. Run tests if available
3. Report: done + skip + fail = total

---

## Safe vs Risky

### Safe (Auto-Apply)
- Parameterize SQL queries
- Remove unused imports/code
- Move secrets to env vars
- Add input validation
- Fix linting issues
- Add type hints
- Update patch dependencies

### Risky (Approval Required)
- Add CSRF protection
- Change authentication
- Modify DB schema
- Change API contracts
- Major dependency updates
- Add caching layers

---

## Output Format

```markdown
# Fix Results

**Applied:** {done} | **Skipped:** {skip} | **Failed:** {fail}
**Verification:** {done} + {skip} + {fail} = {total} ✓

## Changes Made
✓ {file}:{line} - {change}

## Remaining
- {file}:{line} - {issue} (needs manual fix)

## Next Steps
→ Run tests: {test_command}
→ Review: git diff
→ Commit: /cco-commit
```

---

## Context Passing

Receive from `/cco-audit`:
```markdown
CONTEXT FOR /cco-fix:
{issue list with file:line}
```

Pass to `/cco-generate`:
```markdown
CONTEXT FOR /cco-generate:
Fixed {count} files. Need tests for: {file_list}
```

---

## Usage

```bash
/cco-fix                      # Interactive (runs audit if needed)
/cco-fix --security           # Fix security issues
/cco-fix --tech-debt          # Clean up code
/cco-fix --all                # Fix everything safe
/cco-fix --security "auth"    # With focus context
```

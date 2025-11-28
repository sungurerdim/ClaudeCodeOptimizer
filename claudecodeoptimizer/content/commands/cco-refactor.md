---
name: cco-refactor
description: Verified transformations with rollback
---

# /cco-refactor

**Risk mitigation** - Find ALL references → transform in order → verify → rollback on failure.

## Pre-Operation Safety

Requires clean git state. If uncommitted changes exist, AskUserQuestion:
→ Commit first (cco-commit) / Stash / Cancel

## Project Context

Load project context to calibrate refactoring risk assessment.

### Check Existing Context

```bash
cat .claude/cco_context.yaml 2>/dev/null
```

### Context Flow

**If exists:** Ask if still valid (Yes / Update / Refresh)
**If not exists:** Gather with conditional questions (see content/shared/project-context.md)

### Context-Aware Risk Assessment

Adjust risk tolerance based on context:

- **Rollback: git** → More aggressive refactors acceptable
- **Rollback: user_data** → Extra caution, smaller steps
- **Time pressure: urgent** → Defer non-critical refactors
- **Team: 6+** → Consider breaking change impact on others
- **Data: financial** → Extra verification steps for data-touching code

### Using Context

When planning refactors:
- Factor context into "Proceed / Cancel" recommendation
- Suggest deferral if context indicates high risk
- Adjust verification depth based on impact level

## Flow

1. **Map** - Find all refs: definition, imports, calls, types, tests, docs
2. **Plan** - Show affected files, reference count
3. **Confirm** - AskUserQuestion: Proceed / Cancel / Details
4. **Transform** - Apply in order: definition → types → callers → imports → tests → docs
5. **Verify** - After each file: grep old = 0, grep new = expected

## Incremental Verification

After each file change:
- Verify grep counts
- If mismatch: rollback, report which file failed
- Continue only if all checks pass

## Operations

```bash
/cco-refactor rename oldName newName
/cco-refactor move old/path.py new/path.py
/cco-refactor extract "code" new_module.py
/cco-refactor inline helperFunction
```

## Rollback

On any failure:
- Revert all changes (`git checkout .`)
- Report which step failed
- Suggest manual review

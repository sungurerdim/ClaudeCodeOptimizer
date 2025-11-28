---
name: cco-refactor
description: Verified transformations with rollback
---

# /cco-refactor

**Risk mitigation** - Find ALL references → transform in order → verify → rollback on failure.

## Pre-Operation Safety

Requires clean git state. If uncommitted changes exist, AskUserQuestion:
→ Commit first (cco-commit) / Stash / Cancel

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

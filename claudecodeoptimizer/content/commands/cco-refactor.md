---
name: cco-refactor
description: Verified transformations with rollback
---

# /cco-refactor

**Risk mitigation** - Find ALL references → transform in order → verify → rollback on failure.

**Standards:** Pre-Operation Safety | Context Read | Approval Flow | Reference Integrity | Verification | Error Format

Requires clean git state. If uncommitted changes exist → Commit / Stash / Cancel

## Context Application
- **Rollback** - If DB/User-data → extra caution, suggest backup first
- **Type** - Library: warn about public API changes
- **Breaking** - If Never → require deprecation path; if Allowed → clean rename OK
- **Maturity** - If Legacy → prefer wrap over modify; if Greenfield → aggressive OK

## Flow

1. **Map** - Find all refs: definition, imports, calls, types, tests, docs
2. **Plan** - Show affected files, reference count
3. **Confirm** - AskUserQuestion per Approval Flow
4. **Transform** - Apply in order: definition → types → callers → imports → tests → docs
5. **Verify** - After each file: grep old = 0, grep new = expected

## Incremental Verification

After each file change:
- Verify grep counts
- If mismatch: rollback, report which file failed
- Continue only if all checks pass

## Operations

```bash
/cco-refactor rename {old_name} {new_name}
/cco-refactor move {old_path} {new_path}
/cco-refactor extract "{code_block}" {new_module}
/cco-refactor inline {function_name}
```

## Rollback

On any failure:
- Revert all changes (`git checkout .`)
- Report which step failed
- Suggest manual review

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

**First:** Run `/cco-calibrate` to ensure context is loaded.

Read `CCO_CONTEXT_START` block from CLAUDE.md:
- **Guidelines** - Follow listed guidelines
- **Rollback** - If DB/User-data → extra caution, suggest backup first
- **Type** - Library: warn about public API changes

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
/cco-refactor rename {old_name} {new_name}
/cco-refactor move {old_path} {new_path}
/cco-refactor extract "{code_block}" {new_module}
/cco-refactor inline {function_name}
```

All operations work with any file type - paths and names are detected from your project.

## Rollback

On any failure:
- Revert all changes (`git checkout .`)
- Report which step failed
- Suggest manual review

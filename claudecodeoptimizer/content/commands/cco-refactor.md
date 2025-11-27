---
name: cco-refactor
description: Verified transformations with rollback
---

# /cco-refactor

**Risk mitigation** - Find ALL references → transform in order → verify → rollback on failure.

## Agent Delegation

| Phase | Agent | Purpose |
|-------|-------|---------|
| Map | `cco-agent-scan` | Find all references (read-only) |
| Transform | `cco-agent-action` | Apply changes with verification |

### MANDATORY Agent Rules

1. **NEVER use direct Edit/Write tools** - delegate to agents
2. **ALWAYS use agents as first choice**, not fallback after errors
3. Map phase → `cco-agent-scan`
4. Transform phase → `cco-agent-action`

### Error Recovery

On "File unexpectedly modified" or tool errors:
1. Do NOT retry with direct tools
2. Immediately delegate to `cco-agent-action`
3. Agent reads fresh and applies changes
4. If still fails, rollback and report

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

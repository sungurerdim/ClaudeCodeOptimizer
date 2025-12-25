---
name: cco-agent-apply
description: Write operations with verification
tools: Grep, Read, Glob, Bash, Edit, Write, NotebookEdit
model: opus
---

# cco-agent-apply

Execute approved changes with verification. **Fix everything, leave nothing behind.**

## Core Principle [CRITICAL]

Every finding MUST be fixed. No "manual" or "skip" unless:
1. User explicitly declined in AskUserQuestion
2. Fix would break working code (verified by tests)

## Execution [CRITICAL]

**Maximize parallelization at every step. ALL independent tool calls in SINGLE message.**

| Step | Action | Tool Calls | Execution |
|------|--------|------------|-----------|
| 1. Pre-check | Git status | `Bash(git status --short)` | Single |
| 2. Read | All affected files | `Read(file, offset, limit=30)` × N | **PARALLEL** |
| 3. Apply | All independent edits | `Edit(file, fix)` × N | **PARALLEL** (different files) |
| 4. Verify | All checks | `Bash(lint)`, `Bash(type)`, `Bash(test)` | **PARALLEL** |
| 5. Cascade | If new errors | Repeat 3-4 | Sequential |

**CRITICAL Parallelization Rules:**
```javascript
// Step 2: ALL file reads in ONE message
Read("{file_path}")        // All these
Read("{file_path}")        // must be in
Read("{file_path}")        // SINGLE message

// Step 3: Edits to DIFFERENT files in ONE message
Edit("{file_path}", {fix})   // Parallel for
Edit("{file_path}", {fix})   // different files

// Step 4: ALL verification in ONE message
Bash("{lint_command} 2>&1")
Bash("{type_command} 2>&1")
Bash("{test_command} 2>&1")
```

**Rules:** Fix ALL issues │ Parallel reads │ Parallel edits (different files) │ Parallel verification

## Embedded Rules

| Category | Rules |
|----------|-------|
| Safety | Pre-op git status │ Dirty → Commit/Stash/Continue │ Rollback via clean state |
| Tracking | TODO list with ALL items │ One in_progress at a time │ `done + declined + fail = total` |
| Skip | `.git/`, `node_modules/`, `vendor/`, `.venv/`, `dist/`, `build/`, `fixtures/`, `testdata/`, `__snapshots__/`, `examples/` |
| Write | **Force-write always** │ Even if file exists with identical content │ Overwrite to ensure state consistency |

## Fix Categories

| Category | Auto-fix | Approval |
|----------|----------|----------|
| Formatting, Unused imports, Simple refactors, Magic numbers → constants, Missing type stubs | ✓ | |
| Security patches, File deletions, API/behavior changes, Dependency changes | | ✓ |

## Fix Strategies

### Security
| Issue | Fix |
|-------|-----|
| Path traversal | `os.path.realpath()` + prefix check |
| Unverified download | Checksum verification |
| Script execution | Pin version + hash check |
| Hardcoded secrets | `os.getenv()` |
| Permission bypass | Remove flag or add warning |

### Type Errors
| Error | Fix |
|-------|-----|
| Missing stubs | Install type stubs |
| Missing annotation | Add type hint |
| Type mismatch | Fix type or `cast()` |
| Any type | Replace with specific |
| Optional handling | Null check or assert |
| Import errors | Fix import path |

### Quality
| Issue | Fix |
|-------|-----|
| High complexity | Extract helper functions |
| Duplication | Create shared function |
| Magic numbers | Extract to constants |

## Write Operations [CRITICAL]

**Config file operations for cco-config. Always execute - never skip based on content comparison.**

### Modes

| Mode | Target | Behavior |
|------|--------|----------|
| `overwrite` | `context.md` | Delete existing → Write new (always) |
| `overwrite` | Rule files (`*.md`) | Delete existing → Write new (always) |
| `overwrite` | Statusline (`cco-*.js`) | Delete existing → Copy from package (always) |
| `merge` | `settings.json` (Setup) | Read existing → Deep merge → Write |
| `delete` | Rule files, directories | Remove entirely |
| `unmerge` | `settings.json` (Remove) | Read → Remove CCO keys only → Write |

**CRITICAL:** All `overwrite` targets are ALWAYS written. Never skip based on "file exists" or "content matches".

### Mode: overwrite
```python
def overwrite(path, content):
    if exists(path):
        delete(path)
    write(path, content)
```

### Mode: merge
```python
def merge(path, new_settings):
    existing = read_json(path) or {}
    result = deep_merge(existing, new_settings)  # new overrides, preserves unspecified
    write_json(path, result)
```

### Mode: delete
```python
def delete(path):
    if is_dir(path):
        rm_rf(path)
    else:
        rm(path)
```

### Mode: unmerge
```python
CCO_KEYS = ["alwaysThinkingEnabled", "statusLine"]
CCO_ENV_KEYS = ["ENABLE_LSP_TOOL", "MAX_THINKING_TOKENS",
                "MAX_MCP_OUTPUT_TOKENS", "BASH_MAX_OUTPUT_LENGTH"]

def unmerge(path):
    settings = read_json(path)

    # Remove top-level CCO keys
    for key in CCO_KEYS:
        settings.pop(key, None)

    # Remove CCO env keys (preserve others)
    if "env" in settings:
        for key in CCO_ENV_KEYS:
            settings["env"].pop(key, None)
        if not settings["env"]:  # Empty dict
            del settings["env"]

    write_json(path, settings)
```

### Operation Examples

**Setup/Update:**
```javascript
files: [
  // All overwrite - ALWAYS write, never skip
  { path: "rules/cco/context.md", mode: "overwrite", content: "{context_content}" },
  { path: "rules/cco/{language}.md", mode: "overwrite", content: "{rule_content}" },
  { path: "cco-{mode}.js", mode: "overwrite", source: "$CCO_PATH/cco-{mode}.js" },

  // Only settings.json is merged (preserves user settings)
  { path: "settings.json", mode: "merge", content: {
    alwaysThinkingEnabled: {thinking_enabled},
    env: {
      MAX_THINKING_TOKENS: "{budget}",
      MAX_MCP_OUTPUT_TOKENS: "{output_limit}",
      BASH_MAX_OUTPUT_LENGTH: "{output_limit}"
    }
  }}
]
```

**Remove:**
```javascript
files: [
  { path: "rules/cco/", mode: "delete" },
  { path: "settings.json", mode: "unmerge" }
]
```

### CCO-Managed Keys [SSOT]

| Key | Setup | Remove |
|-----|-------|--------|
| `alwaysThinkingEnabled` | Set | Delete |
| `statusLine` | Set (if not Skip) | Delete (if Remove selected) |
| `env.ENABLE_LSP_TOOL` | Set | Delete |
| `env.MAX_THINKING_TOKENS` | Set | Delete |
| `env.MAX_MCP_OUTPUT_TOKENS` | Set | Delete |
| `env.BASH_MAX_OUTPUT_LENGTH` | Set | Delete |

**Never touch:** User-added keys, `permissions` (unless explicitly selected)

## Verification & Cascade

**All verification runs in parallel.** If any fails → cascade fix → re-verify until clean.

```
Fix {SCOPE}-{NNN} → mypy error → Add import → mypy clean → Done
```

## Output Schema

```json
{
  "results": [{ "item": "{id}: {desc} in {file}:{line}", "status": "done|declined|fail", "verification": "..." }],
  "accounting": { "done": "{n}", "declined": "{n}", "fail": "{n}", "total": "{n}" },
  "verification": { "{linter}": "PASS|FAIL", "{type_checker}": "PASS|FAIL", "tests": "PASS|FAIL|N/A" }
}
```

**Status:** `done` (fixed) │ `declined` (user declined) │ `fail` (broke something)

**Invariant:** `done + declined + fail = total`

## Principles

Fix everything │ Verify after change │ Cascade fixes │ Complete accounting │ Reversible (clean git)

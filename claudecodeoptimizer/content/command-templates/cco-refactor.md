---
name: cco-refactor
description: Safe structural transformations with automatic rollback
allowed-tools: Read(*), Grep(*), Glob(*), Edit(*), Bash(git:*), Task(*), TodoWrite
---

# /cco-refactor

**Safe Refactoring** - Find ALL references → transform → verify → rollback on failure.

End-to-end: Maps references, transforms safely, verifies each step.

**Rules:** User Input | Safety | Reference Integrity | Task Tracking

## Context

- Context check: !`grep -c "CCO_ADAPTIVE_START" ./CLAUDE.md 2>/dev/null || echo "0"`
- Git status: !`git status --short`
- Current branch: !`git branch --show-current`

**Static context (Type, Breaking, Maturity, Scale, Team) is read from ./CLAUDE.md already in context.**

## Context Requirement [CRITICAL]

**This command requires CCO_ADAPTIVE in ./CLAUDE.md.**

If context check returns "0":
```
CCO_ADAPTIVE not found in ./CLAUDE.md

Run /cco-tune first to configure project context, then restart CLI.
```
**Stop execution immediately.**

Requires clean git state per Pre-Operation Safety rule.

## Context Application

| Field | Effect |
|-------|--------|
| Rollback | DB/User-data → extra caution, suggest backup first |
| Type | Library → warn about public API changes, check semver impact |
| Breaking | Never → require deprecation path; Allowed → clean rename OK |
| Maturity | Legacy → wrap don't modify, strangler pattern; Greenfield → aggressive OK |
| Scale | 10K+ → incremental refactors, feature flags; <100 → batch changes OK |
| Team | 6+ → document changes for team awareness, update ADRs |

## Agent Integration

| Phase | Agent | Scope | Purpose |
|-------|-------|-------|---------|
| Map | `cco-agent-analyze` | `references` | Cross-file reference mapping |
| Transform | `cco-agent-apply` | `refactor` | Execute approved changes |

**Reference Mapping:** Before any refactor operation, use `cco-agent-analyze` with `scope: references` to get complete reference map including definition, imports, calls, types, tests, and docs.

## Default Behavior

When called without operation:

**Use AskUserQuestion:**
| Question | Options | MultiSelect |
|----------|---------|-------------|
| Operation? | Rename; Move; Extract; Inline; Restructure | false |

After selection, prompt for required parameters using AskUserQuestion.

## Operations

### Rename

Rename function/class/variable across all references.

```bash
/cco-refactor rename {old_name} {new_name}
```

| Step | Action |
|------|--------|
| 1. Map | Find: definition, imports, calls, types, tests, docs |
| 2. Plan | Show affected files and reference counts |
| 3. Transform | Definition → types → callers → imports → tests → docs |
| 4. Verify | grep old = 0, grep new = expected |

### Move

Move file/module to new location, update all imports.

```bash
/cco-refactor move {old_path} {new_path}
```

| Step | Action |
|------|--------|
| 1. Map | Find all import statements referencing this path |
| 2. Plan | Show import paths to update |
| 3. Transform | Move file → update all imports |
| 4. Verify | All imports resolve, no broken references |

### Extract

Extract code block into new function/module.

```bash
/cco-refactor extract {target} --to={destination}
```

| Target | Destination | Example |
|--------|-------------|---------|
| Code block | New function | Extract lines 42-60 to `validate_input()` |
| Function | New module | Extract `parse_config()` to `config.py` |
| Class | New file | Extract `Logger` class to `logger.py` |
| Constant | Constants module | Extract magic values to `constants.py` |

### Extract Constant

Extract hardcoded values to named constants.

```bash
/cco-refactor extract-constant {value} {constant_name}
/cco-refactor extract-constant --all  # Find and extract all magic values
```

| Value Type | Action |
|------------|--------|
| Magic numbers | Extract to named constant |
| String literals | Extract to constant or config |
| Repeated values | Single constant, multiple refs |

### Inline

Inline function calls, remove unnecessary abstraction.

```bash
/cco-refactor inline {function_name}
```

| Step | Action |
|------|--------|
| 1. Map | Find all call sites |
| 2. Analyze | Check for side effects, multiple returns |
| 3. Transform | Replace calls with function body |
| 4. Remove | Delete function definition |
| 5. Verify | Behavior unchanged, tests pass |

### Restructure

Reorganize file/module structure.

```bash
/cco-refactor restructure --flatten {path}    # Flatten deep nesting
/cco-refactor restructure --split {file}      # Split large file
/cco-refactor restructure --merge {files...}  # Merge related files
```

#### Flatten

Reduce directory nesting while preserving functionality.

```
Before: src/utils/helpers/string/format.py
After:  src/utils/string_format.py
```

#### Split

Split large files into focused modules.

```
Before: utils.py (500 lines, 20 functions)
After:  utils/
        ├── __init__.py (re-exports)
        ├── string.py
        ├── date.py
        └── file.py
```

Criteria for splitting:
- Files > 300 lines
- Multiple unrelated concerns
- Low cohesion detected

#### Merge

Combine related small files.

```
Before: validators/email.py (20 lines)
        validators/phone.py (15 lines)
        validators/url.py (18 lines)
After:  validators.py (with all three)
```

Criteria for merging:
- Files < 50 lines
- High cohesion between files
- Same import patterns

## Flow

1. **Map** - Find all references (definition, imports, calls, types, tests, docs)
2. **Plan** - Show affected files, reference count
3. **Confirm** - User approval (Approval Flow)
4. **Transform** - Apply in order, verify each step
5. **Verify** - Final verification (grep counts, tests)
6. **Rollback** - On failure, revert all changes

## Incremental Verification

After each file change:
- Verify grep counts match expected
- If mismatch: rollback, report which file failed
- Continue only if all checks pass

## Output

**Follow output formats precisely.**

### Reference Map
```
┌─ REFERENCE MAP ──────────────────────────────────────────────┐
│ Type       │ Location           │ Count                      │
├────────────┼────────────────────┼────────────────────────────┤
│ Definition │ utils.py:42        │ 1                          │
│ Import     │ api.py, cli.py     │ 2                          │
│ Call       │ api.py:15, cli.py:8│ 5                          │
│ Type hint  │ types.py:22        │ 1                          │
│ Test       │ test_utils.py:30   │ 3                          │
│ Doc        │ README.md:85       │ 1                          │
├────────────┼────────────────────┼────────────────────────────┤
│ TOTAL      │ 8 files            │ 13 references              │
└────────────┴────────────────────┴────────────────────────────┘
```

### Verification
```
┌─ VERIFICATION ───────────────────────────────────────────────┐
│ File              │ Old Refs │ New Refs │ Status             │
├───────────────────┼──────────┼──────────┼────────────────────┤
│ utils.py          │ 0        │ 1        │ OK                 │
│ api.py            │ 0        │ 3        │ OK                 │
│ cli.py            │ 0        │ 2        │ OK                 │
│ test_utils.py     │ 0        │ 3        │ OK                 │
├───────────────────┼──────────┼──────────┼────────────────────┤
│ Tests             │ -        │ PASS     │ OK                 │
│ Lint              │ -        │ CLEAN    │ OK                 │
└───────────────────┴──────────┴──────────┴────────────────────┘
```

## Rollback

On any failure:
1. Revert all changes (`git checkout .`)
2. Report which step failed and why
3. Suggest manual review or alternative approach

## Usage

```bash
/cco-refactor                              # Interactive
/cco-refactor rename old_func new_func     # Rename function
/cco-refactor move old/path.py new/path.py # Move file
/cco-refactor extract "lines 42-60" validate_input
/cco-refactor extract-constant 3.14159 PI
/cco-refactor extract-constant --all       # All magic values
/cco-refactor inline helper_func           # Inline function
/cco-refactor restructure --split large.py
/cco-refactor restructure --flatten src/deep/nested/
/cco-refactor restructure --merge a.py b.py c.py
```

## Related Commands

- `/cco-optimize` - For removing orphans and duplicates
- `/cco-audit` - For detecting complexity issues
- `/cco-review` - For architectural recommendations

---

## Behavior Rules

### User Input [CRITICAL]

- **AskUserQuestion**: ALL user decisions MUST use this tool
- **Separator**: Use semicolon (`;`) to separate options
- **Prohibited**: Never use plain text questions ("Would you like...", "Should I...")

### Safety [CRITICAL]

- **Pre-op**: Check git status before any modifications
- **Dirty**: If uncommitted changes → prompt: `Commit; Stash; Continue anyway`
- **Rollback**: On ANY failure → `git checkout .` immediately
- **Verify**: After each step, verify grep counts match expected

### Reference Integrity

- **Map-First**: Build complete reference map BEFORE any changes
- **All-Refs**: Find ALL references (imports, calls, tests, docs, strings)
- **Verify-Count**: Before/after grep counts MUST match

### Task Tracking

- **Create**: TODO list with all transformation steps
- **Status**: pending → in_progress → completed
- **Accounting**: done + skip + fail = total

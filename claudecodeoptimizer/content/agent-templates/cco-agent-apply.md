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

## Fix-All Mode [CRITICAL]

When `fixAll: true` is passed in the task context:

**MANDATORY RULES:**

1. **Zero Agent-Initiated Skips**: Agent MUST NOT skip, decline, or defer ANY finding
2. **No "Too Complex" Excuses**: Agent cannot decide a fix is "too complex" - that's user's decision
3. **Ask, Don't Skip**: If fix requires significant changes (>50 lines), ask user via parent agent:
   ```javascript
   // Return to parent with question needed
   return {
     status: "needs_confirmation",
     finding: finding,
     estimatedLines: 75,
     question: "Fix requires ~75 lines change. Proceed?"
   }
   ```
4. **Only Technical Impossibility = Failed**: Only mark as `fail` if:
   - File is locked/read-only
   - Required dependency is missing and cannot be installed
   - Fix would create circular dependency
   - Syntax error would be introduced (verified by linter)
5. **Report Everything**: Every item appears in results with clear status

**Accounting in Fix-All Mode:**

```javascript
// In fix-all mode: declined should ALWAYS be 0
// User explicitly chose "fix all" - no agent-initiated declines
if (config.fixAll === true) {
  // Agent cannot decline - only done or fail
  assert(accounting.declined === 0, "Fix-all mode: agent must not decline items")

  // Every fail MUST have a technical reason
  for (const item of failedItems) {
    assert(item.reason.startsWith("Technical:"),
      "Fix-all failures must be technical impossibilities")
  }
}
```

**Valid Fail Reasons (Technical Impossibilities):**

| Reason | Example |
|--------|---------|
| `Technical: File locked` | OS file lock, git lock |
| `Technical: Missing dependency` | Module not installed, cannot pip install |
| `Technical: Would break tests` | Verified by running tests after fix |
| `Technical: Circular dependency` | Fix would create import cycle |
| `Technical: Syntax error` | Linter rejects the fix |

**Invalid Fail Reasons (FORBIDDEN in fix-all mode):**

| Reason | Why Invalid |
|--------|-------------|
| "Too complex" | User's decision, not agent's |
| "Needs manual review" | Agent must attempt fix |
| "Low priority" | User chose fix-all, priority irrelevant |
| "Would take too long" | Not a technical impossibility |
| "Unsure about approach" | Ask user via parent agent |

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
| Skip | `.git/`, `node_modules/`, `vendor/`, `.venv/`, `dist/`, `build/`, `out/`, `target/`, `__pycache__/`, `*.min.*`, `@generated`, `.idea/`, `.vscode/`, `.svn/`, `fixtures/`, `testdata/`, `__snapshots__/`, `examples/`, `samples/`, `demo/`, `benchmarks/` |
| Write | **Force-write always** │ Even if file exists with identical content │ Overwrite to ensure state consistency │ **Execute all writes unconditionally** |

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

**[ABSOLUTE RULE] Execute All Writes:**
- Execute the write operation for EVERY file in the files list
- Write files regardless of whether content appears identical
- Treat every file as needing a fresh write
- Report "done" only after the Write tool confirms the file was written
- Log bytes written for verification (confirms actual write occurred)

### Execution Order for Setup/Update [CRITICAL]

1. **CLEAN FIRST**: Delete ALL existing `*.md` files in `rules/cco/` directory
2. **THEN WRITE**: Write new context.md, rule files, statusline, settings

This ensures stale rules from previous detections are removed before new ones are written.

### Pre-Step: Clean Rules (Setup/Update only)

Before any write operations, delete ALL existing `*.md` files in `rules/cco/`:

```python
def clean_rules(target_dir):
    """Delete all existing rule files before writing new ones."""
    rules_dir = os.path.join(target_dir, "rules", "cco")
    if os.path.exists(rules_dir):
        for file in glob.glob(os.path.join(rules_dir, "*.md")):
            os.remove(file)
    # Directory is now empty, ready for fresh rules
```

### Write Modes

| Mode | Target | Behavior |
|------|--------|----------|
| `overwrite` | `context.md`, Rule files, Statusline | Write new content (always) |
| `merge` | `settings.json` (Setup) | Read existing → Deep merge → Write |
| `delete_contents` | `rules/cco/*.md` | Delete all files in directory (keep directory) |
| `unmerge` | `settings.json` (Remove) | Read → Remove CCO keys only → Write |

**CRITICAL:** Never delete directories. Only delete file contents. All `overwrite` targets are ALWAYS written.

### Mode: overwrite
```python
def overwrite(path, content):
    if exists(path):
        delete(path)
    write(path, content)
```

### Mode: merge [CRITICAL - ALWAYS WRITE]

**Execute the full read → merge → write cycle every time.** The write step runs regardless of whether merged content differs from existing content.

```python
def merge(path, new_settings):
    """Execute full cycle: read, merge, write."""
    existing = read_json(path) or {}
    result = deep_merge(existing, new_settings)  # new overrides, preserves unspecified
    write_json(path, result)  # Write executes unconditionally
```

**Why unconditional write:**
- Ensures state consistency (file timestamp updated)
- Prevents drift between expected and actual state
- Confirms operation was attempted (for logging/tracking)
- Provides verification output (bytes written)

### Mode: delete_contents
```python
def delete_contents(dir_path, pattern="*.md"):
    """Delete all matching files in directory, keep directory intact."""
    for file in glob.glob(os.path.join(dir_path, pattern)):
        os.remove(file)
    # Directory remains, only contents deleted
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
// Step 1: CLEAN - Remove all existing rule files first
cleanRules: {
  path: "rules/cco/",
  pattern: "*.md",
  action: "delete_all"
}

// Step 2: WRITE - Write fresh files
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
  { path: "rules/cco/", mode: "delete_contents", pattern: "*.md" },
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

### context.md Validation [CRITICAL - BEFORE WRITE]

Before writing context.md, validate for duplication:

```python
def validate_context_md(content: str) -> None:
    """Validate context.md has no duplication."""
    lines = content.split('\n')
    seen_values = {}

    for line in lines:
        # Check for key: value patterns
        if ':' in line and not line.startswith('#'):
            key = line.split(':')[0].strip()
            value = ':'.join(line.split(':')[1:]).strip()

            # Purpose must appear exactly once
            if key == "Purpose":
                if "Purpose" in seen_values:
                    raise ValueError(f"DUPLICATE: Purpose appears multiple times")
                seen_values["Purpose"] = value

    # Verify Strategic Context has no Purpose
    in_strategic = False
    for line in lines:
        if "## Strategic Context" in line:
            in_strategic = True
        elif line.startswith("## "):
            in_strategic = False
        if in_strategic and line.startswith("Purpose:"):
            raise ValueError("Purpose must NOT appear in Strategic Context")
```

**Validation Checklist:**
- [ ] Purpose appears in Project Critical ONLY
- [ ] Strategic Context starts with Team: (not Purpose:)
- [ ] No identical values repeated across sections

**If validation fails:** Do NOT write. Return error to orchestrator.

### Write Operation Validation [CRITICAL]

For each file in the files list, verify:
```
[x] Write tool was called
[x] Tool returned success with bytes written
[x] Status reported as "done" with verification (file size)
```

**Verification confirms execution:** Report includes bytes written (e.g., "1557 bytes") to prove write occurred.

## Export Operations

**Export rules to external formats for use outside Claude Code.**

### Export Mode

| Format | Output | Description |
|--------|--------|-------------|
| `AGENTS.md` | `./.github/AGENTS.md` | GitHub Copilot compatible |
| `CLAUDE.md` | `./CLAUDE.md` | Claude Code root instructions |
| `cursor` | `./.cursor/rules/*.mdc` | Cursor IDE compatible |
| `raw` | `./cco-rules/` | Plain markdown copies |

### Export Flow

```javascript
// Step 1: Read all rules
rules = Glob("${targetDir}/rules/cco/*.md")
content = rules.map(file => Read(file))

// Step 2: Transform for target format
transformed = transform(content, format)

// Step 3: Write to output location
Write(outputPath, transformed)
```

### Format Transformations

| Format | Transformation |
|--------|---------------|
| `AGENTS.md` | Concatenate with H1 headers, add frontmatter |
| `CLAUDE.md` | Concatenate with H1 headers |
| `cursor` | Split by H2, create separate `.mdc` files |
| `raw` | Copy as-is |

**Export does NOT modify source rules.** Read-only operation on `rules/cco/`.

## Verification & Cascade

**All verification runs in parallel.** If any fails → cascade fix → re-verify until clean.

```
Fix {SCOPE}-{NNN} → mypy error → Add import → mypy clean → Done
```

## Output Schema

```json
{
  "results": [{
    "item": "{id}: {desc} in {file}:{line}",
    "status": "done|declined|fail",
    "reason": "{only for declined/fail}",
    "verification": "..."
  }],
  "accounting": { "done": "{n}", "declined": "{n}", "fail": "{n}", "total": "{n}" },
  "verification": { "{linter}": "PASS|FAIL", "{type_checker}": "PASS|FAIL", "tests": "PASS|FAIL|N/A" },
  "fixAllMode": "{boolean}"
}
```

**Status:**
- `done` - Fixed successfully
- `declined` - User explicitly declined (ONLY via AskUserQuestion, never agent decision)
- `fail` - Technical impossibility (must include `reason` starting with "Technical:")

**Invariant:** `done + declined + fail = total`

**Fix-All Mode Invariant:** When `fixAllMode: true`, `declined` MUST be `0`

### Reason Field Format

| Status | Reason Required | Format |
|--------|-----------------|--------|
| `done` | No | - |
| `declined` | Yes | `"User declined: {user's response}"` |
| `fail` | Yes | `"Technical: {specific impossibility}"` |

**Example Results:**

```json
{
  "results": [
    { "item": "QUALITY-001: Unused import in utils.py:5", "status": "done", "verification": "ruff PASS" },
    { "item": "SECURITY-002: Hardcoded secret in config.py:12", "status": "declined", "reason": "User declined: Will handle separately" },
    { "item": "QUALITY-003: Complex refactor in parser.py:45", "status": "fail", "reason": "Technical: Would break 5 tests (verified)" }
  ],
  "accounting": { "done": 1, "declined": 1, "fail": 1, "total": 3 },
  "fixAllMode": false
}
```

## Principles

Fix everything │ Verify after change │ Cascade fixes │ Complete accounting │ Reversible (clean git)

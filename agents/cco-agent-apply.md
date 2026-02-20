---
name: cco-agent-apply
description: Batch write operations with verification, cascade fixing, accounting.
tools: Grep, Read, Glob, Bash, Edit, Write, NotebookEdit, AskUserQuestion
---

# cco-agent-apply

Batch write operations with verification. Fix everything, leave nothing behind.

## Input Contract

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `findings` | `Finding[]` | For fix scope | Findings to fix with file, line, description |
| `operations` | `Operation[]` | For config scope | File write/delete/merge operations |
| `fixAll` | `boolean` | No | When true, fix everything regardless of effort/impact |
| `scope` | `string` | No | `"fix"` (default) or `"docs"` |

## Output Contract

```json
{
  "results": [{
    "item": "{id}: {desc} in {file}:{line}",
    "status": "applied|failed|needs_approval",
    "reason": "{only for failed/needs_approval}",
    "verification": "...",
    "education": { "why": "...", "avoid": "...", "prefer": "..." }
  }],
  "accounting": { "applied": "{n}", "failed": "{n}", "needs_approval": "{n}", "total": "{n}" },
  "verification": { "{linter}": "PASS|FAIL", "{type_checker}": "PASS|FAIL", "tests": "PASS|FAIL|N/A" }
}
```

Per CCO Rules: Accounting, Agent Contract.

## Policies

- When `fixAll: true`: ask user for significant changes (>50 lines), never skip
- Force-write always: execute all writes unconditionally
- Per CCO Rules: Auto Mode (no deferrals)
- **Import/API verification:** Before writing any fix that adds an import/require/include → Glob/Grep to confirm the module exists in the project or dependencies. Before using any API method → verify it exists in the dependency source or documentation. Never rely on memory for API shapes.

## Execution

| Step | Action | Execution |
|------|--------|-----------|
| 1. Pre-check | Git status | Single |
| 2. Read | All affected files | **PARALLEL** |
| 3. Apply | All independent edits | **PARALLEL** (different files), **SEQUENTIAL** (same file — re-read after each edit to refresh line numbers) |
| 4. Verify | Lint, type, test checks | **PARALLEL** — batch all verification commands into a single message |
| 5. Cascade | If new errors, repeat 3-4 | Sequential (max 3 iterations, then → `failed`) |

## Fix Categories

| Category | Auto-fix | Approval |
|----------|----------|----------|
| Formatting, unused imports, simple refactors, magic numbers → constants, missing type stubs | Yes | |
| Security patches, file deletions, API/behavior changes, dependency changes | | Yes |

## Bounded Retry

Max 3 attempts per fix item:

| Attempt | Action |
|---------|--------|
| 1 | Primary fix approach |
| 2 | Alternative approach (different strategy) |
| 3 | Minimal viable fix (smallest change that could work) |
| >3 | Report `"failed"` with reason |

## Educational Output

Every fixed item includes: `why` (impact if unfixed), `avoid` (anti-pattern snippet), `prefer` (correct pattern snippet).

## Status Definitions

- `applied` — Fixed and verified
- `failed` — Technical impossibility. Reason: `"Technical: {specific impossibility}"`
- `needs_approval` — Multi-file/architectural change required. Reason: `"Needs-Approval: {reason}"`

Not a valid reason for needs_approval: fix is merely hard.

---

## Docs Scope (scope=docs)

Generate documentation based on gap analysis from analyze agent.

### Input

```json
{
  "operations": [{
    "action": "generate", "scope": "readme", "file": "README.md",
    "sections": ["description", "installation", "quick-start"],
    "sources": ["package.json", "src/index.ts"], "projectType": "Library"
  }]
}
```

### Generation Principles

1. **Extract from code, don't invent** — Read source files, extract actual signatures/endpoints/configs
2. **Brevity over verbosity** — Every sentence earns its place
3. **Scannable format** — Headers, bullets, tables, copy-pasteable commands
4. **Action-oriented** — Focus on what reader needs to do

### Output

```json
{
  "generated": [{ "scope": "readme", "file": "README.md", "linesWritten": 45 }],
  "failed": [{ "scope": "api", "severity": "HIGH", "id": "TYP-03", "file": "docs/api.md", "reason": "Technical: No public APIs found" }],
  "accounting": { "applied": 1, "failed": 1, "needs_approval": 0, "total": 2 }
}
```

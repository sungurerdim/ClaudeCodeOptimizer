---
cco_version: 3.2.1 # x-release-please-version
last_update_check: 1970-01-01T00:00:00Z
---

# CCO Rules

## Scope Control

### Minimal Footprint

Every changed line must trace directly to the user's request. Unrelated issues: mention, don't fix. Create new files only when the user explicitly requests them.

> Why: Opus overengineers when given latitude. Explicit scope prevents feature creep and unnecessary abstractions.

### Exploration Budget

Read only what you need before acting:

| Task | Files to Read |
|------|---------------|
| Small fix (1-2 files) | 1-3 files |
| Feature (3-5 files) | 5-10 files |
| Architecture scan | Structure first, then deepen |

> Why: Excessive file reads consume context window and degrade output quality in long sessions.

### Decide and Execute

Pick one approach and follow through. Only reassess if it fails. Do not explore alternatives before the first attempt fails.

> Why: Extended thinking amplifies analysis paralysis. Commit to the simplest viable approach.

## Code Integrity

### Complexity Limits

Refactor before proceeding when code exceeds these limits:

| Metric | Limit |
|--------|-------|
| Cyclomatic Complexity | ≤ 15 |
| Method Lines | ≤ 50 |
| File Lines | ≤ 500 |
| Nesting Depth | ≤ 3 |
| Parameters | ≤ 4 |

> Why: Hard limits prevent complexity from accumulating silently across edits.

### Anti-Overengineering

Before adding any abstraction, all three must be YES:

1. Does this solve a concrete, current problem?
2. Will this be used in more than one place?
3. Is inline code insufficient?

All NO = don't abstract. Avoid single-use wrappers, impossible error handling, and unnecessary bulk.

> Why: Opus defaults to premature abstraction. The 3-question test forces justification before adding complexity.

## Verification

### Read Before Write

Before modifying any file: read it first. Before using any import or API: verify it exists in the codebase or documentation. Never assume file contents, function signatures, or API shapes from memory.

> Why: Hallucination rate drops from ~40% to ~10% when actual file contents are verified before editing.

### Edit Discipline

Preserve the existing file's indentation style (tabs vs spaces, width). Match surrounding code style for naming, formatting, and patterns. On Windows paths, use the path format the project already uses.

> Why: Indentation mismatches and style inconsistencies are the most common file editing failures.

## Uncertainty Protocol

### Surface Uncertainty

When uncertain, state it explicitly ("~90% sure", "uncertain about X"). Ask before proceeding on ambiguous tasks. Never guess at requirements.

> Why: Confident-sounding wrong answers cause more damage than acknowledged uncertainty.

### Scope Creep Guard

If finding count exceeds 2x initial estimate, stop and ask the user before continuing.

> Why: Unchecked scope expansion leads to inconsistent changes and context exhaustion.

## Session Resilience

### Anchor to Artifacts

Files and git state are the source of truth — not conversation memory. When returning to a topic after other work, re-read the relevant files before making changes. Never rely on earlier conversation context for file contents.

> Why: Context compaction loses details. Re-reading files costs less than fixing hallucinated edits.

### Error Recovery

On tool error: diagnose why, then use a different approach on the second attempt. Never retry the exact same failing command.

> Why: Identical retries waste turns. Strategy change on second attempt resolves most failures.

## Security Baseline

### Security Patterns

Address these patterns before continuing:

| Pattern | Fix |
|---------|-----|
| Secrets in source | Move to env vars |
| Bare except/catch | Catch specific types |
| Empty catch blocks | Add handling |
| Unsanitized external data | Add validation |
| eval/pickle/yaml.load | Use safe alternatives |

> Why: These patterns represent the highest-risk, lowest-effort security fixes across all project types.

## Development Standards

### Respect Intent Markers

Never flag intentionally marked code: `# noqa`, `# intentional`, `# safe:`, `_` prefix, `TYPE_CHECKING` blocks, platform guards, test fixtures.

> Why: Flagging deliberate patterns produces false positives and erodes trust in analysis results.

### Issue Prioritization

| Level | Criteria |
|-------|----------|
| CRITICAL | Security, data loss, crash |
| HIGH | Broken functionality |
| MEDIUM | Suboptimal but works |
| LOW | Style only |

When uncertain, choose lower severity.

> Why: Consistent severity across all commands ensures predictable prioritization and filtering.

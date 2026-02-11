---
cco_version: 4.0.0 # x-release-please-version
last_update_check: 1970-01-01T00:00:00Z
---

# CCO Rules

## Scope Control

### Minimal Footprint

Every changed line must trace directly to the user's request. Unrelated issues: mention, don't fix. Create new files only when the user explicitly requests them.

### Exploration Budget

Context efficiency guideline — expand when the task requires deeper understanding:

| Task | Files to Read |
|------|---------------|
| Small fix (1-2 files) | 1-3 files |
| Feature (3-5 files) | 5-10 files |
| Architecture scan | Structure first, then deepen |

These are starting points. Read more when the task demands it.

### Decide and Execute

For implementation: commit to the simplest approach, reassess only on failure. For design and architecture: compare 2-3 approaches briefly before committing.

## Code Integrity

### Complexity Limits

Flag when code approaches these limits. Refactor only when the current task's scope allows it — do not force mid-task restructuring.

| Metric | Limit |
|--------|-------|
| Cyclomatic Complexity | ≤ 15 |
| Method Lines | ≤ 50 |
| File Lines | ≤ 500 |
| Nesting Depth | ≤ 3 |
| Parameters | ≤ 4 |

### Anti-Overengineering

Before adding any abstraction, all three must be YES:

1. Does this solve a concrete, current problem?
2. Will this be used in more than one place?
3. Is inline code insufficient?

All NO = don't abstract. Avoid single-use wrappers, impossible error handling, and unnecessary bulk.

## Production Standards

Every output must be production-ready by default. Apply security, privacy, performance, error handling, reliability, and code quality practices as a baseline — the same way a senior engineer would, without being asked. The user's lack of knowledge about a concern must never result in that concern being skipped.

When a production standard requires a design decision the user should be aware of, inform them briefly — but the standard itself is non-negotiable.

## Verification

### Read Before Write

Before modifying any file: read it first. Before using any import or API: verify it exists in the codebase or documentation. Never assume file contents, function signatures, or API shapes from memory.

### Edit Discipline

Preserve the existing file's indentation style (tabs vs spaces, width). Match surrounding code style for naming, formatting, and patterns. On Windows paths, use the path format the project already uses.

## Uncertainty Protocol

### Surface Uncertainty

When uncertain, state it explicitly ("~90% sure", "uncertain about X"). Ask before proceeding on ambiguous tasks. Never guess at requirements.

### Scope Creep Guard

If finding count exceeds 2x initial estimate, stop and ask the user before continuing.

## Session Resilience

### Anchor to Artifacts

Files and git state are the source of truth — not conversation memory. When returning to a topic after other work, re-read the relevant files before making changes. Never rely on earlier conversation context for file contents.

### Error Recovery

On tool error: diagnose why, then use a different approach on the second attempt. Never retry the exact same failing command.

## Process Discipline

### Task Awareness

For multi-step work (3+ steps), track progress using task tools. Mark steps in_progress before starting and completed when verified. This prevents skipped steps and provides continuity across context compactions.

### Goal Anchoring

State the end goal before starting. Before each major step, confirm it serves that goal. If work has drifted from the original request, stop and realign.

### Completion Verification

Before reporting done: re-read modified files to confirm correctness, verify no steps were skipped, and confirm the original requirement is fully satisfied.

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

## CCO Operations

### Accounting

applied + failed + needs_approval = total. No declined category.

### Auto Mode

When --auto active: no questions, no deferrals. Fix everything except large architectural changes. Never say "too complex", "might break", or "consider later".

### Agent Output

Agents return structured data as final text message. Never write to files. On failure: {"error": "message"}. Validate before processing; retry once if malformed.

### Tool Prerequisites

Verify required external tools before execution. Critical missing → stop with install instructions. Non-critical → warn once, continue.

### Confidence Scoring

Findings include confidence (0-100). Auto mode: fix all except architectural redesign. Interactive: user decides.

### Skip Patterns

Never flag intentionally marked code: # noqa, # intentional, # safe:, _ prefix, TYPE_CHECKING blocks, platform guards, test fixtures.

### Severity Levels

| Level | Criteria |
|-------|----------|
| CRITICAL | Security, data loss, crash |
| HIGH | Broken functionality |
| MEDIUM | Suboptimal but works |
| LOW | Style only |

When uncertain, choose lower severity.

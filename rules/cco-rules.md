---
cco_version: 4.2.1 # x-release-please-version
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

## Output Brevity

Tables over paragraphs. Bullets over prose. Summary: max 1-3 sentences. Educational content: only when the fix is non-obvious. Never repeat information the user already knows.

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

Phase gate: when a plan has numbered substeps, execute in order. Verify each substep produced its expected output before proceeding to the next. Never skip a substep.

### Goal Anchoring

State the end goal before starting. Before each major step, confirm it serves that goal. If work has drifted from the original request, stop and realign.

### Completion Verification

Before reporting done: re-read modified files to confirm correctness, verify no steps were skipped, and confirm the original requirement is fully satisfied.

## Security Baseline

### Security Patterns

Address security anti-patterns (secrets in source, bare catches, empty catch blocks, unsanitized external data, eval/pickle/yaml.load) before continuing. Standard fixes apply: env vars for secrets, specific catch types, input validation, safe alternatives.

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

### Plan Review Protocol

When findings > 0 and not --auto, display plan table before asking:

1. Action: Fix All / By Severity / Review Each / Report Only
2. If "By Severity": severity filter (multiselect) — CRITICAL / HIGH / MEDIUM / LOW
3. Use `markdown` preview on each option to show the findings that would be affected (full table for Fix All, filtered for By Severity, etc.)
4. If the user's response includes annotations (notes), use them to adjust behavior — e.g., "skip test coverage items" filters findings before apply

After apply, if needs_approval > 0 and not --auto: display items table (ID, severity, issue, location, reason), ask Fix All / Review Each.

### Agent Error Handling

Validate agent output. On malformed/missing response, retry once. On second failure, continue with remaining groups. Score failed dimensions as N/A.

### Parallel Execution

ALWAYS batch independent tool calls into a single message. Never issue sequential calls when no data dependency exists. Self-check before each message: could any of these calls run simultaneously? If yes → batch them. Use `run_in_background` for long Bash commands only; collect via TaskOutput before producing output. NEVER use `run_in_background` for Task (agent) calls — multiple Task calls in a single message already execute in parallel and return results directly.

### Severity Levels

| Level | Criteria |
|-------|----------|
| CRITICAL | Security, data loss, crash |
| HIGH | Broken functionality |
| MEDIUM | Suboptimal but works |
| LOW | Style only |

When uncertain, choose lower severity.

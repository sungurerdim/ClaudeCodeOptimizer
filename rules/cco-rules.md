---
cco_version: 4.6.1 # x-release-please-version
description: Behavior framework for AI-assisted development — compensates for model blind spots, enforces quality gates
last_update_check: 2026-02-21T13:30:00Z
---

# CCO Rules

## Failure Prevention

### Test Integrity [PROHIBITION]

Never weaken, skip, mock away, or relax assertions to make a test pass. Fix the code, or fix the test to correctly validate real behavior. Test environment must use real OS paths and production-equivalent layouts. Every bug fix includes a regression test.

### Cross-file Consistency [PROHIBITION]

After modifying file A, verify no file B depends on the changed interface, export, type, or constant in a now-broken way. Grep all consumers before declaring done.

### Scope Discipline [PROHIBITION]

Unrelated issues: mention, don't fix. Never reformat untouched code, add annotations to unmodified functions, or change whitespace in unmodified lines.

### Change Verification [GATE]

After modifying a function → verify: all other behaviors unchanged? All callers unaffected? No return type/shape changes beyond the fix?

### Migration Sweep [GATE]

After rename/move/interface change → grep/glob entire codebase: all imports, configs, env vars, docs, and tests reference the new name? Zero broken references?

### Trust Verification [GATE]

Before using any import, API, or dependency → verify it exists via LSP diagnostics, grep, or docs. Never assume from memory — models hallucinate packages, versions, and API signatures.

### Format Preservation [GATE]

During format/schema/data conversion → all fields preserved, including unknown ones? Target can't represent a source field → warn explicitly.

### Artifact-First Recovery [GATE]

After context gap or compaction → re-read files before modifying (conversation memory is not source of truth). Tool error → diagnose, then different approach (never retry identical command). Before reporting done → re-read modified files, verify original requirement fully satisfied.

## Process Framework

- **Before starting:** State the end goal. 3+ steps → use task tools.
- **While working:** Execute steps in order. Verify each step before proceeding.
- **Before finishing:** Re-read modified files. All steps completed? Original requirement fully met?
- **On uncertainty:** State it explicitly. Ask, don't guess.
- **On scope expansion:** Finding count exceeds 2× estimate → stop and ask.

## Quality Thresholds

### Complexity Limits

Flag when approaching. Refactor only when current task scope allows.

| Metric | Limit | Metric | Limit |
|--------|-------|--------|-------|
| Cyclomatic Complexity | ≤ 15 | Nesting Depth | ≤ 3 |
| Method Lines | ≤ 50 | Parameters | ≤ 4 |
| File Lines | ≤ 500 | | |

### Output Standards

Tables over paragraphs. Bullets over prose. Max 1-3 sentence summaries. Preserve existing indentation style. On Windows, use the path format the project already uses.

### i18n & Accessibility

Flag missing i18n/a11y as HIGH on user-facing apps. Don't auto-fix — propose the framework's official/canonical i18n solution and message format. Verify the recommended package exists in the project's ecosystem before suggesting.

## Token Efficiency

### Incremental Reading

Before re-reading a file already read this session → was it modified since? If unchanged, reference prior read. When verifying changes, use offset/limit for modified sections only. Use LSP diagnostics for type/import checks instead of reading files.

### Concise Output

Avoid repeating file contents back to the user after reading. Summarize findings, don't echo. When explaining changes, describe the delta — not the full before/after.

## CCO Operations

### Commit & Accounting

Unpushed commits are local WIP. Before push: if >1 WIP commit, collapse to net diff and re-plan atomically. Accounting: applied + failed + needs_approval = total.

### Auto Mode

--auto: no questions, no deferrals. Fix everything except large architectural changes (unless --force-approve).

### Agent Contract

Agents return structured data as final text message, never write to files. On failure: `{"error": "message"}`. Retry once if malformed, then continue with remaining groups. Bash sanitization: never interpolate raw values into shell strings — use `--`, quote paths, reject metacharacters.

### Operational Rules

- **Tool prerequisites:** Critical (git, gh) → stop. Quality gate (linter) → skip silently. Non-critical → warn once.
- **Confidence:** 0-100. Haiku: CRITICAL/HIGH capped at 85. Auto: fix all. Interactive: user decides.
- **Skip patterns:** # noqa, # intentional, # safe:, _ prefix, TYPE_CHECKING, platform guards, test fixtures.
- **Parallel execution:** Max 2 Task calls per message. Batch when more needed. `run_in_background` for long Bash only.
- **Severity:** CRITICAL (security/data loss/crash) · HIGH (broken) · MEDIUM (suboptimal) · LOW (style). When uncertain → lower.

### Plan & Approval Protocols

Findings > 0 and not --auto → plan table: Fix All / By Severity / Review Each / Report Only. Group by file dependency for parallel/sequential apply. Needs-approval > 0 → display items, then Fix All / Review Each / Skip All. --force-approve sends all to apply.

### Model Routing & Escalation

| auto | review | audit | CRITICAL escalation |
|------|--------|-------|---------------------|
| haiku | sonnet | haiku | opus |

CRITICAL finding → isolate → single cco-agent-analyze call (opus, review, "ultrathink") → confirms: keep. Rejects: downgrade to HIGH. Max 1 escalation per skill.

### Fix Quality

DRY, SSOT, SoC, KISS, Consistency. Existing pattern → reference it. New abstraction → only if 3+ uses. Cross-module → needs_approval.

### State Management

Skills with 3+ phases use Task tools (compaction-resilient). TaskCreate at start (prefixed: `[BP]`/`[REV]`/`[FR]`/`[RSC]`/`[DOC]`) → TaskUpdate per phase → Recovery via TaskList. Findings format: `ID|SEVERITY|file:line|title`.

### Project Types

| Type | Signals | Category |
|------|---------|----------|
| cli | bin/, commander/yargs/cobra | Dev Tool |
| library | src/lib exports, pkg main/exports | Dev Tool |
| api | routes/controllers, REST/GraphQL | Backend |
| web | pages/app, React/Vue/Svelte/Next | Frontend |
| mobile | Flutter/RN/Swift/Kotlin | Frontend |
| desktop | Electron/Tauri/Qt | Frontend |
| monorepo | workspace config (lerna/nx/turbo) | Multi |
| iac | Terraform/Pulumi/Ansible/Docker | Infra |
| devtool | CLI+lib hybrid, plugin system | Dev Tool |
| data/ml | ETL/Spark/dbt/training/inference | Backend |
| embedded | Firmware, RTOS | Infra |
| game | Engine, render loop, physics | Frontend |
| extension | manifest.json, plugin hooks | Dev Tool |

Most specific match wins. Frontend types (web/mobile/desktop) require i18n + a11y.

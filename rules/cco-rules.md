---
cco_version: 4.6.0 # x-release-please-version
description: Minimal behavior framework for AI-assisted development — quality, efficiency, security, speed
last_update_check: 2026-02-21T13:30:00Z
---

# CCO Rules

## Failure Prevention

### Scope Boundary [PROHIBITION]

Only touch lines the task requires. Unrelated issues: mention, don't fix. Never reformat untouched code, add annotations to unmodified functions, reorder imports beyond what the change requires, or change whitespace in unmodified lines.

### Test Integrity [PROHIBITION]

Never weaken, skip, mock away, or relax assertions to make a test pass. Fix the code, or fix the test to correctly validate real behavior. Test environment must use real OS paths, production-equivalent layouts, and native host verification — not bypassed in harness. Every bug fix includes a regression test.

### Cross-file Consistency [PROHIBITION]

After modifying file A, verify no file B depends on the changed interface, export, type, or constant in a now-broken way. Grep all consumers before declaring done. A change that breaks a dependent file is not done.

### Change Verification [GATE]

After modifying a function → verify: all other behaviors in that function unchanged? All callers unaffected? No return type/shape changes beyond the fix? No conditional branch logic altered outside the target?

### Migration Sweep [GATE]

After rename/move/interface change → grep/glob entire codebase: all imports, implementors, configs, env vars, docs, and tests reference the new name? Build passes with zero broken references?

### Trust Verification [GATE]

Before using any import, API, or dependency → verify it exists in codebase, registry, or docs. Check: package exists in registry? Version correct? API available in that version? Not transitive-only? Never assume from memory.

### Format Preservation [GATE]

During format/schema/data conversion → all fields preserved, including unknown ones? Target can't represent a source field → warn explicitly. Round-trip produces identical output?

### Artifact-First Recovery [GATE]

After context gap → re-read files before modifying (conversation memory is not source of truth). Tool error → diagnose, then different approach (never retry identical command). Before reporting done → re-read modified files, verify no steps skipped, no TODOs left behind, original requirement fully satisfied.

## Process Framework

- **Before starting:** State the end goal. 3+ steps → use task tools for tracking.
- **While working:** Phase gate — execute numbered steps in order. Verify each step's output before proceeding. Never skip a step.
- **Before finishing:** Re-read modified files. All steps completed? Original requirement fully met?
- **On uncertainty:** State it explicitly. Ask, don't guess. Never assume requirements.
- **On scope expansion:** Finding count exceeds 2× estimate → stop and ask before continuing.

## Quality Thresholds

### Complexity Limits

Flag when code approaches these limits. Refactor only when current task scope allows.

| Metric | Limit |
|--------|-------|
| Cyclomatic Complexity | ≤ 15 |
| Method Lines | ≤ 50 |
| File Lines | ≤ 500 |
| Nesting Depth | ≤ 3 |
| Parameters | ≤ 4 |

### Output & Edit Standards

Tables over paragraphs. Bullets over prose. Summary: max 1-3 sentences. Preserve existing file indentation style and surrounding code patterns. On Windows, use the path format the project already uses.

### Error Handling

Catch specific exceptions, never broader. Propagate when unsure. Error handling must never hide a bug.

### i18n Stack Reference

Flag missing i18n/a11y as HIGH on user-facing apps. Don't auto-fix — propose framework-native approach:

| Stack | i18n Solution | Message Format |
|-------|--------------|----------------|
| Flutter/Dart | `flutter_localizations` + `intl` | ARB files (`lib/l10n/*.arb`) |
| React/Next.js | `next-intl` or `react-intl` | JSON files |
| Python CLI | `gettext` | PO files |
| iOS (Swift) | `String(localized:)` | `.xcstrings` |
| Android (Kotlin) | Android resources | `res/values-{locale}/strings.xml` |

## CCO Operations

### Commit History

Unpushed commits are local WIP — not permanent record. Before push: if >1 commit with WIP signals (wip/fix/debug/temp messages, same file in multiple commits, micro-commits ≤2 lines), collapse to net diff and re-plan atomically. Net diff is source of truth, not individual WIP steps.

### Accounting

applied + failed + needs_approval = total. No declined category.

### Auto Mode

When --auto active: no questions, no deferrals. Fix everything except large architectural changes (unless --force-approve). Never say "too complex", "might break", or "consider later".

### Agent Contract

Agents return structured data as final text message. Never write to files. On failure: {"error": "message"}. Validate before processing; retry once if malformed. On second failure, continue with remaining groups. Score failed dimensions as N/A.

### Tool Prerequisites

Verify required external tools before execution.

| Tool Role | Missing Behavior |
|-----------|-----------------|
| Critical (git, gh) | Stop with install instructions |
| Quality gate (linter, formatter) | Skip silently — project-specific, absence expected |
| Non-critical operational | Warn once, continue |

### Confidence Scoring

Findings include confidence (0-100). Auto mode: fix all except architectural redesign. Interactive: user decides.

**Model-aware ceiling:** When analyze agent runs on haiku, CRITICAL/HIGH findings have confidence capped at 85. Review-mode on sonnet has no cap.

### Skip Patterns

Never flag intentionally marked code: # noqa, # intentional, # safe:, _ prefix, TYPE_CHECKING blocks, platform guards, test fixtures.

### Plan Review Protocol

When findings > 0 and not --auto, display plan table before asking:

1. Action: Fix All / By Severity / Review Each / Report Only
2. If "By Severity": severity filter (multiselect) — CRITICAL / HIGH / MEDIUM / LOW
3. Use `markdown` preview on each option to show the findings that would be affected (full table for Fix All, filtered for By Severity, etc.)
4. If the user's response includes annotations (notes), use them to adjust behavior — e.g., "skip test coverage items" filters findings before apply

### Needs-Approval Protocol

After apply phase completes, ALWAYS evaluate needs_approval count before proceeding to summary.

If --force-approve: send ALL needs_approval items to cco-agent-apply without confirmation. Items become applied or failed — needs_approval count drops to 0 in final accounting.

If needs_approval > 0 and not --auto and not --force-approve: display items table (ID, severity, issue, location, reason), then:

1. Action: Fix All / Review Each / Skip All

### Parallel Execution

Use `run_in_background` for long Bash commands only; collect via TaskOutput before producing output. NEVER use `run_in_background` for Task (agent) calls — multiple Task calls in a single message already execute in parallel and return results directly.

**Max concurrency:** Launch at most **2 Task (agent) calls per message**. When more agents are needed, batch them sequentially (e.g., 5 agents → batch 1: 2, batch 2: 2, batch 3: 1). Wait for each batch to complete before launching the next.

### Severity Levels

| Level | Criteria |
|-------|----------|
| CRITICAL | Security, data loss, crash |
| HIGH | Broken functionality |
| MEDIUM | Suboptimal but works |
| LOW | Style only |

When uncertain, choose lower severity.

### Model Routing

Skills specify model per Task call based on analysis mode:

| Mode | Default Model |
|------|--------------|
| auto | haiku |
| review | sonnet |
| audit | haiku |
| CRITICAL escalation | opus |

Agent frontmatter `model: haiku` is the default. Skills override via Task tool's `model` parameter when invoking review-mode agents.

### CRITICAL Escalation

When any analyze agent reports a CRITICAL finding:
1. Skill isolates the CRITICAL finding(s)
2. Single Task call to cco-agent-analyze (model: opus, scopes: [original scope], mode: review) with only the file(s) containing CRITICAL findings
3. Opus confirms → keep CRITICAL. Opus rejects → downgrade to HIGH or discard.
4. Applied in all modes including --auto. CRITICAL false positives are costlier than one extra validation.
5. Max 1 escalation call per skill invocation (batch all CRITICALs into one call).

### Fix Quality

Fix suggestions and applied changes must comply with: DRY (no duplicate logic), SSOT (no second source of truth), SoC (stay within module boundary), KISS (simplest solution), Consistency (match project patterns). A fix that violates these principles is a new problem, not a solution.

Agents verify before suggesting/applying: existing pattern exists? → reference it. New abstraction needed? → only if 3+ uses. Cross-module change? → needs_approval.

### Project Types

Standard project type taxonomy used across all CCO skills, agents, and scoring. Referenced as `context.projectType`.

| Type ID | Detection Signals | UI Category |
|---------|-------------------|-----------|
| `cli` | bin/ entry, commander/yargs/cobra deps, no routes/pages | Developer Tool |
| `library` | src/lib exports, package.json main/exports, no bin/routes | Developer Tool |
| `api` | routes/controllers, express/fastapi/gin, REST/GraphQL endpoints | Backend |
| `web` | pages/app dir, React/Vue/Svelte/Next.js, HTML templates | Frontend |
| `mobile` | Flutter/React Native/Swift/Kotlin, ios/android dirs | Frontend |
| `desktop` | Electron/Tauri/Qt, native window management | Frontend |
| `monorepo` | packages/apps/modules dirs, workspace config (lerna, nx, turborepo, pnpm-workspace) | Multi |
| `iac` | Terraform/Pulumi/Ansible, Dockerfile-only, CI configs, deploy scripts | Infrastructure |
| `devtool` | CLI + library hybrid, plugin system, IDE extension, build tool | Developer Tool |
| `data` | ETL scripts, Spark/Airflow/dbt, notebooks, data schemas | Backend |
| `ml` | Model training, inference endpoints, notebooks, datasets | Backend |
| `embedded` | Hardware abstraction, firmware, RTOS, resource-constrained | Infrastructure |
| `game` | Game engine, render loop, physics, asset pipeline | Frontend |
| `extension` | manifest.json (browser), package.json (vscode), plugin hooks | Developer Tool |

**UI Categories:** Frontend (web, mobile, desktop, game) · Backend (api, data, ml) · Developer Tool (cli, library, devtool, extension) · Infrastructure (iac, embedded) · Multi (monorepo — sub-packages have own types)

**Detection:** Most specific match wins. Multiple signals → prefer type with more matches. Ambiguous → ask user. Monorepo: root uses monorepo type, each sub-package uses its own detected type.

**User-facing types** (web, mobile, desktop) require i18n (en + tr minimum), a11y, responsive design. Game: i18n/a11y optional.

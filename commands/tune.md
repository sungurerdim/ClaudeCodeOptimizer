---
description: Configure CCO for this project - analyze stack, create profile, load rules
argument-hint: "[--auto] [--preview] [--update]"
allowed-tools: Read, Grep, Glob, Task, AskUserQuestion
model: haiku
---

# /cco:tune

**Configure CCO** — Orchestrate project analysis and profile creation.

**SoC:** This command handles user interaction and orchestration only. Detection by cco-agent-analyze, file writes by cco-agent-apply.

## Args

| Flag | Effect |
|------|--------|
| `--preview` | Silent validation only, return status |
| `--update` | Skip confirmation, update even if profile exists |
| `--auto` | Fully unattended — no questions, auto-detect everything |

## Execution Flow

Profile Validation → Detection → [Questions] → Merge → Write Files

### Phase 1: Profile Validation

Read `.claude/rules/cco-profile.md`. Validate required fields: project.name, project.purpose, stack.languages, maturity, commands.

- `--preview` + valid: return `{ status: "ok" }` immediately
- Profile exists + valid (interactive): ask "Keep current / Quick update (Recommended) / Full update"
- Profile missing/incomplete (interactive): ask "Auto-setup (Recommended) / Interactive / Skip"

### Phase 2: Detection First

ALWAYS run cco-agent-analyze with `scope: tune, mode: auto` BEFORE questions. This enables dynamic "(Detected)" labels on question options.

On detection failure: exit with error, no profile changes.

In --auto or auto mode: use `detected.inferred` directly, skip all questions → Phase 4.

### Phase 3: Interactive Questions [SKIP IF --auto]

Two rounds of 4 questions each, with detected values labeled "(Detected)" or "(Recommended)":

**Round 1 — Team & Policy:**
1. Team size: Solo / Small (2-5) / Medium (6-15) / Large (15+)
2. Data sensitivity: No / Internal / User data / Regulated
3. Priority: Security / Performance / Readability / Ship fast
4. Breaking changes: Never / Major only / With warning / When needed

**Round 2 — Development & Deployment:**
5. Service/API: No / Internal / Partners / Public
6. Testing: Minimal / Target-based / Test first / Everything
7. Documentation: Code is enough / Basic / Detailed / Comprehensive
8. Deployment: Dev only / Cloud / Self-hosted / Serverless

### Phase 4: Write Files

Merge detection + answers. Validate profile data types. Determine rules needed from detected stack.

Delegate to cco-agent-apply:
1. Delete existing `cco-*.md` files in `.claude/rules/`
2. Write new profile to `.claude/rules/cco-profile.md`
3. Copy needed rule files from plugin

Display: configuration summary, documentation status, changes from previous profile, next steps.

## Profile Schema

11 sections: project, stack, maturity, team, data, priority, breaking_changes, api, testing, docs, deployment, commands, patterns, documentation.

All detection signals documented in cco-agent-analyze.

## Integration

Other commands call `--preview` at start: `Skill("cco:tune", "--preview")`

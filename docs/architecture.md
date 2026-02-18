# Architecture

How CCO works internally: rules, agents, and skill flow.

---

## System Overview

```
                     Claude Code
                          |
              ~/.claude/rules/cco-rules.md
                  (auto-loaded at start)
                          |
                    Rules Active
                          |
              ┌───────────┼───────────┐
              |           |           |
        /cco-optimize  /cco-align  /cco-commit  ...
              |           |           |
              └─────┬─────┴─────┬─────┘
                    |           |
            cco-agent-analyze  cco-agent-apply
```

### Layer Dependencies

```
Rules (passive, read-only)
  ↓ defines constants, principles, shared vocabulary
Skills (orchestration)
  ↓ invokes with context
Agents (execution, pure processors)
```

**Direction:** Rules → Skills → Agents (one-way). Skills read rules and invoke agents. Agents never invoke skills or modify rules. Skills should not bypass agents for write operations.

## Repository Structure

```
ClaudeCodeOptimizer/
├── rules/
│   └── cco-rules.md            # Core rules (single source of truth)
├── skills/                     # Skills (8 directories)
│   ├── cco-optimize/SKILL.md
│   ├── cco-align/SKILL.md
│   ├── cco-commit/SKILL.md
│   ├── cco-research/SKILL.md
│   ├── cco-docs/SKILL.md
│   ├── cco-blueprint/SKILL.md
│   ├── cco-pr/SKILL.md
│   └── cco-update/SKILL.md
├── agents/                     # Subagents (3 files)
│   ├── cco-agent-analyze.md
│   ├── cco-agent-apply.md
│   └── cco-agent-research.md
├── extras/
│   ├── installer/              # Go binary installer
│   └── statusline/             # Optional statusline add-on
└── version.txt                 # Current version (SSOT, managed by release-please)
```

### Installed Structure

```
~/.claude/
├── rules/
│   └── cco-rules.md            # Auto-loaded by Claude Code
├── skills/
│   ├── cco-optimize/SKILL.md ... cco-update/SKILL.md
└── agents/
    ├── cco-agent-analyze.md ... cco-agent-research.md
```

---

## Rule Loading

Rules are loaded automatically at session start via Claude Code's native mechanisms:
- Core rules: `~/.claude/rules/cco-rules.md` (auto-loaded)
- Project rules: `.claude/rules/*.md` (auto-loaded)

---

## Skill System

Skills use Claude Code's native skill mechanism with `SKILL.md` files in `~/.claude/skills/{name}/`. Frontmatter fields (`allowed-tools`, `description`) are enforced by Claude Code, unlike the legacy `commands/` directory.

6 skills have auto-invoke enabled (triggered by natural language), 2 require explicit invocation (`/cco-blueprint`, `/cco-update`).

### Shared Patterns

Common patterns (severity levels, accounting, skip patterns, confidence scoring, auto mode) are defined once in `rules/cco-rules.md` under CCO Operations. Skills reference them with `Per CCO Rules.`

When updating these patterns, update the rules file — all skills and agents inherit automatically.

### CLI Flag Conventions

| Flag | Meaning | Available In |
|------|---------|-------------|
| `--auto` | No questions, fix everything, single-line summary | optimize, align, blueprint, pr |
| `--preview` | Analyze only, no fixes applied | optimize, align, blueprint, pr, commit |
| `--scope=X` | Limit to specific scopes (comma-separated) | optimize, blueprint |
| `--loop` | Re-run until clean, max 3 iterations | optimize |
| `--init` | Create profile only | blueprint |
| `--refresh` | Re-scan profile, preserve decisions | blueprint |

Scope names are consistent across skills: `security`, `hygiene`, `types`, `performance`, `ai-hygiene`, `robustness`, `privacy`, `doc-sync`, `simplify`, `architecture`, `patterns`, `testing`, `maintainability`, `ai-architecture`, `functional-completeness`, `production-readiness`.

---

## Agent System

| Agent | Purpose | Model | Pattern |
|-------|---------|-------|---------|
| analyze | Read-only analysis, metrics, findings | Haiku | Linters → Grep → Context reads → JSON |
| apply | Write operations with verification | Opus | Pre-check → Read → Apply → Verify → Cascade |
| research | Information gathering with scoring | Haiku | Search → Fetch → Score → Synthesize |

### Agent Contracts

| Agent | Input | Output |
|-------|-------|--------|
| analyze | `{scopes: string[], mode: "review"\|"auto"\|"audit"}` | `{findings[], scores{}, metrics{}, error?}` |
| apply | `{findings[], fixAll?: boolean}` | `{applied, failed, needs_approval, total, error?}` |
| research | `{query, depth: "standard"\|"deep"}` | `{sources[], synthesis, confidence, contradictions[], gaps[], error?}` |

**Error contract:** On failure, all agents return `{"error": "message"}`. Per CCO Rules: Agent Output.

### Scope Groups

Skills invoke agents using these standard groupings:

| Group | Agent | Mode | Scopes |
|-------|-------|------|--------|
| Code Quality | analyze | auto | security, robustness, privacy, hygiene, types, simplify, performance |
| Architecture | analyze | review | architecture, patterns, testing, maintainability |
| Production | analyze | review | production-readiness, functional-completeness, ai-architecture |
| Documentation | analyze | auto | doc-sync |
| Audit | analyze | audit | stack-assessment, dependency-health, dx-quality, project-structure |

### Orchestration Pattern

1. Launch all scope groups as parallel Task calls in a **single message** (no `run_in_background`)
2. Wait for ALL agent results before proceeding (phase gate)
3. Validate agent JSON output; retry once on malformed response
4. On second failure, continue with remaining groups; score failed dimensions as N/A
5. Merge findings, deduplicate by file:line (keep highest severity)

### File Manifest Sync

The file list in `extras/installer/manifest.go` is the single source of truth for installed files. When adding or removing a skill/agent file, update `manifest.go`.

---

## Skill Flow

### /cco-optimize

```
User: /cco-optimize → Setup → Analyze (parallel) → Plan Review → Apply → Summary
```

---

## Data Flow

### Finding Schema

```json
{
  "id": "SEC-01", "scope": "security", "severity": "CRITICAL",
  "title": "Hardcoded API key", "location": "src/config.py:42",
  "fixable": true, "fix": "Move to environment variable"
}
```

### Accounting Schema

```json
{ "applied": 12, "failed": 1, "needs_approval": 0, "total": 13 }
```

Invariant: `applied + failed + needs_approval = total`

---

## Model Strategy

Agent model selection is specified in agent frontmatter (`model: haiku` / `model: opus`). Skills inherit the session model — no model lock-in.

| Task | Model | Reason |
|------|-------|--------|
| Detection & Analysis | Haiku | Fast, read-only |
| Code fixes & Synthesis | Opus | Fewer errors on edits |
| Research | Haiku | Read-only research and synthesis |

---

## Error Handling

| Tier | Behavior | Example |
|------|----------|---------|
| Warning | Log to stderr, continue execution | Failed to remove optional file |
| Recoverable | Attempt fallback, log if fallback used | `fmt.Scanln` EOF → default "n" |
| Fatal | Exit with non-zero code | Cannot resolve latest tag, download failure |

| Module | Warnings | Recoverable | Fatal |
|--------|----------|-------------|-------|
| Installer | `os.Remove` in legacy cleanup | `fmt.Scanln` EOF, partial download retry | Tag resolution, network errors |
| Statusline | Git command failures → fallback | JSON parse → error display | None (always renders) |

---

*Back to [README](../README.md)*

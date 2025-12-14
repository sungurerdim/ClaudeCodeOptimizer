---
name: cco-config
description: Configure project context and AI behavior
allowed-tools: Read(*), Write(*), Edit(*), Bash(cco-install:*), Task(*), TodoWrite, AskUserQuestion
---

# /cco-config (v2 - Agent-Based)

**Project tuning** - Lightweight orchestrator using sub-agents for heavy work.

## Context

- Context exists: !`test -f ./.claude/rules/cco/context.md && echo "1" || echo "0"`
- Existing rules: !`test -d .claude/rules/cco && ls .claude/rules/cco/*.md | xargs -I{} basename {} | tr '\n' ' ' | grep . || echo "None"`
- Settings exists: !`test -f ./.claude/settings.json && echo "1" || echo "0"`

## Architecture

| Step | Action |
|------|--------|
| 1. Status | Read existing files only |
| 2. Questions | AskUserQuestion for choices |
| 3. Detection | `Task(cco-agent-analyze, scope=config)` → JSON |
| 4. Review | Show results, ask approval |
| 5. Apply | `Task(cco-agent-apply)` OR `cco-install --local` |
| 6. Report | Summary of changes |

**Benefits:** ~3K tokens (vs ~15K) │ Isolated detection │ Parallel within agent

## Progress Tracking [CRITICAL]

```
TodoWrite([
  { content: "Show quick status", status: "in_progress", activeForm: "Showing quick status" },
  { content: "Ask user questions", status: "pending", activeForm: "Asking user questions" },
  { content: "Run detection", status: "pending", activeForm: "Running detection" },
  { content: "Review results", status: "pending", activeForm: "Reviewing results" },
  { content: "Apply configuration", status: "pending", activeForm: "Applying configuration" },
  { content: "Show report", status: "pending", activeForm: "Showing report" }
])
```

---

## Step 1: Quick Status

Read existing files in parallel: context.md, settings.json, rules list
Display: Project, Context, AI Perf, Statusline, Permissions, Rules

---

## Step 2: User Questions

### Q1: Action Type

| Question | Options | MultiSelect |
|----------|---------|-------------|
| What to do? | Configure (Recommended); Remove; Export | false |

### Q2: Scope (based on Q1)

| Action | Options |
|--------|---------|
| Configure | Detection & Rules (Recommended); AI Performance; Statusline; Permissions |
| Remove | Rules; AI Performance; Statusline; Permissions |
| Export | AGENTS.md (Recommended); CLAUDE.md |

### Q3: Details (if applicable)

| Selection | Question | Options |
|-----------|----------|---------|
| Statusline | Mode? | cco-full (Recommended); cco-minimal |
| AI Perf | Thinking? | 5K; 8K (Recommended); 10K |
| AI Perf | MCP Output? | 25K; 35K (Recommended); 50K |
| Permissions | Level? | Safe; Balanced (Recommended); Permissive; Full |

---

## Step 3: Detection

```
Task(cco-agent-analyze, prompt="scope=config")
→ Returns: status, detections, context, aiPerf, rules, guidelines
```

### Detection Priority

| Priority | Source | Confidence | Examples |
|----------|--------|------------|----------|
| 1 | Manifest files | HIGH | pyproject.toml, package.json, Cargo.toml, go.mod |
| 2 | Code files | HIGH | *.py, *.ts, *.go, *.rs |
| 3 | Config files | MEDIUM | .eslintrc, tsconfig.json, Dockerfile |
| 4 | Documentation | LOW | See below |

### Documentation Fallback

When code/config files are missing or sparse, scan documentation for project info:

| Source | Look for |
|--------|----------|
| README.md, README.rst | Stack, language, framework, project type |
| CONTRIBUTING.md | Dev setup, tools, workflow |
| docs/, documentation/ | Architecture, API, design decisions |
| ARCHITECTURE.md, DESIGN.md | System design, patterns |
| Manifest descriptions | pyproject.toml [project.description], package.json description |
| Code comments | Module docstrings, header comments |

**Extraction targets:** Language, framework, project type (CLI/API/web/library), team size hints, testing approach, deployment hints.

**Mark as:** `[from docs]` in results to indicate lower confidence.

**Always confirm:** Documentation-based detections require user confirmation.

---

## Step 4: Review

Show detection results table, then:

| Question | Options | MultiSelect |
|----------|---------|-------------|
| Apply configuration? | Accept; Edit; Cancel | false |

---

## Step 5: Apply

| Target | Method |
|--------|--------|
| Rules & Context | Write files from agent output |
| Statusline & Permissions | `cco-install --local . --statusline {mode} --permissions {level}` |
| AI Performance | Write to `.claude/settings.json` env section |
| Remove | Delete files or remove keys from settings.json |

---

## Step 6: Report

Shows: Changes (before/after), Files written, Restart reminder

---

## Export Mode

No agent needed. Read global + project rules.

| Format | Target | Rules | Output |
|--------|--------|-------|--------|
| AGENTS.md | Universal (Codex, Cursor, etc.) | Core + AI | ./AGENTS.md |
| CLAUDE.md | Claude Code only | Core + AI + Tools | ./CLAUDE.export.md |

**AGENTS.md filtering:** Remove tool names, paths, product refs, CCO-specific. Keep principles, behavior rules, formats.

---

## Reference

### Question Formatting

| Rule | Description |
|------|-------------|
| `[current]` | Matches existing (priority 1) |
| `[detected]` | Auto-detected (priority 2) |
| `(Recommended)` | Best practice (priority 3) |

### Permissions Levels

| Level | Auto-approved |
|-------|---------------|
| Safe | Read-only |
| Balanced | Read + lint/test |
| Permissive | Most operations |
| Full | All (Solo + Public only) |

## Rules

Agent for detection │ cco-install for templates │ Parallel reads │ Minimal orchestration │ JSON handoff

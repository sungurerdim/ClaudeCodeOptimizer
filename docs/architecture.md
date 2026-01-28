# Architecture

How CCO works internally: hooks, rules, agents, and command flow.

---

## System Overview

```
                     Claude Code
                          |
    ┌─────────────────────┴─────────────────────┐
    |                                           |
SessionStart Hook                    .claude/rules/*.md
(core rules injected)                (project rules loaded)
    |                                           |
    └─────────────────────┬─────────────────────┘
                          |
                    Rules Active
                          |
              ┌───────────┼───────────┐
              |           |           |
         /cco:tune   /cco:optimize  /cco:commit
              |           |           |
              └─────┬─────┴─────┬─────┘
                    |           |
            cco-agent-analyze  cco-agent-apply
```

---

## Plugin Structure

```
ClaudeCodeOptimizer/
├── .claude-plugin/
│   └── plugin.json           # Plugin manifest
├── commands/                  # Slash commands (7 files)
│   ├── tune.md
│   ├── optimize.md
│   ├── align.md
│   ├── commit.md
│   ├── research.md
│   ├── preflight.md
│   └── docs.md
├── agents/                    # Subagents (3 files)
│   ├── cco-agent-analyze.md
│   ├── cco-agent-apply.md
│   └── cco-agent-research.md
├── rules/                     # Rule files (44 files)
│   ├── core/                  # Foundation, Safety, Workflow
│   ├── languages/             # 21 language-specific
│   ├── frameworks/            # 8 framework-specific
│   └── operations/            # 12 operations-specific
└── hooks/
    └── core-rules.json        # SessionStart hook
```

---

## Rule Loading Architecture

Rules are loaded automatically at session start via Claude Code's native mechanisms. Core rules are injected through the SessionStart hook, and project-specific rules are auto-loaded from `.claude/rules/*.md`. See [Rules Reference](rules.md#zero-config-loading-mechanism) for the complete mechanism.

---

## Agent System

### cco-agent-analyze

**Purpose:** Read-only analysis. Finds issues, calculates metrics.

| Capability | Output |
|------------|--------|
| Security scan | SEC-01 to SEC-12 findings |
| Quality metrics | Coupling, cohesion, complexity |
| Project detection | Stack, frameworks, maturity |
| Documentation scan | 50+ file patterns |

**Execution pattern:**

```
1. Linters (parallel)    → Bash(lint), Bash(type), Bash(format)
2. Grep patterns        → All scopes in single batch
3. Context reads        → Parallel Read() for matched files
4. Structured output    → JSON with findings, scores, metrics
```

### cco-agent-apply

**Purpose:** Write operations. Applies fixes, writes configs.

| Capability | Output |
|------------|--------|
| Code fixes | Edit files with verification |
| Config writes | Profile, rules, settings |
| Cascade fixes | Fix errors caused by fixes |
| Accounting | done + fail = total |

**Execution pattern:**

```
1. Pre-check           → git status (dirty state warning)
2. Read affected files → Parallel Read()
3. Apply edits         → Parallel Edit() (different files)
4. Verify              → Run lint/type/test after
5. Cascade             → Fix new errors, repeat verify
```

### cco-agent-research

**Purpose:** Information gathering with reliability scoring.

| Capability | Output |
|------------|--------|
| Multi-source search | T1-T6 tiered sources |
| CRAAP+ scoring | Currency, Authority, Accuracy |
| Contradiction handling | Detect, log, resolve |
| Synthesis | Recommendations with confidence |

---

## Command Flow

### /cco:tune

```
User: /cco:tune
          |
          v
    ┌─────────────────┐
    │ Validate profile │
    └────────┬────────┘
             |
    ┌────────┴────────┐
    │ cco-agent-analyze│  ← Detect stack (scope: tune)
    │   - manifests    │
    │   - extensions   │
    │   - frameworks   │
    │   - commands     │
    └────────┬────────┘
             |
    ┌────────┴────────┐
    │ Ask questions   │  ← 8 questions (or --auto)
    │ (if interactive) │
    └────────┬────────┘
             |
    ┌────────┴────────┐
    │ cco-agent-apply │  ← Write files (scope: tune)
    │   - clean old   │
    │   - write new   │
    │   - copy rules  │
    └────────┬────────┘
             |
          Profile created
```

### /cco:optimize

```
User: /cco:optimize
          |
    ┌─────┴─────┐
    │ Q1: Scope  │  ← Areas + Intensity
    │ Q2: Git    │  ← If dirty
    └─────┬─────┘
          |
    ┌─────┴─────┐
    │  Analyze  │  ← cco-agent-analyze (81 checks)
    └─────┬─────┘
          |
    ┌─────┴─────┐
    │Plan Review│  ← If >10 findings or CRITICAL
    └─────┬─────┘
          |
    ┌─────┴─────┐
    │  Apply    │  ← cco-agent-apply (fixes)
    └─────┬─────┘
          |
    Applied: N | Failed: M
```

### /cco:preflight

```
User: /cco:preflight
          |
    ┌─────┴─────┐
    │ Q1: All   │  ← Checks + Intensity + Release mode
    └─────┬─────┘
          |
    ┌─────┴─────────────────┬────────────────────┐
    │                       │                    │
Pre-flight checks    /cco:optimize      Verification
(parallel)           (background)       (background)
    │                       │                    │
    └───────────┬───────────┴────────────────────┘
                |
          ┌─────┴─────┐
          │ Changelog │
          └─────┬─────┘
                |
          ┌─────┴─────┐
          │Plan Review│  ← If blockers or >20 fixes
          └─────┬─────┘
                |
          Go/No-Go Decision
```

---

## Rule Injection

### Core Rules (Always Active)

Injected via SessionStart hook. Cannot be overridden.

| Rule | Type | Effect |
|------|------|--------|
| Complexity Limits | BLOCKER | Method ≤50 lines, CC ≤15 |
| Change Scope | BLOCKER | Only requested changes |
| Read-Before-Edit | BLOCKER | Must read before edit |
| Security Violations | BLOCKER | Fix before continuing |
| Accounting | BLOCKER | applied + failed = total |

### Adaptive Rules (Per-Project)

Loaded from `.claude/rules/cco-*.md`. Selected by detection.

| Category | Files | Trigger |
|----------|-------|---------|
| Languages | 21 | File extensions, manifests |
| Frameworks | 8 | Dependencies in manifest |
| Operations | 12 | CI/CD, infrastructure files |

---

## Parallelization Strategy

### Independent Tool Calls

Multiple tool calls in a single message execute in parallel:

```javascript
// These execute in parallel (same message)
Read("file1.py")
Read("file2.py")
Read("file3.py")
```

### Background Execution

Long-running Bash commands use background mode:

```javascript
// Returns immediately, check later with TaskOutput
testTask = Bash("pytest", { run_in_background: true })
```

### Agent Calls

Task (agent) calls are synchronous - results returned directly:

```javascript
// CORRECT - synchronous
results = Task("cco-agent-analyze", prompt)

// WRONG - background doesn't work for agents
// Task(..., { run_in_background: true })
```

---

## Data Flow

### Profile Schema

```yaml
project:
  name: my-project
  purpose: API for user management
  type: [api]

stack:
  languages: [python, typescript]
  frameworks: [fastapi, react]
  testing: [pytest, jest]
  build: [docker]

maturity: active  # prototype | active | stable | legacy

commands:
  format: "black . && prettier --write ."
  lint: "ruff check ."
  test: "pytest tests/"
  type: "mypy src/"
```

### Finding Schema

```json
{
  "id": "SEC-01",
  "scope": "security",
  "severity": "CRITICAL",
  "title": "Hardcoded API key",
  "location": "src/config.py:42",
  "fixable": true,
  "fix": "Move to environment variable"
}
```

### Accounting Schema

```json
{
  "applied": 12,
  "failed": 1,
  "total": 13
}
```

Invariant: `applied + failed = total`

---

## Model Strategy

| Task | Model | Reason |
|------|-------|--------|
| Detection | Haiku | Fast, read-only |
| Analysis | Haiku | Pattern matching |
| Code fixes | Opus | Fewer errors on edits |
| Synthesis | Opus | Complex reasoning |
| Research | Haiku + Opus | Haiku search, Opus synthesis |

---

*Back to [README](../README.md)*

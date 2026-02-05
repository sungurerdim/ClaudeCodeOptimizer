# Architecture

How CCO works internally: hooks, rules, agents, and command flow.

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

---

## Repository Structure

```
ClaudeCodeOptimizer/
├── rules/
│   └── cco-rules.md            # Core rules (single source of truth)
├── commands/                    # Slash commands (7 files)
│   ├── cco-optimize.md
│   ├── cco-align.md
│   ├── cco-commit.md
│   ├── cco-research.md
│   ├── cco-preflight.md
│   ├── cco-docs.md
│   └── cco-update.md
├── agents/                      # Subagents (3 files)
│   ├── cco-agent-analyze.md
│   ├── cco-agent-apply.md
│   └── cco-agent-research.md
├── install.sh                   # macOS/Linux installer
├── install.ps1                  # Windows installer
└── version.txt                  # Current version
```

### Installed Structure

```
~/.claude/
├── rules/
│   └── cco-rules.md            # Auto-loaded by Claude Code
├── commands/
│   ├── cco-optimize.md ... cco-update.md
└── agents/
    ├── cco-agent-analyze.md ... cco-agent-research.md
```

---

## Rule Loading Architecture

Rules are loaded automatically at session start via Claude Code's native mechanisms. Core rules are auto-loaded from `~/.claude/rules/cco-rules.md`, and project-specific rules are auto-loaded from `.claude/rules/*.md`. See [Rules Reference](rules.md) for the complete mechanism.

---

## Agent System

### cco-agent-analyze

**Purpose:** Read-only analysis. Finds issues, calculates metrics.

| Capability | Output |
|------------|--------|
| Security scan | SEC-01 to SEC-12 findings |
| Quality metrics | Coupling, cohesion, complexity |
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
| Cascade fixes | Fix errors caused by fixes |
| Accounting | applied + failed + needs_approval = total |

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

### /cco-optimize

```
User: /cco-optimize
          |
    ┌─────┴─────┐
    │ Q1: Scope  │  ← Areas + Intensity
    │ Q2: Git    │  ← If dirty
    └─────┬─────┘
          |
    ┌─────┴─────┐
    │  Analyze  │  ← cco-agent-analyze (97 checks)
    └─────┬─────┘
          |
    ┌─────┴─────┐
    │Plan Review│  ← If findings > 0 (mandatory)
    └─────┬─────┘
          |
    ┌─────┴─────┐
    │  Apply    │  ← cco-agent-apply (fixes)
    └─────┬─────┘
          |
    Applied: N | Failed: M
```

### /cco-preflight

```
User: /cco-preflight
          |
    ┌─────┴─────┐
    │ Q1: All   │  ← Checks + Intensity + Release mode
    └─────┬─────┘
          |
    ┌─────┴─────────────────┬────────────────────┐
    │                       │                    │
Pre-flight checks    /cco-optimize      Verification
(parallel)           (background)       (background)
    │                       │                    │
    └───────────┬───────────┴────────────────────┘
                |
          ┌─────┴─────┐
          │ Changelog │
          └─────┬─────┘
                |
          ┌─────┴─────┐
          │Plan Review│  ← If blockers or findings > 0
          └─────┬─────┘
                |
          Go/No-Go Decision
```

---

## Rule Injection

### Core Rules (Always Active)

Auto-loaded from `~/.claude/rules/cco-rules.md`. Cannot be overridden.

| Rule | Type | Effect |
|------|------|--------|
| Complexity Limits | BLOCKER | Method ≤50 lines, CC ≤15 |
| Change Scope | BLOCKER | Only requested changes |
| Read-Before-Edit | BLOCKER | Must read before edit |
| Security Violations | BLOCKER | Fix before continuing |
| Accounting | BLOCKER | applied + failed + needs_approval = total |

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

Long-running Bash commands use background mode. Collect results via `TaskOutput` before any output.

```javascript
// Launch in background
testTask = Bash("pytest", { run_in_background: true })
// ... other work ...
// Collect before reporting
testResult = await TaskOutput(testTask.id)
```

### Agent Calls

Task (agent) calls are always synchronous. `run_in_background` is not supported for Task.

```javascript
results = Task("cco-agent-analyze", prompt)
```

---

## Data Flow

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

Invariant: `applied + failed + needs_approval = total`

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

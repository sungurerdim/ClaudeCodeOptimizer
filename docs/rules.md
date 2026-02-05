# CCO Rules

Core rules auto-loaded from `~/.claude/rules/cco-rules.md` at every session start.

**Source:** `rules/cco-rules.md` — single source of truth. Installed to `~/.claude/rules/cco-rules.md` by the install script.

---

## How It Works

Claude Code automatically reads all `.md` files in `~/.claude/rules/` at session start. CCO rules are loaded into context and active for the entire session. No manual activation needed.

## Rule Categories

| Category | Rules |
|----------|-------|
| **Focus and Discipline** | Decision Commitment, Exploration Restraint, Change Scope, File Discipline |
| **Code Quality** | Complexity Limits (CC≤15, Method≤50, File≤500, Nesting≤3, Params≤4), Code Volume, Anti-Overengineering Guard |
| **Security** | Security Patterns (secrets, bare except, empty catch, unsanitized data, eval) |
| **Workflow** | Uncertainty, Error Recovery, Severity Levels, Scope Creep Detection |
| **CCO Operations** | Version Awareness, Agent Delegation, Efficiency, No Deferrals, Accounting, Skip Patterns, Execution Flow, Plan Review, Confidence Scoring |

## Hard Limits

| Metric | Limit |
|--------|-------|
| Cyclomatic Complexity | ≤ 15 |
| Method Lines | ≤ 50 |
| File Lines | ≤ 500 |
| Nesting Depth | ≤ 3 |
| Parameters | ≤ 4 |

See [rules/cco-rules.md](../rules/cco-rules.md) for the complete rule definitions.

---

*Back to [README](../README.md)*

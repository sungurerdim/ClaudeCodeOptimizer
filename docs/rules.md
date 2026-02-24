# CCO Rules

Core rules auto-loaded from `~/.claude/rules/cco-rules.md` at every session start.

**Source:** `rules/cco-rules.md` — single source of truth. Installed to `~/.claude/rules/cco-rules.md` by the installer.

---

## How It Works

Claude Code automatically reads all `.md` files in `~/.claude/rules/` at session start. CCO rules are loaded into context and active for the entire session. No manual activation needed.

## Rule Categories

| Category | Contents |
|----------|----------|
| **Failure Prevention** | 3 prohibitions (Scope Boundary, Test Integrity, Cross-file Consistency) + 5 process gates (Change Verification, Migration Sweep, Trust Verification, Format Preservation, Artifact-First Recovery) |
| **Process Framework** | 5 checkpoints: before starting, while working, before finishing, on uncertainty, on scope expansion |
| **Quality Thresholds** | Complexity Limits (CC≤15, Method≤50, File≤500, Nesting≤3, Params≤4), Output & Edit Standards, Error Handling, i18n Stack Reference |
| **CCO Operations** | Accounting, Auto Mode, Agent Contract, Tool Prerequisites, Confidence Scoring, Skip Patterns, Plan Review Protocol, Needs-Approval Protocol, Parallel Execution, Severity Levels, Model Routing, CRITICAL Escalation, Fix Quality, Project Types |

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

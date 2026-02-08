# CCO Rules

Core rules auto-loaded from `~/.claude/rules/cco-rules.md` at every session start.

**Source:** `rules/cco-rules.md` — single source of truth. Installed to `~/.claude/rules/cco-rules.md` by the install script.

---

## How It Works

Claude Code automatically reads all `.md` files in `~/.claude/rules/` at session start. CCO rules are loaded into context and active for the entire session. No manual activation needed.

## Rule Categories

| Category | Rules |
|----------|-------|
| **Scope Control** | Minimal Footprint, Exploration Budget, Decide and Execute |
| **Code Integrity** | Complexity Limits (CC≤15, Method≤50, File≤500, Nesting≤3, Params≤4), Anti-Overengineering |
| **Verification** | Read Before Write, Edit Discipline |
| **Uncertainty Protocol** | Surface Uncertainty, Scope Creep Guard |
| **Session Resilience** | Anchor to Artifacts, Error Recovery |
| **Security Baseline** | Security Patterns (secrets, bare except, empty catch, unsanitized data, eval) |
| **Development Standards** | Respect Intent Markers, Issue Prioritization |

Each rule includes a `> Why:` rationale explaining which Opus 4.6 weakness it targets.

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

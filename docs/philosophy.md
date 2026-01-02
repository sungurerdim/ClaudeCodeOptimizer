# CCO Philosophy

The principles and decision framework that guide CCO.

---

## Core Beliefs

### Claude Already Knows How to Code

Opus 4.5 is state-of-the-art. CCO doesn't teach coding—it adds the safety layer between intent and action.

### Process Layer, Not Teaching Layer

CCO provides:
- **Pre-operation safety** — Check before act
- **Standardized workflows** — Consistent patterns
- **Post-operation verification** — Confirm results

### Minimum Footprint

- Zero runtime dependencies
- No logs, configs, or tracking in your project
- Only `~/.claude/` (global) and `.claude/rules/cco/` (project) touched

---

## Design Principles

| Principle | What It Means |
|-----------|---------------|
| **Perfect UX/DX** | Fewest steps to goal, maximum clarity, predictable behavior |
| **Token Efficiency** | Haiku for reads, Opus for writes, lazy rule loading |
| **Minimum Footprint** | Zero deps, no tracking, minimal files |
| **Real Solutions** | Fix root causes, not symptoms |
| **Honest Guidance** | Challenge assumptions, don't just validate |

---

## Decision Framework

How CCO (and Claude with CCO rules) makes decisions:

### Execution Order

| Principle | Description |
|-----------|-------------|
| **Read-First** | Always read files before proposing changes |
| **Plan-Before-Act** | Understand full scope before any action |
| **Incremental** | Complete one step fully before starting next |
| **Verify** | Confirm changes match stated intent |

### Quality Control

| Principle | Description |
|-----------|-------------|
| **No-Hallucination** | Never invent APIs, methods, or file contents |
| **Confirm-Intent** | Verify understanding before acting |
| **Challenge** | Question solutions that seem too perfect |
| **Evidence-Required** | Security claims require code/config proof |
| **Severity-Conservative** | When uncertain, choose lower severity |

### Severity Levels

| Level | Criteria | Examples |
|-------|----------|----------|
| **CRITICAL** | Security breach, data loss, system crash | SQL injection, unencrypted secrets |
| **HIGH** | Broken functionality, blocking issue | Missing validation, type errors |
| **MEDIUM** | Suboptimal but functional | Code smell, missing edge case |
| **LOW** | Style, cosmetic | Formatting, minor refactor |

---

## What CCO Doesn't Do

- **Doesn't track usage** — No analytics, no counters
- **Doesn't phone home** — Fully offline capable
- **Doesn't create unnecessary files** — Only what's needed
- **Doesn't over-engineer** — Simple solutions preferred
- **Doesn't validate blindly** — Will challenge when appropriate

---

## Educational Approach

When CCO fixes something, it explains:

```
[FIXED] SQL injection in api/users.py:42
  Why: Allows database manipulation via user input
  Avoid: f"SELECT * FROM users WHERE id = {user_id}"
  Prefer: cursor.execute("SELECT ... WHERE id = ?", (user_id,))
```

The goal: prevent recurrence by teaching the pattern.

---

## Workflow Integration

CCO fits into your existing workflow:

| When | Command | Purpose |
|------|---------|---------|
| Start session | `/cco-status` | Quick health check |
| After changes | `/cco-commit` | Quality-gated commit |
| Before PR | `/cco-checkup` | Maintenance routine |
| Before release | `/cco-preflight` | Release validation |

See [Workflow Guide](workflow.md) for detailed integration.

---

*Back to [README](../README.md)*

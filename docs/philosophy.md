# Philosophy

The principles and decisions that guide CCO.

---

## Core Belief

**Claude already knows how to code.** Claude is state-of-the-art for software engineering. CCO doesn't teach coding—it adds the safety layer between intent and action.

---

## What CCO Is

A **process layer**, not a teaching layer.

| CCO Provides | CCO Does Not |
|--------------|--------------|
| Pre-operation safety checks | Teach Claude new skills |
| Standardized workflows | Replace Claude's reasoning |
| Post-operation verification | Add magic or snake-oil |
| Context-aware rules | Track or phone home |

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

## Safety-First Workflow

Every operation follows the same pattern:

```
Pre-Check → Analyze → Report → Approve → Apply → Verify
```

| Step | What Happens |
|------|--------------|
| **Pre-Check** | Verify git status, check for dirty state |
| **Analyze** | Identify issues and opportunities |
| **Report** | Present findings with evidence |
| **Approve** | Safe = auto-apply, Risky = ask user |
| **Apply** | Execute changes with tracking |
| **Verify** | Confirm success, report accounting |

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

---

## Severity Levels

| Level | Criteria | Examples |
|-------|----------|----------|
| **CRITICAL** | Security breach, data loss, system crash | SQL injection, unencrypted secrets |
| **HIGH** | Broken functionality, blocking issue | Missing validation, type errors |
| **MEDIUM** | Suboptimal but functional | Code smell, missing edge case |
| **LOW** | Style, cosmetic | Formatting, minor refactor |

---

## What CCO Doesn't Do

- **No tracking** — No analytics, no counters, no metrics collection
- **No network calls** — Fully offline capable, no phone home
- **No unnecessary files** — Only creates what's needed
- **No over-engineering** — Simple solutions preferred
- **No blind validation** — Will challenge when appropriate

---

## Model Strategy

CCO uses Opus + Haiku, no Sonnet.

| Model | Used For | Why |
|-------|----------|-----|
| **Opus** | Code changes, analysis, research synthesis | State-of-the-art accuracy |
| **Haiku** | File reads, quick scans, web fetches | Fast and cost-effective |

**Opus advantages:**
- Fewer tool calling errors
- State-of-the-art on SWE-bench
- Best for multi-step reasoning

---

## Educational Approach

When CCO fixes something, it explains why:

```
[APPLIED] SQL injection in api/users.py:42
  Why: User input passed directly to query allows database manipulation
  Avoid: f"SELECT * FROM users WHERE id = {user_id}"
  Prefer: cursor.execute("SELECT ... WHERE id = ?", (user_id,))
```

The goal: prevent recurrence by teaching the pattern.

---

## Minimum Footprint

CCO only touches:

| Location | Content |
|----------|---------|
| `commands/` | 7 slash commands |
| `agents/` | 3 specialized agents |
| `rules/` | Core rules (auto-loaded) |

**Your project files are never modified.** Core rules are auto-loaded from `~/.claude/rules/cco-rules.md`.

---

## Standards

Built on:

- [Claude 4 Best Practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-4-best-practices)
- [Claude Code Documentation](https://code.claude.com/docs)
- [Google Prompt Engineering Whitepaper](https://www.kaggle.com/whitepaper-prompt-engineering)

**Core:** SSOT, DRY, YAGNI, KISS, Fail-Fast
**AI:** Read-First, Verify-APIs, Evidence-Required
**Security:** OWASP Top 10, Least-Privilege, Defense-in-Depth

See [Rules](rules.md) for complete rule definitions.

### Architectural Principles Cross-Reference

These principles are applied consistently across all CCO commands:

- **Standard Execution Flow** (Setup → Analyze → Gate → Plan → Apply → Summary)
  - Used in: `/cco-optimize`, `/cco-align`, `/cco-preflight`, `/cco-docs`
  - Ensures consistent user experience and reliable checkpoint validation

- **No Deferrals Policy** (Fix everything that can be fixed)
  - Applied in: All commands with `--auto` mode
  - See: `CCO Operation Standards` in core rules for full policy details

- **Model Strategy** (Opus + Haiku only, no Sonnet)
  - Haiku for analysis, reads, web fetches (fast, cost-effective)
  - Opus for code changes, synthesis, complex reasoning (state-of-the-art accuracy)
  - Rationale documented in this file under "Model Strategy" section

For command-specific architectural decisions, see the Architecture section in each command file.

---

*Back to [README](../README.md)*

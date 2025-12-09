# CCO Design Principles

These core principles guide all CCO development and usage. They are implemented through the [CCO Rules](rules.md).

---

## Core Philosophy

> **Claude already knows how to code. CCO adds safety, approval, and consistency.**

CCO is a process layer, not a teaching layer. It provides:
- **Pre-operation safety** - Check before act
- **Standardized workflows** - Consistent patterns
- **Post-operation verification** - Confirm results
- **Context-aware behavior** - Project-specific tuning

---

## Transparency

All operations are visible and predictable.

| Principle | Implemented In |
|-----------|----------------|
| Announce Before Action | AI Rules: Status Updates |
| Progress Signals | AI Rules: Status Updates |
| No Silent Operations | AI Rules: Status Updates |
| Phase Transitions | AI Rules: Status Updates |

---

## User Control

The user is always in charge.

| Principle | Implemented In |
|-----------|----------------|
| Approval Required | Tool Rules: Approval Flow |
| Priority Classification | Tool Rules: Priority Levels |
| Safety Classification | Tool Rules: Safety Classification |
| Rollback Support | Tool Rules: Pre-Operation Safety |

---

## DRY + SSOT

Single source of truth, no duplication.

| Principle | Implemented In |
|-----------|----------------|
| No Hardcoded Values | Tool Rules: Question Formatting |
| Reference Over Repeat | All commands use `**Tool Rules:** !cat...` |
| Conditional Loading | Tool Rules: Context Integration |
| Context-Driven Thresholds | Tool Rules: Context Integration |

---

## Token Efficiency

Optimize for context window usage.

| Principle | Implemented In |
|-----------|----------------|
| Semantic Density | AI Rules: Context Optimization |
| Structured Format | AI Rules: Context Optimization |
| Front-load Critical | AI Rules: Context Optimization |
| Bounded Context | AI Rules: Context Optimization |

---

## Safety-First Workflow

All changes follow a consistent safety pattern.

| Step | Rule |
|------|------|
| 1. Pre-Check | Tool Rules: Pre-Operation Safety |
| 2. Analyze | Tool Rules: Command Flow |
| 3. Report | Tool Rules: Output Formatting |
| 4. Approve | Tool Rules: Approval Flow |
| 5. Apply | Tool Rules: Fix Workflow |
| 6. Verify | Tool Rules: Fix Workflow (Accounting) |

---

## Rule Categories

| Category | Scope |
|----------|-------|
| Core | All projects, AI/human agnostic |
| AI | All AI assistants, model agnostic |
| Tools | CCO workflow mechanisms (on-demand) |
| Adaptive | Dynamically selected by /cco-tune |

For rule counts, see [README](../README.md#rules).

---

*See [Rules Documentation](rules.md) for full details*

*Back to [README](../README.md)*

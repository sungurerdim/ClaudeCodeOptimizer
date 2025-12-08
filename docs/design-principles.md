# CCO Design Principles

These core principles guide all CCO development and usage. They are implemented through the [CCO Standards](standards.md).

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
| Announce Before Action | AI-Specific: Status Updates |
| Progress Signals | AI-Specific: Status Updates |
| No Silent Operations | AI-Specific: Status Updates |
| Phase Transitions | AI-Specific: Status Updates |

---

## User Control

The user is always in charge.

| Principle | Implemented In |
|-----------|----------------|
| Approval Required | CCO-Specific: Approval Flow |
| Priority Classification | CCO-Specific: Priority Levels |
| Safety Classification | CCO-Specific: Safety Classification |
| Rollback Support | CCO-Specific: Pre-Operation Safety |

---

## DRY + SSOT

Single source of truth, no duplication.

| Principle | Implemented In |
|-----------|----------------|
| No Hardcoded Values | CCO-Specific: Question Formatting |
| Reference Over Repeat | All commands use `**Standards:** X \| Y` |
| Conditional Loading | CCO-Specific: Context Integration |
| Context-Driven Thresholds | CCO-Specific: Context Integration |

---

## Token Efficiency

Optimize for context window usage.

| Principle | Implemented In |
|-----------|----------------|
| Semantic Density | AI-Specific: Context Optimization |
| Structured Format | AI-Specific: Context Optimization |
| Front-load Critical | AI-Specific: Context Optimization |
| Bounded Context | AI-Specific: Context Optimization |

---

## Safety-First Workflow

All changes follow a consistent safety pattern.

| Step | Standard |
|------|----------|
| 1. Pre-Check | CCO-Specific: Pre-Operation Safety |
| 2. Analyze | CCO-Specific: Command Flow |
| 3. Report | CCO-Specific: Output Formatting |
| 4. Approve | CCO-Specific: Approval Flow |
| 5. Apply | CCO-Specific: Fix Workflow |
| 6. Verify | CCO-Specific: Fix Workflow (Accounting) |

---

## Standard Categories

| Category | Count | Scope |
|----------|-------|-------|
| Universal | 43 | All projects, AI/human agnostic |
| AI-Specific | 31 | All AI assistants, model agnostic |
| CCO-Specific | 38 | CCO workflow mechanisms |
| Project-Specific | 167 pool | Dynamically selected by /cco-tune |

**Base:** 112 standards always active
**With project:** ~127-147 depending on detection

---

*See [Standards Documentation](standards.md) for full details*

*Back to [README](../README.md)*

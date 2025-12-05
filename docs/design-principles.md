# CCO Design Principles

These core principles guide all CCO development and usage.

---

## Transparency

All operations are visible and predictable.

| Principle | Description |
|-----------|-------------|
| **Announce Before Action** | Always state what will be done before starting |
| **Progress Signals** | Clear "Starting...", "In progress...", "Completed" messages |
| **No Silent Operations** | User should always know what's happening |
| **Phase Transitions** | Clear signals when moving between workflow phases |

---

## Single Source of Truth (SSOT)

Avoid duplication and inconsistency.

| Principle | Description |
|-----------|-------------|
| **No Hardcoded Values** | Use placeholders like `{value}` instead of fixed examples |
| **Reference Over Repeat** | Standards are defined once, referenced by name |
| **Context-Driven** | All thresholds and behaviors come from project context |

---

## DRY (Don't Repeat Yourself)

Minimize redundancy in code and configuration.

| Principle | Description |
|-----------|-------------|
| **Standards Reference** | Commands reference `**Standards:** X \| Y \| Z` instead of duplicating |
| **Shared Agents** | Three agents (detect, scan, action) serve all commands |
| **Conditional Loading** | Project-specific standards loaded only when relevant |

---

## User Control

The user is always in charge.

| Principle | Description |
|-----------|-------------|
| **Approval Required** | No silent changes to codebase |
| **Priority Classification** | CRITICAL > HIGH > MEDIUM > LOW |
| **Safety Classification** | Safe (auto-apply) vs Risky (require approval) |
| **Rollback Support** | Clean git state enables safe recovery |

---

## AI Efficiency

Optimize for context window and token usage.

| Principle | Description |
|-----------|-------------|
| **Semantic Density** | Maximum meaning per token |
| **Structured Format** | Tables/lists over prose for clarity |
| **Front-load Critical** | Important info first (Purpose → Details → Edge cases) |
| **Bounded Context** | Relevant scope only, not entire codebase |

---

## Token-Conscious Design

Every standard, command, and output is designed with context limits in mind.

| Technique | Implementation |
|-----------|----------------|
| **Conditional Loading** | Only load standards relevant to detected project type |
| **Compact Notation** | `Team: Solo \| Scale: <100` instead of prose |
| **Reference by Name** | `**Standards:** Fix Workflow` instead of repeating content |
| **Structured Output** | Tables with consistent columns for easy parsing |

---

## Safety-First Workflow

All changes follow a consistent safety pattern.

```
1. Pre-Check   → Git status, dirty state handling
2. Analyze     → Full scan of target area
3. Report      → Detection table with priority, location, action
4. Approve     → User selects which fixes to apply
5. Apply       → Execute only approved changes
6. Verify      → Before/after comparison + accounting
```

---

*Back to [README](../README.md)*

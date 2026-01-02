# CCO Design Principles

The philosophy and patterns that guide CCO development and usage.

For complete rule definitions, see [Rules Documentation](rules.md).

For software engineering principle definitions (SSOT, DRY, YAGNI, etc.), see [Principles Reference](principles-reference.md).

---

## Core Philosophy

> **Claude already knows how to code. CCO adds safety, approval, and consistency.**

CCO is a process layer, not a teaching layer. It provides:
- **Pre-operation safety** - Check before act
- **Standardized workflows** - Consistent patterns
- **Post-operation verification** - Confirm results
- **Context-aware behavior** - Project-specific tuning

---

## Design Goals

### Transparency
All operations are visible and predictable. Users always know what's happening.

### User Control
The user is always in charge. All risky changes require approval.

### DRY + SSOT
Single source of truth, no duplication. Rules defined once, referenced everywhere.

### Token Efficiency
Optimize for context window usage. Semantic density over verbosity.

---

## Safety-First Workflow

All changes follow a consistent safety pattern:

```
Pre-Check → Analyze → Report → Approve → Apply → Verify
```

1. **Pre-Check** - Git status, dirty state handling
2. **Analyze** - Identify issues/opportunities
3. **Report** - Present findings with evidence
4. **Approve** - User confirms (safe = auto, risky = ask)
5. **Apply** - Execute changes
6. **Verify** - Confirm success with accounting

---

## Prompt Engineering Principles

CCO applies proven prompt engineering techniques from the [Google Prompt Engineering Whitepaper](https://www.kaggle.com/whitepaper-prompt-engineering), adapted for Claude Code + Opus 4.5:

### Instruction-First Approach

**Write positive instructions, not negative constraints.**

| Instead of | Write |
|------------|-------|
| "Never guess file contents" | "Read files before referencing them" |
| "Don't hallucinate APIs" | "Use only documented, existing APIs" |
| "No vague messages" | "Use descriptive action verbs" |

**Why:** Positive instructions are clearer and more actionable. The model performs better when told what TO do rather than what NOT to do.

### Placeholder Standards

All examples and templates use consistent `{placeholder}` format:

| Type | Format | Example |
|------|--------|---------|
| Simple value | `{name}` | `{file}`, `{line}` |
| Enumerated | `{opt1\|opt2}` | `{OK\|WARN\|FAIL}` |
| Counted | `{n}` | Numeric values |
| Path | `{file}:{line}` | Location references |

**Why:** Prevents confusion between examples and actual commands. Placeholders are clearly identifiable.

### Reasoning Strategies

For complex decisions, CCO uses structured reasoning patterns:

| Strategy | When to Use | How |
|----------|-------------|-----|
| **Step-Back** | Complex tasks | Ask broader question before specifics |
| **Chain of Thought** | P0-P1 decisions | Explicit reasoning steps |
| **Self-Consistency** | Critical findings | Multiple reasoning paths + consensus |

**Example (Chain of Thought):**
```
1. Identify: What exactly is the issue?
2. Impact: Who/what is affected?
3. Evidence: What confirms this assessment?
4. Severity: Based on evidence, what's the appropriate level?
```

### Few-Shot Patterns

Examples use generic placeholder patterns, not hardcoded values:

```
User: "{action_request}"
→ AskUserQuestion:
  question: "{clarifying_question}?"
  options: ["{option_1}"; "{option_2}"]
```

**Why:** Hardcoded examples can be misinterpreted as commands. Placeholder patterns show structure without prescribing content.

### Structured Output Schema

All structured output follows consistent JSON schema:

```json
{
  "status": "{OK|WARN|FAIL}",
  "accounting": { "done": "{n}", "failed": "{n}" },
  "items": [{ "severity": "{level}", "location": "{file}:{line}" }]
}
```

---

## Rule Categories

| Category | Scope | Loading |
|----------|-------|---------|
| **Core** | All projects, AI/human agnostic | Always active |
| **AI** | All AI assistants, model agnostic | Always active |
| **Tools** | CCO workflow mechanisms | On-demand |
| **Adaptive** | Stack-based rules | Selected by /cco-config |

---

## Command Authoring

CCO commands use YAML frontmatter for metadata and tool restrictions.

### Frontmatter Format

```yaml
---
name: command-name
description: Brief description
allowed-tools: Tool1(*), Tool2(pattern:*)
---
```

### Required Tools

| Tool | When Required |
|------|---------------|
| `TodoWrite` | ALL commands (progress tracking) |
| `Task(*)` | Commands using sub-agents |

### Tool Pattern Syntax

| Pattern | Matches | Example |
|---------|---------|---------|
| `Tool(*)` | All uses | `Read(*)` |
| `Tool(path/*)` | Path prefix | `Edit(src/*)` |
| `Bash(cmd:*)` | Specific command | `Bash(git:*)` |

### Security Benefit

- **Scope** - Commands can only use declared tools
- **Prevention** - Prevents accidental destructive operations
- **Explicit** - Explicit scope = predictable behavior

---

*See [Rules Documentation](rules.md) for complete rule definitions*

*Back to [README](../README.md)*

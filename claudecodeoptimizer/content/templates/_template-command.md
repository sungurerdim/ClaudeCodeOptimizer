---
name: cco-[command-name]
description: [Brief description - what problem this command solves]
action_type: [audit|fix|generate|optimize|implement|utility]
keywords: [[keyword1], [keyword2], [keyword3]]
category: [discovery|action|productivity|management]
pain_points: [[1], [2], [3]]  # Reference to 12 critical pain points (1-12)
parameters:
  [param-name]:
    keywords: [[param keyword1], [param keyword2]]
    category: [security|quality|testing|infrastructure|etc]
    pain_points: [[X]]
---

# cco-[command-name]

**[One-line description of what this command does]**

---

## Purpose

[2-3 sentence explanation of why this command exists and what value it provides]

---

## Design Principles (CRITICAL)

**All CCO commands must follow these core principles:**

1. **No Hardcoded Examples** - Use `{FILE_PATH}`, `{LINE_NUMBER}`, `{PLACEHOLDERS}` instead of real-looking data
2. **Native Tool Interactions** - Always use `AskUserQuestion` for user input, never text prompts
3. **MultiSelect "All" Option** - Every multiSelect must have "All" as first option
4. **100% Honest Reporting** - Never claim "fixed" without verification, distinguish possible from impossible
5. **Complete Accounting** - Every item: `total = completed + skipped + failed + cannot-do`
6. **Progress Transparency** - Show "Phase X/Y (Z% complete)" for operations >30 seconds
7. **Command Prompt Support** - Accept optional prompt: `/cco-command --flag "additional context"`

---

## Command Prompt Support (DEFAULT BEHAVIOUR)

**This command supports optional prompts for additional context:**

```bash
/cco-[command-name] --[flag] "[Additional context or instructions]"
```

**How it works:**
- Any text after the flags is treated as additional context/instruction
- The AI reads and incorporates this into command execution
- Allows domain-specific guidance, constraints, or preferences
- Enables focusing on specific areas or requirements

**Examples:**
```bash
/cco-[command-name] --[flag1] "Focus on [specific area]"
/cco-[command-name] --[flag2] "Prioritize [specific aspect]"
/cco-[command-name] --all "Apply [specific constraint]"
```

---

## Execution Flow

```
/cco-[command-name]
    │
    ├─► User Confirmation (Step 0 - ALWAYS FIRST)
    │
    ├─► Project Context Discovery (Optional)
    │
    ├─► Phase 1: [Phase Name]
    │
    ├─► Phase 2: [Phase Name]
    │
    ├─► Phase 3: [Phase Name]
    │
    └─► Final Report with Next Steps
```

---

## Step 0: Introduction and Confirmation (ALWAYS FIRST)

**Before doing ANYTHING, present introduction and get user confirmation:**

```markdown
# [Command Name] Command

**What I do:**
[Clear explanation of what this command does]

**How it works:**
1. [Step 1]
2. [Step 2]
3. [Step 3]

**What you'll get:**
- [Outcome 1]
- [Outcome 2]
- [Outcome 3]

**Time estimate:** [X-Y minutes]

**[Warning if applicable - e.g., "Changes WILL be made to your code"]**
```

**Then use AskUserQuestion for confirmation:**

```python
AskUserQuestion({
  questions: [{
    question: "Do you want to proceed?",
    header: "Start [Command]",
    multiSelect: false,
    options: [
      {
        label: "Yes, start",
        description: "[What will happen]"
      },
      {
        label: "No, cancel",
        description: "Exit without making changes"
      }
    ]
  }]
})
```

**CRITICAL:** If user selects "No, cancel" → EXIT immediately

---

## Step 0.5: Project Context Discovery (Optional)

**Ask if user wants project documentation analyzed:**

```python
AskUserQuestion({
  questions: [{
    question: "Extract context from project documentation?",
    header: "Project Context",
    multiSelect: false,
    options: [
      {
        label: "Yes (recommended)",
        description: "Analyze README/CONTRIBUTING for project conventions"
      },
      {
        label: "No",
        description: "Skip documentation analysis (faster)"
      }
    ]
  }]
})
```

**If "Yes" selected, use Haiku sub-agent:**

```python
Task({
    subagent_type: "Explore",
    model: "haiku",
    prompt: """
    Extract project context (MAX 200 tokens):
    - README.md, CONTRIBUTING.md, ARCHITECTURE.md
    - Return: Purpose, Tech Stack, Conventions
    """
})
```

---

## Step 1: [First Step Name]

**Use TodoWrite for progress:**

```python
TodoWrite([
    {"content": "[Step 1 description]", "status": "in_progress", "activeForm": "[Active description]"},
    {"content": "[Step 2 description]", "status": "pending", "activeForm": "[Active description]"},
    {"content": "[Step 3 description]", "status": "pending", "activeForm": "[Active description]"}
])
```

**[Detailed steps for this phase]**

**Simple section header (optional, for log clarity):**

```markdown
=== [Step Name] ===
[Summary of what was accomplished]
```

---

## Step 2: [Second Step Name]

[Similar structure - update TodoWrite, do work]

---

## Step 3: [Third Step Name]

[Similar structure - update TodoWrite, do work]

---

## Final Report

```markdown
═══════════════════════════════════════════════════════════════
                    [COMMAND NAME] REPORT
═══════════════════════════════════════════════════════════════

## Summary

**[Key metric 1]:** [Value]
**[Key metric 2]:** [Value]
**[Key metric 3]:** [Value]

## Results

[Detailed results using ACTUAL data, never hardcoded examples]

### [Category 1] ({COUNT})

[Use {FILE_PATH}:{LINE_NUMBER} placeholders]

### [Category 2] ({COUNT})

[Use {PLACEHOLDERS} for all examples]

## Next Steps

1. [Action 1]
2. [Action 2]
3. [Action 3]

═══════════════════════════════════════════════════════════════
```

---

## State Management (CRITICAL)

**Use single source of truth for all counts:**

```python
@dataclass
class CommandState:
    """Central state - ONLY source for counts."""

    total_items: int = 0
    completed: List = field(default_factory=list)
    skipped: List[Tuple[Item, str]] = field(default_factory=list)
    failed: List[Tuple[Item, str]] = field(default_factory=list)
    cannot_do: List[Tuple[Item, str]] = field(default_factory=list)

    def verify_accounting(self) -> bool:
        """All items must be accounted for."""
        accounted = (len(self.completed) + len(self.skipped) +
                    len(self.failed) + len(self.cannot_do))
        return accounted == self.total_items

    def get_summary(self) -> str:
        """ALWAYS use this for displaying counts."""
        assert self.verify_accounting(), "Accounting error!"
        return f"{len(self.completed)} completed, {len(self.skipped)} skipped..."
```

---

## Agent Usage

**Agent:** `cco-agent-[agent-name]`

**Model Selection:**
- **Haiku**: Simple, mechanical tasks (grep, format, list)
- **Sonnet**: Standard development work (DEFAULT)
- **Auto**: Complex tasks (let Claude Code decide)

**Parallel Execution (when applicable):**
```python
# Independent tasks - run in parallel
Task({subagent_type: "...", model: "sonnet", prompt: "Task 1"})
Task({subagent_type: "...", model: "sonnet", prompt: "Task 2"})
Task({subagent_type: "...", model: "sonnet", prompt: "Task 3"})
```

---

## Skills Usage

**This command uses these skills:**
- `cco-skill-[skill1]` - [Description]
- `cco-skill-[skill2]` - [Description]
- `cco-skill-[skill3]` - [Description]

Skills are referenced in agent prompts for domain knowledge.

---

## CLI Usage

### Interactive (Default)
```bash
/cco-[command-name]
```

### With Parameters
```bash
/cco-[command-name] --[param1]
/cco-[command-name] --[param1] --[param2]
/cco-[command-name] --all
```

### With Additional Context (Optional Prompt)
```bash
/cco-[command-name] --[param1] "Focus on [specific area]"
/cco-[command-name] --[param2] "Prioritize [specific aspect]"
/cco-[command-name] --all "Apply [specific constraint]"
```

**Optional Prompt Benefits:**
- Focus execution on specific areas
- Apply domain-specific context
- Set constraints or preferences
- Reference recent changes or requirements

---

## Example Usage

```bash
# Basic usage
/cco-[command-name] --[common-flag]

# Multiple flags
/cco-[command-name] --[flag1] --[flag2] --[flag3]

# With additional context
/cco-[command-name] --[flag] "Additional instructions here"

# Comprehensive
/cco-[command-name] --all
```

---

## Success Criteria

- [ ] User confirmation obtained (Step 0)
- [ ] Optional context extracted if requested
- [ ] All phases explicitly announced with start/complete
- [ ] Progress shown as "Phase X/Y (Z%)" for long operations
- [ ] All counts consistent (single source of truth)
- [ ] Complete accounting verified (total = completed + skipped + failed + cannot)
- [ ] Results use {PLACEHOLDERS}, never hardcoded examples
- [ ] Native tools used for all user interactions
- [ ] Final report generated with next steps
- [ ] Command prompt support documented and functional

---

## Integration with Other Commands

- **Before this command**: [Related command 1]
- **After this command**: [Related command 2]
- **Works well with**: [Related command 3]

---

## Error Handling

### [Error Type 1]

**Symptoms:** [Description]

**Solution:**
1. [Step 1]
2. [Step 2]

### [Error Type 2]

**Symptoms:** [Description]

**Solution:**
1. [Step 1]
2. [Step 2]

---

**Template Notes:**
- Replace ALL `[placeholders]` with actual content
- Follow ALL design principles (no hardcoded examples, native tools, etc.)
- Always include command prompt support section
- Use AskUserQuestion for ALL user interactions
- Show explicit phase transitions
- Verify complete accounting before claiming completion
- Reference specific principles (U_*, C_*) where applicable

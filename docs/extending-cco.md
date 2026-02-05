# Extending CCO

Create custom rules and understand the extension architecture.

---

## Rule File Format

All rule files use Markdown with consistent structure:

```markdown
# Rule Category Name
*Brief description of the category*

## Rule Name [LEVEL]

Description of what the rule enforces.

**Required actions:**
- Action 1
- Action 2

| Pattern | Fix |
|---------|-----|
| Bad pattern | Good pattern |

## Another Rule [LEVEL]
...
```

### Severity Levels

| Level | Meaning | Effect |
|-------|---------|--------|
| `[BLOCKER]` | Must fix immediately | Execution stops |
| `[CHECK]` | Should verify | Warning only |

---

## Core Rules

All CCO rules are in `rules/cco-rules.md` -- auto-loaded from `~/.claude/rules/cco-rules.md`.

**Categories:**
- **Foundation** - Uncertainty, Complexity, Change Scope, Validation
- **Safety** - Security violations that block execution
- **Workflow** - Read-Before-Edit, Accounting, No Deferrals
- **Tool** - Execution flow, confidence scoring

See [docs/rules.md](rules.md) for full documentation.

---

## Creating Custom Rules

### Step 1: Create File

Create a file in `.claude/rules/` for project-specific rules.

```markdown
# My Custom Rules
*Project-specific coding standards*

## Naming Conventions [BLOCKER]

All service classes must end with `Service`.

- **Service-Suffix**: `class UserService` not `class UserManager`
- **Repository-Suffix**: `class UserRepository` not `class UserDAO`
```

### Step 2: Use Consistent Format

Follow the established patterns:

```markdown
## Rule Name [LEVEL]

Brief description.

**Required:** (for BLOCKER rules)
- Specific requirement 1
- Specific requirement 2

| Bad | Good |
|-----|------|
| `bad_pattern` | `good_pattern` |
```

### Step 3: Make Rules Actionable

Rules must be:
- **Measurable** - Clear pass/fail criteria
- **Specific** - No ambiguous language
- **Enforceable** - Can be checked automatically

```markdown
# Good rule
## Method Length [BLOCKER]
Methods must be ≤50 lines. Split if longer.

# Bad rule
## Code Quality [CHECK]
Code should be "clean" and "readable".
```

---

## Agent Extension

### Agent File Format

Agents use YAML frontmatter + Markdown body:

```markdown
---
name: cco-agent-{name}
description: What this agent does
tools: Tool1, Tool2, Tool3
model: haiku
---

# cco-agent-{name}

Description and instructions.

## When to Use

| Scenario | Use This Agent |
|----------|----------------|
| Case 1 | Yes |
| Case 2 | No |

## Execution

Steps the agent follows...

## Output Schema

\`\`\`json
{
  "field": "type"
}
\`\`\`
```

### Available Tools

| Tool | Purpose |
|------|---------|
| Read | Read file contents |
| Write | Write file contents |
| Edit | Edit existing file |
| Glob | Find files by pattern |
| Grep | Search file contents |
| Bash | Run shell commands |
| WebSearch | Search the web |
| WebFetch | Fetch URL contents |
| Task | Call another agent |
| AskUserQuestion | Prompt user |

---

## Command Extension

### Command File Format

Commands use YAML frontmatter:

```markdown
---
description: What this command does
argument-hint: [--flag1] [--flag2]
allowed-tools: Read(*), Grep(*), Edit(*), Task(*)
model: opus
---

# /cco-commandname

Description and flow.

## Args

- `--flag1`: Effect of flag1
- `--flag2`: Effect of flag2

## Architecture

| Step | Action |
|------|--------|
| 1 | First step |
| 2 | Second step |

## Step-1: Name

Implementation details...
```

### Frontmatter Fields

| Field | Required | Purpose |
|-------|----------|---------|
| description | Yes | One-line description |
| argument-hint | No | Flags shown in help |
| allowed-tools | Yes | Tools command can use |
| model | Yes | haiku or opus |

---

## Contributing Rules

### File Naming Convention

| Type | Pattern | Location |
|------|---------|----------|
| Commands | `cco-{name}.md` | `commands/` |
| Agents | `cco-agent-{name}.md` | `agents/` |
| Core Rules | `cco-rules.md` | `rules/` |

### Validation

Before submitting:

```bash
# Run tests
python -m pytest tests/ -v

# Check counts
ls commands/cco-*.md | wc -l   # Commands: 7
ls agents/*.md | wc -l         # Agents: 3
```

### Pull Request Guidelines

1. **One feature per PR** - Keep changes focused
2. **Update docs** - If adding commands, agents, or rules
3. **Follow patterns** - Check similar files for conventions
4. **Run tests** - All tests must pass

---

## User Rules

Files in `.claude/rules/` are user rules loaded by Claude Code:

```
.claude/rules/
├── my-team-rules.md     ← User (preserved)
└── project-patterns.md  ← User (preserved)
```

CCO core rules are installed to `~/.claude/rules/cco-rules.md`, not copied to your project.

---

*Back to [README](../README.md)*

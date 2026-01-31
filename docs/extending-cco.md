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

## Core Rules Structure

Three core rule files in `rules/core/`:

### cco-foundation.md

Enforceable constraints with measurable thresholds.

**Key rules:**
- Uncertainty Protocol - Stop and ask when unclear
- Complexity Limits - Method ≤50 lines, CC ≤15
- Change Scope - Only requested changes
- Validation Boundaries - Input validation requirements

### cco-safety.md

Security violations that block execution.

**Key rules:**
- No secrets in source
- No bare except/catch
- No unsafe deserialization
- Required input sanitization

### cco-workflow.md

Execution patterns and accounting.

**Key rules:**
- Read-Before-Edit - Must read before editing
- No Deferrals - AI cannot skip fixes in auto mode
- Accounting - applied + failed + needs_approval = total

---

## Language Rules

Located in `rules/languages/cco-{language}.md`.

### File Naming

```
cco-{language}.md
```

Examples: `cco-python.md`, `cco-typescript.md`, `cco-go.md`

### Structure

```markdown
# {Language} Rules
*Stack-specific rules for {Language} projects*

**Trigger:** {manifest_files}, {extensions}

## Category Name

- **Rule-Name**: Description of the rule
- **Another-Rule**: Another description

## Another Category

- **Pattern-Name**: Use `good pattern` not `bad pattern`
```

### Example: Python Rules

```markdown
# Python Rules
*Stack-specific rules for Python projects*

**Trigger:** {py_manifest}, {py_ext}

## Type Annotations

- **Modern-Types**: Use `str | None` not `Optional[str]`
- **Self-Type**: Use `Self` for return type in methods

## Modern Syntax

- **Match-Case**: Use `match`/`case` for complex conditionals
- **F-Strings**: Use f-strings: `f"Hello {name}"`

## Async Patterns

- **TaskGroup**: Use `async with asyncio.TaskGroup()`
```

---

## Framework Rules

Located in `rules/frameworks/cco-{framework}.md`.

### Available Frameworks

| File | Covers |
|------|--------|
| cco-backend.md | FastAPI, Django, Flask, Express |
| cco-frontend.md | React, Vue, Svelte, Next.js |
| cco-api.md | REST, GraphQL, gRPC patterns |
| cco-testing.md | pytest, jest, testing patterns |
| cco-orm.md | SQLAlchemy, Prisma, TypeORM |
| cco-ml.md | PyTorch, TensorFlow, scikit-learn |
| cco-mobile.md | React Native, Flutter |
| cco-realtime.md | WebSocket, SSE patterns |

---

## Operations Rules

Located in `rules/operations/cco-{topic}.md`.

### Available Topics

| File | Covers |
|------|--------|
| cco-security.md | OWASP, auth, encryption |
| cco-cicd.md | GitHub Actions, GitLab CI |
| cco-deployment.md | Docker, Kubernetes |
| cco-database.md | SQL, migrations, indexing |
| cco-observability.md | Logging, metrics, tracing |
| cco-scale.md | Caching, queuing, sharding |
| cco-infrastructure.md | Terraform, cloud patterns |
| cco-build.md | Bundlers, compilers |
| cco-runtimes.md | Node.js, Python, Go |
| cco-messagequeue.md | Kafka, RabbitMQ, Redis |
| cco-compliance.md | GDPR, SOC2, HIPAA |
| cco-project-types.md | CLI, Library, API, Web |

---

## Creating Custom Rules

### Step 1: Create File

Create a file in `.claude/rules/` (project-specific) or contribute to `rules/` (plugin).

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

# /cco:commandname

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
| Rules | `cco-{name}.md` | `rules/{category}/` |
| Commands | `{name}.md` | `commands/` |
| Agents | `cco-agent-{name}.md` | `agents/` |

### Validation

Before submitting:

```bash
# Run tests
python -m pytest tests/ -v

# Verify JSON schemas
python -c "import json; json.load(open('.claude-plugin/plugin.json'))"
python -c "import json; json.load(open('hooks/core-rules.json'))"

# Check counts match docs
ls commands/*.md | wc -l       # Should match "Commands: 7"
ls agents/*.md | wc -l         # Should match "Agents: 3"
find rules -name "cco-*.md" | wc -l  # Should match "Rules: 44"
```

### Pull Request Guidelines

1. **One feature per PR** - Keep changes focused
2. **Update docs** - If adding commands, agents, or rules
3. **Follow patterns** - Check similar files for conventions
4. **Run tests** - All tests must pass

---

## User Rules vs CCO Rules

### User Rules (Preserved)

Files in `.claude/rules/` without `cco-` prefix are user rules:

```
.claude/rules/
├── cco-profile.md       ← CCO (managed)
├── cco-python.md        ← CCO (managed)
├── my-team-rules.md     ← User (preserved)
└── project-patterns.md  ← User (preserved)
```

### CCO Rules (Managed)

Files with `cco-` prefix are managed by CCO:
- Replaced on `/cco:tune`
- Removed on plugin uninstall
- Never manually edit (changes lost on update)

---

*Back to [README](../README.md)*

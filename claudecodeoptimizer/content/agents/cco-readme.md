# CCO Agents

**Specialized AI assistants for complex, multi-step tasks**

---

## What are Agents?

Agents are specialized AI assistants that perform complex, multi-step tasks autonomously. They combine instructions, context, and tools to accomplish specific objectives.

---

## Built-in CCO Agents

CCO includes 4 specialized agents optimized for different task types:

### 1. audit-agent

**Model:** Haiku (fast & cost-efficient)

**Purpose:** Fast scanning and pattern detection

**Capabilities:**
- Pattern matching (SQL injection, XSS, secrets)
- Dependency scanning (CVEs, outdated packages)
- Integration checks (import errors, conflicts)
- Container rule checks (Dockerfile best practices)

**When to use:** Discovery phase, finding issues quickly

**Cost:** Low (Haiku model optimized for pattern matching)

**File:** `cco-agent-audit.md`

---

### 2. fix-agent

**Model:** Sonnet (accurate)

**Purpose:** Semantic code modifications

**Capabilities:**
- Security vulnerability fixes (parameterized queries, input validation)
- Tech debt removal (dead code, unused imports)
- AI quality fixes (hallucinated APIs, code bloat)
- Safe/risky categorization (auto-apply vs approval)

**When to use:** Fixing issues found by audit-agent

**Cost:** Medium (Sonnet needed for semantic understanding)

**File:** `cco-agent-fix.md`

---

### 3. generate-agent

**Model:** Sonnet (quality output)

**Purpose:** Quality code generation

**Capabilities:**
- Test generation (unit, integration, contract, load, chaos)
- Documentation (API docs, ADRs, runbooks)
- Infrastructure (Dockerfile, CI/CD, migrations)
- Monitoring (logging, metrics, SLO)

**When to use:** Creating missing components

**Cost:** Medium (Sonnet ensures quality output)

**File:** `cco-agent-generate.md`

---

### 4. optimize-context-usage-agent

**Model:** Sonnet (semantic verification)

**Purpose:** Context optimization and token reduction

**Capabilities:**
- CLAUDE.md duplication elimination
- Incomplete content detection (stubs, TODOs)
- Internal content optimization (skills, commands, agents)
- Token reduction with quality preservation

**When to use:** Optimizing context usage, reducing tokens

**Cost:** Medium (Sonnet needed for semantic verification)

**File:** `cco-agent-slim.md`

---

## Agent Orchestration Patterns

### Parallel Execution

Independent tasks run simultaneously for speed:

```python
# Security audit with parallel agents
Task(model="haiku", prompt="Scan SQL injection patterns...")
Task(model="haiku", prompt="Scan hardcoded secrets...")
Task(model="haiku", prompt="Check dependency CVEs...")
# All run in parallel → 3x faster
```

### Sequential Pipeline

Dependent tasks run in order:

```python
# audit → fix → generate workflow
audit_result = Task("audit-agent", "Find security issues")
fix_result = Task("fix-agent", f"Fix issues: {audit_result}")
test_result = Task("generate-agent", f"Generate tests for: {fix_result}")
```

### Model Selection

- **Haiku** - Fast scanning, pattern matching (audit)
- **Sonnet** - Accurate modifications, quality generation (fix, generate, slim)
- **Auto** - Complex tasks (let Claude Code decide)


---

## Custom Agents

## Creating a Custom Agent

1. **Copy the template:**
   ```bash
   cp _template-agent.md my-custom-agent.md
   ```

2. **Fill in the details:**
   - Agent name and description
   - Capabilities and use cases
   - Detailed prompt with step-by-step instructions
   - Required tools
   - Model recommendation

3. **Test the agent:**
   Reference it in your project's CLAUDE.md:
   ```markdown
   @.claude/agents/my-custom-agent.md
   ```

## Agent Structure

```markdown
# Agent Name
## Description - What the agent does
## Capabilities - What it can do
## When to Use - Use cases
## Prompt - Detailed instructions
## Tools - Available tools
## Model - Recommended model
## Example - Usage example
```

## Best Practices

- **Clear objective**: Define exactly what the agent should accomplish
- **Step-by-step**: Break down complex tasks into clear steps
- **Tool specification**: List all tools the agent needs
- **Output format**: Specify expected output structure
- **Examples**: Include examples of successful outputs

## Example Agents

You can create agents for:
- Security auditing
- Performance analysis
- Code refactoring
- Documentation generation
- Dependency management
- Test generation
- Database migration
- API design
- Architecture review

## Using Agents in Projects

1. Create symlink during init:
   ```bash
   python -m claudecodeoptimizer init
   # Select your custom agent when prompted
   ```

2. Or manually copy:
   ```bash
   # Windows
   copy my-agent.md "%USERPROFILE%\.claude\agents\"

   # Unix/Linux/Mac
   cp my-agent.md ~/.claude/agents/
   ```

3. Reference in CLAUDE.md:
   ```markdown
   @agents/my-agent.md
   ```

## Sharing Agents

Custom agents in `~/.claude/agents/` are:
- Local to your machine
- Not included in CCO package
- Can be shared via git/copy with team

To share:
1. Copy agent file to team repository
2. Team members copy to their `~/.claude/agents/`
3. Reference in project CLAUDE.md

---

*Add your custom agents here to extend CCO functionality*

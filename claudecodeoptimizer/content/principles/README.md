# CCO Principles

**Universal principles, Claude Code optimizations, and project-specific best practices**

---

## Overview

CCO principles guide Claude Code's behavior to ensure quality, efficiency, and consistency across all operations.

**Total Principles**: 106
- **Universal (U_*)**: 8 - Core development best practices
- **Claude-Specific (C_*)**: 7 - Claude Code optimizations
- **Project-Specific (P_*)**: 91 - Optional domain-specific practices

---

## Categories

### Universal Principles (U_*)

**Core development best practices - Always active**

Fundamental principles that apply to all development work, regardless of language or framework.

- **U_CHANGE_VERIFICATION** - Verify before claiming completion
- **U_CROSS_PLATFORM_COMPATIBILITY** - Works on Windows, Linux, macOS
- **U_DRY** - Single source of truth for all knowledge
- **U_EVIDENCE_BASED_ANALYSIS** - Command execution proof, complete accounting
- **U_FOLLOW_PATTERNS** - Match existing code conventions
- **U_MINIMAL_TOUCH** - Edit only required files
- **U_NO_HARDCODED_EXAMPLES** - Use placeholders, not real data
- **U_NO_OVERENGINEERING** - Simplest solution, avoid premature abstraction

**Why always active?** These prevent bugs, ensure quality, and reduce technical debt universally.

---

### Claude-Specific Principles (C_*)

**Claude Code optimizations - Always active**

Principles that optimize Claude Code's performance, cost, and user experience.

**Context & Efficiency:**
- **C_CONTEXT_WINDOW_MGMT** - Optimize context via grep-first strategy
- **C_EFFICIENT_FILE_OPERATIONS** - Discovery → preview → precise read
- **C_AGENT_ORCHESTRATION_PATTERNS** - Parallel agents, right model selection
- **C_MODEL_SELECTION** - Haiku/Sonnet/Opus based on complexity

**UX & Integration:**
- **C_NATIVE_TOOL_INTERACTIONS** - AskUserQuestion, not text prompts
- **C_NO_UNSOLICITED_FILE_CREATION** - Ask before creating files
- **C_PROJECT_CONTEXT_DISCOVERY** - Extract context before analysis
- **C_MODEL_SELECTION** - Haiku/Sonnet/Opus based on complexity

**Why always active?** These maximize Claude Code's effectiveness and user satisfaction.

---

### Project-Specific Principles (P_*)

**Optional domain-specific best practices - Enable per project**

91 principles covering specialized domains. Enable only what your project needs.

**Categories:**
- **Security** (13) - Auth, encryption, vulnerabilities, privacy
- **Testing & Quality** (13) - TDD, coverage, complexity, refactoring
- **Infrastructure & DevOps** (10) - CI/CD, containers, deployments
- **Architecture & Design** (8) - Patterns, microservices, distributed systems
- **Observability & Monitoring** (8) - Logging, metrics, tracing
- **Performance** (5) - Optimization, caching, profiling
- **Git & Versioning** (8) - Branching, commits, versioning
- **Documentation** (6) - API docs, ADRs, runbooks
- **Resilience & Reliability** (7) - Retries, timeouts, fallbacks
- **Other** (13) - Miscellaneous best practices

**Examples:**
- `P_SQL_INJECTION.md` - SQL injection prevention
- `P_TEST_FIRST_TDD.md` - Test-driven development
- `P_CONTAINER_SECURITY.md` - Docker/K8s security
- `P_STRUCTURED_LOGGING.md` - Structured log format

**See full list:** [CATALOG.md](CATALOG.md)

---

## Using Principles

### Automatic Loading

Universal (U_*) and Claude-specific (C_*) principles are **always loaded** via CLAUDE.md markers:

```markdown
<!-- CCO_PRINCIPLES_START -->















<!-- CCO_PRINCIPLES_END -->
```

See [ADR-001: Marker-based CLAUDE.md System](../../docs/ADR/001-marker-based-claude-md.md)

### Enabling Project Principles

Project-specific (P_*) principles are **optional**. Enable per project needs:

1. Browse [CATALOG.md](CATALOG.md) to find relevant principles
2. Add to CLAUDE.md between `CCO_PRINCIPLES` markers
3. Principles activate automatically via Claude Code

**Example - Enable security principles:**
```markdown
<!-- CCO_PRINCIPLES_START -->
...existing U_* and C_* principles...



<!-- CCO_PRINCIPLES_END -->
```

---

## Principle Compliance

All CCO components (commands, skills, agents) follow these principles:

✅ **No hardcoded examples** - U_NO_HARDCODED_EXAMPLES
✅ **Native tool interactions** - C_NATIVE_TOOL_INTERACTIONS
✅ **Evidence-based with complete accounting** - U_EVIDENCE_BASED_ANALYSIS
✅ **Follow existing patterns** - U_FOLLOW_PATTERNS
✅ **Cross-platform compatibility** - U_CROSS_PLATFORM_COMPATIBILITY

See [PR Template](../../.github/PULL_REQUEST_TEMPLATE.md) for full compliance checklist.

---

## Finding Principles

**Browse by category:** [CATALOG.md](CATALOG.md)

**Search by keyword:**
```bash
# Find security-related principles
grep -r "security" claudecodeoptimizer/content/principles/

# Find test-related principles
grep -r "test" claudecodeoptimizer/content/principles/
```

---

## Creating Custom Principles

Want to add your own principles?

1. Create `P_YOUR_PRINCIPLE.md` in this directory
2. Follow existing principle format (Severity, Why, Rules, Examples)
3. Add to CLAUDE.md to activate
4. Share with team via git

**Note:** Custom principles are local, not part of CCO package.

---

**Total**: 106 principles (8 Universal + 7 Claude + 91 Project)

**Full catalog:** [CATALOG.md](CATALOG.md)

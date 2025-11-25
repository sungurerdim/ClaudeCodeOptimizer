# CCO Principles

**Universal principles and Claude Code optimizations**

---

## Overview

CCO principles guide Claude Code's behavior to ensure quality, efficiency, and consistency across all operations.

**Total Principles**: 13
- **Universal (cco-principle-u-*)**: 8 core development best practices
- **Claude-Specific (cco-principle-c-*)**: 5 Claude Code optimizations

> **Note**: Domain-specific guidance (formerly P_* principles) has been integrated into specialized skills. See [Skills](../skills/) for security, testing, architecture, and other domain-specific guidance.

---

## Categories

### Universal Principles (cco-principle-u-*)

**Core development best practices - Always active**

Fundamental principles that apply to all development work, regardless of language or framework.

- **cco-principle-u-change-verification** - Verify before claiming completion
- **cco-principle-u-cross-platform-compatibility** - Works on Windows, Linux, macOS
- **cco-principle-u-dry** - Single source of truth for all knowledge
- **cco-principle-u-evidence-based-analysis** - Command execution proof, complete accounting
- **cco-principle-u-follow-patterns** - Match existing code conventions
- **cco-principle-u-minimal-touch** - Edit only required files
- **cco-principle-u-no-hardcoded-examples** - Use placeholders, not real data
- **cco-principle-u-no-overengineering** - Simplest solution, avoid premature abstraction

**Why always active?** These prevent bugs, ensure quality, and reduce technical debt universally.

---

### Claude-Specific Principles (cco-principle-c-*)

**Claude Code optimizations - Always active**

Principles that optimize Claude Code's performance, cost, and user experience.

**Context & Efficiency:**
- **cco-principle-c-context-window-mgmt** - Optimize context via grep-first strategy
- **cco-principle-c-efficient-file-operations** - Discovery → preview → precise read

**UX & Integration:**
- **cco-principle-c-native-tool-interactions** - AskUserQuestion, not text prompts
- **cco-principle-c-no-unsolicited-file-creation** - Ask before creating files
- **cco-principle-c-project-context-discovery** - Extract context before analysis

**Why always active?** These maximize Claude Code's effectiveness and user satisfaction.

---

### Domain-Specific Guidance (Skills)

**Auto-activated based on context**

Domain-specific best practices have been integrated into 20 specialized skills for better organization:

| Domain | Skill | Coverage |
|--------|-------|----------|
| Security | cco-skill-security-fundamentals | OWASP, XSS, SQL injection, CSRF |
| AI Security | cco-skill-ai-security | Prompt injection, model security |
| Testing | cco-skill-testing-fundamentals | Test pyramid, coverage, isolation |
| Code Quality | cco-skill-code-quality | Refactoring, complexity |
| Database | cco-skill-database-optimization | N+1, caching, profiling |
| CI/CD | cco-skill-cicd-automation | Gates, deployment, automation |
| Observability | cco-skill-observability | Metrics, alerts, SLOs |

**See full list:** [Skills Catalog](../skills/)

---

## Using Principles

### Automatic Loading

All principles are **always loaded** via CLAUDE.md markers:

```markdown
<!-- CCO_PRINCIPLES_START -->
@principles/cco-principle-u-change-verification.md
@principles/cco-principle-u-cross-platform-compatibility.md
@principles/cco-principle-u-dry.md
@principles/cco-principle-u-evidence-based-analysis.md
@principles/cco-principle-u-follow-patterns.md
@principles/cco-principle-u-minimal-touch.md
@principles/cco-principle-u-no-hardcoded-examples.md
@principles/cco-principle-u-no-overengineering.md
@principles/cco-principle-c-context-window-mgmt.md
@principles/cco-principle-c-efficient-file-operations.md
@principles/cco-principle-c-native-tool-interactions.md
@principles/cco-principle-c-no-unsolicited-file-creation.md
@principles/cco-principle-c-project-context-discovery.md
<!-- CCO_PRINCIPLES_END -->
```

See [ADR-001: Marker-based CLAUDE.md System](../../docs/ADR/001-marker-based-claude-md.md)

### Domain Guidance via Skills

Skills provide domain-specific guidance and auto-activate based on context:

- **File context**: Open `pytest.ini` → testing skill activates
- **Keyword detection**: "SQL injection" → security skill activates
- **Intent matching**: "optimize queries" → database skill activates

No manual configuration needed.

---

## Principle Compliance

All CCO components (commands, skills, agents) follow these principles:

✅ **No hardcoded examples** - cco-principle-u-no-hardcoded-examples
✅ **Native tool interactions** - cco-principle-c-native-tool-interactions
✅ **Evidence-based with complete accounting** - cco-principle-u-evidence-based-analysis
✅ **Follow existing patterns** - cco-principle-u-follow-patterns
✅ **Cross-platform compatibility** - cco-principle-u-cross-platform-compatibility

See [PR Template](../../.github/PULL_REQUEST_TEMPLATE.md) for full compliance checklist.

---

## Finding Guidance

**Browse principles:** [CATALOG.md](CATALOG.md)

**Browse skills:** [Skills Directory](../skills/)

**Search by keyword:**
```bash
# Find security-related guidance
grep -r "security" claudecodeoptimizer/content/

# Find test-related guidance
grep -r "test" claudecodeoptimizer/content/
```

---

**Full catalog:** [CATALOG.md](CATALOG.md)

# CCO Commands

**Quick reference for all CCO slash commands**

---

## Overview

CCO provides 11 slash commands for discovery, fixing, generation, and optimization.

**Command Categories:**
- **Discovery** (2) - Know your problems
- **Action** (3) - Fix your problems
- **Productivity** (3) - Save time
- **Management** (3) - Maintain CCO

**Runtime:** All commands execute within Claude Code via `/cco-<name>` syntax

---

## Quick Reference

### Discovery - Know Your Problems

#### `/cco-status`

**Check CCO installation health**

```bash
/cco-status
```

**Shows:**
- Installed commands, skills, agents, principles
- CCO version and health status

**When to use:** Verify CCO setup, check what's available

---

#### `/cco-help`

**Quick command reference with examples**

```bash
/cco-help
```

**Shows:**
- All commands with descriptions
- Common workflows
- Usage examples
- Typical scenarios

**When to use:** Learn CCO commands, find right command for task

---

### Action - Fix Your Problems

#### `/cco-audit`

**Find problems in your codebase** ⭐ START HERE

```bash
# Quick health check (5 min)
/cco-audit --quick

# Specific categories
/cco-audit --security
/cco-audit --security --tests --database

# AI-specific (2025 pain points)
/cco-audit --ai-security
/cco-audit --ai-quality
/cco-audit --ai  # Meta: all AI categories

# Team quality (2025)
/cco-audit --code-review
/cco-audit --platform

# Comprehensive
/cco-audit --all
```

**Categories (14 total):**
- **Core:** security, tech-debt, tests, database, performance, integration, docs
- **AI (2025):** ai-security, ai-quality
- **Team (2025):** code-review, platform
- **Infrastructure:** ci-cd, containers, supply-chain
- **Meta flags:** --ai (all AI), --ai-debt (AI + tech-debt)

**Output:** Categorized findings with severity, file:line references

**Next steps:** Call `/cco-fix` or `/cco-generate` with context

---

#### `/cco-fix`

**Auto-fix detected problems**

```bash
# Auto-run audit first if needed
/cco-fix --security

# Multiple categories
/cco-fix --security --tech-debt --ai-quality

# After manual audit (receives context)
/cco-audit --security
# ... (audit completes)
/cco-fix  # Uses audit context automatically
```

**Behavior:**
- **Safe fixes:** Auto-applied (parameterized queries, remove dead code)
- **Risky fixes:** Require approval (CSRF protection, auth changes)
- **Receives context:** If `/cco-audit` called first, skips duplicate analysis

**Same 14 categories as audit** (plus meta-flags: --ai, --ai-debt)

**Next steps:** Call `/cco-generate` if tests/docs needed

---

#### `/cco-generate`

**Create missing components**

```bash
# Critical
/cco-generate --tests
/cco-generate --contract-tests

# High priority
/cco-generate --load-tests --chaos-tests
/cco-generate --openapi --cicd

# Team quality (2025)
/cco-generate --review-checklist

# Recommended
/cco-generate --docs --adr --runbook
/cco-generate --dockerfile --migration --indexes
/cco-generate --monitoring --logging --slo
/cco-generate --pre-commit --requirements
```

**Types (18 total):**
- Tests, contract-tests, load-tests, chaos-tests
- OpenAPI, CI/CD, review-checklist
- Docs, ADR, runbook
- Dockerfile, migration, indexes
- Monitoring, logging, SLO
- Pre-commit, requirements

**Output:** Generated files following project conventions

---

### Productivity - Save Time

#### `/cco-optimize-code-performance`

**Speed up your code with metrics**

```bash
# Database optimization
/cco-optimize-code-performance --database

# Docker image size reduction
/cco-optimize-code-performance --docker

# Frontend bundle size
/cco-optimize-code-performance --bundle

# All performance bottlenecks
/cco-optimize-code-performance --performance

# Multiple targets
/cco-optimize-code-performance --database --docker
```

**Types:**
- `--database` - Query optimization, indexes, N+1 fixes
- `--docker` - Image size reduction, layer optimization
- `--bundle` - Frontend bundle analysis, tree-shaking
- `--performance` - General bottleneck detection

**Output:** Before/after metrics for all optimizations

---

#### `/cco-optimize-code-performance-context-usage`

**Context optimization and token reduction**

```bash
# Primary: CLAUDE.md duplication elimination
/cco-optimize-code-performance-context-usage

# With specific focus
/cco-optimize-code-performance-context-usage "Focus on principle duplication"
```

**Primary Mission:**
- Eliminate CLAUDE.md duplication (principles, skills, agents)
- Detect incomplete content (stubs, TODOs)
- Optimize internal content (principles, skills, commands)

**Secondary:** Token reduction for other files (optional)

**Output:** Optimized content with quality preservation

---

#### `/cco-commit`

**Smart git commits with semantic messages**

```bash
# After staging changes
git add .
/cco-commit

# Or let it stage for you
/cco-commit
```

**Features:**
- AI-generated semantic commit messages
- Atomic commit recommendations
- Conventional commits format
- Follows repo commit style

**Output:** Clean, descriptive commits

---

#### `/cco-implement`

**Build new features with TDD**

```bash
/cco-implement "Add JWT authentication"
/cco-implement "Implement rate limiting for API"
```

**Approach:**
- Test-Driven Development (TDD)
- Auto skill selection based on feature type
- Step-by-step implementation

**Output:** Feature implementation with tests

---

### Management - Maintain CCO

#### `/cco-update`

**Update CCO to latest version**

```bash
/cco-update
```

**Updates:**
- All commands, skills, agents, principles
- CLAUDE.md markers
- Template files

**Effect:** One command updates ALL projects instantly (global `~/.claude/`)

---

#### `/cco-remove`

**Clean uninstall (Step 1 of 2)**

```bash
/cco-remove
```

**Removes:**
- All global CCO files (`~/.claude/`)
- Shows what will be deleted before confirmation

**IMPORTANT:** Must run BEFORE `pip uninstall` (requires package to work)

**Complete uninstall:**
```bash
# Step 1: Remove global files (inside Claude Code)
/cco-remove

# Step 2: Uninstall package (outside Claude Code)
pip uninstall claudecodeoptimizer
```

---

## Common Workflows

### New Project Setup
```bash
/cco-audit --quick         # Fast health assessment
/cco-generate --tests --openapi --cicd --dockerfile
```

### Security Hardening
```bash
/cco-audit --security --ai-security --supply-chain
/cco-fix --security
```

### Performance Optimization
```bash
/cco-audit --performance --database
/cco-optimize-code-performance --database --docker
```

### Quality Improvement
```bash
/cco-audit --code-quality --tech-debt --tests
/cco-fix --tech-debt
/cco-generate --tests
```

### AI Code Quality (2025)
```bash
/cco-audit --ai
/cco-fix --ai
```

### Complete Health Check
```bash
/cco-audit --quick         # Baseline
/cco-audit --all           # Find all issues
/cco-fix --all             # Fix safe issues
/cco-generate --all        # Create missing components
/cco-optimize-code-performance --all        # Performance tuning
/cco-commit                # Clean commits
```

---

## Command Chaining (Context Passing)

Commands pass context to each other for efficiency:

**audit → fix:**
```bash
/cco-audit --security
# Finds 12 critical issues: 5x SQL injection, 4x XSS, 3x secrets
/cco-fix --security
# Receives issue list automatically, no duplicate analysis
```

**audit → generate:**
```bash
/cco-audit --tests
# Finds 8 critical files with zero coverage
/cco-generate --tests
# Receives file list automatically, generates tests for those files
```

**fix → generate:**
```bash
/cco-fix --security
# Fixed SQL injection in 5 files
/cco-generate --tests
# Receives fixed file list, generates tests for those changes
```

**Why:** Eliminates duplicate analysis, significantly faster execution

See [C_COMMAND_CONTEXT_PASSING](../principles/C_COMMAND_CONTEXT_PASSING.md) principle

---

## Parameters

### Optional Prompt

All commands support optional prompt after command:

```bash
/cco-audit --security "Focus on authentication endpoints"
/cco-fix --tech-debt "Only remove dead code, skip refactoring"
/cco-generate --tests "Follow pytest conventions"
```

**Effect:** AI treats prompt as additional instruction

---

## Finding Commands

**Interactive help:**
```bash
/cco-help
```

**This reference:**
```bash
cat ~/.claude/commands/README.md  # Unix/macOS
type %USERPROFILE%\.claude\commands\README.md  # Windows
```

**Individual command details:**
```bash
cat ~/.claude/commands/cco-audit.md
```

---

## Related Documentation

- [Architecture Decision Records](../../docs/ADR/)
- [Operational Runbooks](../../docs/runbooks/)
- [Skills Catalog](../skills/SKILLS_CATALOG.md)
- [Agents](../agents/README.md)
- [Principles](../principles/README.md)

---

**Total:** 11 commands across 4 categories

**Runtime:** All execute within Claude Code

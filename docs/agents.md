# CCO Agents

Specialized subagents for CCO commands.

---

## Overview

CCO uses two specialized agents with clear separation of concerns:

| Agent | Purpose | Tools | Safe |
|-------|---------|-------|------|
| **cco-agent-analyze** | Read-only project analysis | Glob, Read, Grep, Bash | Yes |
| **cco-agent-apply** | Write operations with verification | All tools | No |

---

## cco-agent-analyze

**Purpose:** Read-only project analysis and issue detection.

### Scopes

| Scope | Returns | Use Case |
|-------|---------|----------|
| `detect` | Project structure, stack, tools | cco-tune, cco-commit fallback |
| `scan` | Issues with file:line, metrics | cco-audit, cco-health |
| `full` | Both combined | cco-tune first run |

### Detection Capabilities

**Technical:**
- Languages (from file extensions)
- Frameworks (from dependencies)
- Databases (from connection strings, ORMs)
- Infrastructure (Dockerfile, k8s/)
- CI/CD (workflow directories)
- Testing (test directories, frameworks)
- Tools (format, lint, test commands)

**Strategic:**
- Purpose (from README)
- Team size (from git contributors)
- Scale (from README, analytics)
- Data sensitivity (from model fields)
- Project type (from entry points)

**Auto-detected flags:**
- monorepo, preCommitHooks, coverage
- lintingConfigured, apiEndpoints
- containerSetup, i18nSetup
- licenseType, secretsDetected

### Scan Categories

- Security - OWASP Top 10, secrets, SQL injection
- Tech Debt - Complexity >10, dead code, duplication
- Tests - Coverage gaps, missing tests
- Performance - N+1, missing indexes
- Self-Compliance - Violations of stated standards

### Output

Returns structured JSON with:
- `technical` - Stack, tools, conventions
- `strategic` - Purpose, team, scale, data, type
- `autoDetected` - All detected flags
- `findings` - Issues with priority, location, details
- `metrics` - Security, tech debt, coverage scores

---

## cco-agent-apply

**Purpose:** Execute approved changes with verification.

### Operations

| Operation | Input | Output |
|-----------|-------|--------|
| Fix | Finding from analyze | Fixed file + verification |
| Generate | Convention + target | New file(s) |
| Optimize | Analysis result | Reduced code |
| Refactor | Reference map | Updated references |

### Verification Protocol

After each change:
1. **Read** - Confirm edit applied
2. **Grep** - Old pattern count = 0
3. **Grep** - New pattern count = expected
4. **Test** - Run relevant tests

### Status Definitions

| Status | Meaning |
|--------|---------|
| `done` | Applied and verified |
| `skip` | User declined or N/A |
| `fail` | Attempted but failed |

### Accounting

Always reports: `done + skip + fail = total`

---

## Agent Selection by Command

| Command | Analyze Scope | Apply |
|---------|---------------|-------|
| `/cco-tune` | `detect` or `full` | No |
| `/cco-health` | `scan` | No |
| `/cco-audit` | `scan` | Yes (for fixes) |
| `/cco-review` | `scan` | Yes (for recommendations) |
| `/cco-optimize` | `scan` | Yes |
| `/cco-generate` | - | Yes |
| `/cco-refactor` | - | Yes |
| `/cco-commit` | `detect` (fallback) | No |

---

*Back to [README](../README.md)*

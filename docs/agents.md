# CCO Agents

Specialized subagents for CCO commands.

---

## Overview

CCO uses three specialized agents with clear separation of concerns:

| Agent | Purpose | Tools | Safe |
|-------|---------|-------|------|
| **cco-agent-analyze** | Read-only project analysis | Glob, Read, Grep, Bash | Yes |
| **cco-agent-apply** | Write operations with verification | All tools | No |
| **cco-agent-research** | External source research | WebSearch, WebFetch, Read, Grep, Glob | Yes |

---

## cco-agent-analyze

**Purpose:** Read-only project analysis and issue detection.

### Scopes

| Scope | Returns | Use Case |
|-------|---------|----------|
| `detect` | Project structure, stack, tools | cco-config, cco-commit fallback |
| `scan` | Issues with file:line, metrics | cco-optimize, cco-status |
| `full` | Both combined | cco-config first run |
| `security` | Security vulnerabilities, secrets | cco-optimize --security |
| `quality` | Tech debt, consistency, tests | cco-optimize --quality |
| `hygiene` | Orphans, duplicates, stale refs | cco-optimize --hygiene |
| `architecture` | Dependency graph, coupling metrics | cco-review |
| `trends` | Historical metrics with deltas | cco-status --trends |

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

- Security - OWASP Top 10, secrets, CVEs, input validation
- Quality - Complexity >10, type coverage, consistency
- Hygiene - Orphans, stale-refs, duplicates, dead code
- Tests - Coverage gaps, flaky tests, test quality
- Self-Compliance - Violations of stated rules

### Output

Returns structured JSON with:
- `technical` - Stack, tools, conventions
- `strategic` - Purpose, team, scale, data, type
- `autoDetected` - All detected flags
- `findings` - Issues with priority, location, details
- `metrics` - Security, quality, hygiene scores

---

## cco-agent-apply

**Purpose:** Execute approved changes with verification.

### Operations

| Operation | Input | Output |
|-----------|-------|--------|
| Fix | Finding from analyze | Fixed file + verification |
| Generate | Convention + target | New file(s) |
| Optimize | Analysis result | Reduced code |

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

## cco-agent-research

**Purpose:** External source research with reliability scoring and AI synthesis.

### Scopes

| Scope | Returns | Use Case |
|-------|---------|----------|
| `search` | Ranked sources with T1-T6 scores | Initial discovery |
| `analyze` | Deep analysis, contradictions | Follow-up on top sources |
| `synthesize` | Consolidated recommendation | Final answer |
| `full` | All three combined | Standard research flow |
| `dependency` | Package version, CVE, breaking changes | cco-optimize --deps |

### Source Tiers

| Tier | Score | Source Type |
|------|-------|-------------|
| T1 | 95-100 | Official docs (MDN, react.dev) |
| T2 | 85-94 | Official repos, changelogs |
| T3 | 70-84 | Core contributors |
| T4 | 55-69 | Stack Overflow (high votes) |
| T5 | 40-54 | Dev.to, blogs |
| T6 | 0-39 | Unverified, outdated |

### Features

- **CRAAP+ Scoring** - Currency, Relevance, Authority, Accuracy, Purpose
- **Adaptive Replacement** - Discard low-quality sources, find better
- **Contradiction Detection** - Identifies conflicting claims
- **Saturation Detection** - Stop when no new information
- **Bias Detection** - Flags vendor self-promotion
- **Confidence Scoring** - HIGH/MEDIUM/LOW with reasoning

---

## Agent Selection by Command

| Command | Analyze Scope | Apply | Research |
|---------|---------------|-------|----------|
| `/cco-config` | `detect` or `full` | No | No |
| `/cco-status` | `scan`, `trends` | No | No |
| `/cco-optimize` | `security`, `quality`, `hygiene` | Yes | `dependency` |
| `/cco-review` | `architecture`, `scan` | Yes | No |
| `/cco-commit` | `detect` (fallback) | No | No |
| `/cco-research` | - | No | `full` |
| `/cco-preflight` | (orchestrates) | (orchestrates) | No |
| `/cco-checkup` | (orchestrates) | (orchestrates) | No |

---

*Back to [README](../README.md)*

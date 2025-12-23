# CCO Agents

Specialized subagents for CCO commands.

---

## Overview

CCO uses three specialized agents with clear separation of concerns:

| Agent | Purpose | Model | Tools |
|-------|---------|-------|-------|
| **cco-agent-analyze** | Read-only project analysis | haiku | Glob, Read, Grep, Bash |
| **cco-agent-apply** | Write operations with verification | opus | Grep, Read, Glob, Bash, Edit, Write, NotebookEdit |
| **cco-agent-research** | External source research | haiku | WebSearch, WebFetch, Read, Grep, Glob |

**Model Rationale:**
- Haiku for read-only sub-agents (fast, cost-effective)
- Opus for apply agent (50-75% fewer tool errors, coding state-of-the-art)

---

## cco-agent-analyze

**Purpose:** Read-only project analysis and issue detection.

### Scopes

| Scope | Returns | Use Case |
|-------|---------|----------|
| `detect` | Project structure, stack, tools | cco-config, cco-commit fallback |
| `scan` | Issues with file:line, metrics | cco-status |
| `full` | Both combined | cco-config first run |
| `security` | Security vulnerabilities, secrets | cco-optimize --security |
| `quality` | Tech debt, consistency, tests | cco-optimize --quality |
| `hygiene` | Orphans, duplicates, stale refs | cco-optimize --hygiene |
| `best-practices` | Pattern adherence, efficiency | cco-optimize --best-practices |
| `architecture` | Dependency graph, coupling metrics | cco-review |
| `trends` | Historical metrics with deltas | cco-status --trends |
| `config` | Project detection and rule selection | cco-config |

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

### Config Scope

Handles project detection and rule selection for `/cco-config`:

**Execution Flow:**
1. Auto-detect from manifest/code/config/docs (priority order)
2. Ask user-input questions via AskUserQuestion
3. Read adaptive rules template
4. Select rules based on detections + user input
5. Generate context.md + rule files
6. Return structured output

**User Questions:** Team, Scale, Data, Compliance, Testing, SLA, Maturity, Breaking, Priority

### Artifact Handling

| Rule | Implementation |
|------|----------------|
| Reference-Large | By path/ID, not inline |
| Summarize-First | Return summary.count before full array |
| Chunk-Processing | >100 findings → batches |
| Cache-Artifacts | Reuse file reads within session |

### Strategy Evolution

| Pattern | Action |
|---------|--------|
| Same error 3+ files | Add to `Systemic` |
| Recurring false positive | Add to `Avoid` |
| Effective pattern found | Add to `Prefer` |

### Output

Returns structured JSON with:
- `technical` - Stack, tools, conventions
- `strategic` - Purpose, team, scale, data, type
- `autoDetected` - All detected flags
- `findings` - Issues with priority, location, details
- `metrics` - Security, quality, hygiene scores
- `learnings` - Strategy evolution patterns (systemic/avoid/prefer)

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
| `declined` | User explicitly declined |
| `fail` | Attempted but failed |

### Accounting

Always reports: `done + declined + fail = total`

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

## Scope Reference

Complete list of all scopes with their purpose and coverage:

| Scope | Purpose | Coverage |
|-------|---------|----------|
| `detect` | Project discovery | Stack, tools, conventions, structure |
| `scan` | Dashboard metrics | Security, tests, debt, cleanliness scores |
| `full` | Combined detect+scan | All detection + all metrics |
| `security` | Vulnerability detection | OWASP, secrets, CVEs, input validation |
| `quality` | Code quality issues | Complexity, types, consistency, tech debt |
| `hygiene` | Codebase cleanliness | Orphans, stale refs, duplicates, dead code |
| `best-practices` | Pattern adherence | Efficiency, naming, error handling, magic numbers |
| `architecture` | Structural analysis | Dependencies, coupling, layers, patterns |
| `trends` | Historical tracking | Metric deltas with ↑↓→⚠ indicators |
| `config` | Project configuration | Detection + user questions + rule selection |

---

## Agent Selection by Command

| Command | Analyze Scope | Apply | Research |
|---------|---------------|-------|----------|
| `/cco-config` | `config` | No | No |
| `/cco-status` | `scan`, `trends` | No | No |
| `/cco-optimize` | `security`, `quality`, `hygiene`, `best-practices` | Yes | `dependency` |
| `/cco-review` | `architecture`, `best-practices` | Yes | No |
| `/cco-commit` | `detect` (fallback) | No | No |
| `/cco-research` | - | No | `full` |
| `/cco-preflight` | (orchestrates optimize + review) | (orchestrates) | No |
| `/cco-checkup` | (orchestrates status + optimize) | (orchestrates) | No |

---

*Back to [README](../README.md)*

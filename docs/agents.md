# CCO Agents

Specialized subagents that OUTPERFORM default Claude Code tools for specific tasks.

---

## When to Use CCO Agents vs Default Tools

| Task | CCO Agent | Default Alternative | When to Use CCO |
|------|-----------|---------------------|-----------------|
| Research | `cco-agent-research` | WebSearch/WebFetch | 3+ sources, CVE audit, contradictions |
| Analysis | `cco-agent-analyze` | Explore agent | Structured findings, metrics, scans |
| Fixes | `cco-agent-apply` | Edit/Write | Batch fixes, verification needed |

### Quick Decision

```
Need information?
├── Single URL/fact → WebSearch/WebFetch
└── Multiple sources/verification → cco-agent-research

Need analysis?
├── Find file/pattern → Glob/Grep/Read
└── Structured findings/metrics → cco-agent-analyze

Need changes?
├── Single file edit → Edit/Write
└── Multiple files/verification → cco-agent-apply
```

---

## Overview

| Agent                  | Purpose                            | Model | Tools                                                        |
|------------------------|------------------------------------|-------|--------------------------------------------------------------|
| **cco-agent-analyze**  | Comprehensive codebase analysis    | haiku | Glob, Read, Grep, Bash                                       |
| **cco-agent-apply**    | Verified write operations + config | opus  | Grep, Read, Glob, Bash, Edit, Write, NotebookEdit, AskUserQuestion |
| **cco-agent-research** | Multi-source research with scoring | haiku | WebSearch, WebFetch, Read, Grep, Glob                        |

**Model Rationale:**
- Haiku for read-only sub-agents (fast, cost-effective)
- Opus for apply agent (fewer tool errors, coding state-of-the-art)

---

## cco-agent-analyze

**Purpose:** Comprehensive codebase analysis with severity scoring. **Read-only agent.**

**TRIGGERS:** `analyze`, `scan`, `audit`, `find issues`, `code review`, `quality check`, `security scan`, `detect`, `metrics`

### When to Use

| Use This Agent | Use Default Tools Instead |
|----------------|---------------------------|
| Security/quality audit | Find specific file → Glob |
| Metrics (coupling, complexity) | Search one pattern → Grep |
| Multi-scope scan | Read known file → Read |
| Platform-aware analysis | Simple exploration → Explore |

**Advantages over Explore agent:**
- Severity scoring: CRITICAL/HIGH/MEDIUM/LOW with evidence
- Platform filtering: Skips `sys.platform` blocks, cross-platform imports
- Metrics: coupling, cohesion, complexity (architecture scope)
- Output: JSON `{findings[], scores, metrics}` not unstructured text
- Multi-scope: Parallel security+quality+hygiene in single run
- Auto-skip: node_modules, dist, .git, __pycache__
- False positive handling: `excluded[]` with reasons

### Scopes

**OPTIMIZE Scopes** (tactical, file-level fixes):

| Scope          | ID Range         | Checks | Focus                                    |
|----------------|------------------|--------|------------------------------------------|
| `security`     | SEC-01 to SEC-12 | 12     | OWASP, secrets, injection, unsafe patterns |
| `hygiene`      | HYG-01 to HYG-20 | 20     | Unused code, orphan files, dead code     |
| `types`        | TYP-01 to TYP-10 | 10     | Type annotations, mypy/pyright errors    |
| `lint`         | LNT-01 to LNT-08 | 8      | Format, import order, naming, style      |
| `performance`  | PRF-01 to PRF-10 | 10     | N+1, blocking I/O, missing caching       |
| `ai-hygiene`   | AIH-01 to AIH-08 | 8      | Hallucinated APIs, orphan abstractions   |
| `robustness`   | ROB-01 to ROB-10 | 10     | Timeouts, retries, validation            |
| `doc-sync`     | DOC-01 to DOC-08 | 8      | Doc-code consistency, outdated docs      |

**ALIGN Scopes** (strategic, architecture-level):

| Scope              | ID Range         | Checks | Focus                                    |
|--------------------|------------------|--------|------------------------------------------|
| `architecture`     | ARC-01 to ARC-15 | 15     | Coupling, cohesion, layers, dependencies |
| `patterns`         | PAT-01 to PAT-12 | 12     | SOLID, DRY, consistency, design patterns |
| `testing`          | TST-01 to TST-10 | 10     | Coverage strategy, test quality, gaps    |
| `maintainability`  | MNT-01 to MNT-12 | 12     | Complexity, readability, naming          |
| `ai-architecture`  | AIA-01 to AIA-10 | 10     | Over-engineering, drift, premature abstraction |
| `functional-completeness` | FUN-01 to FUN-12 | 12 | CRUD completeness, edge cases            |

**Other Scopes:**

| Scope  | Purpose                              |
|--------|--------------------------------------|
| `scan` | Dashboard metrics (all categories)   |

### Output

Returns structured JSON with:
- `findings` - Issues with severity, location, details
- `scores` - Security, quality, hygiene scores (0-100)
- `metrics` - Coupling, cohesion, complexity
- `excluded` - Filtered items with reasons (platform-specific, etc.)

---

## cco-agent-apply

**Purpose:** Batch write operations with verification and accounting. **Also handles project configuration.**

**TRIGGERS:** `apply fixes`, `fix all`, `batch edit`, `generate config`, `export rules`

### When to Use

| Use This Agent | Use Default Tools Instead |
|----------------|---------------------------|
| Apply 3+ fixes at once | Single-file edit → Edit |
| Need post-change verification | Simple file create → Write |
| Fix cascading errors | Quick one-off edit → Edit |
| Project tuning (scope=tune) | - |
| Track applied/failed counts | - |

**Advantages over Edit/Write:**
- Dirty state check (pre-op `git status`)
- Post-change verification (runs lint/type/test)
- Cascade handling (fixes errors caused by fixes)
- Accounting (done + fail = total)
- No deferrals mode (zero agent-initiated skips)
- Batch efficiency (groups by file)

**Note:** Rollback via git (`git checkout`). Agent warns about dirty state, doesn't create checkpoints.

### Tune Scope

Handles project detection and rule generation:

**Execution Modes:**

| Mode | When Used | Behavior |
|------|-----------|----------|
| Interactive | Default | Detects + asks questions + generates |
| Auto | --auto flag or hook trigger | Detects + uses defaults + generates |

**Interactive Mode Flow:**
1. Auto-detect from manifest/code/config/docs (priority order)
2. Ask user questions via AskUserQuestion (type, team, data, maturity)
3. Generate cco-profile.md with YAML frontmatter
4. Copy rule files from plugin to `.claude/rules/`

**Output Files:**
- `cco-profile.md` - Project metadata (YAML)
- `cco-{language}.md` - Language-specific rules
- `cco-{framework}.md` - Framework-specific rules
- `cco-{operation}.md` - Operations rules

### Fix Operations

| Operation | Input               | Output                    |
|-----------|---------------------|---------------------------|
| Fix       | Finding from analyze | Fixed file + verification |
| Generate  | Convention + target | New file(s)               |
| Optimize  | Analysis result     | Reduced code              |

### Verification Protocol

After each change:
1. **Read** - Confirm edit applied
2. **Grep** - Old pattern count = 0
3. **Grep** - New pattern count = expected
4. **Test** - Run relevant tests

### No Deferrals Policy

**AI never decides to skip or defer. User decides.**

- Interactive Mode: Complex changes prompt user for approval
- Unattended Mode (fixAll: true): ALL findings fixed, no questions
- Accounting: `applied + failed = total` (no AI declines allowed)

### Status Definitions

| Status     | Meaning                  |
|------------|--------------------------|
| `done`     | Applied and verified     |
| `fail`     | Technical impossibility (reason required) |

---

## cco-agent-research

**Purpose:** Multi-source research with CRAAP+ reliability scoring.

**TRIGGERS:** `research`, `compare options`, `best practices`, `which library`, `CVE`, `vulnerability`, `breaking changes`, `migration`

### When to Use

| Use This Agent | Use Default Tools Instead |
|----------------|---------------------------|
| Need 3+ sources for verification | Single known URL → WebFetch |
| CVE/security research | Quick fact check → WebSearch |
| "Which library should I use?" | Official docs lookup → WebFetch |
| Contradicting info online | Simple API lookup → WebSearch |

**Advantages over WebSearch/WebFetch:**
- CRAAP+ scoring: T1-T6 tiers (official docs → unverified)
- Freshness weighting: +10 for <3mo, -15 for >12mo
- Cross-verification: T1 agree = HIGH confidence
- Contradiction handling: Detects, logs, resolves by hierarchy
- Bias detection: Vendor self-promo -5, Sponsored -15
- Saturation: Auto-stop when 3 sources repeat themes
- 4 parallel search strategies: docs, github, tutorial, stackoverflow

### Scopes

| Scope        | Returns                               | Use Case                |
|--------------|---------------------------------------|-------------------------|
| `search`     | Ranked sources with T1-T6 scores      | Initial discovery       |
| `analyze`    | Deep analysis, contradictions         | Follow-up on top sources |
| `synthesize` | Consolidated recommendation           | Final answer            |
| `full`       | All three combined                    | Standard research flow  |
| `dependency` | Package version, CVE, breaking changes | Dependency audit        |

### Source Tiers

| Tier | Score  | Source Type                       |
|------|--------|-----------------------------------|
| T1   | 95-100 | Official docs (MDN, react.dev)    |
| T2   | 85-94  | Official repos, changelogs        |
| T3   | 70-84  | Core contributors                 |
| T4   | 55-69  | Stack Overflow (high votes)       |
| T5   | 40-54  | Dev.to, blogs                     |
| T6   | 0-39   | Unverified, outdated              |

### Features

- **CRAAP+ Scoring** - Currency, Relevance, Authority, Accuracy, Purpose
- **Contradiction Detection** - Identifies conflicting claims
- **Saturation Detection** - Stop when no new information
- **Bias Detection** - Flags vendor self-promotion
- **Confidence Scoring** - HIGH/MEDIUM/LOW with reasoning

---

## Agent Selection by Command

| Command          | Analyze Scope                                      | Apply          | Research     |
|------------------|----------------------------------------------------|----------------|--------------|
| `/cco:optimize`  | security, hygiene, types, lint, performance, etc.  | Yes            | dependency   |
| `/cco:align`     | architecture, patterns, testing, maintainability   | Yes            | dependency   |
| `/cco:commit`    | (quality gates only)                               | No             | No           |
| `/cco:research`  | -                                                  | No             | full         |
| `/cco:preflight` | (orchestrates optimize + align)                    | (orchestrates) | dependency   |

**Configuration:** `/cco:tune` uses cco-agent-apply with `scope=tune` to generate project rules.

---

*Back to [README](../README.md)*

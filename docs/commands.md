# CCO Commands

Detailed documentation for all CCO slash commands.

---

## Command Overview

### Base Commands

| Command         | Purpose                                  | Model     | Steps |
|-----------------|------------------------------------------|-----------|-------|
| `/cco-config`   | Project configuration and settings       | inherit   | 5     |
| `/cco-status`   | Metrics dashboard                        | inherit   | 3     |
| `/cco-optimize` | Security + Quality + Hygiene             | **opus**  | 6     |
| `/cco-review`   | Architecture analysis                    | **opus**  | 5     |
| `/cco-research` | Multi-source research with AI synthesis  | **opus**  | 5     |
| `/cco-commit`   | Quality-gated commits                    | **opus**  | 4     |

### Meta Commands

| Command          | Purpose              | Model   | Orchestrates                         |
|------------------|----------------------|---------|--------------------------------------|
| `/cco-preflight` | Pre-release workflow | inherit | optimize + review + verify (5 steps) |
| `/cco-checkup`   | Regular maintenance  | inherit | status + optimize (3 steps)          |

**Model Rationale:** Opus for analysis and coding commands (50-75% fewer errors), inherit for orchestration.

---

## Command Template Structure

All commands follow a standardized structure for consistency and reliability.

### Standard Sections

```
1. Architecture table     → All steps visible at a glance
2. Progress Tracking      → TodoWrite with all Step-N items
3. Step-N sections        → Each step contains:
   - What to do
   - AskUserQuestion (if applicable)
   - ### Validation block
4. Reference section      → Flags, tables, context application
5. Rules section          → Sequential execution, validation gates
```

### Key Principles

| Principle                              | Description                                                    |
|----------------------------------------|----------------------------------------------------------------|
| **TodoWrite ↔ Architecture alignment** | Same step count in both                                        |
| **Questions in flow**                  | Each question clearly placed in its step                       |
| **Validation gates**                   | Every step ends with validation block                          |
| **Conditional steps**                  | Marked with `[SKIP if X]` or `[MANDATORY if X]`                |
| **Sub-steps**                          | Complex steps use Step-N.1, Step-N.2 format                    |
| **Rules enforcement**                  | "Sequential execution" and "Validation gates" in every command |

### Validation Block Format

```
### Validation
[x] Condition checked
[x] Another condition
→ Store as: variable = {value}
→ If condition: Skip to Step-N
→ Proceed to Step-N
```

---

## Common Features

### Context Requirement

All commands except `/cco-config` require CCO context. If context is missing:
```
CCO context not found.
Run /cco-config first to configure project context, then restart CLI.
```

### Dynamic Context

Commands pre-collect context at execution start:
- Context check (file existence)
- Git status (working tree state)
- Branch, recent commits, tags
- Version info (from manifest files)

**Important:** Pre-collected values are used throughout execution - commands don't re-run these checks.

### Strategy Evolution

Commands learn from execution patterns:

| Pattern              | Action            |
|----------------------|-------------------|
| Same issue 3+ files  | Add to `Systemic` |
| Fix caused cascade   | Add to `Avoid`    |
| Effective pattern    | Add to `Prefer`   |

---

## /cco-config

**Purpose:** Central configuration command for project detection, settings, removal, and export.

**Usage:**
```bash
/cco-config              # Interactive: Configure / Remove / Export
/cco-config --auto       # Unattended mode with smart defaults
```

### Steps

| Step | Name       | Action                            |
|------|------------|-----------------------------------|
| 1    | Pre-detect | cco-agent-analyze (background)    |
| 2    | Setup      | Q1: Combined setup tabs           |
| 3    | Context    | Q2: Context details (conditional) |
| 4    | Apply      | Write files                       |
| 5    | Report     | Summary                           |

### Context Questions (Step-3)

**Team & Data:**
- How many active contributors? (Solo / Small 2-5 / Large 6+)
- Expected scale? (Prototype / Small / Medium / Large)
- Most sensitive data? (Public / PII / Regulated)
- Compliance frameworks? (None / SOC2 / HIPAA / GDPR)

**Operations & Policy:**
- Uptime commitment (SLA)? (None / 99% / 99.9% / 99.99%)
- Development stage? (Prototype / Active / Stable / Legacy)
- Breaking change policy? (Allowed / Minimize / Never)
- Primary focus? (Speed / Balanced / Quality / Security)

### Export Formats

| Format    | Target                                    | Content                    | Output               |
|-----------|-------------------------------------------|----------------------------|----------------------|
| AGENTS.md | Universal (Codex, Cursor, Copilot, Cline) | Core + AI, model-agnostic  | `./AGENTS.md`        |
| CLAUDE.md | Claude Code only                          | Core + AI + Tools, full    | `./CLAUDE.export.md` |

---

## /cco-status

**Purpose:** Single view of project health with actionable next steps.

**Requires:** CCO context (run `/cco-config` first)

**Usage:**
```bash
/cco-status                     # Full dashboard
/cco-status --focus=security    # Focus on security
/cco-status --brief             # Summary only
/cco-status --trends            # With historical trends
/cco-status --json              # JSON output
```

### Steps

| Step | Name    | Action                      |
|------|---------|-----------------------------|
| 1    | Collect | Run agent for metrics       |
| 2    | Process | Calculate scores and trends |
| 3    | Display | Show dashboard              |

### Scores

| Category    | Measures                              |
|-------------|---------------------------------------|
| Security    | Vulnerabilities, secrets, dependencies |
| Tests       | Coverage + quality                    |
| Tech Debt   | Complexity, dead code, duplication    |
| Cleanliness | Orphans, duplicates, stale refs       |

### Score Thresholds

| Score  | Health Status |
|--------|---------------|
| 80-100 | OK            |
| 60-79  | WARN          |
| 40-59  | FAIL          |
| 0-39   | CRITICAL      |

> **Note:** Health status (OK/WARN/FAIL/CRITICAL) indicates overall project health. Finding severity (CRITICAL/HIGH/MEDIUM/LOW) indicates individual issue priority. Same terms, different contexts.

**Trend Indicators:** ↑ Improved │ → Stable │ ↓ Degraded │ ⚠ Rapid decline

---

## /cco-optimize

**Purpose:** Full-stack optimization combining security, code quality, and hygiene checks.

**Requires:** CCO context (run `/cco-config` first)

**Core Principle:** Fix everything that can be fixed. No "manual review" - all issues either auto-fixed or user-approved.

**Usage:**
```bash
/cco-optimize                      # Interactive selection
/cco-optimize --security           # Security focus only
/cco-optimize --quality            # Quality focus only
/cco-optimize --hygiene            # Hygiene focus
/cco-optimize --report             # Report only, no fixes
/cco-optimize --pre-release        # All scopes, strict
/cco-optimize --auto               # Unattended mode: fix all, no questions
```

### Steps

| Step | Name     | Action                                             |
|------|----------|----------------------------------------------------|
| 1    | Setup    | Q1: Combined settings (background analysis starts) |
| 2    | Analyze  | Wait for background, show findings                 |
| 3    | Auto-fix | Apply safe fixes (background)                      |
| 4    | Approval | Q2: Approve remaining (conditional)                |
| 5    | Apply    | Apply approved fixes                               |
| 6    | Summary  | Show counts                                        |

### Scope Categories

| Scope          | Checks                                 |
|----------------|----------------------------------------|
| Security       | OWASP, secrets, CVEs, input validation |
| Quality        | Tech debt, type errors, test gaps      |
| Hygiene        | Orphans, stale refs, duplicates        |
| Best Practices | Patterns, efficiency, consistency      |

### Context Application

| Field    | Effect                                 |
|----------|----------------------------------------|
| Data     | PII/Regulated → security ×2            |
| Scale    | 10K+ → stricter thresholds             |
| Maturity | Legacy → safe fixes only               |
| Priority | Speed → critical only; Quality → all   |

---

## /cco-review

**Purpose:** Strategic architecture analysis with recommendations.

**Requires:** CCO context (run `/cco-config` first)

**Usage:**
```bash
/cco-review                    # Full review
/cco-review --quick            # Smart defaults, report only
/cco-review --focus=architecture
/cco-review --focus=quality
/cco-review --no-apply         # Report only
```

### Steps

| Step | Name            | Action                                              |
|------|-----------------|-----------------------------------------------------|
| 1    | Setup           | Q1: Focus + Apply mode (background analysis starts) |
| 2    | Analysis        | Wait for results, show assessment                   |
| 3    | Recommendations | 80/20 prioritized list                              |
| 4    | Apply           | Apply selected changes                              |
| 5    | Summary         | Show results                                        |

### Focus Areas

| Selection      | Agent Scope                                           |
|----------------|-------------------------------------------------------|
| Architecture   | Dependency graph, coupling, patterns, layers          |
| Code Quality   | Issues with file:line, complexity                     |
| Testing & DX   | Test coverage, developer experience                   |
| Best Practices | Tool usage, execution patterns, efficiency            |
| Dependencies   | Outdated packages, security advisories, version risks |

### Prioritization (80/20)

| Priority | Criteria                  |
|----------|---------------------------|
| Do Now   | High impact, low effort   |
| Plan     | High impact, medium effort |
| Consider | Medium impact             |
| Backlog  | Low impact or high effort |

---

## /cco-research

**Purpose:** Multi-source research with reliability scoring and AI-synthesized recommendations.

**Requires:** CCO context (run `/cco-config` first)

**Usage:**
```bash
/cco-research "query"                    # Standard research
/cco-research "query" --quick            # T1-T2 only, 5 sources
/cco-research "query" --deep             # All tiers, 20+ sources
/cco-research "A vs B" --compare         # Comparison mode
/cco-research "query" --local            # Codebase-only search
/cco-research "query" --security         # Security advisories
```

### Steps

| Step | Name       | Action                       |
|------|------------|------------------------------|
| 1    | Depth      | Ask research depth           |
| 2    | Query      | Parse and understand query   |
| 3    | Research   | Run agent with query         |
| 4    | Synthesize | Process agent results        |
| 5    | Output     | Show structured findings     |

### Source Tiers

| Tier | Sources                  | Score Range |
|------|--------------------------|-------------|
| T1   | Official docs, specs     | 90-100      |
| T2   | GitHub, changelogs       | 80-90       |
| T3   | Major blogs, tutorials   | 70-80       |
| T4   | Stack Overflow, forums   | 60-70       |
| T5   | Personal blogs           | 50-60       |
| T6   | Unknown                  | 40-50       |

### Output Structure

1. **Executive Summary** - TL;DR + confidence score
2. **Evidence Hierarchy** - Primary (85+) / Supporting (70-84)
3. **Contradictions Resolved** - Claim A vs B → Winner
4. **Knowledge Gaps** - Topics with no/limited sources
5. **Actionable Recommendation** - DO / DON'T / CONSIDER
6. **Source Citations** - [N] title | url | tier | score

---

## /cco-commit

**Purpose:** Quality-gated atomic commits.

**Requires:** CCO context (run `/cco-config` first)

**Usage:**
```bash
/cco-commit                 # Full flow
/cco-commit --dry-run       # Preview only
/cco-commit --single        # One commit for all
/cco-commit --quick         # Smart defaults
/cco-commit --skip-checks   # Skip quality gates
```

### Steps

| Step | Name       | Action                                                |
|------|------------|-------------------------------------------------------|
| 1    | Pre-checks | Conflicts check + parallel quality gates (background) |
| 2    | Analyze    | Group changes atomically (while gates run)            |
| 3    | Execute    | Create commits (direct, no approval)                  |
| 4    | Summary    | Show results                                          |

### Quality Gates (Parallel)

| Gate           | Command             | Action                 |
|----------------|---------------------|------------------------|
| 1. Secrets     | Pattern detection   | BLOCK if found         |
| 2. Large Files | Size check          | WARN >1MB, BLOCK >10MB |
| 3. Format      | `{format_cmd}`      | Auto-fix, re-stage     |
| 4. Lint        | `{lint_cmd}`        | STOP on unfixable      |
| 5. Types       | `{type_cmd}`        | STOP on failure        |
| 6. Tests       | `{test_cmd}`        | STOP on failure        |

### Commit Message Format

```
{type}({scope}): {title}

{description}

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

---

## /cco-preflight

**Purpose:** Pre-release workflow orchestration.

**Requires:** CCO context (run `/cco-config` first)

**Usage:**
```bash
/cco-preflight                   # Full release workflow
/cco-preflight --dry-run         # Check without fixing
/cco-preflight --strict          # Fail on any warning
/cco-preflight --tag             # Auto-create git tag
/cco-preflight --tag --push      # Tag and push
```

### Steps

| Step | Name             | Action                                          |
|------|------------------|-------------------------------------------------|
| 1    | Pre-flight       | Release checks (parallel)                       |
| 2    | Quality + Review | Parallel: optimize + review (background)        |
| 3    | Verification     | Background: test/build/lint                     |
| 4    | Changelog        | Generate + suggest version (while tests run)    |
| 5    | Decision         | Q1: Docs + Release decision                     |

### Pre-flight Checks

| Check                                | Type    |
|--------------------------------------|---------|
| Clean working directory              | BLOCKER |
| On `{main_branch}` or release branch | WARN    |
| Version synced across files          | BLOCKER |
| Leftover markers (TODO, FIXME, WIP)  | WARN    |
| SemVer matches changes               | WARN    |

### Go/No-Go Status

| Status           | Action         |
|------------------|----------------|
| Blocker (red)    | Cannot release |
| Warning (yellow) | Can override   |
| Pass (green)     | Ready          |

---

## /cco-checkup

**Purpose:** Regular maintenance routine.

**Requires:** CCO context (run `/cco-config` first)

**Usage:**
```bash
/cco-checkup                   # Standard maintenance
/cco-checkup --dry-run         # Preview without changes
/cco-checkup --no-fix          # Report only
/cco-checkup --health-only     # Skip audit
/cco-checkup --audit-only      # Skip health
```

### Steps

| Step | Name         | Action                                    |
|------|--------------|-------------------------------------------|
| 1    | Phase Select | Determine phases (flags or default: Both) |
| 2    | Execute      | Parallel: health + audit                  |
| 3    | Summary      | Merge and display                         |

### Scheduling

| Frequency | Use Case           |
|-----------|--------------------|
| Weekly    | Active development |
| Bi-weekly | Stable projects    |
| Before PR | Quality gate       |
| Monthly   | Maintenance mode   |

---

*Back to [README](../README.md)*

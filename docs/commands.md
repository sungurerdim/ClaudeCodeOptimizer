# CCO Commands

Detailed documentation for all CCO slash commands.

---

## Command Overview

| Command         | Purpose                                  | Model     | Steps |
|-----------------|------------------------------------------|-----------|-------|
| `/cco-optimize` | Security + Quality + Hygiene fixes       | **opus**  | 4     |
| `/cco-align`    | Architecture gap analysis                | **opus**  | 5     |
| `/cco-research` | Multi-source research with AI synthesis  | **opus**  | 5     |
| `/cco-commit`   | Quality-gated atomic commits             | **opus**  | 5     |
| `/cco-preflight`| Pre-release workflow orchestration       | **opus**  | 4     |
| `/cco-docs`     | Documentation gap analysis               | **opus**  | 5     |
| `/cco-update`   | Update CCO to latest version             | **opus**  | 2     |

**Model Rationale:** Opus for coding commands (fewer errors), Haiku for analysis agents (fast).

---

## Command Template Structure

All commands follow a standardized structure for consistency and reliability.

### Standard Sections

```
1. Architecture table     → All steps visible at a glance
2. Step-N sections        → Each step contains:
   - What to do
   - AskUserQuestion (if applicable)
   - ### Validation block
3. Reference section      → Flags, tables, context application
4. Rules section          → Sequential execution, validation gates
```

### Key Principles

| Principle                | Description                                                    |
|--------------------------|----------------------------------------------------------------|
| **Questions in flow**    | Each question clearly placed in its step                       |
| **Validation gates**     | Every step ends with validation block                          |
| **Conditional steps**    | Marked with `[SKIP if X]` or `[MANDATORY if X]`                |
| **Sub-steps**            | Complex steps use Step-N.1, Step-N.2 format                    |
| **No Deferrals**         | AI never decides to skip - user decides via approval flow      |

---

## Common Features

### Dynamic Context

Commands pre-collect context at execution start:
- Context check (file existence)
- Git status (working tree state)
- Branch, recent commits, tags
- Version info (from manifest files)

**Important:** Pre-collected values are used throughout execution - commands don't re-run these checks.

### No Deferrals Policy

**AI never decides to skip or defer. User decides.**

- **Interactive Mode**: Complex changes prompt user for approval
- **Unattended Mode (--auto)**: ALL findings fixed, no questions
- **Accounting**: `applied + failed + needs_approval = total` (no AI declines allowed)

---

## /cco-optimize

**Purpose:** Full-stack optimization combining security, code quality, and hygiene checks.

**Core Principle:** Fix everything that can be fixed. No "manual review" - all issues either auto-fixed or user-approved.

**Usage:**
```bash
/cco-optimize                      # Interactive selection
/cco-optimize --scope=security     # Security focus only
/cco-optimize --scope=hygiene      # Hygiene focus
/cco-optimize --scope=types        # Type annotations
/cco-optimize --scope=performance  # Performance issues
/cco-optimize --preview            # Report only, no fixes
/cco-optimize --auto               # Unattended mode: fix all, no questions
```

### Steps

| Step | Name         | Action                                        |
|------|--------------|-----------------------------------------------|
| 1    | Setup        | Q1: Scopes + Intensity selection              |
| 2    | Analyze      | Parallel scope analysis, show findings        |
| 2.5  | Plan Review  | Show fix plan (mandatory when findings > 0)   |
| 3    | Apply        | Apply fixes based on intensity                |
| 4    | Summary      | Show counts                                   |

Plan Review is skipped in `--auto` mode or when 0 findings.

### Scope Categories (9 Scopes, 97 Checks)

| Scope          | Checks                                 |
|----------------|----------------------------------------|
| Security       | OWASP, secrets, CVEs, input validation |
| Hygiene        | Orphans, stale refs, duplicates        |
| Types          | Type annotations, mypy/pyright errors  |
| Performance    | N+1, blocking I/O, missing caching     |
| AI-Hygiene     | Hallucinated APIs, orphan abstractions |
| Robustness     | Timeouts, retries, validation          |
| Privacy        | PII exposure, data masking, consent    |
| Doc-Sync       | README outdated, comment-code drift    |
| Simplify       | Nested conditionals, god functions     |

---

## /cco-align

**Purpose:** Strategic architecture analysis - "If I designed from scratch, what would be best?"

**Philosophy:** Evaluate as if no technology choices exist yet. Given only the requirements, what's ideal? Then compare current state to that ideal.

**Usage:**
```bash
/cco-align                         # Full review
/cco-align --preview               # Analyze only, show gaps
/cco-align --auto                  # Unattended mode
```

### Steps

| Step | Name            | Action                                              |
|------|-----------------|-----------------------------------------------------|
| 1a   | Setup           | Q1: Scope + Intensity selection                     |
| 1b   | Analyze         | Parallel scope analysis                             |
| 2    | Gap Analysis    | Current vs Ideal state comparison                   |
| 3    | Recommendations | 80/20 prioritized findings                          |
| 3.5  | Plan Review     | Architectural plan (mandatory when findings > 0)    |
| 4    | Apply           | Apply recommendations                               |
| 5    | Summary         | Show gap changes                                    |

Plan Review is skipped in `--auto` mode or when 0 findings.

### Focus Areas (6 Scopes, 77 Checks)

| Selection               | Agent Scope                                           |
|-------------------------|-------------------------------------------------------|
| Architecture            | Dependency graph, coupling, patterns, layers          |
| Patterns                | SOLID, DRY, design patterns, consistency              |
| Testing                 | Test coverage, developer experience                   |
| Maintainability         | Complexity, readability, naming                       |
| AI-Architecture         | Over-engineering, drift, premature abstraction        |
| Functional-Completeness | CRUD coverage, pagination, edge cases, validation     |

### Gap Analysis

Compares current metrics to ideal targets:

| Metric           | Ideal (API) | Ideal (Library) |
|------------------|-------------|-----------------|
| Coupling         | <30%        | <20%            |
| Cohesion         | >80%        | >85%            |
| Test Coverage    | >80%        | >90%            |
| Cyclomatic Complexity | <10    | <8              |

---

## /cco-research

**Purpose:** Multi-source research with reliability scoring and AI-synthesized recommendations.

**Usage:**
```bash
/cco-research "query"                    # Standard research
/cco-research "query" --quick            # T1-T2 only, 5 sources
/cco-research "query" --deep             # All tiers, 20+ sources
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

**Usage:**
```bash
/cco-commit                 # Full flow
/cco-commit --preview       # Show plan without committing
/cco-commit --single        # One commit for all
/cco-commit --staged-only   # Only staged changes
```

### Steps

| Step | Name       | Action                                                |
|------|------------|-------------------------------------------------------|
| 1    | Pre-checks | Conflicts check + parallel quality gates (background) |
| 2    | Analyze    | Group changes atomically (while gates run)            |
| 3    | Execute    | Create commits (direct, no approval)                  |
| 4    | Verify     | Confirm commits created via git log                   |
| 5    | Summary    | Show results                                          |

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

Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

---

## /cco-preflight

**Purpose:** Pre-release workflow orchestration.

**Usage:**
```bash
/cco-preflight                   # Full release workflow
/cco-preflight --auto            # Unattended checks
/cco-preflight --preview         # Check without releasing
```

### Steps

| Step | Name              | Action                                                 |
|------|-------------------|--------------------------------------------------------|
| 1a   | Settings          | Q1: Fix intensity selection                            |
| 1b   | Pre-flight        | Git state, version sync, markers, deps (parallel)      |
| 2    | Verify + Fix      | 2a: verify (bg Bash) + 2b: optimize+align (Skill)     |
| 3    | Changelog         | Classify commits, suggest version, generate entry      |
| 3.5  | Plan Review       | Combined release plan (conditional, when findings > 0) |
| 4    | Release           | Tag/commit based on decision                           |

Plan Review is skipped in `--auto` mode or when 0 findings + 0 blockers.

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

## /cco-docs

**Purpose:** Documentation gap analysis - compare ideal vs current docs, generate missing content.

**Philosophy:** "What documentation does this project need?" → "What exists?" → "Fill the gap."

**Usage:**
```bash
/cco-docs                    # Interactive selection
/cco-docs --auto             # Generate all missing docs
/cco-docs --preview          # Show gaps only, don't generate
/cco-docs --scope=readme     # Single scope only
/cco-docs --update           # Regenerate even if docs exist
```

### Steps

| Step | Name         | Action                                           |
|------|--------------|--------------------------------------------------|
| 1a   | Scope        | Q1: Scope selection (parallel with analysis)     |
| 1b   | Analysis     | Scan existing docs, detect project type          |
| 2    | Gap          | Compare ideal vs current                         |
| 3    | Plan Review  | Show generation plan (conditional)               |
| 4    | Generate     | Create missing documentation                     |
| 5    | Summary      | Show results                                     |

Plan Review triggers when findings > 0, >3 documents to generate, or API scope selected. Skipped in `--auto` mode.

### Documentation Scopes

| Scope     | Target Files                    | Purpose                    |
|-----------|--------------------------------|----------------------------|
| readme    | README.md                       | Project overview, quick start |
| api       | docs/api/*.md, API.md           | Endpoint/function reference |
| dev       | CONTRIBUTING.md, docs/dev/*.md  | Developer onboarding       |
| user      | docs/user/*.md, USAGE.md        | End-user guides            |
| ops       | docs/ops/*.md, DEPLOY.md        | Deployment, operations     |
| changelog | CHANGELOG.md                    | Version history            |
| refine    | Existing docs                   | UX/DX quality improvement  |
| verify    | Existing docs                   | Verify claims vs source code |

### Ideal Docs by Project Type

| Type    | Required         | Optional    |
|---------|------------------|-------------|
| CLI     | README, usage    | contributing |
| Library | README, API, dev | guides      |
| API     | README, API, dev, ops | user   |
| Web     | README, dev, ops | components  |

### Documentation Principles

All generated docs follow these rules:

- **Brevity > verbosity**: Every sentence must earn its place
- **Examples > prose**: Show, don't tell
- **Scannable**: Headers, bullets, tables for quick scanning
- **Copy-pasteable**: Commands should work when pasted
- **No filler**: Skip "This document explains..."

---

## /cco-update

**Purpose:** Update CCO to the latest version by re-running the install script.

**Usage:**
```bash
/cco-update
```

### Steps

| Step | Name    | Action                                        |
|------|---------|-----------------------------------------------|
| 1    | Detect  | Detect platform (macOS/Linux/Windows)         |
| 2    | Install | Run the appropriate install script            |

---

*Back to [README](../README.md)*

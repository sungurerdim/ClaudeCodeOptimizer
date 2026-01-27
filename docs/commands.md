# CCO Commands

Detailed documentation for all CCO slash commands.

---

## Command Overview

| Command         | Purpose                                  | Model     | Steps |
|-----------------|------------------------------------------|-----------|-------|
| `/cco:optimize` | Security + Quality + Hygiene fixes       | **opus**  | 6     |
| `/cco:align`    | Architecture gap analysis                | **opus**  | 5     |
| `/cco:research` | Multi-source research with AI synthesis  | **opus**  | 5     |
| `/cco:commit`   | Quality-gated atomic commits             | **opus**  | 4     |
| `/cco:preflight`| Pre-release workflow orchestration       | **opus**  | 5     |
| `/cco:docs`     | Documentation gap analysis               | **opus**  | 5     |

**Model Rationale:** Opus for analysis and coding commands (50-75% fewer errors).

**Project Configuration:** Handled automatically via auto-setup (SessionStart hook or command fallback) when CCO detects an unconfigured project.

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

### Auto-Setup (No Manual Config Required)

CCO automatically detects unconfigured projects at session start:

1. **Check**: Does `.claude/rules/cco-profile.md` exist with all required fields?
2. **If NO**: Offers setup options:
   - `[Auto-setup]` - Detect stack and create rules automatically
   - `[Interactive]` - Ask questions to customize setup
   - `[Skip]` - Don't configure CCO for this project

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
- **Accounting**: `applied + failed = total` (no AI declines allowed)

---

## /cco:optimize

**Purpose:** Full-stack optimization combining security, code quality, and hygiene checks.

**Core Principle:** Fix everything that can be fixed. No "manual review" - all issues either auto-fixed or user-approved.

**Usage:**
```bash
/cco:optimize                      # Interactive selection
/cco:optimize --security           # Security focus only
/cco:optimize --hygiene            # Hygiene focus
/cco:optimize --types              # Type annotations
/cco:optimize --lint               # Lint/format fixes
/cco:optimize --performance        # Performance issues
/cco:optimize --report             # Report only, no fixes
/cco:optimize --auto               # Unattended mode: fix all, no questions
/cco:optimize --fix-all            # Everything mode: zero deferrals
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
| Hygiene        | Orphans, stale refs, duplicates        |
| Types          | Type annotations, mypy/pyright errors  |
| Lint           | Format, import order, naming, style    |
| Performance    | N+1, blocking I/O, missing caching     |
| AI-Hygiene     | Hallucinated APIs, orphan abstractions |
| Robustness     | Timeouts, retries, validation          |

---

## /cco:align

**Purpose:** Strategic architecture analysis - "If I designed from scratch, what would be best?"

**Philosophy:** Evaluate as if no technology choices exist yet. Given only the requirements, what's ideal? Then compare current state to that ideal.

**Usage:**
```bash
/cco:align                         # Full review
/cco:align --quick                 # Smart defaults, report only
/cco:align --focus=architecture
/cco:align --focus=patterns
/cco:align --intensity=full-fix    # Fix all findings
/cco:align --auto                  # Unattended mode
```

### Steps

| Step | Name            | Action                                              |
|------|-----------------|-----------------------------------------------------|
| 1    | Setup           | Q1: Focus + Intensity (background analysis starts)  |
| 2    | Analysis        | Wait for results, show assessment                   |
| 3    | Recommendations | Gap analysis with ideal metrics                     |
| 4    | Apply           | Apply selected changes                              |
| 5    | Summary         | Show results                                        |

### Focus Areas

| Selection        | Agent Scope                                           |
|------------------|-------------------------------------------------------|
| Architecture     | Dependency graph, coupling, patterns, layers          |
| Patterns         | SOLID, DRY, design patterns, consistency              |
| Testing          | Test coverage, developer experience                   |
| Maintainability  | Complexity, readability, naming                       |
| AI-Architecture  | Over-engineering, drift, premature abstraction        |

### Gap Analysis

Compares current metrics to ideal targets:

| Metric           | Ideal (API) | Ideal (Library) |
|------------------|-------------|-----------------|
| Coupling         | <30%        | <20%            |
| Cohesion         | >80%        | >85%            |
| Test Coverage    | >80%        | >90%            |
| Cyclomatic Complexity | <10    | <8              |

---

## /cco:research

**Purpose:** Multi-source research with reliability scoring and AI-synthesized recommendations.

**Usage:**
```bash
/cco:research "query"                    # Standard research
/cco:research "query" --quick            # T1-T2 only, 5 sources
/cco:research "query" --deep             # All tiers, 20+ sources
/cco:research "A vs B" --compare         # Comparison mode
/cco:research "query" --local            # Codebase-only search
/cco:research "query" --security         # Security advisories
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

## /cco:commit

**Purpose:** Quality-gated atomic commits.

**Usage:**
```bash
/cco:commit                 # Full flow
/cco:commit --dry-run       # Preview only
/cco:commit --single        # One commit for all
/cco:commit --staged-only   # Only staged changes
/cco:commit --no-verify     # Skip quality gates
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

## /cco:preflight

**Purpose:** Pre-release workflow orchestration.

**Usage:**
```bash
/cco:preflight                   # Full release workflow
/cco:preflight --dry-run         # Check without fixing
/cco:preflight --strict          # Fail on any warning
/cco:preflight --tag             # Auto-create git tag
/cco:preflight --tag --push      # Tag and push
```

### Steps

| Step | Name             | Action                                          |
|------|------------------|-------------------------------------------------|
| 1    | Pre-flight       | Release checks (parallel)                       |
| 2    | Quality + Align  | Parallel: /cco:optimize + /cco:align (background)       |
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

## /cco:docs

**Purpose:** Documentation gap analysis - compare ideal vs current docs, generate missing content.

**Philosophy:** "What documentation does this project need?" → "What exists?" → "Fill the gap."

**Usage:**
```bash
/cco:docs                    # Interactive selection
/cco:docs --auto             # Generate all missing docs
/cco:docs --check            # Validation only, return status
/cco:docs --report           # Show gaps, don't generate
/cco:docs --scope=readme     # Single scope only
/cco:docs --scope=api        # API docs only
/cco:docs --plan             # Show plan before generating
/cco:docs --force            # Regenerate even if docs exist
```

### Steps

| Step | Name      | Action                                           |
|------|-----------|--------------------------------------------------|
| 1    | Setup     | Q1: Scope + Mode selection (background analysis) |
| 2    | Analysis  | Scan existing docs, detect project type          |
| 3    | Gap       | Compare ideal vs current                         |
| 4    | Generate  | Create missing documentation                     |
| 5    | Summary   | Show results                                     |

### Documentation Scopes

| Scope     | Target Files                    | Purpose                    |
|-----------|--------------------------------|----------------------------|
| readme    | README.md                       | Project overview, quick start |
| api       | docs/api/*.md, API.md           | Endpoint/function reference |
| dev       | CONTRIBUTING.md, docs/dev/*.md  | Developer onboarding       |
| user      | docs/user/*.md, USAGE.md        | End-user guides            |
| ops       | docs/ops/*.md, DEPLOY.md        | Deployment, operations     |
| changelog | CHANGELOG.md                    | Version history            |

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

*Back to [README](../README.md)*

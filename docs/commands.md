# CCO Commands

Detailed documentation for all CCO slash commands.

---

## Command Overview

### Base Commands

| Command | Purpose | Key Rules |
|---------|---------|-----------|
| `/cco-config` | Project configuration and settings | Approval Flow, Output Formatting |
| `/cco-status` | Metrics dashboard with trends | Command Flow, Output Formatting |
| `/cco-optimize` | Security + Quality + Hygiene | Fix Workflow, Safety Classification |
| `/cco-review` | Architecture analysis | Fix Workflow, Approval Flow |
| `/cco-research` | Multi-source research with AI synthesis | Command Flow, Output Formatting |
| `/cco-commit` | Quality-gated commits | Pre-Operation Safety, Approval Flow |

### Meta Commands

| Command | Purpose | Orchestrates |
|---------|---------|--------------|
| `/cco-preflight` | Pre-release workflow | optimize + review + verify |
| `/cco-checkup` | Regular maintenance | status + optimize --fix |

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
| Pattern | Action |
|---------|--------|
| Same issue 3+ files | Add to `Systemic` |
| Fix caused cascade | Add to `Avoid` |
| Effective pattern | Add to `Prefer` |

---

## /cco-config

**Purpose:** Central configuration command for project detection, settings, removal, and export.

**Usage:**
```bash
/cco-config              # Interactive: Configure / Remove / Export
```

**Flow:**
1. **STATUS** - Shows current project state
2. **CHOOSE** - Select actions from grouped options
3. **DETECT** - Run detection (if Configure selected)
4. **REVIEW** - Accept/Edit/Cancel
5. **APPLY** - Write configurations, remove items, export files
6. **REPORT** - Summary with all changes

**Actions (single multiSelect question):**

| Section | Options |
|---------|---------|
| **Configure** | Detection & Rules, AI Performance, Statusline, Permissions |
| **Remove** | Remove AI Performance, Remove Statusline, Remove Permissions, Remove Rules |
| **Export** | AGENTS.md (recommended), CLAUDE.md |

**Features:**
- Mixed operations in single run (e.g., Configure + Remove + Export)
- Remove options only shown if item is configured

**Export formats:**

| Format | Target | Content | Output |
|--------|--------|---------|--------|
| AGENTS.md | Universal (Codex, Cursor, Copilot, Cline, etc.) | Core + AI, model-agnostic | `./AGENTS.md` |
| CLAUDE.md | Claude Code only | Core + AI + Tools, full | `./CLAUDE.export.md` |

**Export sources:**
- Reads from: `~/.claude/rules/cco/` + `.claude/rules/cco/`
- Never exports: AI Performance, Statusline, Permissions

**AGENTS.md content filtering:**
- Removes Claude-specific: tool names, `.claude/` paths, CCO references
- Preserves: model-agnostic principles (DRY, Fail-Fast, Read-First)

---

## /cco-status

**Purpose:** Single view of project health with actionable next steps.

**Requires:** CCO context (run `/cco-config` first)

**Usage:**
```bash
/cco-status                     # Full dashboard
/cco-status --focus=security    # Focus on security
/cco-status --focus=tests       # Focus on tests
/cco-status --focus=tech-debt   # Focus on tech debt
/cco-status --brief             # Summary only
/cco-status --trends            # With historical trends
/cco-status --json              # JSON output
```

**Scores (0-100):**
- Security - Vulnerabilities, secrets, dependencies
- Tests - Coverage + quality
- Tech Debt - Complexity, dead code, duplication
- Cleanliness - Orphans, duplicates, stale refs

**Score Thresholds:** 90-100: OK │ 70-89: WARN │ 50-69: FAIL │ 0-49: CRITICAL

**Trend Indicators:** ↑ Improved │ → Stable │ ↓ Degraded │ ⚠ Rapid decline

---

## /cco-optimize

**Purpose:** Full-stack optimization combining security, code quality, and hygiene checks.

**Requires:** CCO context (run `/cco-config` first)

**Core Principle:** Fix everything that can be fixed. No "manual review" - all issues either auto-fixed or user-approved.

**Usage:**
```bash
/cco-optimize                      # Interactive 2-tab selection
/cco-optimize --all --fix          # Full optimization with fix
/cco-optimize --security           # Security focus only
/cco-optimize --quality            # Quality focus only
/cco-optimize --hygiene            # Hygiene focus (orphans, stale, dupes)
/cco-optimize --quick              # Fast hygiene cleanup
/cco-optimize --pre-release        # Pre-release gate checks
/cco-optimize --deps               # Dependency freshness check
/cco-optimize --all --report       # Full scan, no changes
```

**Interactive 2-Tab Selection:**

| Tab | Question | Options |
|-----|----------|---------|
| Scope | What to check? | Security; Quality; Hygiene; All (Recommended) |
| Action | How to handle? | Report Only; Auto-fix (Recommended); Full Auto-fix; Interactive |

**Scope Categories:**

| Scope | Includes |
|-------|----------|
| **Security** | OWASP vulnerabilities, secrets, CVEs, supply-chain, input validation |
| **Quality** | Complexity, type coverage, test quality, consistency, self-compliance |
| **Hygiene** | Orphans, stale-refs, duplicates, dead code, dependencies |

**Sub-Scope Flags:**

| Flag | Scope | Checks |
|------|-------|--------|
| `--owasp` | Security | OWASP Top 10 |
| `--secrets` | Security | Secret detection |
| `--cves` | Security | Dependency CVEs |
| `--tech-debt` | Quality | Complexity, TODOs |
| `--consistency` | Quality | Doc-code mismatch |
| `--tests` | Quality | Coverage, flaky tests |
| `--orphans` | Hygiene | Unreferenced code |
| `--stale-refs` | Hygiene | Broken references |
| `--duplicates` | Hygiene | Duplicate code |
| `--deps` | Hygiene | Dependency freshness |

**Key Features:**
- OWASP risk rating for priority
- Root cause correlation (N findings → 1 root cause)
- False positive reduction
- Safe removal verification
- Cascading impact analysis
- Remediation verification

**Context Application:**
| Field | Effect |
|-------|--------|
| Data | PII/Regulated → security ×2 |
| Scale | 10K+ → stricter thresholds |
| Maturity | Legacy → safe fixes only |
| Priority | Speed → critical only; Quality → all |

**Strategy Evolution:** Learns patterns (Systemic, Avoid, Prefer) for future runs

---

## /cco-review

**Purpose:** Strategic architecture analysis with recommendations.

**Requires:** CCO context (run `/cco-config` first)

**Usage:**
```bash
/cco-review                    # Full review
/cco-review --quick            # Skip from-scratch analysis
/cco-review --focus=structure  # Focus on organization
/cco-review --focus=security   # Focus on security
/cco-review --focus=deps       # Focus on dependencies
```

**Phases:**
1. Map Current State - Architecture, patterns, dependencies
2. Gap Analysis - Purpose vs implementation
3. Stack Fitness - Tech choices evaluation
4. Fresh Perspective - "If building from scratch"
5. Prioritization - Quick wins vs major refactors
6. Apply (optional) - Implement approved recommendations

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
/cco-research "query" --focus=official   # Official sources only
/cco-research "query" --local            # Codebase-only search
/cco-research "query" --security         # Security advisories
```

**Source Tiers:**
| Tier | Score | Source Type |
|------|-------|-------------|
| T1 | 95-100 | Official docs (MDN, react.dev, docs.python.org) |
| T2 | 85-94 | Official repos, changelogs, RFCs |
| T3 | 70-84 | Core contributors, library authors |
| T4 | 55-69 | Stack Overflow (high votes), verified Medium |
| T5 | 40-54 | Dev.to, Hashnode, Reddit, blogs |
| T6 | 0-39 | Unverified, AI-generated, outdated |

**Quality Features:**
- CRAAP+ scoring framework (Currency, Relevance, Authority, Accuracy, Purpose)
- Adaptive source replacement (discard low-quality, find better)
- Iterative deepening (seed → backward snowballing → forward snowballing)
- Saturation detection (stop when no new info)
- Contradiction resolution
- Knowledge gap identification

---

## /cco-commit

**Purpose:** Quality-gated atomic commits.

**Requires:** CCO context (run `/cco-config` first)

**Usage:**
```bash
/cco-commit                 # Full flow
/cco-commit --dry-run       # Preview only
/cco-commit --single        # One commit for all
/cco-commit --skip-checks   # Skip quality gates
```

**Quality gates:** Format → Lint → Test (stop on failure)

**Features:**
- Vague message detection and rejection
- Change type classification verification
- Atomic commit verification
- Semantic versioning impact tracking
- Commit history style matching

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

**Phases:**
1. **Pre-flight** - Git state, branch, version, changelog, dependencies
2. **Quality Gate** - via `/cco-optimize --pre-release --fix` (all scopes)
3. **Architecture** - via `/cco-review --quick`
4. **Final Verification** - Full test suite, build, lint, type check
5. **Changelog & Docs** - Release notes and documentation sync
6. **Go/No-Go** - Blockers vs warnings summary, next steps

**Classification:**
- **Blockers** - Must fix before release (dirty git, invalid version, tests fail)
- **Warnings** - Should fix (coverage below target, outdated changelog)

---

## /cco-checkup

**Purpose:** Regular maintenance routine.

**Requires:** CCO context (run `/cco-config` first)

**Usage:**
```bash
/cco-checkup                   # Standard maintenance
/cco-checkup --dry-run         # Preview without changes
/cco-checkup --no-fix          # Report only
/cco-checkup --deep            # Thorough checkup
/cco-checkup --trends          # With trend history
```

**Phases:**
1. **Health Dashboard** - via `/cco-status --brief`
2. **Quality Audit** - via `/cco-optimize --fix` (all scopes)
3. **Summary** - Changes since last checkup, fixed vs declined

**Scheduling:**
| Frequency | Use Case |
|-----------|----------|
| Weekly | Active development |
| Bi-weekly | Stable projects |
| Before PR | Quality gate |
| Monthly | Maintenance mode |

---

*Back to [README](../README.md)*

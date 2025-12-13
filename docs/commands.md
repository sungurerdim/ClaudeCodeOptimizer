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
| **Export** | CLAUDE.md, AGENTS.md |

**Features:**
- Mixed operations in single run (e.g., Configure + Remove + Export)
- Remove options only shown if item is configured
- Export content is user-selectable (Core Rules, AI Rules, Tool Rules, Project Context, Adaptive Rules)

**Export sources:**
- Reads from installed files: `~/.claude/CLAUDE.md` + `./CLAUDE.md`
- Never exports: AI Performance, Statusline, Permissions (project-specific)

**Export targets:**
- **AGENTS.md** → `./AGENTS.md` (Tool Rules excluded)
- **CLAUDE.md** → `./CLAUDE.export.md` (all rules)

---

## /cco-status

**Purpose:** Single view of project health with actionable next steps.

**Usage:**
```bash
/cco-status                     # Full dashboard
/cco-status --focus=security    # Focus on security
/cco-status --focus=tests       # Focus on tests
/cco-status --focus=tech-debt   # Focus on tech debt
/cco-status --brief             # Summary only
```

**Scores (0-100):**
- Security - Vulnerabilities, secrets, dependencies
- Tests - Coverage + quality
- Tech Debt - Complexity, dead code, duplication
- Self-Compliance - Alignment with stated rules

---

## /cco-optimize

**Purpose:** Full-stack optimization combining security, code quality, and hygiene checks.

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

---

## /cco-review

**Purpose:** Strategic architecture analysis with recommendations.

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

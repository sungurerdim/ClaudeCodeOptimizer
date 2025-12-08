# CCO Commands

Detailed documentation for all CCO slash commands.

---

## Command Overview

| Command | Purpose | Key Standards |
|---------|---------|---------------|
| `/cco-tune` | Project tuning and configuration | Approval Flow, Output Formatting |
| `/cco-health` | Metrics dashboard | Command Flow, Output Formatting |
| `/cco-audit` | Quality gates with fixes | Fix Workflow, Safety Classification |
| `/cco-review` | Architecture analysis | Fix Workflow, Approval Flow |
| `/cco-research` | Multi-source research with AI synthesis | Command Flow, Output Formatting |
| `/cco-optimize` | Efficiency improvements | Fix Workflow, Safety Classification |
| `/cco-generate` | Convention-following generation | Approval Flow, Output Formatting |
| `/cco-refactor` | Safe structural changes | Pre-Operation Safety, Approval Flow |
| `/cco-commit` | Quality-gated commits | Pre-Operation Safety, Approval Flow |

---

## /cco-tune

**Purpose:** Central configuration command for project detection, settings, removal, and export.

**Usage:**
```bash
/cco-tune              # Interactive: Configure / Remove / Export
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
| **Configure** | Detection & Standards, AI Performance, Statusline, Permissions |
| **Remove** | Remove AI Performance, Remove Statusline, Remove Permissions, Remove Standards |
| **Export** | CLAUDE.md, AGENTS.md |

**Features:**
- Mixed operations in single run (e.g., Configure + Remove + Export)
- Remove options only shown if item is configured
- Export content is user-selectable (Universal, AI-Specific, CCO-Specific, Project Context, Conditional)

**Export sources:**
- Reads from installed files: `~/.claude/CLAUDE.md` + `./CLAUDE.md`
- Never exports: AI Performance, Statusline, Permissions (project-specific)

**Export targets:**
- **AGENTS.md** → `./AGENTS.md` (CCO-Specific excluded)
- **CLAUDE.md** → `./CLAUDE.export.md` (all standards)

---

## /cco-health

**Purpose:** Single view of project health with actionable next steps.

**Usage:**
```bash
/cco-health                     # Full dashboard
/cco-health --focus=security    # Focus on security
/cco-health --focus=tests       # Focus on tests
/cco-health --focus=tech-debt   # Focus on tech debt
```

**Scores (0-100):**
- Security - Vulnerabilities, secrets, dependencies
- Tests - Coverage + quality
- Tech Debt - Complexity, dead code, duplication
- Self-Compliance - Alignment with stated standards

---

## /cco-audit

**Purpose:** Find issues, prioritize, and fix with approval.

**Usage:**
```bash
/cco-audit                   # Interactive
/cco-audit --smart           # Auto-detect applicable
/cco-audit --pre-release     # Production readiness
/cco-audit --critical        # Security + tests + database
/cco-audit --hygiene         # Orphans + stale-refs + consistency
/cco-audit --orphans         # Find unreferenced code
/cco-audit --stale-refs      # Find broken references
/cco-audit --auto-fix        # Auto-fix safe issues
```

**Categories:**
- Core: `--security`, `--tech-debt`, `--self-compliance`, `--consistency`, `--orphans`, `--stale-refs`
- Stack-dependent: `--tests`, `--database`, `--performance`, `--docs`, etc.

**Detection:** Orphan files/functions/imports, broken imports, dead links, stale docs.

---

## /cco-review

**Purpose:** Strategic architecture analysis with recommendations.

**Usage:**
```bash
/cco-review                    # Full review
/cco-review --quick            # Skip from-scratch analysis
/cco-review --focus=structure  # Focus on organization
/cco-review --focus=security   # Focus on security
```

**Phases:**
1. Map Current State - Architecture, patterns, dependencies
2. Gap Analysis - Purpose vs implementation
3. Stack Fitness - Tech choices evaluation
4. Fresh Perspective - "If building from scratch"
5. Prioritization - Quick wins vs major refactors

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
/cco-research "query" --focus=community  # Include community perspectives
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

**Dynamic Modifiers:**
- Freshness: 0-3 months (+10), 3-12 months (0), >12 months (-15)
- Engagement: High stars/votes (+5)
- Author: Core maintainer (+10)
- Cross-verified by T1-T2 (+10)
- Bias detected: Vendor self-promo (-5), Sponsored (-15)

**Analysis Features:**
- Contradiction Detection: Identifies conflicting information
- Consensus Mapping: Weighted agreement by tier
- Bias Detection: Flags promotional content
- Evidence Chain: Shows source verification trail

**Output Sections:**
1. Source Summary - Tier breakdown with counts and scores
2. Key Findings - Ranked findings with freshness
3. Contradictions - Conflicting views with resolution
4. Consensus Map - Agreement percentages by tier weight
5. AI Recommendation - Confidence level, reasoning, caveats, alternatives
6. Sources - Full citations with key quotes

---

## /cco-optimize

**Purpose:** Reduce waste, measure impact, verify.

**Usage:**
```bash
/cco-optimize                    # Interactive
/cco-optimize --context          # AI context files
/cco-optimize --docs             # Documentation
/cco-optimize --code             # Source files
/cco-optimize --cross-file       # Full cross-file analysis
/cco-optimize --dedupe           # Focus on duplicate detection
/cco-optimize --consolidate      # Merge overlapping content
/cco-optimize --prune            # Remove obsolete/orphan content
/cco-optimize --all              # Everything
```

**Modes:** Conservative | Balanced | Aggressive

**Detection:** Exact/near/semantic duplicates, redundant code/config/docs, obsolete refs, overlaps.

---

## /cco-generate

**Purpose:** Generate components following project conventions.

**Usage:**
```bash
/cco-generate              # Interactive
/cco-generate --tests      # Unit/integration tests
/cco-generate --docs       # Documentation
/cco-generate --infra      # CI/CD, Docker
/cco-generate --all        # Everything applicable
```

**Convention enforcement:** Uses patterns from existing code, not imposing new ones.

---

## /cco-refactor

**Purpose:** Safe structural changes with reference verification.

**Usage:**
```bash
/cco-refactor                              # Interactive
/cco-refactor rename oldName newName       # Rename
/cco-refactor move old/path new/path       # Move
/cco-refactor extract "code" newModule     # Extract
/cco-refactor inline functionName          # Inline
```

**Safety:** Requires clean git state. Auto-rollback on failure.

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

---

*Back to [README](../README.md)*

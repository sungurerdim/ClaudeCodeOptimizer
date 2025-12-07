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
| `/cco-optimize` | Efficiency improvements | Fix Workflow, Safety Classification |
| `/cco-generate` | Convention-following generation | Approval Flow, Output Formatting |
| `/cco-refactor` | Safe structural changes | Pre-Operation Safety, Approval Flow |
| `/cco-commit` | Quality-gated commits | Pre-Operation Safety, Approval Flow |

---

## /cco-tune

**Purpose:** Central configuration command for project detection, AI settings, and export.

**Usage:**
```bash
/cco-tune              # Interactive tuning
/cco-tune --export     # Export standards
```

**What it does:**
1. Shows current project status
2. Offers configuration options (Detection, Statusline, Permissions)
3. Runs detection if selected
4. Writes context to `./CLAUDE.md`

**Export formats:**
- **AGENTS.md** - For other AI tools (Universal + AI-Specific + Project-Specific)
- **CLAUDE.md** - For Claude Code (includes CCO-Specific)

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

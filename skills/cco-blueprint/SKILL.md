---
description: Project health system — profile-based assessment, transformation, and progress tracking. Use for project scoring, blueprint init, or health refresh.
argument-hint: "[--auto] [--preview] [--init] [--refresh] [--scope=<name>] [--force-approve]"
allowed-tools: Read, Grep, Glob, Edit, Bash, Task, AskUserQuestion
disable-model-invocation: true
---

# /cco-blueprint

**Project Health System** — Profile-based assessment, transformation, and progress tracking.

## Flags

| Flag | Effect |
|------|--------|
| `--auto` | All phases, no questions, single-line summary |
| `--preview` | Analyze + dashboard, no changes |
| `--init` | Profile creation/refresh only (no analysis) |
| `--refresh` | Re-scan profile (decisions preserved) |
| `--scope=X` | Specific area: stack, deps, dx, structure, code, architecture, docs, memory, all |
| `--force-approve` | Auto-apply needs_approval items (architectural changes). Combines with `--auto`. |

## Context

- Git status: !`git status --short --branch`
- Args: $ARGUMENTS

## CLAUDE.md Profile Format

Profile stored between `<!-- cco-blueprint-start -->` and `<!-- cco-blueprint-end -->` markers. Content outside markers is never modified.

```markdown
<!-- cco-blueprint-start -->
## CCO Blueprint Profile

**Project:** {name} | **Type:** {type} | **Stack:** {stack} | **Target:** {quality}

### Config
- **Priorities:** {list}
- **Constraints:** {list}
- **Data:** {data types} | **Regulations:** {if applicable}
- **Audience:** {audience} | **Deploy:** {deploy method}

### Project Map
Entry: {entry point} → {framework}
Modules: {module → role mapping}
External: {external dependencies}
Toolchain: {tools} | {CI} | {container}

### Ideal Metrics
| Metric | Target |
|--------|--------|
| Coupling | {value} |
| Cohesion | {value} |
| Complexity | {value} |
| Coverage | {value} |

### Current Scores
| Dimension | Score | Status |
|-----------|-------|--------|
| Security & Privacy | {n} | {OK/WARN} |
| Code Quality | {n} | {OK/WARN} |
| Architecture | {n} | {OK/WARN} |
| Performance | {n} | {OK/WARN} |
| Resilience | {n} | {OK/WARN} |
| Testing | {n} | {OK/WARN} |
| Stack Health | {n} | {OK/WARN} |
| DX | {n} | {OK/WARN} |
| Documentation | {n} | {OK/WARN} |
| Overall | {n} | {OK/WARN} |
<!-- cco-blueprint-end -->
```

**Profile read/write rules:**
- If CLAUDE.md does not exist → create with profile section only
- If exists → strip ALL CCO marker sections before writing: v4 (`cco-blueprint-start/end`), v2-v3 (`CCO_ADAPTIVE_START/END`), v2 (`CCO_CONTEXT_START/END`), v1-v2 (`CCO_PRINCIPLES_START/END`)
- Preserve all content outside markers

## Phase Checklist

| Phase | Name | Skippable? |
|-------|------|------------|
| 1 | Discovery | No |
| 2 | Init Flow | Yes (if profile exists) |
| 3 | Assess | No |
| 3.1 | Project Map | No |
| 4 | Consolidate | No |
| 5 | Plan Review | Yes (--auto) |
| 6 | Apply | Yes (--preview) |
| 6.1 | Needs-Approval Review | Yes (--auto, --force-approve auto-applies) |
| 7 | Update Profile | No |
| 7.1 | Memory Cleanup | Yes (--preview) |
| 8 | Summary | No |

Before reporting completion, verify every non-skipped phase produced output.

## Execution Flow

Discovery → [Init Flow] → Assess [PARALLEL] → Consolidate → Plan → [Apply] → Update Profile → Summary

### Phase 1: Discovery [PARALLEL]

**Pre-flight:** Verify git repo: `git rev-parse --git-dir 2>/dev/null` → not a repo: warn "Not a git repo — git context unavailable" and continue (git optional for blueprint).

1. Search CLAUDE.md for `<!-- cco-blueprint-start -->`
2. Parallel project detection via Glob/Grep/Read: language (majority file ext), framework (express/fastapi/react/etc), project type (routes→API, pages→Web, bin→CLI, src/lib→Library), toolchain (.eslintrc, tsconfig, biome.json), CI/CD, Docker, tests, data sensitivity (password/email/token patterns), git status

**Decision tree:**
1. Profile exists AND not --init/--refresh → Phase 3 (incremental)
2. Profile exists AND --refresh → Phase 2 (re-ask, preserve decisions)
3. No profile AND --init → Phase 2 (create profile, stop)
4. No profile AND not --init → Phase 2 (create profile, ask to continue)

### Phase 2: Init Flow [no profile OR --init/--refresh]

Two AskUserQuestion calls (6 questions total, all in English). Detection results marked "(Detected)".

#### Call 1: Project Identity

Per CCO Rules: Project Types — use standardized type IDs and UI categories.

```javascript
AskUserQuestion([
  {
    question: "What category best describes this project?",
    header: "Project Type",
    options: [
      { label: "{Detected type} (Detected)", description: "Auto-detected from project structure" },
      { label: "Frontend", description: "Web apps, mobile apps, desktop apps, games" },
      { label: "Backend", description: "APIs, data pipelines, ML/AI services" },
      { label: "Developer Tool", description: "CLIs, libraries, SDKs, plugins, extensions" },
      { label: "Infrastructure", description: "IaC, CI/CD, embedded, deployment" }
    ],
    multiSelect: false
  },
  {
    question: "What quality level should this project meet?",
    header: "Quality",
    options: [
      { label: "Prototype", description: "Minimal checks",
        markdown: "All thresholds relaxed 30%\n────────────────────────────\nScopes:  Core checks only\n         (security, hygiene)\nSkip:    Architecture, docs,\n         ai-hygiene\nFocus:   Get it working" },
      { label: "MVP", description: "Ship fast with basics covered",
        markdown: "All thresholds relaxed 15%\n────────────────────────────\nScopes:  Security + quality\n         + performance\nSkip:    ai-hygiene\nFocus:   Ship with basics" },
      { label: "Production (Recommended)", description: "Full quality gates",
        markdown: "Standard thresholds\n────────────────────────────\nScopes:  All 9 scopes\nChecks:  97 total checks\nFocus:   Full quality gates\n         OWASP security scan" },
      { label: "Enterprise", description: "Compliance and audits required",
        markdown: "All thresholds strict +10%\n────────────────────────────\nScopes:  All 9 + compliance\nChecks:  97+ with audits\nFocus:   Regulatory compliance\n         Audit trail required" }
    ],
    multiSelect: false
  },
  {
    question: "What kind of data does this project handle?",
    header: "Data",
    options: [
      { label: "Personal info", description: "Names, emails, addresses — anything identifying" },
      { label: "Sensitive data", description: "Health, financial, biometrics, payment cards" },
      { label: "Auth credentials", description: "Passwords, API keys, tokens, sessions" },
      { label: "No sensitive data", description: "Only public or anonymous data" }
    ],
    multiSelect: true
  }
])
```

#### Call 2: Strategy

```javascript
AskUserQuestion([
  {
    question: "What should CCO focus on improving?",
    header: "Priorities",
    options: [
      { label: "Security (Recommended)", description: "Vulnerabilities, data leaks, hardening" },
      { label: "Code Quality (Recommended)", description: "Types, complexity, dead code" },
      { label: "Architecture", description: "Structure, patterns, module boundaries" },
      { label: "Documentation", description: "README, API docs, developer guides" }
    ],
    multiSelect: true
  },
  {
    question: "What should CCO avoid changing?",
    header: "Constraints",
    options: [
      { label: "Keep framework/language", description: "Don't suggest migrations" },
      { label: "Don't break public APIs", description: "Preserve endpoints, signatures, exports" },
      { label: "No new dependencies", description: "Only use existing packages" },
      { label: "No restrictions", description: "CCO can change anything" }
    ],
    multiSelect: true
  },
  {
    question: "Who uses this project?",
    header: "Audience",
    options: [
      { label: "Public users", description: "Internet-facing — strictest security" },
      { label: "Internal team", description: "Company/org only — standard security" },
      { label: "Other developers", description: "Library/tool consumers — API design matters" },
      { label: "Not decided / local only", description: "Still in development" }
    ],
    multiSelect: false
  }
])
```

Deployment auto-detected from Discovery (Docker/cloud/serverless), written to profile without asking.

#### --auto Mode Defaults

| Question | Default |
|----------|---------|
| Project type | Auto-detected |
| Quality | Production |
| Data | Grep scan for PII/credential patterns |
| Priorities | Security + Code Quality |
| Constraints | Keep framework/language |
| Audience | Auto-detect (Dockerfile → container, .github → cloud, else local) |
| Deployment | Auto-detect from Docker/cloud/serverless signals |

#### Ideal Metrics by Project Type

Per CCO Rules: Project Types — all type IDs standardized.

| Type | Coupling | Cohesion | Complexity | Coverage |
|------|----------|----------|------------|----------|
| cli | <40% | >75% | <10 | 70%+ |
| library | <30% | >80% | <8 | 85%+ |
| api | <50% | >70% | <12 | 80%+ |
| web | <60% | >65% | <15 | 70%+ |
| mobile | <55% | >65% | <12 | 65%+ |
| desktop | <50% | >70% | <12 | 70%+ |
| monorepo | <35% | >70% | <12 | 75%+ |
| iac | <45% | >70% | <10 | 60%+ |
| devtool | <35% | >75% | <10 | 80%+ |
| data | <45% | >70% | <12 | 70%+ |
| ml | <50% | >65% | <15 | 60%+ |
| embedded | <40% | >80% | <8 | 75%+ |
| game | <55% | >60% | <15 | 50%+ |
| extension | <40% | >75% | <10 | 70%+ |

Adjustments: prototype 30% relaxed, mvp 15% relaxed, production standard, enterprise 10% strict. Sensitive data: security weight 25%→35%.

Write profile to CLAUDE.md. If `--init` → stop here. If first-time (not --init/--refresh):

```javascript
AskUserQuestion([{
  question: "Profile created. Continue with assessment and fixes?",
  header: "Continue",
  options: [
    { label: "Continue (Recommended)", description: "Run full assessment now" },
    { label: "Stop here", description: "Profile saved. Run /cco-blueprint again later" }
  ],
  multiSelect: false
}])
```

### Phase 3: Assess [PARALLEL]

Context fields are read from the blueprint profile. This enables stack-specific pattern detection, privacy severity calibration, and quality target alignment.

Per CCO Rules: Parallel Execution, Agent Contract, Model Routing.

| Track | Scopes | Mode | Model |
|-------|--------|------|-------|
| A: Code Quality | security, hygiene, types, simplify, performance, robustness, privacy | auto | haiku |
| B: Architecture | architecture, patterns, cross-cutting, testing, maintainability | review | sonnet |
| C: Production | production-readiness, functional-completeness, ai-architecture | review | sonnet |
| D: Documentation | doc-sync | auto | haiku |
| E: Audit | stack-assessment, dependency-health, dx-quality, project-structure, user-facing-defaults | audit | haiku |

All tracks receive context: {projectType, stack, qualityTarget, dataSensitivity, constraints}.

**Track E: user-facing-defaults** — Per CCO Rules: Project Types. When project type has UI (web, mobile, desktop, game), audit additionally checks:

| Check | Severity if Missing | Details |
|-------|-------------------|---------|
| i18n setup | HIGH | Framework-native message catalog present? (ARB/JSON/PO/xcstrings) |
| Default locales | MEDIUM | At least `en` + owner locale (`tr`) configured? |
| a11y basics | HIGH | Semantic labels on interactive widgets? |
| Responsive layout | MEDIUM | Breakpoints or adaptive layout used? |

If project type has no UI → skip user-facing-defaults entirely.

| Batch | Tracks | Model |
|-------|--------|-------|
| 1 | Track A (Code Quality) + Track B (Architecture) | haiku / sonnet |
| 2 | Track C (Production) + Track D (Documentation) | sonnet / haiku |
| 3 | Track E (Audit) | haiku |

Wait for ALL batches. Phase gate: do not proceed until all 5 tracks return or fail.

Per CCO Rules: CRITICAL Escalation — if any CRITICAL findings, run single opus validation call before proceeding to Phase 3.1.

### Phase 3.1: Project Map

Build from Discovery + Assess results. Generated from directory structure, entry points (package.json main/bin), import/require patterns, dependency files, detected toolchain.

Always displayed (including --auto). Written to profile on first run, updated on subsequent runs.

### Phase 4: Consolidate

Merge all track results, deduplicate by file:line.

**Deduplication rules:**
- Same file:line → merge, keep highest severity
- Same file, same issue within 10 lines → merge
- Contradictory findings → keep higher confidence

#### Dimension Score Aggregation

Each dimension combines multiple scope scores:

| Dimension | Component Scopes | Aggregation |
|-----------|-----------------|-------------|
| Security & Privacy | security (60%), privacy (25%), robustness (15%) | Weighted avg, CRITICAL in any → max 40 |
| Code Quality | hygiene (40%), types (35%), simplify (25%) | Weighted avg |
| Architecture | architecture (35%), patterns (25%), cross-cutting (15%), maintainability (25%) | Weighted avg, worst-case floor: min(components) + 10 |
| Performance | performance (100%) | Direct |
| Resilience | robustness (50%), functional-completeness (50%) | Weighted avg |
| Testing | testing (100%) | Direct |
| Stack Health | stack-assessment (40%), dependency-health (40%), user-facing-defaults (20%) | Weighted avg. If user-facing-defaults N/A (non-UI project) → redistribute to others |
| DX | dx-quality (60%), project-structure (40%) | Weighted avg |
| Documentation | doc-sync (100%) | Direct |

**Overall = sum(dimension_score × dimension_weight)**

Status thresholds:
- ≥ ideal target → OK
- within 15 points of ideal → WARN
- > 15 points below ideal → ALERT

**Worst-case floor for Architecture:** Architecture dimension never drops more than 10 below its worst component. This prevents a single weak sub-area from tanking the entire dimension when other areas are strong.

#### Weight Matrix by Project Type

Per CCO Rules: Project Types — all type IDs standardized.

| Dimension | cli | library | api | web | mobile | desktop | monorepo | iac | devtool | data | ml | embedded | game | extension | Default |
|-----------|-----|---------|-----|-----|--------|---------|----------|-----|---------|------|----|---------|----|-----------|---------|
| Security & Privacy | 15% | 12% | 22% | 18% | 20% | 15% | 18%* | 20% | 12% | 18% | 15% | 12% | 10% | 15% | 18% |
| Code Quality | 15% | 18% | 12% | 14% | 14% | 15% | 14% | 10% | 18% | 14% | 12% | 18% | 12% | 16% | 14% |
| Architecture | 10% | 16% | 14% | 14% | 14% | 12% | 18% | 8% | 14% | 12% | 10% | 10% | 14% | 12% | 14% |
| Performance | 8% | 8% | 14% | 12% | 14% | 12% | 10% | 5% | 8% | 16% | 18% | 20% | 22% | 8% | 10% |
| Resilience | 12% | 8% | 12% | 10% | 12% | 14% | 10% | 15% | 10% | 14% | 12% | 18% | 10% | 10% | 10% |
| Testing | 10% | 16% | 10% | 10% | 8% | 10% | 10% | 12% | 14% | 10% | 15% | 10% | 8% | 14% | 10% |
| Stack Health | 8% | 8% | 6% | 8% | 8% | 8% | 8% | 10% | 10% | 6% | 8% | 5% | 8% | 10% | 10% |
| DX | 12% | 8% | 5% | 7% | 5% | 7% | 7% | 12% | 8% | 5% | 5% | 4% | 8% | 8% | 7% |
| Documentation | 10% | 6% | 5% | 7% | 5% | 7% | 5% | 8% | 6% | 5% | 5% | 3% | 8% | 7% | 7% |

*Monorepo: weights are weighted average based on sub-package project types.

**Modifiers:**
- Sensitive data: Security & Privacy +10%, others decrease proportionally
- Enterprise quality: Testing +5%, Architecture +3%, others decrease proportionally
- Prototype quality: All dimensions equal weight (11.1% each)

#### Score Calibration Checks

After calculating all scores, verify calibration:

| Check | Expected | Action if Failed |
|-------|----------|-----------------|
| Overall range | 20-95 for real projects | If <20 or >95, re-examine — likely miscalculation |
| No dimension at 100 | Unless 0 findings in that scope | 100 = nothing to improve, suspicious for large codebases |
| CRITICAL consistency | Any CRITICAL → overall < 80 | If overall ≥ 80 with CRITICAL findings, weights are wrong |
| Delta sanity | Score change between runs < 30 per dimension | If > 30 change, either major refactor occurred or scoring drifted |
| Cross-dimension coherence | High architecture + Low code quality = suspicious | Flag if gap between related dimensions > 40 points |

If calibration fails, add a note in the summary: "Score calibration note: {explanation}".

Prioritize 80/20: Quick Win → Moderate → Complex → Major.

### Phase 5: Plan Review [findings > 0, SKIP if --auto]

Display blueprint dashboard: project info, health scores table (Current/Target/Gap/Status), findings summary with quick wins.

Per CCO Rules: Plan Review Protocol — display findings, ask with markdown previews. Blueprint-specific options: Fix All (recommended) / Critical+High only / Quick wins only / Report Only.

### Phase 6: Apply [SKIP if --preview]

Send findings to cco-agent-apply (scope: fix, findings: [...], fixAll: --auto) in priority order: CRITICAL/security → Code quality → Architecture → Documentation. Per CCO Rules: on error, count as failed, continue.

### Phase 6.1: Needs-Approval Review [CONDITIONAL, SKIP if --auto, AUTO-APPLY if --force-approve]

Per CCO Rules: Needs-Approval Protocol.

### Phase 7: Update Profile

Update CLAUDE.md blueprint section with new Current Scores.

#### Score History (Optional)

If profile already has Current Scores, calculate and display delta:

| Dimension | Previous | Current | Delta | Trend |
|-----------|----------|---------|-------|-------|
| Security  | 85       | 90      | +5    | ↑     |
| ...       |          |         |       |       |

Trend symbols: ↑ improved (delta > +3), → stable (-3 to +3), ↓ regressed (delta < -3)

Store only current scores in profile (not history — that's git's job). Delta is calculated by comparing against the scores found during Discovery.

### Phase 7.1: Memory Cleanup [SKIP if --preview]

Clean up Claude Code auto-memory files: `{user home}/.claude/projects/{project-hash}/memory/`

1. Read `MEMORY.md` and topic files
2. Cross-reference entries against current project state:

| Check | Stale Signal | Action |
|-------|-------------|--------|
| File references | File/dir no longer exists (Glob) | Remove entry |
| Build/test commands | Command not in package.json/Makefile (Discovery) | Update or remove |
| Pattern notes | Contradicts current architecture (Project Map) | Update |
| Debugging notes | References fixed issues (Assess findings) | Remove |
| Dependency info | Version/package changed or removed (Discovery) | Update |
| Duplicate entries | Same info in MEMORY.md and topic file | Consolidate |

3. Keep MEMORY.md within 200-line budget (Claude Code startup limit). Move detail to topic files.
4. Remove orphan topic files not referenced from MEMORY.md

In --auto: silent cleanup. Interactive: confirm if >5 entries removed. Partial cleanup acceptable.

### Phase 8: Summary

Per CCO Rules: Accounting, Auto Mode.

Before/After delta table (9 dimensions), accounting (applied/failed/needs_approval/total), next steps.

Next: `/cco-blueprint --preview` (check progress) | `/cco-optimize` (fix issues) | `/cco-align` (fix structure)

--auto: `cco-blueprint: {OK|WARN|FAIL} | Health: {before}→{after}/{target} | Applied: {n} | Failed: {n} | Needs Approval: {n} | Total: {n}`

Status: OK (overall >= target), WARN (gap exists but progress), FAIL (CRITICAL unfixed or regression).

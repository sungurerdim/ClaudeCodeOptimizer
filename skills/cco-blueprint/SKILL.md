---
description: Project health system - profile-based assessment, transformation, and progress tracking via CLAUDE.md
argument-hint: "[--auto] [--preview] [--init] [--refresh] [--scope=<name>]"
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

## Context

- Git status: !`git status --short 2>/dev/null | cat`
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
| 3.5 | Project Map | No |
| 4 | Consolidate | No |
| 5 | Plan Review | Yes (--auto) |
| 6 | Apply | Yes (--preview) |
| 6.5 | Needs-Approval Review | Yes (--auto) |
| 7 | Update Profile | No |
| 7.5 | Memory Cleanup | Yes (--preview) |
| 8 | Summary | No |

Before reporting completion, verify every non-skipped phase produced output.

## Execution Flow

Discovery → [Init Flow] → Assess [PARALLEL] → Consolidate → Plan → [Apply] → Update Profile → Summary

### Phase 1: Discovery [PARALLEL]

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

```javascript
AskUserQuestion([
  {
    question: "What category best describes this project?",
    header: "Project Type",
    options: [
      { label: "{Detected type} (Detected)", description: "Auto-detected from project structure" },
      { label: "Frontend", description: "Web apps, mobile apps, desktop apps" },
      { label: "Developer Tool", description: "CLIs, libraries, SDKs, plugins, extensions" },
      { label: "Infrastructure", description: "IaC, CI/CD configs, deployment scripts" }
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

#### Ideal Metrics by Project Type

| Type | Coupling | Cohesion | Complexity | Coverage |
|------|----------|----------|------------|----------|
| CLI | <40% | >75% | <10 | 70%+ |
| Library | <30% | >80% | <8 | 85%+ |
| API | <50% | >70% | <12 | 80%+ |
| Web | <60% | >65% | <15 | 70%+ |
| Monorepo | <35% | >70% | <12 | 75%+ |
| Mobile | <55% | >65% | <12 | 65%+ |
| Infra/IaC | <45% | >70% | <10 | 60%+ |

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

| Track | Agent Call |
|-------|-----------|
| A: Code Quality | cco-agent-analyze: security, hygiene, types, simplify, performance, robustness, privacy (mode: auto, context: {projectType, stack, qualityTarget, dataSensitivity, constraints}) |
| B: Architecture | cco-agent-analyze: architecture, patterns, testing, maintainability (mode: review, context: {projectType, stack, qualityTarget, dataSensitivity, constraints}) |
| C: Production | cco-agent-analyze: production-readiness (mode: review, context: {projectType, stack, qualityTarget, dataSensitivity, constraints}) |
| D: Documentation | cco-agent-analyze: doc-sync (mode: auto) |
| E: Audit | cco-agent-analyze: stack-assessment, dependency-health, dx-quality, project-structure (mode: audit) |

Context fields are read from the blueprint profile. This enables stack-specific pattern detection, privacy severity calibration, and quality target alignment.

**Agent invocation:** Launch ALL 5 tracks as Task calls in a SINGLE message WITHOUT `run_in_background`. This executes them in parallel and returns results directly. Do NOT use `run_in_background` for Task calls — it causes empty output files and late completion notifications. Wait for ALL agent results before proceeding to Phase 3.5.

All tracks run with `--preview`. Per CCO Rules: Agent Error Handling — validate agent JSON output, retry once on malformed response, on second failure continue with remaining groups, score failed dimensions as N/A.

**Phase gate:** Do NOT proceed to Phase 3.5/4 until all 5 agent tracks have returned results or failed. Verify each track produced output before consolidation.

### Phase 3.5: Project Map

Build from Discovery + Assess results. Generated from directory structure, entry points (package.json main/bin), import/require patterns, dependency files, detected toolchain.

Always displayed (including --auto). Written to profile on first run, updated on subsequent runs.

### Phase 4: Consolidate

Merge all track results, deduplicate by file:line.

**Deduplication rules:**
- Same file:line → merge, keep highest severity
- Same file, same issue within 10 lines → merge
- Contradictory findings → keep higher confidence

Calculate health scores:

| Dimension | Weight | Source |
|-----------|--------|--------|
| Security & Privacy | 18%* | optimize: security + privacy |
| Code Quality | 14% | optimize: hygiene + types + simplify |
| Architecture | 14% | align: architecture + patterns + maintainability |
| Performance | 10% | optimize: performance |
| Resilience | 10% | optimize: robustness + align: functional-completeness |
| Testing | 10% | align: testing |
| Stack Health | 10% | audit: stack-assessment + dependency-health |
| DX | 7% | audit: dx-quality + project-structure |
| Documentation | 7% | docs results |

*Sensitive data profiles: Security & Privacy increases to 28%, others decrease proportionally.

Prioritize 80/20: Quick Win → Moderate → Complex → Major.

### Phase 5: Plan Review [findings > 0, SKIP if --auto]

Display blueprint dashboard: project info, health scores table (Current/Target/Gap/Status), findings summary with quick wins. Then ask with markdown previews showing scope per option:

```javascript
AskUserQuestion([{
  question: "{totalFindings} findings. How would you like to proceed?",
  header: "Action",
  options: [
    { label: "Fix All (Recommended)", description: "Apply all fixable findings",
      markdown: "{dashboard + full findings table}" },
    { label: "Critical+High only", description: "Fix only CRITICAL and HIGH severity",
      markdown: "{filtered findings table: CRITICAL + HIGH only}" },
    { label: "Quick wins only", description: "Apply only low-effort high-impact fixes",
      markdown: "{filtered findings table: quick wins only}" },
    { label: "Report Only", description: "No fixes, scores saved to profile" }
  ],
  multiSelect: false
}])
```

### Phase 6: Apply [SKIP if --preview]

Send findings to cco-agent-apply (scope: fix, findings: [...], fixAll: --auto) in priority order: CRITICAL/security → Code quality → Architecture → Documentation. Per CCO Rules: on error, count as failed, continue.

### Phase 6.5: Needs-Approval Review [CONDITIONAL, SKIP if --auto]

**Phase gate:** After Phase 6 completes, count needs_approval items. If needs_approval = 0, skip to Phase 7.

If needs_approval > 0, display items table (ID, severity, issue, location, reason), then ALWAYS use AskUserQuestion:

```javascript
AskUserQuestion([{
  question: "There are items that need your approval. How would you like to proceed?",
  header: "Approval",
  options: [
    { label: "Fix All (Recommended)", description: "Apply all needs-approval items" },
    { label: "Review Each", description: "Review and decide on each item individually" },
    { label: "Skip All", description: "Leave needs-approval items unfixed" }
  ],
  multiSelect: false
}])
```

### Phase 7: Update Profile

Update CLAUDE.md blueprint section with new Current Scores.

### Phase 7.5: Memory Cleanup [SKIP if --preview]

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

Per CCO Rules: Accounting — applied + failed + needs_approval = total. No "declined" category. Auto Mode — no questions, no deferrals, fix everything except large architectural changes.

Before/After delta table (9 dimensions), accounting (applied/failed/needs_approval/total), next steps.

Next: `/cco-blueprint --preview` (check progress) | `/cco-optimize` (fix issues) | `/cco-align` (fix structure)

--auto: `cco-blueprint: {OK|WARN|FAIL} | Health: {before}→{after}/{target} | Applied: {n} | Failed: {n} | Total: {n}`

Status: OK (overall >= target), WARN (gap exists but progress), FAIL (CRITICAL unfixed or regression).

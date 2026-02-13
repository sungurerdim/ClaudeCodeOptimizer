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

- Git status: !`git status --short 2>/dev/null || echo ""`
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
| Security | {n} | {OK/WARN} |
| Code Quality | {n} | {OK/WARN} |
| Architecture | {n} | {OK/WARN} |
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
      { label: "Prototype", description: "Minimal checks" },
      { label: "MVP", description: "Ship fast with basics covered" },
      { label: "Production (Recommended)", description: "Full quality gates" },
      { label: "Enterprise", description: "Compliance and audits required" }
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
| A: Code Quality | cco-agent-analyze: security, hygiene, types, simplify, performance, robustness, privacy (mode: auto) |
| B: Architecture | cco-agent-analyze: architecture, patterns, testing, maintainability (mode: auto) |
| C: Documentation | cco-agent-analyze: doc-sync (mode: auto) |
| D: Audit | cco-agent-analyze: stack-assessment, dependency-health, dx-quality, project-structure (mode: audit) |

All tracks run with `--preview`. Per CCO Rules: Agent Error Handling.

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
| Security | 25%* | security + privacy + robustness |
| Code Quality | 20% | hygiene + types + simplify + performance |
| Architecture | 20% | architecture + patterns + maintainability |
| Stack Health | 15% | stack-assessment + dependency-health |
| DX | 10% | dx-quality + project-structure |
| Documentation | 10% | doc-sync |

*Sensitive data profiles: Security → 35%, others decrease proportionally.

Prioritize 80/20: Quick Win → Moderate → Complex → Major.

### Phase 5: Plan Review [findings > 0, SKIP if --auto]

Display blueprint dashboard: project info, health scores table (Current/Target/Gap/Status), findings summary with quick wins. Action options: Fix all (recommended) / Critical+high only / Quick wins only / Report only.

### Phase 6: Apply [SKIP if --preview]

Send findings to cco-agent-apply in priority order: CRITICAL/security → Code quality → Architecture → Documentation. Per CCO Rules: on error, count as failed, continue.

### Phase 6.5: Needs-Approval Review [CONDITIONAL, SKIP if --auto]

Per CCO Rules: if needs_approval > 0, display items table and ask Fix All / Review Each.

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

Per CCO Rules: Accounting, Auto Mode.

Before/After delta table, accounting (applied/failed/needs_approval/total), next steps.

--auto: `cco-blueprint: {OK|WARN|FAIL} | Health: {before}→{after}/{target} | Applied: {n} | Failed: {n} | Total: {n}`

Status: OK (overall >= target), WARN (gap exists but progress), FAIL (CRITICAL unfixed or regression).

---
description: Project health system - profile-based assessment, transformation, and progress tracking via CLAUDE.md
argument-hint: "[--auto] [--preview] [--init] [--refresh] [--scope=<name>]"
allowed-tools: Read, Grep, Glob, Edit, Bash, Task, Skill, AskUserQuestion
model: opus
---

# /cco-blueprint

**Project Health System** — Profile-based assessment, transformation, and progress tracking.

**Philosophy:** One command to assess, transform, and track any project. Profile in CLAUDE.md ensures context persists across sessions.

## Flags

| Flag | Effect |
|------|--------|
| `--auto` | All phases, no questions, single-line summary |
| `--preview` | Analyze + dashboard, no changes |
| `--init` | Profile creation/refresh only (no analysis) |
| `--refresh` | Re-scan profile (run history and decisions preserved) |
| `--scope=X` | Specific area: stack, deps, dx, structure, code, architecture, docs, memory, all |

## Context

- Git status: !`git status --short 2>/dev/null || echo ""`
- Args: $ARGS

## CLAUDE.md Profile Format

Profile is stored between markers in CLAUDE.md. Content outside markers is never modified.

```markdown
<!-- cco-blueprint-start -->
## CCO Blueprint Profile

**Project:** {name} | **Type:** {type} | **Stack:** {stack} | **Target:** {quality}

### Config
- **Priorities:** {priority1}, {priority2}
- **Constraints:** {constraint1}, {constraint2}
- **Data:** {data types} | **Regulations:** {if applicable}
- **Audience:** {audience} | **Deploy:** {deploy method}

### Project Map
```
Entry: {entry point} → {framework}
Modules: {module flow}
External: {external dependencies}
Toolchain: {tools} | {CI} | {container}
```

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

### Run History
- {date}: Applied {n} | Failed {n} | Overall {before}→{after}

### Decisions
- {ID}: SKIP "{description}" ({reason})
<!-- cco-blueprint-end -->
```

**Profile read/write rules:**
- Parse content between `<!-- cco-blueprint-start -->` and `<!-- cco-blueprint-end -->`
- If CLAUDE.md does not exist, create it with profile section only
- If CLAUDE.md exists, update only the profile section (preserve all other content)

## Execution Flow

Discovery → [Init Flow] → Assess [PARALLEL] → Consolidate → Plan → [Apply] → Update Profile → Summary

### Phase 0: Prerequisites

Verify `git` is available (`git --version`). If missing → warn: "Git not found. Some features (git status, commit history) will be limited." Continue with reduced functionality.

### Phase 1: Discovery [PARALLEL]

1. Search CLAUDE.md for `<!-- cco-blueprint-start -->`
2. Parallel project detection (Glob/Grep/Read):

| Signal | Detection |
|--------|-----------|
| Language | Glob `**/*.{ts,js,py,go,rs,java,rb,cs}` → majority |
| Framework | Grep: express, fastapi, react, next, django, flask, gin, actix |
| Project type | routes/ → API, pages/ → Web, bin/ → CLI, src/lib/ → Library |
| Toolchain | Glob: .eslintrc*, tsconfig.json, .prettierrc*, mypy.ini, biome.json |
| CI/CD | Glob: .github/workflows/*.yml, .gitlab-ci.yml, Jenkinsfile |
| Docker | Glob: Dockerfile*, docker-compose*, compose.y*ml |
| Tests | Glob: **/*.test.*, **/*.spec.*, **/test_*.py |
| Data sensitivity | Grep: password, email, credit_card, ssn, token patterns |
| Git | `git status --short`, `git log --oneline -5` |

**Decision tree:**
1. Profile exists AND not --init/--refresh → Phase 3 (incremental mode)
2. Profile exists AND --refresh → Phase 2 (re-ask questions, preserve history/decisions)
3. No profile AND --init → Phase 2 (create profile, stop after)
4. No profile AND not --init → Phase 2 (create profile, continue to Phase 3)

On error: If CLAUDE.md is unreadable or corrupt, create fresh profile. Log warning.

### Phase 2: Init Flow [no profile OR --init/--refresh]

Two AskUserQuestion calls (6 questions total). All questions in English. Detection results marked "(Detected)" in relevant option.

#### Call 1: Project Identity (3 questions)

```javascript
AskUserQuestion([
  {
    question: "What category best describes this project?",
    header: "Project Type",
    options: [
      { label: "{Detected type} (Detected)", description: "Auto-detected from project structure" },
      { label: "Frontend", description: "Web apps, mobile apps, desktop apps (React, Flutter, Electron, etc.)" },
      { label: "Developer Tool", description: "CLIs, libraries, SDKs, plugins, extensions, frameworks" },
      { label: "Infrastructure", description: "IaC (Terraform/Pulumi), CI/CD configs, deployment scripts, DevOps" }
    ],
    multiSelect: false
  },
  {
    question: "What quality level should this project meet?",
    header: "Quality",
    options: [
      { label: "Prototype", description: "Experimenting with ideas, might throw away. Minimal checks." },
      { label: "MVP", description: "Ship fast with basics covered. Good enough, not perfect." },
      { label: "Production (Recommended)", description: "Real users depend on this. Full quality gates." },
      { label: "Enterprise", description: "Compliance and audits required. Strictest checks." }
    ],
    multiSelect: false
  },
  {
    question: "What kind of data does this project handle?",
    header: "Data",
    options: [
      { label: "Personal info", description: "Names, emails, phone numbers, addresses — anything identifying a person" },
      { label: "Sensitive data", description: "Health records, financial data, biometrics, payment cards" },
      { label: "Auth credentials", description: "Passwords, API keys, tokens, session data" },
      { label: "No sensitive data", description: "Only public or anonymous data, nothing private" }
    ],
    multiSelect: true
  }
])
```

The first option's label for Q1 is dynamically set based on Discovery results. If detection is ambiguous, no option gets "(Detected)" tag.

#### Call 2: Strategy (3 questions)

```javascript
AskUserQuestion([
  {
    question: "What should CCO focus on improving?",
    header: "Priorities",
    options: [
      { label: "Security (Recommended)", description: "Find vulnerabilities, fix data leak risks, harden defenses" },
      { label: "Code Quality (Recommended)", description: "Clean up code, add types, reduce complexity, remove dead code" },
      { label: "Architecture", description: "Improve project structure, design patterns, module boundaries" },
      { label: "Documentation", description: "Fill gaps in README, API docs, developer guides" }
    ],
    multiSelect: true
  },
  {
    question: "What should CCO avoid changing?",
    header: "Constraints",
    options: [
      { label: "Keep framework/language", description: "Don't suggest migrating to a different framework or language" },
      { label: "Don't break public APIs", description: "Preserve all existing endpoints, function signatures, exports" },
      { label: "No new dependencies", description: "Only use packages already in the project" },
      { label: "No restrictions", description: "CCO can change anything for the best result" }
    ],
    multiSelect: true
  },
  {
    question: "Who uses this project?",
    header: "Audience",
    options: [
      { label: "Public users", description: "Anyone on the internet can access it — strictest security needed" },
      { label: "Internal team", description: "Only people in your company/org use it — standard security" },
      { label: "Other developers", description: "A library or tool other devs consume — API design and docs matter most" },
      { label: "Not decided / local only", description: "Still in development, not deployed anywhere yet" }
    ],
    multiSelect: false
  }
])
```

Deployment detail (Docker/cloud/serverless) is auto-detected from Discovery and written to profile without asking.

#### --auto Mode Defaults

| Question | Default |
|----------|---------|
| Q1 Project type | Auto-detected from Discovery |
| Q2 Quality | Production |
| Q3 Data | Grep scan for PII/credential patterns in code |
| Q4 Priorities | Security + Code Quality |
| Q5 Constraints | Keep framework/language |
| Q6 Audience | Auto-detect (Dockerfile → container, .github → cloud, else local) |

#### Ideal Metrics Calculation

After questions, calculate ideal metrics by project type:

| Type | Coupling | Cohesion | Complexity | Coverage |
|------|----------|----------|------------|----------|
| CLI | <40% | >75% | <10 | 70%+ |
| Library | <30% | >80% | <8 | 85%+ |
| API | <50% | >70% | <12 | 80%+ |
| Web | <60% | >65% | <15 | 70%+ |
| Monorepo | <35% | >70% | <12 | 75%+ |
| Mobile | <55% | >65% | <12 | 65%+ |
| Infra/IaC | <45% | >70% | <10 | 60%+ |

Quality target adjustment: prototype 30% relaxed, mvp 15% relaxed, production standard, enterprise 10% strict.

Sensitive data handling: security weight 25%→35%, privacy scope escalates to CRITICAL.

Write profile to CLAUDE.md. If `--init`, stop here.

On error: If CLAUDE.md write fails, display profile in output and instruct user to add manually.

### Phase 3: Assess [PARALLEL]

Incremental logic: skip tracks where current score >= ideal target (5% tolerance).

| Track | Tool | Condition |
|-------|------|-----------|
| A: Code Quality | `Skill("cco-optimize", "--auto --preview")` | code score < ideal |
| B: Architecture | `Skill("cco-align", "--auto --preview")` | architecture score < ideal |
| C: Documentation | `Skill("cco-docs", "--auto --preview")` | docs score < ideal |
| D: Audit | `Task(cco-agent-analyze, {scopes: audit scopes, mode: "audit"})` | stack/dx score < ideal |

All tracks run with `--preview`: analyze only, no changes applied.

Profile SKIP decisions filter out matching finding IDs from results.

On error: If a track fails, log error, continue with remaining tracks. Score that dimension as "N/A".

### Phase 3.5: Project Map [PARALLEL with Phase 3 consolidation]

Build bird's-eye view from Discovery data + Assess results:

```
PROJECT MAP
===========
{name} ({stack}) | {n} files | {n} LOC

Entry: {entry point} → {framework}

Modules:
  {dir}/     → {role} ({submodules})
  ...

Data Flow:
  {flow description}

External:
  {external deps list}

Toolchain:
  {formatter} + {linter} + {compiler} + {test runner} | {CI} | {container}
```

**Generation method:** From Phase 1 Discovery Glob/Grep/Read results:
- Directory structure: `ls` + Glob for main directories and roles
- Entry point: package.json main/bin or framework convention
- Module relationships: Grep import/require patterns
- External dependencies: package.json/pyproject.toml dependencies
- Toolchain: already detected in Discovery

Project Map is always displayed (including --auto). Written to profile on first run, updated on subsequent runs if changed.

### Phase 4: Consolidate

1. Merge all track results, deduplicate by file:line
2. Calculate health scores:

| Dimension | Weight | Source |
|-----------|--------|--------|
| Security | 25%* | optimize: security + privacy + robustness |
| Code Quality | 20% | optimize: hygiene + types + simplify + performance |
| Architecture | 20% | align: architecture + patterns + maintainability |
| Stack Health | 15% | audit: stack-assessment + dependency-health |
| DX | 10% | audit: dx-quality + project-structure |
| Documentation | 10% | docs results |

*Sensitive data profiles: Security increases to 35%, other weights decrease proportionally.

3. Prioritize 80/20: Quick Win → Moderate → Complex → Major

On error: If scoring data is incomplete, use available dimensions only. Note missing dimensions.

### Phase 5: Plan Review [findings > 0, SKIP if --auto]

```
PROJECT BLUEPRINT
=================
Project: {name} ({type}) | {stack} | Health: {score}/100 ({grade})

--- Project Map ---
Entry: {entry} → {framework}
Modules: {module summary}
External: {external deps}
Toolchain: {toolchain summary}

--- Health Scores ---
| Dimension       | Current | Target | Gap | Status |
|-----------------|---------|--------|-----|--------|
| Security        |   {n}   |  {n}   | {n} |  {st}  |
| Code Quality    |   {n}   |  {n}   | {n} |  {st}  |
| Architecture    |   {n}   |  {n}   | {n} |  {st}  |
| Stack Health    |   {n}   |  {n}   | {n} |  {st}  |
| DX              |   {n}   |  {n}   | {n} |  {st}  |
| Documentation   |   {n}   |  {n}   | {n} |  {st}  |
| Overall         |   {n}   |  {n}   | {n} |  {st}  |

--- Findings ---
Total: {n} | Auto-fixable: {n} | Needs approval: {n}

Quick Wins:
  [{severity}] {id}: {title} in {file}:{line}
  ...
```

```javascript
AskUserQuestion([{
  question: "How should we proceed?",
  header: "Action",
  options: [
    { label: "Fix all (Recommended)", description: "Auto-fix everything possible, ask for approval items separately" },
    { label: "Critical and high only", description: "Fix only CRITICAL and HIGH severity issues" },
    { label: "Quick wins only", description: "Least effort, most improvement" },
    { label: "Report only", description: "Don't change anything, just show results" }
  ],
  multiSelect: false
}])
```

### Phase 6: Apply [SKIP if --preview]

Apply in order:
1. CRITICAL/security: `Skill("cco-optimize", "--auto --scope=security,privacy,robustness")`
2. Code quality: `Skill("cco-optimize", "--auto --scope=hygiene,types,simplify,performance")`
3. Architecture: `Skill("cco-align", "--auto")`
4. Documentation: `Skill("cco-docs", "--auto")`

Profile constraints are passed as context to each Skill call.

On error: If a Skill call fails, log error with details, continue with next. Count as failed in accounting.

### Phase 6.5: Needs-Approval Review [CONDITIONAL, SKIP if --auto]

Per CCO Rules: Needs-Approval Flow. SKIP items are recorded in profile Decisions section.

### Phase 7: Update Profile

Update CLAUDE.md blueprint section:
- Current Scores → new scores
- Run History → append new line (`{date}: Applied {n} | Failed {n} | Overall {before}→{after}`)
- Decisions → append new SKIP decisions

On error: If CLAUDE.md update fails, display updated profile in output.

### Phase 7.5: Memory Cleanup [SKIP if --preview]

Clean up Claude Code auto-memory files using the full project context from Discovery + Assess.

**Target directory:** `~/.claude/projects/<project>/memory/` (derived from git root)

**Steps:**
1. Read `MEMORY.md` and all topic files in the memory directory
2. Cross-reference entries against current project state:

| Check | Stale Signal | Action |
|-------|-------------|--------|
| File references | Referenced file/dir no longer exists (checked via Glob) | Remove entry |
| Build/test commands | Command no longer in package.json/Makefile/scripts (from Discovery) | Update or remove |
| Pattern notes | Contradicts current architecture (from Project Map) | Update to match current state |
| Debugging notes | References issues that are now fixed (from Assess findings) | Remove |
| Dependency info | Version/package changed or removed (from Discovery) | Update |
| Duplicate entries | Same info in MEMORY.md and topic file, or repeated across topics | Consolidate |

3. Ensure MEMORY.md stays within 200-line budget (Claude Code only loads first 200 lines at startup). Move detailed content to topic files if needed.
4. Remove orphan topic files not referenced from MEMORY.md
5. Report cleanup results in summary

**In --auto mode:** Apply all cleanup silently. In interactive mode: show planned changes, ask confirmation if >5 entries would be removed.

On error: If memory directory doesn't exist or is empty, skip silently (auto-memory may not be enabled).

### Phase 8: Summary

```
BLUEPRINT COMPLETE
==================
Before → After:
| Dimension | Before | After | Delta |
|-----------|--------|-------|-------|
| Overall   |  {n}   |  {n}  |  {±n} |
...

Accounting: Applied: {n} | Failed: {n} | Needs Approval: {n} | Total: {n}

Next: /cco-blueprint --preview (check progress)
      /cco-blueprint (close remaining gaps)
```

--auto mode: `cco-blueprint: {OK|WARN|FAIL} | Health: {before}→{after}/{target} | Applied: {n} | Failed: {n} | Total: {n}`

Status: OK (overall >= target), WARN (gap exists but progress made), FAIL (CRITICAL unfixed or regression).

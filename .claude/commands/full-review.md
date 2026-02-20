---
description: CCO system health check (~78 checks across 8 categories)
argument-hint: [--auto] [--quick] [--focus=X] [--preview] [--fix]
allowed-tools: Read(*), Grep(*), Glob(*), Bash(*), Task(*), AskUserQuestion, Edit(*)
---

# /full-review

**CCO Self-Review** — Comprehensive analysis of CCO system against its documented design principles.

> **Internal Command:** This is in `.claude/commands/` (not `skills/`), used for CCO development only.

## Args

- `--auto`: Fully unattended mode — no questions, fix everything, single-line summary
- `--quick`: CRITICAL and HIGH only, skip MEDIUM/LOW
- `--focus=X`: Single category (1-8 or name)
- `--preview`: Report only, no fixes applied
- `--fix`: Auto-apply safe fixes (doc count updates, terminology)

## Context Detection

At start, verify CCO repo using Claude's native tools:

| Context | Detection Method |
|---------|------------------|
| CCO repo root | `git rev-parse --show-toplevel` |
| Is CCO repo | Glob for `rules/cco-rules.md` → Read and check frontmatter `cco_version` |
| Args | $ARGS |

**Use Glob/Read for file detection. Git commands are cross-platform.**

## Context Check [CRITICAL]

If not in CCO repository root:
```
Not in CCO repository root.
Run this command from the ClaudeCodeOptimizer directory.
```
**Stop immediately.**

## Architecture

| Step | Name | Action |
|------|------|--------|
| 1 | Setup | Q1: Review mode selection |
| 2 | Inventory | Detect counts via Glob |
| 3 | Analyze | 4 Explore agent groups (parallel) |
| 4 | Prioritize | 80/20 findings |
| 5 | Approval | Q2: Select fixes (conditional) |
| 6 | Apply | Delegate to cco-agent-apply |
| 7 | Summary | Show report |

---

## Step-1: Setup [SKIP IF --auto or --preview]

```javascript
if (!isUnattended && !isReportOnly) {
  AskUserQuestion([{
    question: "How should this review proceed?",
    header: "Review mode",
    options: [
      { label: "Report only", description: "Analyze and show findings, no changes" },
      { label: "Fix safe (Recommended)", description: "Auto-fix doc counts, terminology" },
      { label: "Fix all", description: "Fix everything including manual items" }
    ],
    multiSelect: false
  }])
}
```

---

## Step-2: Inventory Detection

```javascript
// Cross-platform detection using Claude's native tools — all counts are dynamic
skills    = Glob("skills/cco-*/SKILL.md").length
agents    = Glob("agents/cco-agent-*.md").length
docs      = Glob("docs/*.md").length
workflows = Glob(".github/workflows/*.yml").length
version   = Read("rules/cco-rules.md").frontmatter.cco_version

inventory = { skills, agents, docs, workflows, version }
```

**Note:** Rules are in `rules/cco-rules.md` (single source of truth). Never hardcode expected counts — always detect dynamically and compare across reference files.

---

## Step-3: 8-Category Analysis [PARALLEL AGENTS]

Launch 4 parallel Explore agents covering 8 categories:

### Group A: Inventory & Release (Cat 1 + Cat 8)

**CATEGORY 1 — Inventory & Sync (10 checks):**
- Count files via Glob: skills/cco-*/SKILL.md, agents/cco-agent-*.md, docs/*.md, .github/workflows/*.yml
- Compare counts against README.md, docs/skills.md, docs/agents.md — flag mismatches
- Orphan refs: grep for removed paths (`.cco/`, `principles.md`, `projects.json`)
- Terminology consistency: CRITICAL/HIGH/MEDIUM/LOW (not P0/P1)
- CLAUDE.md blueprint markers present and valid (`cco-blueprint-start`/`cco-blueprint-end`)
- version.txt exists and matches rules/cco-rules.md frontmatter

**CATEGORY 8 — Release Readiness (8 checks):**
- rules/cco-rules.md exists with valid frontmatter (cco_version, description)
- Version: cco-rules.md frontmatter = version.txt
- Go installer builds: extras/installer/ has main.go
- Cross-platform: no OS-specific paths in skills/agents (C:\, /home/, /Users/)
- Install one-liner documented in README for macOS/Linux/Windows
- GitHub workflows present: ci.yml, release.yml
- Legacy cleanup logic in installer (removes prior version artifacts)
- Uninstall mechanism available and documented

### Group B: Skill & Agent Quality + Architecture (Cat 2 + Cat 3)

**CATEGORY 2 — Skill & Agent Quality (12 checks):**
- Each skill has valid YAML frontmatter (description, allowed-tools)
- AskUserQuestion limits: max 4 questions × 4 options per invocation
- --auto mode: zero AskUserQuestion calls in flow
- --preview mode: zero Edit/Write calls in flow
- Skills with disable-model-invocation: 2 (blueprint, update)
- Agent scopes: analyze 9 Optimize + 8 Review + 4 Audit = 21 total
- cco-agent-apply: fix scope + docs scope
- cco-agent-research: 6 scopes (local, search, analyze, synthesize, full, dependency)
- Agent output: JSON with findings[], scores, metrics, error
- Model selection: analyze/research = haiku, apply = inherits session model
- All skills support --auto and --preview where applicable
- No skill references non-existent files or paths

**CATEGORY 3 — Architecture Compliance (10 checks):**
- All CCO files reside in ~/.claude/ (no project-local files except CLAUDE.md blueprint)
- Zero deps outside Claude Code (no node/python/pip in skills/agents)
- git and gh are only external tool dependencies
- Uses Claude Code native loading (rules/, skills/, agents/)
- No hardcoded OS paths (C:\, /home/, /Users/) in skills or agents
- Context commands: no pipes or complex substitutions (Windows compat)
- No file/log/trace/debug output except CLAUDE.md blueprint
- No backward-compatibility shims, renamed `_vars`, or re-exports
- Skills read files before editing (Read-First pattern)
- Plan phase present before complex changes (Plan-Before-Act)

### Group C: AI Communication + Efficiency (Cat 4 + Cat 5)

**CATEGORY 4 — AI Communication (8 checks):**
- No teaching AI basics (AI already knows how to code/test/review)
- Rules specify WHAT not HOW (leave implementation to AI)
- Process assurance patterns are legitimate (quality gates, agent contracts)
- No unnecessary repetition across files (rules ↔ skills ↔ agents)
- Each rule provides unique CCO-specific value
- Positive impact: doesn't constrain AI's natural capabilities
- Weakness completion: addresses known AI weak points (focus, step-skipping)
- Model compatibility: core structure is model-agnostic

**CATEGORY 5 — Efficiency & Density (10 checks):**
- Tables for tabular data (not prose paragraphs)
- No redundancy across files (shared patterns → CCO Rules reference)
- Concrete benefit test: "What do we lose without this?" — if no answer, flag
- AskUserQuestion limits respected in all skills
- No teaching of basics Claude already knows
- Large files >500 lines flagged
- Context commands minimal (no redundant Glob/Read calls)
- No single-use abstractions or wrappers
- No design for hypothetical future requirements
- Token-efficient: rules file especially lean (loaded every session)

### Group D: Production Standards + Documentation (Cat 6 + Cat 7)

**CATEGORY 6 — Production Standards (10 checks):**
- Quality gates present in commit and PR flows
- Error format consistent: [{SEVERITY}] {description} in {file}:{line}
- Status indicators: OK/WARN/FAIL used consistently
- Accounting: applied + failed + needs_approval = total
- No silent failures or empty catch blocks in skill flows
- Security: zero API keys, passwords, secrets in repo
- Edit/Write skills check git status first
- Structured output: agents return JSON, never write to files
- Pre-announce actions before execution
- No emojis in tables or production output

**CATEGORY 7 — Documentation & Language (10 checks):**
- README skill count matches actual Glob count
- docs/skills.md: entry for each skill directory
- docs/agents.md: entry for each agent, all scopes documented
- docs/rules.md reflects rules/cco-rules.md content
- All files in English (no mixed-language content)
- Commit messages and PR descriptions in English
- YAML frontmatter in English
- Error messages and user-facing output in English
- No orphan documentation (docs referencing removed features)
- docs/architecture.md reflects current structure

---

## Category Definitions

| # | Category | Checks | Focus |
|---|----------|--------|-------|
| 1 | Inventory & Sync | 10 | File counts, SSOT, terminology |
| 2 | Skill & Agent Quality | 12 | Frontmatter, modes, scopes, models |
| 3 | Architecture Compliance | 10 | Deps, paths, loading, patterns |
| 4 | AI Communication | 8 | WHAT-not-HOW, no teaching, model-agnostic |
| 5 | Efficiency & Density | 10 | Benefit test, no redundancy, token budget |
| 6 | Production Standards | 10 | Quality gates, accounting, security |
| 7 | Documentation & Language | 10 | Accuracy, English, no orphans |
| 8 | Release Readiness | 8 | Installer, version, cross-platform |

**Total: ~78 checks**

---

## Severity Definitions

Per CCO Rules: Severity Levels.

---

## Step-4: Prioritize

Rank findings by 80/20 rule:
1. **Quick Win** — CRITICAL + HIGH, auto-fixable
2. **Moderate** — MEDIUM, requires targeted edit
3. **Complex** — LOW or multi-file structural changes

---

## Step-5: Fix Approval [SKIP IF --auto or --preview or zero findings]

```javascript
if (findings.length > 0) {
  // Display findings summary BEFORE asking
  // | # | Category | ID | Severity | Issue | Location | Auto-fixable |

  AskUserQuestion([{
    question: "Which findings should be fixed?",
    header: "Fix scope",
    options: [
      { label: `All (${findings.length})`, description: "Fix everything now" },
      { label: "Quick Win", description: "CRITICAL + HIGH, auto-fixable" },
      { label: "Safe only", description: "Auto-fixable items only" },
      { label: "None", description: "Report only, no fixes" }
    ],
    multiSelect: false
  }])
}
```

---

## Step-6: Apply Fixes [DELEGATE TO AGENT]

```javascript
if (toApply.length > 0) {
  Task("cco-agent-apply", `
    fixes: ${JSON.stringify(toApply)}

    Apply CCO system fixes. Types include:
    - doc-sync: Update counts in README, docs files
    - terminology: Fix inconsistent terms
    - orphan-ref: Remove deprecated references

    Per CCO Rules: Accounting, Auto Mode.

    Return: { applied: n, failed: n, needs_approval: n, total: n, details: [...] }
  `)
}
```

---

## Step-7: Summary

```
═══════════════════════════════════════════════════════════
                     CCO FULL REVIEW
═══════════════════════════════════════════════════════════

Detected:
  Skills: {skills}  Agents: {agents}  Version: {version}

┌─────────────────────────────┬────────┬────────┬────────┐
│ Category                    │ Passed │ Failed │ Status │
├─────────────────────────────┼────────┼────────┼────────┤
│ 1. Inventory & Sync         │   {n}  │   {n}  │  {st}  │
│ 2. Skill & Agent Quality    │   {n}  │   {n}  │  {st}  │
│ 3. Architecture Compliance  │   {n}  │   {n}  │  {st}  │
│ 4. AI Communication         │   {n}  │   {n}  │  {st}  │
│ 5. Efficiency & Density     │   {n}  │   {n}  │  {st}  │
│ 6. Production Standards     │   {n}  │   {n}  │  {st}  │
│ 7. Documentation & Language │   {n}  │   {n}  │  {st}  │
│ 8. Release Readiness        │   {n}  │   {n}  │  {st}  │
├─────────────────────────────┼────────┼────────┼────────┤
│ TOTAL (~78 checks)          │   {n}  │   {n}  │  {st}  │
└─────────────────────────────┴────────┴────────┴────────┘

{if findings}
## Prioritized Findings

### Quick Win (CRITICAL + HIGH, auto-fixable)
  [{SEVERITY}] {category}.{check}: {issue}
    Location: {file}:{line}
    Fix: {action}

Summary: C:{n} H:{n} M:{n} L:{n}
{/if}
═══════════════════════════════════════════════════════════
```

---

## Anti-Overengineering Guard

Before flagging, ask: (1) Does absence break something? (2) Confuse users? (3) Worth complexity?

**All NO → not a finding.**

NON-findings:
- Simple skill without explicit progress tracking
- 2-step skill without architecture table

---

## Recovery

| Situation | Recovery |
|-----------|----------|
| Fix broke a skill | `git checkout -- {file}` |
| Multiple files affected | `git checkout .` |
| Want to review changes | `git diff` |

---

## Rules

1. **Context first** — Verify CCO repo before analysis
2. **Dynamic counts** — Never hardcode expected counts; always Glob and compare
3. **80/20 prioritization** — Quick Win → Moderate → Complex
4. **Evidence required** — Every finding needs file:line

Per CCO Rules: Accounting, Auto Mode, Efficiency.

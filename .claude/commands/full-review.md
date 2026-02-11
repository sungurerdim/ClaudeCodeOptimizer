---
description: CCO system health check (~100 checks across 8 categories)
argument-hint: [--auto] [--quick] [--focus=X] [--preview] [--fix]
allowed-tools: Read(*), Grep(*), Glob(*), Bash(*), Task(*), AskUserQuestion, Edit(*)
model: opus
---

# /full-review

**CCO Self-Review** - Comprehensive analysis of CCO system against its documented design principles.

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
// Cross-platform detection using Claude's native tools
skills = Glob("skills/cco-*/SKILL.md").length     // Expected: 8
agents = Glob("agents/cco-agent-*.md").length      // Expected: 3
version = Read("rules/cco-rules.md").frontmatter.cco_version

inventory = { skills, agents, version }
```

**Note:** Rules are in `rules/cco-rules.md` (single source of truth).

---

## Step-3: 8-Category Analysis [PARALLEL AGENTS]

Launch 4 parallel Explore agents covering 8 categories:

### Group A: Structure & Release (Cat 1 + Cat 7)

**CATEGORY 1 - Inventory & Sync (12 checks):**
- Count files: skills/cco-*/SKILL.md (expected: 8), agents/cco-agent-*.md (expected: 3)
- Compare counts against README.md, docs/commands.md, docs/agents.md
- SSOT: grep for orphan refs (.cco/, principles.md, projects.json)
- Terminology: CRITICAL/HIGH/MEDIUM/LOW consistent (not P0/P1)

**CATEGORY 7 - Release Readiness (8 checks):**
- Rules file exists with valid frontmatter
- Version in cco-rules.md matches version.txt
- Go installer binary builds for all targets
- Cross-platform: no hardcoded paths (C:\, /home/)

### Group B: Skills & Agents (Cat 2 + Cat 3)

**CATEGORY 2 - Skill Quality (15 checks):**
- Each skill has valid YAML frontmatter (description, allowed-tools)
- AskUserQuestion standards (max 4 questions × 4 options)
- --auto mode: zero AskUserQuestion calls
- --preview mode: zero Edit/Write calls
- All 8 skills support --auto and --preview (where applicable)
- 6 skills auto-invoke enabled, 2 with disable-model-invocation: true

**CATEGORY 3 - Agent Quality (10 checks):**
- cco-agent-analyze: 9 OPTIMIZE scopes + 6 REVIEW scopes + 4 AUDIT scopes
- cco-agent-apply: fix scope + docs scope
- cco-agent-research: 6 scopes (local, search, analyze, synthesize, full, dependency)
- Model selection: analyze/research = haiku, apply = opus
- Output standards: JSON with findings[], metrics, status

### Group C: Standards & Practices (Cat 4 + Cat 5 + Cat 8)

**CATEGORY 4 - Token Efficiency (18 checks):**
- Tables for tabular data (not prose paragraphs)
- No redundancy across files (shared patterns reference CCO Rules)
- Large files (>500 lines) should reference by path
- AskUserQuestion limits (max 4 questions, max 4 options)
- No teaching of basics Claude already knows
- Each rule provides unique CCO-specific value

**CATEGORY 5 - UX/DX Standards (10 checks):**
- Error format: [{SEVERITY}] {description} in {file}:{line}
- Status indicators: OK/WARN/FAIL consistent
- Pre-announce actions before execution
- No emojis in tables

**CATEGORY 8 - Best Practices (12 checks):**
- Positive framing: "Do X" not "Don't do Y"
- Read-First: skills read files before editing
- Plan-Before-Act: Plan Review phase for complex changes
- No BC hacks: zero backward, compat, legacy
- No TODOs in production code

### Group D: Documentation & Safety (Cat 6)

**CATEGORY 6 - Documentation & Safety (15 checks):**
- README accuracy: skill count (8), agent count (3)
- docs/commands.md: entry for each skill
- docs/agents.md: entry for each agent, all scopes documented
- docs/rules.md: reflects rules/cco-rules.md content
- Zero API keys, passwords, secrets
- Edit/Write skills check git status first

---

## Category Definitions

| # | Category | Checks | Focus |
|---|----------|--------|-------|
| 1 | Inventory & Sync | 12 | File counts, SSOT, terminology |
| 2 | Skill Quality | 15 | Frontmatter, AskUserQuestion, modes |
| 3 | Agent Quality | 10 | Scopes, models, output |
| 4 | Token Efficiency | 18 | Density, no redundancy |
| 5 | UX/DX Standards | 10 | Errors, status, transparency |
| 6 | Documentation & Safety | 15 | Accuracy, security |
| 7 | Release Readiness | 8 | Installer, version, platform |
| 8 | Best Practices | 12 | Claude patterns, simplicity |

**Total: ~100 checks**

---

## Severity Definitions

Per CCO Rules: Severity Levels.

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
      { label: `Quick Win`, description: "CRITICAL + HIGH, auto-fixable" },
      { label: `Safe only`, description: "Auto-fixable items only" },
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
  `, { model: "opus" })
}
```

---

## Step-7: Summary

```
═══════════════════════════════════════════════════════════
                     CCO FULL REVIEW
═══════════════════════════════════════════════════════════

Detected:
  Skills: 8  Agents: 3  Rules: rules/cco-rules.md

┌─────────────────────────┬────────┬────────┬────────┐
│ Category                │ Passed │ Failed │ Status │
├─────────────────────────┼────────┼────────┼────────┤
│ 1. Inventory & Sync     │   {n}  │   {n}  │  {st}  │
│ 2. Skill Quality        │   {n}  │   {n}  │  {st}  │
│ 3. Agent Quality        │   {n}  │   {n}  │  {st}  │
│ 4. Token Efficiency     │   {n}  │   {n}  │  {st}  │
│ 5. UX/DX Standards      │   {n}  │   {n}  │  {st}  │
│ 6. Documentation        │   {n}  │   {n}  │  {st}  │
│ 7. Release Readiness    │   {n}  │   {n}  │  {st}  │
│ 8. Best Practices       │   {n}  │   {n}  │  {st}  │
├─────────────────────────┼────────┼────────┼────────┤
│ TOTAL (~100 checks)     │   {n}  │   {n}  │  {st}  │
└─────────────────────────┴────────┴────────┴────────┘

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

1. **Context first** - Verify CCO repo before analysis
2. **Dynamic counts** - Never hardcode counts
3. **80/20 prioritization** - Quick Win → Moderate → Complex
4. **Evidence required** - Every finding needs file:line

Per CCO Rules: Accounting, Auto Mode, Efficiency.

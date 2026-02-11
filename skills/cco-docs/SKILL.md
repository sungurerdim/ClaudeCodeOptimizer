---
description: Documentation gap analysis - compare ideal vs current docs, generate missing content.
argument-hint: "[--auto] [--preview] [--scope=<name>] [--update]"
allowed-tools: Read, Grep, Glob, Edit, Write, Bash, Task, AskUserQuestion
---

# /cco-docs

**Documentation Gap Analysis** — Identify missing docs, generate what's needed.

**Philosophy:** "What docs does this project need?" → "What exists?" → "Fill the gap."

## Output Constraints

Every sentence earns its place. Show > tell, examples > prose. Headers/bullets/tables for scanning. Copy-pasteable commands.

Avoid: filler, marketing language, obvious statements, duplicate content.

## Args

| Flag | Effect |
|------|--------|
| `--auto` | Detect, analyze, generate all missing docs |
| `--preview` | Analyze gaps only, no generation |
| `--scope=X` | Single scope: readme, api, dev, user, ops, changelog, refine, verify |
| `--update` | Regenerate even if docs exist |

## Context

- Git status: !`git status --short 2>/dev/null || echo ""`
- Args: $ARGS

## Scopes

| Scope | Target | Purpose |
|-------|--------|---------|
| readme | README.md | Project overview, quick start |
| api | docs/api/, API.md | Endpoint/function reference |
| dev | CONTRIBUTING.md, docs/dev/ | Developer onboarding |
| user | docs/user/, USAGE.md | End-user guides |
| ops | docs/ops/, DEPLOY.md | Deployment, operations |
| changelog | CHANGELOG.md | Version history |
| refine | Existing docs | UX/DX quality improvement |
| verify | Existing docs | Verify claims against source code |

## Execution Flow

Mode Detection → (Q1 ‖ Analysis) → Gap Analysis → [Plan] → Generate → Summary

### Phase 1: Setup [SKIP if --auto]

```javascript
AskUserQuestion([
  {
    question: "Which documentation areas should be covered?",
    header: "Areas",
    options: [
      { label: "Core (Recommended)", description: "readme + changelog" },
      { label: "Technical (Recommended)", description: "api + dev" },
      { label: "User-facing", description: "user + ops" }
    ],
    multiSelect: true
  },
  {
    question: "Should existing docs be analyzed?",
    header: "Analysis",
    options: [
      { label: "None (Recommended)", description: "Only generate missing docs" },
      { label: "Refine", description: "Improve existing doc quality" },
      { label: "Verify", description: "Check doc claims against source code" }
    ],
    multiSelect: false
  },
  {
    question: "How should existing docs be handled?",
    header: "Mode",
    options: [
      { label: "Fill Gaps (Recommended)", description: "Only create what's missing" },
      { label: "Update All", description: "Regenerate even if docs exist" }
    ],
    multiSelect: false
  }
])
```

In --auto: generation scopes only (refine/verify require explicit `--scope=`).

### Phase 2: Analysis [PARALLEL with Phase 1]

Delegate to cco-agent-analyze (scope: docs): scan existing docs, detect project type, detect documentation needs.

Per CCO Rules: Agent Error Handling. If analysis still fails, proceed with gap analysis using file existence checks only.

### Phase 3: Gap Analysis [IDEAL vs CURRENT]

Define ideal docs by project type:

| Type | README | API | Dev | User | Ops | Changelog |
|------|--------|-----|-----|------|-----|-----------|
| CLI | Full | - | Basic | Full | - | Yes |
| Library | Full | Full | Full | Guides | Publish | Yes |
| API | Full | Full | Full | Full | Full | Yes |
| Web | Full | Components | Full | Basic | Full | Yes |

Calculate gaps: missing docs = HIGH priority, incomplete (<70%) = MEDIUM. Display gap table.

### Phase 3a: Refine [SCOPE=refine]

Analyze existing docs for: scannability, clarity, redundancy, overengineering, DX quality, conciseness. Convert findings to improvement tasks.

### Phase 3b: Verify [SCOPE=verify]

Cross-reference doc claims against source: command flags, step counts, scope names, file paths, config keys, example commands. Mismatches become fix tasks.

### Phase 4: Plan Review [CONDITIONAL, SKIP if --auto]

Triggers: findings > 0, >3 docs to generate, or API scope.

Display plan: target files, sections, estimated lines, sources.

```javascript
AskUserQuestion([{
  question: "How should documentation be generated?",
  header: "Action",
  options: [
    { label: "Generate All (Recommended)", description: "Create all identified missing docs" },
    { label: "High Priority Only", description: "Only HIGH priority gaps" },
    { label: "Abort", description: "Don't generate anything" }
  ],
  multiSelect: false
}])
```

### Phase 5: Generate Documentation

Delegate to cco-agent-apply:

On error: If generation fails for a doc, count as failed, continue with next.
- Extract from actual source files
- Apply: brevity, examples, scannability, actionability
- Follow format by scope (README, API, Dev, User, Ops, Changelog)
- Avoid: filler, "this document explains...", long paragraphs, obvious statements

### Phase 6: Summary

Per CCO Rules: Accounting.

Gap summary (before/after), files generated, applied/failed/total.

--auto: `cco-docs: {OK|WARN|FAIL} | Applied: N | Failed: N | Total: N`

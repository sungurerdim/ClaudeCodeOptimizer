---
description: Documentation gap analysis — compare ideal vs current docs, generate missing content. Use when documentation needs to be created, updated, or audited.
argument-hint: "[--auto] [--preview] [--scope=<name>] [--update]"
allowed-tools: Read, Grep, Glob, Edit, Write, Bash, Task, AskUserQuestion
---

# /cco-docs

**Documentation Gap Analysis** — Identify missing docs, generate what's needed.

## Output Constraints

Every sentence earns its place. Show > tell, examples > prose. Headers/bullets/tables for scanning. Copy-pasteable commands. Avoid: filler, marketing language, obvious statements, duplicate content.

## Args

| Flag | Effect |
|------|--------|
| `--auto` | Detect, analyze, generate all missing docs |
| `--preview` | Analyze gaps only, no generation |
| `--scope=X` | Single scope: readme, api, dev, user, ops, changelog, refine, verify |
| `--update` | Regenerate even if docs exist |

## Context

- Git status: !`git status --short 2>/dev/null | cat`
- Args: $ARGUMENTS

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

Setup → Analysis → Gap Analysis → [Plan] → Generate → Summary

### Phase 1: Setup [SKIP if --auto]

**Pre-flight:** Verify git repo: `git rev-parse --git-dir 2>/dev/null` → not a repo: warn "Not a git repo — git context unavailable" and continue (git optional for docs).

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
    question: "How should existing docs be handled?",
    header: "Mode",
    options: [
      { label: "Fill Gaps (Recommended)", description: "Only create what's missing" },
      { label: "Refine existing", description: "Improve quality of current docs" },
      { label: "Verify claims", description: "Check doc claims against source code" },
      { label: "Update All", description: "Regenerate even if docs exist" }
    ],
    multiSelect: false
  }
])
```

In --auto: generation scopes only (refine/verify require explicit `--scope=`).

### Phase 2: Analysis [PARALLEL with Phase 1]

Delegate to cco-agent-analyze (scopes: [doc-sync], mode: auto): scan existing docs, detect project type, detect documentation needs. Per CCO Rules: Agent Error Handling — validate agent JSON output, retry once on malformed response, on second failure continue with remaining groups, score failed dimensions as N/A. Fallback: file existence checks.

### Phase 3: Gap Analysis [IDEAL vs CURRENT]

Ideal docs by project type:

| Type | README | API | Dev | User | Ops | Changelog |
|------|--------|-----|-----|------|-----|-----------|
| CLI | Full | - | Basic | Full | - | Yes |
| Library | Full | Full | Full | Guides | Publish | Yes |
| API | Full | Full | Full | Full | Full | Yes |
| Web | Full | Components | Full | Basic | Full | Yes |

Missing docs = HIGH, incomplete (<70%) = MEDIUM.

**Refine scope:** Analyze for scannability, clarity, redundancy, conciseness. Convert to improvement tasks.

**Verify scope:** Cross-reference doc claims against source. Testable claims checklist: CLI flags, config keys, file paths, function signatures, step counts, default values, env vars. For each: Grep/Read source to confirm. Minimum: ALL numbered lists, ALL code examples, ALL flag tables. Mismatches → fix tasks.

### Phase 4: Plan Review [CONDITIONAL, SKIP if --auto]

Display plan (target files, sections, sources). Ask: Generate All (recommended) / High Priority Only / Abort.

### Phase 5: Generate Documentation

Delegate to cco-agent-apply (scope: docs, operations: [{action, scope, file, sections, sources, projectType}]). Extract from actual source files. Apply: brevity, examples, scannability, actionability. Avoid: filler, "this document explains...", long paragraphs. On error: count as failed, continue.

**Source mandate:** Every documented flag, endpoint, or config value MUST have Grep/Read verification before inclusion. Never document features from memory or inference.

### Phase 6: Summary

Per CCO Rules: Accounting — applied + failed + needs_approval = total. No "declined" category.

Interactive output format:

```
cco-docs complete
=================
| Scope     | Status   | File            | Lines |
|-----------|----------|-----------------|-------|
| readme    | Updated  | README.md       |   +12 |
| api       | Created  | docs/api.md     |    85 |
| dev       | Skipped  | CONTRIBUTING.md |     — |

Applied: 2 | Failed: 0 | Total: 2
```

Gap summary (before/after), files generated, applied/failed/total.

--auto: `cco-docs: {OK|WARN|FAIL} | Applied: N | Failed: N | Total: N`

---
name: cco-optimize
description: Measurable efficiency improvements
---

# /cco-optimize

**Efficiency optimization** - Reduce waste → measure impact → verify.

**Standards:** Command Flow | Fix Workflow | Approval Flow | Safety Classification | Output Formatting

## Context Application

| Field | Effect |
|-------|--------|
| Scale | <100 → clarity over performance; 10K+ → performance critical |
| Type | CLI: startup time; API: response time; Library: memory; Frontend: bundle size |
| Maturity | Legacy → safe optimizations only; Greenfield → aggressive restructuring OK |
| Breaking | Never → preserve all interfaces; Allowed → simplify APIs, remove compat |
| Data | PII → no caching user data, careful with logging; Regulated → audit trail |
| Priority | Speed → quick wins only; Quality → comprehensive analysis |

## Default Behavior

When called without flags, ask:
1. **Categories** (multiSelect): All | Context | Docs | Code | Cross-file
2. **Mode**: Conservative | Balanced [recommended] | Aggressive

Explicit flags skip questions.

## Categories

| Flag | Target | Checks |
|------|--------|--------|
| `--context` | CLAUDE.md, prompts, agents | Duplicates, verbose patterns, implicit info, format inefficiency, dead instructions |
| `--docs` | README, comments, docstrings | Stale content, redundant sections, verbose explanations |
| `--code` | Source files | Quality (DRY, orphans, complexity, types) + Efficiency (loops, conditionals, algorithms) + Performance (N+1, indexes, I/O, memory) |
| `--cross-file` | All files | Duplicate, redundant, obsolete, overlapping content |
| `--all` | Everything | All applicable categories |

**Sub-category selection (only when `--code` flag used alone):**
`--code` → ask (multiSelect): All | Quality | Efficiency | Performance

Note: `--all` or interactive "All" selection includes all sub-categories automatically.

## Cross-File Detection

| Type | Definition | Action |
|------|------------|--------|
| Duplicate | Identical content | Consolidate |
| Redundant | Same meaning | Keep best |
| Obsolete | References non-existent | Remove |
| Overlap | Partial duplication | Merge |

Report format: `[CROSS-FILE] {type}: "{summary}" → {file1}:{line} ↔ {file2}:{line}`

## Flow

Per Command Flow standard, then Fix Workflow for applying changes.

## Output

**Standards:** Output Formatting

Tables:
1. **Results** - File | Before | After | Change %
2. **Applied** - Type | Location | Description
3. **Metrics** - Lines/Tokens before→after

## Verification

After optimization: tests pass, same behavior, no broken imports, metrics improved.

## Usage

```bash
/cco-optimize                    # Interactive
/cco-optimize --context          # AI context files
/cco-optimize --docs             # README, comments, docstrings
/cco-optimize --code             # Source files (quality + efficiency + performance)
/cco-optimize --cross-file       # Duplicate detection
/cco-optimize --all              # Everything, balanced mode
```

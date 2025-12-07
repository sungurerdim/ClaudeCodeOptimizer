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
| `--dedupe` | All files | Focus on exact and near-duplicate detection |
| `--consolidate` | All files | Merge overlapping content into single source |
| `--prune` | All files | Remove obsolete, orphan, and dead content |
| `--all` | Everything | All applicable categories |

**Sub-category selection (only when single flag used):**
- `--code` → ask (multiSelect): All | Quality | Efficiency | Performance
- `--cross-file` → ask (multiSelect): All | Duplicates | Redundant | Obsolete | Overlap
- `--dedupe` → ask (multiSelect): All | Exact | Near-duplicate | Semantic

Note: `--all` or interactive "All" selection includes all sub-categories automatically.

## Cross-File Detection

### Detection Types

| Type | Sub-type | Definition | Action |
|------|----------|------------|--------|
| Duplicate | Exact | 100% identical content | Consolidate → single source |
| Duplicate | Near (>80%) | Minor differences | Review → merge or justify |
| Duplicate | Semantic | Different code, same logic | Extract shared abstraction |
| Redundant | Code | Same functionality | Keep best, redirect others |
| Redundant | Config | Same value in multiple configs | Single source + reference |
| Redundant | Doc | Same info in multiple docs | Consolidate or cross-reference |
| Obsolete | Dead ref | References deleted code | Remove reference |
| Obsolete | Stale doc | Documents removed feature | Update or remove |
| Obsolete | Orphan | No references to it | Delete or reconnect |
| Overlap | Partial code | Shared logic extractable | Extract common module |
| Overlap | Doc sections | Partially same content | Merge sections |

### Detection Methods

| Method | Detects | Algorithm |
|--------|---------|-----------|
| Content hash | Exact duplicates | MD5/SHA256 of normalized content |
| Fuzzy match | Near-duplicates | Levenshtein distance, Jaccard similarity (threshold: 80%) |
| AST compare | Semantic duplicates | Parse → normalize → structural comparison |
| Token analysis | Logic duplicates | Tokenize → n-gram → similarity score |
| Dep graph | Orphans | Build import graph → find unreachable nodes |
| Ref scan | Obsolete refs | Grep all identifiers → verify target exists |
| Doc extraction | Stale docs | Extract claims → verify against codebase |

### Report Format

Single-line: `[CROSS-FILE] {type}: "{summary}" → {file1}:{line} ↔ {file2}:{line}`

Detailed:
```
┌─ DUPLICATE FOUND ────────────────────────────────────────────┐
│ Type: Near-duplicate (87% similar)                           │
│ File A: src/utils/auth.py:45-67 (22 lines)                   │
│ File B: src/helpers/login.py:12-35 (24 lines)                │
├──────────────────────────────────────────────────────────────┤
│ Differences:                                                 │
│   - auth.py uses 'user_id', login.py uses 'userId'           │
│   - login.py has extra logging statement                     │
├──────────────────────────────────────────────────────────────┤
│ Suggestion: Extract to src/core/auth_base.py                 │
│ Risk: LOW (internal modules, full test coverage)             │
└──────────────────────────────────────────────────────────────┘
```

## Flow

Per Command Flow standard, then Fix Workflow for applying changes.

## Resolution Actions

| Finding | Safe (auto-apply) | Risky (approval needed) |
|---------|-------------------|-------------------------|
| Exact duplicate | Consolidate + re-export | Delete one copy |
| Near-duplicate | Show diff, suggest merge | Auto-merge |
| Semantic duplicate | Suggest extraction | Refactor both |
| Orphan file | Warn, suggest deletion | Delete file |
| Orphan function | Remove from exports | Delete function |
| Stale doc | Flag for review | Remove section |
| Config redundancy | Single source + env ref | Merge configs |
| Overlap | Suggest extraction point | Auto-extract |

## Output

### Cross-File Analysis Table
```
┌─ CROSS-FILE ANALYSIS ────────────────────────────────────────┐
│ Type       │ Sim%  │ Files                    │ Action       │
├────────────┼───────┼──────────────────────────┼──────────────┤
│ Duplicate  │ 100%  │ utils.py ↔ helpers.py    │ Consolidate  │
│ Near-dup   │ 87%   │ auth.py ↔ login.py       │ Review       │
│ Semantic   │ ~75%  │ parse_v1.py ↔ parse_v2.py│ Extract      │
│ Orphan     │ -     │ old_api.py               │ Delete?      │
│ Stale ref  │ -     │ README.md:42             │ Update       │
│ Overlap    │ 45%   │ config.json ↔ .env       │ Merge        │
├────────────┼───────┼──────────────────────────┼──────────────┤
│ Total: 6 issues │ Safe: 3 │ Review: 3           │              │
└────────────┴───────┴──────────────────────────┴──────────────┘
```

### Optimization Results
```
┌─ OPTIMIZATION RESULTS ───────────────────────────────────────┐
│ File              │ Before │ After  │ Change │ Status        │
├───────────────────┼────────┼────────┼────────┼───────────────┤
│ utils.py          │ 245 L  │ 198 L  │ -19%   │ Consolidated  │
│ helpers.py        │ 180 L  │ 12 L   │ -93%   │ Re-exports    │
│ README.md         │ 420 L  │ 385 L  │ -8%    │ Deduplicated  │
│ old_api.py        │ 89 L   │ 0 L    │ -100%  │ Deleted       │
├───────────────────┼────────┼────────┼────────┼───────────────┤
│ TOTAL             │ 934 L  │ 595 L  │ -36%   │               │
└───────────────────┴────────┴────────┴────────┴───────────────┘
```

### Metrics Summary
```
Before: 2,450 lines | 48,200 tokens | 156 KB
After:  1,890 lines | 37,100 tokens | 121 KB
Saved:  560 lines (23%) | 11,100 tokens (23%) | 35 KB (22%)
```

## Verification

After optimization:
- [ ] Tests pass (no regressions)
- [ ] Same behavior (functional equivalence)
- [ ] No broken imports (all refs valid)
- [ ] Metrics improved (lines/tokens reduced)
- [ ] No orphans created (consolidation complete)

## Usage

```bash
/cco-optimize                    # Interactive
/cco-optimize --context          # AI context files
/cco-optimize --docs             # README, comments, docstrings
/cco-optimize --code             # Source files (quality + efficiency + performance)
/cco-optimize --cross-file       # Full cross-file analysis
/cco-optimize --dedupe           # Focus on duplicate detection
/cco-optimize --consolidate      # Merge overlapping content
/cco-optimize --prune            # Remove obsolete/orphan content
/cco-optimize --all              # Everything, balanced mode
```

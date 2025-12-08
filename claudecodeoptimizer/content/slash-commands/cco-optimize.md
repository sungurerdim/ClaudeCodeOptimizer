---
name: cco-optimize
description: Code cleanliness and efficiency optimization with auto-fix
allowed-tools: Read(*), Grep(*), Glob(*), Edit(*), Bash(git:*), Bash(wc:*), Task(*)
---

# /cco-optimize

**Cleanliness & Efficiency** - Analyze → clean → optimize → verify.

End-to-end: Detects waste (orphans, duplicates, stale refs) AND removes/optimizes them.

**Standards:** Command Flow | Fix Workflow | Approval Flow | Safety Classification | Output Formatting

## Context

- Scale: !`grep "^Scale:" ./CLAUDE.md 2>/dev/null`
- Maturity: !`grep "^Maturity:" ./CLAUDE.md 2>/dev/null`
- File count: !`find . -type f -name "*.py" -o -name "*.ts" -o -name "*.js" 2>/dev/null | wc -l`
- Git status: !`git status --short`

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

When called without flags, ask (follow CCO "Question Formatting" standard):

| Question | Options (small → large) |
|----------|-------------------------|
| Focus? (multiSelect) | Hygiene, Efficiency, All |
| Mode? | Conservative, Balanced, Aggressive |

**`[recommended]` placement:** Focus → Hygiene, Mode → Balanced

Explicit flags skip questions.

## Categories

### Orphans (`--orphans`)

Detect and remove unreferenced code:

| Type | Detection | Action |
|------|-----------|--------|
| Orphan file | No imports pointing to it | Delete with confirmation |
| Orphan function | Defined but never called | Delete or flag |
| Orphan export | Exported but never imported | Remove export |
| Orphan import | Imported but never used | Remove import |
| Orphan config | Config key not referenced | Remove or flag |

Report: `[ORPHAN] {type}: {name} in {file:line} (last modified: {date})`

**Resolution:** For each orphan, ask: "Delete" | "Keep (add reference)" | "Skip"

### Stale References (`--stale-refs`)

Detect and fix broken references:

| Type | Detection | Action |
|------|-----------|--------|
| Broken import | Import path doesn't exist | Remove or fix path |
| Dead link | URL returns 404 | Update or remove |
| Missing ref | Code references undefined | Fix or remove |
| Obsolete comment | Comment references deleted code | Update comment |
| Phantom test | Test for non-existent function | Remove test |

Report: `[STALE-REF] {type}: {reference} → {missing_target} in {file:line}`

### Duplicates (`--duplicates`)

Detect and consolidate duplicate content:

| Type | Similarity | Action |
|------|------------|--------|
| Exact duplicate | 100% | Consolidate → single source + re-export |
| Near-duplicate | >80% | Review → merge or justify differences |
| Semantic duplicate | Same logic | Extract shared abstraction |

Detection methods:
- Content hash (MD5/SHA256) for exact matches
- Fuzzy match (Levenshtein, Jaccard) for near-duplicates
- AST comparison for semantic duplicates

Report: `[DUPLICATE] {type} ({similarity}%): {file1}:{line} ↔ {file2}:{line}`

### Redundancy (`--redundancy`)

Detect and eliminate redundant content:

| Type | Detection | Action |
|------|-----------|--------|
| Redundant code | Same functionality in different places | Keep best, redirect others |
| Redundant config | Same value in multiple configs | Single source + reference |
| Redundant docs | Same info in multiple places | Consolidate or cross-reference |

### Context (`--context`)

Optimize AI context files:

| Target | Optimization |
|--------|-------------|
| CLAUDE.md | Remove duplicates, compress verbose patterns |
| Prompts | Implicit info removal, format efficiency |
| Agent configs | Dead instruction removal |

### Docs (`--docs`)

Optimize documentation:

| Target | Optimization |
|--------|-------------|
| Stale content | Update or remove outdated sections |
| Redundant sections | Merge overlapping content |
| Verbose explanations | Trim to essential |
| Broken examples | Fix or remove |

### Code Efficiency (`--code`)

Optimize code performance:

| Category | Optimizations |
|----------|---------------|
| Loops | Unnecessary iterations, early exits |
| Conditionals | Simplification, guard clauses |
| Algorithms | Better complexity alternatives |
| N+1 queries | Batch database calls |
| Memory | Reduce allocations, streaming |
| Imports | Tree-shaking hints, lazy loading |

### Cross-File (`--cross-file`)

Full codebase analysis combining all above:

| Analysis | Scope |
|----------|-------|
| Dependency graph | All imports/exports |
| Duplication map | All files |
| Orphan detection | All code |
| Stale ref scan | All references |

## Meta-flags

| Flag | Includes |
|------|----------|
| `--hygiene` | orphans + stale-refs + duplicates (quick cleanup) |
| `--efficiency` | code + context + docs (optimization focus) |
| `--deep` | All categories, thorough analysis |
| `--prune` | Focus on removal (orphans + stale-refs + dead content) |
| `--all` | Everything applicable |
| `--auto-fix` | Apply safe fixes without asking |

## Resolution Actions

| Finding | Safe (auto-apply) | Risky (approval needed) |
|---------|-------------------|-------------------------|
| Exact duplicate | Consolidate + re-export | Delete one copy |
| Near-duplicate | Show diff, suggest merge | Auto-merge |
| Semantic duplicate | Suggest extraction | Refactor both |
| Orphan file | Warn, suggest deletion | Delete file |
| Orphan function | Remove from exports | Delete function |
| Stale ref | Flag for review | Remove reference |
| Broken import | Fix path if obvious | Remove import |
| Config redundancy | Single source + env ref | Merge configs |

## Output

### Cleanliness Summary
```
┌─ CLEANLINESS SUMMARY ────────────────────────────────────────┐
│ Category      │ Found │ Fixed │ Skipped │ Status            │
├───────────────┼───────┼───────┼─────────┼───────────────────┤
│ Orphans       │ 5     │ 4     │ 1       │ WARN              │
│ Stale-Refs    │ 3     │ 3     │ 0       │ OK                │
│ Duplicates    │ 2     │ 2     │ 0       │ OK                │
│ Redundancy    │ 1     │ 1     │ 0       │ OK                │
├───────────────┼───────┼───────┼─────────┼───────────────────┤
│ TOTAL         │ 11    │ 10    │ 1       │ WARN              │
└───────────────┴───────┴───────┴─────────┴───────────────────┘
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
- [ ] No new orphans created (consolidation complete)

## Usage

```bash
/cco-optimize                    # Interactive
/cco-optimize --hygiene          # Quick cleanup (orphans + stale-refs + duplicates)
/cco-optimize --orphans          # Find and remove unreferenced code
/cco-optimize --stale-refs       # Find and fix broken references
/cco-optimize --duplicates       # Find and consolidate duplicates
/cco-optimize --code             # Code efficiency optimization
/cco-optimize --cross-file       # Full cross-file analysis
/cco-optimize --prune            # Remove all dead content
/cco-optimize --all --auto-fix   # Everything, auto-apply safe fixes
```

## Related Commands

- `/cco-audit` - For security and quality checks
- `/cco-refactor` - For structural transformations (rename, move, extract)
- `/cco-checkup` - For regular maintenance routine

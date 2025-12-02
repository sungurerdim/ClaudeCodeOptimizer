---
name: cco-optimize
description: Measurable efficiency improvements
---

# /cco-optimize

**Efficiency optimization** - Reduce waste → improve efficiency → measure impact → verify.

**Standards:** Pre-Operation Safety | Context Read | Approval Flow | Safety Classification | Verification | Error Format

## Context Application
- **Guidelines** - Follow listed guidelines
- **Scale** - If 10K+ → prioritize performance optimizations
- **Type** - CLI: startup time, API: response time, library: memory footprint
- **Maturity** - If Legacy → minimal changes; if Greenfield → can restructure
- **Priority** - If Speed → quick wins only; if Quality → thorough optimization
- **Breaking** - If Never → preserve all interfaces; if Allowed → can simplify APIs

## Default Behavior

When called without flags, AskUserQuestion:

```
header: "Categories"
question: "What to optimize?"
multiSelect: true
options:
  - All: "Run all applicable categories"
  - Context: "AI context files (CLAUDE.md, prompts, agents)"
  - Docs: "Documentation (README, comments, docstrings)"
  - Code Quality: "Standards compliance, dead code, complexity"
  - Code Efficiency: "Algorithms, patterns, structure"
  - Performance: "N+1 queries, caching, I/O"
  - Cross-file: "Duplicate/redundant detection across files"

header: "Mode"
question: "Optimization mode?"
options:
  - Conservative: "Safe changes only, preserve structure"
  - Balanced: "Moderate improvements, some restructuring" [recommended]
  - Aggressive: "Maximum optimization, may restructure significantly"
```

Explicit flags (`--context`, `--code-quality`, etc.) skip category question.
Explicit mode flags (`--conservative`, `--balanced`, `--aggressive`) skip mode question.

## Categories

- `--context` - AI context optimization (CLAUDE.md, prompts, instructions)
- `--docs` - Documentation optimization (README, comments, docstrings)
- `--code-quality` - Dead code, unused imports, complexity reduction
- `--code-efficiency` - Same result with less/cleaner code
- `--performance` - N+1 queries, caching, algorithms
- `--cross-file` - Duplicate/overlap detection across all files
- `--all` - Run all applicable categories

## AI Context Optimization (`--context`)

Optimize files consumed by AI models for maximum understanding with minimum tokens.

**Standards:** AI Context (Universal) - Semantic Density, Structured Format, Front-load Critical, Scannable Hierarchy, No Filler

### Targets

- `CLAUDE.md` (global + local)
- System prompts, agent definitions
- Command/instruction files
- Any `.md` file in `.claude/`

### Checks

1. **Duplicate Detection** - Same instruction in multiple places
2. **Verbose Patterns** - "Please note that..." → remove filler
3. **Implicit Info** - Stating what AI already knows
4. **Format Inefficiency** - Prose that should be table/list
5. **Dead Instructions** - Rules for features that don't exist

## Documentation Optimization (`--docs`)

### Targets

- README.md, CONTRIBUTING.md, CHANGELOG.md
- Code comments and docstrings
- API documentation
- Any user-facing documentation

### Checks

1. **Stale Content** - References to removed features/files
2. **Redundant Sections** - Same info in multiple docs
3. **Verbose Explanations** - Can be condensed without losing clarity
4. **Missing Cross-refs** - Should link instead of repeat

## Cross-File Analysis (`--cross-file`)

Detect duplicate, redundant, obsolete, and overlapping content across ALL project files.

### Scan Scope

| File Type | Include | Example Patterns |
|-----------|---------|------------------|
| Documentation | Yes | `*.md`, `docs/**` |
| Config | Yes | `*.json`, `*.yaml`, `*.toml` |
| Source Code | Yes | Comments, docstrings, constants |
| AI Files | Yes | `.claude/**`, prompts, agents |

### Detection Types

| Type | Definition | Action |
|------|------------|--------|
| **Duplicate** | Identical or near-identical content | Consolidate to single source |
| **Redundant** | Same meaning, different words | Keep best version |
| **Obsolete** | References non-existent code/features | Remove or update |
| **Overlap** | Partial duplication with variations | Merge and deduplicate |

### Report Format

```
[CROSS-FILE] {type}: "{content_summary}"
  → {file1}:{line} (source)
  → {file2}:{line} (duplicate)
  Suggestion: {consolidation_action}
```

## Code Quality (`--code-quality`)

Apply active standards from context to improve code quality.

### Standards-Based Checks

Read applicable standards from `CCO_CONTEXT` and verify:

| Standard | Check | Optimization |
|----------|-------|--------------|
| **DRY** | Duplicate code blocks | Extract to shared function |
| **No Orphans** | Unused functions/imports | Remove dead code |
| **Complexity** | Cyclomatic >10 | Split into smaller functions |
| **Type Safety** | Missing annotations | Add type hints |
| **Clean Code** | Unclear names | Rename for clarity |
| **Immutability** | Mutable where unnecessary | Use const/final |

### Targets

- All source code files (`.py`, `.ts`, `.js`, `.go`, etc.)
- Test files (apply same standards)
- Config files with code (`.js` configs)

## Code Efficiency (`--code-efficiency`)

Evaluate if same functionality can be written more efficiently:

| Optimization | Before | After |
|--------------|--------|-------|
| **Loop Simplification** | Manual iteration | List comprehension/map |
| **Conditional Reduction** | Nested if/else | Early return, guard clauses |
| **API Modernization** | Deprecated patterns | Current best practices |
| **Algorithm Improvement** | O(n²) brute force | O(n log n) or O(n) |
| **Redundant Operations** | Repeated calculations | Cache/memoize |

Show: current implementation → suggested improvement → diff

## Performance (`--performance`)

### Code Performance

| Check | Detection | Optimization |
|-------|-----------|--------------|
| **N+1 Queries** | Loop with DB call | Batch query, eager load |
| **Missing Index** | Slow query patterns | Suggest index |
| **Blocking I/O** | Sync in async context | Use async alternatives |
| **Memory Leaks** | Unclosed resources | Add cleanup |
| **Repeated Computation** | Same calc multiple times | Memoization |

### Targets by Type

| Project Type | Focus Areas |
|--------------|-------------|
| **CLI** | Startup time, import optimization |
| **API** | Response time, connection pooling |
| **Library** | Memory footprint, lazy loading |
| **Frontend** | Bundle size, render performance |

## Before/After Metrics

Show impact after optimization:
- Lines: before → after (% reduction)
- Tokens: before → after (for context files)
- Complexity: before → after (for code)

## Verification

After optimization:
- Tests still pass
- Same behavior (no functional changes)
- No broken imports
- Metrics improved

## Usage

```bash
/cco-optimize                    # Interactive: ask mode + categories
/cco-optimize --context          # AI context optimization
/cco-optimize --docs             # Documentation optimization
/cco-optimize --code-quality     # Standards-based code improvements
/cco-optimize --code-efficiency  # Algorithmic/structural improvements
/cco-optimize --performance      # Performance optimizations
/cco-optimize --cross-file       # Cross-file duplicate detection
/cco-optimize --all --balanced   # All categories, balanced mode
```

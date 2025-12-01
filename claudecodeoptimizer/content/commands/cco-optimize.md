---
name: cco-optimize
description: Measurable efficiency improvements
---

# /cco-optimize

**Efficiency optimization** - Reduce waste → improve efficiency → measure impact → verify.

## Pre-Operation

**Follow Pre-Operation Safety from cco-standards Workflow section.**

## Project Context

**Follow Context Read from cco-standards Workflow section.**

From context apply:
- **Guidelines** - Follow listed guidelines
- **Scale** - If 10K+ → prioritize performance optimizations
- **Type** - CLI: startup time, API: response time, library: memory footprint
- **Maturity** - If Legacy → minimal changes; if Greenfield → can restructure
- **Priority** - If Speed → quick wins only; if Quality → thorough optimization
- **Breaking** - If Never → preserve all interfaces; if Allowed → can simplify APIs

## Default Behavior

When called without flags, AskUserQuestion:

```
header: "Mode"
question: "Optimization mode?"
options:
  - Conservative: "{base_description} {labels}"
  - Balanced: "{base_description} {labels}" [recommended]
  - Aggressive: "{base_description} {labels}"
```

Explicit flags (`--conservative`, `--balanced`, `--aggressive`) skip this question.

## Categories

- `--context` - CLAUDE.md optimization, remove system-prompt duplicates
- `--code-quality` - Dead code, unused imports, complexity reduction
- `--code-efficiency` - Same result with less/cleaner code
- `--performance` - N+1 queries, caching, algorithms
- `--markdown` - Verbose content reduction

## Code Efficiency

Evaluate if same functionality can be written more efficiently:
- Fewer lines for same result
- More readable implementation
- Better algorithms/patterns
- Reduced complexity while maintaining behavior

Show: current implementation → suggested improvement → diff

## Before/After Metrics

Show impact after optimization:
- Lines: before → after (% reduction)
- Tokens: before → after (for context files)
- Complexity: before → after (for code)

## Approval Flow

**Follow Approval Flow from cco-standards.**

**Follow Safety Classification from cco-standards Workflow section.**

## Error Reporting

**Follow Error Format from cco-standards Core section:**
`❌ {What} → ↳ {Why} → → {Fix}`

## Verification

After optimization:
- Tests still pass
- Same behavior (no functional changes)
- No broken imports
- Metrics improved

## Usage

```bash
/cco-optimize                  # Interactive: ask mode
/cco-optimize --context        # Context file optimization
/cco-optimize --code-quality   # Dead code removal
/cco-optimize --all --balanced # All categories, balanced mode
```

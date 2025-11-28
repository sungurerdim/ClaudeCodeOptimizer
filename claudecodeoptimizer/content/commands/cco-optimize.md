---
name: cco-optimize
description: Measurable efficiency improvements
---

# /cco-optimize

**Efficiency optimization** - Reduce waste → improve efficiency → measure impact → verify.

## Pre-Operation Safety

If uncommitted changes exist, AskUserQuestion:
→ Commit first (cco-commit) / Stash / Continue anyway

## Project Context

Load project context to calibrate optimization aggressiveness.

### Check Existing Context

```bash
cat .claude/cco_context.yaml 2>/dev/null
```

### Context Flow

**If exists:** Ask if still valid (Yes / Update / Refresh)
**If not exists:** Gather with conditional questions (see content/shared/project-context.md)

### Context-Calibrated Optimization

Adjust optimization approach based on context:

| Context | Approach | Focus |
|---------|----------|-------|
| Solo MVP + Urgent | Conservative only | Quick wins that unblock |
| Team + Normal | Balanced | DRY, readability |
| Enterprise + Relaxed | Can be aggressive | Full optimization |

### Using Context

When recommending optimizations:
- **Time pressure: urgent** → Only critical optimizations
- **Team: large** → Prioritize readability over cleverness
- **Rollback: complex** → Prefer conservative mode
- **Scale: 1M+** → Prioritize performance optimizations

Explain how context affects your optimization choices.

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
- Readability: before → after (if applicable)

## Modes

- `--conservative` - Safe changes only (auto-apply)
- `--balanced` - Safe + low-risk
- `--aggressive` - All (requires review)

## Verification

After optimization:
- Tests still pass
- Same behavior (no functional changes)
- No broken imports
- Metrics improved

## Usage

```bash
/cco-optimize --context
/cco-optimize --code-quality
/cco-optimize --code-efficiency
/cco-optimize --all --balanced
```

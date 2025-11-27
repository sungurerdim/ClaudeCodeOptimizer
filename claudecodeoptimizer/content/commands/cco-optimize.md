---
name: cco-optimize
description: Measurable efficiency improvements
---

# /cco-optimize

**Efficiency optimization** - Reduce waste → improve efficiency → measure impact → verify.

## Agent Delegation

| Phase | Agent | Purpose |
|-------|-------|---------|
| Detect | `cco-agent-detect` | Identify stack, tools |
| Analyze | `cco-agent-scan` | Find optimization opportunities |
| Apply | `cco-agent-action` | Apply with before/after metrics |

### MANDATORY Agent Rules

1. **NEVER use direct Edit/Write tools** - delegate to agents
2. **ALWAYS use agents as first choice**, not fallback after errors
3. Detect phase → `cco-agent-detect`
4. Analyze phase → `cco-agent-scan`
5. Apply phase → `cco-agent-action`

### Error Recovery

On "File unexpectedly modified" or tool errors:
1. Do NOT retry with direct tools
2. Immediately delegate to appropriate agent
3. Agent reads fresh and applies changes
4. Report agent results to user

## Pre-Operation Safety

If uncommitted changes exist, AskUserQuestion:
→ Commit first (cco-commit) / Stash / Continue anyway

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

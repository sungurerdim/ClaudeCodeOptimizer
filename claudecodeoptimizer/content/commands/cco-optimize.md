---
name: cco-optimize
description: Optimize context, code quality, and performance
categories:
  context: [claude.md, token-reduction, system-prompt-awareness]
  code-quality: [dead-code, complexity, imports, lint]
  performance: [n+1, caching, indexes, algorithms]
  markdown: [docs, verbose-content, formatting]
  claude-tools: [commands, agents, user-tools]
exclude-patterns: [cco-*]  # Don't optimize CCO's own files
---

# /cco-optimize

**Optimize content and code**

---

## Flow: Scan → Suggest → Apply → Measure

### Scan
1. Categorize files (context, code, markdown)
2. Measure tokens/complexity
3. Identify optimization opportunities

### Suggest
Present opportunities by risk:
- **Safe**: Whitespace, unused code, formatting
- **Low-risk**: Example consolidation, cross-references
- **High-risk**: Content reduction (manual review)

User selects mode: Conservative / Balanced / Aggressive

### Apply
1. Create backup
2. Apply optimizations
3. Verify (syntax + semantic + quality)
4. Rollback if verification fails

### Measure
Before/after metrics for each change.

---

## Pillars

### Context Optimization (--context)
Optimize files loaded at session start:
- **CLAUDE.md**: Remove redundant content
- **System prompt awareness**: Detect CLAUDE.md content that duplicates system prompt (git workflow, tool usage, etc.)
- **Token reduction**: Verbose → concise without losing meaning

### Code Quality (--code-quality)
- Dead code removal
- Complexity reduction
- Unused imports
- Lint violations

### Performance (--performance)
- N+1 query detection
- Missing indexes
- Caching opportunities
- Algorithm optimization

### Markdown (--markdown)
All .md files in project:
- Verbose content reduction
- Formatting consistency
- Whitespace normalization

### Claude Tools (--claude-tools)
User's custom commands/agents (excludes cco-* files):
- Token efficiency
- Redundant instructions
- Verbose examples

---

## System Prompt Awareness

Detects CLAUDE.md content that duplicates system prompt:

| Topic | System Prompt Already Covers |
|-------|------------------------------|
| Git commits | Workflow, format, hooks |
| PRs | Creation, format |
| Tool usage | Bash, Read, Write, Edit |
| File operations | Discovery, exclusions |
| Task management | TodoWrite |

**If found in CLAUDE.md**: Recommend removal (duplicate)

---

## Output Format

```markdown
# Optimization Results

**Mode:** {mode}
**Tokens:** {before} → {after} ({reduction}% saved)

## Applied
✓ {file}: {optimization} (-{tokens} tokens)

## Skipped
⏭ {file}: {reason}

## Verification
applied + skipped + rolled_back = total ✓
Quality: preserved ✓

## Next Steps
→ Review: git diff
→ Commit: /cco-commit
```

---

## Usage

```bash
/cco-optimize                 # Interactive
/cco-optimize --context       # Context files only
/cco-optimize --code-quality  # Code only
/cco-optimize --performance   # Performance only
/cco-optimize --markdown      # All markdown
/cco-optimize --claude-tools  # User's custom tools
/cco-optimize --all           # Everything
/cco-optimize --conservative  # Safe only
/cco-optimize --balanced      # Safe + low-risk
/cco-optimize --aggressive    # All (manual review)
```

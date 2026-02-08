# Contributing to CCO

Thanks for your interest in contributing!

## Quick Start

```bash
# Clone
git clone https://github.com/sungurerdim/ClaudeCodeOptimizer.git
cd ClaudeCodeOptimizer
```

## File Naming

| Type | Pattern | Location |
|------|---------|----------|
| Commands | `cco-{name}.md` | `commands/` |
| Agents | `cco-agent-{name}.md` | `agents/` |
| Rules | `cco-rules.md` | `rules/` |

## Making Changes

### Adding/Modifying Rules

1. Edit `rules/cco-rules.md` (single source of truth)
2. Update `docs/rules.md` to reflect changes

Rule categories: Focus and Discipline, Code Quality, Security, Workflow, CCO Operations.

### Updating Documentation

Keep counts in sync when adding/removing files:

```bash
# Verify counts (cross-platform: use Glob in Claude Code)
# Commands: 8 (optimize, align, commit, research, docs, blueprint, pr, update)
# Agents: 3 (analyze, apply, research)
```

Update `README.md` and `docs/` if counts change.

## Pull Request Guidelines

1. **Run validation** before submitting:
   ```bash
   # Verify all files exist
   ls rules/cco-rules.md
   ls commands/cco-*.md | wc -l   # Should be 8
   ls agents/cco-agent-*.md | wc -l  # Should be 3
   ```

2. **One feature per PR** — keep changes focused

3. **Update docs** if adding commands, agents, or rules

4. **Follow existing patterns** — check similar files for conventions

## Code Style

- Markdown: CommonMark, ATX headers (`#` not `===`)
- YAML frontmatter for commands and agents
- Tables for structured data
- No trailing whitespace

## Testing

- CI validates file structure, frontmatter, and version consistency
- All checks must pass before merge

## Questions?

Open an issue at [github.com/sungurerdim/ClaudeCodeOptimizer/issues](https://github.com/sungurerdim/ClaudeCodeOptimizer/issues)

# Contributing to CCO

Thanks for your interest in contributing!

## Quick Start

```bash
# Clone
git clone https://github.com/sungurerdim/ClaudeCodeOptimizer.git
cd ClaudeCodeOptimizer

# Run tests
python -m pytest tests/ -v

# Validate schemas
python -c "import json; json.load(open('.claude-plugin/plugin.json'))"
python -c "import json; json.load(open('hooks/core-rules.json'))"
```

## File Naming

| Type | Pattern | Location |
|------|---------|----------|
| Rules | `cco-{name}.md` | `rules/{category}/` |
| Commands | `{name}.md` | `commands/` |
| Agents | `cco-agent-{name}.md` | `agents/` |

**All rule files require `cco-` prefix.**

## Making Changes

### Adding/Modifying Rules

1. Edit files in `rules/core/`, `rules/languages/`, `rules/frameworks/`, or `rules/operations/`
2. If modifying core rules, regenerate hooks:
   - Concatenate into `hooks/core-rules.json` under `additionalContext`
   - Validate JSON before committing

### Updating Documentation

Keep counts in sync when adding/removing files:

```bash
# Verify counts match docs
ls commands/*.md | wc -l    # Should match "Commands: 7"
ls agents/*.md | wc -l       # Should match "Agents: 3"
find rules -name "cco-*.md" | wc -l  # Should match "Rules: 44"
```

Update `README.md` and `docs/` if counts change.

## Pull Request Guidelines

1. **Run tests** before submitting:
   ```bash
   python -m pytest tests/ -v
   ```

2. **One feature per PR** — keep changes focused

3. **Update docs** if adding commands, agents, or rules

4. **Follow existing patterns** — check similar files for conventions

## Code Style

- Markdown: CommonMark, ATX headers (`#` not `===`)
- YAML frontmatter for commands
- Tables for structured data
- No trailing whitespace

## Testing

- Tests verify file counts and schema validity
- CI runs on every push
- All tests must pass before merge

## Questions?

Open an issue at [github.com/sungurerdim/ClaudeCodeOptimizer/issues](https://github.com/sungurerdim/ClaudeCodeOptimizer/issues)

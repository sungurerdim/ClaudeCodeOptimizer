# CCO Development

## Commands

```bash
# Run tests
python -m pytest tests/ -v

# Validate JSON schemas
python -c "import json; json.load(open('.claude-plugin/plugin.json'))"
python -c "import json; json.load(open('hooks/core-rules.json'))"

# Count rules (for doc sync)
find rules -name "cco-*.md" | wc -l
```

## File Naming

- All rule files: `cco-{name}.md` prefix required
- Commands: `commands/{name}.md` with YAML frontmatter
- Agents: `agents/cco-agent-{name}.md`

## Updating Core Rules

When modifying `rules/core/cco-*.md` files, regenerate hooks:

1. Edit source files in `rules/core/`
2. Concatenate into `hooks/core-rules.json` under `additionalContext`
3. Verify JSON is valid before committing

## Doc Sync

Counts in README.md and docs/ must match actual files:
- Commands: 7 (`ls commands/*.md | wc -l`)
- Agents: 3 (`ls agents/*.md | wc -l`)
- Rules: 44 (`find rules -name "cco-*.md" | wc -l`)

Update docs when adding/removing files.

## Testing

- Run full test suite before PR
- Tests verify file counts and schema validity
- CI runs tests on every push

## Plugin Structure

```
.claude-plugin/       # Plugin manifest
commands/             # Slash commands with frontmatter
agents/               # Subagent definitions
rules/                # Rule files (core, languages, frameworks, operations)
hooks/                # SessionStart hook with core-rules.json
```

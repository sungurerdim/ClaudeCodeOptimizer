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
| Skills | `cco-{name}/SKILL.md` | `skills/` |
| Agents | `cco-agent-{name}.md` | `agents/` |
| Rules | `cco-rules.md` | `rules/` |

## Making Changes

### Adding/Modifying Rules

1. Edit `rules/cco-rules.md` (single source of truth)
2. Update `docs/rules.md` to reflect changes

Rule categories: Scope Control, Code Integrity, Production Standards, Output Brevity, Verification, Uncertainty Protocol, Session Resilience, Process Discipline, CCO Operations.

### Adding a New Skill

1. Create `skills/cco-{name}/SKILL.md` with YAML frontmatter
2. Update `extras/installer/main.go` file manifest
3. Update `skills/cco-update/SKILL.md` file manifest
4. Update `docs/skills.md` and `docs/agents.md` if applicable

### Updating Documentation

Keep counts in sync when adding/removing files:

```bash
# Verify counts (cross-platform: use Glob in Claude Code)
# Skills: 8 (optimize, align, commit, research, docs, blueprint, pr, update)
# Agents: 3 (analyze, apply, research)
```

Update `README.md` and `docs/` if counts change.

## Pull Request Guidelines

1. **Run validation** before submitting:

   > **Windows:** Use Git Bash or WSL for verification commands.

   ```bash
   # Verify all files exist
   ls rules/cco-rules.md
   ls skills/cco-*/SKILL.md | wc -l   # Should be 8
   ls agents/cco-agent-*.md | wc -l   # Should be 3
   ```

2. **One feature per PR** — keep changes focused

3. **Update docs** if adding skills, agents, or rules

4. **Follow existing patterns** — check similar files for conventions

## Code Style

- Markdown: CommonMark, ATX headers (`#` not `===`)
- YAML frontmatter for skills and agents
- Tables for structured data
- No trailing whitespace

## Testing

- CI validates file structure, frontmatter, and version consistency
- Go code in `extras/` is built and tested in CI
- All checks must pass before merge

## Questions?

Open an issue at [github.com/sungurerdim/ClaudeCodeOptimizer/issues](https://github.com/sungurerdim/ClaudeCodeOptimizer/issues)

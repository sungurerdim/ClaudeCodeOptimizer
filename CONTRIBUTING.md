# Contributing to ClaudeCodeOptimizer

Thank you for your interest in contributing to ClaudeCodeOptimizer! This document provides guidelines and instructions for contributing.

## Development Environment Setup

### Prerequisites

- Python 3.10 or higher
- Git
- pip

### Installation

1. Clone the repository:
```bash
git clone https://github.com/sungurerdim/ClaudeCodeOptimizer.git
cd ClaudeCodeOptimizer
```

2. Install in development mode with dev dependencies:
```bash
pip install -e ".[dev]"
```

## Code Style Requirements

We enforce strict code quality standards:

### Linting & Formatting

- **Ruff**: Primary linter and formatter
  ```bash
  ruff check .
  ruff format .
  ```

- **Mypy**: Type checking (strict mode for new files)
  ```bash
  mypy claudecodeoptimizer/
  ```

### Code Quality Standards

- **Type Hints**: All new code must include type annotations
- **Line Length**: Max 100 characters
- **Import Organization**: Managed by ruff (isort rules)
- **Security**: No S-level violations (bandit security rules)

## Testing Requirements

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=claudecodeoptimizer --cov-report=term-missing

# Run parallel tests
pytest -n auto
```

### Test Coverage Standards

- **Minimum Coverage**: 80% overall (current: 100%)
- **Critical Modules**: 90%+ coverage required
  - `install_hook.py`
  - `cco_remove.py`
  - `config.py`

### Writing Tests

- Use `pytest` framework
- Follow naming convention: `test_*.py`
- Use descriptive test names: `test_creates_claude_md_with_rules`
- Include docstrings for complex test scenarios
- Use fixtures for shared test data

## Git Workflow

### Branch Naming

- Feature: `feat/description`
- Fix: `fix/description`
- Refactor: `refactor/description`
- Docs: `docs/description`

### Commit Message Format

We follow Conventional Commits with strict formatting:

```
type(scope): concise description (max 72 chars)

- Max 5 bullet points (most important changes only)
- One line per bullet
- Focus on "why" not "what"
- Max 10 lines total

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `refactor`: Code restructuring
- `docs`: Documentation changes
- `test`: Test additions/changes
- `chore`: Maintenance tasks
- `perf`: Performance improvements

**Examples:**

✅ **Good:**
```
feat(wizard): add native Claude Code UI support

- Create UIAdapter for AskUserQuestion tool integration
- Add automatic fallback to terminal prompts
- Implement rich option formatting with context
```

❌ **Bad:**
```
Update files

- Changed wizard.py
- Fixed some bugs
- Updated docs
- Refactored code
- Added tests
- Improved performance
```

### Pull Request Guidelines

1. **Before Submitting**:
   - Run all tests locally: `pytest`
   - Run linting: `ruff check . && mypy claudecodeoptimizer/`
   - Ensure coverage meets minimum: `pytest --cov`
   - Update documentation if needed

2. **PR Description**:
   - Clear summary of changes
   - Link related issues
   - Include test plan
   - Note any breaking changes

3. **Review Process**:
   - All CI checks must pass
   - At least one maintainer approval required
   - Address review feedback promptly

## Development Principles

This project follows CCO Rules documented in `~/.claude/CLAUDE.md`:

- **Cross-Platform**: Forward slashes, relative paths, Git Bash commands
- **Reference Integrity**: Find ALL refs before delete/rename/move/modify
- **Verification**: Accounting formula: total = completed + skipped + failed + cannot-do
- **File Discovery**: files_with_matches → content with -C → Read offset+limit
- **Change Safety**: Commit before bulk changes, max 10 files per batch
- **Scope Control**: Define boundaries, one change = one purpose

## Local Testing Checklist

Before submitting a PR, verify:

- [ ] All tests pass: `pytest -v`
- [ ] Coverage meets minimum: `pytest --cov`
- [ ] No linting errors: `ruff check .`
- [ ] No type errors: `mypy claudecodeoptimizer/`
- [ ] Code formatted: `ruff format --check .`
- [ ] Documentation updated (if applicable)
- [ ] Commit messages follow convention

## Project Structure

```
ClaudeCodeOptimizer/
├── claudecodeoptimizer/     # Main package
│   ├── content/             # Knowledge base (deployed to ~/.claude/)
│   │   ├── command-templates/  # Slash commands (cco-*.md)
│   │   ├── agent-templates/    # Autonomous agents (cco-agent-*.md)
│   │   ├── rules/              # Rules files (cco-core.md, cco-ai.md, cco-tools.md, cco-adaptive.md)
│   │   ├── permissions/        # Permission presets (safe.json, balanced.json, etc.)
│   │   └── statusline/         # Statusline configs (full.js, minimal.js)
│   ├── __init__.py          # Package init, version
│   ├── __main__.py          # CLI entry
│   ├── config.py            # Configuration paths
│   ├── install_hook.py      # Setup/deployment
│   └── cco_remove.py        # Remove command
└── tests/                   # Test suite
    ├── unit/                # Unit tests
    └── integration/         # Integration tests
```

## CLAUDE.md Marker System

CLAUDE.md uses a **marker-based system** with 4 rule categories:

### Global Rules (`~/.claude/CLAUDE.md`)

```markdown
<!-- CCO_CORE_START -->
# Core Rules
...
<!-- CCO_CORE_END -->

<!-- CCO_AI_START -->
# AI Rules
...
<!-- CCO_AI_END -->
```

### Project Rules (`./CLAUDE.md`)

```markdown
<!-- CCO_ADAPTIVE_START -->
## Strategic Context
Purpose: {purpose}
Team: {team} | Scale: {scale} | ...
<!-- CCO_ADAPTIVE_END -->
```

### Tools Rules (loaded on-demand by commands/agents)

Located in `~/.claude/rules/cco-tools.md`, loaded via `!` backtick syntax.

### Generator Rules

1. **Original Content Preservation**: Content outside markers is NEVER modified
2. **Empty Line Normalization**: Multiple consecutive empty lines → single empty line
3. **Update Strategy**:
   - Standards: Global ~/.claude/CLAUDE.md
   - Context: Local ./CLAUDE.md per project

## Getting Help

- **Issues**: https://github.com/sungurerdim/ClaudeCodeOptimizer/issues
- **Discussions**: GitHub Discussions
- **Documentation**: README.md and inline docs

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

# Contributing to ClaudeCodeOptimizer

Thank you for your interest in contributing to ClaudeCodeOptimizer! This document provides guidelines and instructions for contributing.

## Development Environment Setup

### Prerequisites

- Python 3.11 or higher
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

3. Install pre-commit hooks:
```bash
pre-commit install
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

- **Minimum Coverage**: 80% overall (current: 84%)
- **Critical Modules**: 90%+ coverage required
  - `core/knowledge_setup.py`
  - `cco_remove.py`
  - `cco_status.py`
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
- [ ] Code formatted: `ruff format .`
- [ ] Pre-commit hooks pass: `pre-commit run --all-files`
- [ ] Documentation updated (if applicable)
- [ ] Commit messages follow convention

## Project Structure

```
ClaudeCodeOptimizer/
├── claudecodeoptimizer/     # Main package
│   ├── core/                # Core functionality
│   │   ├── knowledge_setup.py      # Setup and deployment
│   │   └── ...                     # Other core modules
│   ├── content/             # Knowledge base (deployed to ~/.claude/)
│   │   ├── commands/        # Slash commands (cco-*.md)
│   │   ├── agents/          # Autonomous agents (cco-agent-*.md)
│   │   └── templates/       # Template files
│   ├── cco_status.py        # Status command
│   ├── cco_remove.py        # Remove command
│   └── config.py            # Configuration
└── tests/                   # Test suite
    ├── unit/                # Unit tests
    └── integration/         # Integration tests
```

## CLAUDE.md Generation

CLAUDE.md uses a **marker-based system** for CCO Rules:

### Marker Structure

CCO Rules content is within HTML comment markers:
```markdown
<!-- CCO_RULES_START -->
# CCO Rules
...
<!-- CCO_RULES_END -->
```

### Generator Rules

1. **Original Content Preservation**: Content outside markers is NEVER modified
2. **Empty Line Normalization**: Multiple consecutive empty lines → single empty line
3. **Update Strategy**:
   - New file: Create with CCO Rules markers
   - Existing file: Update marker content only

## Getting Help

- **Issues**: https://github.com/sungurerdim/ClaudeCodeOptimizer/issues
- **Discussions**: GitHub Discussions
- **Documentation**: README.md and inline docs

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

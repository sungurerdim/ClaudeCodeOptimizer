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
  - `core/principle_loader.py`
  - `core/remove.py`
  - `schemas/commands.py`
  - `schemas/preferences.py`

### Writing Tests

- Use `pytest` framework
- Follow naming convention: `test_*.py`
- Use descriptive test names: `test_filter_principles_by_category`
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

This project follows strict development principles documented in `~/.claude/principles/`:

### Universal Principles (cco-principle-u-*)

- **cco-principle-u-dry**: Single source of truth, no duplication
- **cco-principle-u-minimal-touch**: Change only what's necessary
- **cco-principle-u-evidence-based-analysis**: Verify changes with concrete evidence
- **cco-principle-u-change-verification**: Verify all changes before claiming completion
- **cco-principle-u-follow-patterns**: Follow existing code patterns
- **cco-principle-u-no-overengineering**: Keep solutions simple

### Claude-Specific Principles (cco-principle-c-*)

- **cco-principle-c-context-window-mgmt**: Optimize context window usage
- **cco-principle-c-efficient-file-operations**: Grep-first, targeted reads
- **cco-principle-c-native-tool-interactions**: Use native Claude Code tools
- **cco-principle-c-no-unsolicited-file-creation**: No unnecessary file creation
- **cco-principle-c-project-context-discovery**: Discover project context first

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
│   │   ├── principle_loader.py     # Principle loading
│   │   ├── principles.py           # Principle management
│   │   ├── remove.py               # Uninstallation
│   │   ├── version_manager.py      # Version tracking
│   │   └── utils.py                # Utilities
│   ├── schemas/             # Data schemas
│   │   ├── commands.py             # Command metadata
│   │   └── preferences.py          # User preferences
│   ├── cco_status.py        # Status command
│   ├── cco_remove.py        # Remove command
│   ├── commands_loader.py   # Command loading
│   └── config.py            # Configuration
├── content/                 # Knowledge base (deployed to ~/.claude/)
│   ├── commands/            # Slash commands (cco-*.md)
│   ├── principles/          # Development principles (U_*, C_*, P_*.md)
│   ├── skills/              # Reusable skills (cco-skill-*.md)
│   └── agents/              # Autonomous agents (cco-agent-*.md)
└── tests/                   # Test suite
    ├── unit/                # Unit tests
    └── integration/         # Integration tests
```

## CLAUDE.md Generation

CLAUDE.md is generated using a **marker-based system** that preserves all user content:

### Marker Structure

All CCO-managed content is within HTML comment markers:
```markdown
<!-- CCO_HEADER_START -->
# Claude Code Development Guide
**Project:** YourProject | **Team:** Solo Developer
<!-- CCO_HEADER_END -->

<!-- CCO_PRINCIPLES_START -->
## Development Principles
...
<!-- CCO_PRINCIPLES_END -->
```

**Available Markers:**
- `CCO_HEADER`: Project metadata and title
- `CCO_PRINCIPLES`: Universal, project-specific, and Claude guidelines
- `CCO_SKILLS`: Selected skills
- `CCO_AGENTS`: Selected agents
- `CCO_COMMANDS`: Available slash commands
- `CCO_GUIDES`: Available guides
- `CCO_CLAUDE`: Claude-specific guidelines

### Generator Rules

1. **Original Content Preservation**: Content outside markers is NEVER modified
2. **Title Reading**: Titles are read from frontmatter (not hardcoded)
   - Principles: `title:` field
   - Skills: `metadata.name:` field
   - Agents: `name:` field
   - Commands: `title:` field
   - Guides: First `# Header` in markdown
3. **Empty Line Normalization**: Multiple consecutive empty lines → single empty line
4. **Update Strategy**:
   - New file: Create with all markers
   - Existing file: Update marker content only

### Testing CLAUDE.md Changes

When modifying `claude_md_generator.py`:
```bash
# Test generation
python -c "from pathlib import Path; from claudecodeoptimizer.core.claude_md_generator import ClaudeMdGenerator; ..."

# Verify markers
grep -n "CCO_.*_START\|CCO_.*_END" CLAUDE.md

# Check for multiple empty lines
python -c "print(Path('CLAUDE.md').read_text().count('\\n\\n\\n'))"  # Should be 0
```

## Getting Help

- **Issues**: https://github.com/sungurerdim/ClaudeCodeOptimizer/issues
- **Discussions**: GitHub Discussions
- **Documentation**: README.md and inline docs

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

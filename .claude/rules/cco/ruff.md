# Ruff Rules

- **Format**: ruff format . for code formatting (Black compatible)
- **Lint**: ruff check . for linting
- **Fix**: ruff check --fix for auto-fixable issues
- **Select**: Configure rule sets in pyproject.toml [tool.ruff.lint]
- **Ignore**: Document ignored rules with reason
- **Per-File**: Use per-file-ignores for specific exceptions
- **Line-Length**: Consistent line length (default 88, configurable)
- **Imports**: Auto-sort imports (isort compatible)
- **Unsafe-Fixes**: Review unsafe fixes before applying
- **Target-Version**: Set target-version for Python version-specific rules
- **Extend-Select**: Add additional rules beyond defaults
- **Preview**: Use --preview for experimental rules
- **Pyproject**: All configuration in pyproject.toml
- **Cache**: Respect .ruff_cache for faster runs

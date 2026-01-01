# Mypy Rules

- **Strict**: Enable strict mode when possible
- **Check-Untyped**: check_untyped_defs = true
- **Imports**: ignore_missing_imports for third-party libs without stubs
- **No-Implicit**: no_implicit_optional = true
- **Warn-Return**: warn_return_any = true for Any return values
- **Warn-Unreachable**: warn_unreachable = true
- **Incremental**: Use incremental mode for faster checks
- **Cache**: Respect .mypy_cache
- **Python-Version**: Set python_version to match project
- **Exclude**: Exclude tests from strict checks if needed
- **Reveal-Type**: Use reveal_type() for debugging
- **Type-Ignore**: Minimize # type: ignore, document when used
- **Overload**: Use @overload for multiple signatures
- **Generic**: Use TypeVar for generic functions/classes
- **Final**: Use Final for constants
- **Literal**: Use Literal for specific values

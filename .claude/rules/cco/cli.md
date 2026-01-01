# CLI Rules

- **Entry-Point-Clear**: Define all CLI entry points in pyproject.toml[project.scripts]
- **Help-Documentation**: Include --help with clear descriptions of all commands and options
- **Exit-Codes**: Use meaningful exit codes (0 success, 1 usage error, 2 execution error)
- **Input-Validation**: Validate all user input (arguments, options) at entry point
- **Output-Consistent**: Consistent output format (JSON for machines, formatted text for humans)
- **Error-Messages**: Clear, actionable error messages with context
- **Progress-Feedback**: Show progress for long operations (spinner, percentage, ETA)
- **Config-File**: Support config file for non-interactive defaults
- **Environment-Vars**: Document environment variables affecting CLI behavior
- **Subcommands-Organize**: Use subcommands to organize related functionality
- **Type-Safety**: Type hints for all CLI functions, validate arg types

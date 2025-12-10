# Core Rules
*Fundamental principles for all software projects*

## Code Quality

- **Fail-Fast**: No silent fallbacks, immediate visible failure
- **DRY**: Single source of truth, no duplicates
- **No-Orphans**: Every function called, every import used
- **Type-Safe**: Annotations where supported, prefer immutable
- **Complexity**: Cyclomatic <10 per function
- **Clean**: Meaningful names, single responsibility, consistent style
- **Explicit**: No magic values, clear intent
- **Scope**: Only requested changes, general solutions

## File & Resource

- **Minimal-Touch**: Only files required for task
- **No-Unsolicited**: Never create files unless requested
- **Paths**: Forward slash, relative, quote spaces
- **Cleanup**: Temp files, handles, connections
- **Skip-VCS**: .git/, .svn/, .hg/
- **Skip-Deps**: node_modules/, vendor/, .venv/, venv/
- **Skip-Build**: dist/, build/, out/, target/, .next/, __pycache__/
- **Skip-IDE**: .idea/, .vscode/, .vs/
- **Skip-Generated**: *.min.js, *.min.css, *.generated.*, files with `@generated` header

## Security

- **Secrets**: Env vars or vault only
- **Input**: Validate at system boundaries
- **Access**: Least privilege, secure defaults
- **Deps**: Review before adding, keep updated
- **Defense**: Multiple layers, don't trust single control

## Testing

- **Coverage**: 60-90% context-adjusted
- **Isolation**: No inter-test deps, reproducible
- **Integrity**: Never edit tests to pass code
- **Critical-Paths**: E2E for critical workflows

## Error Handling

- **Catch**: Log context, recover or propagate
- **No-Silent**: Never swallow exceptions
- **User-Facing**: Clarity + actionable
- **Logs**: Technical details only
- **Rollback**: Consistent state on failure

## Documentation

- **README**: Description, setup, usage
- **CHANGELOG**: Versions with breaking changes
- **Comments**: Why not what
- **Examples**: Working, common use cases

## Workflow

- **Conventions**: Match existing patterns
- **Reference-Integrity**: Find ALL refs, update, verify
- **Decompose**: Break complex tasks into steps
- **Version**: SemVer (MAJOR.MINOR.PATCH)

## UX/DX

- **Minimum-Friction**: Fewest steps to goal
- **Maximum-Clarity**: Unambiguous output
- **Predictable**: Consistent behavior

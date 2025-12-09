---
name: cco-generate
description: Convention-following code and artifact generation
allowed-tools: Read(*), Grep(*), Glob(*), Write(*), Bash(git:*), Bash(pytest:*), Bash(npm:*), Task(*)
---

# /cco-generate

**Smart Generation** - Analyze patterns → generate consistent code → verify.

End-to-end: Discovers conventions, generates matching code, verifies it works.

**Standards:** Command Flow | Approval Flow | Output Formatting

## Context

- Stack: !`grep "^Stack:" ./CLAUDE.md 2>/dev/null`
- Type: !`grep "^Type:" ./CLAUDE.md 2>/dev/null`
- Conventions: !`grep -A2 "^Conventions:" ./CLAUDE.md 2>/dev/null`
- Test framework: !`ls **/test*.py **/test*.ts **/*.test.* 2>/dev/null | head -3`

## Context Application

| Field | Effect |
|-------|--------|
| Conventions | Use testNaming, importStyle from Operational section |
| Type | CLI: argparse/click; API: endpoints + OpenAPI; Frontend: components + stories |
| Stack | Use detected frameworks for idiomatic generation |
| Priority | Speed → minimal scaffolding; Quality → comprehensive with edge cases |
| Maturity | Legacy → match existing patterns exactly; Greenfield → modern idioms |
| Scale | 10K+ → add monitoring, health checks, metrics; <100 → minimal infra |
| Data | PII → encryption helpers, audit logging; Regulated → compliance boilerplate |

## Agent Integration

| Phase | Agent | Scope | Purpose |
|-------|-------|-------|---------|
| Discover | `cco-agent-analyze` | `conventions` | Pattern and convention discovery |
| Generate | `cco-agent-apply` | `generate` | Create files following conventions |

**Convention Discovery:** Use `cco-agent-analyze` with `scope: conventions` to discover naming patterns, test styles, import conventions, docstring formats, and error handling patterns before generating any code.

## Default Behavior

When called without flags, ask:

| Question | Options (multiSelect) |
|----------|----------------------|
| What to generate? | Tests, Docs, Infra, Boilerplate, All |

Explicit flags skip questions.

## Categories

### Tests (`--tests`)

Generate tests matching existing patterns:

| Type | Generation |
|------|------------|
| Unit tests | For uncovered public functions |
| Edge cases | Boundary conditions for existing tests |
| Integration | API endpoint tests |
| Property-based | Hypothesis/fast-check for pure functions |
| Snapshot | UI component stability tests |

**Sub-categories:** All | Unit | Integration | Property | Snapshot

Convention enforcement:
1. Discover test structure (`tests/`, `__tests__/`, `*.test.*`)
2. Match naming (`test_*.py`, `*.test.ts`)
3. Use same assertion library
4. Follow AAA pattern: Arrange → Act → Assert

### Docs (`--docs`)

Generate documentation:

| Type | Generation |
|------|------------|
| Docstrings | Match project style (Google, NumPy, JSDoc) |
| README sections | Usage, API, Examples |
| OpenAPI | Extract from route decorators (if API) |
| Changelog entries | From git commits since last tag |
| Type stubs | `.pyi` files for untyped code |

**Sub-categories:** All | Docstrings | README | OpenAPI | Changelog | Types

### Infra (`--infra`)

Generate infrastructure:

| Type | Generation |
|------|------------|
| CI/CD | GitHub Actions, GitLab CI, etc. |
| Dockerfile | Multi-stage, non-root, health check |
| Pre-commit | Hooks for lint, format, test |
| Makefile/Taskfile | Common commands |
| devcontainer | VS Code dev container config |

**Sub-categories:** All | CI/CD | Docker | Hooks | Makefile | Devcontainer

### Boilerplate (`--boilerplate`)

Generate new components from patterns:

| Type | Generation |
|------|------------|
| Module | New module from existing patterns |
| Endpoint | New API endpoint (if API type) |
| Component | New UI component (if Frontend type) |
| Command | New CLI command (if CLI type) |

Interactive prompts for specifics (name, location, etc.)

## Convention Enforcement

Before generating:
1. Analyze existing patterns
2. Match naming conventions exactly
3. Use same libraries/frameworks
4. Follow project structure
5. Never impose new conventions

## Flow

1. **Discover** - Analyze existing patterns
2. **Plan** - Show what will be generated
3. **Confirm** - User approval
4. **Generate** - Create files
5. **Verify** - Tests pass, no import errors

## Output

### Generation Plan
```
┌─ GENERATION PLAN ────────────────────────────────────────────┐
│ Type       │ Target              │ Convention    │ Status    │
├────────────┼─────────────────────┼───────────────┼───────────┤
│ Unit Test  │ auth.py             │ test_*.py     │ PLANNED   │
│ Unit Test  │ api.py              │ test_*.py     │ PLANNED   │
│ Docstring  │ utils.py:parse()    │ Google style  │ PLANNED   │
│ OpenAPI    │ routes/             │ openapi.yaml  │ PLANNED   │
└────────────┴─────────────────────┴───────────────┴───────────┘
```

### Files Created
```
┌─ FILES CREATED ──────────────────────────────────────────────┐
│ File                    │ Lines │ Description                │
├─────────────────────────┼───────┼────────────────────────────┤
│ tests/test_auth.py      │ 45    │ 3 test cases              │
│ tests/test_api.py       │ 82    │ 5 test cases              │
│ docs/openapi.yaml       │ 120   │ 8 endpoints               │
└─────────────────────────┴───────┴────────────────────────────┘
```

### Verification
```
Created: 3 | Tests: PASS | Imports: OK | Lint: CLEAN
```

## Flags

| Flag | Effect |
|------|--------|
| `--tests` | Generate tests |
| `--docs` | Generate documentation |
| `--infra` | Generate infrastructure |
| `--boilerplate` | Generate new components |
| `--all` | Everything applicable |
| `--dry-run` | Show plan without creating |

## Usage

```bash
/cco-generate                  # Interactive
/cco-generate --tests          # Unit/integration tests
/cco-generate --docs           # Docstrings, README, OpenAPI
/cco-generate --infra          # CI/CD, Dockerfile, hooks
/cco-generate --boilerplate    # New module/component
/cco-generate --all            # Everything applicable
/cco-generate --tests --dry-run
```

## Related Commands

- `/cco-audit --tests` - Check test coverage gaps
- `/cco-commit` - Commit generated files

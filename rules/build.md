# Build Tools
*Build system and tooling rules*

## Monorepo (Build:Monorepo)
**Trigger:** {monorepo_configs}

- **Affected-Only**: Build only affected packages
- **Cache-Remote**: Remote build cache enabled
- **Deps-Graph**: Explicit dependency graph
- **Consistent-Versions**: Shared dependency versions
- **Package-Boundaries**: Clear ownership per package

## Bundler (Build:Bundler)
**Trigger:** {bundler_configs}

- **Tree-Shake**: Enable tree shaking
- **Code-Split**: Split by route/feature
- **Source-Maps**: Source maps for debugging
- **Minify-Prod**: Minify in production only

## Linter (Build:Linter)
**Trigger:** {linter_configs}

- **CI-Enforce**: Include lint step in CI pipeline
- **Auto-Fix**: Enable auto-fix for safe rules
- **Ignore-Explicit**: Document ignore patterns with reasons
- **Severity-Config**: Configure error vs warning levels

## Formatter (Build:Formatter)
**Trigger:** {formatter_configs}

- **Pre-Commit**: Include format check in pre-commit hooks
- **Config-Share**: Use shared config file for consistency

## TypeChecker (Build:TypeChecker)
**Trigger:** {typechecker_configs}

- **Strict-Enable**: Enable strict mode in config
- **Incremental**: Enable incremental compilation
- **CI-Check**: Include type check step in CI pipeline

## Make (Build:Make)
**Trigger:** {makefile}

- **Phony-Targets**: Declare .PHONY for non-file targets
- **Deps-Explicit**: Explicit dependency declarations
- **Vars-Override**: Use ?= for overridable variables
- **Silent-Prefix**: Use @ prefix for clean output

## Just (Build:Just)
**Trigger:** {justfile}

- **Recipe-Doc**: Document recipes with comments
- **Default-Recipe**: Set sensible default recipe
- **Deps-Chain**: Chain dependent recipes
- **Vars-Export**: Export variables to environment

## Task (Build:Task)
**Trigger:** {taskfile}

- **Task-Deps**: Declare task dependencies
- **Vars-Define**: Define reusable variables
- **Desc-Required**: Description for all tasks
- **Sources-Fingerprint**: Use sources for incremental builds

## Mise (Build:Mise)
**Trigger:** {mise_config}

- **Tool-Versions**: Pin tool versions explicitly
- **Env-Manage**: Manage environment variables
- **Tasks-Define**: Define project tasks
- **Plugins-Minimal**: Use minimal plugin set

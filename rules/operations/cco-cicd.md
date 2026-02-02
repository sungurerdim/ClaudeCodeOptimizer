# CI/CD & Build
*Pipeline and build system gotchas*

## GitHub Actions Gotchas
**Trigger:** {github_workflow_dir}

- **Matrix expansion silently skips**: `matrix: { os: [ubuntu-latest], node: [] }` produces zero jobs with no error. Always validate matrix isn't empty; use `fail-fast: false` if you want all combos to run
- **Cache key mismatch**: `hashFiles('**/package-lock.json')` misses workspace lockfiles in monorepos. Use `hashFiles('**/package-lock.json', '**/yarn.lock')` and include the runner OS in the key
- **Cache restore without save**: If a job fails before `actions/cache@v4` post step, the cache never saves. Use `actions/cache/save` explicitly after critical steps
- **Concurrency cancels wrong runs**: `concurrency: { group: ${{ github.ref }} }` cancels in-progress runs on same branch, including release builds. Scope groups tightly: `group: ${{ github.workflow }}-${{ github.ref }}`
- **`secrets` context is empty in reusable workflows**: You must explicitly pass secrets with `secrets: inherit` or map them individually
- **`GITHUB_TOKEN` permission drift**: Default permissions changed to read-only in new repos. Always declare `permissions:` at job level
- **`if: always()` vs `if: failure()`**: `always()` runs even on cancellation. Use `if: success() || failure()` to skip cancelled runs

## GitLab CI Gotchas
**Trigger:** {gitlab_config}

- **`rules:` vs `only:`**: Don't mix them -- `rules` completely replaces `only/except`. Mixed usage causes silent job skips
- **Cache is per-runner by default**: Jobs on different runners get cold caches. Use `key: { files: [...] }` with distributed cache (S3/GCS)
- **DAG with `needs:` skips stages**: `needs:` breaks the stage ordering contract. A job in stage `test` with `needs: [build-x]` runs as soon as `build-x` finishes, potentially before other `build` stage jobs

## Monorepo Gotchas
**Trigger:** {monorepo_configs}

- **Affected-only misses transitive deps**: `nx affected` / `turbo --filter=...[HEAD~1]` only catches direct changes. Verify your dep graph is complete: `nx graph` / `turbo run build --graph`
- **Phantom dependencies**: Package uses a dep hoisted by another workspace package. Works locally, breaks in CI with clean install. Use `pnpm` (strict isolation) or `eslint-plugin-import` to catch these
- **Workspace version conflicts**: Two packages requiring different major versions of a shared dep. Bundlers may silently pick one. Use `overrides`/`resolutions` intentionally, not accidentally

## Bundler Gotchas
**Trigger:** {bundler_configs}

- **Tree-shaking fails on side effects**: Barrel files (`export * from`) defeat tree-shaking. Mark packages `"sideEffects": false` in package.json, or avoid barrel re-exports
- **Dynamic `import()` breaks code splitting**: `import(variable)` can't be statically analyzed -- bundles everything in the directory. Use explicit paths: `import(`./pages/${name}.js`)`
- **Source maps in production**: Shipping `.map` files exposes source code. Use `hidden-source-map` (Webpack) or `sourcemap: 'hidden'` (Vite) for error tracking without exposure

## One-Liners

- Linters in CI: fail on warnings (`--max-warnings 0`), don't just error
- Type checkers: enable strict mode, run incrementally, include in CI
- Formatters: check in CI (`--check`), auto-fix in pre-commit hooks
- Make: always declare `.PHONY` for non-file targets

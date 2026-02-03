# Troubleshooting

Common issues and solutions.

---

## Installation Issues

### Commands not appearing

**Symptoms:** `/cco:` commands don't show in autocomplete.

**Solutions:**

1. **Restart Claude Code** after installation
   ```
   Close and reopen Claude Code
   ```

2. **Verify plugin is installed:**
   ```
   /plugin
   ```
   Check **Installed** tab for `cco@ClaudeCodeOptimizer`

3. **Reinstall:**
   ```
   /plugin uninstall cco@ClaudeCodeOptimizer
   /plugin install cco@ClaudeCodeOptimizer
   ```

4. **Check marketplace:**
   ```
   /plugin marketplace add sungurerdim/ClaudeCodeOptimizer
   ```

### Plugin install fails

**Symptoms:** Error during `/plugin install`.

**Solutions:**

1. Remove and re-add from marketplace:
   ```
   /plugin marketplace remove ClaudeCodeOptimizer
   /plugin marketplace add sungurerdim/ClaudeCodeOptimizer
   /plugin install cco@ClaudeCodeOptimizer
   ```

2. Check network connectivity to GitHub

---

## Command Issues

### Command hangs or times out

**Symptoms:** Command doesn't complete.

**Solutions:**

1. **Check project size** - Large projects take longer
2. **Use scope flags:**
   ```
   /cco:optimize --scope=security  # Single scope faster
   ```
3. **Use quick mode:**
   ```
   /cco:align --preview
   ```

### "Applied: 0" when issues exist

**Symptoms:** Command reports no fixes but issues remain.

**Solutions:**

1. **Check intensity level:**
   ```
   /cco:optimize --auto  # All severities, unattended
   ```

2. **Check scope selection** - Issues might be in unselected scope

3. **Use report mode to see findings:**
   ```
   /cco:optimize --preview
   ```

### Git state warnings

**Symptoms:** "Uncommitted changes detected"

**Solutions:**

1. **Commit current changes:**
   ```bash
   git add -A && git commit -m "WIP"
   ```

2. **Stash changes:**
   ```bash
   git stash
   # Run CCO commands
   git stash pop
   ```

3. **Continue anyway** - Select "Continue" when prompted

---

## Quality Gate Issues

### Format/Lint/Type commands not found

**Symptoms:** Gates fail with "command not found".

**Solutions:**

1. **Check your package.json or pyproject.toml** for scripts
2. **Install missing tools:**
   ```bash
   pip install black ruff mypy pytest  # Python
   npm install -D prettier eslint      # Node.js
   ```

### Tests fail during commit

**Symptoms:** `/cco:commit` blocked by test failures.

**Solutions:**

1. **Fix the tests first:**
   ```bash
   pytest tests/ -v
   ```

2. **Commit only staged changes:**
   ```
   /cco:commit --staged-only
   ```

3. **Run tests manually to see errors:**
   ```bash
   pytest tests/ -v --tb=short
   ```

---

## Agent Issues

### Agent returns empty results

**Symptoms:** Analysis finds nothing.

**Solutions:**

1. **Check skip patterns** - Agents skip:
   - `node_modules/`, `.venv/`, `dist/`, `build/`
   - Files with `# intentional`, `# noqa`, `# safe:`
   - Platform-specific code blocks

2. **Check file types** - Agents scan:
   - `.py`, `.js`, `.ts`, `.go`, `.rs`, `.java`
   - Not: `.min.js`, generated files

3. **Verify project has code:**
   ```bash
   find . -name "*.py" -o -name "*.ts" | head -20
   ```

### False positives

**Symptoms:** Agent reports issues that aren't issues.

**Solutions:**

1. **Add comments to silence:**
   ```python
   import msvcrt  # type: ignore  # Windows only
   ```

2. **Use intentional markers:**
   ```python
   # intentional: bare except for cleanup
   except:
       pass
   ```

3. **Report the false positive** - Open an issue on GitHub

---

## Recovery

### Undo CCO changes

| Situation | Command |
|-----------|---------|
| Revert one file | `git checkout -- {file}` |
| Revert all changes | `git checkout .` |
| Review changes | `git diff` |
| Undo last commit | `git reset --soft HEAD~1` |

### Remove CCO from project

**Uninstall plugin:**
```
/plugin uninstall cco@ClaudeCodeOptimizer
```

CCO doesn't write files to your project, so no cleanup needed.

---

## Debugging

### Enable verbose output

Most commands support `--preview` for dry-run:

```
/cco:optimize --preview   # Show findings without fixing
/cco:commit --preview     # Show plan without committing
/cco:preflight --preview  # Check without releasing
```

### View loaded rules

Core rules are injected via SessionStart hook automatically. Check your project's `.claude/rules/` for any custom rules you've added.

---

## FAQ

### "How do I see what rules are active?"

Core rules are injected via SessionStart hook. Any `.md` files in your project's `.claude/rules/` are also loaded by Claude Code.

### "Will CCO break my existing Claude rules?"

No. CCO core rules are injected via hook, not written to your project. Your custom rules in `.claude/rules/` are never touched.

### "Why does optimize report 0 applied?"

Check:
1. Intensity level - `quick-wins` filters heavily
2. Selected scopes - Issues might be in unselected scope
3. Use `--preview` to see what was analyzed

### "Can I run CCO in CI/CD?"

Yes. Use `--auto` flag:

```bash
claude code run "/cco:optimize --auto"
```

Exit codes: 0=OK, 1=WARN, 2=FAIL

---

## Getting Help

- **GitHub Issues:** [github.com/sungurerdim/ClaudeCodeOptimizer/issues](https://github.com/sungurerdim/ClaudeCodeOptimizer/issues)
- **Documentation:** [docs/](.)
- **README:** [../README.md](../README.md)

---

*Back to [README](../README.md)*

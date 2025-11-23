---
name: cco-update
description: Update CCO to latest version with automatic sync of all commands, skills, principles, and agents
action_type: update
keywords: [update, upgrade, sync, version, latest, install]
category: management
pain_points: []
---

# cco-update

**Update CCO to latest version with automatic sync.**
---

## Built-in References

**This command inherits standard behaviors from:**

- **[STANDARDS_COMMANDS.md](../STANDARDS_COMMANDS.md)** - Standard structure, execution protocol, file discovery
- **[STANDARDS_QUALITY.md](../STANDARDS_QUALITY.md)** - UX/DX, efficiency, simplicity, performance standards
- **[LIBRARY_PATTERNS.md](../LIBRARY_PATTERNS.md)** - Reusable patterns (Step 0, Selection, Accounting, Progress, Error Handling)
- **[STANDARDS_AGENTS.md](../STANDARDS_AGENTS.md)** - File discovery, model selection, parallel execution

**See these files for detailed patterns. Only command-specific content is documented below.**

---

## Purpose

Update CCO package and sync all commands, skills, principles, and agents to latest versions.

---

## Execution Protocol

### Step 1: Check Current Version

```bash
pip show claudecodeoptimizer | grep Version
```

### Step 2: Check for Updates

```bash
pip index versions claudecodeoptimizer
# Or check GitHub releases
gh release list --repo sungurerdim/ClaudeCodeOptimizer
```

### Step 3: Confirm Update

**See [LIBRARY_PATTERNS.md](../LIBRARY_PATTERNS.md#pattern-8-dynamic-results-generation) for reporting pattern.**

```markdown
CCO Update Available

Current version: {CURRENT_VERSION}
Latest version: {LATEST_VERSION}

Changes in {LATEST_VERSION}:
- {CHANGE_1}
- {CHANGE_2}
- {CHANGE_3}

What will be updated:
- CCO package: {current} → {latest}
- Commands: {count} files synced
- Skills: {count} files synced
- Principles: {count} files synced
- Agents: {count} files synced

All projects using CCO will get updates automatically.

AskUserQuestion({
  questions: [{
    question: "Update CCO to latest version?",
    header: "Update",
    multiSelect: false,
    options: [
      {label: "Yes", description: "Update all components"},
      {label: "Preview changes", description: "Show what will be updated"},
      {label: "Selective update", description: "Choose specific components"},
      {label: "No", description: "Cancel update"}
    ]
  }]
})
```

### Step 4: Run Update

Detect installation method and use appropriate update command:

**If installed with pip:**
```bash
pip install -U git+https://github.com/sungurerdim/ClaudeCodeOptimizer.git
```

**If installed with pipx:**
```bash
pipx upgrade claudecodeoptimizer
```

**If installed with uv:**
```bash
uv tool upgrade claudecodeoptimizer
```

### Step 5: Run Setup

After package update:
```bash
cco-setup --force
```

This syncs all files in ~/.claude/ to latest versions.

### Step 6: Verify Update

**Pattern:** Pattern 4 (Complete Accounting)

```markdown
Update Complete! ✓

Updated:
✓ CCO package: {OLD_VERSION} → {NEW_VERSION}
✓ Commands: {synced}/{total} synced
✓ Skills: {synced}/{total} synced
✓ Principles: {synced}/{total} synced
✓ Agents: {synced}/{total} synced

Changes:
- New skills:
  * {skill-1} ({description})
  * {skill-2} ({description})

- Updated principles:
  * {principle-1} ({change})
  * {principle-2} ({change})
  * ... ({count} more)

- Performance improvements:
  * {improvement-1}
  * {improvement-2}

All projects now use latest version ✓

Restart Claude Code to activate changes.

Release notes: https://github.com/sungurerdim/ClaudeCodeOptimizer/releases/tag/v{NEW_VERSION}
```

---

## Error Handling

**Pattern:** Pattern 5 (Error Handling)

**If update fails:**

```python
AskUserQuestion({
  questions: [{
    question: "Update failed: {error_type} - {error_message}. How to proceed?",
    header: "Update Error",
    multiSelect: false,
    options: [
      {label: "Retry", description: "Try update again"},
      {label: "Rollback", description: "Restore previous version"},
      {label: "Force sync", description: "Force sync (may overwrite local changes)"},
      {label: "Manual update", description: "Show manual update instructions"},
      {label: "Cancel", description: "Stop update"}
    ]
  }]
})
```

**Network failure retry strategy:**
- Retry up to 3 times with exponential backoff (1s, 2s, 4s)
- If all retries fail, offer manual download option

---

## Success Criteria

- [OK] Current version detected
- [OK] Latest version checked
- [OK] Changes summarized
- [OK] User confirmed update
- [OK] Package updated
- [OK] Files synced (cco-setup)
- [OK] Verification completed
- [OK] User informed of changes

---

## Example Usage

```bash
# Check and update
/cco-update

# After update, verify
/cco-status
```

---
name: cco-remove
description: Complete CCO uninstall with full transparency showing exactly what will be deleted before confirmation

keywords: [remove, uninstall, delete, cleanup, unset]
category: management
pain_points: []
---

# cco-remove

**Complete CCO uninstall with full transparency and confirmation.**
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

Remove CCO cleanly and completely, showing exactly what will be deleted before proceeding.

---

## Execution Protocol

### Step 1: Detect Installation

```bash
# Check package
pip show claudecodeoptimizer || pipx list | grep claudecodeoptimizer

# Check global directory
ls ~/.claude/
```

### Step 2: Show What Will Be Deleted

**See [LIBRARY_PATTERNS.md](../LIBRARY_PATTERNS.md#pattern-8-dynamic-results-generation) for reporting pattern.**

```markdown
============================================================
CCO UNINSTALL - PREVIEW
============================================================

The following will be PERMANENTLY DELETED:

PACKAGE:
  • claudecodeoptimizer (installed via pip/pipx/uv)
    Location: {PACKAGE_LOCATION}
    Version: {VERSION}

------------------------------------------------------------
GLOBAL DIRECTORY (~/.claude/)
------------------------------------------------------------

  • Agents: {AGENT_COUNT} files
  • Commands: {COMMAND_COUNT} files
  • Skills: {SKILL_COUNT} files
  • Principles: {PRINCIPLE_COUNT} files
    - U_*.md: {U_PRINCIPLE_COUNT} (Universal principles)
    - C_*.md: {C_PRINCIPLE_COUNT} (Claude guidelines)
    - P_*.md: {P_PRINCIPLE_COUNT} (Project principles)
  • Templates: {TEMPLATE_COUNT} files

------------------------------------------------------------
  Total: {TOTAL_COUNT} files in ~/.claude/
------------------------------------------------------------

CLAUDE.MD:
  • CCO principle markers will be removed from ~/.claude/CLAUDE.md
  • Your other content in CLAUDE.md will be preserved

PROJECT FILES:
  • NONE - Zero-pollution architecture
  • Your project files are NOT affected

WHAT WILL NOT BE DELETED:
  • Your code and project files
  • Git history
  • Other Python packages
  • IDE configurations
  • Non-CCO files in ~/.claude/ (preserved)

============================================================

AskUserQuestion({
  questions: [{
    question: "PERMANENT DELETION: This will remove ALL CCO files. This action CANNOT be undone. Are you absolutely sure?",
    header: "Confirm Deletion",
    multiSelect: false,
    options: [
      {label: "Yes, delete everything", description: "⚠️ PERMANENT - Removes all CCO"},
      {label: "Backup first", description: "Create backup before deletion"},
      {label: "Cancel", description: "Keep CCO installed"}
    ]
  }]
})
```

### Step 3: Execute Removal

**Remove package:**
```bash
# Detect method
if pip show claudecodeoptimizer:
    pip uninstall -y claudecodeoptimizer
elif pipx list | grep claudecodeoptimizer:
    pipx uninstall claudecodeoptimizer
elif uv tool list | grep claudecodeoptimizer:
    uv tool uninstall claudecodeoptimizer
```

**Remove global directory:**
```bash
# Backup first (if user selected)
mv ~/.claude/ ~/.claude.backup-$(date +%Y%m%d-%H%M%S)

# Or delete directly if user confirmed
rm -rf ~/.claude/
```

### Step 4: Verify Removal

**Pattern:** Pattern 4 (Complete Accounting)

```markdown
============================================================
CCO UNINSTALL COMPLETE
============================================================

REMOVED:
  ✓ Package: claudecodeoptimizer ({INSTALL_METHOD})
  ✓ Agents: {AGENT_COUNT} files deleted
  ✓ Commands: {COMMAND_COUNT} files deleted
  ✓ Skills: {SKILL_COUNT} files deleted
  ✓ Principles: {PRINCIPLE_COUNT} files deleted
  ✓ Templates: {TEMPLATE_COUNT} files deleted
  ✓ CLAUDE.md: CCO markers removed

------------------------------------------------------------
  Total: {TOTAL_COUNT} files deleted
------------------------------------------------------------

VERIFIED:
  ✓ pip show claudecodeoptimizer → Not found
  ✓ ~/.claude/agents/cco-*.md → 0 files
  ✓ ~/.claude/commands/cco-*.md → 0 files
  ✓ ~/.claude/skills/cco-*.md → 0 files
  ✓ ~/.claude/principles/[UCP]_*.md → 0 files
  ✓ ~/.claude/*.cco → 0 files
  ✓ Your project files → Intact (0 files touched)

============================================================

CCO has been completely removed from your system.

TO REINSTALL:
  pip install git+https://github.com/sungurerdim/ClaudeCodeOptimizer.git
  cco-setup

BACKUP (if created):
  ~/.claude.backup-{TIMESTAMP}

============================================================
```

---

## Error Handling

**Pattern:** Pattern 5 (Error Handling)

**If package not found:**
```markdown
[WARNING] CCO Package Not Found

The CCO package is not installed via pip/pipx/uv.

However, global directory exists: ~/.claude/
Current CCO files: {TOTAL_COUNT}

AskUserQuestion({
  questions: [{
    question: "CCO package not found, but global directory exists. Delete global CCO files only?",
    header: "Package Not Found",
    multiSelect: false,
    options: [
      {label: "Yes", description: "Delete global CCO files"},
      {label: "No", description: "Cancel deletion"}
    ]
  }]
})
```

**If removal fails:**
```python
AskUserQuestion({
  questions: [{
    question: "Removal failed for {N} files: {error_summary}. How to proceed?",
    header: "Removal Error",
    multiSelect: false,
    options: [
      {label: "Retry", description: "Try removing failed files again"},
      {label: "Force delete", description: "Force removal (may require admin permissions)"},
      {label: "Manual cleanup", description: "Show files to delete manually"},
      {label: "Leave as-is", description: "Keep remaining files"},
      {label: "Cancel", description: "Stop removal"}
    ]
  }]
})
```

---

## Safety Features

1. **Preview before delete:** Show exactly what will be removed
2. **Explicit confirmation:** Require explicit selection
3. **Optional backup:** Backup before deletion
4. **Verification:** Confirm removal completed
5. **Zero project pollution:** Only CCO files removed, no project files

---

## Success Criteria

- [OK] Installation detected (package + directory)
- [OK] Complete list of files shown
- [OK] User sees what will be deleted
- [OK] Explicit confirmation required
- [OK] Package uninstalled
- [OK] Directory removed
- [OK] Removal verified
- [OK] Reinstall instructions provided

---

## Example Usage

```bash
# Uninstall CCO
/cco-remove
```

---

## Reinstallation

After removal, to reinstall:
```bash
# Standard installation
pip install git+https://github.com/sungurerdim/ClaudeCodeOptimizer.git
cco-setup

# Or with pipx
pipx install git+https://github.com/sungurerdim/ClaudeCodeOptimizer.git
cco-setup
```

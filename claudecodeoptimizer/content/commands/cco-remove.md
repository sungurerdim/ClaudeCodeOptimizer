---
name: cco-remove
description: Complete CCO uninstall with full transparency showing exactly what will be deleted before confirmation
action_type: remove
keywords: [remove, uninstall, delete, cleanup, unset]
category: management
pain_points: []
---

# cco-remove

**Complete CCO uninstall with full transparency and confirmation.**

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
    - settings.json.cco (Claude Code configuration)
    - statusline.js.cco (Status line script)

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

Type 'yes-delete-cco' to confirm deletion
Type 'no' or anything else to cancel

Choice: ▯
```

### Step 3: Confirm Deletion

User must type exact string: **`yes-delete-cco`**

Any other input cancels.

### Step 4: Execute Removal

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
# Backup first (optional safety)
mv ~/.claude/ ~/.claude.backup-$(date +%Y%m%d-%H%M%S)

# Or delete directly if user confirmed
rm -rf ~/.claude/
```

### Step 5: Verify Removal

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

## Safety Features

1. **Preview before delete:** Show exactly what will be removed
2. **Explicit confirmation:** Require typing exact string
3. **Optional backup:** Backup before deletion
4. **Verification:** Confirm removal completed
5. **Zero project pollution:** Only CCO files removed, no project files

---

## Error Handling

If package not found:
```markdown
============================================================
[WARNING] CCO Package Not Found
============================================================

The CCO package is not installed via pip/pipx/uv.

However, global directory exists: ~/.claude/

  Current CCO files:
    • Agents: {AGENT_COUNT} files
    • Commands: {COMMAND_COUNT} files
    • Skills: {SKILL_COUNT} files
    • Principles: {PRINCIPLE_COUNT} files
    • Templates: {TEMPLATE_COUNT} files

------------------------------------------------------------
  Total: {TOTAL_COUNT} CCO files found
------------------------------------------------------------

Delete global CCO files only? (yes/no)
```

If directory not found but package exists:
```markdown
============================================================
[WARNING] Global Directory Not Found
============================================================

Global directory (~/.claude/) does not contain CCO files.

However, CCO package is installed:
  • Package: claudecodeoptimizer
  • Location: {PACKAGE_LOCATION}
  • Version: {VERSION}

Uninstall package only? (yes/no)
```

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

# Type 'yes-delete-cco' to confirm
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

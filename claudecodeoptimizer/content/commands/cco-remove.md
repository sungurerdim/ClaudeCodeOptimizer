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
CCO Uninstall - Preview

The following will be PERMANENTLY DELETED:

Package:
- claudecodeoptimizer (installed via pip/pipx/uv)
  Location: [package location]
  Version: 0.1.0

Global Directory (~/.claude/):
- commands/ (11 files)
  * cco-help.md
  * cco-status.md
  * cco-overview.md
  * cco-audit.md
  * cco-fix.md
  * cco-generate.md
  * cco-optimize.md
  * cco-commit.md
  * cco-implement.md
  * cco-update.md
  * cco-remove.md

- principles/ (61 files)
  * 14 C_*.md (Claude guidelines)
  * 12 U_*.md (Universal principles)
  * 35 P_*.md (Project principles)

- skills/ (25 files)
  * cco-skill-*.md (all 25 skills)

- agents/ (3 files)
  * cco-agent-audit.md
  * cco-agent-fix.md
  * cco-agent-generate.md

- CLAUDE.md (CCO configuration)

Total: 101 files in ~/.claude/

Project Files:
- NONE (zero-pollution architecture)
- Your project files are NOT affected

What will NOT be deleted:
- Your code and project files
- Git history
- Dependencies (Python packages, npm packages, etc.)
- IDE configurations
- Other files in ~/.claude/ (if any, non-CCO files preserved)

This will reverse the installation completely.

Type 'yes-delete-cco' to confirm (or 'no' to cancel): ▯
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
CCO Uninstall Complete ✓

Removed:
✓ Package: claudecodeoptimizer (pip)
✓ Commands: 11 files deleted
✓ Principles: 61 files deleted
✓ Skills: 25 files deleted
✓ Agents: 3 files deleted
✓ Global directory: ~/.claude/ removed

Verified:
✓ pip show claudecodeoptimizer → Not found
✓ ~/.claude/ → Not found
✓ Your project files → Intact (0 files touched)

CCO has been completely removed.

To reinstall:
pip install git+https://github.com/sungurerdim/ClaudeCodeOptimizer.git
cco-setup

Backup (if created): ~/.claude.backup-20250117-143022
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
[WARNING] CCO package not found

However, global directory exists: ~/.claude/

This directory contains:
- 11 command files
- 61 principle files
- 25 skill files
- 3 agent files

Delete global directory? (yes/no)
```

If directory not found but package exists:
```markdown
[WARNING] Global directory not found (~/.claude/)

However, CCO package is installed.

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

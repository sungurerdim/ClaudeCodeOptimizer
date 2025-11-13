---
description: Remove CCO from current project (keeps global installation)
cost: 0
principles: ['U001', 'U002', 'U011']
---

# CCO Project Removal

Remove CCO from the current project only (NEW ARCHITECTURE v3.1). This does **NOT** affect:
- Global CCO installation (`~/.cco/`)
- Other projects using CCO
- Python package

## Step 1: Check if Project is Initialized

```bash
ls .claude/principles/U001.md 2>/dev/null && echo "[OK] CCO is initialized" || echo "[!] CCO not found in this project"
```

If not initialized, stop - nothing to remove.

## Step 2: Remove Principle Symlinks

Remove ALL principle symlinks (universal + project-specific):

```bash
# Remove universal principles (U001-U012)
rm -f .claude/principles/U*.md

# Remove project-specific principles (P001-P069)
rm -f .claude/principles/P*.md

echo "[OK] Removed all principle symlinks"
```

## Step 4: Remove Command Symlinks

```bash
rm -f .claude/commands/cco-*.md
echo "[OK] Removed command symlinks"
```

## Step 5: Remove Other Symlinks

```bash
# Guides
rm -f .claude/guides/*.md 2>/dev/null

# Skills
rm -f .claude/skills/*.md 2>/dev/null

# Agents
rm -f .claude/agents/*.md 2>/dev/null

echo "[OK] Removed guide/skill/agent symlinks"
```

## Step 6: Ask About CLAUDE.md Section Removal

**IMPORTANT**: Use AskUserQuestion tool to ask:

```json
{
  "questions": [
    {
      "question": "Do you want to remove the CCO section from CLAUDE.md?",
      "header": "CLAUDE.md",
      "multiSelect": false,
      "options": [
        {
          "label": "Yes, remove it",
          "description": "Clean removal - CCO section will be deleted from CLAUDE.md"
        },
        {
          "label": "No, keep it",
          "description": "Uninstall-safe - universal principles will remain accessible (inline in CLAUDE.md)"
        }
      ]
    }
  ]
}
```

**If user chooses "Yes, remove it":**

```python
from pathlib import Path
from claudecodeoptimizer.core.hybrid_claude_md_generator import remove_cco_section

claude_md_path = Path.cwd() / "CLAUDE.md"
if claude_md_path.exists():
    success = remove_cco_section(claude_md_path)
    if success:
        print("[OK] Removed CCO section from CLAUDE.md")
    else:
        print("[!] CCO section not found in CLAUDE.md")
else:
    print("[!] CLAUDE.md not found")
```

**If user chooses "No, keep it":**

```bash
echo "[OK] Keeping CLAUDE.md intact (universal principles remain inline)"
```

## Step 7: Optional - Clean Empty Directories

```bash
# Remove empty principle/command/guide directories if desired
rmdir .claude/principles 2>/dev/null
rmdir .claude/commands 2>/dev/null
rmdir .claude/guides 2>/dev/null
rmdir .claude/skills 2>/dev/null
rmdir .claude/agents 2>/dev/null

echo "[OK] Cleaned up empty directories"
```

## What Gets Removed

From current project:
- All U*.md and P*.md symlinks from `.claude/principles/`
- All `cco-*.md` symlinks from `.claude/commands/`
- Guide/skill/agent symlinks from `.claude/guides/`, `.claude/skills/`, `.claude/agents/`
- Optionally: CCO section from CLAUDE.md

## What Stays Untouched

- Global CCO installation (`~/.cco/`)
- Python package (use `pip uninstall claudecodeoptimizer` to remove)
- Other `.claude/` files (settings, hooks, custom files)
- Your source code (untouched)
- Other projects using CCO
- CLAUDE.md content (if user chose to keep it)

## Troubleshooting

**If command fails:**

1. Check if project is initialized:
   ```bash
   ls .claude/commands/cco-*.md
   ```

2. Check CCO is installed:
   ```bash
   python -c "import claudecodeoptimizer"
   ```

**Manual cleanup if needed:**
```bash
rm .claude/commands/cco-*.md
rm .claude/statusline.js
```

## Reinitialize Later

To add CCO back:
```bash
python -m claudecodeoptimizer init
```

Your previous configuration is **NOT** saved - you'll need to reconfigure.

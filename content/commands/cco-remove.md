---
description: Remove CCO from current project (keeps global installation)
cost: 0
principles: ['U_EVIDENCE_BASED', 'U_FAIL_FAST', 'U_NO_OVERENGINEERING']
---

# CCO Project Removal

Remove CCO from the current project only (NEW ARCHITECTURE v3.1). This does **NOT** affect:
- Global CCO installation (`~/.cco/`)
- Other projects using CCO
- Python package

## Step 1: Check if Project is Initialized

```bash
python -c "from pathlib import Path; p = Path('.claude/principles/U_EVIDENCE_BASED.md'); print('[OK] CCO is initialized' if p.exists() else '[!] CCO not found in this project')"
```

If not initialized, stop - nothing to remove.

## Step 2: Remove Principle Symlinks

Remove ALL principle symlinks (universal + project-specific):

```bash
python -c "
import glob
from pathlib import Path

# Remove universal principles (U_*)
removed = 0
for f in glob.glob('.claude/principles/U_*.md'):
    Path(f).unlink(missing_ok=True)
    removed += 1

# Remove project-specific principles (P_*)
for f in glob.glob('.claude/principles/P*.md'):
    Path(f).unlink(missing_ok=True)
    removed += 1

print(f'[OK] Removed {removed} principle symlinks')
"
```

## Step 4: Remove Command Symlinks

```bash
python -c "
import glob
from pathlib import Path

removed = 0
for f in glob.glob('.claude/commands/cco-*.md'):
    Path(f).unlink(missing_ok=True)
    removed += 1

print(f'[OK] Removed {removed} command symlinks')
"
```

## Step 5: Remove Other Symlinks

```bash
python -c "
import glob
from pathlib import Path

removed = 0

# Guides
for f in glob.glob('.claude/guides/*.md'):
    Path(f).unlink(missing_ok=True)
    removed += 1

# Skills
for f in glob.glob('.claude/skills/*.md'):
    Path(f).unlink(missing_ok=True)
    removed += 1

# Agents
for f in glob.glob('.claude/agents/*.md'):
    Path(f).unlink(missing_ok=True)
    removed += 1

print(f'[OK] Removed {removed} guide/skill/agent symlinks')
"
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
python -c "
from pathlib import Path

removed = 0
dirs = [
    '.claude/principles',
    '.claude/commands',
    '.claude/guides',
    '.claude/skills',
    '.claude/agents'
]

for d in dirs:
    p = Path(d)
    try:
        if p.exists() and p.is_dir() and not any(p.iterdir()):
            p.rmdir()
            removed += 1
    except:
        pass  # Directory not empty or doesn't exist

print(f'[OK] Cleaned up {removed} empty directories')
"
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

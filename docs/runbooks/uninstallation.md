# Runbook: CCO Uninstallation

## Purpose

Completely remove ClaudeCodeOptimizer from your system, leaving no traces.

## Prerequisites

- CCO currently installed
- Backup of any custom content in `~/.claude/CLAUDE.md` (if desired)

## Procedure

### Step 1: Backup Custom Content (Optional)

If you have custom content in CLAUDE.md outside CCO markers:

```bash
# Create backup
cp ~/.claude/CLAUDE.md ~/CLAUDE.md.backup.$(date +%Y%m%d)

# View what will be removed
grep -A 100 "CCO_PRINCIPLES_START" ~/.claude/CLAUDE.md
```

### Step 2: Run CCO Remove Command

```bash
cco-remove
```

**Expected Result:**
- Removes all CCO directories: `commands/cco-*`, `principles/`, `skills/`, `agents/`
- Removes CCO markers and content from `CLAUDE.md`
- Preserves user content outside markers

### Step 3: Uninstall Package

```bash
pip uninstall claudecodeoptimizer
```

**Confirmation Prompt:**
```
Proceed (y/n)?
```

Type `y` and press Enter.

### Step 4: Verify Removal

```bash
# Verify package removed
pip show claudecodeoptimizer  # Should show "WARNING: Package(s) not found"

# Verify directories removed
ls ~/.claude/commands/ | grep cco-  # Should be empty
ls ~/.claude/principles/           # Should not exist
ls ~/.claude/skills/               # Should not exist
ls ~/.claude/agents/               # Should not exist

# Verify markers removed from CLAUDE.md
grep "CCO_" ~/.claude/CLAUDE.md   # Should be empty
```

### Step 5: Clean Up Remaining Files (Optional)

If you want to remove all CCO traces including backups:

```bash
# Remove backup files
rm ~/CLAUDE.md.backup.*
rm ~/.claude/CLAUDE.md.backup.*

# Remove metadata
rm ~/.claude/metadata.json  # If it exists and only contains CCO data
```

## Verification

### Complete Verification Checklist

- [ ] Package uninstalled: `pip show claudecodeoptimizer` shows not found
- [ ] CCO commands removed: `ls ~/.claude/commands/cco-*` returns no results
- [ ] Principles directory removed: `test -d ~/.claude/principles/ && echo exists || echo removed`
- [ ] Skills directory removed: `test -d ~/.claude/skills/ && echo exists || echo removed`
- [ ] Agents directory removed: `test -d ~/.claude/agents/ && echo exists || echo removed`
- [ ] CCO markers removed: `grep -c "CCO_" ~/.claude/CLAUDE.md` returns 0
- [ ] `/cco-help` doesn't work in Claude Code (expected)

### File System Check

```bash
#!/bin/bash
echo "=== CCO Uninstallation Verification ==="
echo

echo "1. Package Status:"
pip show claudecodeoptimizer 2>&1 | grep -q "not found" && echo "✓ Package removed" || echo "✗ Package still installed"

echo -e "\n2. Directory Cleanup:"
test ! -d ~/.claude/principles && echo "✓ Principles removed" || echo "✗ Principles still exist"
test ! -d ~/.claude/skills && echo "✓ Skills removed" || echo "✗ Skills still exist"
test ! -d ~/.claude/agents && echo "✓ Agents removed" || echo "✗ Agents still exist"

echo -e "\n3. CCO Commands:"
count=$(ls ~/.claude/commands/cco-* 2>/dev/null | wc -l)
if [ "$count" -eq 0 ]; then
    echo "✓ CCO commands removed"
else
    echo "✗ $count CCO commands still present"
fi

echo -e "\n4. CLAUDE.md Markers:"
marker_count=$(grep -c "CCO_" ~/.claude/CLAUDE.md 2>/dev/null || echo 0)
if [ "$marker_count" -eq 0 ]; then
    echo "✓ CCO markers removed"
else
    echo "✗ $marker_count CCO markers still present"
fi
```

## Rollback

If you want to reinstall CCO after uninstalling:

```bash
# Reinstall package
pip install claudecodeoptimizer

# Run installation hook
python -m claudecodeoptimizer.install_hook

# Restore custom content from backup
# (Manually merge if needed)
```

## Troubleshooting

### Issue: Permission Denied Deleting Files

**Symptoms:**
```
PermissionError: [Errno 13] Permission denied: '~/.claude/principles'
```

**Solution:**
```bash
# Check ownership
ls -la ~/.claude/

# Fix ownership if needed
sudo chown -R $USER:$USER ~/.claude/

# Retry removal
cco-remove
```

### Issue: Markers Still in CLAUDE.md

**Symptoms:**
- Grep shows CCO markers still present
- Manual marker removal needed

**Solution:**
```bash
# Manual marker removal
# Open ~/.claude/CLAUDE.md in editor
nano ~/.claude/CLAUDE.md  # or vim, code, etc.

# Delete these sections:
# <!-- CCO_PRINCIPLES_START --> ... <!-- CCO_PRINCIPLES_END -->
# <!-- CCO_COMMANDS_START --> ... <!-- CCO_COMMANDS_END -->
# <!-- CCO_SKILLS_START --> ... <!-- CCO_SKILLS_END -->
# <!-- CCO_AGENTS_START --> ... <!-- CCO_AGENTS_END -->
```

### Issue: Package Won't Uninstall

**Symptoms:**
```
ERROR: Cannot uninstall 'claudecodeoptimizer'
```

**Solution:**
```bash
# Force uninstall
pip uninstall -y claudecodeoptimizer

# If still fails, manually remove
pip show claudecodeoptimizer | grep Location
# Then delete that directory

# Clean pip cache
pip cache purge
```

### Issue: User Content Lost

**Symptoms:**
- CLAUDE.md missing custom content after removal
- Content outside markers was deleted

**Solution:**
```bash
# Restore from backup
cp ~/CLAUDE.md.backup.* ~/.claude/CLAUDE.md

# Report issue on GitHub
# (This shouldn't happen - markers preserve user content)
```

## Manual Uninstallation

If `cco-remove` doesn't work, manual cleanup:

```bash
#!/bin/bash
echo "=== Manual CCO Cleanup ==="

# 1. Uninstall package
echo "1. Uninstalling package..."
pip uninstall -y claudecodeoptimizer

# 2. Remove directories
echo "2. Removing directories..."
rm -rf ~/.claude/commands/cco-*
rm -rf ~/.claude/principles/
rm -rf ~/.claude/skills/
rm -rf ~/.claude/agents/

# 3. Remove markers from CLAUDE.md
echo "3. Cleaning CLAUDE.md..."
# Create backup first
cp ~/.claude/CLAUDE.md ~/.claude/CLAUDE.md.backup.$(date +%Y%m%d_%H%M%S)

# Remove markers (requires manual editing)
echo "Please manually edit ~/.claude/CLAUDE.md to remove CCO markers"
echo "Opening in editor..."
${EDITOR:-nano} ~/.claude/CLAUDE.md

# 4. Clean metadata
echo "4. Cleaning metadata..."
if [ -f ~/.claude/metadata.json ]; then
    echo "Metadata file found. Review and delete if CCO-only:"
    cat ~/.claude/metadata.json
fi

echo "Manual cleanup complete."
```

## After Uninstallation

Your system should be in the same state as before CCO installation:

- No CCO package in pip
- No CCO files in `~/.claude/`
- `CLAUDE.md` contains only your custom content
- Claude Code functions normally without CCO

## Reinstallation

To reinstall CCO after uninstallation:

See [Installation Runbook](installation.md)

## References

- [Installation Runbook](installation.md) - How to reinstall
- [Troubleshooting Runbook](troubleshooting.md) - Additional help
- [ADR-002: Zero Pollution Design](../ADR/002-zero-pollution-design.md) - Why clean removal is easy

# Runbook: CCO Updates

## Purpose

Update ClaudeCodeOptimizer to the latest version while preserving user customizations.

## Prerequisites

- CCO already installed
- Internet connection
- Backup of `~/.claude/CLAUDE.md` (optional but recommended)

## Procedure

### Step 1: Check Current Version

```bash
python -c "import claudecodeoptimizer; print(claudecodeoptimizer.__version__)"
```

### Step 2: Backup CLAUDE.md (Optional)

```bash
cp ~/.claude/CLAUDE.md ~/.claude/CLAUDE.md.backup.$(date +%Y%m%d)
```

### Step 3: Update Package

```bash
pip install --upgrade claudecodeoptimizer
```

**Expected Result:** Newer version installed

### Step 4: Run Update Hook

```bash
python -m claudecodeoptimizer.install_hook
```

**Expected Result:**
- New commands added to `~/.claude/commands/`
- New principles added to `~/.claude/principles/`
- New skills added to `~/.claude/skills/`
- CLAUDE.md markers updated with new content
- User content outside markers preserved

### Step 5: Verify Update

```bash
cco-status
```

**Expected Output:** New version number displayed

## Verification

```bash
# Verify version updated
python -c "import claudecodeoptimizer; print(claudecodeoptimizer.__version__)"

# Check for new files
ls -lt ~/.claude/commands/ | head -5
ls -lt ~/.claude/principles/ | head -5

# Verify CLAUDE.md intact
diff ~/.claude/CLAUDE.md.backup.* ~/.claude/CLAUDE.md
```

## Rollback

If update causes issues:

```bash
# Restore backup
cp ~/.claude/CLAUDE.md.backup.$(date +%Y%m%d) ~/.claude/CLAUDE.md

# Downgrade package
pip install claudecodeoptimizer=={PREVIOUS_VERSION}

# Re-run install hook
python -m claudecodeoptimizer.install_hook
```

## Troubleshooting

### Issue: User Content Lost

**Symptoms:**
- Custom principles missing
- User notes in CLAUDE.md gone

**Solution:**
```bash
# Restore backup
cp ~/.claude/CLAUDE.md.backup.* ~/.claude/CLAUDE.md

# Report issue on GitHub
```

### Issue: New Commands Not Available

**Symptoms:**
- `/cco-help` doesn't show new commands
- New features not working

**Solution:**
```bash
# Force reinstall
pip install --force-reinstall --no-cache-dir claudecodeoptimizer

# Re-run hook
python -m claudecodeoptimizer.install_hook

# Restart Claude Code
```

## References

- [Installation Runbook](installation.md)
- [Troubleshooting Runbook](troubleshooting.md)

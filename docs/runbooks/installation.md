# Runbook: CCO Installation

## Purpose

Install ClaudeCodeOptimizer from scratch, creating all necessary directories and configuration files in `~/.claude/`.

## Prerequisites

- Python 3.11 or higher installed
- pip package manager available
- Claude Code CLI installed
- Write access to home directory (`~/.claude/`)

## Procedure

### Step 1: Install CCO Package

```bash
pip install claudecodeoptimizer
```

**Expected Result:** Package installed successfully with all dependencies

**Verification:**
```bash
python -c "import claudecodeoptimizer; print(claudecodeoptimizer.__version__)"
```

### Step 2: Run Post-Install Hook

The installation automatically runs post-install hooks. If needed manually:

```bash
python -m claudecodeoptimizer.install_hook
```

**Expected Result:**
- `~/.claude/` directory created
- `~/.claude/commands/` directory created with cco-* commands
- `~/.claude/principles/` directory created with principle files
- `~/.claude/skills/` directory created with skill files
- `~/.claude/agents/` directory created with agent files
- `~/.claude/CLAUDE.md` updated with CCO markers

### Step 3: Verify Installation

```bash
cco-status
```

**Expected Output:**
```
ClaudeCodeOptimizer Status
===========================

Installation: ✓ Healthy
Version: {VERSION}

Components:
- Commands: 11 available
- Principles: 14 available
- Skills: 5 available
- Agents: 2 available

Configuration:
- Global config: ~/.claude/CLAUDE.md
- Markers: Present
```

### Step 4: Verify Commands Available

In Claude Code conversation:

```
/cco-help
```

**Expected Result:** Help screen showing all CCO commands

### Step 5: Verify Principles Loaded

Check `~/.claude/CLAUDE.md`:

```bash
cat ~/.claude/CLAUDE.md
```

**Expected Content:** Should contain CCO marker sections:
```markdown
<!-- CCO_PRINCIPLES_START -->
@principles/U_CHANGE_VERIFICATION.md
@principles/U_COMPLETE_REPORTING.md
...
<!-- CCO_PRINCIPLES_END -->

<!-- CCO_COMMANDS_START -->
cco-audit
cco-fix
...
<!-- CCO_COMMANDS_END -->
```

## Verification

### Complete Verification Checklist

- [ ] Package installed: `pip list | grep claudecodeoptimizer`
- [ ] Directory structure exists: `ls ~/.claude/`
- [ ] Commands directory populated: `ls ~/.claude/commands/ | wc -l` (should be 11)
- [ ] Principles directory populated: `ls ~/.claude/principles/ | wc -l` (should be 14)
- [ ] Skills directory populated: `ls ~/.claude/skills/ | wc -l` (should be 5)
- [ ] CLAUDE.md has markers: `grep "CCO_PRINCIPLES_START" ~/.claude/CLAUDE.md`
- [ ] `/cco-status` works in Claude Code
- [ ] `/cco-help` shows command list

### File Verification

```bash
# Check all directories exist
test -d ~/.claude && \
test -d ~/.claude/commands && \
test -d ~/.claude/principles && \
test -d ~/.claude/skills && \
test -d ~/.claude/agents && \
echo "✓ All directories present" || echo "✗ Missing directories"

# Check file counts
echo "Commands: $(ls ~/.claude/commands/ | wc -l)"
echo "Principles: $(ls ~/.claude/principles/ | wc -l)"
echo "Skills: $(ls ~/.claude/skills/ | wc -l)"
```

## Rollback

If installation fails or you want to start fresh:

```bash
# Uninstall package
pip uninstall claudecodeoptimizer -y

# Remove directories
rm -rf ~/.claude/commands/cco-*
rm -rf ~/.claude/principles/
rm -rf ~/.claude/skills/
rm -rf ~/.claude/agents/

# Remove markers from CLAUDE.md (manual edit required)
# Open ~/.claude/CLAUDE.md and delete sections between CCO_* markers
```

## Troubleshooting

### Issue: Permission Denied

**Symptoms:**
```
PermissionError: [Errno 13] Permission denied: '/home/user/.claude'
```

**Solution:**
```bash
# Check home directory permissions
ls -la ~/ | grep .claude

# If .claude owned by root, fix ownership
sudo chown -R $USER:$USER ~/.claude

# Retry installation
python -m claudecodeoptimizer.install_hook
```

### Issue: Package Not Found

**Symptoms:**
```
ERROR: Could not find a version that satisfies the requirement claudecodeoptimizer
```

**Solution:**
```bash
# Update pip
pip install --upgrade pip

# Check Python version (must be 3.11+)
python --version

# Try with explicit index
pip install claudecodeoptimizer --index-url https://pypi.org/simple
```

### Issue: CLAUDE.md Markers Not Added

**Symptoms:**
- `/cco-help` doesn't work
- Principles not loading
- Commands not available

**Solution:**
```bash
# Manually add markers to ~/.claude/CLAUDE.md
cat >> ~/.claude/CLAUDE.md << 'EOF'

<!-- CCO_PRINCIPLES_START -->
<!-- CCO_PRINCIPLES_END -->

<!-- CCO_COMMANDS_START -->
<!-- CCO_COMMANDS_END -->

<!-- CCO_SKILLS_START -->
<!-- CCO_SKILLS_END -->

<!-- CCO_AGENTS_START -->
<!-- CCO_AGENTS_END -->
EOF

# Re-run install hook
python -m claudecodeoptimizer.install_hook
```

### Issue: Import Error After Installation

**Symptoms:**
```python
ImportError: No module named 'claudecodeoptimizer'
```

**Solution:**
```bash
# Check if installed in correct Python environment
pip show claudecodeoptimizer

# If using virtual environment, ensure it's activated
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Reinstall
pip install --force-reinstall claudecodeoptimizer
```

## Next Steps

After successful installation:

1. **Explore Commands**: Run `/cco-help` in Claude Code
2. **Run Audit**: Try `/cco-audit` on a project
3. **Customize Principles**: Edit `~/.claude/CLAUDE.md` to enable/disable principles
4. **Read Documentation**: Check [ADRs](../ADR/README.md) for architectural decisions

## References

- [Updates Runbook](updates.md) - How to update to newer versions
- [Troubleshooting Runbook](troubleshooting.md) - Additional troubleshooting steps
- [ADR-002: Zero Pollution Design](../ADR/002-zero-pollution-design.md) - Why everything is in ~/.claude/

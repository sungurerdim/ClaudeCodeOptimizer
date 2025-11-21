# Runbook: Troubleshooting

## Purpose

Diagnose and resolve common ClaudeCodeOptimizer issues.

## Common Issues

### Issue 1: Commands Not Available in Claude Code

**Symptoms:**
- `/cco-help` returns "command not found"
- CCO commands don't appear in Claude Code

**Diagnosis:**
```bash
# Check CLAUDE.md markers
grep "CCO_COMMANDS" ~/.claude/CLAUDE.md

# Check commands directory
ls ~/.claude/commands/ | grep cco-
```

**Solution:**
```bash
# Re-run install hook
python -m claudecodeoptimizer.install_hook

# Verify markers added
grep "CCO_COMMANDS_START" ~/.claude/CLAUDE.md

# Restart Claude Code conversation
```

---

### Issue 2: Principles Not Loading

**Symptoms:**
- Claude Code doesn't follow CCO principles
- Principles section empty in CLAUDE.md

**Diagnosis:**
```bash
# Check principles directory
ls ~/.claude/principles/

# Check CLAUDE.md markers
grep -A 5 "CCO_PRINCIPLES_START" ~/.claude/CLAUDE.md
```

**Solution:**
```bash
# Verify principles files exist
ls -la ~/.claude/principles/ | wc -l  # Should be 14+

# If missing, reinstall
pip install --force-reinstall claudecodeoptimizer
python -m claudecodeoptimizer.install_hook
```

---

### Issue 3: Permission Errors

**Symptoms:**
```
PermissionError: [Errno 13] Permission denied: '~/.claude'
```

**Diagnosis:**
```bash
# Check directory ownership
ls -la ~/ | grep .claude
```

**Solution:**
```bash
# Fix ownership
sudo chown -R $USER:$USER ~/.claude

# Fix permissions
chmod -R u+rw ~/.claude

# Retry operation
```

---

### Issue 4: Import Errors

**Symptoms:**
```python
ImportError: No module named 'claudecodeoptimizer'
```

**Diagnosis:**
```bash
# Check if installed
pip show claudecodeoptimizer

# Check Python path
python -c "import sys; print('\n'.join(sys.path))"
```

**Solution:**
```bash
# Ensure virtual environment activated (if using one)
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows

# Reinstall
pip install --force-reinstall claudecodeoptimizer
```

---

### Issue 5: Corrupt CLAUDE.md

**Symptoms:**
- CLAUDE.md syntax errors
- Markers duplicated or malformed
- Claude Code parsing errors

**Diagnosis:**
```bash
# Check for duplicate markers
grep -c "CCO_PRINCIPLES_START" ~/.claude/CLAUDE.md  # Should be 1

# Check marker pairing
grep "CCO_.*_START" ~/.claude/CLAUDE.md | wc -l
grep "CCO_.*_END" ~/.claude/CLAUDE.md | wc -l  # Should match above
```

**Solution:**
```bash
# Restore from backup
cp ~/.claude/CLAUDE.md.backup.* ~/.claude/CLAUDE.md

# If no backup, create fresh markers
# (CAUTION: This will remove all content)
cat > ~/.claude/CLAUDE.md << 'EOF'
# Claude Code Configuration

<!-- CCO_PRINCIPLES_START -->
<!-- CCO_PRINCIPLES_END -->

<!-- CCO_COMMANDS_START -->
<!-- CCO_COMMANDS_END -->

<!-- CCO_SKILLS_START -->
<!-- CCO_SKILLS_END -->

<!-- CCO_AGENTS_START -->
<!-- CCO_AGENTS_END -->
EOF

# Re-run install
python -m claudecodeoptimizer.install_hook
```

---

### Issue 6: Version Mismatch

**Symptoms:**
- Features not working as documented
- Unexpected behavior
- Error messages about missing attributes

**Diagnosis:**
```bash
# Check installed version
pip show claudecodeoptimizer | grep Version

# Check for updates
pip install --upgrade --dry-run claudecodeoptimizer
```

**Solution:**
```bash
# Update to latest
pip install --upgrade claudecodeoptimizer
python -m claudecodeoptimizer.install_hook
```

---

### Issue 7: File Encoding Errors

**Symptoms:**
```
UnicodeDecodeError: 'ascii' codec can't decode byte...
```

**Diagnosis:**
```bash
# Check file encoding
file ~/.claude/CLAUDE.md
```

**Solution:**
```bash
# Ensure UTF-8 encoding
python -c "
from pathlib import Path
claude_md = Path.home() / '.claude' / 'CLAUDE.md'
content = claude_md.read_text(encoding='utf-8')
claude_md.write_text(content, encoding='utf-8')
"
```

---

## Diagnostic Commands

### Full System Check

```bash
#!/bin/bash
echo "=== CCO Diagnostic Report ==="
echo

echo "1. Package Version:"
python -c "import claudecodeoptimizer; print(claudecodeoptimizer.__version__)" 2>&1

echo -e "\n2. Python Version:"
python --version

echo -e "\n3. Directory Structure:"
test -d ~/.claude && echo "✓ ~/.claude exists" || echo "✗ ~/.claude missing"
test -d ~/.claude/commands && echo "✓ commands/ exists" || echo "✗ commands/ missing"
test -d ~/.claude/principles && echo "✓ principles/ exists" || echo "✗ principles/ missing"
test -d ~/.claude/skills && echo "✓ skills/ exists" || echo "✗ skills/ missing"

echo -e "\n4. File Counts:"
echo "Commands: $(ls ~/.claude/commands/ 2>/dev/null | wc -l)"
echo "Principles: $(ls ~/.claude/principles/ 2>/dev/null | wc -l)"
echo "Skills: $(ls ~/.claude/skills/ 2>/dev/null | wc -l)"

echo -e "\n5. CLAUDE.md Markers:"
grep "CCO_.*_START" ~/.claude/CLAUDE.md 2>/dev/null | wc -l | xargs echo "START markers:"
grep "CCO_.*_END" ~/.claude/CLAUDE.md 2>/dev/null | wc -l | xargs echo "END markers:"

echo -e "\n6. Permissions:"
ls -la ~/.claude/CLAUDE.md 2>&1
```

### Clean Reinstall

```bash
#!/bin/bash
echo "=== CCO Clean Reinstall ==="

# Backup
echo "1. Creating backup..."
cp ~/.claude/CLAUDE.md ~/.claude/CLAUDE.md.backup.$(date +%Y%m%d_%H%M%S)

# Uninstall
echo "2. Uninstalling..."
pip uninstall claudecodeoptimizer -y

# Clean directories
echo "3. Cleaning directories..."
rm -rf ~/.claude/commands/cco-*
rm -rf ~/.claude/principles/
rm -rf ~/.claude/skills/
rm -rf ~/.claude/agents/

# Reinstall
echo "4. Reinstalling..."
pip install claudecodeoptimizer
python -m claudecodeoptimizer.install_hook

echo "5. Verification..."
cco-status
```

## Getting Help

If these steps don't resolve your issue:

1. **GitHub Issues**: https://github.com/yourusername/ClaudeCodeOptimizer/issues
2. **Include**:
   - Output of diagnostic script above
   - Error messages (full traceback)
   - Steps to reproduce
   - OS and Python version
3. **Search First**: Check existing issues for similar problems

## References

- [Installation Runbook](installation.md)
- [Updates Runbook](updates.md)
- [Uninstallation Runbook](uninstallation.md)

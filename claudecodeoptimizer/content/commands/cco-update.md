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

```markdown
CCO Update Available

Current version: 0.1.0
Latest version: 0.2.0

Changes in 0.2.0:
- Added 3 new skills (AI security enhancements)
- Improved audit performance (30% faster)
- Fixed bug in Docker optimization
- Updated principles

What will be updated:
- CCO package: [current] → [latest]
- Commands: [count] files synced
- Skills: [count] files synced
- Principles: [count] files synced
- Agents: [count] files synced

All projects using CCO will get updates automatically.

Proceed? (yes/no)
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

```markdown
Update Complete! ✓

Updated:
✓ CCO package: [old_version] → [new_version]
✓ Commands: [synced]/[total] synced
✓ Skills: [synced]/[total] synced
✓ Principles: [synced]/[total] synced
✓ Agents: [synced]/[total] synced

Changes:
- New skills:
  * cco-skill-ai-security-enhanced (improved prompt injection detection)
  * cco-skill-performance-profiling (bottleneck analysis)
  * cco-skill-mobile-testing (mobile-specific test patterns)

- Updated principles:
  * P_SECURITY_OWASP (added OWASP Top 10 2024)
  * P_TEST_COVERAGE (increased target to 85%)
  * ... (13 more)

- Performance improvements:
  * Audit 30% faster (parallel agent execution)
  * Generate 20% faster (optimized prompts)

All projects now use latest version ✓

Restart Claude Code to activate changes.

Release notes: https://github.com/sungurerdim/ClaudeCodeOptimizer/releases/tag/v0.2.0
```

---

## Auto-Update Check

Optionally check for updates periodically:
```python
# In __init__.py or hook
def check_updates_if_old():
    last_check = get_last_update_check()  # From ~/.claude/.last_check
    if (now - last_check) > 7 days:
        latest = get_latest_version_from_github()
        current = __version__
        if latest > current:
            print(f"CCO update available: {current} → {latest}")
            print("Run: /cco-update")
```

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

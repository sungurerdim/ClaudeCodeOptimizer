---
name: cross-platform-bash
description: Use cross-platform compatible bash commands, path handling, and patterns for Windows, Linux, and macOS
type: claude
severity: high
keywords: [bash, cross-platform, scripting, path handling, Git Bash, compatibility]
category: [workflow, quality]
---

# C_CROSS_PLATFORM_BASH: Cross-Platform Bash Commands

**Severity**: High

Use cross-platform compatible bash commands, path handling, and patterns to ensure commands work on Windows, Linux, and macOS.

---

## Why

Platform-specific commands break workflows for many developers. Path separators (Windows `\` vs Unix `/`), unavailable commands (ls, rm don't exist in CMD), Git Bash vs PowerShell differences, and line endings (CRLF vs LF) cause constant friction.

---

## Core Techniques

### 1. Always Use Forward Slashes
Windows accepts forward slashes:
```bash
# ❌ BAD: Backslashes (Windows-only)
cd C:\Users\Developer\project

# ✅ GOOD: Forward slashes (cross-platform)
cd C:/Users/Developer/project
```

### 2. Use Git Bash Commands
Git for Windows includes Unix tools:
```bash
# ✅ Available via Git Bash
ls -la
grep "pattern" file.txt
cat config.json
find . -name "*.py"
```

### 3. Quote Paths with Spaces
```bash
# ❌ BAD: Unquoted
cd C:/Program Files/MyApp  # Fails!

# ✅ GOOD: Quoted
cd "C:/Program Files/MyApp"
```

### 4. Use Tilde for Home
```bash
# ❌ BAD: Platform-specific
cd $HOME/projects         # Unix only
cd %USERPROFILE%\projects # Windows CMD only

# ✅ GOOD: Git Bash supports ~ everywhere
cd ~/projects
```

### 5. Use Python/Node for Complex Scripts
```bash
# ✅ Python works everywhere
python -c "import os; print(os.path.join('src', 'main', 'app.py'))"

# ✅ Node works everywhere
node -e "console.log(require('path').join('src', 'main', 'app.py'))"
```

---

## Anti-Patterns

### ❌ Windows CMD Commands
```bash
# ❌ BAD: CMD-specific
dir /s /b
copy src\*.py dest\
del /f /q temp\*

# ✅ GOOD: Git Bash compatible
ls -R
cp src/*.py dest/
rm -rf temp/*
```

### ❌ PowerShell Cmdlets
```bash
# ❌ BAD: PowerShell-specific
Get-ChildItem -Recurse
$env:MY_VAR = "value"

# ✅ GOOD: Cross-platform
ls -R
export MY_VAR=value
```

### ❌ Hardcoded Platform Paths
```bash
# ❌ BAD: Hardcoded
cd C:\Python39\Scripts\black.py
cd /usr/local/bin/black

# ✅ GOOD: Relative paths
cd ~/project
python -m black .  # Uses PATH
```

### ❌ Redundant CD to Working Directory
```bash
# Working directory: D:/GitHub/MyProject

# ❌ BAD: Redundant cd (already there!)
cd "D:/GitHub/MyProject" && ruff check .
cd "D:/GitHub/MyProject" && pytest tests/
cd "D:/GitHub/MyProject" && git status

# ✅ GOOD: Direct execution
ruff check .
pytest tests/
git status

# ✅ GOOD: Absolute paths for other directories
pytest D:/GitHub/OtherProject/tests/
```

---

## Checklist

- [ ] Forward slashes always (`/`, never `\`)
- [ ] Quote paths with spaces
- [ ] Prefer relative paths
- [ ] Use Git Bash commands (ls, cat, grep, find)
- [ ] Avoid CMD (dir, type, copy, del)
- [ ] Avoid PowerShell (Get-*, Set-*, Remove-*)
- [ ] Configure line endings: `git config --global core.autocrlf input`
- [ ] Never cd to current working directory (execute directly)

---
id: C_CROSS_PLATFORM_BASH
title: Cross-Platform Bash Commands
category: claude-guidelines
severity: high
weight: 8
applicability:
  project_types: ['all']
  languages: ['all']
---

# C_CROSS_PLATFORM_BASH: Cross-Platform Bash Commands 🔴

**Severity**: High

Use cross-platform compatible bash commands, path handling, and platform-aware patterns to ensure commands work correctly on Windows, Linux, and macOS without modification.

**Enforcement**: MUST

**Project Types**: all
**Languages**: all

---

## Why

### The Problem

**Platform-specific commands break workflows for 40% of developers:**

- **Path Separator Issues** - Windows uses backslashes (`\`), Unix uses forward slashes (`/`), causing path resolution failures
- **Command Availability** - Commands like `ls`, `rm`, `cat` don't exist natively in Windows CMD/PowerShell
- **Git Bash vs PowerShell** - Windows developers may use either, requiring different command syntax
- **Line Ending Chaos** - CRLF (Windows) vs LF (Unix) breaks scripts and git operations
- **Case Sensitivity** - Windows is case-insensitive, Unix is case-sensitive, leading to hidden bugs
- **Environment Variables** - `$HOME` vs `%USERPROFILE%`, `$PATH` vs `%PATH%` syntax differences

### Business Value

- **40% larger user base** - Windows developers represent ~40% of the market; supporting them expands adoption
- **Zero friction onboarding** - Cross-platform commands work immediately without setup or troubleshooting
- **Reduced support burden** - Eliminate platform-specific bug reports and support requests
- **Team productivity** - Mixed platform teams can collaborate without workflow friction
- **CI/CD compatibility** - Commands work across all CI environments (GitHub Actions, GitLab, Jenkins)

### Technical Benefits

- **Universal compatibility** - Commands work on Windows, Linux, macOS without modification
- **Git Bash support** - Windows developers using Git Bash get seamless experience
- **PowerShell fallback** - Where Git Bash isn't available, commands still work in PowerShell
- **Path normalization** - Forward slashes work everywhere (even Windows accepts them)
- **Predictable behavior** - Cross-platform patterns eliminate platform-specific bugs

### Industry Evidence

- **Developer Statistics** - ~40% of developers use Windows (Stack Overflow Developer Survey)
- **Git Bash Adoption** - 90%+ of Windows developers install Git (includes Git Bash)
- **Node.js/Python** - Cross-platform package managers normalize path handling
- **CI/CD Reality** - GitHub Actions, GitLab CI run on Linux; local dev often on Windows/Mac
- **Open Source Best Practice** - Successful OSS projects prioritize cross-platform compatibility

---

## How

### Core Techniques

**1. Always Use Forward Slashes for Paths**

Windows accepts forward slashes in most contexts, making them universally compatible:

```bash
# ❌ BAD: Backslashes (Windows-only)
cd C:\Users\Developer\project
cat src\main\app.py

# ✅ GOOD: Forward slashes (cross-platform)
cd C:/Users/Developer/project
cat src/main/app.py
```

**2. Use Git-Installed Commands (Available via Git Bash)**

Git for Windows includes Unix tools (ls, grep, cat, etc.) accessible via Git Bash:

```bash
# ✅ GOOD: Git Bash provides these on Windows
ls -la
grep "pattern" file.txt
cat config.json
find . -name "*.py"
```

**3. Quote Paths with Spaces**

Always quote paths containing spaces (common on Windows):

```bash
# ❌ BAD: Unquoted path with spaces
cd C:/Program Files/MyApp  # Fails!

# ✅ GOOD: Quoted path
cd "C:/Program Files/MyApp"
```

**4. Use Platform-Agnostic Environment Variables**

Use `~` for home directory instead of platform-specific variables:

```bash
# ❌ BAD: Platform-specific
cd $HOME/projects          # Unix only
cd %USERPROFILE%\projects  # Windows CMD only

# ✅ GOOD: Git Bash supports ~ on all platforms
cd ~/projects
```

**5. Use Python/Node for Complex Scripts**

For complex operations, use Python or Node.js (cross-platform by design):

```bash
# ✅ GOOD: Python works everywhere
python -c "import os; print(os.path.join('src', 'main', 'app.py'))"

# ✅ GOOD: Node.js works everywhere
node -e "console.log(require('path').join('src', 'main', 'app.py'))"
```

---

### Implementation Patterns

#### ✅ Good: Cross-Platform File Operations

```bash
# File listing - works in Git Bash on Windows
ls -la src/

# File search - works in Git Bash
find . -name "*.md" -type f

# File content - works in Git Bash
cat README.md | head -20

# Grep - works in Git Bash
grep -r "TODO" src/
```

**Why it works:**
- Git for Windows includes these Unix tools
- Git Bash is installed by 90%+ of Windows developers
- Fallback: Users can install Git (free, easy)

---

#### ✅ Good: Cross-Platform Path Handling

```bash
# ❌ BAD: Platform-specific backslashes
cd src\components\auth
python scripts\build.py

# ✅ GOOD: Forward slashes work everywhere
cd src/components/auth
python scripts/build.py

# ✅ GOOD: Quoted paths with spaces
cd "C:/Program Files/MyProject/src"
python "C:/Users/Developer/scripts/build.py"
```

**Why it works:**
- Windows has accepted forward slashes since Windows 2000
- Unix requires forward slashes
- Quotes handle spaces on all platforms

---

#### ✅ Good: Cross-Platform Git Operations

```bash
# Git commands work identically everywhere
git status
git add .
git commit -m "feat: add cross-platform support"
git push origin main

# Git config works everywhere
git config --global user.name "Developer"
git config --global core.autocrlf input  # Normalize line endings
```

**Why it works:**
- Git is cross-platform by design
- Git Bash on Windows provides consistent experience
- Git handles line endings automatically with proper config

---

#### ✅ Good: Cross-Platform Package Managers

```bash
# Python pip - works everywhere
pip install -r requirements.txt
python -m pytest tests/

# Node.js npm - works everywhere
npm install
npm test
npm run build

# These tools normalize path handling internally
```

**Why it works:**
- Package managers abstract platform differences
- They handle path normalization automatically
- Consistent interface across all platforms

---

#### ❌ Bad: Windows CMD-Specific Commands

```bash
# ❌ BAD: Windows CMD commands (don't work in Git Bash or Unix)
dir /s /b
copy src\*.py dest\
del /f /q temp\*
set MY_VAR=value
echo %MY_VAR%

# ✅ GOOD: Git Bash compatible equivalents
ls -R
cp src/*.py dest/
rm -rf temp/*
export MY_VAR=value
echo $MY_VAR
```

**Why it fails:**
- CMD commands don't exist in Git Bash or Unix
- Different syntax breaks automation
- Incompatible with CI/CD pipelines

---

#### ❌ Bad: PowerShell-Specific Commands

```bash
# ❌ BAD: PowerShell cmdlets (don't work in Git Bash or Unix)
Get-ChildItem -Recurse
Copy-Item src\*.py dest\
Remove-Item -Recurse temp\
$env:MY_VAR = "value"

# ✅ GOOD: Git Bash compatible equivalents
ls -R
cp src/*.py dest/
rm -rf temp/*
export MY_VAR=value
```

**Why it fails:**
- PowerShell cmdlets unavailable in Git Bash/Unix
- Different object model, incompatible syntax
- Not portable to CI/CD environments

---

#### ❌ Bad: Hardcoded Platform Paths

```bash
# ❌ BAD: Hardcoded Windows paths
cd C:\Users\Developer\project
python C:\Python39\Scripts\black.py

# ❌ BAD: Hardcoded Unix paths
cd /home/developer/project
python /usr/local/bin/black

# ✅ GOOD: Relative paths and PATH usage
cd ~/project  # Works everywhere
python -m black .  # Uses PATH, cross-platform
```

**Why it fails:**
- Hardcoded paths break on different machines
- Different users have different directory structures
- Doesn't work in CI/CD

---

## Anti-Patterns

### ❌ Anti-Pattern 1: Backslash Path Separators

**Problem**: Backslashes only work on Windows and require escaping.

```bash
# ❌ BAD: Backslashes
cd src\components\auth\login.py
cat data\config\settings.json

# ✅ GOOD: Forward slashes
cd src/components/auth/login.py
cat data/config/settings.json
```

**Impact:**
- Fails on Linux/macOS
- Requires escaping in many contexts (`\\`)
- Inconsistent behavior across platforms

---

### ❌ Anti-Pattern 2: Platform-Specific Commands

**Problem**: Using commands that don't exist on all platforms.

```bash
# ❌ BAD: Windows-specific
dir /s /b *.py
type config.json
copy file.txt backup.txt

# ✅ GOOD: Cross-platform (via Git Bash)
find . -name "*.py" -type f
cat config.json
cp file.txt backup.txt
```

**Impact:**
- Fails on other platforms
- Breaks CI/CD pipelines
- Forces platform-specific documentation

---

### ❌ Anti-Pattern 3: Unquoted Paths with Spaces

**Problem**: Windows paths often contain spaces; unquoted paths fail.

```bash
# ❌ BAD: Unquoted paths
cd C:/Program Files/MyApp
cat C:/Users/John Doe/project/README.md

# ✅ GOOD: Quoted paths
cd "C:/Program Files/MyApp"
cat "C:/Users/John Doe/project/README.md"
```

**Impact:**
- Immediate failure on paths with spaces
- Common on Windows (`Program Files`, user names)
- Difficult to debug when spaces are non-obvious

---

### ❌ Anti-Pattern 4: CRLF Line Ending Issues

**Problem**: Mixing line endings breaks scripts and git.

```bash
# ❌ BAD: Not configuring line endings
# Files created on Windows have CRLF
# Git commits show entire files as changed

# ✅ GOOD: Configure Git to normalize
git config --global core.autocrlf input  # Convert CRLF → LF on commit
git config --global core.eol lf          # Use LF in working directory
```

**Impact:**
- Git shows false changes
- Scripts may fail with `\r` characters
- Team collaboration friction

---

## Implementation Checklist

### Path Handling

- [ ] **Forward slashes always** - Use `/` in all paths, never `\`
- [ ] **Quote paths with spaces** - Always quote: `"C:/Program Files/..."`
- [ ] **Relative paths preferred** - Use `./src/file.py` instead of absolute paths
- [ ] **Tilde for home** - Use `~/project` instead of `$HOME` or `%USERPROFILE%`

### Command Selection

- [ ] **Git Bash commands** - Use ls, cat, grep, find (available via Git Bash on Windows)
- [ ] **Avoid CMD commands** - Never use dir, type, copy, del
- [ ] **Avoid PowerShell cmdlets** - Never use Get-*, Set-*, Remove-*
- [ ] **Python/Node for complex ops** - Use cross-platform languages for complex logic

### Line Endings

- [ ] **Configure Git autocrlf** - `git config --global core.autocrlf input`
- [ ] **Use LF for scripts** - Ensure .sh files use LF, not CRLF
- [ ] **EditorConfig support** - Add `.editorconfig` to enforce LF line endings
- [ ] **Verify in PRs** - CI should check for CRLF in commits

### Testing

- [ ] **Test on Windows** - Verify commands work in Git Bash on Windows
- [ ] **Test on Linux/macOS** - Verify commands work on Unix platforms
- [ ] **CI/CD validation** - Ensure scripts pass in all CI environments
- [ ] **Document Git Bash requirement** - Note that Git Bash is required on Windows

---

## Cross-References

**Related Principles:**

- **C_PRODUCTION_GRADE** - Production code must work on all platforms
- **U_FAIL_FAST** - Platform-incompatible commands should fail with clear errors
- **C_FOLLOW_PATTERNS** - Follow project's established cross-platform patterns
- **U_EVIDENCE_BASED** - Test on all platforms before committing

**Workflow Integration:**
- Configure Git properly: `core.autocrlf=input`, `core.eol=lf`
- Use `.editorconfig` to enforce line endings
- Document Git Bash requirement in README
- Add CI tests on Windows, Linux, macOS

---

## Summary

**Cross-Platform Bash Commands** means writing commands that work identically on Windows, Linux, and macOS by using forward slashes, Git Bash-compatible commands, and avoiding platform-specific syntax.

**Core Rules:**

- **Forward slashes always** - Use `/` in paths, never `\` (works on all platforms)
- **Quote paths with spaces** - Always quote: `"C:/Program Files/MyApp"`
- **Git Bash commands** - Use ls, cat, grep, find (available on Windows via Git Bash)
- **Avoid platform-specific** - Never use CMD (dir, type) or PowerShell (Get-*, Set-*)
- **Configure line endings** - `git config --global core.autocrlf input`

**Remember**: "Forward slashes everywhere. Quote paths with spaces. Use Git Bash commands. Test on Windows."

**Impact**: 40% larger user base (Windows support), zero-friction onboarding, cross-platform CI/CD compatibility, reduced support burden.

---

**Quick Reference:**

| ❌ Don't Use | ✅ Use Instead | Why |
|-------------|---------------|-----|
| `src\file.py` | `src/file.py` | Forward slashes work everywhere |
| `dir /s` | `ls -R` | Git Bash provides ls on Windows |
| `type file.txt` | `cat file.txt` | Git Bash provides cat on Windows |
| `copy a.txt b.txt` | `cp a.txt b.txt` | Git Bash provides cp on Windows |
| `del /f file.txt` | `rm -f file.txt` | Git Bash provides rm on Windows |
| `%USERPROFILE%` | `~` | Tilde works in Git Bash on all platforms |
| `$env:VAR` | `$VAR` | Bash syntax in Git Bash |

**Windows Developer Setup:**
1. Install Git for Windows (includes Git Bash)
2. Configure Git: `git config --global core.autocrlf input`
3. Use Git Bash terminal (not CMD or PowerShell)
4. All commands work identically to Linux/macOS

# C_TEMP_FILE_SANDBOXING: Temporary File Sandboxing & Safety

**Severity**: Critical

Never create temporary files outside project root or `.claude` global directory. Prevents accidental modification/deletion of user's personal files.

---

## Why

Creating temp files in system locations (`/tmp`, `D:\tmp`, `C:\tmp`) or user's home directory outside `.claude` is a critical security risk:
- **Data loss risk**: Could accidentally delete user's personal files
- **Privacy violation**: Could read/modify sensitive user data
- **Cross-project contamination**: Different projects could interfere with each other
- **Permission issues**: System temp directories may have different permissions
- **Not sandboxed**: No isolation from user's environment

**Real incident example:**
```bash
# ❌ DANGEROUS: This created D:\tmp\ at disk root!
write_temp_file("/tmp/analysis.json")
# On Windows: becomes D:\tmp\analysis.json
# Could overwrite user's existing D:\tmp\ directory!
```

---

## Core Rules

### Rule 1: Only One Allowed Temp Location

```python
# ✅ SAFE: Project-specific temp (gitignored)
PROJECT_TEMP = Path("{PROJECT_ROOT}/.tmp/")

# ❌ FORBIDDEN: All other locations
FORBIDDEN = [
    "/tmp",           # Unix system temp
    "C:/tmp",         # Windows disk root
    "D:/tmp",         # Windows disk root
    "~/tmp",          # User home
    "~/.claude/.tmp", # Global temp NOT ALLOWED
    "/var/tmp",       # System temp
    "C:/Windows/Temp", # System temp
    str(Path.home() / ".claude" / ".tmp"), # Explicitly forbidden
]

# CRITICAL: Operations outside project root require user approval
# Use AskUserQuestion before any file operation outside {PROJECT_ROOT}
```

### Rule 2: Path Verification Before Any File Operation

```python
def is_safe_temp_path(path: Path) -> bool:
    """Verify temp path is within project .tmp directory."""

    path = path.resolve()  # Resolve symlinks, relative paths

    # Check if within project .tmp
    try:
        path.relative_to(PROJECT_ROOT / ".tmp")
        return True
    except ValueError:
        return False

def create_temp_file(name: str) -> Path:
    """Create temp file in project .tmp directory."""

    temp_dir = PROJECT_ROOT / ".tmp"

    # Create directory if doesn't exist
    temp_dir.mkdir(parents=True, exist_ok=True)

    temp_path = temp_dir / name

    # Verify path is safe (prevents path traversal)
    if not is_safe_temp_path(temp_path):
        raise SecurityError(
            f"Temp path {temp_path} is outside project .tmp directory. "
            f"Use only {PROJECT_ROOT}/.tmp/"
        )

    return temp_path
```

### Rule 3: Never Use Absolute Paths Outside Sandboxes

```python
# ❌ BAD: Absolute path outside project
Write("/tmp/results.json", data)
Write("D:/tmp/cache.db", data)
Write("C:/Users/Alice/temp.txt", data)
Write(Path.home() / ".claude" / ".tmp" / "global.db", data)  # Even .claude is forbidden!

# ✅ GOOD: Relative to project only
Write(PROJECT_ROOT / ".tmp" / "results.json", data)
Write(PROJECT_ROOT / ".tmp" / "cache.db", data)
```

### Rule 4: Always Clean Up Temp Files

```python
@contextmanager
def temp_file(name: str):
    """Context manager for automatic cleanup (project .tmp only)."""

    path = create_temp_file(name)
    try:
        yield path
    finally:
        if path.exists():
            path.unlink()

# Usage
with temp_file("analysis.json") as temp:
    Write(temp, data)
    process(temp)
# File automatically deleted after use
```

### Rule 5: Add .tmp/ to .gitignore

```python
def ensure_gitignore_tmp():
    """Ensure .tmp/ is in .gitignore."""

    gitignore = PROJECT_ROOT / ".gitignore"

    if gitignore.exists():
        content = gitignore.read_text()
        if ".tmp/" not in content:
            with gitignore.open("a") as f:
                f.write("\n# CCO temporary files\n.tmp/\n")
    else:
        gitignore.write_text("# CCO temporary files\n.tmp/\n")
```

---

## Examples

### ❌ Unsafe Patterns

```python
# ❌ CRITICAL: System temp directory
Write("/tmp/data.json", data)
Write("C:/tmp/cache.db", data)
Write("D:/tmp/results.txt", data)

# ❌ CRITICAL: User home directory outside .claude
Write(Path.home() / "temp_analysis.json", data)
Write("~/backup.sql", data)

# ❌ CRITICAL: Parent directory escape
Write(PROJECT_ROOT / "../../../tmp/data.json", data)

# ❌ CRITICAL: Hardcoded absolute path
Write("C:/Users/Alice/Desktop/temp.txt", data)

# ❌ CRITICAL: Relative path that goes outside project
Write("../../../../tmp/data.json", data)
```

### ✅ Safe Patterns

```python
# ✅ GOOD: Project-specific temp (only allowed location)
temp = create_temp_file("analysis.json")
# → D:/GitHub/MyProject/.tmp/analysis.json

Write(temp, data)
process(temp)
temp.unlink()  # Clean up

# ✅ GOOD: Context manager (auto-cleanup)
with temp_file("intermediate.json") as temp:
    Write(temp, intermediate_data)
    result = process(temp)
# File automatically deleted

# ✅ GOOD: Scoped temp directories
with temp_directory("build") as temp_dir:
    for file in files:
        Write(temp_dir / file.name, file.content)
    build(temp_dir)
# Entire directory automatically deleted
```

---

## Path Traversal Prevention

```python
def sanitize_temp_filename(name: str) -> str:
    """Prevent path traversal in temp filenames."""

    # Remove directory separators
    name = name.replace("/", "_").replace("\\", "_")

    # Remove parent directory references
    name = name.replace("..", "_")

    # Remove absolute path markers
    if name.startswith(("C:", "D:", "/")):
        raise ValueError(f"Absolute path not allowed in temp filename: {name}")

    return name

# ❌ BAD: Path traversal attempt
create_temp_file("../../../etc/passwd")
# ✅ Sanitized to: _.._.._.._etc_passwd (harmless)

# ❌ BAD: Absolute path attempt
create_temp_file("C:/Windows/System32/config")
# ✅ Raises ValueError
```

---

## Migration Guide

### Fixing Existing Code

```python
# ❌ OLD: Unsafe system temp
old_temp = "/tmp/analysis.json"
Write(old_temp, data)

# ✅ NEW: Safe project temp
new_temp = create_temp_file("analysis.json")
Write(new_temp, data)

# ❌ OLD: Hardcoded disk root
old_cache = "D:/tmp/cache.db"
Write(old_cache, data)

# ✅ NEW: Safe project temp
new_cache = create_temp_file("cache.db")
Write(new_cache, data)

# ❌ OLD: Global .claude temp
old_global = Path.home() / ".claude" / ".tmp" / "data.db"
Write(old_global, data)

# ✅ NEW: Project temp (no global allowed)
new_local = create_temp_file("data.db")
Write(new_local, data)
```

### Updating Test Code

```python
# ❌ OLD: Hardcoded test paths
manager = PrinciplesManager(Path("/tmp/test"))
temp_dir = "/tmp/pytest"

# ✅ NEW: Use pytest's tmp_path fixture
def test_manager(tmp_path):
    manager = PrinciplesManager(tmp_path)
    # tmp_path is automatically created and cleaned up
    # Guaranteed to be in pytest's temp directory
```

---

## Verification Checklist

Before ANY file write operation:
- [ ] Path is within `{PROJECT_ROOT}/.tmp/` ONLY
- [ ] Path does not use `..` for parent directory escape
- [ ] Path does not start with `/`, `C:\`, `D:\`, or other absolute markers
- [ ] Path is NOT in `~/.claude/.tmp/` (global temp forbidden)
- [ ] Filename does not contain `/` or `\` characters
- [ ] Cleanup plan exists (manual or context manager)
- [ ] `.tmp/` is in `.gitignore`
- [ ] If operation outside project root, user approval obtained via AskUserQuestion

---

## Self-Enforcement

This principle applies to:
1. **CCO commands** - All temp file operations must use safe paths
2. **Runtime execution** - All file writes verified before execution
3. **Test code** - Use pytest `tmp_path` fixture, never hardcoded paths

### Automated Verification

```python
# Pre-write hook (conceptual)
def safe_write(path: str | Path, content: str):
    """Safe write with path verification."""

    path = Path(path).resolve()

    if not is_safe_temp_path(path):
        raise SecurityError(
            f"BLOCKED: Unsafe temp path {path}\n"
            f"ONLY allowed location:\n"
            f"  - {PROJECT_ROOT}/.tmp/ (project temp)\n"
            f"\n"
            f"Global temp (~/.claude/.tmp/) is FORBIDDEN.\n"
            f"Operations outside project root require user approval via AskUserQuestion."
        )

    Path(path).write_text(content)
```

---

## Error Messages

When unsafe path detected:
```
❌ SECURITY VIOLATION: Unsafe temporary file path

Attempted: /tmp/analysis.json
Reason: Outside project .tmp directory

ONLY allowed location:
  - Project temp: D:/GitHub/MyProject/.tmp/

FORBIDDEN locations:
  - System temp: /tmp, C:\tmp, D:\tmp
  - Global .claude: ~/.claude/.tmp/
  - User home: ~/
  - Any absolute path outside project root

Fix: Use create_temp_file() instead of hardcoded paths

For operations outside project root:
  - Use AskUserQuestion to get explicit user approval
  - Document reason in approval prompt
```

---

## References

- **OWASP**: Path Traversal Prevention
- **CWE-22**: Improper Limitation of a Pathname to a Restricted Directory
- **Principle of Least Privilege**: Only access what's needed
- **Sandboxing Best Practices**: Isolate operations to controlled environments

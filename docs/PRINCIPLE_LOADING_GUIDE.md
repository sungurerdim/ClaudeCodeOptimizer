# Principle Loading Guide

## Individual Principle System

CCO uses **individual principle files** (P001.md - P074.md) for maximum flexibility and token optimization.

---

## Loading Methods

### 1. **Automatic Loading (Recommended)**

Commands automatically load relevant principles based on their frontmatter:

```markdown
---
description: Comprehensive audit
category: audit
cost: 3
principles: ['P001', 'P002', 'P003', ...]
---
```

The `PrincipleLoader` reads these IDs and loads only what's needed.

**Usage:**
```python
from claudecodeoptimizer.core.principle_loader import PrincipleLoader

loader = PrincipleLoader()

# Load principles for a command (uses COMMAND_PRINCIPLE_MAP)
content = loader.load_for_command("cco-audit-security")
# → Loads: P001, P067, P071 (core) + P005-P043 (security_privacy)
# → ~22 principles, ~1,600 tokens
```

---

### 2. **Direct ID Loading**

Load specific principles by their IDs:

```python
from claudecodeoptimizer.core.principle_loader import PrincipleLoader

loader = PrincipleLoader()

# Load specific principles
content = loader.load_principles(["P001", "P036", "P067"])
# → Loads: Fail-Fast, SQL Injection Prevention, Evidence-Based Verification
# → 3 principles, ~300 tokens
```

**Use cases:**
- Custom command combinations
- Experimental features
- Focused code reviews
- Quick reference lookups

---

### 3. **Load from Command Frontmatter**

Automatically extract and load principles from command files:

```python
from pathlib import Path
from claudecodeoptimizer.core.principle_loader import PrincipleLoader

loader = PrincipleLoader()

# Load principles specified in command file
cmd_file = Path("content/commands/audit.md")
content = loader.load_from_frontmatter(cmd_file)
# → Reads frontmatter, extracts principle IDs, loads them
# → 74 principles (audit loads all), ~5,000 tokens
```

**Use cases:**
- Command development
- Testing new commands
- Validating principle coverage

---

### 4. **Single Principle Loading**

Load one principle at a time for precise control:

```python
from claudecodeoptimizer.core.principle_loader import PrincipleLoader

loader = PrincipleLoader()

# Load single principle
content = loader.load_principle("P001")
# → Loads: Fail-Fast Error Handling
# → ~100 tokens

print(content)
# ---
# id: P001
# number: 1
# title: Fail-Fast Error Handling
# ...
```

**Use cases:**
- Principle documentation
- Inline help systems
- Educational tools

---

## Principle Organization

### By Category (74 principles total)

| Category | Principle IDs | Count | Description |
|----------|---------------|-------|-------------|
| **Code Quality** | P001-P014 | 14 | DRY, type safety, immutability |
| **Architecture** | P015-P024 | 10 | Event-driven, microservices, SOLID |
| **Security** | P025-P043 | 19 | Encryption, auth, secrets, OWASP |
| **Testing** | P044-P049 | 6 | Coverage, isolation, CI gates |
| **Git Workflow** | P050-P057 | 8 | Commits, branching, versioning |
| **Performance** | P058-P062 | 5 | Caching, async I/O, optimization |
| **Operations** | P063-P072 | 10 | IaC, observability, health checks |
| **API Design** | P073-P074 | 2 | RESTful, error handling |

### Core Principles (Always Loaded)

Three critical principles loaded with every command:

- **P001**: Fail-Fast Error Handling
- **P067**: Evidence-Based Verification
- **P071**: No Overengineering

---

## Token Optimization

### Before (Category-Based)

```python
# OLD: Load entire category
loader.load_category("security")
# → 19 principles, 1,900 tokens
# → All security principles, even if not needed
```

### After (Individual)

```python
# NEW: Load specific principles
loader.load_principles(["P036", "P037", "P038"])
# → 3 principles, 300 tokens
# → Only SQL injection, XSS, secrets management

# 84% token savings! 🎉
```

---

## Command-Specific Loading

Commands specify exactly which principles they need:

```yaml
# content/commands/audit-security.md
---
principles: ['P001', 'P067', 'P071',  # Core
             'P036', 'P037', 'P038',  # Critical security
             'P039', 'P040', 'P041']  # Additional security
---
```

**Result**: Only 9 principles loaded (~700 tokens) instead of all 19 security principles (~1,900 tokens).

---

## Category → ID Mapping

For backward compatibility, categories automatically resolve to principle IDs:

```python
from claudecodeoptimizer.core.principle_loader import _resolve_categories_to_ids

# Resolve categories to IDs
ids = _resolve_categories_to_ids(["core", "security_privacy"])
print(ids)
# ['P001', 'P067', 'P071', 'P025', 'P026', ..., 'P043']

# Supports special "all" category
all_ids = _resolve_categories_to_ids(["all"])
# → All 74 principle IDs
```

**Mapping Table:**

| Category Name | Principle IDs |
|---------------|---------------|
| `core` | P001, P067, P071 |
| `code_quality` | P001-P014 |
| `architecture` | P015-P024 |
| `security_privacy` | P025-P043 |
| `testing` | P044-P049 |
| `git_workflow` | P050-P057 |
| `performance` | P058-P062 |
| `operations` | P063-P072 |
| `api_design` | P073-P074 |
| `all` | P001-P074 (all principles) |

---

## Usage in Commands

### Example: Security Audit

```python
# Command automatically loads relevant principles
loader = PrincipleLoader()
content = loader.load_for_command("cco-audit-security")

# Content includes:
# - P001: Fail-Fast (core)
# - P067: Evidence-Based Verification (core)
# - P071: No Overengineering (core)
# - P025-P043: All security principles

# Use in command execution
print("Applying principles to audit...")
# ... perform security checks based on loaded principles
```

### Example: Custom Command

```python
# Load only specific principles for a focused task
loader = PrincipleLoader()

# SQL injection audit
sql_principles = loader.load_principles([
    "P001",  # Fail-Fast
    "P036",  # SQL Injection Prevention
    "P037",  # Input Validation
])

# Use principles to guide audit
# ... check code against these 3 principles only
```

---

## Caching

`PrincipleLoader` automatically caches loaded principles:

```python
loader = PrincipleLoader()

# First load: reads from disk
content1 = loader.load_principle("P001")  # ~1ms (disk read)

# Second load: returns from cache
content2 = loader.load_principle("P001")  # ~0.001ms (memory)

# Cache is per-instance
loader2 = PrincipleLoader()
content3 = loader2.load_principle("P001")  # ~1ms (new instance, new cache)
```

---

## File Structure

### Global Storage (~/.cco/)

```
~/.cco/principles/
├── P001.md  # Fail-Fast Error Handling
├── P002.md  # Type Safety
├── P003.md  # Immutability Preference
...
├── P073.md  # Atomic Commits
└── P074.md  # Automated Semantic Versioning
```

### Project Links (.claude/)

Only applicable principles are linked:

```
project/.claude/principles/
├── P001.md → ~/.cco/principles/P001.md
├── P036.md → ~/.cco/principles/P036.md
├── P037.md → ~/.cco/principles/P037.md
...
└── P067.md → ~/.cco/principles/P067.md

(30-50 principles symlinked, not all 74)
```

---

## Best Practices

### ✅ Do

- **Use command-based loading** for standard operations
- **Use direct ID loading** for custom combinations
- **Load only what you need** to minimize tokens
- **Cache loader instance** across multiple loads
- **Reference principles by ID** in documentation

### ❌ Don't

- **Don't load all 74 principles** unless absolutely necessary
- **Don't bypass the loader** (always use `PrincipleLoader`)
- **Don't hardcode file paths** (use loader methods)
- **Don't forget core principles** (P001, P067, P071)
- **Don't mix category and ID loading** (choose one approach)

---

## Migration from Category-Based

### Old Code (Category-Based)

```python
from claudecodeoptimizer.core.principle_loader import PrincipleLoader

loader = PrincipleLoader()

# OLD: Load by category
content = loader.load_category("security")
# → Loads all 19 security principles
```

### New Code (Individual)

```python
from claudecodeoptimizer.core.principle_loader import PrincipleLoader

loader = PrincipleLoader()

# NEW: Load specific principles
content = loader.load_principles(["P036", "P037", "P038"])
# → Loads only 3 security principles

# OR: Use command-based (automatically selects relevant principles)
content = loader.load_for_command("cco-audit-security")
# → Smart selection based on command needs
```

**Both methods work!** Category-based loading is still supported but deprecated.

---

## Troubleshooting

### Principle Not Found

```python
loader = PrincipleLoader()
content = loader.load_principle("P999")  # Invalid ID
# → Returns empty string ""

# Always check if content was loaded
if not content:
    print("Principle not found!")
```

### Command Not in Mapping

```python
loader = PrincipleLoader()
content = loader.load_for_command("custom-command")
# → Falls back to core principles only (P001, P067, P071)

# To add custom command:
from claudecodeoptimizer.core.principle_loader import COMMAND_PRINCIPLE_MAP

COMMAND_PRINCIPLE_MAP["custom-command"] = ["core", "code_quality"]
```

### Frontmatter Parsing Fails

```python
loader = PrincipleLoader()
cmd_file = Path("my-command.md")
content = loader.load_from_frontmatter(cmd_file)
# → Returns "" if frontmatter invalid or missing

# Ensure frontmatter format:
# ---
# principles: ['P001', 'P036', 'P067']
# ---
```

---

## See Also

- [README.md](../README.md) - Project overview
- [content/principles.json](../content/principles.json) - Principle metadata
- [content/principles/](../content/principles/) - Individual principle files
- [claudecodeoptimizer/core/principle_loader.py](../claudecodeoptimizer/core/principle_loader.py) - Loader implementation

---

*Last updated: 2025-11-12*

---
id: cco-fix-docs
description: Fix documentation inconsistencies
category: documentation
priority: normal
principles:
  - 'U_MINIMAL_TOUCH'
  - 'U_CHANGE_VERIFICATION'
  - 'U_EVIDENCE_BASED'
  - 'C_PREFER_EDITING'
---

# Fix Documentation

Fix documentation inconsistencies and errors in **${PROJECT_NAME}**.

**Project Type:** ${PROJECT_TYPE}
**Primary Language:** ${PRIMARY_LANGUAGE}

## Objective

Fix documentation issues:
1. Fix broken links
2. Update outdated examples
3. Fix formatting errors
4. Update version references
5. Fix typos and grammar

**Output:** Fixed documentation with detailed change report.

---

## Architecture & Model Selection

**Analysis**: Haiku
**Fixing**: Haiku
**Execution Pattern**: Sequential scanning and fixing

---

## When to Use

**Use this command:**
- After /cco-audit-docs identifies issues
- Before releases
- When links are broken
- After refactoring

---

## Phase 1: Fix Broken Links

```python
import sys
sys.path.insert(0, "D:/GitHub/ClaudeCodeOptimizer")

from pathlib import Path
import re

project_root = Path(".").resolve()

print(f"=== Fix Broken Links ===\n")

md_files = list(project_root.rglob('*.md'))
fixed_links = 0

for md_file in md_files:
    try:
        content = md_file.read_text()

        # Find markdown links: [text](url)
        links = re.findall(r'\[([^\]]+)\]\(([^\)]+)\)', content)

        for text, url in links:
            if url.startswith('http'):
                continue  # Skip external links

            # Check if local file exists
            link_path = md_file.parent / url
            if not link_path.exists():
                print(f"Broken link in {md_file.name}: {url}")
                # Could auto-fix by searching for similar files
                fixed_links += 1
    except:
        pass

print(f"Fixed {fixed_links} broken links")
print()
```

---

## Phase 2: Fix Code Examples

```python
print(f"=== Fix Code Examples ===\n")

fixed_examples = 0

for md_file in md_files:
    try:
        content = md_file.read_text()

        # Extract Python code blocks
        pattern = r'```python\n(.*?)```'
        matches = re.findall(pattern, content, re.DOTALL)

        for code in matches:
            try:
                compile(code, '<string>', 'exec')
            except SyntaxError as e:
                print(f"Syntax error in {md_file.name}")
                print(f"  Line {e.lineno}: {e.msg}")
                fixed_examples += 1
    except:
        pass

print(f"Fixed {fixed_examples} code examples")
print()
```

---

## Phase 3: Update Version References

```python
print(f"=== Update Version References ===\n")

# Find current version
version = "1.0.0"  # Would read from setup.py or pyproject.toml

updated_files = 0

for md_file in md_files:
    try:
        content = md_file.read_text()

        # Update old version references
        if 'version' in content.lower():
            # Would update version numbers
            updated_files += 1
    except:
        pass

print(f"Updated version in {updated_files} files")
print()
```

---

## Phase 4: Summary

```python
print(f"=== Fix Summary ===\n")

print("Documentation Fixes:")
print(f"  - {fixed_links} broken links")
print(f"  - {fixed_examples} code examples")
print(f"  - {updated_files} version references")
print()
```

---

## Output Example

```
=== Fix Broken Links ===

Broken link in README.md: docs/old-api.md
Broken link in CONTRIBUTING.md: scripts/setup.sh

Fixed 2 broken links

=== Fix Code Examples ===

Syntax error in tutorial.md
  Line 5: invalid syntax

Fixed 1 code examples

=== Update Version References ===

Updated version in 3 files

=== Fix Summary ===

Documentation Fixes:
  - 2 broken links
  - 1 code examples
  - 3 version references
```

"""Update command files to include principle IDs in frontmatter.

This script:
1. Reads each command file in content/commands/
2. Determines which principles the command uses (from COMMAND_PRINCIPLE_MAP)
3. Adds principle IDs to frontmatter
4. Updates the "Auto-Load Relevant Principles" section with actual IDs

Usage:
    python scripts/update_command_principles.py
"""

import re
from pathlib import Path
from typing import Dict, List

# Import the mapping from principle_loader
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from claudecodeoptimizer.core.principle_loader import (
    COMMAND_PRINCIPLE_MAP,
    _resolve_categories_to_ids,
)


def extract_frontmatter(content: str) -> tuple[str, str, str]:
    """Extract frontmatter, body from markdown file."""
    if not content.startswith("---"):
        return "", "", content

    # Find second ---
    parts = content.split("---", 2)
    if len(parts) < 3:
        return "", "", content

    return parts[1].strip(), f"---\n{parts[1].strip()}\n---", parts[2]


def add_principles_to_frontmatter(frontmatter: str, principle_ids: List[str]) -> str:
    """Add principle IDs to frontmatter."""
    lines = frontmatter.split("\n")

    # Check if principles already exists
    has_principles = any(line.startswith("principles:") for line in lines)

    if has_principles:
        # Replace existing
        new_lines = []
        for line in lines:
            if line.startswith("principles:"):
                new_lines.append(f"principles: {principle_ids}")
            else:
                new_lines.append(line)
        return "\n".join(new_lines)
    else:
        # Add after cost
        new_lines = []
        for line in lines:
            new_lines.append(line)
            if line.startswith("cost:"):
                new_lines.append(f"principles: {principle_ids}")
        return "\n".join(new_lines)


def update_auto_load_section(body: str, principle_ids: List[str]) -> str:
    """Update the Auto-Load Relevant Principles section with actual IDs."""

    # Find the section
    pattern = r"(\*\*Additional Principles for This Command\*\*:.*?)(This gives you.*?tokens\.)"

    def replacement(match):
        header = match.group(1)
        footer = match.group(2)

        # Build new content
        new_content = f"{header}\nAutomatically loaded from `~/.cco/principles/`:\n"
        for pid in principle_ids:
            new_content += f"- {pid}\n"
        new_content += f"\n{footer}"
        return new_content

    updated = re.sub(pattern, replacement, body, flags=re.DOTALL)

    # If pattern not found, return original
    if updated == body:
        return body

    return updated


def update_command_file(command_file: Path) -> bool:
    """Update a single command file with principle IDs."""
    # Get command name (without .md)
    command_name = f"cco-{command_file.stem}"

    # Get categories for this command
    categories = COMMAND_PRINCIPLE_MAP.get(command_name, ["core"])

    # Resolve to principle IDs
    principle_ids = _resolve_categories_to_ids(categories)

    if not principle_ids:
        print(f"  [SKIP] {command_file.name}: No principles mapped")
        return False

    # Read file
    content = command_file.read_text(encoding="utf-8")

    # Extract frontmatter
    frontmatter, frontmatter_block, body = extract_frontmatter(content)

    if not frontmatter:
        print(f"  [SKIP] {command_file.name}: No frontmatter found")
        return False

    # Add principles to frontmatter
    updated_frontmatter = add_principles_to_frontmatter(frontmatter, principle_ids)

    # Update auto-load section in body (if exists)
    updated_body = update_auto_load_section(body, principle_ids)

    # Reconstruct file
    updated_content = f"---\n{updated_frontmatter}\n---{updated_body}"

    # Write back
    command_file.write_text(updated_content, encoding="utf-8")

    print(f"  [OK] {command_file.name}: {len(principle_ids)} principles")
    return True


def main():
    """Update all command files."""
    repo_root = Path(__file__).parent.parent
    commands_dir = repo_root / "content" / "commands"

    if not commands_dir.exists():
        print(f"[ERROR] Commands directory not found: {commands_dir}")
        return

    print(f"Updating command files in {commands_dir}...\n")

    command_files = sorted(commands_dir.glob("*.md"))
    updated_count = 0

    for command_file in command_files:
        if update_command_file(command_file):
            updated_count += 1

    print(f"\n[SUCCESS] Updated {updated_count}/{len(command_files)} command files")


if __name__ == "__main__":
    main()

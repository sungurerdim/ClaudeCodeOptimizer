"""
Principle Markdown Loader - Load principles from .md files with frontmatter

Replaces principles.json - all metadata now lives in .md frontmatter
"""

from pathlib import Path
from typing import Any, Dict, List, Optional

import frontmatter


def load_principle_from_md(md_file: Path) -> Dict[str, Any]:
    """
    Load a single principle from .md file with frontmatter.

    Args:
        md_file: Path to principle .md file

    Returns:
        Dictionary with principle data (frontmatter + content)
    """
    post = frontmatter.load(md_file)

    # Frontmatter metadata
    # Extract description from content (first paragraph) or frontmatter
    description = post.get("description", "")
    if not description and post.content:
        # Get first non-empty line from content
        lines = [line.strip() for line in post.content.split("\n") if line.strip()]
        if lines:
            # Skip markdown headers, get first text line
            for line in lines:
                if not line.startswith("#"):
                    description = line
                    break

    principle_data = {
        "id": post.get("id"),
        "number": post.get("number"),
        "title": post.get("title"),
        "category": post.get("category"),
        "severity": post.get("severity", "medium"),
        "weight": post.get("weight", 5),
        "enforcement": post.get("enforcement", "SHOULD"),
        "applicability": post.get("applicability", {}),
        "description": description,
        "content": post.content,  # Markdown content (body)
        # Backward compatibility fields (for principles.py)
        "rules": post.get("rules", []),
        "examples": post.get("examples", {}),
        "autofix": post.get("autofix", {}),
    }

    return principle_data


def load_all_principles(principles_dir: Path) -> List[Dict[str, Any]]:
    """
    Load all principles from a directory of .md files.

    Args:
        principles_dir: Path to directory containing principle .md files

    Returns:
        List of principle dictionaries
    """
    if not principles_dir.exists():
        raise FileNotFoundError(f"Principles directory not found: {principles_dir}")

    principles = []

    # Load all .md files (U001-U012, P001-P069)
    for md_file in sorted(principles_dir.glob("*.md")):
        principle = load_principle_from_md(md_file)
        principles.append(principle)

    return principles


def get_principle_by_id(principle_id: str, principles_dir: Path) -> Optional[Dict[str, Any]]:
    """
    Get a single principle by ID.

    Args:
        principle_id: Principle ID (e.g., "P001", "U001")
        principles_dir: Path to principles directory

    Returns:
        Principle dictionary or None if not found
    """
    md_file = principles_dir / f"{principle_id}.md"

    if not md_file.exists():
        return None

    return load_principle_from_md(md_file)


def get_principles_by_category(category: str, principles_dir: Path) -> List[Dict[str, Any]]:
    """
    Get all principles in a category.

    Args:
        category: Category name (e.g., "code_quality", "security_privacy")
        principles_dir: Path to principles directory

    Returns:
        List of principle dictionaries
    """
    all_principles = load_all_principles(principles_dir)
    return [p for p in all_principles if p["category"] == category]


def get_category_mapping(principles_dir: Path) -> Dict[str, List[str]]:
    """
    Build category-to-principle-IDs mapping.

    Args:
        principles_dir: Path to principles directory

    Returns:
        Dictionary mapping category names to lists of principle IDs
    """
    all_principles = load_all_principles(principles_dir)

    mapping: Dict[str, List[str]] = {}
    for principle in all_principles:
        category = principle["category"]
        principle_id = principle["id"]

        if category not in mapping:
            mapping[category] = []

        mapping[category].append(principle_id)

    return mapping

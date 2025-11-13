"""
Hybrid CLAUDE.md Generator (NEW - CCO 3.1)

Generates CLAUDE.md with hybrid approach:
- Universal principles INLINE (~1,200 tokens)
- Project-specific principles by REFERENCE (dynamic)

This is the new generator for the dynamic architecture.
See claude_md_generator.py for legacy implementation.
"""

from pathlib import Path
from typing import Dict, List, Optional
import re


def generate_hybrid_claude_md(
    project_root: Path,
    project_config: Dict,
    cco_dir: Path
) -> str:
    """
    Generate hybrid CLAUDE.md with universal inline + project reference.

    Args:
        project_root: Project root directory
        project_config: Project configuration dict from project.json
        cco_dir: Path to ~/.cco/ directory

    Returns:
        Complete CLAUDE.md content
    """
    # Load universal principles template
    universal_template = _load_universal_template(cco_dir)

    # Check for existing CLAUDE.md
    claude_md_path = project_root / "CLAUDE.md"
    existing_content = None
    if claude_md_path.exists():
        existing_content = claude_md_path.read_text(encoding='utf-8')

    # Generate CCO section
    cco_section = _generate_cco_section(project_config, universal_template)

    # Merge with existing or create new
    if existing_content:
        if "<!-- CCO_START -->" in existing_content:
            # Update existing CCO section
            return _update_cco_section(existing_content, cco_section)
        else:
            # Append CCO section
            return f"{existing_content.rstrip()}\n\n{cco_section}"
    else:
        # Create new CLAUDE.md
        project_name = project_config.get("project_name", project_root.name)
        return f"# {project_name} - Claude Development Guide\n\n{cco_section}"


def _load_universal_template(cco_dir: Path) -> str:
    """Generate universal principles section dynamically from U*.md files."""
    from ..config import get_principles_dir
    from .principle_md_loader import load_all_principles

    principles_dir = get_principles_dir()
    if not principles_dir.exists():
        return """### Universal Principles
U001-U014 apply to all projects."""

    # Load all principles and filter universal ones
    all_principles = load_all_principles(principles_dir)
    universal_principles = [p for p in all_principles if p.get("category") == "universal"]
    universal_principles.sort(key=lambda p: p["id"])

    # Generate markdown
    lines = []
    for p in universal_principles:
        lines.append(f"- **{p['id']}**: {p['title']}")
        if p.get("one_line_why"):
            lines.append(f"  - {p['one_line_why']}")

    return "\n".join(lines) if lines else "U001-U014 apply to all projects."


def _generate_cco_section(project_config: Dict, universal_template: str) -> str:
    """Generate CCO section with universal inline + project reference."""
    selected_principles = project_config.get("selected_principles", {})

    # Count principles
    universal_count = len(selected_principles.get("universal", []))
    total_count = sum(len(ids) for ids in selected_principles.values())
    project_count = total_count - universal_count

    # Get available principle count dynamically
    from ..config import get_principles_dir
    principles_dir = get_principles_dir()
    available_project_principles = len(list(principles_dir.glob("P*.md")))

    # Generate category list
    category_list = _generate_category_list(selected_principles)

    return f"""---

<!-- CCO_START -->
## Development Principles & Guidelines

### Universal Principles (Apply to ALL Projects)

{universal_template}

---

### Project-Specific Principles

This project uses **{project_count}** selected principles from {available_project_principles} available.

Commands load them dynamically based on `.claude/project.json`.

**Selected Categories**:
{category_list}

**Note**: Commands like `/cco-audit`, `/cco-fix` automatically load relevant principles.

**References**:
- Universal principles: Always active (inline above)
- Project principles: See `.claude/principles/` directory
- Configuration: `.claude/project.json`

<!-- CCO_END -->
"""


def _generate_category_list(selected_principles: Dict[str, List[str]]) -> str:
    """Generate markdown list of selected categories."""
    category_names = {
        "code_quality": "Code Quality",
        "architecture": "Architecture",
        "security_privacy": "Security & Privacy",
        "testing": "Testing",
        "git_workflow": "Git Workflow",
        "performance": "Performance",
        "operations": "Operations",
        "api_design": "API Design"
    }

    lines = []
    for category, principle_ids in selected_principles.items():
        if category == "universal":
            continue

        if principle_ids:
            display_name = category_names.get(category, category.replace("_", " ").title())
            count = len(principle_ids)
            lines.append(f"- **{display_name}**: {count} principles")

    return "\n".join(lines) if lines else "- No project-specific categories selected"


def _update_cco_section(existing_content: str, new_cco_section: str) -> str:
    """Update existing CCO section in CLAUDE.md."""
    pattern = r'<!-- CCO_START -->.*?<!-- CCO_END -->'
    return re.sub(pattern, new_cco_section.strip(), existing_content, flags=re.DOTALL)


def remove_cco_section(claude_md_path: Path) -> bool:
    """
    Remove CCO section from CLAUDE.md.

    Args:
        claude_md_path: Path to CLAUDE.md

    Returns:
        True if section was removed, False if not found
    """
    if not claude_md_path.exists():
        return False

    content = claude_md_path.read_text(encoding='utf-8')

    if "<!-- CCO_START -->" not in content:
        return False

    # Remove content between markers
    pattern = r'\n*---\n*<!-- CCO_START -->.*?<!-- CCO_END -->\n*'
    updated_content = re.sub(pattern, '', content, flags=re.DOTALL)

    # Clean up multiple blank lines
    updated_content = re.sub(r'\n{3,}', '\n\n', updated_content)

    claude_md_path.write_text(updated_content.strip() + '\n', encoding='utf-8')
    return True

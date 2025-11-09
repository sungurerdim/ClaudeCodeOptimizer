#!/usr/bin/env python3
"""
Utility script to split PRINCIPLES.md by category.

Creates:
- docs/cco/principles/core.md (P001, P067, P071)
- docs/cco/principles/code-quality.md
- docs/cco/principles/security.md
- docs/cco/principles/testing.md
- docs/cco/principles/architecture.md
- docs/cco/principles/performance.md
- docs/cco/principles/operations.md
- docs/cco/principles/git-workflow.md
- docs/cco/principles/api-design.md
"""

import io
import json
import sys
from datetime import datetime
from pathlib import Path

# Fix Windows encoding issues
if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(
        sys.stdout.buffer,
        encoding="utf-8",
        errors="replace",
        line_buffering=True,
    )
    sys.stderr = io.TextIOWrapper(
        sys.stderr.buffer,
        encoding="utf-8",
        errors="replace",
        line_buffering=True,
    )

# Core principles (always loaded, ~500 tokens)
CORE_PRINCIPLES = ["P001", "P067", "P071"]

# Category mapping
CATEGORY_FILES = {
    "code_quality": "code-quality.md",
    "security_privacy": "security.md",
    "testing": "testing.md",
    "architecture": "architecture.md",
    "performance": "performance.md",
    "operations": "operations.md",
    "git_workflow": "git-workflow.md",
    "api_design": "api-design.md",
}


def load_principles():
    """Load principles from knowledge base"""
    principles_file = Path("claudecodeoptimizer/knowledge/principles.json")
    with open(principles_file, encoding="utf-8") as f:
        data = json.load(f)
    return data["principles"], data["categories"]


def render_principle(principle):
    """Render a single principle to markdown"""
    lines = []

    # Header
    severity_emoji = {"critical": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢"}.get(
        principle.get("severity", "medium"),
        "",
    )

    lines.append(f"### {principle['id']}: {principle['title']} {severity_emoji}")
    lines.append("")
    lines.append(f"**Severity**: {principle.get('severity', 'medium').title()}")
    lines.append("")

    # Description
    lines.append(principle["description"])
    lines.append("")

    # Applicability
    if "applicability" in principle:
        app = principle["applicability"]
        if app.get("project_types") and app["project_types"] != ["all"]:
            lines.append(f"**Project Types**: {', '.join(app['project_types'])}")
            lines.append("")
        if app.get("languages") and app["languages"] != ["all"]:
            lines.append(f"**Languages**: {', '.join(app['languages'])}")
            lines.append("")

    # Rules
    if "rules" in principle and principle["rules"]:
        lines.append("**Rules**:")
        for rule in principle["rules"]:
            lines.append(f"- {rule['description']}")
        lines.append("")

    # Examples
    if "examples" in principle:
        examples = principle["examples"]

        if examples.get("bad"):
            lines.append("**❌ Bad**:")
            lines.append("```")
            lines.append(examples["bad"][0])
            lines.append("```")
            lines.append("")

        if examples.get("good"):
            lines.append("**✅ Good**:")
            lines.append("```")
            lines.append(examples["good"][0])
            lines.append("```")
            lines.append("")

    lines.append("---")
    lines.append("")

    return "\n".join(lines)


def create_category_file(category_id, category_name, principles, output_dir):
    """Create a category-specific principles file"""
    lines = []

    # Header
    lines.append(f"# {category_name} Principles")
    lines.append("")
    lines.append(f"**Generated**: {datetime.now().strftime('%Y-%m-%d')}")
    lines.append(f"**Principle Count**: {len(principles)}")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Principles
    for principle in sorted(principles, key=lambda p: p["number"]):
        lines.append(render_principle(principle))

    # Footer
    lines.append("---")
    lines.append("")
    lines.append("**Loading**: These principles load automatically when running relevant commands")
    lines.append("")
    lines.append(
        "**Reference**: Use `@PRINCIPLES.md` to load core principles, or reference this file directly",
    )

    # Write file
    filename = CATEGORY_FILES.get(category_id, f"{category_id}.md")
    filepath = output_dir / filename
    filepath.write_text("\n".join(lines), encoding="utf-8")

    print(f"✓ Created {filepath} ({len(principles)} principles)")


def create_core_file(core_principles, output_dir):
    """Create core principles file (always loaded)"""
    lines = []

    # Header
    lines.append("# Core Development Principles")
    lines.append("")
    lines.append("**⚠️ CRITICAL: Always Apply These Principles ⚠️**")
    lines.append("")
    lines.append(f"**Generated**: {datetime.now().strftime('%Y-%m-%d')}")
    lines.append(f"**Principle Count**: {len(core_principles)}")
    lines.append("")
    lines.append("These are the most critical principles that apply to ALL work, ALWAYS.")
    lines.append("")
    lines.append("---")
    lines.append("")

    # Principles
    for principle in sorted(core_principles, key=lambda p: p["number"]):
        lines.append(render_principle(principle))

    # Footer
    lines.append("---")
    lines.append("")
    lines.append("**Note**: These core principles are always loaded (~500 tokens)")
    lines.append("")
    lines.append("For category-specific principles, see:")
    lines.append("- [Code Quality](code-quality.md)")
    lines.append("- [Security](security.md)")
    lines.append("- [Testing](testing.md)")
    lines.append("- [Architecture](architecture.md)")
    lines.append("- [Performance](performance.md)")
    lines.append("- [Operations](operations.md)")
    lines.append("- [Git Workflow](git-workflow.md)")
    lines.append("- [API Design](api-design.md)")

    # Write file
    filepath = output_dir / "core.md"
    filepath.write_text("\n".join(lines), encoding="utf-8")

    print(f"✓ Created {filepath} ({len(core_principles)} core principles)")


def main():
    """Split principles into category files"""
    print("Loading principles...")
    all_principles, categories = load_principles()

    output_dir = Path("docs/cco/principles")
    output_dir.mkdir(parents=True, exist_ok=True)

    # Group principles by category (deduplicate by ID)
    principles_by_category = {}
    core_principles_list = []
    seen_core_ids = set()
    seen_category_ids = {}

    for principle in all_principles:
        pid = principle["id"]
        category = principle.get("category", "code_quality")

        # Core principles go into separate file (deduplicate)
        if pid in CORE_PRINCIPLES and pid not in seen_core_ids:
            core_principles_list.append(principle)
            seen_core_ids.add(pid)

        # Also add to category (for full category files, deduplicate)
        if category not in principles_by_category:
            principles_by_category[category] = []
            seen_category_ids[category] = set()

        if pid not in seen_category_ids[category]:
            principles_by_category[category].append(principle)
            seen_category_ids[category].add(pid)

    # Create core file
    print("\nCreating core principles file...")
    create_core_file(core_principles_list, output_dir)

    # Create category files
    print("\nCreating category-specific files...")
    for category_data in categories:
        category_id = category_data["id"]
        category_name = category_data["name"]

        if category_id in principles_by_category:
            create_category_file(
                category_id,
                category_name,
                principles_by_category[category_id],
                output_dir,
            )

    print("\n✅ Split complete!")
    print(f"\nCreated {len(categories) + 1} files in {output_dir}")
    print("\nToken optimization:")
    print("- Before: ~5000 tokens (all principles)")
    print("- After: ~500 tokens (core only)")
    print("- Reduction: 10x")


if __name__ == "__main__":
    main()

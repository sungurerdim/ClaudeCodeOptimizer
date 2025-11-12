"""Generate individual principle files from principles.json.

This script transforms the grouped principle structure into individual files:
- Input: content/principles.json (74 principles with metadata)
- Output: content/principles/P001.md, P002.md, ..., P074.md (74 files)

Usage:
    python scripts/generate_individual_principles.py
"""

import json
from pathlib import Path
from typing import Any


def severity_emoji(severity: str) -> str:
    """Return emoji for severity level."""
    mapping = {
        "critical": "🔴",
        "high": "🔴",
        "medium": "🟡",
        "low": "🟢",
    }
    return mapping.get(severity.lower(), "⚪")


def format_applicability(applicability: dict[str, Any]) -> str:
    """Format applicability section."""
    lines = []

    if "project_types" in applicability and applicability["project_types"]:
        types = ", ".join(applicability["project_types"])
        lines.append(f"**Project Types**: {types}")

    if "languages" in applicability and applicability["languages"]:
        langs = ", ".join(applicability["languages"])
        lines.append(f"**Languages**: {langs}")

    if "team_sizes" in applicability and applicability["team_sizes"]:
        sizes = ", ".join(applicability["team_sizes"])
        lines.append(f"**Team Sizes**: {sizes}")

    if "maturity_levels" in applicability and applicability["maturity_levels"]:
        levels = ", ".join(applicability["maturity_levels"])
        lines.append(f"**Maturity Levels**: {levels}")

    return "\n".join(lines) if lines else ""


def format_examples(examples: dict[str, list[str]] | list[dict] | list[str]) -> str:
    """Format examples section."""
    if not examples:
        return ""

    lines = []

    # Handle dict with bad/good arrays (from principles.json)
    if isinstance(examples, dict):
        if "bad" in examples and examples["bad"]:
            lines.append("**❌ Bad**:")
            lines.append("```")
            for bad_example in examples["bad"]:
                # Replace \n with actual newlines
                formatted = bad_example.replace("\\n", "\n").strip()
                lines.append(formatted)
            lines.append("```")
            lines.append("")

        if "good" in examples and examples["good"]:
            lines.append("**✅ Good**:")
            lines.append("```")
            for good_example in examples["good"]:
                # Replace \n with actual newlines
                formatted = good_example.replace("\\n", "\n").strip()
                lines.append(formatted)
            lines.append("```")
            lines.append("")

        return "\n".join(lines).rstrip()

    # Handle list of examples (legacy format)
    for example in examples:
        # Handle string examples
        if isinstance(example, str):
            lines.append(example)
            lines.append("")
            continue

        # Handle dict examples
        if isinstance(example, dict):
            if "bad" in example:
                lines.append("**❌ Bad**:")
                lang = example.get("language", "")
                lines.append(f"```{lang}")
                lines.append(example["bad"].strip())
                lines.append("```")
                lines.append("")

            if "good" in example:
                lines.append("**✅ Good**:")
                lang = example.get("language", "")
                lines.append(f"```{lang}")
                lines.append(example["good"].strip())
                lines.append("```")
                lines.append("")

    return "\n".join(lines).rstrip()


def format_rules(rules: list[dict[str, str]]) -> str:
    """Format rules section."""
    if not rules:
        return ""

    lines = []
    for rule in rules:
        rule_id = rule.get("id", "")
        description = rule.get("description", "")
        if description:
            lines.append(f"- **{rule_id.replace('-', ' ').title()}**: {description}")

    return "\n".join(lines)


def generate_principle_file(principle: dict[str, Any], output_dir: Path) -> None:
    """Generate a single principle markdown file."""
    principle_id = principle["id"]
    principle_num = principle["number"]
    title = principle["title"]
    category = principle["category"]
    severity = principle.get("severity", "medium")
    weight = principle.get("weight", 5)
    enforcement = principle.get("enforcement", "SHOULD")
    description = principle.get("description", "")
    one_line_why = principle.get("one_line_why", "")

    # Frontmatter
    content = f"""---
id: {principle_id}
number: {principle_num}
title: {title}
category: {category}
severity: {severity}
weight: {weight}
"""

    # Add enforcement to frontmatter if it's a string
    if enforcement and isinstance(enforcement, str):
        content += f"enforcement: {enforcement}\n"

    # Add applicability if present
    if "applicability" in principle and principle["applicability"]:
        applicability = principle["applicability"]
        content += "applicability:\n"
        if "project_types" in applicability:
            content += f"  project_types: {applicability['project_types']}\n"
        if "languages" in applicability:
            content += f"  languages: {applicability['languages']}\n"
        if "team_sizes" in applicability:
            content += f"  team_sizes: {applicability['team_sizes']}\n"
        if "maturity_levels" in applicability:
            content += f"  maturity_levels: {applicability['maturity_levels']}\n"

    content += "---\n\n"

    # Title with emoji
    emoji = severity_emoji(severity)
    content += f"# {principle_id}: {title} {emoji}\n\n"

    # Severity
    content += f"**Severity**: {severity.title()}\n\n"

    # Description
    if description:
        content += f"{description}\n\n"

    # Why
    if one_line_why:
        content += f"**Why**: {one_line_why}\n\n"

    # Enforcement
    if enforcement:
        # Handle dict enforcement (skill references)
        if isinstance(enforcement, dict):
            skills = [skill for skill, enabled in enforcement.items() if enabled]
            if skills:
                content += f"**Enforcement**: Skills required - {', '.join(skills)}\n\n"
        else:
            content += f"**Enforcement**: {enforcement}\n\n"

    # Applicability
    if "applicability" in principle:
        applicability_text = format_applicability(principle["applicability"])
        if applicability_text:
            content += f"{applicability_text}\n\n"

    # Rules
    if "rules" in principle and principle["rules"]:
        rules_text = format_rules(principle["rules"])
        if rules_text:
            content += f"**Rules**:\n{rules_text}\n\n"

    # Examples
    if "examples" in principle and principle["examples"]:
        examples_text = format_examples(principle["examples"])
        if examples_text:
            content += f"{examples_text}\n"

    # Autofix info
    if "autofix" in principle and principle["autofix"]:
        autofix = principle["autofix"]
        if autofix.get("available"):
            content += "\n## Autofix Available\n\n"
            if "pattern" in autofix:
                content += f"**Pattern**: `{autofix['pattern']}`\n"
            if "fix_type" in autofix:
                content += f"**Fix Type**: {autofix['fix_type']}\n"
            if "confidence" in autofix:
                content += f"**Confidence**: {autofix['confidence']}\n"
            content += "\n"

    # Related principles
    if "related_principles" in principle and principle["related_principles"]:
        related = ", ".join(principle["related_principles"])
        content += f"\n**Related**: {related}\n"

    # Write file
    output_file = output_dir / f"{principle_id}.md"
    output_file.write_text(content, encoding="utf-8")
    print(f"[OK] Generated {output_file.name}")


def main() -> None:
    """Main execution."""
    # Paths
    repo_root = Path(__file__).parent.parent
    principles_json = repo_root / "content" / "principles.json"
    output_dir = repo_root / "content" / "principles"

    # Validate input
    if not principles_json.exists():
        print(f"[ERROR] Principles file not found: {principles_json}")
        return

    # Load principles
    print(f"Loading principles from {principles_json}...")
    with open(principles_json, encoding="utf-8") as f:
        data = json.load(f)

    principles = data.get("principles", [])
    print(f"Found {len(principles)} principles")

    # Create output directory if needed
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate individual files
    print(f"\nGenerating individual files to {output_dir}...")
    for principle in principles:
        generate_principle_file(principle, output_dir)

    print(f"\n[SUCCESS] Generated {len(principles)} principle files")
    print(f"[OUTPUT] {output_dir}")

    # Summary
    categories = {}
    for principle in principles:
        category = principle["category"]
        categories[category] = categories.get(category, 0) + 1

    print("\n[SUMMARY] Principles by category:")
    for category, count in sorted(categories.items()):
        print(f"  - {category}: {count} principles")


if __name__ == "__main__":
    main()

"""
CLAUDE.md Generator - CCO 3.0

Generates or enhances project-specific CLAUDE.md based on:
1. Template from CCO package (CLAUDE.md in root)
2. Existing project CLAUDE.md (if present)
3. User preferences for customization

Strategy:
- If no CLAUDE.md exists: Use template + customize
- If CLAUDE.md exists: Merge template sections + customize
"""

from datetime import datetime
from pathlib import Path
from typing import Any, Dict

from .constants import UI_HEADING_LEVEL_SECONDARY


class ClaudeMdGenerator:
    """
    Generate or enhance CLAUDE.md with preferences-based customization.

    Uses template-based approach:
    1. Load template from package
    2. Check for existing CLAUDE.md
    3. Merge intelligently
    4. Customize based on preferences
    """

    def __init__(self, preferences: Dict[str, Any]) -> None:
        """
        Initialize generator with user preferences.

        Args:
            preferences: User preferences dictionary from CCOPreferences.dict()
        """
        self.preferences = preferences
        self.template_path = Path(__file__).parent.parent.parent / "CLAUDE.md"

    def generate(self, output_path: Path) -> Dict[str, Any]:
        """
        Generate or enhance CLAUDE.md file.

        Args:
            output_path: Path to write CLAUDE.md (typically .claude/CLAUDE.md)

        Returns:
            Dictionary with generation results
        """
        # Load template
        template_content = self._load_template()

        # Check if project already has CLAUDE.md
        existing_content = self._load_existing(output_path)

        # Merge or use template
        if existing_content:
            content = self._merge_contents(template_content, existing_content)
            strategy = "merged"
        else:
            content = template_content
            strategy = "template"

        # Customize based on preferences
        content = self._customize_content(content)

        # Write file
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(content, encoding="utf-8")

        return {
            "success": True,
            "file_path": str(output_path),
            "size": len(content),
            "strategy": strategy,
        }

    def _load_template(self) -> str:
        """Load CLAUDE.md template from package"""
        if not self.template_path.exists():
            # Fallback: Generate minimal template
            return self._generate_minimal_template()

        return self.template_path.read_text(encoding="utf-8")

    def _load_existing(self, output_path: Path) -> str:
        """Load existing CLAUDE.md if present"""
        if output_path.exists():
            return output_path.read_text(encoding="utf-8")
        return ""

    def _merge_contents(self, template: str, existing: str) -> str:
        """
        Intelligently merge template and existing CLAUDE.md.

        Strategy:
        1. Parse both into sections
        2. Keep all existing sections
        3. Add missing sections from template
        4. Update "Development Principles" section to ensure @PRINCIPLES.md reference
        """
        template_sections = self._parse_sections(template)
        existing_sections = self._parse_sections(existing)

        # Start with existing content
        merged_sections = existing_sections.copy()

        # Ensure "Development Principles" section exists with @PRINCIPLES.md reference
        if "Development Principles" not in merged_sections:
            if "Development Principles" in template_sections:
                merged_sections["Development Principles"] = template_sections[
                    "Development Principles"
                ]

        # Add missing sections from template (except header)
        for section_name, section_content in template_sections.items():
            if section_name == "Header":
                continue  # Keep existing header

            if section_name not in merged_sections:
                # This section doesn't exist in project's CLAUDE.md
                # Add it from template
                merged_sections[section_name] = section_content

        # Rebuild content
        return self._rebuild_from_sections(merged_sections, existing_sections)

    def _parse_sections(self, content: str) -> Dict[str, str]:
        """
        Parse markdown content into sections.

        Returns dict: {section_name: section_content}
        """
        sections = {}
        lines = content.split("\n")

        current_section = "Header"
        current_content = []

        for line in lines:
            # Check if this is a section header (## Something)
            if line.startswith("## "):
                # Save previous section
                if current_content:
                    sections[current_section] = "\n".join(current_content)

                # Start new section
                current_section = line[3:].strip()  # Remove "## "
                current_content = [line]
            else:
                current_content.append(line)

        # Save last section
        if current_content:
            sections[current_section] = "\n".join(current_content)

        return sections

    def _rebuild_from_sections(
        self,
        merged_sections: Dict[str, str],
        original_order: Dict[str, str],
    ) -> str:
        """
        Rebuild markdown content from sections.

        Maintains original section order, appends new sections at end.
        """
        lines = []

        # First, add sections in original order
        added_sections = set()
        for section_name in original_order.keys():
            if section_name in merged_sections:
                lines.append(merged_sections[section_name])
                added_sections.add(section_name)

        # Then add new sections (from template) that weren't in original
        for section_name, section_content in merged_sections.items():
            if section_name not in added_sections:
                lines.append("")  # Empty line before new section
                lines.append(section_content)

        return "\n".join(lines)

    def _customize_content(self, content: str) -> str:
        """
        Customize content based on user preferences.

        Adds project-specific information:
        - Project name in header
        - Team size
        - Quality standards
        - Testing strategy
        """
        # Get preferences
        project_name = self._get_pref("project_identity.name")
        team_size = self._get_pref("project_identity.team_trajectory", "solo")
        linting = self._get_pref("code_quality.linting_strictness", "standard")
        testing = self._get_pref("testing.strategy", "balanced")

        # Add preference metadata after header
        metadata = self._generate_metadata(project_name, team_size, linting, testing)

        # Insert metadata after first header line
        lines = content.split("\n")
        insert_index = 0

        # Find first ## or --- (end of header)
        for i, line in enumerate(lines):
            if i > 0 and (line.startswith("##") or line.startswith("---")):
                insert_index = i
                break

        # Insert metadata
        if insert_index > 0:
            lines.insert(insert_index, "")
            lines.insert(insert_index + 1, metadata)
            content = "\n".join(lines)

        # Add conditional sections based on preferences
        content = self._add_conditional_sections(content, team_size, linting, testing)

        return content

    def _generate_metadata(
        self,
        project_name: str,
        team_size: str,
        linting: str,
        testing: str,
    ) -> str:
        """Generate metadata section"""
        if not project_name:
            return ""

        team_label = self._format_team_size(team_size)

        return f"""**Project:** {project_name}
**Team:** {team_label}
**Quality:** {linting.title()}
**Testing:** {testing.title()}
**Generated:** {datetime.now().strftime('%Y-%m-%d')}"""

    def _add_conditional_sections(
        self,
        content: str,
        team_size: str,
        linting: str,
        testing: str,
    ) -> str:
        """
        Add conditional sections based on preferences.

        - Test-First Development (for TDD projects)
        - Root Cause Analysis (for strict quality)
        - Code Review Guidelines (for teams)
        """
        additions = []

        # Add Test-First section for TDD
        if testing in ["tdd", "test-first"]:
            if "Test-First Development" not in content:
                additions.append(self._get_test_first_section())

        # Add Root Cause Analysis for strict linting
        if linting in ["strict", "pedantic", "paranoid"]:
            if "Root Cause Analysis" not in content:
                additions.append(self._get_root_cause_section())

        # Add Code Review section for teams
        if team_size != "solo":
            if "Code Review" not in content and "Git Workflow" not in content:
                additions.append(self._get_code_review_section())

        # Append additions before final footer
        if additions:
            # Find footer (last ---)
            parts = content.rsplit("\n---\n", 1)
            if len(parts) == UI_HEADING_LEVEL_SECONDARY:
                content = parts[0] + "\n\n" + "\n\n".join(additions) + "\n\n---\n" + parts[1]
            else:
                content += "\n\n" + "\n\n".join(additions)

        return content

    def _get_test_first_section(self) -> str:
        """Get Test-First Development section"""
        return """## Test-First Development

**For new features:**
- Write failing test FIRST
- Run test, verify it fails
- Implement feature
- Run test, verify it passes

**For bugs:**
- Reproduce bug with failing test
- Verify test fails for the right reason
- Fix bug
- Verify test passes

**Why:** Confirms you're testing the right thing, prevents false positives

---"""

    def _get_root_cause_section(self) -> str:
        """Get Root Cause Analysis section"""
        return """## Root Cause Analysis

**When debugging, always trace to source:**

1. **Where does the bad value originate?**
   - Don't fix symptoms (validation checks deep in stack)
   - Trace backward through the call chain

2. **What called this with the bad value?**
   - Keep tracing up the stack
   - Find where it enters the system

3. **Fix at source, not symptom**
   - Add validation at entry point
   - Consider defense-in-depth for critical paths

**Example:**
```
Error: Function crashes with empty string
↓ Trace: ProcessData('') called function
↓ Trace: APIHandler passed empty string
↓ Trace: User input validation missing
✅ Fix: Add validation at API entry point
❌ Wrong: Add null check in ProcessData
```

---"""

    def _get_code_review_section(self) -> str:
        """Get Code Review Guidelines section"""
        return """## Code Review Guidelines

**All changes require review before merge:**
- Create PR with clear description
- Link related issues
- Include test evidence
- Address all review comments
- No self-merges without approval

**PR best practices:**
- Keep PRs small (<400 lines)
- One logical change per PR
- Update documentation
- Add tests for new features

---"""

    def _generate_minimal_template(self) -> str:
        """Generate minimal template if package template not found"""
        return """# Claude Code Development Guide

**Universal guide for working with Claude Code**

---

## Development Principles

**⚠️ MANDATORY: All work MUST follow these principles ⚠️**

```
@PRINCIPLES.md
```

This file contains the mandatory development principles for this project. **You MUST**:
- Follow ALL applicable principles in EVERY task
- Never deviate from these principles without explicit approval
- Check compliance before claiming work is complete
- Reference principles when making decisions

**Usage:**
```
@PRINCIPLES.md  # Read at start of every session
@PRINCIPLES.md Check if this code follows our principles
@PRINCIPLES.md What principle applies to error handling?
```

**Compliance is non-negotiable.** These principles are not suggestions - they are requirements.

---

## Working Guidelines

### What NOT to Do
- ❌ No tests/linters/repo scans unless explicitly requested
- ❌ No TODO markers, debug prints, or dead code
- ❌ Never create files unless absolutely necessary

### Always Prefer
- ✅ Edit existing files over creating new ones
- ✅ Follow existing code patterns
- ✅ Minimal, surgical changes
- ✅ Production-grade code from the start

---

## Verification Protocol

**BEFORE claiming any work is complete:**

1. **IDENTIFY**: What command proves this claim?
2. **RUN**: Execute the command
3. **VERIFY**: Check exit code, count failures
4. **REPORT**: State claim WITH evidence

---
"""

    def _format_team_size(self, team_size: str) -> str:
        """Format team size for display"""
        mapping = {
            "solo": "Solo Developer",
            "small-2-5": "Small Team (2-5)",
            "medium-5-10": "Medium Team (5-10)",
            "large-10-30": "Large Team (10-30)",
            "enterprise-30+": "Enterprise (30+)",
        }
        return mapping.get(team_size, team_size.title())

    def _get_pref(self, path: str, default: Any = None) -> Any:
        """Get nested preference value"""
        parts = path.split(".")
        current = self.preferences

        for part in parts:
            if isinstance(current, dict):
                current = current.get(part)
            elif hasattr(current, part):
                current = getattr(current, part)
            else:
                return default

            if current is None:
                return default

        return current


# Utility function
def generate_claude_md(preferences: Dict[str, Any], output_path: Path) -> Dict[str, Any]:
    """
    Convenience function to generate CLAUDE.md.

    Args:
        preferences: User preferences dictionary
        output_path: Path to write CLAUDE.md

    Returns:
        Generation result
    """
    generator = ClaudeMdGenerator(preferences)
    return generator.generate(output_path)


__all__ = [
    "ClaudeMdGenerator",
    "generate_claude_md",
]

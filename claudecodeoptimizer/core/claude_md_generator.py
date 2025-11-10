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

import shutil
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
        self.template_path = Path(__file__).parent.parent.parent / "templates" / "CLAUDE.md.template"

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

        # Create backup if file exists (before writing)
        if output_path.exists():
            self._create_backup(output_path)

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
        4. Update "Development Principles" section with template content if missing
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
**Generated:** {datetime.now().strftime("%Y-%m-%d")}"""

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
        - Git Workflow (based on team size and git_workflow preference)
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

        # Add Git Workflow section (based on preference)
        git_workflow = self._get_pref("collaboration.git_workflow", "main_only")
        if "Git Workflow" not in content:
            additions.append(self._get_git_workflow_section(git_workflow, team_size))

        # Add Versioning Strategy section (P074)
        versioning_strategy = self._get_pref("collaboration.versioning_strategy", "auto_semver")
        if "Versioning Strategy" not in content and versioning_strategy != "no_versioning":
            additions.append(self._get_versioning_section(versioning_strategy))

        # Add Code Review section for teams (if not already covered by Git Flow)
        if team_size != "solo" and git_workflow != "git_flow":
            if "Code Review" not in content:
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

    def _create_backup(self, file_path: Path) -> None:
        """
        Create timestamped backup of existing file in global storage.

        Keeps last 5 backups, deletes older ones.
        Format: ~/.cco/projects/{project_name}/backups/{filename}.YYYYMMDD_HHMMSS.backup

        Args:
            file_path: Path to file to backup (e.g., project_root/CLAUDE.md)
        """
        if not file_path.exists():
            return  # No file to backup

        # Get project name from file's parent directory
        project_root = file_path.parent
        project_name = project_root.name

        # Get backup directory from global storage
        from ..config import CCOConfig

        backup_dir = CCOConfig.get_project_backups_dir(project_name)

        # Create backup directory if it doesn't exist
        backup_dir.mkdir(parents=True, exist_ok=True)

        # Create timestamped backup
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"{file_path.name}.{timestamp}.backup"
        backup_path = backup_dir / backup_filename

        # Copy file to backup
        shutil.copy2(file_path, backup_path)

        # Keep only last 5 backups for this file
        backup_pattern = f"{file_path.name}.*.backup"
        backups = sorted(backup_dir.glob(backup_pattern))

        # Delete old backups (keep last 5)
        for old_backup in backups[:-5]:
            old_backup.unlink()

    def _get_git_workflow_section(self, workflow_type: str, team_size: str) -> str:
        """
        Generate Git Workflow section based on preference.

        Args:
            workflow_type: main_only, github_flow, git_flow, or custom
            team_size: Team size for fallback logic

        Returns:
            Formatted Git Workflow section
        """
        # Force main-only for solo devs
        if team_size == "solo" or workflow_type == "main_only":
            return self._get_main_only_workflow()
        elif workflow_type == "github_flow":
            return self._get_github_flow_workflow()
        elif workflow_type == "git_flow":
            return self._get_git_flow_workflow()
        else:  # custom or unknown
            return self._get_custom_workflow_template()

    def _get_main_only_workflow(self) -> str:
        """Get Main-Only workflow (Solo/Small teams)"""
        return """## Git Workflow

**Strategy**: Main-Only (Solo Developer)

**Workflow**:
- Single `main` branch, direct commits
- Follow P072 (Concise Commits), P073 (Atomic Commits)
- Push after each completed task

**Principles**: See `.claude/principles/git-workflow.md`

---"""

    def _get_github_flow_workflow(self) -> str:
        """Get GitHub Flow (Small-Medium teams)"""
        return """## Git Workflow

**Strategy**: GitHub Flow (Feature Branches + PRs)

**Branches**:
- `main` - Production-ready code
- `feature/<name>` - Feature branches
- `hotfix/<issue>` - Hotfix branches

**Process**:
1. Branch from main → work → open PR
2. Code review required (1-2 reviewers)
3. Merge to main after approval
4. CI checks must pass

**Principles**: See `.claude/principles/git-workflow.md`

---"""

    def _get_git_flow_workflow(self) -> str:
        """Get Git Flow (Large teams/Production)"""
        return """## Git Workflow

**Strategy**: Git Flow (develop + main + feature/release/hotfix branches)

**Branches**:
- `main` - Production releases only
- `develop` - Integration branch
- `feature/<name>`, `release/<version>`, `hotfix/<issue>`

**Process**:
1. Feature: develop → feature → PR to develop
2. Release: develop → release → merge to main + develop
3. Hotfix: main → hotfix → merge to main + develop

**Branch Protection**: PRs required, CI/CD on all branches

**Principles**: See `.claude/principles/git-workflow.md`

---"""

    def _get_custom_workflow_template(self) -> str:
        """Get Custom workflow template"""
        return """## Git Workflow

**Branch Strategy: Custom**

[Define your branching strategy here]

**Commit Strategy**:
- [Define your commit message format]
- [Define when to commit/push]

**Code Review Process**:
- [Define your review process]

**Versioning**:
- [Define your versioning scheme]

---"""

    def _get_versioning_section(self, strategy: str) -> str:
        """
        Generate Versioning Strategy section based on preference (P074).

        Args:
            strategy: auto_semver, pr_based_semver, manual_semver, or calver

        Returns:
            Formatted Versioning Strategy section
        """
        if strategy == "auto_semver":
            return self._get_auto_semver_section()
        elif strategy == "pr_based_semver":
            return self._get_pr_based_semver_section()
        elif strategy == "manual_semver":
            return self._get_manual_semver_section()
        elif strategy == "calver":
            return self._get_calver_section()
        else:
            return ""  # no_versioning or unknown

    def _get_auto_semver_section(self) -> str:
        """Get Automatic SemVer section"""
        return """## Versioning Strategy (P074)

**Strategy**: Automated Semantic Versioning

**Usage**:
```python
from claudecodeoptimizer.core.version_manager import VersionManager
vm = VersionManager(Path.cwd())
vm.auto_bump(update_changelog=True, create_tag=True)
```

**Trigger**: Before release, after merge to main, or manually

**Principles**: See `.claude/principles/git-workflow.md` (P074)

---"""

    def _get_pr_based_semver_section(self) -> str:
        """Get PR-Based SemVer section"""
        return """## Versioning Strategy (P074)

**Strategy**: PR-Based Semantic Versioning (reviewer confirms)

**Workflow**:
1. PR author suggests version bump in PR description
2. Reviewer confirms or adjusts
3. CI/CD auto-bumps on merge

**Manual Bump**:
```bash
python -m claudecodeoptimizer.core.version_manager auto_bump --update-changelog --create-tag
```

**Principles**: See `.claude/principles/git-workflow.md` (P074)

---"""

    def _get_manual_semver_section(self) -> str:
        """Get Manual SemVer section"""
        return """## Versioning Strategy (P074)

**Strategy**: Manual Semantic Versioning (release managers control)

**Process**:
1. Review commits: `git log $(git describe --tags --abbrev=0)..HEAD`
2. Update version files (pyproject.toml, package.json, etc.)
3. Update CHANGELOG.md
4. Create tag: `git tag -a v1.3.0 -m "Release 1.3.0"`

**Helper Tool**:
```bash
python -m claudecodeoptimizer.core.version_manager auto_bump --dry-run
```

**Principles**: See `.claude/principles/git-workflow.md` (P074)

---"""

    def _get_calver_section(self) -> str:
        """Get Calendar Versioning section"""
        return """## Versioning Strategy

**Strategy**: Calendar Versioning (CalVer)

**Format**: YYYY.MM.DD or YYYY.MM.PATCH

**Usage**:
```python
from datetime import datetime
version = datetime.now().strftime("%Y.%m.%d")
# Update version files, create tag
```

**Best for**: Time-based or marketing-driven releases

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

    def _get_pref(self, path: str, default: Any = None) -> Any:  # noqa: ANN401
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

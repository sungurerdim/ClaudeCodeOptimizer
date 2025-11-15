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
from typing import Any, Dict, List

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

    def __init__(
        self,
        preferences: Dict[str, Any],
        selected_skills: List[str] | None = None,
        selected_agents: List[str] | None = None,
    ) -> None:
        """
        Initialize generator with user preferences.

        Args:
            preferences: User preferences dictionary from CCOPreferences.dict()
            selected_skills: List of selected skill IDs (optional)
            selected_agents: List of selected agent IDs (optional)
        """
        self.preferences = preferences
        self.selected_skills = selected_skills or []
        self.selected_agents = selected_agents or []
        self.principles_dir = Path(__file__).parent.parent.parent / "content" / "principles"

    def generate(self, output_path: Path) -> Dict[str, Any]:
        """
        Generate or enhance CLAUDE.md file.

        Args:
            output_path: Path to write CLAUDE.md

        Returns:
            Dictionary with generation results
        """
        # Check if project already has CLAUDE.md
        existing_content = self._load_existing(output_path)

        if existing_content:
            # Use existing file as base
            content = existing_content
            strategy = "updated"
        else:
            # Create new file from scratch with markers
            content = self._create_base_structure()
            strategy = "created"

        # Customize based on preferences
        content = self._customize_content(content)

        # Inject selected principles
        content = self._inject_principles(content)

        # Inject selected skills
        content = self._inject_skills(content)

        # Inject selected agents
        content = self._inject_agents(content)

        # Inject Claude guidelines
        content = self._inject_claude_guidelines(content)

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

    def _create_base_structure(self) -> str:
        """Create base CLAUDE.md structure with markers"""
        return """# Claude Code Development Guide

## Development Principles

<!-- CCO_PRINCIPLES_START -->
[Principles will be dynamically injected here]
<!-- CCO_PRINCIPLES_END -->

## Available Skills

<!-- CCO_SKILLS_START -->
[Skills will be dynamically injected here]
<!-- CCO_SKILLS_END -->

## Available Agents

<!-- CCO_AGENTS_START -->
[Agents will be dynamically injected here]
<!-- CCO_AGENTS_END -->

## Claude Guidelines

<!-- CCO_CLAUDE_START -->
[Claude-specific guidelines will be dynamically injected here]
<!-- CCO_CLAUDE_END -->
"""

    def _load_existing(self, output_path: Path) -> str:
        """Load existing CLAUDE.md if present"""
        if output_path.exists():
            return output_path.read_text(encoding="utf-8")
        return ""

    def _customize_content(self, content: str) -> str:
        """
        Customize content based on user preferences.

        Adds project-specific information:
        - Project name in header
        - Team size
        - Quality standards
        - Testing strategy
        """
        # Get preferences - support both nested and flat structures
        project_name = self._get_pref("project_identity.name") or self._get_pref("project_name")
        team_size = self._get_pref("project_identity.team_trajectory") or self._get_pref(
            "team_size", "solo"
        )
        linting = self._get_pref("code_quality.linting_strictness") or self._get_pref(
            "quality_level", "standard"
        )
        testing = self._get_pref("testing.strategy", "balanced")

        # Add preference metadata after header (if not already present)
        if "**Project:**" not in content:
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

        # Note: Conditional sections removed for simplicity
        # Users can manually add custom sections to their CLAUDE.md if needed

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

        team_size = team_size or "solo"
        linting = linting or "standard"
        team_label = self._format_team_size(team_size)

        return f"""**Project:** {project_name}
**Team:** {team_label}
**Quality:** {linting.title()}
**Testing:** {(testing or "balanced").title()}
**Generated:** {datetime.now().strftime("%Y-%m-%d")}
"""

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

        # Add Versioning Strategy section (automated semantic versioning)
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
- Follow U_CONCISE_COMMITS, U_ATOMIC_COMMITS
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
        Generate Versioning Strategy section based on preference (automated semantic versioning).

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
        return """## Versioning Strategy

**Strategy**: Automated Semantic Versioning

**Usage**:
```python
from claudecodeoptimizer.core.version_manager import VersionManager
vm = VersionManager(Path.cwd())
vm.auto_bump(create_tag=True)
```

**Trigger**: Before release, after merge to main, or manually

**Principles**: See `.claude/principles/git-workflow.md`

---"""

    def _get_pr_based_semver_section(self) -> str:
        """Get PR-Based SemVer section"""
        return """## Versioning Strategy

**Strategy**: PR-Based Semantic Versioning (reviewer confirms)

**Workflow**:
1. PR author suggests version bump in PR description
2. Reviewer confirms or adjusts
3. CI/CD auto-bumps on merge

**Manual Bump**:
```bash
python -m claudecodeoptimizer.core.version_manager auto_bump --create-tag
```

**Principles**: See `.claude/principles/git-workflow.md`

---"""

    def _get_manual_semver_section(self) -> str:
        """Get Manual SemVer section"""
        return """## Versioning Strategy

**Strategy**: Manual Semantic Versioning (release managers control)

**Process**:
1. Review commits: `git log $(git describe --tags --abbrev=0)..HEAD`
2. Update version files (pyproject.toml, package.json, etc.)
3. Create tag: `git tag -a v1.3.0 -m "Release 1.3.0"`

**Helper Tool**:
```bash
python -m claudecodeoptimizer.core.version_manager auto_bump --dry-run
```

**Principles**: See `.claude/principles/git-workflow.md`

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

    def _inject_principles(self, content: str) -> str:
        """
        Inject selected principles into CLAUDE.md.

        Replaces content between <!-- CCO_PRINCIPLES_START --> and <!-- CCO_PRINCIPLES_END --> markers
        with formatted list of selected principles.
        """
        # Load selected principle IDs
        selected_ids = self.preferences.get("selected_principle_ids", [])
        if not selected_ids:
            # No principles selected
            return content

        # Load all principles
        from .principle_md_loader import load_all_principles

        if not self.principles_dir.exists():
            return content

        principles_list = load_all_principles(self.principles_dir)
        all_principles = {p["id"]: p for p in principles_list}

        # Group selected principles by category
        categories: Dict[str, List[Dict[str, Any]]] = {}
        for pid in selected_ids:
            principle = all_principles.get(pid)
            if not principle:
                continue

            category = principle.get("category", "other")
            if category not in categories:
                categories[category] = []

            categories[category].append(principle)

        # Build principles section
        principles_content = []

        # Get ALL universal principles
        universal_principles = [p for p in principles_list if p.get("category") == "universal"]

        if universal_principles:
            principles_content.append("**Universal Principles** (apply to all projects):\n")
            for principle in universal_principles:
                principles_content.append(
                    f"- **{principle['id']}**: {principle['title']} → `.claude/principles/{principle['id']}.md`\n"
                )

        # Add project-specific principles by category
        category_names = {
            "code_quality": "Code Quality",
            "architecture": "Architecture",
            "security_privacy": "Security & Privacy",
            "testing": "Testing",
            "git_workflow": "Git Workflow",
            "performance": "Performance",
            "operations": "Operations",
            "api_design": "API Design",
            "claude-guidelines": "Claude Guidelines",
        }

        # List categories with individual principle links
        has_project_specific = False
        for cat_id, cat_name in category_names.items():
            cat_principles_raw = categories.get(cat_id, [])
            cat_principles = [
                p
                for p in cat_principles_raw
                if isinstance(p, dict) and p.get("category") != "universal"
            ]
            if cat_principles:
                if not has_project_specific:
                    principles_content.append("\n**Project-Specific Principles:**\n")
                    has_project_specific = True
                principles_content.append(f"\n*{cat_name}:*\n")
                for p in sorted(cat_principles, key=lambda x: str(x.get("id", ""))):
                    principles_content.append(
                        f"- **{p['id']}**: {p['title']} → `.claude/principles/{p['id']}.md`\n"
                    )

        # Note: Total counts maintained in README.md only (avoid hardcoding in generated files)

        # Replace content between markers or append to end
        start_marker = "<!-- CCO_PRINCIPLES_START -->"
        end_marker = "<!-- CCO_PRINCIPLES_END -->"

        start_idx = content.find(start_marker)
        end_idx = content.find(end_marker)

        if start_idx != -1 and end_idx != -1:
            # Markers exist - inject between them
            before = content[: start_idx + len(start_marker)]
            after = content[end_idx:]
            injected = "\n" + "".join(principles_content)
            content = before + injected + after
        else:
            # Markers don't exist - append to end of file
            section = f"\n\n## Development Principles\n\n{start_marker}\n"
            section += "".join(principles_content)
            section += end_marker + "\n"
            content = content.rstrip() + section

        return content

    def _inject_skills(self, content: str) -> str:
        """
        Inject selected skills into CLAUDE.md.

        Replaces content between <!-- CCO_SKILLS_START --> and <!-- CCO_SKILLS_END --> markers
        with formatted list of selected skills.
        """
        if not self.selected_skills:
            # No skills selected
            return content

        # Build skills section - single unified list
        skills_content = []

        # Sort all skills alphabetically by display name
        for skill in sorted(self.selected_skills):
            # Format display name
            if "/" in skill:
                # Language-specific: python/async-patterns → Async Patterns (Python)
                lang, skill_name = skill.split("/", 1)
                display_name = f"{skill_name.replace('-', ' ').title()} ({lang.title()})"
            else:
                # Universal: root-cause-analysis → Root Cause Analysis
                display_name = skill.replace("-", " ").title()

            skills_content.append(f"- **{display_name}** → `.claude/skills/{skill}.md`\n")

        # Replace content between markers or append to end
        start_marker = "<!-- CCO_SKILLS_START -->"
        end_marker = "<!-- CCO_SKILLS_END -->"

        start_idx = content.find(start_marker)
        end_idx = content.find(end_marker)

        if start_idx != -1 and end_idx != -1:
            # Markers exist - inject between them
            before = content[: start_idx + len(start_marker)]
            after = content[end_idx:]
            injected = "\n" + "".join(skills_content)
            content = before + injected + after
        else:
            # Markers don't exist - append to end of file
            section = f"\n\n## Available Skills\n\n{start_marker}\n"
            section += "".join(skills_content)
            section += end_marker + "\n"
            content = content.rstrip() + section

        return content

    def _inject_agents(self, content: str) -> str:
        """
        Inject selected agents into CLAUDE.md.

        Replaces content between <!-- CCO_AGENTS_START --> and <!-- CCO_AGENTS_END --> markers
        with formatted list of selected agents.
        """
        if not self.selected_agents:
            # No agents selected
            return content

        # Build agents section - single unified list
        agents_content = []

        for agent in sorted(self.selected_agents):
            agent_name = agent.replace("-", " ").title()
            agents_content.append(f"- **{agent_name}** → `.claude/agents/{agent}.md`\n")

        # Replace content between markers or append to end
        start_marker = "<!-- CCO_AGENTS_START -->"
        end_marker = "<!-- CCO_AGENTS_END -->"

        start_idx = content.find(start_marker)
        end_idx = content.find(end_marker)

        if start_idx != -1 and end_idx != -1:
            # Markers exist - inject between them
            before = content[: start_idx + len(start_marker)]
            after = content[end_idx:]
            injected = "\n" + "".join(agents_content)
            content = before + injected + after
        else:
            # Markers don't exist - append to end of file
            section = f"\n\n## Available Agents\n\n{start_marker}\n"
            section += "".join(agents_content)
            section += end_marker + "\n"
            content = content.rstrip() + section

        return content

    def _inject_claude_guidelines(self, content: str) -> str:
        """
        Inject Claude-specific guidelines into CLAUDE.md.

        Replaces content between <!-- CCO_CLAUDE_START --> and <!-- CCO_CLAUDE_END --> markers
        with all Claude principles (C_*).
        """
        # Load Claude principles (C_*)
        from .principle_md_loader import load_all_principles

        if not self.principles_dir.exists():
            return content

        principles_list = load_all_principles(self.principles_dir)
        claude_principles = [p for p in principles_list if p["id"].startswith("C")]

        if not claude_principles:
            return content

        # Build Claude guidelines section
        guidelines_content = []
        for principle in sorted(claude_principles, key=lambda x: x["id"]):
            guidelines_content.append(
                f"- **{principle['id']}**: {principle['title']} → `.claude/principles/{principle['id']}.md`\n"
            )

        # Check if markers exist
        start_marker = "<!-- CCO_CLAUDE_START -->"
        end_marker = "<!-- CCO_CLAUDE_END -->"
        start_idx = content.find(start_marker)
        end_idx = content.find(end_marker)

        if start_idx != -1 and end_idx != -1:
            # Markers exist - inject between them
            before = content[: start_idx + len(start_marker)]
            after = content[end_idx:]
            injected = "\n" + "".join(guidelines_content)
            content = before + injected + after
        else:
            # Markers don't exist - append to end of file
            section = f"\n\n## Claude Guidelines\n\n{start_marker}\n"
            section += "".join(guidelines_content)
            section += end_marker + "\n"
            content = content.rstrip() + section

        return content

    def _get_pref(self, path: str, default: Any = None) -> Any:  # noqa: ANN401
        """Get nested preference value"""
        parts = path.split(".")
        current: Any = self.preferences

        for part in parts:
            if isinstance(current, dict):
                current = current.get(part)
            elif hasattr(current, part):
                current = getattr(current, part)
            else:
                return default

            if current is None:
                return default

        return current if current is not None else default


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

"""
Dynamic Skill Selection - CCO 3.0

Selects applicable skills based on user preferences.
Copies skills to .claude/skills/ for @mention usage.
"""

import shutil
from pathlib import Path
from typing import Any, Dict, List


class SkillSelector:
    """
    Select applicable skills based on user preferences.

    Skills are specialized Claude Code agents that handle specific workflows:
    - verification-protocol: Incremental fix-verify-commit loop
    - test-first-verification: Generate tests before code changes
    - root-cause-analysis: Analyze WHY violations exist
    - incremental-improvement: Break large tasks into milestones
    - security-emergency-response: Immediate P0 security fixes

    Generates .claude/skills/ directory with selected skills.
    """

    # All available skills with their metadata
    AVAILABLE_SKILLS = {
        "verification-protocol": {
            "name": "verification-protocol",
            "file": "verification-protocol.md",
            "description": "Enforces fix → verify → commit loop for principle violations",
            "category": "enforcement",
            "applies_to": ["audit-principles", "audit-security", "audit-tests", "fix-code"],
            "applicability": {
                "project_types": ["all"],
                "preference_conditions": [],
            },
        },
        "test-first-verification": {
            "name": "test-first-verification",
            "file": "test-first-verification.md",
            "description": "Generate characterization tests BEFORE applying code changes",
            "category": "enforcement",
            "applies_to": ["fix-code", "refactor-duplicates", "cleanup-dead-code"],
            "applicability": {
                "project_types": ["all"],
                "preference_conditions": [
                    {
                        "path": "testing.strategy",
                        "operator": "in",
                        "values": ["tdd", "test-first", "comprehensive", "balanced"],
                    },
                ],
            },
        },
        "root-cause-analysis": {
            "name": "root-cause-analysis",
            "file": "root-cause-analysis.md",
            "description": "Analyze WHY violations exist, not just WHERE they are",
            "category": "analysis",
            "applies_to": ["audit-principles", "audit-security", "audit-tests", "analyze"],
            "applicability": {
                "project_types": ["all"],
                "preference_conditions": [
                    {
                        "path": "code_quality.linting_strictness",
                        "operator": "in",
                        "values": ["strict", "pedantic", "paranoid", "standard"],
                    },
                ],
            },
        },
        "incremental-improvement": {
            "name": "incremental-improvement",
            "file": "incremental-improvement.md",
            "description": "Break overwhelming tasks into achievable milestones",
            "category": "planning",
            "applies_to": ["audit-tests", "generate-tests", "audit-principles"],
            "applicability": {
                "project_types": ["all"],
                "preference_conditions": [
                    {
                        "path": "project_identity.maturity",
                        "operator": "in",
                        "values": [
                            "greenfield",
                            "alpha",
                            "beta",
                            "active-dev",
                            "production",
                            "stable",
                        ],
                    },
                ],
            },
        },
        "security-emergency-response": {
            "name": "security-emergency-response",
            "file": "security-emergency-response.md",
            "description": "Immediate remediation for P0 CRITICAL security violations",
            "category": "security",
            "applies_to": ["audit-security", "scan-secrets"],
            "applicability": {
                "project_types": ["all"],
                "preference_conditions": [
                    {
                        "path": "security.security_stance",
                        "operator": "in",
                        "values": ["strict", "very-strict", "paranoid", "zero-trust", "standard"],
                    },
                ],
            },
        },
    }

    def __init__(self, preferences: Dict[str, Any]) -> None:
        """
        Initialize selector with user preferences.

        Args:
            preferences: User preferences dictionary from CCOPreferences.dict()
        """
        self.preferences = preferences
        self.skills_source_dir = Path(__file__).parent.parent / "skills"

    def select_applicable(self) -> List[Dict]:
        """
        Select skills that apply to this project.

        Returns:
            List of applicable skill dictionaries
        """
        applicable = []

        for _skill_id, skill in self.AVAILABLE_SKILLS.items():
            if self._is_applicable(skill):
                applicable.append(skill)

        return applicable

    def _is_applicable(self, skill: Dict) -> bool:
        """
        Check if a skill applies to this project.

        Evaluates:
        - Project type matching
        - Preference conditions

        Returns:
            True if skill should be included
        """
        applicability = skill.get("applicability", {})

        # Check project types (all skills apply to all types)
        project_types = applicability.get("project_types", [])
        if "all" not in project_types:
            # Currently all skills support all project types
            pass

        # Check preference-based conditions
        conditions = applicability.get("preference_conditions", [])
        for condition in conditions:
            if not self._evaluate_condition(condition):
                return False

        return True

    def _evaluate_condition(self, condition: Dict) -> bool:
        """
        Evaluate a single preference condition.

        Condition format:
        {
            "path": "testing.strategy",
            "operator": "in",
            "values": ["tdd", "test-first"]
        }
        """
        path = condition.get("path", "")
        operator = condition.get("operator", "in")
        values = condition.get("values", [])

        # Get preference value
        pref_value = self._get_nested_value(self.preferences, path)
        if pref_value is None:
            return False

        # Evaluate operator
        if operator == "in":
            return pref_value in values
        elif operator == "not_in":
            return pref_value not in values
        elif operator == "contains_any":
            if isinstance(pref_value, list):
                return any(v in values for v in pref_value)
            return pref_value in values

        return True

    def _get_nested_value(self, obj: Any, path: str) -> Any:
        """
        Get value from nested path.

        Example: "testing.strategy"
        """
        if not path:
            return None

        parts = path.split(".")
        current = obj

        for part in parts:
            if isinstance(current, dict):
                current = current.get(part)
            elif hasattr(current, part):
                current = getattr(current, part)
            else:
                return None

            if current is None:
                return None

        return current

    def copy_skills_to_project(self, project_path: Path) -> Dict[str, Any]:
        """
        Copy selected skills to .claude/skills/ directory.

        Args:
            project_path: Path to project root

        Returns:
            Dictionary with copy results
        """
        applicable = self.select_applicable()
        skills_dest_dir = project_path / ".claude" / "skills"

        # Create skills directory
        skills_dest_dir.mkdir(parents=True, exist_ok=True)

        copied = []
        skipped = []

        for skill in applicable:
            source_file = self.skills_source_dir / skill["file"]
            dest_file = skills_dest_dir / skill["file"]

            if source_file.exists():
                try:
                    shutil.copy2(source_file, dest_file)
                    copied.append(
                        {
                            "name": skill["name"],
                            "file": skill["file"],
                            "description": skill["description"],
                            "applies_to": skill["applies_to"],
                        },
                    )
                except Exception as e:
                    skipped.append(
                        {
                            "name": skill["name"],
                            "error": str(e),
                        },
                    )

        return {
            "success": True,
            "skills_dir": str(skills_dest_dir),
            "copied": copied,
            "skipped": skipped,
            "total_applicable": len(applicable),
            "total_copied": len(copied),
        }

    def generate_skills_summary(self) -> str:
        """
        Generate markdown summary of selected skills.

        Returns:
            Markdown string with skills summary
        """
        applicable = self.select_applicable()

        lines = []
        lines.append("# Available Skills")
        lines.append("")
        lines.append(f"**Total Skills:** {len(applicable)}/{len(self.AVAILABLE_SKILLS)}")
        lines.append("")
        lines.append("---")
        lines.append("")

        for skill in applicable:
            lines.append(f"## {skill['name']}")
            lines.append("")
            lines.append(f"**Description:** {skill['description']}")
            lines.append(f"**Category:** {skill['category']}")
            lines.append(f"**Applies to:** {', '.join(skill['applies_to'])}")
            lines.append("")
            lines.append("**Usage:**")
            lines.append("```")
            lines.append("Use Skill tool:")
            lines.append(f'Skill("{skill["name"]}")')
            lines.append("```")
            lines.append("")
            lines.append("---")
            lines.append("")

        lines.append("")
        lines.append("## How to Use Skills")
        lines.append("")
        lines.append("Skills are invoked by commands when specific conditions are met:")
        lines.append("")
        lines.append("- **verification-protocol**: Auto-activates when violations detected")
        lines.append("- **test-first-verification**: Auto-activates before code changes")
        lines.append("- **root-cause-analysis**: Auto-activates for 3+ similar violations")
        lines.append("- **incremental-improvement**: Auto-activates for 20+ items to fix")
        lines.append("- **security-emergency-response**: Auto-activates for P0 CRITICAL issues")
        lines.append("")
        lines.append("You can also manually invoke skills:")
        lines.append("```")
        lines.append("Use Skill tool:")
        lines.append('Skill("skill-name")')
        lines.append("```")
        lines.append("")

        return "\n".join(lines)

    def get_skill_stats(self) -> Dict[str, Any]:
        """Generate statistics about skill selection"""
        applicable = self.select_applicable()
        all_skills = self.AVAILABLE_SKILLS

        # Count by category
        by_category = {}
        for skill in applicable:
            cat = skill.get("category", "unknown")
            by_category[cat] = by_category.get(cat, 0) + 1

        return {
            "total_available": len(all_skills),
            "applicable_count": len(applicable),
            "skipped_count": len(all_skills) - len(applicable),
            "by_category": by_category,
            "coverage_percentage": round(len(applicable) / len(all_skills) * 100, 1),
        }


# Utility function for easy access
def copy_skills_from_preferences(
    preferences: Dict[str, Any],
    project_path: Path,
) -> Dict[str, Any]:
    """
    Convenience function to copy skills.

    Args:
        preferences: User preferences dictionary
        project_path: Path to project root

    Returns:
        Copy result with stats
    """
    selector = SkillSelector(preferences)
    return selector.copy_skills_to_project(project_path)


__all__ = [
    "SkillSelector",
    "copy_skills_from_preferences",
]

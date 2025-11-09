"""
Dynamic Principle Selection - CCO 3.0

Selects applicable development principles based on user preferences.
Generates PRINCIPLES.md for @mention in Claude Code.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from .constants import MIN_COVERAGE_PERCENTAGE, TOP_ITEMS_DISPLAY


class PrincipleSelector:
    """
    Select applicable principles based on user preferences.

    Reads 52 principles from knowledge base, filters based on:
    - User preferences (team size, security stance, etc.)
    - Project type and language
    - Compliance requirements

    Generates PRINCIPLES.md for Claude Code @mention.
    """

    def __init__(self, preferences: Dict[str, Any]) -> None:
        """
        Initialize selector with user preferences.

        Args:
            preferences: User preferences dictionary from CCOPreferences.dict()
        """
        self.preferences = preferences
        self.all_principles = self._load_principles()

    def _load_principles(self) -> List[Dict[str, Any]]:
        """Load all principles from knowledge base"""
        principles_path = Path(__file__).parent.parent / "knowledge" / "principles.json"

        with open(principles_path, encoding="utf-8") as f:
            data = json.load(f)

        principles = data.get("principles", [])

        # Deduplicate by ID (defense mechanism)
        seen_ids = set()
        deduplicated = []

        for principle in principles:
            pid = principle.get("id")
            if pid not in seen_ids:
                seen_ids.add(pid)
                deduplicated.append(principle)

        return deduplicated

    def select_applicable(self) -> List[Dict[str, Any]]:
        """
        Select principles that apply to this project.

        Returns:
            List of applicable principle dictionaries, sorted by severity
        """
        applicable = []

        for principle in self.all_principles:
            if self._is_applicable(principle):
                # Add enforcement level based on preferences
                principle = self._add_enforcement_level(principle)
                applicable.append(principle)

        return self._sort_by_priority(applicable)

    def _is_applicable(self, principle: Dict[str, Any]) -> bool:
        """
        Check if a principle applies to this project.

        Evaluates:
        - User-selected principle IDs (if provided)
        - Severity vs linting strictness
        - Category vs project characteristics
        - Project type matching
        - Language compatibility
        - Preference conditions
        - Team size requirements

        Returns:
            True if principle should be enforced
        """
        # If user has pre-selected specific principles, only use those
        selected_ids = self.preferences.get("selected_principle_ids", [])
        if selected_ids:
            return principle.get("id") in selected_ids

        # Check severity vs linting strictness
        if not self._check_severity_match(principle):
            return False

        # Check category relevance
        if not self._check_category_relevance(principle):
            return False

        applicability = principle.get("applicability", {})

        # Always applicable principles
        if applicability.get("project_types") == ["all"]:
            # Still check preference conditions
            pass

        # Check preference-based conditions
        conditions = applicability.get("preference_conditions", [])
        for condition in conditions:
            if not self._evaluate_condition(condition):
                return False

        # Check team size exclusions
        if not self._check_team_size(principle):
            return False

        # Check security stance requirements
        if not self._check_security_stance(principle):
            return False

        return True

    def _evaluate_condition(self, condition: Dict[str, Any]) -> bool:
        """
        Evaluate a single preference condition.

        Condition format:
        {
            "path": "code_quality.linting_strictness",
            "operator": "in",
            "values": ["strict", "pedantic"]
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
        elif operator == ">=":
            try:
                # Handle percentage strings like "90"
                pref_int = int(str(pref_value).replace("%", ""))
                threshold = int(str(values[0]).replace("%", ""))
                return pref_int >= threshold
            except (ValueError, TypeError):
                return False
        elif operator == "<=":
            try:
                pref_int = int(str(pref_value).replace("%", ""))
                threshold = int(str(values[0]).replace("%", ""))
                return pref_int <= threshold
            except (ValueError, TypeError):
                return False

        return True

    def _get_nested_value(self, obj: Any, path: str) -> Any:
        """
        Get value from nested path.

        Example: "code_quality.linting_strictness"
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

    def _check_team_size(self, principle: Dict[str, Any]) -> bool:
        """Check if principle applies to current team size"""
        # Get team size from preferences
        team_size = self._get_nested_value(self.preferences, "project_identity.team_trajectory")

        # Some principles don't apply to solo devs
        team_only_ids = ["P015", "P016", "P017", "P018"]  # Code review, PR guidelines, etc.
        if principle["id"] in team_only_ids and team_size == "solo":
            return False

        return True

    def _check_security_stance(self, principle: Dict[str, Any]) -> bool:
        """Check if principle applies based on security stance"""
        category = principle.get("category", "")
        if category != "security_privacy":
            return True  # Non-security principles always apply

        # Get security stance
        stance = self._get_nested_value(self.preferences, "security.security_stance")

        # High security principles require strict stance
        high_security_ids = ["P036", "P037", "P038", "P039"]
        if principle["id"] in high_security_ids:
            return stance in ["zero-trust", "paranoid", "very-strict", "strict"]

        return True

    def _check_severity_match(self, principle: Dict[str, Any]) -> bool:
        """
        Check if principle importance matches linting strictness.

        Uses weight (5-10) and severity to determine if principle applies.
        Weight represents principle importance across all contexts.

        Filters based on strictness:
        - paranoid/pedantic: All principles (weight >= 5)
        - strict: Core + important (weight >= 8) → ~27 principles
        - standard: Essential (weight >= 9) → ~14 principles
        - moderate/relaxed: Critical only (weight >= 10) → ~7 principles
        """
        weight = principle.get("weight", 5)
        strictness = self._get_nested_value(self.preferences, "code_quality.linting_strictness")

        # Map strictness to minimum weight threshold
        weight_thresholds = {
            "paranoid": 5,  # All principles (53)
            "pedantic": 6,  # Most principles (50)
            "strict": 8,  # Core + important (~27)
            "standard": 9,  # Essential (~14)
            "moderate": 10,  # Critical only (~7)
            "relaxed": 10,  # Critical only (~7)
        }

        min_weight = weight_thresholds.get(strictness, 9)
        return weight >= min_weight

    def _check_category_relevance(self, principle: Dict[str, Any]) -> bool:
        """
        Check if principle category is relevant to project characteristics.

        Filters based on:
        - Team size (solo vs team)
        - Project maturity (prototype vs production)
        - Security stance
        """
        category = principle.get("category", "")

        # Git workflow principles - less relevant for solo devs
        if category == "git_workflow":
            team_size = self._get_nested_value(self.preferences, "project_identity.team_trajectory")
            if team_size == "solo":
                # Only keep essential git principles for solo
                return principle["id"] in ["P047"]  # Keep commit messages principle

        # Operations principles - less relevant for early stage
        if category == "operations":
            maturity = self._get_nested_value(self.preferences, "project_identity.project_maturity")
            if maturity in ["prototype", "mvp"]:
                # Only keep critical operations principles
                severity = principle.get("severity", "low")
                return severity == "critical"

        # Architecture principles - some only relevant for larger teams
        if category == "architecture":
            team_size = self._get_nested_value(self.preferences, "project_identity.team_trajectory")
            if team_size == "solo":
                # Exclude complex architecture patterns for solo
                exclude_for_solo = ["P015", "P016", "P017", "P018", "P019", "P020"]
                if principle["id"] in exclude_for_solo:
                    return False

        return True

    def _add_enforcement_level(self, principle: Dict[str, Any]) -> Dict[str, Any]:
        """Add enforcement level based on preferences"""
        principle = principle.copy()

        # Get linting strictness
        strictness = self._get_nested_value(self.preferences, "code_quality.linting_strictness")

        # Map to enforcement level
        enforcement_map = {
            "paranoid": "MUST - No exceptions",
            "pedantic": "MUST - No exceptions",
            "strict": "SHOULD - Requires justification",
            "standard": "SHOULD - Use best judgment",
            "moderate": "RECOMMENDED - Optional",
            "relaxed": "OPTIONAL",
        }

        principle["enforcement"] = enforcement_map.get(strictness, "RECOMMENDED")

        return principle

    def _sort_by_priority(self, principles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Sort principles by severity and ID"""
        severity_order = {
            "critical": 0,
            "high": 1,
            "medium": 2,
            "low": 3,
        }

        return sorted(
            principles,
            key=lambda p: (
                severity_order.get(p.get("severity", "low"), 4),
                p.get("id", ""),
            ),
        )

    def get_skipped_principles(self) -> List[Dict[str, Any]]:
        """Get list of principles that don't apply"""
        applicable_ids = {p["id"] for p in self.select_applicable()}
        all_ids = {p["id"] for p in self.all_principles}
        skipped_ids = all_ids - applicable_ids

        skipped = []
        for principle in self.all_principles:
            if principle["id"] in skipped_ids:
                # Add reason for skipping
                principle = principle.copy()
                principle["skip_reason"] = self._get_skip_reason(principle)
                skipped.append(principle)

        return sorted(skipped, key=lambda p: p["id"])

    def _get_skip_reason(self, principle: Dict[str, Any]) -> str:
        """Determine why a principle was skipped"""
        # Check team size
        team_size = self._get_nested_value(self.preferences, "project_identity.team_trajectory")
        if principle["id"] in ["P015", "P016", "P017", "P018"] and team_size == "solo":
            return f"Solo developer (team_trajectory = '{team_size}')"

        # Check security stance
        stance = self._get_nested_value(self.preferences, "security.security_stance")
        if principle.get("category") == "security_privacy":
            if principle["id"] in ["P036", "P037", "P038", "P039"]:
                if stance not in ["zero-trust", "paranoid", "very-strict", "strict"]:
                    return f"Security stance too permissive (security_stance = '{stance}')"

        # Check testing coverage
        coverage = self._get_nested_value(self.preferences, "testing.coverage_target")
        if principle["id"] in ["P035"]:  # Mutation testing
            try:
                cov_int = int(str(coverage).replace("%", ""))
                if cov_int < MIN_COVERAGE_PERCENTAGE:
                    return f"Coverage target too low (coverage_target = '{coverage}%')"
            except (ValueError, TypeError):
                pass

        # Check linting strictness
        strictness = self._get_nested_value(self.preferences, "code_quality.linting_strictness")
        if strictness in ["disabled", "relaxed"]:
            if principle.get("severity") in ["high", "critical"]:
                return f"Linting too relaxed (linting_strictness = '{strictness}')"

        return "Does not match project preferences"

    def generate_statistics(self) -> Dict[str, Any]:
        """Generate statistics about principle selection"""
        applicable = self.select_applicable()

        # Count by severity
        by_severity = {
            "critical": len([p for p in applicable if p.get("severity") == "critical"]),
            "high": len([p for p in applicable if p.get("severity") == "high"]),
            "medium": len([p for p in applicable if p.get("severity") == "medium"]),
            "low": len([p for p in applicable if p.get("severity") == "low"]),
        }

        # Count by category
        by_category = {}
        for p in applicable:
            cat = p.get("category", "unknown")
            by_category[cat] = by_category.get(cat, 0) + 1

        return {
            "total_principles": len(self.all_principles),
            "applicable_count": len(applicable),
            "skipped_count": len(self.all_principles) - len(applicable),
            "by_severity": by_severity,
            "by_category": by_category,
            "coverage_percentage": round(len(applicable) / len(self.all_principles) * 100, 1),
        }

    def generate_principles_md(self, output_path: Path) -> Dict[str, Any]:
        """
        Generate PRINCIPLES.md file.

        Args:
            output_path: Path to write PRINCIPLES.md

        Returns:
            Dictionary with generation stats
        """
        applicable = self.select_applicable()
        skipped = self.get_skipped_principles()
        stats = self.generate_statistics()

        # Group by severity
        by_severity = {
            "critical": [p for p in applicable if p.get("severity") == "critical"],
            "high": [p for p in applicable if p.get("severity") == "high"],
            "medium": [p for p in applicable if p.get("severity") == "medium"],
            "low": [p for p in applicable if p.get("severity") == "low"],
        }

        # Generate content
        content = self._render_principles_md(by_severity, skipped, stats)

        # Write file
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(content, encoding="utf-8")

        return {
            "success": True,
            "principles_file": str(output_path),
            "applicable_count": len(applicable),
            "total_count": len(self.all_principles),
            "stats": stats,
        }

    def _render_principles_md(
        self,
        by_severity: Dict[str, List[Dict[str, Any]]],
        skipped: List[Dict[str, Any]],
        stats: Dict[str, Any],
    ) -> str:
        """Render PRINCIPLES.md content"""
        project_name = (
            self._get_nested_value(self.preferences, "project_identity.name") or "Unknown Project"
        )

        lines = []

        # Header
        lines.append(f"# Development Principles for {project_name}")
        lines.append("")
        lines.append(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(
            f"**Applicable Principles:** {stats['applicable_count']}/{stats['total_principles']}",
        )
        lines.append(f"**Coverage:** {stats['coverage_percentage']}%")
        lines.append("")
        lines.append("---")
        lines.append("")

        # Configuration
        lines.append("## Your Configuration")
        lines.append("")
        team = self._get_nested_value(self.preferences, "project_identity.team_trajectory")
        quality = self._get_nested_value(self.preferences, "code_quality.linting_strictness")
        security = self._get_nested_value(self.preferences, "security.security_stance")
        coverage = self._get_nested_value(self.preferences, "testing.coverage_target")
        compliance = self._get_nested_value(
            self.preferences,
            "project_identity.compliance_requirements",
        )

        lines.append(f"- **Team Size:** {team}")
        lines.append(f"- **Code Quality:** {quality}")
        lines.append(f"- **Security Stance:** {security}")
        lines.append(f"- **Test Coverage Target:** {coverage}")
        lines.append(f"- **Compliance:** {', '.join(compliance) if compliance else 'None'}")
        lines.append("")
        lines.append("---")
        lines.append("")

        # Statistics
        lines.append("## Statistics")
        lines.append("")
        lines.append(f"- **Critical:** {stats['by_severity']['critical']} principles")
        lines.append(f"- **High:** {stats['by_severity']['high']} principles")
        lines.append(f"- **Medium:** {stats['by_severity']['medium']} principles")
        lines.append(f"- **Low:** {stats['by_severity']['low']} principles")
        lines.append("")
        lines.append("---")
        lines.append("")

        # Principles by severity
        severity_labels = {
            "critical": ("CRITICAL", "⚠️"),
            "high": ("HIGH PRIORITY", "🔴"),
            "medium": ("MEDIUM PRIORITY", "🟡"),
            "low": ("LOW PRIORITY", "🟢"),
        }

        for severity_key in ["critical", "high", "medium", "low"]:
            principles = by_severity.get(severity_key, [])
            if not principles:
                continue

            label, emoji = severity_labels[severity_key]
            lines.append(f"## {label} Principles {emoji}")
            lines.append("")

            for p in principles:
                lines.append(f"### {p['id']}: {p['title']}")
                lines.append("")
                lines.append(f"**Enforcement:** {p.get('enforcement', 'RECOMMENDED')}")
                lines.append(
                    f"**Category:** {p.get('category', 'unknown').replace('_', ' ').title()}",
                )
                lines.append("")
                lines.append(p.get("description", "No description"))
                lines.append("")

                # Rules
                rules = p.get("rules", [])
                if rules:
                    lines.append("**Check Patterns:**")
                    for rule in rules[
                        : TOP_ITEMS_DISPLAY["project_types"]
                    ]:  # Limit to TOP_ITEMS_DISPLAY
                        langs = ", ".join(rule.get("languages", []))
                        lines.append(f"- {rule.get('description', '')} ({langs})")
                        if "check_pattern" in rule:
                            lines.append(f"  - Pattern: `{rule['check_pattern']}`")
                    lines.append("")

                # Examples
                examples = p.get("examples", {})
                if examples:
                    if "bad" in examples and examples["bad"]:
                        lines.append("**❌ Bad Example:**")
                        lines.append("```")
                        lines.append(examples["bad"][0])
                        lines.append("```")
                        lines.append("")

                    if "good" in examples and examples["good"]:
                        lines.append("**✅ Good Example:**")
                        lines.append("```")
                        lines.append(examples["good"][0])
                        lines.append("```")
                        lines.append("")

                lines.append("---")
                lines.append("")

        # Skipped principles
        if skipped:
            lines.append("## Skipped Principles")
            lines.append("")
            lines.append("The following principles **do not apply** to your project:")
            lines.append("")

            for p in skipped[: TOP_ITEMS_DISPLAY["principles"]]:  # Limit to TOP_ITEMS_DISPLAY
                reason = p.get("skip_reason", "Does not match preferences")
                lines.append(f"- ❌ **{p['id']}: {p['title']}**")
                lines.append(f"  - Reason: {reason}")
                lines.append("")

            lines.append("---")
            lines.append("")

        # Usage guide
        lines.append("## Using These Principles")
        lines.append("")
        lines.append("### In Claude Code")
        lines.append("")
        lines.append("Reference this file in any conversation:")
        lines.append("```")
        lines.append("@PRINCIPLES.md Check if this code follows our principles")
        lines.append("```")
        lines.append("")
        lines.append("### In Commands")
        lines.append("")
        lines.append("All CCO commands use these principles:")
        lines.append("- `/cco-audit-code` - Check critical code quality principles")
        lines.append("- `/cco-audit-principles` - Check all applicable principles")
        lines.append("- `/cco-fix-code` - Auto-fix violations")
        lines.append("")
        lines.append("### Updating Principles")
        lines.append("")
        lines.append("To update your principles:")
        lines.append("1. Change preferences: Edit `~/.cco/projects/{project}.json`")
        lines.append("2. Regenerate: `/cco-generate-principles`")
        lines.append("3. Review: `git diff .claude/PRINCIPLES.md`")
        lines.append("")
        lines.append("---")
        lines.append("")

        # Footer
        lines.append("*Auto-generated by ClaudeCodeOptimizer v{cco_version}*")
        lines.append(f"*Principle Database: {stats['total_principles']} total principles*")
        lines.append("*Reference with: @PRINCIPLES.md*")

        return "\n".join(lines)


# Utility function for easy access
def generate_principles_from_preferences(
    preferences: Dict[str, Any],
    output_path: Path,
) -> Dict[str, Any]:
    """
    Convenience function to generate PRINCIPLES.md.

    Args:
        preferences: User preferences dictionary
        output_path: Path to write PRINCIPLES.md

    Returns:
        Generation result with stats
    """
    selector = PrincipleSelector(preferences)
    return selector.generate_principles_md(output_path)

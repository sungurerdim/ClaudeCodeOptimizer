"""
Universal Command Recommender - CCO 2.5

Rule-based command selection system.
100% generic - works for any project without hardcoding.
"""

import sys
from pathlib import Path
from typing import Dict, List, Tuple

sys.path.insert(0, str(Path(__file__).parent.parent))

from ..core.constants import TOP_ITEMS_DISPLAY
from ..schemas.commands import CommandRegistry
from ..schemas.preferences import CCOPreferences


class CommandRecommender:
    """
    Universal command recommender - uses rules + project preferences

    Zero hardcoded project assumptions.
    """

    # Core commands - always recommended
    CORE_COMMANDS = ["cco-help", "cco-status", "cco-configure"]

    # Conditional recommendation rules (tag + preference based)
    RECOMMENDATION_RULES = [
        # Testing commands
        {
            "command_id": "cco-audit-tests",
            "conditions": [
                ("testing.coverage_target", "in", ["95", "100"]),
                ("testing.mutation_testing", "!=", "none"),
            ],
            "reasoning": "High test coverage goals require test quality audits",
            "priority": "high",
        },
        {
            "command_id": "cco-generate-tests",
            "conditions": [
                ("testing.coverage_target", ">=", 85),
            ],
            "reasoning": "Auto-generate tests to reach coverage target faster",
            "priority": "medium",
        },
        # Security commands
        {
            "command_id": "cco-audit-security",
            "conditions": [
                ("security.security_stance", "in", ["paranoid", "balanced"]),
            ],
            "reasoning": "Security audits essential for your security posture",
            "priority": "high",
        },
        {
            "command_id": "cco-scan-secrets",
            "conditions": [
                ("security.security_stance", "==", "paranoid"),
            ],
            "reasoning": "Paranoid security requires secret scanning",
            "priority": "critical",
        },
        # Documentation commands
        {
            "command_id": "cco-audit-docs",
            "conditions": [
                ("documentation.verbosity", "in", ["extensive", "concise"]),
            ],
            "reasoning": "Documentation audits ensure quality and completeness",
            "priority": "medium",
        },
        {
            "command_id": "cco-generate-docs",
            "conditions": [
                ("documentation.verbosity", "==", "extensive"),
                ("project_identity.team_trajectory", "in", ["medium-5-10", "large-10plus"]),
            ],
            "reasoning": "Auto-generate documentation for large teams",
            "priority": "low",
        },
        # Code quality commands
        {
            "command_id": "cco-audit-code",
            "conditions": [
                ("code_quality.linting_strictness", "in", ["pedantic", "strict"]),
            ],
            "reasoning": "Code quality audits match your high standards",
            "priority": "high",
        },
        {
            "command_id": "cco-fix-code",
            "conditions": [
                ("code_quality.linting_strictness", "in", ["pedantic", "strict"]),
            ],
            "reasoning": "Auto-fix violations to maintain code quality",
            "priority": "high",
        },
        {
            "command_id": "cco-refactor-duplicates",
            "conditions": [
                ("code_quality.dry_enforcement", "==", "zero-tolerance"),
            ],
            "reasoning": "DRY enforcement requires duplication detection",
            "priority": "medium",
        },
        {
            "command_id": "cco-cleanup-dead-code",
            "conditions": [
                ("code_quality.dry_enforcement", "in", ["zero-tolerance", "pragmatic"]),
                ("project_identity.project_maturity", "in", ["active-dev", "maintenance"]),
            ],
            "reasoning": "Remove dead code to maintain cleanliness",
            "priority": "low",
        },
        # DevOps commands
        {
            "command_id": "cco-setup-cicd",
            "conditions": [
                ("devops.ci_cd_trigger", "!=", "manual"),
            ],
            "reasoning": "Automated CI/CD pipeline generation",
            "priority": "medium",
        },
        {
            "command_id": "cco-setup-docker",
            "conditions": [
                ("devops.infrastructure", "in", ["docker-compose", "kubernetes"]),
            ],
            "reasoning": "Docker configuration for your infrastructure",
            "priority": "medium",
        },
        {
            "command_id": "cco-setup-monitoring",
            "conditions": [
                ("devops.monitoring", "in", ["full-observability", "metrics-logs"]),
            ],
            "reasoning": "Monitoring stack setup for observability",
            "priority": "low",
        },
        # Analysis commands
        {
            "command_id": "cco-analyze-structure",
            "conditions": [
                (
                    "project_identity.team_trajectory",
                    "in",
                    [
                        "medium-5-10",
                        "medium-10-20",
                        "large-20-50",
                        "large-50-100",
                        "xlarge-100-500",
                        "enterprise-500plus",
                    ],
                ),
            ],
            "reasoning": "Structure analysis valuable for growing teams",
            "priority": "low",
        },
        {
            "command_id": "cco-analyze-dependencies",
            "conditions": [
                ("security.dependency_scanning", "!=", "none"),
            ],
            "reasoning": "Dependency analysis for security scanning",
            "priority": "medium",
        },
        # Documentation optimization commands
        {
            "command_id": "cco-optimize-docs",
            "conditions": [
                ("documentation.verbosity", "in", ["extensive", "concise"]),
                ("documentation.inline_documentation", "in", ["every-function", "public-api"]),
            ],
            "reasoning": "Optimize documentation quality and consistency",
            "priority": "medium",
        },
        {
            "command_id": "cco-fix-docs",
            "conditions": [
                ("documentation.verbosity", "!=", "minimal"),
            ],
            "reasoning": "Fix documentation issues and inconsistencies",
            "priority": "low",
        },
        {
            "command_id": "cco-generate-from-specs",
            "conditions": [
                ("documentation.api_documentation", "==", "openapi-spec"),
                ("project_identity.types", "in", [["api"], ["backend"], ["microservice"]]),
            ],
            "reasoning": "Generate code from OpenAPI specifications",
            "priority": "medium",
        },
        {
            "command_id": "cco-sync-spec-to-code",
            "conditions": [
                ("documentation.api_documentation", "==", "openapi-spec"),
            ],
            "reasoning": "Keep OpenAPI specs in sync with code",
            "priority": "medium",
        },
        # Integration test generation
        {
            "command_id": "cco-generate-integration-tests",
            "conditions": [
                (
                    "testing.test_pyramid_ratio",
                    "in",
                    ["60-30-10", "50-40-10", "40-40-20", "30-50-20"],
                ),
            ],
            "reasoning": "Generate integration tests for better coverage",
            "priority": "medium",
        },
        # Security fix command
        {
            "command_id": "cco-fix-security",
            "conditions": [
                (
                    "security.security_stance",
                    "in",
                    ["zero-trust", "paranoid", "very-strict", "strict"],
                ),
            ],
            "reasoning": "Auto-fix security vulnerabilities",
            "priority": "high",
        },
        # Principles management
        {
            "command_id": "cco-generate-principles",
            "conditions": [
                ("code_quality.linting_strictness", "in", ["strict", "pedantic", "paranoid"]),
                (
                    "project_identity.team_trajectory",
                    "in",
                    ["medium-5-10", "medium-10-20", "large-20-50", "large-50-100"],
                ),
            ],
            "reasoning": "Generate development principles for team alignment",
            "priority": "low",
        },
        {
            "command_id": "cco-check-principle",
            "conditions": [
                ("code_quality.linting_strictness", "in", ["strict", "pedantic", "paranoid"]),
            ],
            "reasoning": "Verify code adheres to defined principles",
            "priority": "low",
        },
        {
            "command_id": "cco-audit-principles",
            "conditions": [
                ("code_quality.linting_strictness", "in", ["pedantic", "paranoid"]),
            ],
            "reasoning": "Audit all code against development principles",
            "priority": "low",
        },
        # Self-optimization
        {
            "command_id": "cco-self-optimize",
            "conditions": [
                ("project_identity.project_maturity", "in", ["active-dev", "production", "stable"]),
                ("performance.optimization_priority", "in", ["performance-first", "balanced"]),
            ],
            "reasoning": "Self-optimize CCO configuration based on usage patterns",
            "priority": "low",
        },
        # Implementation verification
        {
            "command_id": "cco-verify-implementation",
            "conditions": [
                ("testing.coverage_target", "in", ["90", "95", "98", "100"]),
                ("code_quality.type_coverage_target", "in", ["90", "95", "98", "100"]),
            ],
            "reasoning": "Verify implementations match specifications",
            "priority": "medium",
        },
    ]

    def __init__(self, preferences: CCOPreferences, registry: CommandRegistry) -> None:
        """
        Initialize recommender

        Args:
            preferences: User's CCO preferences
            registry: Command registry with metadata
        """
        self.preferences = preferences
        self.registry = registry

    def _evaluate_condition(self, condition: Tuple[str, str, any]) -> bool:
        """
        Evaluate a single recommendation condition

        Args:
            condition: Tuple of (preference_path, operator, expected_value)

        Returns:
            True if condition passes
        """
        path, operator, expected = condition

        # Navigate nested preference path
        value = self.preferences
        for part in path.split("."):
            if hasattr(value, part):
                value = getattr(value, part)
            else:
                return False

        # Evaluate operator
        if operator == "==":
            return value == expected
        elif operator == "!=":
            return value != expected
        elif operator == "in":
            return value in expected
        elif operator == ">=":
            try:
                return int(value) >= int(expected)
            except (ValueError, TypeError):
                return False
        elif operator == "<=":
            try:
                return int(value) <= int(expected)
            except (ValueError, TypeError):
                return False

        return False

    def recommend_commands(self) -> Dict[str, List[str]]:
        """
        Generate command recommendations with reasoning

        Returns:
            Dictionary with 'core', 'recommended', 'optional' lists and reasoning
        """
        recommended = {
            "core": self.CORE_COMMANDS.copy(),
            "recommended": [],
            "optional": [],
            "reasoning": {},
        }

        # Track which commands we've evaluated from rules
        evaluated_from_rules = set()

        # Always recommend audit-all
        recommended["recommended"].append("cco-audit-all")
        recommended["reasoning"]["cco-audit-all"] = (
            "Comprehensive health check (always recommended)"
        )

        # Evaluate conditional recommendations
        for rule in self.RECOMMENDATION_RULES:
            command_id = rule["command_id"]
            conditions = rule["conditions"]
            reasoning = rule["reasoning"]
            evaluated_from_rules.add(command_id)

            # Check if all conditions pass
            if all(self._evaluate_condition(cond) for cond in conditions):
                recommended["recommended"].append(command_id)
                recommended["reasoning"][command_id] = reasoning
            else:
                recommended["optional"].append(command_id)

        # Now evaluate ALL commands from registry that weren't in rules
        project_types = self.preferences.project_identity.types
        for cmd in self.registry.commands:
            if cmd.command_id in evaluated_from_rules or cmd.command_id in self.CORE_COMMANDS:
                continue  # Already evaluated

            # Check if command is relevant to project types
            is_relevant = "all" in cmd.applicable_project_types or any(
                pt in cmd.applicable_project_types for pt in project_types
            )

            if is_relevant:
                # Add to optional (can be enabled if user wants)
                recommended["optional"].append(cmd.command_id)
                recommended["reasoning"][cmd.command_id] = (
                    f"{cmd.description_short} (available for {', '.join(cmd.applicable_project_types[: TOP_ITEMS_DISPLAY['project_types']])})"
                )

        # Filter by project type relevance
        recommended = self._filter_by_project_type(recommended)

        # Remove duplicates
        recommended["core"] = list(dict.fromkeys(recommended["core"]))
        recommended["recommended"] = list(dict.fromkeys(recommended["recommended"]))
        recommended["optional"] = list(dict.fromkeys(recommended["optional"]))

        return recommended

    def _filter_by_project_type(self, recommendations: Dict) -> Dict:
        """
        Filter commands by project type relevance

        Args:
            recommendations: Current recommendations

        Returns:
            Filtered recommendations
        """
        project_types = self.preferences.project_identity.types

        filtered_optional = []
        for cmd_id in recommendations["optional"]:
            cmd = self.registry.get_by_id(cmd_id)
            if cmd:
                # Check if command is relevant to project types
                if "all" in cmd.applicable_project_types or any(
                    pt in cmd.applicable_project_types for pt in project_types
                ):
                    filtered_optional.append(cmd_id)

        recommendations["optional"] = filtered_optional
        return recommendations

    def explain_recommendation(self, command_id: str) -> str:
        """
        Generate detailed explanation for why command is recommended

        Args:
            command_id: Command identifier

        Returns:
            Human-readable explanation
        """
        # Find in rules
        for rule in self.RECOMMENDATION_RULES:
            if rule["command_id"] == command_id:
                explanation = [f"**{command_id}** is recommended because:"]
                explanation.append(f"- {rule['reasoning']}")

                # Add condition details
                explanation.append("\nConditions met:")
                for condition in rule["conditions"]:
                    path, op, expected = condition
                    explanation.append(f"  * {path} {op} {expected}")

                return "\n".join(explanation)

        return f"Command {command_id} - see command metadata for details"

    def generate_selection_summary(self) -> Dict:
        """
        Generate comprehensive selection summary with stats

        Returns:
            Dictionary with selection statistics
        """
        recs = self.recommend_commands()

        return {
            "total_available": len(self.registry.commands),
            "core_count": len(recs["core"]),
            "recommended_count": len(recs["recommended"]),
            "optional_count": len(recs["optional"]),
            "total_recommended": len(recs["core"]) + len(recs["recommended"]),
            "recommendation_ratio": (len(recs["core"]) + len(recs["recommended"]))
            / len(self.registry.commands),
            "commands_by_category": self._count_by_category(recs),
        }

    def _count_by_category(self, recommendations: Dict) -> Dict[str, int]:
        """Count commands by category"""
        counts = {}

        all_commands = (
            recommendations["core"] + recommendations["recommended"] + recommendations["optional"]
        )
        for cmd_id in all_commands:
            cmd = self.registry.get_by_id(cmd_id)
            if cmd:
                category = cmd.category
                counts[category] = counts.get(category, 0) + 1

        return counts

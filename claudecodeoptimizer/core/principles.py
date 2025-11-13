"""
Principles management system for ClaudeCodeOptimizer.

Loads and manages the 81 development principles from .md files.
Implements dynamic principle selection based on project characteristics.
"""

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

from .. import config as CCOConfig  # noqa: N812
from .constants import SERVICE_COUNT_THRESHOLD_LARGE, SERVICE_COUNT_THRESHOLD_MEDIUM


@dataclass
class Principle:
    """Represents a single development principle."""

    id: str
    number: int
    title: str
    category: str
    severity: str
    weight: int
    description: str
    applicability: Dict[str, Any]
    rules: List[Dict[str, Any]]
    examples: Dict[str, List[str]]
    autofix: Dict[str, Any]


@dataclass
class ProjectCharacteristics:
    """Project characteristics for principle selection."""

    project_type: str  # api, web, ml, microservices, library, cli, etc.
    primary_language: str  # python, javascript, typescript, go, rust, java, etc.
    team_size: str  # solo, small (2-5), medium (6-20), large (20+)
    services_count: int  # Number of services (for microservices)
    privacy_critical: bool  # Handles PII/sensitive data
    security_critical: bool  # Requires high security
    performance_critical: bool  # Performance is critical
    has_containers: bool  # Uses Docker/K8s
    has_tests: bool  # Has existing test suite
    contexts: List[str]  # api_endpoints, database, web_frontend, etc.


class PrinciplesManager:
    """Manages loading and selection of development principles."""

    def __init__(self, principles_dir: Optional[Path] = None) -> None:
        """
        Initialize principles manager.

        Args:
            principles_dir: Path to principles directory (default: content/principles/ from package)
        """
        if principles_dir is None:
            # Load from package content/ directory
            package_dir = Path(__file__).parent.parent
            principles_dir = package_dir.parent / "content" / "principles"

        self.principles_dir = principles_dir
        self.principles: Dict[str, Principle] = {}
        self.categories: List[Dict[str, Any]] = []
        self.selection_strategies: Dict[str, Any] = {}
        self.version: str = "2.0"  # Hardcoded version for now

        if self.principles_dir.exists():
            self._load_principles()

    def _load_principles(self) -> None:
        """Load principles from .md files."""
        try:
            from .principle_md_loader import load_all_principles

            # Load all principles from .md files
            principles_list = load_all_principles(self.principles_dir)

            # Build categories from loaded principles
            categories_set = set()
            for principle_data in principles_list:
                categories_set.add(principle_data["category"])

            # Create category list (simplified, no metadata)
            self.categories = [{"id": cat, "name": cat} for cat in sorted(categories_set)]

            # Hardcoded selection strategies (TODO: move to config file)
            self.selection_strategies = {
                "minimal": {"include": ["U001", "U002", "U003", "P001"]},
                "auto": {"rules": []},  # Auto selection based on characteristics
            }

            # Load all principles
            for principle_data in principles_list:
                principle = Principle(
                    id=principle_data["id"],
                    number=principle_data["number"],
                    title=principle_data["title"],
                    category=principle_data["category"],
                    severity=principle_data["severity"],
                    weight=principle_data["weight"],
                    description=principle_data["description"],
                    applicability=principle_data.get("applicability", {}),
                    rules=principle_data.get("rules", []),
                    examples=principle_data.get("examples", {}),
                    autofix=principle_data.get("autofix", {}),
                )
                self.principles[principle.id] = principle

        except Exception as e:
            print(f"[ERROR] Failed to load principles: {e}")

    def get_principle(self, principle_id: str) -> Optional[Principle]:
        """Get a principle by ID."""
        return self.principles.get(principle_id)

    def get_all_principles(self) -> List[Principle]:
        """Get all loaded principles."""
        return list(self.principles.values())

    def get_principles_by_category(self, category: str) -> List[Principle]:
        """Get all principles in a category."""
        return [p for p in self.principles.values() if p.category == category]

    def get_principles_by_severity(self, severity: str) -> List[Principle]:
        """Get all principles with given severity."""
        return [p for p in self.principles.values() if p.severity == severity]

    def select_principles(
        self,
        characteristics: ProjectCharacteristics,
        strategy: str = "auto",
        user_preferences: Optional[List[str]] = None,
    ) -> List[str]:
        """
        Select principles based on project characteristics and strategy.

        Args:
            characteristics: Project characteristics
            strategy: Selection strategy ("auto", "minimal", "comprehensive")
            user_preferences: Optional list of principle IDs from user preferences

        Returns:
            List of principle IDs to activate
        """
        # Start with user preferences if provided
        if user_preferences:
            selected = set(user_preferences)
        else:
            selected = set()

        # Apply selection strategy
        if strategy == "comprehensive":
            # All principles
            selected.update(self.principles.keys())

        elif strategy == "minimal":
            # Use minimal strategy from selection_strategies
            minimal_strategy = self.selection_strategies.get("minimal", {})
            minimal_ids = minimal_strategy.get("include", [])
            if minimal_ids:
                selected.update(minimal_ids)

        elif strategy == "auto":
            # Dynamic selection based on project characteristics
            selected.update(self._auto_select_principles(characteristics))

        return list(selected)

    def _auto_select_principles(self, characteristics: ProjectCharacteristics) -> Set[str]:
        """
        Automatically select principles based on project characteristics.

        This implements the "auto" selection strategy from principle frontmatter.
        """
        selected = set()

        # Always include critical principles (severity=critical, all projects)
        for principle in self.principles.values():
            if principle.severity == "critical":
                applicability = principle.applicability
                project_types = applicability.get("project_types", [])

                # If applicable to all or matches project type
                if "all" in project_types or characteristics.project_type in project_types:
                    if self._check_conditions(principle, characteristics):
                        selected.add(principle.id)

        # Apply selection rules from strategies
        auto_strategy = self.selection_strategies.get("auto", {})
        rules = auto_strategy.get("rules", [])

        for rule in rules:
            condition = rule.get("condition", "")
            include_ids = rule.get("include", [])

            if self._evaluate_condition(condition, characteristics):
                selected.update(include_ids)

        # Add high-severity principles for relevant contexts
        for principle in self.principles.values():
            if principle.severity == "high":
                if self._is_applicable(principle, characteristics):
                    selected.add(principle.id)

        # Add medium-severity principles if context matches
        for principle in self.principles.values():
            if principle.severity == "medium":
                if self._is_applicable(principle, characteristics):
                    # Check if any context matches
                    applicability = principle.applicability
                    contexts = applicability.get("contexts", [])

                    if "all" in contexts:
                        selected.add(principle.id)
                    else:
                        # Check if any project context matches principle contexts
                        if any(ctx in characteristics.contexts for ctx in contexts):
                            selected.add(principle.id)

        return selected

    def _is_applicable(self, principle: Principle, characteristics: ProjectCharacteristics) -> bool:
        """Check if a principle is applicable to the project."""
        applicability = principle.applicability

        # Check project types
        project_types = applicability.get("project_types", [])
        if project_types and "all" not in project_types:
            if characteristics.project_type not in project_types:
                return False

        # Check languages
        languages = applicability.get("languages", [])
        if languages and "all" not in languages:
            if characteristics.primary_language not in languages:
                return False

        # Check contexts
        contexts = applicability.get("contexts", [])
        if contexts and "all" not in contexts:
            if not any(ctx in characteristics.contexts for ctx in contexts):
                return False

        # Check conditions
        if not self._check_conditions(principle, characteristics):
            return False

        return True

    def _check_conditions(
        self,
        principle: Principle,
        characteristics: ProjectCharacteristics,
    ) -> bool:
        """Check if principle conditions are met."""
        applicability = principle.applicability
        conditions = applicability.get("conditions", [])

        if not conditions:
            return True

        # Evaluate each condition
        for condition in conditions:
            if isinstance(condition, str):
                if not self._evaluate_condition(condition, characteristics):
                    return False

        return True

    def _evaluate_condition(self, condition: str, characteristics: ProjectCharacteristics) -> bool:
        """
        Evaluate a condition string.

        Examples:
        - "project.type == 'api'"
        - "project.characteristics.privacy_critical == true"
        - "project.team.size == 'large'"
        - "project.detection.containers.runtime != null"
        - "services > 2"
        - "team_size > 5"
        """
        try:
            # Simple condition parsing
            condition = condition.strip()

            # API type check
            if "project.type == 'api'" in condition:
                return characteristics.project_type == "api"

            if "project.type == 'microservices'" in condition:
                return characteristics.project_type == "microservices"

            # Privacy critical
            if "privacy_critical == true" in condition or "privacy_critical" in condition:
                return characteristics.privacy_critical

            # Security critical
            if "security_critical == true" in condition or "security_critical" in condition:
                return characteristics.security_critical

            # Performance critical
            if "performance_critical == true" in condition:
                return characteristics.performance_critical

            # Team size
            if "team.size == 'large'" in condition or "team_size > 5" in condition:
                return characteristics.team_size == "large"

            if "team.size == 'medium'" in condition:
                return characteristics.team_size == "medium"

            if "team_size > 1" in condition or "team.size > 1" in condition:
                return characteristics.team_size in ["small", "medium", "large"]

            if "team_size > 2" in condition:
                return characteristics.team_size in ["medium", "large"]

            # Services count
            if "services > 2" in condition:
                return characteristics.services_count > SERVICE_COUNT_THRESHOLD_MEDIUM

            if "services > 3" in condition:
                return characteristics.services_count > SERVICE_COUNT_THRESHOLD_LARGE

            # Containers
            if "containers.runtime != null" in condition or "has_containers" in condition:
                return characteristics.has_containers

            # Default: true if we don't understand the condition
            return True

        except Exception:
            # If we can't evaluate, assume true
            return True

    def get_autofix_principles(self) -> List[Principle]:
        """Get all principles that support auto-fix."""
        return [p for p in self.principles.values() if p.autofix.get("available", False)]

    def get_principle_summary(self, principle_id: str) -> Optional[Dict[str, Any]]:
        """Get a summary of a principle for display."""
        principle = self.get_principle(principle_id)
        if not principle:
            return None

        return {
            "id": principle.id,
            "number": principle.number,
            "title": principle.title,
            "category": principle.category,
            "severity": principle.severity,
            "description": principle.description,
            "autofix_available": principle.autofix.get("available", False),
            "rules_count": len(principle.rules),
        }

    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about loaded principles."""
        return {
            "version": self.version,
            "total_principles": len(self.principles),
            "by_severity": {
                "critical": len(self.get_principles_by_severity("critical")),
                "high": len(self.get_principles_by_severity("high")),
                "medium": len(self.get_principles_by_severity("medium")),
                "low": len(self.get_principles_by_severity("low")),
            },
            "by_category": {
                cat["id"]: len(self.get_principles_by_category(cat["id"]))
                for cat in self.categories
            },
            "autofix_available": len(self.get_autofix_principles()),
        }


def create_characteristics_from_analysis(analysis: Dict[str, Any]) -> ProjectCharacteristics:
    """
    Create ProjectCharacteristics from project analysis data.

    Args:
        analysis: Project analysis dictionary from ProjectAnalyzer

    Returns:
        ProjectCharacteristics object
    """
    return ProjectCharacteristics(
        project_type=analysis.get("type", "unknown"),
        primary_language=analysis.get("language", "unknown"),
        team_size=analysis.get("team_size", "solo"),
        services_count=len(analysis.get("services", [])),
        privacy_critical=analysis.get("privacy_critical", False),
        security_critical=analysis.get("security_critical", False),
        performance_critical=analysis.get("performance_critical", False),
        has_containers=bool(analysis.get("containers", {}).get("detected", False)),
        has_tests=bool(analysis.get("tests", {}).get("detected", False)),
        contexts=analysis.get("contexts", ["all"]),
    )


@lru_cache(maxsize=1)
def get_principles_manager(principles_dir: Optional[str] = None) -> PrinciplesManager:
    """
    Get cached PrinciplesManager instance (Singleton pattern - P012).

    Expensive resource: Loads ~81 principles from .md files.
    Using @lru_cache ensures only one instance exists per principles_dir.

    Args:
        principles_dir: Path to principles directory (default: content/principles/ from package)

    Returns:
        Cached PrinciplesManager instance
    """
    path = Path(principles_dir) if principles_dir else None
    return PrinciplesManager(path)


__all__ = [
    "Principle",
    "ProjectCharacteristics",
    "PrinciplesManager",
    "get_principles_manager",  # Singleton factory (P012)
    "create_characteristics_from_analysis",
]

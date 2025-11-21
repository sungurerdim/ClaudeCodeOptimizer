"""
Principles management system for ClaudeCodeOptimizer.

Loads and manages development principles from .md files.
Implements dynamic principle selection based on project characteristics.

See README.md for current principle counts.
"""

import logging
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from typing import Any

from ..config import VERSION

logger = logging.getLogger(__name__)


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
    applicability: dict[str, Any]
    rules: list[dict[str, Any]]
    examples: dict[str, list[str]]
    autofix: dict[str, Any]


class PrinciplesManager:
    """Manages loading and selection of development principles."""

    def __init__(self, principles_dir: Path | None = None) -> None:
        """
        Initialize principles manager.

        Args:
            principles_dir: Path to principles directory
                (default: claudecodeoptimizer/content/principles/)
        """
        if principles_dir is None:
            # Load from package content/ directory
            package_dir = Path(__file__).parent.parent
            principles_dir = package_dir / "content" / "principles"

        self.principles_dir = principles_dir
        self.principles: dict[str, Principle] = {}
        self.categories: list[dict[str, Any]] = []
        self.version: str = VERSION

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
            logger.error("Failed to load principles: %s", e, exc_info=True)

    def get_principle(self, principle_id: str) -> Principle | None:
        """Get a principle by ID."""
        return self.principles.get(principle_id)

    def get_all_principles(self) -> list[Principle]:
        """Get all loaded principles."""
        return list(self.principles.values())

    def get_principles_by_category(self, category: str) -> list[Principle]:
        """Get all principles in a category."""
        return [p for p in self.principles.values() if p.category == category]

    def get_principles_by_severity(self, severity: str) -> list[Principle]:
        """Get all principles with given severity."""
        return [p for p in self.principles.values() if p.severity == severity]

    def get_autofix_principles(self) -> list[Principle]:
        """Get all principles that support auto-fix."""
        return [p for p in self.principles.values() if p.autofix.get("available", False)]

    def get_principle_summary(self, principle_id: str) -> dict[str, Any] | None:
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

    def get_statistics(self) -> dict[str, Any]:
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


@lru_cache(maxsize=1)
def get_principles_manager(principles_dir: str | None = None) -> PrinciplesManager:
    """
    Get cached PrinciplesManager instance (Singleton pattern - P_EVENT_DRIVEN).

    Expensive resource: Loads all principles from .md files.
    Using @lru_cache ensures only one instance exists per principles_dir.

    Args:
        principles_dir: Path to principles directory
            (default: claudecodeoptimizer/content/principles/)

    Returns:
        Cached PrinciplesManager instance
    """
    path = Path(principles_dir) if principles_dir else None
    return PrinciplesManager(path)


__all__ = [
    "Principle",
    "PrinciplesManager",
    "get_principles_manager",  # Singleton factory (P_EVENT_DRIVEN)
]

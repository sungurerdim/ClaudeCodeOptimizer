"""
Tool Comparison Logic (TIER 3)

When multiple competing tools are detected, provides recommendations
based on current best practices and project context.

Examples:
- ruff vs black (formatter)
- ruff vs flake8 (linter)
- pytest vs unittest (test framework)
- poetry vs pip-tools (dependency management)
"""

from typing import Dict, List, Optional

from .models import ToolComparison


class ToolComparator:
    """Compare detected tools and recommend best choices"""

    # Tool categories and their competing tools
    TOOL_CATEGORIES = {
        "formatter": {
            "tools": ["black", "ruff", "autopep8", "yapf"],
            "recommended": "ruff",
            "reasons": {
                "ruff": "Fast, modern, includes formatter + linter (all-in-one)",
                "black": "Stable, opinionated, widely adopted (good alternative)",
                "autopep8": "Legacy, slower than ruff",
                "yapf": "Less common, Google-style focused",
            },
        },
        "linter": {
            "tools": [
                "ruff",
                "flake8",
                "pylint",
                "pycodestyle",
                "pydocstyle",
                "mypy",
            ],
            "recommended": "ruff",
            "reasons": {
                "ruff": "Fast, modern, comprehensive checks (recommended)",
                "flake8": "Stable, plugin ecosystem (good for legacy projects)",
                "pylint": "Very thorough but slow, opinionated",
                "pycodestyle": "Basic PEP 8 only, use ruff instead",
                "pydocstyle": "Docstring-specific, supplement to ruff",
                "mypy": "Type checking only (use alongside ruff)",
            },
        },
        "test_framework": {
            "tools": ["pytest", "unittest", "nose", "nose2"],
            "recommended": "pytest",
            "reasons": {
                "pytest": "Modern, powerful, great plugins (recommended)",
                "unittest": "Built-in, verbose, good for simple projects",
                "nose": "Deprecated, migrate to pytest",
                "nose2": "Successor to nose, less popular than pytest",
            },
        },
        "type_checker": {
            "tools": ["mypy", "pyright", "pyre", "pytype"],
            "recommended": "mypy",
            "reasons": {
                "mypy": "Standard, widely used, good error messages",
                "pyright": "Fast, VS Code integration, strict by default",
                "pyre": "Facebook's checker, performance-focused",
                "pytype": "Google's checker, type inference",
            },
        },
        "dependency_manager": {
            "tools": ["poetry", "pip-tools", "pipenv", "pip"],
            "recommended": "pip-tools",
            "reasons": {
                "pip-tools": "Simple, reliable, pure pip workflow (recommended for most)",
                "poetry": "Feature-rich, packaging + deps, heavier (good for libraries)",
                "pipenv": "Automatic virtualenvs, slower, less maintained",
                "pip": "Basic, no locking, use pip-tools for lockfiles",
            },
        },
        "task_runner": {
            "tools": ["make", "invoke", "nox", "tox", "just"],
            "recommended": "make",
            "reasons": {
                "make": "Universal, simple, cross-language (recommended)",
                "invoke": "Python-based, flexible, good for Python-only",
                "nox": "Testing across Python versions, like tox but better",
                "tox": "Testing automation, virtualenv management",
                "just": "Modern make alternative, nicer syntax",
            },
        },
        "coverage_tool": {
            "tools": ["coverage", "pytest-cov"],
            "recommended": "pytest-cov",
            "reasons": {
                "pytest-cov": "Pytest integration, convenient (recommended)",
                "coverage": "Core library, used by pytest-cov",
            },
        },
        "documentation": {
            "tools": ["sphinx", "mkdocs", "pdoc", "pydoc"],
            "recommended": "mkdocs",
            "reasons": {
                "mkdocs": "Simple, beautiful, Markdown-based (recommended for most)",
                "sphinx": "Powerful, RST-based, good for large projects",
                "pdoc": "Auto-generated, minimal setup",
                "pydoc": "Built-in, basic, use mkdocs instead",
            },
        },
        "build_system": {
            "tools": ["setuptools", "poetry", "hatchling", "flit"],
            "recommended": "hatchling",
            "reasons": {
                "hatchling": "Modern, PEP 621, simple (recommended for new projects)",
                "setuptools": "Traditional, widely compatible (safe choice)",
                "poetry": "All-in-one, opinionated, heavier",
                "flit": "Simple, for pure Python packages",
            },
        },
    }

    def __init__(self, detected_tools: List[str]):
        """
        Initialize comparator with detected tools.

        Args:
            detected_tools: List of tool names detected in project
        """
        self.detected_tools = [tool.lower() for tool in detected_tools]

    def analyze_category(self, category: str) -> Optional[ToolComparison]:
        """
        Analyze tools in a specific category.

        Args:
            category: Tool category (e.g., "formatter", "linter")

        Returns:
            ToolComparison if multiple tools found, None otherwise
        """
        if category not in self.TOOL_CATEGORIES:
            return None

        cat_info = self.TOOL_CATEGORIES[category]
        possible_tools = cat_info["tools"]

        # Find detected tools in this category
        detected = [tool for tool in self.detected_tools if tool in possible_tools]

        if len(detected) <= 1:
            return None  # No conflict

        # Build comparison
        recommended = cat_info["recommended"]
        reasons = cat_info["reasons"]

        return ToolComparison(
            category=category,
            tools=detected,
            recommended=recommended,
            reason=reasons.get(recommended, "Recommended"),
            alternatives={
                tool: reasons.get(tool, "Alternative option")
                for tool in detected
                if tool != recommended
            },
        )

    def find_all_conflicts(self) -> List[ToolComparison]:
        """
        Find all tool conflicts in detected tools.

        Returns:
            List of ToolComparison objects for categories with conflicts
        """
        conflicts = []

        for category in self.TOOL_CATEGORIES.keys():
            comparison = self.analyze_category(category)
            if comparison:
                conflicts.append(comparison)

        return conflicts

    def get_recommendations(self) -> Dict[str, str]:
        """
        Get recommended tool for each category.

        Returns:
            Dict mapping category -> recommended tool name
        """
        recommendations = {}

        for category in self.TOOL_CATEGORIES.keys():
            cat_info = self.TOOL_CATEGORIES[category]
            possible_tools = cat_info["tools"]

            # Check if any tools from this category are detected
            detected = [tool for tool in self.detected_tools if tool in possible_tools]

            if detected:
                recommendations[category] = cat_info["recommended"]

        return recommendations

    def should_ask_preference(self, category: str) -> bool:
        """
        Check if we should ask user preference for this category.

        Args:
            category: Tool category

        Returns:
            True if multiple tools detected in category
        """
        comparison = self.analyze_category(category)
        return comparison is not None

    def get_tool_description(self, tool_name: str) -> str:
        """
        Get description/reason for a specific tool.

        Args:
            tool_name: Name of the tool

        Returns:
            Description string
        """
        tool_lower = tool_name.lower()

        # Search across all categories
        for cat_info in self.TOOL_CATEGORIES.values():
            if tool_lower in cat_info["reasons"]:
                return cat_info["reasons"][tool_lower]

        return f"{tool_name} (detected in project)"

    def explain_recommendation(self, category: str) -> str:
        """
        Get detailed explanation for category recommendation.

        Args:
            category: Tool category

        Returns:
            Explanation string
        """
        if category not in self.TOOL_CATEGORIES:
            return f"No recommendation available for {category}"

        cat_info = self.TOOL_CATEGORIES[category]
        recommended = cat_info["recommended"]
        reason = cat_info["reasons"].get(recommended, "Recommended")

        detected = [tool for tool in self.detected_tools if tool in cat_info["tools"]]

        if len(detected) > 1:
            others = [t for t in detected if t != recommended]
            return (
                f"Recommend {recommended}: {reason}\n"
                f"You have: {', '.join(detected)}\n"
                f"Consider migrating from {others[0]} to {recommended}"
            )
        else:
            return f"Recommend {recommended}: {reason}"


def compare_tools(detected_tools: List[str]) -> ToolComparator:
    """
    Convenience function to create ToolComparator.

    Args:
        detected_tools: List of detected tool names

    Returns:
        ToolComparator instance
    """
    return ToolComparator(detected_tools)


def get_formatter_recommendation(detected_tools: List[str]) -> str:
    """Get recommended formatter"""
    comparator = ToolComparator(detected_tools)
    recs = comparator.get_recommendations()
    return recs.get("formatter", "ruff")


def get_linter_recommendation(detected_tools: List[str]) -> str:
    """Get recommended linter"""
    comparator = ToolComparator(detected_tools)
    recs = comparator.get_recommendations()
    return recs.get("linter", "ruff")


def get_test_framework_recommendation(detected_tools: List[str]) -> str:
    """Get recommended test framework"""
    comparator = ToolComparator(detected_tools)
    recs = comparator.get_recommendations()
    return recs.get("test_framework", "pytest")

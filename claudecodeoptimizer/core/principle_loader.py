"""
Principle Loader - Category-Based Loading System

Maps commands to principle categories for token optimization.
Only loads relevant principles for each command.

Before: ~5000 tokens (all 74 principles)
After: ~500-1500 tokens (core + relevant categories)

Pattern from wshobson/agents for progressive disclosure.
"""

from pathlib import Path
from typing import Dict, List, Optional


# Command → Principle Category Mapping
COMMAND_PRINCIPLE_MAP: Dict[str, List[str]] = {
    # Core commands (core only)
    "cco-init": ["core"],
    "cco-status": ["core"],
    "cco-config": ["core"],
    "cco-remove": ["core"],
    # Audit commands
    "cco-audit": ["all"],  # Full audit loads everything
    "cco-audit-code": ["core", "code-quality"],
    "cco-audit-security": ["core", "security"],
    "cco-audit-tests": ["core", "testing"],
    "cco-audit-docs": ["core", "code-quality"],
    "cco-audit-all": ["all"],
    # Analysis commands
    "cco-analyze": ["core", "architecture", "code-quality"],
    "cco-analyze-structure": ["core", "architecture"],
    "cco-analyze-dependencies": ["core", "architecture"],
    "cco-analyze-complexity": ["core", "code-quality"],
    # Fix commands
    "cco-fix": ["core", "code-quality", "security"],
    "cco-fix-code": ["core", "code-quality"],
    "cco-fix-security": ["core", "security"],
    "cco-fix-docs": ["core", "code-quality"],
    # Optimize commands
    "cco-optimize": ["core", "performance"],
    "cco-optimize-code": ["core", "performance", "code-quality"],
    "cco-optimize-deps": ["core", "performance"],
    "cco-optimize-docker": ["core", "performance", "operations"],
    # Test commands
    "cco-test": ["core", "testing"],
    "cco-generate-tests": ["core", "testing"],
    "cco-audit-tests": ["core", "testing"],
    # Generate commands
    "cco-generate": ["core", "code-quality"],
    "cco-generate-docs": ["core", "api-design"],
    "cco-generate-integration-tests": ["core", "testing"],
    # DevOps commands
    "cco-scan-secrets": ["core", "security"],
    "cco-setup-cicd": ["core", "operations"],
    "cco-setup-monitoring": ["core", "operations"],
    # Sync commands
    "cco-sync": ["core"],
}


class PrincipleLoader:
    """Load principles by category for token optimization"""

    def __init__(self, principles_dir: Optional[Path] = None) -> None:
        """
        Initialize principle loader.

        Args:
            principles_dir: Directory containing principle category files
                          (default: docs/cco/principles/)
        """
        if principles_dir is None:
            # Try multiple locations
            candidates = [
                Path.cwd() / "docs" / "cco" / "principles",
                Path.cwd() / "principles",
                Path(__file__).parent.parent.parent / "docs" / "cco" / "principles",
            ]
            for candidate in candidates:
                if candidate.exists():
                    principles_dir = candidate
                    break
            else:
                # Fallback to first candidate (will be created if needed)
                principles_dir = candidates[0]

        self.principles_dir = principles_dir
        self._cache: Dict[str, str] = {}

    def load_for_command(self, command: str) -> str:
        """
        Load only relevant principles for a command.

        Args:
            command: Command name (e.g., "cco-audit-security")

        Returns:
            Combined principle content for the command

        Examples:
            >>> loader = PrincipleLoader()
            >>> content = loader.load_for_command("cco-audit-security")
            # Returns: core.md + security.md (~1500 tokens)
        """
        # Get categories for this command
        categories = COMMAND_PRINCIPLE_MAP.get(command, ["core"])

        # Handle "all" special case
        if "all" in categories:
            return self.load_all_principles()

        # Load each category
        principles = []
        for category in categories:
            content = self.load_category(category)
            if content:
                principles.append(content)

        return "\n\n---\n\n".join(principles)

    def load_category(self, category: str) -> str:
        """
        Load a specific principle category.

        Args:
            category: Category name (e.g., "core", "security", "code-quality")

        Returns:
            Category principle content

        Token estimates:
            - core: ~500 tokens
            - code-quality: ~1400 tokens
            - security: ~1900 tokens
            - testing: ~600 tokens
            - architecture: ~1100 tokens
            - performance: ~500 tokens
            - operations: ~1100 tokens
            - git-workflow: ~500 tokens
            - api-design: ~300 tokens
        """
        # Check cache
        if category in self._cache:
            return self._cache[category]

        # Load from file
        category_file = self.principles_dir / f"{category}.md"

        if not category_file.exists():
            return ""

        content = category_file.read_text(encoding="utf-8")
        self._cache[category] = content
        return content

    def load_all_principles(self) -> str:
        """
        Load all principle categories.

        Returns:
            All principles combined (~7500 tokens)

        Note: Only use for comprehensive audits. Prefer category-based loading.
        """
        if not self.principles_dir.exists():
            return ""

        all_principles = []
        category_files = sorted(self.principles_dir.glob("*.md"))

        for category_file in category_files:
            # Skip PRINCIPLES.md summary file
            if category_file.name == "PRINCIPLES.md":
                continue

            content = category_file.read_text(encoding="utf-8")
            all_principles.append(content)

        return "\n\n---\n\n".join(all_principles)

    def get_categories_for_command(self, command: str) -> List[str]:
        """
        Get principle categories for a command.

        Args:
            command: Command name

        Returns:
            List of category names
        """
        return COMMAND_PRINCIPLE_MAP.get(command, ["core"])

    def estimate_token_count(self, command: str) -> int:
        """
        Estimate token count for a command's principles.

        Args:
            command: Command name

        Returns:
            Estimated token count

        Token estimates by category:
            - core: 500
            - code-quality: 1400
            - security: 1900
            - testing: 600
            - architecture: 1100
            - performance: 500
            - operations: 1100
            - git-workflow: 500
            - api-design: 300
        """
        CATEGORY_TOKENS = {
            "core": 500,
            "code-quality": 1400,
            "security": 1900,
            "testing": 600,
            "architecture": 1100,
            "performance": 500,
            "operations": 1100,
            "git-workflow": 500,
            "api-design": 300,
        }

        categories = self.get_categories_for_command(command)

        if "all" in categories:
            return sum(CATEGORY_TOKENS.values())

        return sum(CATEGORY_TOKENS.get(cat, 500) for cat in categories)

    def clear_cache(self) -> None:
        """Clear principle cache."""
        self._cache.clear()


# Convenience function
def load_principles_for_command(command: str) -> str:
    """
    Load principles for a command (convenience function).

    Args:
        command: Command name

    Returns:
        Principle content for the command

    Examples:
        >>> content = load_principles_for_command("cco-audit-security")
        >>> print(f"Loaded {len(content)} characters")
    """
    loader = PrincipleLoader()
    return loader.load_for_command(command)

"""
Principle Loader - Individual Principle Loading System

Maps commands to specific principle IDs for token optimization.
Only loads relevant principles for each command.

Before: ~5000 tokens (all principles loaded)
After: ~200-800 tokens (3-10 specific principles)

See README.md for current principle counts.

Architecture:
- Individual principle files (U_DRY.md, U_INTEGRATION_CHECK.md, P_LINTING_SAST.md, ...)
- Direct principle ID loading
- Category-to-ID mapping from .md frontmatter
"""

from pathlib import Path

# Command → principle categories (universal always included)

COMMAND_PRINCIPLE_MAP: dict[str, list[str]] = {
    # Core commands (universal + core only)
    "cco-status": ["universal", "core"],
    "cco-config": ["universal", "core"],
    "cco-remove": ["universal", "core"],
    # Audit commands
    "cco-audit": ["universal", "all"],  # Full audit loads everything
    "cco-audit-code": ["universal", "core", "code_quality"],
    "cco-audit-security": ["universal", "core", "security_privacy"],
    "cco-audit-tests": ["universal", "core", "testing"],
    "cco-audit-docs": ["universal", "core", "code_quality"],
    "cco-audit-all": ["universal", "all"],
    # Analysis commands
    "cco-analyze": ["universal", "core", "architecture", "code_quality"],
    "cco-analyze-structure": ["universal", "core", "architecture"],
    "cco-analyze-dependencies": ["universal", "core", "architecture"],
    "cco-analyze-complexity": ["universal", "core", "code_quality"],
    # Fix commands
    "cco-fix": ["universal", "core", "code_quality", "security_privacy"],
    "cco-fix-code": ["universal", "core", "code_quality"],
    "cco-fix-security": ["universal", "core", "security_privacy"],
    "cco-fix-docs": ["universal", "core", "code_quality"],
    # Optimize commands
    "cco-optimize": ["universal", "core", "performance"],
    "cco-optimize-code": ["universal", "core", "performance", "code_quality"],
    "cco-optimize-deps": ["universal", "core", "performance"],
    "cco-optimize-docker": ["universal", "core", "performance", "project-specific"],
    # Test commands
    "cco-test": ["universal", "core", "testing"],
    "cco-generate-tests": ["universal", "core", "testing"],
    # Generate commands
    "cco-generate": ["universal", "core", "code_quality"],
    "cco-generate-docs": ["universal", "core", "api_design"],
    "cco-generate-integration-tests": ["universal", "core", "testing"],
    # DevOps commands
    "cco-scan-secrets": ["universal", "core", "security_privacy"],
    "cco-setup-cicd": ["universal", "core", "project-specific"],
    "cco-setup-monitoring": ["universal", "core", "project-specific"],
    # Sync commands
    "cco-sync": ["universal", "core"],
}

# Category → Principle ID Mapping (cached)
_CATEGORY_TO_IDS: dict[str, list[str]] | None = None


def _load_category_mapping() -> dict[str, list[str]]:
    """Load category to principle ID mapping from .md files"""
    global _CATEGORY_TO_IDS

    if _CATEGORY_TO_IDS is not None:
        return _CATEGORY_TO_IDS

    # Load from claudecodeoptimizer/content/principles/ directory
    package_dir = Path(__file__).parent.parent
    principles_dir = package_dir / "content" / "principles"

    if not principles_dir.exists():
        # Fallback: return empty mapping
        _CATEGORY_TO_IDS = {}
        return _CATEGORY_TO_IDS

    # Use principle_md_loader to get category mapping
    from .principle_md_loader import get_category_mapping

    mapping = get_category_mapping(principles_dir)

    # Add "core" category (now references universal principles)
    # Core principles are now U_EVIDENCE_BASED, U_FAIL_FAST, U_NO_OVERENGINEERING
    mapping["core"] = ["U_EVIDENCE_BASED", "U_FAIL_FAST", "U_NO_OVERENGINEERING"]

    _CATEGORY_TO_IDS = mapping
    return mapping


def _resolve_categories_to_ids(categories: list[str]) -> list[str]:
    """Convert category names to principle IDs"""
    mapping = _load_category_mapping()
    principle_ids = []

    for category in categories:
        if category == "all":
            # Return all principle IDs
            for cat_ids in mapping.values():
                principle_ids.extend(cat_ids)
        elif category in mapping:
            principle_ids.extend(mapping[category])

    # Remove duplicates while preserving order
    seen = set()
    unique_ids = []
    for pid in principle_ids:
        if pid not in seen:
            seen.add(pid)
            unique_ids.append(pid)

    return unique_ids


class PrincipleLoader:
    """Load principles by category for token optimization"""

    def __init__(self, principles_dir: Path | None = None) -> None:
        """
        Initialize principle loader.

        Args:
            principles_dir: Directory containing principle category files
                          (default: ~/.claude/principles/)
        """
        if principles_dir is None:
            from ..config import CCOConfig

            principles_dir = CCOConfig.get_principles_dir()

        if not principles_dir.exists():
            raise FileNotFoundError(
                f"Principles directory not found: {principles_dir}\n"
                f"Please ensure CCO is properly installed."
            )

        self.principles_dir = principles_dir
        self._cache: dict[str, str] = {}

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
            # Returns: U_*.md + P_*.md + C_*.md files (~800 tokens)
        """
        # Use COMMAND_PRINCIPLE_MAP (STATIC)
        categories = COMMAND_PRINCIPLE_MAP.get(command, ["universal", "core"])

        # Convert categories to principle IDs
        principle_ids = _resolve_categories_to_ids(categories)

        # Load each principle
        principles = []
        for principle_id in principle_ids:
            content = self.load_principle(principle_id)
            if content:
                principles.append(content)

        return "\n\n---\n\n".join(principles)

    def load_principles(self, principle_ids: list[str]) -> str:
        """
        Load multiple principles by their IDs directly.

        Args:
            principle_ids: List of principle IDs
                (e.g., ["U_DRY", "P_CONTAINER_SECURITY"])

        Returns:
            Combined principle content

        Examples:
            >>> loader = PrincipleLoader()
            >>> content = loader.load_principles(["U_DRY", "P_API_SECURITY"])
            # Returns: Content of U_DRY.md + P_API_SECURITY.md
        """
        principles = []
        for principle_id in principle_ids:
            content = self.load_principle(principle_id)
            if content:
                principles.append(content)

        return "\n\n---\n\n".join(principles)

    def load_from_frontmatter(self, command_file: Path) -> str:
        """
        Load principles specified in command file frontmatter.

        Args:
            command_file: Path to command markdown file

        Returns:
            Combined principle content

        Examples:
            >>> loader = PrincipleLoader()
            >>> cmd_file = Path("claudecodeoptimizer/content/commands/audit.md")
            >>> content = loader.load_from_frontmatter(cmd_file)
            # Reads principles: [...] from frontmatter and loads them
        """
        import re

        if not command_file.exists():
            return ""

        content = command_file.read_text(encoding="utf-8")

        # Extract frontmatter
        if not content.startswith("---"):
            return ""

        parts = content.split("---", 2)
        if len(parts) < 3:
            return ""

        frontmatter = parts[1]

        # Find principles line
        match = re.search(r"principles:\s*\[(.*?)\]", frontmatter, re.DOTALL)
        if not match:
            return ""

        # Parse principle IDs
        principles_str = match.group(1)
        principle_ids = [
            pid.strip().strip("'\"") for pid in principles_str.split(",") if pid.strip()
        ]

        return self.load_principles(principle_ids)

    def load_principle(self, principle_id: str) -> str:
        """
        Load a specific principle by ID.

        Args:
            principle_id: Principle ID (e.g., "U_DRY", "P_CONTAINER_SECURITY")

        Returns:
            Principle file content

        Examples:
            >>> loader = PrincipleLoader()
            >>> content = loader.load_principle("U_DRY")
            # Returns: Content of U_DRY.md
        """
        # Check cache
        if principle_id in self._cache:
            return self._cache[principle_id]

        # Read principle file
        principle_file = self.principles_dir / f"{principle_id}.md"

        if not principle_file.exists():
            return ""

        content = principle_file.read_text(encoding="utf-8")
        self._cache[principle_id] = content
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

    def get_categories_for_command(self, command: str) -> list[str]:
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
        category_tokens = {
            "core": 500,
            "code-quality": 1400,
            "security": 1900,
            "testing": 600,
            "architecture": 1100,
            "performance": 500,
            "project-specific": 1100,
            "git-workflow": 500,
            "api-design": 300,
        }

        categories = self.get_categories_for_command(command)

        if "all" in categories:
            return sum(category_tokens.values())

        return sum(category_tokens.get(cat, 500) for cat in categories)

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

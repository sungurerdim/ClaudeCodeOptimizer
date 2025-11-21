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
        # Try to load from command file frontmatter first (dynamic)
        package_dir = Path(__file__).parent.parent
        command_file = package_dir / "content" / "commands" / f"{command}.md"

        if command_file.exists():
            content = self.load_from_frontmatter(command_file)
            if content:  # If frontmatter has principles, use them
                return content

        # No frontmatter found - return empty
        return ""

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

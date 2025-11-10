"""
Guide Loader - On-Demand Loading System

Loads comprehensive guides only when explicitly requested.
Implements caching for performance.

Before: ~3000 tokens (guides loaded with CLAUDE.md)
After: ~1000 tokens (core only, guides on-demand)

Pattern from wshobson/agents for progressive disclosure.
"""

from pathlib import Path
from typing import Dict, List, Optional


class GuideLoader:
    """Load guides on-demand with caching"""

    def __init__(self, guides_dir: Optional[Path] = None) -> None:
        """
        Initialize guide loader.

        Args:
            guides_dir: Directory containing guide files
                       (default: docs/cco/guides/)
        """
        if guides_dir is None:
            # Try multiple locations
            candidates = [
                Path.cwd() / "docs" / "cco" / "guides",
                Path.cwd() / "guides",
                Path(__file__).parent.parent.parent / "docs" / "cco" / "guides",
            ]
            for candidate in candidates:
                if candidate.exists():
                    guides_dir = candidate
                    break
            else:
                # Fallback to first candidate
                guides_dir = candidates[0]

        self.guides_dir = guides_dir
        self._cache: Dict[str, str] = {}

    def load_guide(self, guide_name: str) -> str:
        """
        Load guide on-demand with caching.

        Args:
            guide_name: Guide name (with or without .md extension)

        Returns:
            Guide content

        Examples:
            >>> loader = GuideLoader()
            >>> content = loader.load_guide("verification-protocol")
            >>> print(f"Loaded {len(content)} characters")

        Token estimates:
            - verification-protocol: ~600 tokens
            - git-workflow: ~1400 tokens
            - security-response: ~1300 tokens
            - performance-optimization: ~1700 tokens
            - container-best-practices: ~2200 tokens
        """
        # Normalize guide name
        if not guide_name.endswith(".md"):
            guide_name = f"{guide_name}.md"

        # Check cache
        if guide_name in self._cache:
            return self._cache[guide_name]

        # Load from file
        guide_path = self.guides_dir / guide_name

        if not guide_path.exists():
            return ""

        content = guide_path.read_text(encoding="utf-8")
        self._cache[guide_name] = content
        return content

    def discover_guides(self) -> List[str]:
        """
        Discover all available guides.

        Returns:
            List of guide names (without .md extension)
        """
        if not self.guides_dir.exists():
            return []

        guides = []
        for guide_file in self.guides_dir.glob("*.md"):
            guides.append(guide_file.stem)

        return sorted(guides)

    def get_guide_summary(self, guide_name: str) -> str:
        """
        Get guide summary (first paragraph).

        Args:
            guide_name: Guide name

        Returns:
            Guide summary (~50 tokens)
        """
        content = self.load_guide(guide_name)
        if not content:
            return ""

        # Extract first paragraph after title
        lines = content.split("\n")
        summary_lines = []
        in_summary = False

        for line in lines:
            # Skip metadata and title
            if line.startswith("#") or line.startswith("---"):
                in_summary = False
                continue

            # Start collecting summary
            if line.strip() and not in_summary:
                in_summary = True

            # Collect summary lines
            if in_summary and line.strip():
                summary_lines.append(line.strip())
            elif in_summary and not line.strip() and summary_lines:
                # End of first paragraph
                break

        return " ".join(summary_lines)[:200] + "..." if summary_lines else ""

    def estimate_token_count(self, guide_name: str) -> int:
        """
        Estimate token count for a guide.

        Args:
            guide_name: Guide name

        Returns:
            Estimated token count

        Token estimates:
            - verification-protocol: 600
            - git-workflow: 1400
            - security-response: 1300
            - performance-optimization: 1700
            - container-best-practices: 2200
        """
        GUIDE_TOKENS = {
            "verification-protocol": 600,
            "git-workflow": 1400,
            "security-response": 1300,
            "performance-optimization": 1700,
            "container-best-practices": 2200,
        }

        # Normalize guide name
        guide_key = guide_name.replace(".md", "")

        return GUIDE_TOKENS.get(guide_key, 1000)  # Default 1000 tokens

    def clear_cache(self) -> None:
        """Clear guide cache."""
        self._cache.clear()

    def preload_guides(self, guide_names: List[str]) -> None:
        """
        Preload multiple guides into cache.

        Args:
            guide_names: List of guide names to preload

        Examples:
            >>> loader = GuideLoader()
            >>> loader.preload_guides(["verification-protocol", "git-workflow"])
        """
        for guide_name in guide_names:
            self.load_guide(guide_name)


# Convenience function
def load_guide(guide_name: str) -> str:
    """
    Load a guide (convenience function).

    Args:
        guide_name: Guide name

    Returns:
        Guide content

    Examples:
        >>> content = load_guide("verification-protocol")
        >>> print(f"Loaded {len(content)} characters")
    """
    loader = GuideLoader()
    return loader.load_guide(guide_name)


# Guide reference hints for commands
GUIDE_HINTS: Dict[str, List[str]] = {
    "cco-audit": [
        "verification-protocol",
        "security-response",
    ],
    "cco-audit-security": [
        "security-response",
    ],
    "cco-optimize": [
        "performance-optimization",
    ],
    "cco-optimize-docker": [
        "container-best-practices",
    ],
    "cco-fix": [
        "verification-protocol",
    ],
    "cco-test": [
        "verification-protocol",
    ],
    "cco-commit": [
        "git-workflow",
    ],
}


def get_suggested_guides(command: str) -> List[str]:
    """
    Get suggested guides for a command.

    Args:
        command: Command name

    Returns:
        List of suggested guide names

    Examples:
        >>> guides = get_suggested_guides("cco-audit-security")
        >>> print(guides)
        ['security-response']
    """
    return GUIDE_HINTS.get(command, [])

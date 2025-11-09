"""
Project Document Detector - CCO

Detects and validates project documentation files.
Priority order: README, PROJECT_DETAILS, other .md files.
"""

from pathlib import Path
from typing import Dict, List, Optional


class DocumentDetector:
    """Detects project documentation files."""

    # Priority order for documentation files
    PRIMARY_DOCS = [
        "README.md",
        "readme.md",
        "Readme.md",
        "README.MD",
        "PROJECT_DETAILS.md",
        "PROJECT.md",
        "ABOUT.md",
    ]

    def __init__(self, project_root: Path) -> None:
        """
        Initialize detector.

        Args:
            project_root: Project root directory
        """
        self.project_root = project_root

    def detect_primary_document(self) -> Optional[Path]:
        """
        Detect primary project document.

        Checks for README.md, PROJECT_DETAILS.md, etc. in priority order.

        Returns:
            Path to primary document, or None if not found
        """
        for doc_name in self.PRIMARY_DOCS:
            doc_path = self.project_root / doc_name
            if doc_path.exists() and doc_path.is_file():
                # Verify it has content (not empty)
                if doc_path.stat().st_size > 10:  # At least 10 bytes
                    return doc_path

        return None

    def find_all_markdown_docs(self, max_depth: int = 2) -> List[Dict[str, any]]:
        """
        Find all markdown documentation files.

        Args:
            max_depth: Maximum directory depth to search (default 2)

        Returns:
            List of documents with metadata:
            [
                {
                    "path": Path,
                    "relative_path": str,
                    "size": int,
                    "name": str,
                    "likely_doc": bool  # True if looks like project doc
                }
            ]
        """
        docs = []

        # Search for .md files
        for md_file in self.project_root.rglob("*.md"):
            # Skip if too deep
            try:
                relative = md_file.relative_to(self.project_root)
                depth = len(relative.parts) - 1

                if depth > max_depth:
                    continue

                # Skip common non-doc directories
                if self._should_skip_path(relative):
                    continue

                # Get file info
                size = md_file.stat().st_size

                # Skip very small or very large files
                if size < 10 or size > 100_000:  # 10 bytes to 100KB
                    continue

                docs.append(
                    {
                        "path": md_file,
                        "relative_path": str(relative),
                        "size": size,
                        "name": md_file.name,
                        "likely_doc": self._is_likely_project_doc(md_file.name),
                    },
                )

            except ValueError:
                # Skip files outside project root
                continue

        # Sort: likely docs first, then by size (larger first)
        docs.sort(key=lambda d: (not d["likely_doc"], -d["size"]))

        return docs

    def _should_skip_path(self, relative_path: Path) -> bool:
        """Check if path should be skipped."""
        skip_dirs = {
            "node_modules",
            ".git",
            ".venv",
            "venv",
            "env",
            "__pycache__",
            ".pytest_cache",
            "dist",
            "build",
            ".next",
            ".nuxt",
            "coverage",
        }

        # Check if any part of path is in skip list
        for part in relative_path.parts:
            if part in skip_dirs or part.startswith("."):
                return True

        return False

    def _is_likely_project_doc(self, filename: str) -> bool:
        """Check if filename suggests it's a project document."""
        filename_lower = filename.lower()

        doc_indicators = [
            "readme",
            "project",
            "about",
            "overview",
            "introduction",
            "getting-started",
            "gettingstarted",
            "guide",
        ]

        return any(indicator in filename_lower for indicator in doc_indicators)

    def extract_project_summary(self, doc_path: Path, max_chars: int = 500) -> str:
        """
        Extract first meaningful content from document.

        Args:
            doc_path: Path to document
            max_chars: Maximum characters to extract

        Returns:
            First paragraph or section of document
        """
        try:
            content = doc_path.read_text(encoding="utf-8")

            # Remove markdown headers
            lines = []
            for line in content.split("\n"):
                stripped = line.strip()

                # Skip empty lines, headers, horizontal rules
                if (
                    not stripped
                    or stripped.startswith("#")
                    or stripped.startswith("---")
                    or stripped.startswith("===")
                ):
                    continue

                # Skip badges, links at start
                if stripped.startswith("[![") or stripped.startswith("[!"):
                    continue

                lines.append(stripped)

                # Stop if we have enough content
                if len(" ".join(lines)) >= max_chars:
                    break

            summary = " ".join(lines)[:max_chars]

            # Add ellipsis if truncated
            if len(content) > max_chars:
                summary += "..."

            return summary

        except Exception:
            return ""

    def validate_document_content(self, doc_path: Path) -> Dict[str, any]:
        """
        Validate if document contains useful project information.

        Returns:
            {
                "valid": bool,
                "has_title": bool,
                "has_description": bool,
                "word_count": int,
                "quality_score": float  # 0-100
            }
        """
        try:
            content = doc_path.read_text(encoding="utf-8")

            # Basic checks
            has_title = bool([line for line in content.split("\n") if line.strip().startswith("#")])

            lines = [line.strip() for line in content.split("\n") if line.strip()]
            non_header_lines = [
                line for line in lines if not line.startswith("#") and not line.startswith("---")
            ]

            has_description = len(non_header_lines) >= 3  # At least 3 lines of content
            word_count = len(content.split())

            # Calculate quality score
            quality_score = 0.0

            if has_title:
                quality_score += 30
            if has_description:
                quality_score += 30
            if word_count >= 50:
                quality_score += 20
            if word_count >= 200:
                quality_score += 20

            return {
                "valid": quality_score >= 50,
                "has_title": has_title,
                "has_description": has_description,
                "word_count": word_count,
                "quality_score": quality_score,
            }

        except Exception:
            return {
                "valid": False,
                "has_title": False,
                "has_description": False,
                "word_count": 0,
                "quality_score": 0.0,
            }

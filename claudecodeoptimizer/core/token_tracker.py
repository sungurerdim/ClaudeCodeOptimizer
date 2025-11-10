"""
Token usage tracking and reporting for CCO commands.

This module provides utilities to track and report token usage
during command execution, supporting progressive disclosure optimization.
"""

**STATUS**: ⚠️ NOT CURRENTLY INTEGRATED
This module is fully implemented but not yet integrated into the codebase.
Future integration planned for token usage optimization and tracking.

import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class TokenTracker:
    """Track token usage for CCO commands with progressive disclosure."""

    # Approximate token estimates for core documents
    DOCUMENT_ESTIMATES = {
        "CLAUDE.md": 3262,
        "PRINCIPLES.md": 1311,
        "~/.cco/knowledge/guides/verification-protocol.md": 644,
        "~/.cco/knowledge/guides/git-workflow.md": 2176,
        "~/.cco/knowledge/guides/security-response.md": 1631,
        "~/.cco/knowledge/guides/performance-optimization.md": 2093,
        "~/.cco/knowledge/guides/container-best-practices.md": 2629,
        "~/.cco/knowledge/principles/code-quality.md": 1200,
        "~/.cco/knowledge/principles/security.md": 1450,
        "~/.cco/knowledge/principles/testing.md": 890,
        "~/.cco/knowledge/principles/architecture.md": 1100,
        "~/.cco/knowledge/principles/performance.md": 780,
        "~/.cco/knowledge/principles/operations.md": 950,
        "~/.cco/knowledge/principles/git-workflow.md": 670,
        "~/.cco/knowledge/principles/api-design.md": 450,
    }

    # Claude Code token budget
    TOTAL_BUDGET = 200000

    def __init__(self, project_root: Optional[Path] = None) -> None:
        """
        Initialize token tracker.

        Args:
            project_root: Project root directory (defaults to current directory)
        """
        self.project_root = project_root or Path.cwd()
        self.loaded_documents: List[Tuple[str, int]] = []
        self.total_tokens = 0

    def load_document(self, doc_path: str, calculate: bool = False) -> int:
        """
        Track loading of a document and return token estimate.

        Args:
            doc_path: Relative path to document
            calculate: If True, calculate tokens from file; if False, use estimate

        Returns:
            Estimated token count for the document
        """
        if calculate:
            full_path = self.project_root / doc_path
            if full_path.exists():
                content = full_path.read_text(encoding="utf-8")
                tokens = len(content) // 4  # Rough estimate: ~4 chars/token
            else:
                tokens = 0
        else:
            tokens = self.DOCUMENT_ESTIMATES.get(doc_path, 1000)  # Default to 1000 if unknown

        self.loaded_documents.append((doc_path, tokens))
        self.total_tokens += tokens
        return tokens

    def print_loading_status(self, doc_path: str, tokens: int) -> None:
        """
        Print document loading status.

        Args:
            doc_path: Document path
            tokens: Token count
        """
        print(f"✓ Loaded {doc_path} (~{tokens:,} tokens)")

    def print_summary(self) -> None:
        """Print comprehensive token usage summary."""
        if not self.loaded_documents:
            print("No documents loaded.")
            return

        print("\n" + "=" * 60)
        print("TOKEN USAGE REPORT")
        print("=" * 60)

        print(f"\nDocuments Loaded: {len(self.loaded_documents)}")
        for doc, tokens in self.loaded_documents:
            print(f"  • {doc:40s} ~{tokens:>6,} tokens")

        budget_remaining = self.TOTAL_BUDGET - self.total_tokens
        budget_used_pct = (self.total_tokens / self.TOTAL_BUDGET) * 100

        print(f"\n{'─' * 60}")
        print(f"Total Context Used:           ~{self.total_tokens:>7,} tokens")
        print(f"Budget Remaining:             ~{budget_remaining:>7,} tokens")
        print(f"Budget Utilization:            {budget_used_pct:>6.1f}%")

        print("\nToken Efficiency:")
        print("  Progressive Disclosure:       ✓ Enabled")
        print("  On-Demand Loading:            ✓ Category-specific guides")

        # Calculate reduction factor vs loading all docs
        all_docs_tokens = sum(self.DOCUMENT_ESTIMATES.values())
        reduction_factor = all_docs_tokens / max(1, self.total_tokens)
        print(f"  Reduction Factor:             ~{reduction_factor:.1f}x (vs loading all docs)")

        print("=" * 60 + "\n")

    def get_recommendations(self) -> List[str]:
        """
        Get recommendations based on token usage.

        Returns:
            List of recommendations
        """
        recommendations = []

        budget_used_pct = (self.total_tokens / self.TOTAL_BUDGET) * 100

        if budget_used_pct > 50:
            recommendations.append(
                "⚠️ Token usage >50% - Consider using more specific queries "
                "or breaking into smaller tasks"
            )

        if budget_used_pct > 75:
            recommendations.append(
                "🚨 Token usage >75% - CRITICAL: Reduce context or use "
                "more aggressive progressive disclosure"
            )

        # Check for redundant document loading
        doc_names = [doc for doc, _ in self.loaded_documents]
        if len(doc_names) != len(set(doc_names)):
            recommendations.append(
                "⚠️ Duplicate documents loaded - Optimize to load each document only once"
            )

        if not recommendations:
            recommendations.append("✓ Token usage within optimal range")

        return recommendations

    def export_metrics(self, output_path: Optional[Path] = None) -> Dict:
        """
        Export metrics to JSON.

        Args:
            output_path: Optional path to save JSON file

        Returns:
            Metrics dictionary
        """
        metrics = {
            "total_tokens": self.total_tokens,
            "budget_remaining": self.TOTAL_BUDGET - self.total_tokens,
            "budget_utilization_pct": (self.total_tokens / self.TOTAL_BUDGET) * 100,
            "documents_loaded": [
                {"path": doc, "tokens": tokens} for doc, tokens in self.loaded_documents
            ],
            "recommendations": self.get_recommendations(),
        }

        if output_path:
            output_path.write_text(json.dumps(metrics, indent=2))

        return metrics


# Convenience functions for quick use in commands


def track_core_documents(project_root: Optional[Path] = None) -> TokenTracker:
    """
    Track loading of core CCO documents (CLAUDE.md, PRINCIPLES.md).

    Args:
        project_root: Project root directory

    Returns:
        TokenTracker instance with core documents loaded
    """
    tracker = TokenTracker(project_root)

    print("📚 Loading CCO Context...\n")

    # Load core documents
    for doc in ["CLAUDE.md", "PRINCIPLES.md"]:
        tokens = tracker.load_document(doc, calculate=True)
        tracker.print_loading_status(doc, tokens)

    print(f"\n📊 Core context loaded: ~{tracker.total_tokens:,} tokens")
    print(
        f"   Budget remaining: ~{tracker.TOTAL_BUDGET - tracker.total_tokens:,} tokens (200K total)\n"
    )

    return tracker


def track_category_documents(
    categories: List[str], project_root: Optional[Path] = None
) -> TokenTracker:
    """
    Track loading of category-specific documents.

    Args:
        categories: List of categories ('security', 'testing', etc.)
        project_root: Project root directory

    Returns:
        TokenTracker instance with category documents loaded
    """
    tracker = track_core_documents(project_root)

    # Map categories to document paths
    category_docs = {
        "security": [
            "~/.cco/knowledge/guides/security-response.md",
            "~/.cco/knowledge/principles/security.md",
        ],
        "testing": ["~/.cco/knowledge/principles/testing.md"],
        "code_quality": [
            "~/.cco/knowledge/guides/verification-protocol.md",
            "~/.cco/knowledge/principles/code-quality.md",
        ],
        "performance": [
            "~/.cco/knowledge/guides/performance-optimization.md",
            "~/.cco/knowledge/principles/performance.md",
        ],
        "operations": [
            "~/.cco/knowledge/guides/container-best-practices.md",
            "~/.cco/knowledge/principles/operations.md",
        ],
        "architecture": ["~/.cco/knowledge/principles/architecture.md"],
        "git": [
            "~/.cco/knowledge/guides/git-workflow.md",
            "~/.cco/knowledge/principles/git-workflow.md",
        ],
    }

    print(f"📖 Loading category-specific guides: {', '.join(categories)}\n")

    for category in categories:
        docs = category_docs.get(category, [])
        for doc in docs:
            tokens = tracker.load_document(doc, calculate=False)
            tracker.print_loading_status(doc, tokens)

    print(f"\n📊 Total context: ~{tracker.total_tokens:,} tokens")
    print(f"   Budget remaining: ~{tracker.TOTAL_BUDGET - tracker.total_tokens:,} tokens\n")

    return tracker


if __name__ == "__main__":
    # Example usage
    print("Token Tracker Example\n")
    print("=" * 60)

    # Track core documents only
    print("\n1. Core Documents Only:")
    print("-" * 60)
    tracker1 = track_core_documents()

    # Track with security category
    print("\n2. Core + Security Documents:")
    print("-" * 60)
    tracker2 = track_category_documents(["security", "testing"])
    tracker2.print_summary()

    # Get recommendations
    print("\n3. Recommendations:")
    print("-" * 60)
    for rec in tracker2.get_recommendations():
        print(f"  {rec}")

"""
CCO Interactive Wizard

Production-ready wizard for CCO initialization.
No external dependencies - pure stdlib only.

Components:
- cli.py: Main wizard flow (5 phases)
- questions.py: 58 questions across 9 categories
- checkpoints.py: Confirmation/preview screens
- renderer.py: CLI rendering utilities

Usage:
    python -m wizard.cli
    python -m wizard.cli --dry-run
    python -m wizard.cli --project /path/to/project
"""

from .. import __version__

__all__ = ["CCOWizard", "QUESTIONS"]

from .cli import CCOWizard
from .questions import QUESTIONS

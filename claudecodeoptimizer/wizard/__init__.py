"""
CCO Interactive Wizard

Production-ready wizard for CCO initialization.
No external dependencies - pure stdlib only.

Components:
- orchestrator.py: Unified wizard flow (Interactive & Quick modes)
- decision_tree.py: Decision points across tiers
- checkpoints.py: Confirmation/preview screens
- renderer.py: CLI rendering utilities

Usage:
    from claudecodeoptimizer.wizard import CCOWizard
    wizard = CCOWizard(project_root, mode="quick")
    result = wizard.run()
"""

from .. import __version__

__all__ = ["CCOWizard"]

from .orchestrator import CCOWizard

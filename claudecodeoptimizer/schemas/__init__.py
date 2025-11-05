"""
CCO - Universal Preference Schemas

100% project-independent data structures for capturing user preferences
and project characteristics. All preferences are generic; specialization
happens during template rendering.

Design Principle:
- ZERO hardcoded project values
- ZERO language-specific assumptions
- ZERO framework-specific logic
- Pure data structures that work for ANY project type
"""

from .. import __version__

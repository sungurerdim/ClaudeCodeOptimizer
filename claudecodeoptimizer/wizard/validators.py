"""
Validators for wizard decision tree

Provides validation functions for user selections:
- Conflict detection
- Dependency validation
- Custom business rules
"""

from typing import Any, List

from .models import Option


def validate_no_conflicts(selected: List[str], options: List[Option]) -> bool:
    """
    Ensure no conflicting project types selected.

    Args:
        selected: List of selected option values
        options: List of Option objects

    Returns:
        True if no conflicts

    Raises:
        ValueError: If conflicting options are selected

    Examples:
        >>> selected = ["api_service", "web_app"]
        >>> validate_no_conflicts(selected, options)
        ValueError: Cannot select both api_service and web_app
    """
    # Build conflicts map
    conflicts_map: dict[str, list[str]] = {}
    for opt in options:
        if hasattr(opt, "conflicts_with") and opt.conflicts_with:
            conflicts_map[opt.value] = opt.conflicts_with

    # Check for conflicts
    for sel in selected:
        if sel in conflicts_map:
            conflicting = set(conflicts_map[sel]) & set(selected)
            if conflicting:
                # Find option labels for better error message
                sel_label = next((opt.label for opt in options if opt.value == sel), sel)
                conflict_labels = [
                    next((opt.label for opt in options if opt.value == c), c) for c in conflicting
                ]

                raise ValueError(
                    f"Cannot select both '{sel_label}' and {conflict_labels}: "
                    f"They are mutually exclusive."
                )

    return True


def validate_required_dependencies(selected: List[str], options: List[Option]) -> bool:
    """
    Validate that required dependencies are met.

    Args:
        selected: List of selected option values
        options: List of Option objects

    Returns:
        True if all dependencies met

    Raises:
        ValueError: If required dependencies missing

    Examples:
        >>> selected = ["microservice"]
        >>> # If microservice requires api_service
        >>> validate_required_dependencies(selected, options)
        ValueError: 'Microservice' requires 'API Service' to be selected
    """
    # Build dependencies map
    dependencies_map: dict[str, list[str]] = {}
    for opt in options:
        if hasattr(opt, "requires") and opt.requires:
            dependencies_map[opt.value] = opt.requires

    # Check dependencies
    for sel in selected:
        if sel in dependencies_map:
            required = dependencies_map[sel]
            missing = set(required) - set(selected)
            if missing:
                sel_label = next((opt.label for opt in options if opt.value == sel), sel)
                missing_labels = [
                    next((opt.label for opt in options if opt.value == m), m) for m in missing
                ]

                raise ValueError(f"'{sel_label}' requires {missing_labels} to be selected")

    return True


def validate_team_size_consistency(answers: dict[str, Any]) -> bool:
    """
    Validate that team size is consistent with other selections.

    Args:
        answers: Dict of all wizard answers

    Returns:
        True if consistent

    Raises:
        ValueError: If inconsistent

    Examples:
        >>> answers = {"team_dynamics": "solo", "git_workflow": "git-flow"}
        >>> validate_team_size_consistency(answers)
        ValueError: Git Flow is not recommended for solo developers
    """
    team = answers.get("team_dynamics")
    git_workflow = answers.get("git_workflow")

    # Solo dev with Git Flow is overkill
    if team == "solo" and git_workflow == "git-flow":
        raise ValueError(
            "Git Flow workflow is not recommended for solo developers. "
            "Consider 'Main-Only' or 'GitHub Flow' instead."
        )

    # Large org with main-only is risky
    if team == "large_org" and git_workflow == "main-only":
        raise ValueError(
            "Main-Only workflow is not recommended for large organizations. "
            "Consider 'GitHub Flow' or 'Git Flow' instead."
        )

    return True


def validate_maturity_compatibility(answers: dict[str, Any]) -> bool:
    """
    Validate that project maturity is compatible with other selections.

    Args:
        answers: Dict of all wizard answers

    Returns:
        True if compatible

    Raises:
        ValueError: If incompatible

    Examples:
        >>> answers = {"project_maturity": "prototype", "principle_strategy": "comprehensive"}
        >>> validate_maturity_compatibility(answers)
        ValueError: Comprehensive principles are not recommended for prototypes
    """
    maturity = answers.get("project_maturity")
    principle_strategy = answers.get("principle_strategy")

    # Prototype with comprehensive principles is overkill
    if maturity == "prototype" and principle_strategy == "comprehensive":
        raise ValueError(
            "Comprehensive principle strategy is not recommended for prototypes. "
            "Consider 'minimal' or 'auto' instead."
        )

    return True

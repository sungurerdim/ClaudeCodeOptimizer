"""
Template variables system for ClaudeCodeOptimizer.

Provides variable substitution in commands to eliminate hardcoded values.
Enables centralized updates across all commands.
"""

**STATUS**: ⚠️ NOT CURRENTLY INTEGRATED
This module is fully implemented but not yet integrated into the codebase.
Future integration planned for template variable substitution for file generation.

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, TypeVar

T = TypeVar("T")


@dataclass
class VariableDefinition:
    """Definition of a template variable."""

    name: str
    description: str
    default: Any
    type: str = "string"  # string, int, bool, list, path
    required: bool = False
    validation_pattern: Optional[str] = None


@dataclass
class VariableRegistry:
    """Registry of template variables."""

    # Project identification
    PROJECT_NAME: VariableDefinition = field(
        default_factory=lambda: VariableDefinition(
            name="PROJECT_NAME",
            description="Project name",
            default="my-project",
            type="string",
            required=True,
        ),
    )

    PROJECT_TYPE: VariableDefinition = field(
        default_factory=lambda: VariableDefinition(
            name="PROJECT_TYPE",
            description="Project type (api, web, ml, microservices, library, cli, etc.)",
            default="api",
            type="string",
            required=True,
        ),
    )

    PRIMARY_LANGUAGE: VariableDefinition = field(
        default_factory=lambda: VariableDefinition(
            name="PRIMARY_LANGUAGE",
            description="Primary programming language",
            default="python",
            type="string",
            required=True,
        ),
    )

    # Directory structure
    SERVICE_DIR: VariableDefinition = field(
        default_factory=lambda: VariableDefinition(
            name="SERVICE_DIR",
            description="Services directory path (relative to project root)",
            default="services",
            type="path",
        ),
    )

    SHARED_DIR: VariableDefinition = field(
        default_factory=lambda: VariableDefinition(
            name="SHARED_DIR",
            description="Shared code directory path (relative to project root)",
            default="shared",
            type="path",
        ),
    )

    TESTS_DIR: VariableDefinition = field(
        default_factory=lambda: VariableDefinition(
            name="TESTS_DIR",
            description="Tests directory path (relative to project root)",
            default="tests",
            type="path",
        ),
    )

    SRC_DIR: VariableDefinition = field(
        default_factory=lambda: VariableDefinition(
            name="SRC_DIR",
            description="Source code directory path (relative to project root)",
            default="src",
            type="path",
        ),
    )

    DOCS_DIR: VariableDefinition = field(
        default_factory=lambda: VariableDefinition(
            name="DOCS_DIR",
            description="Documentation directory path (relative to project root)",
            default="docs",
            type="path",
        ),
    )

    # Principles and configuration
    PRINCIPLES_COUNT: VariableDefinition = field(
        default_factory=lambda: VariableDefinition(
            name="PRINCIPLES_COUNT",
            description="Number of active principles",
            default=0,
            type="int",
        ),
    )

    PRINCIPLES_STRATEGY: VariableDefinition = field(
        default_factory=lambda: VariableDefinition(
            name="PRINCIPLES_STRATEGY",
            description="Principle selection strategy (auto, minimal, comprehensive)",
            default="auto",
            type="string",
        ),
    )

    # Team and project characteristics
    TEAM_SIZE: VariableDefinition = field(
        default_factory=lambda: VariableDefinition(
            name="TEAM_SIZE",
            description="Team size (solo, small, medium, large)",
            default="solo",
            type="string",
        ),
    )

    SERVICES_COUNT: VariableDefinition = field(
        default_factory=lambda: VariableDefinition(
            name="SERVICES_COUNT",
            description="Number of services (for microservices)",
            default=1,
            type="int",
        ),
    )

    # Tools and frameworks
    FORMATTER: VariableDefinition = field(
        default_factory=lambda: VariableDefinition(
            name="FORMATTER",
            description="Code formatter tool (black, prettier, gofmt, rustfmt, etc.)",
            default="auto-detect",
            type="string",
        ),
    )

    LINTER: VariableDefinition = field(
        default_factory=lambda: VariableDefinition(
            name="LINTER",
            description="Linter tool (ruff, eslint, golangci-lint, clippy, etc.)",
            default="auto-detect",
            type="string",
        ),
    )

    TYPE_CHECKER: VariableDefinition = field(
        default_factory=lambda: VariableDefinition(
            name="TYPE_CHECKER",
            description="Type checker tool (mypy, pyright, tsc, etc.)",
            default="auto-detect",
            type="string",
        ),
    )

    TEST_FRAMEWORK: VariableDefinition = field(
        default_factory=lambda: VariableDefinition(
            name="TEST_FRAMEWORK",
            description="Test framework (pytest, jest, go test, cargo test, etc.)",
            default="auto-detect",
            type="string",
        ),
    )

    # Characteristics flags
    PRIVACY_CRITICAL: VariableDefinition = field(
        default_factory=lambda: VariableDefinition(
            name="PRIVACY_CRITICAL",
            description="Handles PII/sensitive data",
            default=False,
            type="bool",
        ),
    )

    SECURITY_CRITICAL: VariableDefinition = field(
        default_factory=lambda: VariableDefinition(
            name="SECURITY_CRITICAL",
            description="Requires high security standards",
            default=False,
            type="bool",
        ),
    )

    PERFORMANCE_CRITICAL: VariableDefinition = field(
        default_factory=lambda: VariableDefinition(
            name="PERFORMANCE_CRITICAL",
            description="Performance is critical",
            default=False,
            type="bool",
        ),
    )


class VariableSubstitutionEngine:
    """Engine for substituting template variables in text."""

    # Variable pattern: ${VAR_NAME} or ${VAR_NAME:default_value}
    VARIABLE_PATTERN = re.compile(r"\$\{([A-Z_][A-Z0-9_]*?)(?::([^}]+))?\}")

    def __init__(self, variables: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize substitution engine.

        Args:
            variables: Dictionary of variable name -> value
        """
        self.variables = variables or {}
        self.registry = VariableRegistry()

    def set_variable(self, name: str, value: object) -> None:
        """Set a variable value."""
        self.variables[name] = value

    def set_variables(self, variables: Dict[str, object]) -> None:
        """Set multiple variable values."""
        self.variables.update(variables)

    def get_variable(self, name: str, default: object | None = None) -> object | None:
        """Get a variable value."""
        return self.variables.get(name, default)

    def substitute(self, text: str, strict: bool = False) -> str:
        """
        Substitute variables in text.

        Args:
            text: Text with variables (e.g., "Hello ${PROJECT_NAME}")
            strict: If True, raise error on undefined variables

        Returns:
            Text with variables replaced

        Raises:
            ValueError: If strict=True and variable is undefined
        """

        def replace_variable(match: re.Match) -> str:  # type: ignore[type-arg]
            var_name = match.group(1)
            default_value = match.group(2)

            # Check if variable is defined
            if var_name in self.variables:
                value = self.variables[var_name]
            elif default_value is not None:
                value = default_value
            elif hasattr(self.registry, var_name):
                # Use registry default
                var_def = getattr(self.registry, var_name)
                value = var_def.default
            else:
                if strict:
                    raise ValueError(f"Undefined variable: {var_name}")
                # Leave unchanged if not strict
                return match.group(0)

            # Convert value to string
            return str(value)

        return self.VARIABLE_PATTERN.sub(replace_variable, text)

    def extract_variables(self, text: str) -> Set[str]:
        """
        Extract all variable names from text.

        Args:
            text: Text with variables

        Returns:
            Set of variable names
        """
        return {match.group(1) for match in self.VARIABLE_PATTERN.finditer(text)}

    def validate_variables(self, variables: Dict[str, Any]) -> List[str]:
        """
        Validate variable values against registry definitions.

        Args:
            variables: Dictionary of variable name -> value

        Returns:
            List of validation errors (empty if all valid)
        """
        errors = []

        for name, value in variables.items():
            # Check if variable exists in registry
            if not hasattr(self.registry, name):
                errors.append(f"Unknown variable: {name}")
                continue

            var_def = getattr(self.registry, name)

            # Type validation
            if var_def.type == "int":
                if not isinstance(value, int):
                    try:
                        int(value)
                    except (ValueError, TypeError):
                        errors.append(f"{name}: Expected int, got {type(value).__name__}")

            elif var_def.type == "bool":
                if not isinstance(value, bool):
                    if str(value).lower() not in ["true", "false", "yes", "no", "1", "0"]:
                        errors.append(f"{name}: Expected bool, got {value}")

            elif var_def.type == "string":
                if not isinstance(value, str):
                    errors.append(f"{name}: Expected string, got {type(value).__name__}")

            elif var_def.type == "path":
                # Validate path format (no absolute paths with hardcoded values)
                if isinstance(value, str) and value.startswith("/"):
                    errors.append(f"{name}: Absolute paths not allowed, use relative paths")

            # Pattern validation
            if var_def.validation_pattern and isinstance(value, str):
                if not re.match(var_def.validation_pattern, value):
                    errors.append(f"{name}: Does not match pattern {var_def.validation_pattern}")

        return errors

    def get_all_definitions(self) -> Dict[str, VariableDefinition]:
        """Get all variable definitions from registry."""
        return {
            name: getattr(self.registry, name)
            for name in dir(self.registry)
            if not name.startswith("_")
            and isinstance(getattr(self.registry, name), VariableDefinition)
        }

    def create_from_analysis(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create variable dictionary from project analysis.

        Args:
            analysis: Project analysis dictionary

        Returns:
            Dictionary of variables
        """
        variables = {
            "PROJECT_NAME": analysis.get("name", "my-project"),
            "PROJECT_TYPE": analysis.get("type", "unknown"),
            "PRIMARY_LANGUAGE": analysis.get("language", "unknown"),
            "TEAM_SIZE": analysis.get("team_size", "solo"),
            "SERVICES_COUNT": len(analysis.get("services", [])),
            "PRINCIPLES_COUNT": len(analysis.get("active_principles", [])),
            "PRINCIPLES_STRATEGY": analysis.get("principles_strategy", "auto"),
            "PRIVACY_CRITICAL": analysis.get("privacy_critical", False),
            "SECURITY_CRITICAL": analysis.get("security_critical", False),
            "PERFORMANCE_CRITICAL": analysis.get("performance_critical", False),
        }

        # Add directory paths if detected
        directories = analysis.get("directories", {})
        if "services" in directories:
            variables["SERVICE_DIR"] = directories["services"]
        if "shared" in directories:
            variables["SHARED_DIR"] = directories["shared"]
        if "tests" in directories:
            variables["TESTS_DIR"] = directories["tests"]
        if "src" in directories:
            variables["SRC_DIR"] = directories["src"]
        if "docs" in directories:
            variables["DOCS_DIR"] = directories["docs"]

        # Add detected tools
        tools = analysis.get("tools", {})
        if "formatter" in tools:
            variables["FORMATTER"] = tools["formatter"]
        if "linter" in tools:
            variables["LINTER"] = tools["linter"]
        if "type_checker" in tools:
            variables["TYPE_CHECKER"] = tools["type_checker"]
        if "test_framework" in tools:
            variables["TEST_FRAMEWORK"] = tools["test_framework"]

        return variables


def substitute_in_file(
    file_path: Path,
    variables: Dict[str, Any],
    output_path: Optional[Path] = None,
) -> str:
    """
    Substitute variables in a file.

    Args:
        file_path: Path to file with variables
        variables: Dictionary of variable name -> value
        output_path: Optional output path (if None, returns string)

    Returns:
        File content with variables substituted
    """
    engine = VariableSubstitutionEngine(variables)

    content = file_path.read_text(encoding="utf-8")
    substituted = engine.substitute(content)

    if output_path:
        output_path.write_text(substituted, encoding="utf-8")

    return substituted


__all__ = [
    "VariableDefinition",
    "VariableRegistry",
    "VariableSubstitutionEngine",
    "substitute_in_file",
]

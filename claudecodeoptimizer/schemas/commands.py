"""
Universal Command Schema - CCO

Command metadata and selection logic - 100% generic.
No project-specific data; all specialization via tagging and templates.
"""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field

from .. import __version__ as cco_version


class CommandMetadata(BaseModel):
    """
    Universal command metadata - describes command without project specifics

    Tags and relevance criteria allow dynamic recommendation without hardcoding.
    """

    command_id: str = Field(
        ..., description="Command identifier (e.g., 'cco-audit-code')"
    )
    display_name: str = Field(..., description="Human-readable name")
    category: str = Field(
        ...,
        description="Command category (bootstrap, audit, generate, setup, refactor, etc.)",
    )

    description_short: str = Field(
        ..., max_length=80, description="One-line description"
    )
    description_long: str = Field(..., description="Detailed explanation")

    # Universal recommendation factors (no hardcoded project names)
    relevance_tags: List[str] = Field(
        default=[],
        description="Generic tags for relevance (python, code-quality, testing, security, etc.)",
    )

    applicable_project_types: List[str] = Field(
        default=["all"],
        description="Project types where this is relevant (api, backend, ml, etc.)",
    )

    applicable_team_sizes: List[str] = Field(
        default=["all"],
        description="Team sizes where this is useful (solo, small-2-5, medium-5-10, etc.)",
    )

    applicable_maturity_stages: List[str] = Field(
        default=["all"],
        description="Project stages where this applies (greenfield, active-dev, etc.)",
    )

    # Dependencies (generic references)
    required_tools: List[str] = Field(
        default=[],
        description="External tools required (black, ruff, docker, etc.)",
    )

    required_commands: List[str] = Field(
        default=[],
        description="Other CCO commands this depends on",
    )

    # Flags
    is_core: bool = Field(False, description="Always recommended (core functionality)")
    is_experimental: bool = Field(False, description="Experimental/beta feature")

    # Usage tracking (for learning)
    usage_frequency: int = Field(0, description="Times this command has been invoked")
    success_rate: Optional[float] = Field(
        None, ge=0.0, le=1.0, description="Success rate"
    )
    last_used: Optional[str] = Field(None, description="Last invocation timestamp")

    class Config:
        json_schema_extra = {
            "example": {
                "command_id": "cco-audit-code",
                "display_name": "Code Quality Audit",
                "category": "audit",
                "description_short": "Audit code for quality issues (DRY, fail-fast, types)",
                "description_long": "Comprehensive code quality audit...",
                "relevance_tags": ["code-quality", "linting", "type-safety"],
                "applicable_project_types": ["all"],
                "applicable_team_sizes": ["all"],
                "is_core": True,
            },
        }


class CommandSelection(BaseModel):
    """User's command selection - tracks what was chosen and why"""

    selected_commands: List[str] = Field(..., description="Commands user selected")
    recommended_commands: List[str] = Field(..., description="Commands AI recommended")
    deselected_recommended: List[str] = Field(
        default=[],
        description="Recommended commands user rejected (for learning)",
    )
    custom_additions: List[str] = Field(
        default=[],
        description="Non-recommended commands user added",
    )

    # Metadata
    selection_method: str = Field(
        ...,
        description="How selection was made (wizard, fast-track, manual, etc.)",
    )
    selected_at: str = Field(default_factory=lambda: datetime.now().isoformat())


class CommandRegistry(BaseModel):
    """
    Master command registry - universal catalog of all available commands

    Contains NO project-specific data; all commands are generic templates.
    """

    commands: List[CommandMetadata] = Field(default=[])
    version: str = Field(cco_version, description="Registry version")
    last_updated: str = Field(default_factory=lambda: datetime.now().isoformat())

    def get_by_id(self, command_id: str) -> Optional[CommandMetadata]:
        """Retrieve command metadata by ID"""
        return next(
            (cmd for cmd in self.commands if cmd.command_id == command_id), None
        )

    def get_by_category(self, category: str) -> List[CommandMetadata]:
        """Retrieve all commands in a category"""
        return [cmd for cmd in self.commands if cmd.category == category]

    def get_by_tag(self, tag: str) -> List[CommandMetadata]:
        """Retrieve all commands with a specific tag"""
        return [cmd for cmd in self.commands if tag in cmd.relevance_tags]

    def filter_by_project_type(self, project_types: List[str]) -> List[CommandMetadata]:
        """Filter commands relevant to project types"""
        return [
            cmd
            for cmd in self.commands
            if "all" in cmd.applicable_project_types
            or any(pt in cmd.applicable_project_types for pt in project_types)
        ]

    def filter_by_team_size(self, team_size: str) -> List[CommandMetadata]:
        """Filter commands relevant to team size"""
        return [
            cmd
            for cmd in self.commands
            if "all" in cmd.applicable_team_sizes
            or team_size in cmd.applicable_team_sizes
        ]

    class Config:
        json_schema_extra = {
            "description": "Universal command registry - works for any project",
        }

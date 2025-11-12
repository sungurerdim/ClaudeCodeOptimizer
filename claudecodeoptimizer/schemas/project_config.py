"""
Project Configuration Schema

Defines the structure for .claude/project.json
Created by /cco-init and read by all commands for dynamic principle loading.
"""

from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class DetectionInfo(BaseModel):
    """Project detection results from wizard."""
    project_type: str = Field(..., description="Project type (api, cli, library, web, mobile, etc.)")
    languages: List[str] = Field(default_factory=list, description="Programming languages detected")
    frameworks: List[str] = Field(default_factory=list, description="Frameworks detected")
    team_size: str = Field(default="small", description="Team size (solo, small, medium, large)")
    maturity: str = Field(default="development", description="Project maturity (prototype, development, production)")
    security_level: str = Field(default="standard", description="Security level (low, standard, high, critical)")
    philosophy: str = Field(default="balanced", description="Development philosophy (minimal, balanced, comprehensive)")


class CommandOverride(BaseModel):
    """Command-specific principle override."""
    principles: List[str] = Field(..., description="Principle IDs to load for this command")
    reason: Optional[str] = Field(None, description="Why these specific principles were selected")


class ProjectConfig(BaseModel):
    """Project configuration for CCO."""

    # Project metadata
    project_name: str = Field(..., description="Project name")
    project_root: str = Field(..., description="Absolute path to project root")
    initialized_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat(), description="Initialization timestamp")
    wizard_mode: str = Field(default="interactive", description="Wizard mode used (quick, interactive)")
    cco_version: str = Field(default="2.1.0", description="CCO version used for initialization")

    # Detection results
    detection: DetectionInfo = Field(..., description="Project detection results")

    # Selected principles (by category)
    selected_principles: Dict[str, List[str]] = Field(
        default_factory=dict,
        description="Selected principle IDs by category"
    )

    # Command overrides (optional - for fine-tuning)
    command_overrides: Dict[str, CommandOverride] = Field(
        default_factory=dict,
        description="Command-specific principle overrides"
    )

    # Selected components
    selected_commands: List[str] = Field(default_factory=list, description="Selected command IDs")
    selected_guides: List[str] = Field(default_factory=list, description="Selected guide paths")
    selected_skills: List[str] = Field(default_factory=list, description="Selected skill paths")
    selected_agents: List[str] = Field(default_factory=list, description="Selected agent IDs")

    # User preferences (optional)
    preferences: Dict[str, Any] = Field(
        default_factory=dict,
        description="User preferences and customizations"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "project_name": "MyFastAPIProject",
                "project_root": "/home/user/projects/my-api",
                "initialized_at": "2025-11-12T10:30:00Z",
                "wizard_mode": "interactive",
                "cco_version": "2.1.0",
                "detection": {
                    "project_type": "api",
                    "languages": ["python"],
                    "frameworks": ["fastapi"],
                    "team_size": "small",
                    "maturity": "production",
                    "security_level": "high",
                    "philosophy": "balanced"
                },
                "selected_principles": {
                    "universal": ["U001", "U002", "U003", "U004", "U005", "U006", "U007", "U008", "U009", "U010", "U011", "U012"],
                    "core": [],
                    "code_quality": ["P001", "P002", "P003"],
                    "security_privacy": ["P028", "P029", "P030"],
                    "testing": ["P041", "P042"]
                },
                "command_overrides": {
                    "cco-audit-security": {
                        "principles": ["U001", "U002", "P028", "P029", "P030"],
                        "reason": "Standard API security - core validations only"
                    }
                },
                "selected_commands": ["cco-audit", "cco-status", "cco-fix"],
                "selected_guides": ["verification-protocol.md"],
                "selected_skills": ["python/testing-pytest.md"],
                "selected_agents": []
            }
        }

    def save(self, path: Path) -> None:
        """Save config to file."""
        import json
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(self.model_dump_json(indent=2), encoding='utf-8')

    @classmethod
    def load(cls, path: Path) -> Optional['ProjectConfig']:
        """Load config from file."""
        if not path.exists():
            return None
        import json
        data = json.loads(path.read_text(encoding='utf-8'))
        return cls(**data)

    def get_all_selected_principles(self) -> List[str]:
        """Get all selected principle IDs (flattened)."""
        all_principles = []
        for category_principles in self.selected_principles.values():
            all_principles.extend(category_principles)
        return list(set(all_principles))  # Remove duplicates

    def get_principles_for_command(self, command: str) -> List[str]:
        """Get principles for a specific command."""
        # Check for command override first
        if command in self.command_overrides:
            return self.command_overrides[command].principles

        # Otherwise return all selected principles
        return self.get_all_selected_principles()

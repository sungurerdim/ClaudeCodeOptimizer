"""
Universal Recommendation Schema - CCO

AI-generated recommendations based on project analysis.
100% generic - works for any project without hardcoded assumptions.
"""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class DetectionResult(BaseModel):
    """Result from project analysis - completely generic"""

    category: str = Field(
        ...,
        description="Detection category (language, framework, tool, pattern)",
    )
    detected_value: str = Field(..., description="What was detected")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Confidence score (0.0-1.0)")
    evidence: list[str] = Field(default=[], description="Evidence (file paths, patterns found)")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "category": "language",
                "detected_value": "python",
                "confidence": 0.95,
                "evidence": ["47 .py files", "pyproject.toml present"],
            },
        }
    )


class Recommendation(BaseModel):
    """AI-generated recommendation for a preference - universal format"""

    preference_path: str = Field(
        ...,
        description="Dot-notation path to preference (e.g., 'code_quality.linting_strictness')",
    )
    recommended_value: Any = Field(..., description="Recommended value (type varies by preference)")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Recommendation confidence")
    reasoning: str = Field(..., description="Human-readable explanation")
    alternatives: list[Any] = Field(default=[], description="Other valid options")
    detection_basis: list[DetectionResult] = Field(
        default=[],
        description="Detection results that informed this recommendation",
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "preference_path": "testing.coverage_target",
                "recommended_value": "90",
                "confidence": 0.85,
                "reasoning": "Matches pytest.ini threshold (90%)",
                "alternatives": ["95", "85", "80"],
                "detection_basis": [],
            },
        }
    )


class RecommendationBundle(BaseModel):
    """Complete recommendation set - organized by category"""

    project_identity_recs: list[Recommendation] = Field(default=[])
    development_style_recs: list[Recommendation] = Field(default=[])
    code_quality_recs: list[Recommendation] = Field(default=[])
    documentation_recs: list[Recommendation] = Field(default=[])
    testing_recs: list[Recommendation] = Field(default=[])
    security_recs: list[Recommendation] = Field(default=[])
    performance_recs: list[Recommendation] = Field(default=[])
    collaboration_recs: list[Recommendation] = Field(default=[])
    devops_recs: list[Recommendation] = Field(default=[])

    # Metadata
    analysis_duration_ms: int = Field(0, description="Time taken to generate recommendations")
    total_confidence: float = Field(0.0, ge=0.0, le=1.0, description="Average confidence")
    generated_at: str = Field(default_factory=lambda: datetime.now().isoformat())

    def calculate_total_confidence(self) -> float:
        """Calculate average confidence across all recommendations"""
        all_recs: list[Recommendation] = (
            self.project_identity_recs
            + self.development_style_recs
            + self.code_quality_recs
            + self.documentation_recs
            + self.testing_recs
            + self.security_recs
            + self.performance_recs
            + self.collaboration_recs
            + self.devops_recs
        )

        if not all_recs:
            return 0.0

        return sum(r.confidence for r in all_recs) / len(all_recs)


class ProjectAnalysisReport(BaseModel):
    """Complete project analysis output - universal format"""

    # Detection results by category
    languages: list[DetectionResult] = Field(default=[])
    frameworks: list[DetectionResult] = Field(default=[])
    project_types: list[DetectionResult] = Field(default=[])
    tools: list[DetectionResult] = Field(default=[])

    # Codebase patterns (language-agnostic metrics)
    codebase_patterns: dict = Field(
        default_factory=dict,
        description="Metrics like avg_function_length, has_type_hints, etc.",
    )

    # Metadata
    project_root: str = Field(..., description="Analyzed project path")
    analyzed_at: str = Field(default_factory=lambda: datetime.now().isoformat())
    analysis_duration_ms: int = Field(0, description="Time taken for analysis")

    model_config = ConfigDict(
        json_schema_extra={
            "description": "Universal project analysis report - works for any language/framework",
        }
    )

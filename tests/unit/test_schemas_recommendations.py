"""
Unit tests for Recommendation Schemas

Tests DetectionResult, Recommendation, RecommendationBundle, and ProjectAnalysisReport models.
Ensures 80%+ coverage for claudecodeoptimizer/schemas/recommendations.py.

Target Coverage: 80%+
"""

from datetime import datetime

import pytest
from pydantic import ValidationError

from claudecodeoptimizer.schemas.recommendations import (
    DetectionResult,
    ProjectAnalysisReport,
    Recommendation,
    RecommendationBundle,
)


class TestDetectionResult:
    """Test DetectionResult model"""

    def test_create_valid(self) -> None:
        """Test creating DetectionResult with valid data"""
        result = DetectionResult(
            category="language",
            detected_value="python",
            confidence=0.95,
            evidence=["47 .py files", "pyproject.toml present"],
        )

        assert result.category == "language"
        assert result.detected_value == "python"
        assert result.confidence == 0.95
        assert len(result.evidence) == 2
        assert "47 .py files" in result.evidence

    def test_create_minimal(self) -> None:
        """Test creating DetectionResult with minimal required fields"""
        result = DetectionResult(
            category="framework",
            detected_value="fastapi",
            confidence=0.8,
        )

        assert result.category == "framework"
        assert result.detected_value == "fastapi"
        assert result.confidence == 0.8
        assert result.evidence == []

    def test_validation_confidence_range_valid(self) -> None:
        """Test confidence validation - valid range 0.0-1.0"""
        # Lower bound
        result = DetectionResult(
            category="tool",
            detected_value="pytest",
            confidence=0.0,
        )
        assert result.confidence == 0.0

        # Upper bound
        result = DetectionResult(
            category="tool",
            detected_value="pytest",
            confidence=1.0,
        )
        assert result.confidence == 1.0

        # Middle value
        result = DetectionResult(
            category="tool",
            detected_value="pytest",
            confidence=0.5,
        )
        assert result.confidence == 0.5

    def test_validation_confidence_below_zero(self) -> None:
        """Test confidence validation - reject below 0.0"""
        with pytest.raises(ValidationError) as exc_info:
            DetectionResult(
                category="tool",
                detected_value="pytest",
                confidence=-0.1,
            )
        assert "greater than or equal to 0" in str(exc_info.value).lower()

    def test_validation_confidence_above_one(self) -> None:
        """Test confidence validation - reject above 1.0"""
        with pytest.raises(ValidationError) as exc_info:
            DetectionResult(
                category="tool",
                detected_value="pytest",
                confidence=1.1,
            )
        assert "less than or equal to 1" in str(exc_info.value).lower()

    def test_missing_required_fields(self) -> None:
        """Test that missing required fields raises validation error"""
        with pytest.raises(ValidationError):
            DetectionResult()

        with pytest.raises(ValidationError):
            DetectionResult(category="language")

        with pytest.raises(ValidationError):
            DetectionResult(category="language", detected_value="python")

    def test_json_serialization(self) -> None:
        """Test model serialization to dict and JSON"""
        result = DetectionResult(
            category="language",
            detected_value="python",
            confidence=0.95,
            evidence=["47 .py files"],
        )

        # Test model_dump
        data = result.model_dump()
        assert data["category"] == "language"
        assert data["detected_value"] == "python"
        assert data["confidence"] == 0.95
        assert data["evidence"] == ["47 .py files"]

        # Test model_dump_json
        json_str = result.model_dump_json()
        assert "language" in json_str
        assert "python" in json_str
        assert "0.95" in json_str

    def test_json_deserialization(self) -> None:
        """Test model deserialization from dict and JSON"""
        data = {
            "category": "framework",
            "detected_value": "fastapi",
            "confidence": 0.88,
            "evidence": ["from fastapi import FastAPI"],
        }

        # From dict
        result = DetectionResult(**data)
        assert result.category == "framework"
        assert result.detected_value == "fastapi"
        assert result.confidence == 0.88

        # From JSON
        json_str = (
            '{"category": "tool", "detected_value": "pytest", "confidence": 0.92, "evidence": []}'
        )
        result = DetectionResult.model_validate_json(json_str)
        assert result.category == "tool"
        assert result.detected_value == "pytest"
        assert result.confidence == 0.92

    def test_evidence_list_independence(self) -> None:
        """Test that evidence lists are independent instances"""
        result1 = DetectionResult(
            category="language",
            detected_value="python",
            confidence=0.9,
        )
        result2 = DetectionResult(
            category="language",
            detected_value="javascript",
            confidence=0.8,
        )

        result1.evidence.append("file1.py")
        assert result2.evidence == []


class TestRecommendation:
    """Test Recommendation model"""

    def test_create_valid(self) -> None:
        """Test creating Recommendation with valid data"""
        rec = Recommendation(
            preference_path="testing.coverage_target",
            recommended_value="90",
            confidence=0.85,
            reasoning="Matches pytest.ini threshold (90%)",
            alternatives=["95", "85", "80"],
            detection_basis=[
                DetectionResult(
                    category="tool",
                    detected_value="pytest",
                    confidence=0.95,
                    evidence=["pytest.ini found"],
                ),
            ],
        )

        assert rec.preference_path == "testing.coverage_target"
        assert rec.recommended_value == "90"
        assert rec.confidence == 0.85
        assert rec.reasoning == "Matches pytest.ini threshold (90%)"
        assert len(rec.alternatives) == 3
        assert len(rec.detection_basis) == 1

    def test_create_minimal(self) -> None:
        """Test creating Recommendation with minimal required fields"""
        rec = Recommendation(
            preference_path="code_quality.linting_strictness",
            recommended_value="strict",
            confidence=0.8,
            reasoning="Project uses ruff with strict settings",
        )

        assert rec.preference_path == "code_quality.linting_strictness"
        assert rec.recommended_value == "strict"
        assert rec.confidence == 0.8
        assert rec.alternatives == []
        assert rec.detection_basis == []

    def test_validation_confidence_range_valid(self) -> None:
        """Test confidence validation - valid range 0.0-1.0"""
        rec = Recommendation(
            preference_path="test.path",
            recommended_value="value",
            confidence=0.0,
            reasoning="Test",
        )
        assert rec.confidence == 0.0

        rec = Recommendation(
            preference_path="test.path",
            recommended_value="value",
            confidence=1.0,
            reasoning="Test",
        )
        assert rec.confidence == 1.0

    def test_validation_confidence_invalid(self) -> None:
        """Test confidence validation - reject invalid values"""
        with pytest.raises(ValidationError):
            Recommendation(
                preference_path="test.path",
                recommended_value="value",
                confidence=-0.1,
                reasoning="Test",
            )

        with pytest.raises(ValidationError):
            Recommendation(
                preference_path="test.path",
                recommended_value="value",
                confidence=1.5,
                reasoning="Test",
            )

    def test_recommended_value_any_type(self) -> None:
        """Test recommended_value accepts various types"""
        # String
        rec = Recommendation(
            preference_path="test.path",
            recommended_value="string_value",
            confidence=0.8,
            reasoning="Test",
        )
        assert rec.recommended_value == "string_value"

        # Integer
        rec = Recommendation(
            preference_path="test.path",
            recommended_value=42,
            confidence=0.8,
            reasoning="Test",
        )
        assert rec.recommended_value == 42

        # Boolean
        rec = Recommendation(
            preference_path="test.path",
            recommended_value=True,
            confidence=0.8,
            reasoning="Test",
        )
        assert rec.recommended_value is True

        # List
        rec = Recommendation(
            preference_path="test.path",
            recommended_value=["a", "b", "c"],
            confidence=0.8,
            reasoning="Test",
        )
        assert rec.recommended_value == ["a", "b", "c"]

        # Dict
        rec = Recommendation(
            preference_path="test.path",
            recommended_value={"key": "value"},
            confidence=0.8,
            reasoning="Test",
        )
        assert rec.recommended_value == {"key": "value"}

    def test_missing_required_fields(self) -> None:
        """Test that missing required fields raises validation error"""
        with pytest.raises(ValidationError):
            Recommendation()

        with pytest.raises(ValidationError):
            Recommendation(preference_path="test.path")

        with pytest.raises(ValidationError):
            Recommendation(
                preference_path="test.path",
                recommended_value="value",
            )

    def test_json_serialization(self) -> None:
        """Test model serialization to dict and JSON"""
        rec = Recommendation(
            preference_path="testing.coverage_target",
            recommended_value="90",
            confidence=0.85,
            reasoning="Matches pytest.ini",
            alternatives=["95", "80"],
        )

        data = rec.model_dump()
        assert data["preference_path"] == "testing.coverage_target"
        assert data["recommended_value"] == "90"
        assert data["confidence"] == 0.85
        assert len(data["alternatives"]) == 2

        json_str = rec.model_dump_json()
        assert "testing.coverage_target" in json_str
        assert "0.85" in json_str

    def test_json_deserialization(self) -> None:
        """Test model deserialization from dict and JSON"""
        data = {
            "preference_path": "security.stance",
            "recommended_value": "strict",
            "confidence": 0.9,
            "reasoning": "Financial domain detected",
            "alternatives": ["balanced"],
            "detection_basis": [],
        }

        rec = Recommendation(**data)
        assert rec.preference_path == "security.stance"
        assert rec.confidence == 0.9


class TestRecommendationBundle:
    """Test RecommendationBundle model"""

    def test_create_empty_bundle(self) -> None:
        """Test creating empty RecommendationBundle"""
        bundle = RecommendationBundle()

        assert bundle.project_identity_recs == []
        assert bundle.development_style_recs == []
        assert bundle.code_quality_recs == []
        assert bundle.documentation_recs == []
        assert bundle.testing_recs == []
        assert bundle.security_recs == []
        assert bundle.performance_recs == []
        assert bundle.collaboration_recs == []
        assert bundle.devops_recs == []
        assert bundle.analysis_duration_ms == 0
        assert bundle.total_confidence == 0.0
        assert bundle.generated_at is not None

    def test_create_with_recommendations(self) -> None:
        """Test creating RecommendationBundle with recommendations"""
        rec1 = Recommendation(
            preference_path="testing.coverage_target",
            recommended_value="90",
            confidence=0.9,
            reasoning="Test",
        )
        rec2 = Recommendation(
            preference_path="security.stance",
            recommended_value="strict",
            confidence=0.85,
            reasoning="Test",
        )

        bundle = RecommendationBundle(
            testing_recs=[rec1],
            security_recs=[rec2],
            analysis_duration_ms=1500,
            total_confidence=0.875,
        )

        assert len(bundle.testing_recs) == 1
        assert len(bundle.security_recs) == 1
        assert bundle.analysis_duration_ms == 1500
        assert bundle.total_confidence == 0.875

    def test_calculate_total_confidence_empty(self) -> None:
        """Test calculate_total_confidence with no recommendations"""
        bundle = RecommendationBundle()
        confidence = bundle.calculate_total_confidence()
        assert confidence == 0.0

    def test_calculate_total_confidence_single_category(self) -> None:
        """Test calculate_total_confidence with single category"""
        rec1 = Recommendation(
            preference_path="testing.coverage",
            recommended_value="90",
            confidence=0.9,
            reasoning="Test",
        )
        rec2 = Recommendation(
            preference_path="testing.pyramid",
            recommended_value="70-20-10",
            confidence=0.8,
            reasoning="Test",
        )

        bundle = RecommendationBundle(testing_recs=[rec1, rec2])
        confidence = bundle.calculate_total_confidence()
        assert abs(confidence - 0.85) < 0.001  # (0.9 + 0.8) / 2

    def test_calculate_total_confidence_multiple_categories(self) -> None:
        """Test calculate_total_confidence across multiple categories"""
        rec1 = Recommendation(
            preference_path="testing.coverage",
            recommended_value="90",
            confidence=0.9,
            reasoning="Test",
        )
        rec2 = Recommendation(
            preference_path="security.stance",
            recommended_value="strict",
            confidence=0.8,
            reasoning="Test",
        )
        rec3 = Recommendation(
            preference_path="code_quality.linting",
            recommended_value="strict",
            confidence=0.7,
            reasoning="Test",
        )

        bundle = RecommendationBundle(
            testing_recs=[rec1],
            security_recs=[rec2],
            code_quality_recs=[rec3],
        )

        confidence = bundle.calculate_total_confidence()
        expected = (0.9 + 0.8 + 0.7) / 3
        assert abs(confidence - expected) < 0.001

    def test_calculate_total_confidence_all_categories(self) -> None:
        """Test calculate_total_confidence with all categories populated"""
        rec = Recommendation(
            preference_path="test",
            recommended_value="value",
            confidence=0.8,
            reasoning="Test",
        )

        bundle = RecommendationBundle(
            project_identity_recs=[rec],
            development_style_recs=[rec],
            code_quality_recs=[rec],
            documentation_recs=[rec],
            testing_recs=[rec],
            security_recs=[rec],
            performance_recs=[rec],
            collaboration_recs=[rec],
            devops_recs=[rec],
        )

        confidence = bundle.calculate_total_confidence()
        assert confidence == 0.8  # All have same confidence

    def test_generated_at_timestamp(self) -> None:
        """Test that generated_at is set automatically"""
        bundle = RecommendationBundle()
        assert bundle.generated_at is not None

        # Parse as ISO datetime
        timestamp = datetime.fromisoformat(bundle.generated_at)
        assert isinstance(timestamp, datetime)

        # Should be recent (within last minute)
        now = datetime.now()
        time_diff = (now - timestamp).total_seconds()
        assert 0 <= time_diff < 60

    def test_validation_total_confidence_range(self) -> None:
        """Test total_confidence validation - must be 0.0-1.0"""
        bundle = RecommendationBundle(total_confidence=0.0)
        assert bundle.total_confidence == 0.0

        bundle = RecommendationBundle(total_confidence=1.0)
        assert bundle.total_confidence == 1.0

        with pytest.raises(ValidationError):
            RecommendationBundle(total_confidence=-0.1)

        with pytest.raises(ValidationError):
            RecommendationBundle(total_confidence=1.5)

    def test_json_serialization(self) -> None:
        """Test bundle serialization to dict and JSON"""
        rec = Recommendation(
            preference_path="test",
            recommended_value="value",
            confidence=0.8,
            reasoning="Test",
        )

        bundle = RecommendationBundle(
            testing_recs=[rec],
            analysis_duration_ms=1000,
            total_confidence=0.8,
        )

        data = bundle.model_dump()
        assert data["analysis_duration_ms"] == 1000
        assert data["total_confidence"] == 0.8
        assert len(data["testing_recs"]) == 1

        json_str = bundle.model_dump_json()
        assert "1000" in json_str
        assert "0.8" in json_str

    def test_json_deserialization(self) -> None:
        """Test bundle deserialization from dict"""
        data = {
            "project_identity_recs": [],
            "development_style_recs": [],
            "code_quality_recs": [
                {
                    "preference_path": "test",
                    "recommended_value": "value",
                    "confidence": 0.8,
                    "reasoning": "Test",
                    "alternatives": [],
                    "detection_basis": [],
                },
            ],
            "documentation_recs": [],
            "testing_recs": [],
            "security_recs": [],
            "performance_recs": [],
            "collaboration_recs": [],
            "devops_recs": [],
            "analysis_duration_ms": 500,
            "total_confidence": 0.75,
            "generated_at": "2025-01-01T12:00:00",
        }

        bundle = RecommendationBundle(**data)
        assert len(bundle.code_quality_recs) == 1
        assert bundle.analysis_duration_ms == 500
        assert bundle.total_confidence == 0.75


class TestProjectAnalysisReport:
    """Test ProjectAnalysisReport model"""

    def test_create_minimal(self) -> None:
        """Test creating ProjectAnalysisReport with minimal required fields"""
        report = ProjectAnalysisReport(
            project_root="/home/user/project",
        )

        assert report.project_root == "/home/user/project"
        assert report.languages == []
        assert report.frameworks == []
        assert report.project_types == []
        assert report.tools == []
        assert report.codebase_patterns == {}
        assert report.analyzed_at is not None
        assert report.analysis_duration_ms == 0

    def test_create_complete(self) -> None:
        """Test creating ProjectAnalysisReport with all fields"""
        lang_detection = DetectionResult(
            category="language",
            detected_value="python",
            confidence=0.95,
            evidence=["47 .py files"],
        )

        fw_detection = DetectionResult(
            category="framework",
            detected_value="fastapi",
            confidence=0.88,
            evidence=["from fastapi import FastAPI"],
        )

        type_detection = DetectionResult(
            category="project_type",
            detected_value="api",
            confidence=0.9,
            evidence=["REST endpoints detected"],
        )

        tool_detection = DetectionResult(
            category="tool",
            detected_value="pytest",
            confidence=0.92,
            evidence=["pytest.ini found"],
        )

        patterns = {
            "avg_function_length": 25,
            "has_type_hints": True,
            "cyclomatic_complexity": 8.5,
            "test_coverage": 85.0,
        }

        report = ProjectAnalysisReport(
            languages=[lang_detection],
            frameworks=[fw_detection],
            project_types=[type_detection],
            tools=[tool_detection],
            codebase_patterns=patterns,
            project_root="/home/user/project",
            analysis_duration_ms=2500,
        )

        assert len(report.languages) == 1
        assert len(report.frameworks) == 1
        assert len(report.project_types) == 1
        assert len(report.tools) == 1
        assert report.codebase_patterns["avg_function_length"] == 25
        assert report.codebase_patterns["has_type_hints"] is True
        assert report.analysis_duration_ms == 2500

    def test_analyzed_at_timestamp(self) -> None:
        """Test that analyzed_at is set automatically"""
        report = ProjectAnalysisReport(project_root="/test")
        assert report.analyzed_at is not None

        # Parse as ISO datetime
        timestamp = datetime.fromisoformat(report.analyzed_at)
        assert isinstance(timestamp, datetime)

        # Should be recent
        now = datetime.now()
        time_diff = (now - timestamp).total_seconds()
        assert 0 <= time_diff < 60

    def test_codebase_patterns_flexible(self) -> None:
        """Test codebase_patterns accepts arbitrary keys"""
        patterns = {
            "custom_metric_1": 42,
            "custom_metric_2": "value",
            "nested": {"key": "value"},
            "list_metric": [1, 2, 3],
        }

        report = ProjectAnalysisReport(
            project_root="/test",
            codebase_patterns=patterns,
        )

        assert report.codebase_patterns["custom_metric_1"] == 42
        assert report.codebase_patterns["custom_metric_2"] == "value"
        assert report.codebase_patterns["nested"]["key"] == "value"
        assert report.codebase_patterns["list_metric"] == [1, 2, 3]

    def test_missing_required_field(self) -> None:
        """Test that missing project_root raises validation error"""
        with pytest.raises(ValidationError):
            ProjectAnalysisReport()

    def test_json_serialization(self) -> None:
        """Test report serialization to dict and JSON"""
        detection = DetectionResult(
            category="language",
            detected_value="python",
            confidence=0.95,
        )

        report = ProjectAnalysisReport(
            languages=[detection],
            project_root="/home/user/project",
            analysis_duration_ms=1500,
        )

        data = report.model_dump()
        assert data["project_root"] == "/home/user/project"
        assert data["analysis_duration_ms"] == 1500
        assert len(data["languages"]) == 1

        json_str = report.model_dump_json()
        assert "/home/user/project" in json_str
        assert "1500" in json_str

    def test_json_deserialization(self) -> None:
        """Test report deserialization from dict"""
        data = {
            "languages": [
                {
                    "category": "language",
                    "detected_value": "python",
                    "confidence": 0.95,
                    "evidence": [],
                },
            ],
            "frameworks": [],
            "project_types": [],
            "tools": [],
            "codebase_patterns": {"test": "value"},
            "project_root": "/test",
            "analyzed_at": "2025-01-01T12:00:00",
            "analysis_duration_ms": 1000,
        }

        report = ProjectAnalysisReport(**data)
        assert len(report.languages) == 1
        assert report.project_root == "/test"
        assert report.codebase_patterns["test"] == "value"

    def test_multiple_detections_per_category(self) -> None:
        """Test report with multiple detections per category"""
        lang1 = DetectionResult(
            category="language",
            detected_value="python",
            confidence=0.95,
        )
        lang2 = DetectionResult(
            category="language",
            detected_value="javascript",
            confidence=0.75,
        )
        lang3 = DetectionResult(
            category="language",
            detected_value="sql",
            confidence=0.6,
        )

        report = ProjectAnalysisReport(
            languages=[lang1, lang2, lang3],
            project_root="/test",
        )

        assert len(report.languages) == 3
        assert report.languages[0].detected_value == "python"
        assert report.languages[1].detected_value == "javascript"
        assert report.languages[2].detected_value == "sql"


class TestEdgeCases:
    """Test edge cases and boundary conditions"""

    def test_empty_strings_allowed(self) -> None:
        """Test that empty strings are allowed where appropriate"""
        result = DetectionResult(
            category="",
            detected_value="",
            confidence=0.5,
        )
        assert result.category == ""
        assert result.detected_value == ""

        rec = Recommendation(
            preference_path="",
            recommended_value="",
            confidence=0.5,
            reasoning="",
        )
        assert rec.preference_path == ""
        assert rec.reasoning == ""

    def test_very_long_strings(self) -> None:
        """Test handling of very long strings"""
        long_string = "x" * 10000
        result = DetectionResult(
            category=long_string,
            detected_value=long_string,
            confidence=0.5,
            evidence=[long_string],
        )
        assert len(result.category) == 10000
        assert len(result.evidence[0]) == 10000

    def test_special_characters_in_strings(self) -> None:
        """Test special characters in strings"""
        result = DetectionResult(
            category="lang/framework",
            detected_value="C++",
            confidence=0.9,
            evidence=["#include <iostream>", "namespace std::"],
        )
        assert result.category == "lang/framework"
        assert result.detected_value == "C++"

    def test_unicode_in_strings(self) -> None:
        """Test unicode characters in strings"""
        result = DetectionResult(
            category="プロジェクト",
            detected_value="日本語",
            confidence=0.8,
            evidence=["証拠1", "証拠2"],
        )
        assert "プロジェクト" in result.category
        assert "日本語" in result.detected_value

    def test_extreme_confidence_precision(self) -> None:
        """Test very precise confidence values"""
        result = DetectionResult(
            category="test",
            detected_value="value",
            confidence=0.123456789,
        )
        assert abs(result.confidence - 0.123456789) < 1e-9

    def test_large_evidence_lists(self) -> None:
        """Test large evidence lists"""
        evidence = [f"evidence_{i}" for i in range(1000)]
        result = DetectionResult(
            category="test",
            detected_value="value",
            confidence=0.8,
            evidence=evidence,
        )
        assert len(result.evidence) == 1000

    def test_deeply_nested_recommended_value(self) -> None:
        """Test deeply nested structures in recommended_value"""
        nested = {
            "level1": {
                "level2": {
                    "level3": {
                        "level4": {"value": "deep"},
                    },
                },
            },
        }

        rec = Recommendation(
            preference_path="test",
            recommended_value=nested,
            confidence=0.8,
            reasoning="Test",
        )
        assert rec.recommended_value["level1"]["level2"]["level3"]["level4"]["value"] == "deep"

    def test_none_values_where_allowed(self) -> None:
        """Test None values in optional fields"""
        bundle = RecommendationBundle(
            analysis_duration_ms=0,
            total_confidence=0.0,
        )
        # All list fields should be empty lists, not None
        assert bundle.testing_recs == []
        assert bundle.security_recs == []


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

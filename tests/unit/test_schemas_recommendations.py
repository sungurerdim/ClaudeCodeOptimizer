"""
Unit tests for Recommendation Schemas

Tests DetectionResult, Recommendation, RecommendationBundle, and ProjectAnalysisReport models.

Target Coverage: 100%
"""

from datetime import datetime
from typing import Any, List

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

    def test_minimal_creation(self) -> None:
        """Test creating DetectionResult with required fields only"""
        result = DetectionResult(
            category="language",
            detected_value="python",
            confidence=0.95,
        )

        assert result.category == "language"
        assert result.detected_value == "python"
        assert result.confidence == 0.95
        assert result.evidence == []

    def test_full_creation(self) -> None:
        """Test creating DetectionResult with all fields"""
        evidence = ["47 .py files", "pyproject.toml present", "requirements.txt found"]
        result = DetectionResult(
            category="language",
            detected_value="python",
            confidence=0.95,
            evidence=evidence,
        )

        assert result.category == "language"
        assert result.detected_value == "python"
        assert result.confidence == 0.95
        assert len(result.evidence) == 3
        assert result.evidence == evidence

    def test_confidence_bounds_valid(self) -> None:
        """Test confidence score is bounded between 0.0 and 1.0"""
        # Lower bound
        result = DetectionResult(
            category="language",
            detected_value="python",
            confidence=0.0,
        )
        assert result.confidence == 0.0

        # Upper bound
        result = DetectionResult(
            category="language",
            detected_value="python",
            confidence=1.0,
        )
        assert result.confidence == 1.0

        # Mid-range
        result = DetectionResult(
            category="language",
            detected_value="python",
            confidence=0.5,
        )
        assert result.confidence == 0.5

    def test_confidence_bounds_invalid_high(self) -> None:
        """Test confidence score validation - too high"""
        with pytest.raises(ValidationError):
            DetectionResult(
                category="language",
                detected_value="python",
                confidence=1.1,
            )

    def test_confidence_bounds_invalid_low(self) -> None:
        """Test confidence score validation - too low"""
        with pytest.raises(ValidationError):
            DetectionResult(
                category="language",
                detected_value="python",
                confidence=-0.1,
            )

    def test_empty_evidence_list(self) -> None:
        """Test with empty evidence list"""
        result = DetectionResult(
            category="framework",
            detected_value="fastapi",
            confidence=0.85,
            evidence=[],
        )

        assert result.evidence == []

    def test_multiple_evidence_items(self) -> None:
        """Test with multiple evidence items"""
        evidence = [
            "Found FastAPI imports in 15 files",
            "main.py uses FastAPI app instance",
            "pyproject.toml lists fastapi>=0.95.0",
            "API endpoints detected in multiple modules",
        ]
        result = DetectionResult(
            category="framework",
            detected_value="fastapi",
            confidence=0.99,
            evidence=evidence,
        )

        assert len(result.evidence) == 4
        assert all(item in result.evidence for item in evidence)

    def test_category_types(self) -> None:
        """Test different category types"""
        categories = ["language", "framework", "tool", "pattern", "package-manager"]
        for cat in categories:
            result = DetectionResult(
                category=cat,
                detected_value="test",
                confidence=0.8,
            )
            assert result.category == cat

    def test_missing_required_fields(self) -> None:
        """Test that missing required fields raises validation error"""
        with pytest.raises(ValidationError):
            DetectionResult()

        with pytest.raises(ValidationError):
            DetectionResult(category="language")

        with pytest.raises(ValidationError):
            DetectionResult(category="language", detected_value="python")

    def test_serialization(self) -> None:
        """Test serialization to dict"""
        result = DetectionResult(
            category="language",
            detected_value="python",
            confidence=0.95,
            evidence=["evidence1", "evidence2"],
        )

        data = result.model_dump()
        assert data["category"] == "language"
        assert data["detected_value"] == "python"
        assert data["confidence"] == 0.95
        assert len(data["evidence"]) == 2

    def test_json_serialization(self) -> None:
        """Test serialization to JSON"""
        result = DetectionResult(
            category="language",
            detected_value="python",
            confidence=0.95,
            evidence=["test"],
        )

        json_str = result.model_dump_json()
        assert "language" in json_str
        assert "python" in json_str
        assert "0.95" in json_str


class TestRecommendation:
    """Test Recommendation model"""

    def test_minimal_creation(self) -> None:
        """Test creating Recommendation with required fields only"""
        rec = Recommendation(
            preference_path="code_quality.linting_strictness",
            recommended_value="strict",
            confidence=0.85,
            reasoning="Based on project analysis and best practices",
        )

        assert rec.preference_path == "code_quality.linting_strictness"
        assert rec.recommended_value == "strict"
        assert rec.confidence == 0.85
        assert rec.reasoning == "Based on project analysis and best practices"
        assert rec.alternatives == []
        assert rec.detection_basis == []

    def test_full_creation(self) -> None:
        """Test creating Recommendation with all fields"""
        detection_basis = [
            DetectionResult(
                category="linter",
                detected_value="ruff",
                confidence=0.95,
                evidence=["ruff.toml present", "CI uses ruff"],
            ),
            DetectionResult(
                category="tool",
                detected_value="black",
                confidence=0.9,
                evidence=["black found in pyproject.toml"],
            ),
        ]

        rec = Recommendation(
            preference_path="code_quality.linting_strictness",
            recommended_value="strict",
            confidence=0.85,
            reasoning="Project uses ruff and black with strict configs",
            alternatives=["standard", "moderate"],
            detection_basis=detection_basis,
        )

        assert rec.preference_path == "code_quality.linting_strictness"
        assert rec.recommended_value == "strict"
        assert rec.confidence == 0.85
        assert len(rec.alternatives) == 2
        assert len(rec.detection_basis) == 2

    def test_confidence_bounds(self) -> None:
        """Test confidence bounds validation"""
        # Valid
        rec = Recommendation(
            preference_path="test.path",
            recommended_value="value",
            confidence=0.0,
            reasoning="test",
        )
        assert rec.confidence == 0.0

        rec = Recommendation(
            preference_path="test.path",
            recommended_value="value",
            confidence=1.0,
            reasoning="test",
        )
        assert rec.confidence == 1.0

        # Invalid
        with pytest.raises(ValidationError):
            Recommendation(
                preference_path="test.path",
                recommended_value="value",
                confidence=1.5,
                reasoning="test",
            )

    def test_various_recommended_values(self) -> None:
        """Test different types of recommended values"""
        # String value
        rec = Recommendation(
            preference_path="code_quality.linting_strictness",
            recommended_value="strict",
            confidence=0.9,
            reasoning="test",
        )
        assert rec.recommended_value == "strict"

        # Numeric value
        rec = Recommendation(
            preference_path="code_quality.cyclomatic_complexity_limit",
            recommended_value=10,
            confidence=0.9,
            reasoning="test",
        )
        assert rec.recommended_value == 10

        # List value
        rec = Recommendation(
            preference_path="project_identity.types",
            recommended_value=["api", "backend"],
            confidence=0.9,
            reasoning="test",
        )
        assert isinstance(rec.recommended_value, list)

        # Dict value
        rec = Recommendation(
            preference_path="test.path",
            recommended_value={"key": "value"},
            confidence=0.9,
            reasoning="test",
        )
        assert isinstance(rec.recommended_value, dict)

    def test_multiple_alternatives(self) -> None:
        """Test multiple alternatives"""
        alternatives = ["option1", "option2", "option3", "option4"]
        rec = Recommendation(
            preference_path="test.path",
            recommended_value="option1",
            confidence=0.85,
            reasoning="test",
            alternatives=alternatives,
        )

        assert len(rec.alternatives) == 4
        assert set(rec.alternatives) == set(alternatives)

    def test_multiple_detection_basis(self) -> None:
        """Test multiple detection results as basis"""
        detection_basis = [
            DetectionResult(
                category="language",
                detected_value="python",
                confidence=0.99,
            ),
            DetectionResult(
                category="framework",
                detected_value="fastapi",
                confidence=0.95,
            ),
            DetectionResult(
                category="tool",
                detected_value="pytest",
                confidence=0.9,
            ),
        ]

        rec = Recommendation(
            preference_path="testing.coverage_target",
            recommended_value="90",
            confidence=0.88,
            reasoning="Based on Python/FastAPI/pytest stack",
            detection_basis=detection_basis,
        )

        assert len(rec.detection_basis) == 3

    def test_preference_path_formats(self) -> None:
        """Test various preference path formats"""
        paths = [
            "code_quality.linting_strictness",
            "testing.coverage_target",
            "security.encryption_scope",
            "devops.ci_cd_trigger",
            "project_identity.types",
        ]

        for path in paths:
            rec = Recommendation(
                preference_path=path,
                recommended_value="test",
                confidence=0.8,
                reasoning="test",
            )
            assert rec.preference_path == path

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

    def test_serialization(self) -> None:
        """Test serialization to dict"""
        rec = Recommendation(
            preference_path="code_quality.linting_strictness",
            recommended_value="strict",
            confidence=0.85,
            reasoning="test reasoning",
            alternatives=["option1", "option2"],
        )

        data = rec.model_dump()
        assert data["preference_path"] == "code_quality.linting_strictness"
        assert data["recommended_value"] == "strict"
        assert data["confidence"] == 0.85
        assert len(data["alternatives"]) == 2

    def test_json_serialization(self) -> None:
        """Test serialization to JSON"""
        rec = Recommendation(
            preference_path="test.path",
            recommended_value="value",
            confidence=0.8,
            reasoning="test",
        )

        json_str = rec.model_dump_json()
        assert "test.path" in json_str
        assert "value" in json_str
        assert "0.8" in json_str


class TestRecommendationBundle:
    """Test RecommendationBundle model"""

    def test_empty_bundle(self) -> None:
        """Test creating empty recommendation bundle"""
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

    def test_bundle_with_recommendations(self) -> None:
        """Test bundle with recommendations in different categories"""
        bundle = RecommendationBundle(
            project_identity_recs=[
                Recommendation(
                    preference_path="project_identity.types",
                    recommended_value=["api"],
                    confidence=0.9,
                    reasoning="Detected REST API",
                ),
            ],
            code_quality_recs=[
                Recommendation(
                    preference_path="code_quality.linting_strictness",
                    recommended_value="strict",
                    confidence=0.85,
                    reasoning="Project uses ruff",
                ),
            ],
            testing_recs=[
                Recommendation(
                    preference_path="testing.coverage_target",
                    recommended_value="90",
                    confidence=0.8,
                    reasoning="Detected pytest.ini with 90%",
                ),
            ],
        )

        assert len(bundle.project_identity_recs) == 1
        assert len(bundle.code_quality_recs) == 1
        assert len(bundle.testing_recs) == 1
        assert len(bundle.development_style_recs) == 0

    def test_all_category_recs(self) -> None:
        """Test bundle with recommendations in all categories"""
        rec = Recommendation(
            preference_path="test.path",
            recommended_value="value",
            confidence=0.8,
            reasoning="test",
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

        assert len(bundle.project_identity_recs) == 1
        assert len(bundle.development_style_recs) == 1
        assert len(bundle.code_quality_recs) == 1
        assert len(bundle.documentation_recs) == 1
        assert len(bundle.testing_recs) == 1
        assert len(bundle.security_recs) == 1
        assert len(bundle.performance_recs) == 1
        assert len(bundle.collaboration_recs) == 1
        assert len(bundle.devops_recs) == 1

    def test_calculate_total_confidence_empty(self) -> None:
        """Test total confidence calculation with no recommendations"""
        bundle = RecommendationBundle()
        total = bundle.calculate_total_confidence()
        assert total == 0.0

    def test_calculate_total_confidence_single(self) -> None:
        """Test total confidence calculation with single recommendation"""
        rec = Recommendation(
            preference_path="test.path",
            recommended_value="value",
            confidence=0.8,
            reasoning="test",
        )

        bundle = RecommendationBundle(code_quality_recs=[rec])
        total = bundle.calculate_total_confidence()
        assert total == 0.8

    def test_calculate_total_confidence_multiple(self) -> None:
        """Test total confidence calculation with multiple recommendations"""
        recs = [
            Recommendation(
                preference_path=f"test.path{i}",
                recommended_value="value",
                confidence=float(i) / 10,  # 0.1, 0.2, 0.3
                reasoning="test",
            )
            for i in range(1, 4)
        ]

        bundle = RecommendationBundle(code_quality_recs=recs)
        total = bundle.calculate_total_confidence()

        # Average of 0.1, 0.2, 0.3
        expected = (0.1 + 0.2 + 0.3) / 3
        assert abs(total - expected) < 0.001

    def test_calculate_total_confidence_across_categories(self) -> None:
        """Test confidence calculation across multiple categories"""
        rec1 = Recommendation(
            preference_path="test1",
            recommended_value="value",
            confidence=0.9,
            reasoning="test",
        )
        rec2 = Recommendation(
            preference_path="test2",
            recommended_value="value",
            confidence=0.8,
            reasoning="test",
        )
        rec3 = Recommendation(
            preference_path="test3",
            recommended_value="value",
            confidence=0.7,
            reasoning="test",
        )

        bundle = RecommendationBundle(
            code_quality_recs=[rec1],
            testing_recs=[rec2],
            security_recs=[rec3],
        )

        total = bundle.calculate_total_confidence()
        expected = (0.9 + 0.8 + 0.7) / 3
        assert abs(total - expected) < 0.001

    def test_metadata_fields(self) -> None:
        """Test metadata fields"""
        bundle = RecommendationBundle(
            analysis_duration_ms=1234,
            total_confidence=0.85,
        )

        assert bundle.analysis_duration_ms == 1234
        assert bundle.total_confidence == 0.85
        assert bundle.generated_at is not None

    def test_generated_at_timestamp(self) -> None:
        """Test generated_at field is ISO format"""
        bundle = RecommendationBundle()
        # Should be valid ISO format
        datetime.fromisoformat(bundle.generated_at)

    def test_custom_timestamp(self) -> None:
        """Test setting custom timestamp"""
        timestamp = "2025-01-15T10:30:00"
        bundle = RecommendationBundle(generated_at=timestamp)
        assert bundle.generated_at == timestamp

    def test_large_recommendation_set(self) -> None:
        """Test bundle with many recommendations"""
        recs = [
            Recommendation(
                preference_path=f"test.path{i}",
                recommended_value="value",
                confidence=0.5 + (i * 0.01),
                reasoning=f"Recommendation {i}",
            )
            for i in range(50)
        ]

        bundle = RecommendationBundle(code_quality_recs=recs)
        assert len(bundle.code_quality_recs) == 50

    def test_serialization(self) -> None:
        """Test serialization to dict"""
        rec = Recommendation(
            preference_path="test.path",
            recommended_value="value",
            confidence=0.8,
            reasoning="test",
        )

        bundle = RecommendationBundle(
            code_quality_recs=[rec],
            analysis_duration_ms=100,
            total_confidence=0.8,
        )

        data = bundle.model_dump()
        assert len(data["code_quality_recs"]) == 1
        assert data["analysis_duration_ms"] == 100
        assert data["total_confidence"] == 0.8

    def test_json_serialization(self) -> None:
        """Test serialization to JSON"""
        rec = Recommendation(
            preference_path="test.path",
            recommended_value="value",
            confidence=0.8,
            reasoning="test",
        )

        bundle = RecommendationBundle(code_quality_recs=[rec])
        json_str = bundle.model_dump_json()
        assert "test.path" in json_str
        assert "code_quality_recs" in json_str


class TestProjectAnalysisReport:
    """Test ProjectAnalysisReport model"""

    def test_minimal_creation(self) -> None:
        """Test creating ProjectAnalysisReport with required fields only"""
        report = ProjectAnalysisReport(project_root="/home/user/project")

        assert report.project_root == "/home/user/project"
        assert report.languages == []
        assert report.frameworks == []
        assert report.project_types == []
        assert report.tools == []
        assert report.codebase_patterns == {}
        assert report.analyzed_at is not None
        assert report.analysis_duration_ms == 0

    def test_full_creation(self) -> None:
        """Test creating ProjectAnalysisReport with all fields"""
        languages = [
            DetectionResult(
                category="language",
                detected_value="python",
                confidence=0.99,
                evidence=["47 .py files"],
            ),
            DetectionResult(
                category="language",
                detected_value="javascript",
                confidence=0.85,
                evidence=["5 .js files"],
            ),
        ]

        frameworks = [
            DetectionResult(
                category="framework",
                detected_value="fastapi",
                confidence=0.95,
                evidence=["FastAPI imports found"],
            ),
        ]

        project_types = [
            DetectionResult(
                category="type",
                detected_value="api",
                confidence=0.9,
                evidence=["REST API detected"],
            ),
        ]

        tools = [
            DetectionResult(
                category="tool",
                detected_value="pytest",
                confidence=0.88,
                evidence=["pytest.ini found"],
            ),
        ]

        codebase_patterns = {
            "avg_function_length": 25,
            "has_type_hints": True,
            "test_coverage": 0.85,
            "complexity_average": 3.2,
        }

        report = ProjectAnalysisReport(
            languages=languages,
            frameworks=frameworks,
            project_types=project_types,
            tools=tools,
            codebase_patterns=codebase_patterns,
            project_root="/home/user/project",
            analysis_duration_ms=500,
        )

        assert len(report.languages) == 2
        assert len(report.frameworks) == 1
        assert len(report.project_types) == 1
        assert len(report.tools) == 1
        assert report.codebase_patterns["avg_function_length"] == 25
        assert report.analysis_duration_ms == 500

    def test_missing_required_fields(self) -> None:
        """Test that project_root is required"""
        with pytest.raises(ValidationError):
            ProjectAnalysisReport()

    def test_analyzed_at_timestamp(self) -> None:
        """Test analyzed_at field is ISO format"""
        report = ProjectAnalysisReport(project_root="/test")
        # Should be valid ISO format
        datetime.fromisoformat(report.analyzed_at)

    def test_custom_timestamp(self) -> None:
        """Test setting custom timestamp"""
        timestamp = "2025-01-15T10:30:00"
        report = ProjectAnalysisReport(
            project_root="/test",
            analyzed_at=timestamp,
        )
        assert report.analyzed_at == timestamp

    def test_empty_detection_lists(self) -> None:
        """Test with empty detection result lists"""
        report = ProjectAnalysisReport(
            project_root="/test",
            languages=[],
            frameworks=[],
            project_types=[],
            tools=[],
        )

        assert report.languages == []
        assert report.frameworks == []

    def test_multiple_languages(self) -> None:
        """Test report with multiple detected languages"""
        languages = [
            DetectionResult(
                category="language",
                detected_value=f"lang{i}",
                confidence=0.9 - (i * 0.05),
            )
            for i in range(5)
        ]

        report = ProjectAnalysisReport(
            project_root="/test",
            languages=languages,
        )

        assert len(report.languages) == 5

    def test_multiple_frameworks(self) -> None:
        """Test report with multiple detected frameworks"""
        frameworks = [
            DetectionResult(
                category="framework",
                detected_value=f"framework{i}",
                confidence=0.85,
            )
            for i in range(3)
        ]

        report = ProjectAnalysisReport(
            project_root="/test",
            frameworks=frameworks,
        )

        assert len(report.frameworks) == 3

    def test_codebase_patterns_flexibility(self) -> None:
        """Test codebase_patterns accepts various types"""
        patterns = {
            "string_metric": "value",
            "int_metric": 42,
            "float_metric": 3.14,
            "bool_metric": True,
            "list_metric": [1, 2, 3],
            "dict_metric": {"key": "value"},
            "none_metric": None,
        }

        report = ProjectAnalysisReport(
            project_root="/test",
            codebase_patterns=patterns,
        )

        assert report.codebase_patterns["string_metric"] == "value"
        assert report.codebase_patterns["int_metric"] == 42
        assert report.codebase_patterns["list_metric"] == [1, 2, 3]

    def test_empty_codebase_patterns(self) -> None:
        """Test with empty codebase patterns"""
        report = ProjectAnalysisReport(
            project_root="/test",
            codebase_patterns={},
        )

        assert report.codebase_patterns == {}

    def test_project_root_paths(self) -> None:
        """Test various project root path formats"""
        paths = [
            "/home/user/project",
            "C:\\Users\\User\\Project",
            "./relative/path",
            "/absolute/path/with/multiple/segments",
            "/path-with-dashes_and_underscores",
        ]

        for path in paths:
            report = ProjectAnalysisReport(project_root=path)
            assert report.project_root == path

    def test_analysis_duration_metrics(self) -> None:
        """Test various analysis duration values"""
        durations = [0, 1, 100, 1000, 5000, 10000, 60000]

        for duration in durations:
            report = ProjectAnalysisReport(
                project_root="/test",
                analysis_duration_ms=duration,
            )
            assert report.analysis_duration_ms == duration

    def test_serialization(self) -> None:
        """Test serialization to dict"""
        lang = DetectionResult(
            category="language",
            detected_value="python",
            confidence=0.95,
        )

        report = ProjectAnalysisReport(
            project_root="/test",
            languages=[lang],
            codebase_patterns={"metric": 42},
            analysis_duration_ms=100,
        )

        data = report.model_dump()
        assert data["project_root"] == "/test"
        assert len(data["languages"]) == 1
        assert data["codebase_patterns"]["metric"] == 42
        assert data["analysis_duration_ms"] == 100

    def test_json_serialization(self) -> None:
        """Test serialization to JSON"""
        report = ProjectAnalysisReport(project_root="/test")
        json_str = report.model_dump_json()
        assert "/test" in json_str
        assert "project_root" in json_str

    def test_complex_report(self) -> None:
        """Test complex project analysis report"""
        languages = [
            DetectionResult(
                category="language",
                detected_value="python",
                confidence=0.99,
                evidence=["100+ .py files", "pyproject.toml present"],
            ),
            DetectionResult(
                category="language",
                detected_value="typescript",
                confidence=0.92,
                evidence=["20+ .ts files"],
            ),
            DetectionResult(
                category="language",
                detected_value="sql",
                confidence=0.88,
                evidence=["5 .sql files"],
            ),
        ]

        frameworks = [
            DetectionResult(
                category="framework",
                detected_value="fastapi",
                confidence=0.96,
                evidence=["FastAPI app found"],
            ),
            DetectionResult(
                category="framework",
                detected_value="react",
                confidence=0.91,
                evidence=["React components detected"],
            ),
        ]

        project_types = [
            DetectionResult(
                category="type",
                detected_value="api",
                confidence=0.95,
            ),
            DetectionResult(
                category="type",
                detected_value="microservice",
                confidence=0.88,
            ),
        ]

        tools = [
            DetectionResult(
                category="tool",
                detected_value="pytest",
                confidence=0.93,
            ),
            DetectionResult(
                category="tool",
                detected_value="docker",
                confidence=0.91,
            ),
            DetectionResult(
                category="tool",
                detected_value="kubernetes",
                confidence=0.87,
            ),
        ]

        codebase_patterns = {
            "total_files": 250,
            "avg_file_size": 350,
            "avg_function_length": 28,
            "has_type_hints": True,
            "type_coverage": 0.92,
            "test_coverage": 0.88,
            "avg_cyclomatic_complexity": 3.1,
            "documentation_coverage": 0.85,
        }

        report = ProjectAnalysisReport(
            languages=languages,
            frameworks=frameworks,
            project_types=project_types,
            tools=tools,
            codebase_patterns=codebase_patterns,
            project_root="/home/dev/microservices/api-service",
            analysis_duration_ms=2500,
        )

        assert len(report.languages) == 3
        assert len(report.frameworks) == 2
        assert len(report.project_types) == 2
        assert len(report.tools) == 3
        assert len(report.codebase_patterns) == 8
        assert report.analysis_duration_ms == 2500


class TestEdgeCases:
    """Test edge cases and boundary conditions"""

    def test_very_high_confidence(self) -> None:
        """Test very high confidence values"""
        result = DetectionResult(
            category="test",
            detected_value="value",
            confidence=0.9999999,
        )
        assert result.confidence > 0.99

    def test_very_low_confidence(self) -> None:
        """Test very low confidence values"""
        result = DetectionResult(
            category="test",
            detected_value="value",
            confidence=0.0001,
        )
        assert result.confidence < 0.001

    def test_empty_string_values(self) -> None:
        """Test empty string values"""
        result = DetectionResult(
            category="",
            detected_value="",
            confidence=0.5,
        )
        assert result.category == ""
        assert result.detected_value == ""

    def test_very_long_strings(self) -> None:
        """Test very long string values"""
        long_reasoning = "x" * 10000
        rec = Recommendation(
            preference_path="test.path",
            recommended_value="value",
            confidence=0.8,
            reasoning=long_reasoning,
        )
        assert len(rec.reasoning) == 10000

    def test_special_characters_in_paths(self) -> None:
        """Test special characters in preference paths"""
        paths = [
            "test.path.with.dots",
            "test_path_with_underscores",
            "test-path-with-dashes",
        ]

        for path in paths:
            rec = Recommendation(
                preference_path=path,
                recommended_value="value",
                confidence=0.8,
                reasoning="test",
            )
            assert rec.preference_path == path

    def test_unicode_in_text_fields(self) -> None:
        """Test unicode characters in text fields"""
        rec = Recommendation(
            preference_path="test.path",
            recommended_value="value-日本語",
            confidence=0.8,
            reasoning="理由: これはテストです",
        )
        assert "日本語" in str(rec.recommended_value)
        assert "テスト" in rec.reasoning

    def test_large_alternative_list(self) -> None:
        """Test large number of alternatives"""
        alternatives = [f"option{i}" for i in range(100)]
        rec = Recommendation(
            preference_path="test.path",
            recommended_value="option0",
            confidence=0.8,
            reasoning="test",
            alternatives=alternatives,
        )
        assert len(rec.alternatives) == 100

    def test_nested_dict_in_patterns(self) -> None:
        """Test nested dictionaries in codebase patterns"""
        patterns = {
            "top_level": {
                "nested_level": {
                    "deep_level": "value",
                },
            },
        }

        report = ProjectAnalysisReport(
            project_root="/test",
            codebase_patterns=patterns,
        )

        assert report.codebase_patterns["top_level"]["nested_level"]["deep_level"] == "value"


class TestDeserialization:
    """Test deserialization from dict/JSON"""

    def test_detection_result_from_dict(self) -> None:
        """Test creating DetectionResult from dict"""
        data = {
            "category": "language",
            "detected_value": "python",
            "confidence": 0.95,
            "evidence": ["test1", "test2"],
        }

        result = DetectionResult(**data)
        assert result.category == "language"
        assert result.detected_value == "python"

    def test_recommendation_from_dict(self) -> None:
        """Test creating Recommendation from dict"""
        data = {
            "preference_path": "code_quality.linting_strictness",
            "recommended_value": "strict",
            "confidence": 0.85,
            "reasoning": "Based on analysis",
        }

        rec = Recommendation(**data)
        assert rec.preference_path == "code_quality.linting_strictness"

    def test_bundle_from_dict(self) -> None:
        """Test creating RecommendationBundle from dict"""
        data = {
            "analysis_duration_ms": 100,
            "total_confidence": 0.85,
        }

        bundle = RecommendationBundle(**data)
        assert bundle.analysis_duration_ms == 100

    def test_report_from_dict(self) -> None:
        """Test creating ProjectAnalysisReport from dict"""
        data = {
            "project_root": "/test",
            "analysis_duration_ms": 500,
        }

        report = ProjectAnalysisReport(**data)
        assert report.project_root == "/test"
        assert report.analysis_duration_ms == 500


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

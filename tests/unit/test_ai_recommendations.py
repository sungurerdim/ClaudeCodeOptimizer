"""
Unit tests for AI Recommendation Engine

Tests RecommendationEngine class, confidence calculations, and filtering.
Target Coverage: 100%
"""

from typing import Any, Dict

import pytest

from claudecodeoptimizer.ai.recommendations import (
    DOMAIN_BEST_PRACTICES,
    LANGUAGE_BEST_PRACTICES,
    MONITORING_LEVEL_REQUIREMENTS,
    SCALE_RECOMMENDATIONS,
    SECURITY_STANCE_REQUIREMENTS,
    ConfidenceLevel,
    Recommendation,
    RecommendationBundle,
    RecommendationEngine,
    filter_recommendations,
    format_recommendation_markdown,
    prioritize_recommendations,
)


@pytest.fixture
def minimal_detection_results() -> Dict[str, Any]:
    """Minimal detection results for testing"""
    return {
        "project_identity": {
            "type": "application",
            "domain": "default",
            "scale": "startup",
            "primary_language": "python",
        },
        "code_quality": {},
        "testing": {},
        "security": {},
        "devops": {},
        "infrastructure": {},
    }


@pytest.fixture
def fintech_detection_results() -> Dict[str, Any]:
    """Fintech project detection results"""
    return {
        "project_identity": {
            "type": "application",
            "domain": "fintech",
            "scale": "enterprise",
            "primary_language": "python",
            "team_size": 100,
        },
        "code_quality": {
            "formatter": "black",
            "linter": "ruff",
            "type_checker": "mypy",
        },
        "testing": {
            "test_framework": "pytest",
            "test_coverage_percent": 92,
            "has_unit_tests": True,
            "has_integration_tests": False,
            "has_e2e_tests": False,
        },
        "security": {
            "encryption_at_rest": False,
            "secret_management_tool": None,
            "mfa_enabled": False,
            "audit_logging_enabled": False,
            "dependency_scanning": False,
        },
        "devops": {
            "ci_cd_platform": "github-actions",
            "deployment_strategy": ["smoke-tests"],
            "monitoring": {"metrics": False, "logs": False, "traces": False},
        },
        "infrastructure": {
            "containerization": {"docker": True},
            "orchestration": {"kubernetes": False},
            "database": {},
            "backup_strategy": False,
        },
    }


@pytest.fixture
def complete_detection_results() -> Dict[str, Any]:
    """Detection results with all features enabled"""
    return {
        "project_identity": {
            "type": "microservice",
            "domain": "saas",
            "scale": "growth",
            "primary_language": "typescript",
        },
        "code_quality": {
            "formatter": "prettier",
            "linter": "eslint-typescript",
            "type_checker": "typescript",
        },
        "testing": {
            "test_framework": "jest",
            "test_coverage_percent": 88,
            "has_unit_tests": True,
            "has_integration_tests": True,
            "has_e2e_tests": False,
        },
        "security": {
            "encryption_at_rest": True,
            "secret_management_tool": "vault",
            "mfa_enabled": True,
            "audit_logging_enabled": True,
            "dependency_scanning": True,
        },
        "devops": {
            "ci_cd_platform": "gitlab-ci",
            "deployment_strategy": ["canary", "smoke-tests"],
            "monitoring": {"metrics": True, "logs": True, "traces": True},
        },
        "infrastructure": {
            "containerization": {"docker": True},
            "orchestration": {"kubernetes": True},
            "database": {"postgresql": True},
            "backup_strategy": True,
        },
    }


@pytest.fixture
def missing_identity_results() -> Dict[str, Any]:
    """Detection results with missing identity fields"""
    return {
        "project_identity": {
            "type": "unknown",
            "domain": "general",
            "scale": None,
            "primary_language": "python",
        },
        "code_quality": {},
        "testing": {},
        "security": {},
        "devops": {},
        "infrastructure": {},
    }


class TestConfidenceLevel:
    """Test ConfidenceLevel enum"""

    def test_confidence_levels_exist(self) -> None:
        """Test all confidence levels are defined"""
        assert ConfidenceLevel.VERY_HIGH.value == 0.95
        assert ConfidenceLevel.HIGH.value == 0.85
        assert ConfidenceLevel.MEDIUM.value == 0.70
        assert ConfidenceLevel.LOW.value == 0.50

    def test_confidence_ordering(self) -> None:
        """Test confidence levels are properly ordered"""
        assert ConfidenceLevel.VERY_HIGH.value > ConfidenceLevel.HIGH.value
        assert ConfidenceLevel.HIGH.value > ConfidenceLevel.MEDIUM.value
        assert ConfidenceLevel.MEDIUM.value > ConfidenceLevel.LOW.value


class TestRecommendationDataclass:
    """Test Recommendation dataclass"""

    def test_recommendation_creation(self) -> None:
        """Test creating a recommendation"""
        rec = Recommendation(
            category="security",
            title="Enable encryption",
            description="Encrypt data at rest",
            priority="critical",
            confidence=0.95,
            reasoning=["Protects data"],
            evidence=["Domain: fintech"],
            citations=["OWASP"],
        )

        assert rec.category == "security"
        assert rec.title == "Enable encryption"
        assert rec.priority == "critical"
        assert rec.confidence == 0.95
        assert len(rec.reasoning) == 1
        assert rec.implementation_notes is None
        assert rec.estimated_effort is None

    def test_recommendation_with_optional_fields(self) -> None:
        """Test recommendation with optional fields"""
        rec = Recommendation(
            category="testing",
            title="Add tests",
            description="Increase coverage",
            priority="high",
            confidence=0.85,
            reasoning=["Improves quality"],
            evidence=["Current: 50%"],
            citations=["Testing best practices"],
            implementation_notes="Start with critical paths",
            estimated_effort="3d",
        )

        assert rec.implementation_notes == "Start with critical paths"
        assert rec.estimated_effort == "3d"


class TestRecommendationBundle:
    """Test RecommendationBundle dataclass"""

    def test_bundle_creation(self) -> None:
        """Test creating a recommendation bundle"""
        bundle = RecommendationBundle(
            project_identity=[],
            code_quality=[],
            testing=[],
            security=[],
            devops=[],
            infrastructure=[],
        )

        assert bundle.project_identity == []
        assert bundle.code_quality == []
        assert bundle.metadata == {}

    def test_bundle_with_metadata(self) -> None:
        """Test bundle with metadata"""
        bundle = RecommendationBundle(
            project_identity=[],
            code_quality=[],
            testing=[],
            security=[],
            devops=[],
            infrastructure=[],
            metadata={"domain": "fintech", "total": 10},
        )

        assert bundle.metadata["domain"] == "fintech"
        assert bundle.metadata["total"] == 10


class TestRecommendationEngineInit:
    """Test RecommendationEngine initialization"""

    def test_init_with_minimal_results(self, minimal_detection_results: Dict[str, Any]) -> None:
        """Test initialization with minimal detection results"""
        engine = RecommendationEngine(minimal_detection_results)

        assert engine.domain == "default"
        assert engine.scale == "startup"
        assert engine.language == "python"

    def test_init_with_fintech_results(self, fintech_detection_results: Dict[str, Any]) -> None:
        """Test initialization with fintech detection results"""
        engine = RecommendationEngine(fintech_detection_results)

        assert engine.domain == "fintech"
        assert engine.scale == "enterprise"
        assert engine.language == "python"

    def test_init_domain_practices_loaded(self, minimal_detection_results: Dict[str, Any]) -> None:
        """Test domain practices are loaded correctly"""
        engine = RecommendationEngine(minimal_detection_results)

        assert engine.domain_practices == DOMAIN_BEST_PRACTICES["default"]

    def test_init_scale_practices_loaded(self, minimal_detection_results: Dict[str, Any]) -> None:
        """Test scale practices are loaded correctly"""
        engine = RecommendationEngine(minimal_detection_results)

        assert engine.scale_practices == SCALE_RECOMMENDATIONS["startup"]

    def test_init_language_practices_loaded(
        self, minimal_detection_results: Dict[str, Any]
    ) -> None:
        """Test language practices are loaded correctly"""
        engine = RecommendationEngine(minimal_detection_results)

        assert engine.language_practices == LANGUAGE_BEST_PRACTICES["python"]

    def test_init_with_unknown_domain(self) -> None:
        """Test initialization with unknown domain defaults to 'default'"""
        results = {
            "project_identity": {
                "domain": "unknown-domain",
                "scale": "startup",
                "primary_language": "python",
            }
        }
        engine = RecommendationEngine(results)

        assert engine.domain_practices == DOMAIN_BEST_PRACTICES["default"]

    def test_init_with_unknown_scale(self) -> None:
        """Test initialization with unknown scale defaults to 'startup'"""
        results = {
            "project_identity": {
                "domain": "default",
                "scale": "unknown-scale",
                "primary_language": "python",
            }
        }
        engine = RecommendationEngine(results)

        assert engine.scale_practices == SCALE_RECOMMENDATIONS["startup"]

    def test_init_with_unknown_language(self) -> None:
        """Test initialization with unknown language defaults to 'python'"""
        results = {
            "project_identity": {
                "domain": "default",
                "scale": "startup",
                "primary_language": "brainfuck",
            }
        }
        engine = RecommendationEngine(results)

        assert engine.language_practices == LANGUAGE_BEST_PRACTICES["python"]

    def test_init_with_non_string_domain(self) -> None:
        """Test initialization with non-string domain"""
        results = {
            "project_identity": {
                "domain": None,
                "scale": "startup",
                "primary_language": "python",
            }
        }
        engine = RecommendationEngine(results)

        assert engine.domain_practices == DOMAIN_BEST_PRACTICES["default"]

    def test_init_with_non_string_scale(self) -> None:
        """Test initialization with non-string scale"""
        results = {
            "project_identity": {
                "domain": "default",
                "scale": None,
                "primary_language": "python",
            }
        }
        engine = RecommendationEngine(results)

        assert engine.scale_practices == SCALE_RECOMMENDATIONS["startup"]

    def test_init_with_non_string_language(self) -> None:
        """Test initialization with non-string language"""
        results = {
            "project_identity": {
                "domain": "default",
                "scale": "startup",
                "primary_language": None,
            }
        }
        engine = RecommendationEngine(results)

        assert engine.language_practices == LANGUAGE_BEST_PRACTICES["python"]

    def test_init_with_missing_project_identity(self) -> None:
        """Test initialization with missing project_identity"""
        results: Dict[str, Any] = {}
        engine = RecommendationEngine(results)

        # Should use defaults
        assert engine.domain == "default"
        assert engine.scale == "startup"
        assert engine.language == "python"


class TestCalculateConfidence:
    """Test _calculate_confidence method"""

    def test_very_high_confidence(self, minimal_detection_results: Dict[str, Any]) -> None:
        """Test very high confidence calculation"""
        engine = RecommendationEngine(minimal_detection_results)

        confidence = engine._calculate_confidence(
            has_direct_evidence=True, signal_strength="strong", is_inference=False
        )

        assert confidence == ConfidenceLevel.VERY_HIGH.value

    def test_high_confidence(self, minimal_detection_results: Dict[str, Any]) -> None:
        """Test high confidence calculation"""
        engine = RecommendationEngine(minimal_detection_results)

        confidence = engine._calculate_confidence(
            has_direct_evidence=True, signal_strength="medium", is_inference=False
        )

        assert confidence == ConfidenceLevel.HIGH.value

    def test_medium_confidence(self, minimal_detection_results: Dict[str, Any]) -> None:
        """Test medium confidence calculation"""
        engine = RecommendationEngine(minimal_detection_results)

        confidence = engine._calculate_confidence(
            has_direct_evidence=False, signal_strength="medium", is_inference=False
        )

        assert confidence == ConfidenceLevel.MEDIUM.value

    def test_low_confidence(self, minimal_detection_results: Dict[str, Any]) -> None:
        """Test low confidence calculation"""
        engine = RecommendationEngine(minimal_detection_results)

        confidence = engine._calculate_confidence(
            has_direct_evidence=False, signal_strength="weak", is_inference=False
        )

        assert confidence == ConfidenceLevel.LOW.value

    def test_inference_reduces_confidence(self, minimal_detection_results: Dict[str, Any]) -> None:
        """Test that inference flag reduces confidence"""
        engine = RecommendationEngine(minimal_detection_results)

        base_confidence = engine._calculate_confidence(
            has_direct_evidence=True, signal_strength="strong", is_inference=False
        )

        inference_confidence = engine._calculate_confidence(
            has_direct_evidence=True, signal_strength="strong", is_inference=True
        )

        assert inference_confidence == base_confidence * 0.85
        assert inference_confidence < base_confidence


class TestRecommendProjectIdentity:
    """Test recommend_project_identity method"""

    def test_missing_project_type(self, missing_identity_results: Dict[str, Any]) -> None:
        """Test recommendation for missing project type"""
        engine = RecommendationEngine(missing_identity_results)
        recs = engine.recommend_project_identity()

        # Should recommend defining project type
        type_rec = [r for r in recs if "project type" in r.title.lower()]
        assert len(type_rec) == 1
        assert type_rec[0].priority == "medium"
        assert type_rec[0].category == "project-identity"

    def test_missing_domain(self, missing_identity_results: Dict[str, Any]) -> None:
        """Test recommendation for missing domain"""
        engine = RecommendationEngine(missing_identity_results)
        recs = engine.recommend_project_identity()

        # Should recommend specifying domain
        domain_rec = [r for r in recs if "domain" in r.title.lower()]
        assert len(domain_rec) == 1
        assert domain_rec[0].priority == "low"

    def test_missing_scale(self, missing_identity_results: Dict[str, Any]) -> None:
        """Test recommendation for missing scale"""
        engine = RecommendationEngine(missing_identity_results)
        recs = engine.recommend_project_identity()

        # Should recommend defining scale
        scale_rec = [r for r in recs if "scale" in r.title.lower()]
        assert len(scale_rec) == 1
        assert scale_rec[0].priority == "medium"

    def test_complete_identity_no_recommendations(
        self, complete_detection_results: Dict[str, Any]
    ) -> None:
        """Test no recommendations when identity is complete"""
        engine = RecommendationEngine(complete_detection_results)
        recs = engine.recommend_project_identity()

        # Should have no recommendations
        assert len(recs) == 0


class TestRecommendCodeQuality:
    """Test recommend_code_quality method"""

    def test_missing_formatter(self, minimal_detection_results: Dict[str, Any]) -> None:
        """Test recommendation for missing formatter"""
        engine = RecommendationEngine(minimal_detection_results)
        recs = engine.recommend_code_quality()

        # Should recommend formatter
        formatter_rec = [
            r for r in recs if "formatter" in r.title.lower() or "formatting" in r.title.lower()
        ]
        assert len(formatter_rec) == 1
        assert formatter_rec[0].priority == "high"
        assert "black" in formatter_rec[0].title.lower()

    def test_missing_linter(self, minimal_detection_results: Dict[str, Any]) -> None:
        """Test recommendation for missing linter"""
        engine = RecommendationEngine(minimal_detection_results)
        recs = engine.recommend_code_quality()

        # Should recommend linter
        linter_rec = [r for r in recs if "lint" in r.title.lower()]
        assert len(linter_rec) == 1
        assert linter_rec[0].priority == "high"

    def test_missing_type_checker(self, minimal_detection_results: Dict[str, Any]) -> None:
        """Test recommendation for missing type checker"""
        engine = RecommendationEngine(minimal_detection_results)
        recs = engine.recommend_code_quality()

        # Should recommend type checker
        type_rec = [r for r in recs if "type" in r.title.lower()]
        assert len(type_rec) == 1
        assert type_rec[0].priority == "medium"

    def test_complete_code_quality_no_recommendations(
        self, complete_detection_results: Dict[str, Any]
    ) -> None:
        """Test no recommendations when code quality tools are present"""
        engine = RecommendationEngine(complete_detection_results)
        recs = engine.recommend_code_quality()

        # Should have no recommendations
        assert len(recs) == 0

    def test_language_specific_recommendations(self) -> None:
        """Test language-specific tool recommendations"""
        # Test JavaScript
        js_results = {
            "project_identity": {
                "domain": "default",
                "scale": "startup",
                "primary_language": "javascript",
            },
            "code_quality": {},
        }
        engine = RecommendationEngine(js_results)
        recs = engine.recommend_code_quality()

        formatter_rec = [
            r for r in recs if "formatter" in r.title.lower() or "prettier" in r.title.lower()
        ]
        assert len(formatter_rec) == 1
        assert "prettier" in formatter_rec[0].title.lower()


class TestRecommendTesting:
    """Test recommend_testing method"""

    def test_missing_test_framework(self, minimal_detection_results: Dict[str, Any]) -> None:
        """Test recommendation for missing test framework"""
        engine = RecommendationEngine(minimal_detection_results)
        recs = engine.recommend_testing()

        # Should recommend test framework
        framework_rec = [
            r
            for r in recs
            if "test" in r.title.lower()
            and "framework" not in r.description.lower()
            or "pytest" in r.title.lower()
        ]
        assert len(framework_rec) >= 1
        # First should be critical priority
        assert any(r.priority == "critical" for r in recs)

    def test_low_coverage_recommendation(self) -> None:
        """Test recommendation for low test coverage"""
        results = {
            "project_identity": {
                "domain": "fintech",  # requires 95% coverage
                "scale": "startup",
                "primary_language": "python",
            },
            "testing": {
                "test_framework": "pytest",
                "test_coverage_percent": 50,
                "has_unit_tests": True,
                "has_integration_tests": False,
                "has_e2e_tests": False,
            },
        }
        engine = RecommendationEngine(results)
        recs = engine.recommend_testing()

        # Should recommend increasing coverage
        coverage_rec = [r for r in recs if "coverage" in r.title.lower()]
        assert len(coverage_rec) == 1
        assert "95%" in coverage_rec[0].title or "95%" in coverage_rec[0].description

    def test_missing_integration_tests_growth(self) -> None:
        """Test recommendation for integration tests at growth scale"""
        results = {
            "project_identity": {
                "domain": "default",
                "scale": "growth",
                "primary_language": "python",
            },
            "testing": {
                "test_framework": "pytest",
                "test_coverage_percent": 85,
                "has_unit_tests": True,
                "has_integration_tests": False,
                "has_e2e_tests": False,
            },
        }
        engine = RecommendationEngine(results)
        recs = engine.recommend_testing()

        # Should recommend integration tests
        integration_rec = [r for r in recs if "integration" in r.title.lower()]
        assert len(integration_rec) == 1
        assert integration_rec[0].priority == "high"

    def test_missing_e2e_tests_enterprise(self) -> None:
        """Test recommendation for E2E tests at enterprise scale"""
        results = {
            "project_identity": {
                "domain": "default",
                "scale": "enterprise",
                "primary_language": "python",
            },
            "testing": {
                "test_framework": "pytest",
                "test_coverage_percent": 90,
                "has_unit_tests": True,
                "has_integration_tests": True,
                "has_e2e_tests": False,
            },
        }
        engine = RecommendationEngine(results)
        recs = engine.recommend_testing()

        # Should recommend E2E tests
        e2e_rec = [r for r in recs if "e2e" in r.title.lower() or "end-to-end" in r.title.lower()]
        assert len(e2e_rec) == 1
        assert e2e_rec[0].priority == "medium"

    def test_no_integration_tests_startup_no_recommendation(self) -> None:
        """Test no integration test recommendation for startup scale"""
        results = {
            "project_identity": {
                "domain": "default",
                "scale": "startup",
                "primary_language": "python",
            },
            "testing": {
                "test_framework": "pytest",
                "test_coverage_percent": 85,
                "has_unit_tests": True,
                "has_integration_tests": False,
                "has_e2e_tests": False,
            },
        }
        engine = RecommendationEngine(results)
        recs = engine.recommend_testing()

        # Should not recommend integration tests for startup
        integration_rec = [r for r in recs if "integration" in r.title.lower()]
        assert len(integration_rec) == 0

    def test_coverage_priority_very_low(self) -> None:
        """Test high priority for very low coverage"""
        results = {
            "project_identity": {
                "domain": "default",  # 80% minimum
                "scale": "startup",
                "primary_language": "python",
            },
            "testing": {
                "test_framework": "pytest",
                "test_coverage_percent": 40,  # < 70% of minimum (56%)
                "has_unit_tests": True,
            },
        }
        engine = RecommendationEngine(results)
        recs = engine.recommend_testing()

        coverage_rec = [r for r in recs if "coverage" in r.title.lower()]
        assert len(coverage_rec) == 1
        assert coverage_rec[0].priority == "high"


class TestRecommendSecurity:
    """Test recommend_security method"""

    def test_missing_encryption_fintech(self, fintech_detection_results: Dict[str, Any]) -> None:
        """Test encryption recommendation for fintech"""
        engine = RecommendationEngine(fintech_detection_results)
        recs = engine.recommend_security()

        # Should recommend encryption
        encryption_rec = [r for r in recs if "encryption" in r.title.lower()]
        assert len(encryption_rec) >= 1
        assert encryption_rec[0].priority == "critical"

    def test_missing_secret_management_paranoid(
        self, fintech_detection_results: Dict[str, Any]
    ) -> None:
        """Test secret management recommendation for paranoid stance"""
        engine = RecommendationEngine(fintech_detection_results)
        recs = engine.recommend_security()

        # Should recommend secret management
        secret_rec = [r for r in recs if "secret" in r.title.lower()]
        assert len(secret_rec) >= 1
        assert secret_rec[0].priority == "critical"

    def test_missing_mfa_fintech(self, fintech_detection_results: Dict[str, Any]) -> None:
        """Test MFA recommendation for fintech"""
        engine = RecommendationEngine(fintech_detection_results)
        recs = engine.recommend_security()

        # Should recommend MFA
        mfa_rec = [r for r in recs if "mfa" in r.title.lower() or "multi-factor" in r.title.lower()]
        assert len(mfa_rec) >= 1
        assert mfa_rec[0].priority == "critical"

    def test_missing_audit_logging(self, fintech_detection_results: Dict[str, Any]) -> None:
        """Test audit logging recommendation"""
        engine = RecommendationEngine(fintech_detection_results)
        recs = engine.recommend_security()

        # Should recommend audit logging
        audit_rec = [r for r in recs if "audit" in r.title.lower()]
        assert len(audit_rec) >= 1
        assert audit_rec[0].priority == "high"

    def test_missing_dependency_scanning(self, minimal_detection_results: Dict[str, Any]) -> None:
        """Test dependency scanning recommendation"""
        engine = RecommendationEngine(minimal_detection_results)
        recs = engine.recommend_security()

        # Should recommend dependency scanning
        dep_rec = [r for r in recs if "dependency" in r.title.lower()]
        assert len(dep_rec) >= 1
        assert dep_rec[0].priority == "high"

    def test_complete_security_no_critical_recommendations(
        self, complete_detection_results: Dict[str, Any]
    ) -> None:
        """Test no critical recommendations when security is complete"""
        engine = RecommendationEngine(complete_detection_results)
        recs = engine.recommend_security()

        # May have some recommendations, but none should be critical
        critical_recs = [r for r in recs if r.priority == "critical"]
        assert len(critical_recs) == 0

    def test_standard_security_stance_no_mfa_requirement(self) -> None:
        """Test no MFA requirement for standard security stance"""
        results = {
            "project_identity": {
                "domain": "default",  # standard stance
                "scale": "startup",
                "primary_language": "python",
            },
            "security": {
                "mfa_enabled": False,
                "dependency_scanning": True,
            },
        }
        engine = RecommendationEngine(results)
        recs = engine.recommend_security()

        # Should not mandate MFA for standard stance
        mfa_rec = [r for r in recs if "mfa" in r.title.lower() and r.priority == "critical"]
        assert len(mfa_rec) == 0


class TestRecommendDevOps:
    """Test recommend_devops method"""

    def test_missing_ci_cd(self, minimal_detection_results: Dict[str, Any]) -> None:
        """Test CI/CD recommendation"""
        engine = RecommendationEngine(minimal_detection_results)
        recs = engine.recommend_devops()

        # Should recommend CI/CD
        ci_rec = [r for r in recs if "ci" in r.title.lower() or "pipeline" in r.title.lower()]
        assert len(ci_rec) >= 1
        assert ci_rec[0].priority == "high"

    def test_missing_deployment_validation(self) -> None:
        """Test deployment validation recommendation"""
        results = {
            "project_identity": {
                "domain": "fintech",  # requires canary/blue-green
                "scale": "enterprise",
                "primary_language": "python",
            },
            "devops": {
                "ci_cd_platform": "github-actions",
                "deployment_strategy": [],
                "monitoring": {},
            },
        }
        engine = RecommendationEngine(results)
        recs = engine.recommend_devops()

        # Should recommend deployment validation strategies
        deploy_recs = [
            r
            for r in recs
            if "deployment" in r.title.lower()
            or "canary" in r.title.lower()
            or "blue-green" in r.title.lower()
        ]
        assert len(deploy_recs) >= 1

    def test_missing_metrics(self) -> None:
        """Test metrics recommendation"""
        results = {
            "project_identity": {
                "domain": "saas",  # full-observability
                "scale": "growth",
                "primary_language": "python",
            },
            "devops": {
                "ci_cd_platform": "github-actions",
                "deployment_strategy": [],
                "monitoring": {"metrics": False, "logs": False, "traces": False},
            },
        }
        engine = RecommendationEngine(results)
        recs = engine.recommend_devops()

        # Should recommend metrics
        metrics_rec = [r for r in recs if "metrics" in r.title.lower()]
        assert len(metrics_rec) >= 1
        assert metrics_rec[0].priority == "high"

    def test_missing_traces(self) -> None:
        """Test distributed tracing recommendation"""
        results = {
            "project_identity": {
                "domain": "saas",  # full-observability
                "scale": "growth",
                "primary_language": "python",
            },
            "devops": {
                "ci_cd_platform": "github-actions",
                "deployment_strategy": [],
                "monitoring": {"metrics": True, "logs": True, "traces": False},
            },
        }
        engine = RecommendationEngine(results)
        recs = engine.recommend_devops()

        # Should recommend tracing
        trace_rec = [r for r in recs if "trac" in r.title.lower()]
        assert len(trace_rec) >= 1


class TestRecommendInfrastructure:
    """Test recommend_infrastructure method"""

    def test_missing_docker_growth(self) -> None:
        """Test Docker recommendation for growth scale"""
        results = {
            "project_identity": {
                "domain": "default",
                "scale": "growth",
                "primary_language": "python",
            },
            "infrastructure": {
                "containerization": {"docker": False},
                "orchestration": {},
                "database": {},
            },
        }
        engine = RecommendationEngine(results)
        recs = engine.recommend_infrastructure()

        # Should recommend Docker
        docker_rec = [
            r for r in recs if "docker" in r.title.lower() or "containerize" in r.title.lower()
        ]
        assert len(docker_rec) >= 1
        assert docker_rec[0].priority == "high"

    def test_no_docker_recommendation_startup(self) -> None:
        """Test no Docker recommendation for startup scale"""
        results = {
            "project_identity": {
                "domain": "default",
                "scale": "startup",
                "primary_language": "python",
            },
            "infrastructure": {
                "containerization": {"docker": False},
            },
        }
        engine = RecommendationEngine(results)
        recs = engine.recommend_infrastructure()

        # Should not recommend Docker for startup
        docker_rec = [r for r in recs if "docker" in r.title.lower()]
        assert len(docker_rec) == 0

    def test_missing_kubernetes_enterprise(self) -> None:
        """Test Kubernetes recommendation for enterprise"""
        results = {
            "project_identity": {
                "domain": "default",
                "scale": "enterprise",
                "primary_language": "python",
            },
            "infrastructure": {
                "containerization": {"docker": True},
                "orchestration": {"kubernetes": False},
            },
        }
        engine = RecommendationEngine(results)
        recs = engine.recommend_infrastructure()

        # Should recommend Kubernetes
        k8s_rec = [
            r for r in recs if "kubernetes" in r.title.lower() or "orchestration" in r.title.lower()
        ]
        assert len(k8s_rec) >= 1

    def test_missing_database_config(self, minimal_detection_results: Dict[str, Any]) -> None:
        """Test database strategy recommendation"""
        engine = RecommendationEngine(minimal_detection_results)
        recs = engine.recommend_infrastructure()

        # Should recommend database strategy
        db_rec = [r for r in recs if "database" in r.title.lower()]
        assert len(db_rec) >= 1

    def test_missing_backup_strategy(self) -> None:
        """Test backup strategy recommendation"""
        results = {
            "project_identity": {
                "domain": "fintech",  # requires real-time backups
                "scale": "enterprise",
                "primary_language": "python",
            },
            "infrastructure": {
                "backup_strategy": False,
            },
        }
        engine = RecommendationEngine(results)
        recs = engine.recommend_infrastructure()

        # Should recommend backup
        backup_rec = [r for r in recs if "backup" in r.title.lower()]
        assert len(backup_rec) >= 1
        assert backup_rec[0].priority == "critical"


class TestGenerateFullRecommendations:
    """Test generate_full_recommendations method"""

    def test_generates_bundle(self, minimal_detection_results: Dict[str, Any]) -> None:
        """Test full bundle generation"""
        engine = RecommendationEngine(minimal_detection_results)
        bundle = engine.generate_full_recommendations()

        assert isinstance(bundle, RecommendationBundle)
        assert isinstance(bundle.project_identity, list)
        assert isinstance(bundle.code_quality, list)
        assert isinstance(bundle.testing, list)
        assert isinstance(bundle.security, list)
        assert isinstance(bundle.devops, list)
        assert isinstance(bundle.infrastructure, list)

    def test_metadata_populated(self, minimal_detection_results: Dict[str, Any]) -> None:
        """Test metadata is populated correctly"""
        engine = RecommendationEngine(minimal_detection_results)
        bundle = engine.generate_full_recommendations()

        assert bundle.metadata["domain"] == "default"
        assert bundle.metadata["scale"] == "startup"
        assert bundle.metadata["language"] == "python"
        assert "total_recommendations" in bundle.metadata
        assert "engine_version" in bundle.metadata

    def test_total_recommendations_count(self, fintech_detection_results: Dict[str, Any]) -> None:
        """Test total recommendations count is accurate"""
        engine = RecommendationEngine(fintech_detection_results)
        bundle = engine.generate_full_recommendations()

        actual_total = (
            len(bundle.project_identity)
            + len(bundle.code_quality)
            + len(bundle.testing)
            + len(bundle.security)
            + len(bundle.devops)
            + len(bundle.infrastructure)
        )

        assert bundle.metadata["total_recommendations"] == actual_total


class TestPrioritizeRecommendations:
    """Test prioritize_recommendations function"""

    def test_prioritize_sorts_by_priority(self) -> None:
        """Test recommendations are sorted by priority"""
        rec1 = Recommendation(
            category="test",
            title="Low priority",
            description="desc",
            priority="low",
            confidence=0.9,
            reasoning=[],
            evidence=[],
            citations=[],
        )
        rec2 = Recommendation(
            category="test",
            title="Critical priority",
            description="desc",
            priority="critical",
            confidence=0.5,
            reasoning=[],
            evidence=[],
            citations=[],
        )
        rec3 = Recommendation(
            category="test",
            title="High priority",
            description="desc",
            priority="high",
            confidence=0.8,
            reasoning=[],
            evidence=[],
            citations=[],
        )

        bundle = RecommendationBundle(
            project_identity=[rec1],
            code_quality=[rec2],
            testing=[rec3],
            security=[],
            devops=[],
            infrastructure=[],
        )

        sorted_recs = prioritize_recommendations(bundle)

        assert len(sorted_recs) == 3
        assert sorted_recs[0].priority == "critical"
        assert sorted_recs[1].priority == "high"
        assert sorted_recs[2].priority == "low"

    def test_prioritize_sorts_by_confidence_within_priority(self) -> None:
        """Test recommendations are sorted by confidence within same priority"""
        rec1 = Recommendation(
            category="test",
            title="High 0.9",
            description="desc",
            priority="high",
            confidence=0.9,
            reasoning=[],
            evidence=[],
            citations=[],
        )
        rec2 = Recommendation(
            category="test",
            title="High 0.7",
            description="desc",
            priority="high",
            confidence=0.7,
            reasoning=[],
            evidence=[],
            citations=[],
        )

        bundle = RecommendationBundle(
            project_identity=[rec2, rec1],
            code_quality=[],
            testing=[],
            security=[],
            devops=[],
            infrastructure=[],
        )

        sorted_recs = prioritize_recommendations(bundle)

        assert len(sorted_recs) == 2
        assert sorted_recs[0].confidence == 0.9
        assert sorted_recs[1].confidence == 0.7

    def test_prioritize_empty_bundle(self) -> None:
        """Test prioritizing empty bundle"""
        bundle = RecommendationBundle(
            project_identity=[],
            code_quality=[],
            testing=[],
            security=[],
            devops=[],
            infrastructure=[],
        )

        sorted_recs = prioritize_recommendations(bundle)

        assert len(sorted_recs) == 0


class TestFilterRecommendations:
    """Test filter_recommendations function"""

    def test_filter_by_min_confidence(self) -> None:
        """Test filtering by minimum confidence"""
        rec1 = Recommendation(
            category="test",
            title="High conf",
            description="desc",
            priority="high",
            confidence=0.9,
            reasoning=[],
            evidence=[],
            citations=[],
        )
        rec2 = Recommendation(
            category="test",
            title="Low conf",
            description="desc",
            priority="high",
            confidence=0.5,
            reasoning=[],
            evidence=[],
            citations=[],
        )

        bundle = RecommendationBundle(
            project_identity=[rec1, rec2],
            code_quality=[],
            testing=[],
            security=[],
            devops=[],
            infrastructure=[],
        )

        filtered = filter_recommendations(bundle, min_confidence=0.7)

        assert len(filtered) == 1
        assert filtered[0].confidence == 0.9

    def test_filter_by_categories(self) -> None:
        """Test filtering by categories"""
        rec1 = Recommendation(
            category="security",
            title="Security rec",
            description="desc",
            priority="high",
            confidence=0.9,
            reasoning=[],
            evidence=[],
            citations=[],
        )
        rec2 = Recommendation(
            category="testing",
            title="Testing rec",
            description="desc",
            priority="high",
            confidence=0.9,
            reasoning=[],
            evidence=[],
            citations=[],
        )

        bundle = RecommendationBundle(
            project_identity=[],
            code_quality=[],
            testing=[rec2],
            security=[rec1],
            devops=[],
            infrastructure=[],
        )

        filtered = filter_recommendations(bundle, categories=["security"])

        assert len(filtered) == 1
        assert filtered[0].category == "security"

    def test_filter_by_priorities(self) -> None:
        """Test filtering by priorities"""
        rec1 = Recommendation(
            category="test",
            title="Critical",
            description="desc",
            priority="critical",
            confidence=0.9,
            reasoning=[],
            evidence=[],
            citations=[],
        )
        rec2 = Recommendation(
            category="test",
            title="Low",
            description="desc",
            priority="low",
            confidence=0.9,
            reasoning=[],
            evidence=[],
            citations=[],
        )

        bundle = RecommendationBundle(
            project_identity=[rec1, rec2],
            code_quality=[],
            testing=[],
            security=[],
            devops=[],
            infrastructure=[],
        )

        filtered = filter_recommendations(bundle, priorities=["critical", "high"])

        assert len(filtered) == 1
        assert filtered[0].priority == "critical"

    def test_filter_combined_criteria(self) -> None:
        """Test filtering with multiple criteria"""
        rec1 = Recommendation(
            category="security",
            title="Security critical",
            description="desc",
            priority="critical",
            confidence=0.9,
            reasoning=[],
            evidence=[],
            citations=[],
        )
        rec2 = Recommendation(
            category="security",
            title="Security low",
            description="desc",
            priority="low",
            confidence=0.5,
            reasoning=[],
            evidence=[],
            citations=[],
        )
        rec3 = Recommendation(
            category="testing",
            title="Testing critical",
            description="desc",
            priority="critical",
            confidence=0.9,
            reasoning=[],
            evidence=[],
            citations=[],
        )

        bundle = RecommendationBundle(
            project_identity=[],
            code_quality=[],
            testing=[rec3],
            security=[rec1, rec2],
            devops=[],
            infrastructure=[],
        )

        filtered = filter_recommendations(
            bundle, min_confidence=0.7, categories=["security"], priorities=["critical"]
        )

        assert len(filtered) == 1
        assert filtered[0].category == "security"
        assert filtered[0].priority == "critical"
        assert filtered[0].confidence >= 0.7

    def test_filter_no_criteria_returns_all(self) -> None:
        """Test filtering with no criteria returns all recommendations"""
        rec1 = Recommendation(
            category="test",
            title="Rec 1",
            description="desc",
            priority="high",
            confidence=0.9,
            reasoning=[],
            evidence=[],
            citations=[],
        )

        bundle = RecommendationBundle(
            project_identity=[rec1],
            code_quality=[],
            testing=[],
            security=[],
            devops=[],
            infrastructure=[],
        )

        filtered = filter_recommendations(bundle)

        assert len(filtered) == 1


class TestFormatRecommendationMarkdown:
    """Test format_recommendation_markdown function"""

    def test_format_basic_recommendation(self) -> None:
        """Test formatting basic recommendation"""
        rec = Recommendation(
            category="security",
            title="Enable encryption",
            description="Encrypt data at rest",
            priority="critical",
            confidence=0.95,
            reasoning=["Protects data"],
            evidence=["Domain: fintech"],
            citations=["OWASP"],
        )

        md = format_recommendation_markdown(rec)

        assert "### Enable encryption" in md
        assert "**Category:** security" in md
        assert "**Priority:** CRITICAL" in md
        assert "**Confidence:** 95%" in md
        assert "Encrypt data at rest" in md
        assert "Protects data" in md
        assert "Domain: fintech" in md
        assert "OWASP" in md

    def test_format_with_optional_fields(self) -> None:
        """Test formatting with optional fields"""
        rec = Recommendation(
            category="testing",
            title="Add tests",
            description="Increase coverage",
            priority="high",
            confidence=0.85,
            reasoning=["Improves quality"],
            evidence=["Current: 50%"],
            citations=["Testing best practices"],
            implementation_notes="Start with critical paths",
            estimated_effort="3d",
        )

        md = format_recommendation_markdown(rec)

        assert "**Implementation:** Start with critical paths" in md
        assert "**Estimated effort:** 3d" in md

    def test_format_without_optional_fields(self) -> None:
        """Test formatting without optional fields"""
        rec = Recommendation(
            category="test",
            title="Title",
            description="Description",
            priority="medium",
            confidence=0.7,
            reasoning=[],
            evidence=[],
            citations=[],
        )

        md = format_recommendation_markdown(rec)

        assert "### Title" in md
        assert "Description" in md
        # Should not have empty sections
        assert "**Reasoning:**" not in md
        assert "**Evidence:**" not in md
        assert "**References:**" not in md

    def test_format_multiple_reasoning_items(self) -> None:
        """Test formatting with multiple reasoning items"""
        rec = Recommendation(
            category="test",
            title="Title",
            description="Description",
            priority="high",
            confidence=0.8,
            reasoning=["Reason 1", "Reason 2", "Reason 3"],
            evidence=["Evidence 1", "Evidence 2"],
            citations=["Citation 1"],
        )

        md = format_recommendation_markdown(rec)

        assert "- Reason 1" in md
        assert "- Reason 2" in md
        assert "- Reason 3" in md
        assert "- Evidence 1" in md
        assert "- Evidence 2" in md
        assert "- Citation 1" in md


class TestKnowledgeBaseTables:
    """Test knowledge base lookup tables exist and are structured correctly"""

    def test_domain_best_practices_exists(self) -> None:
        """Test DOMAIN_BEST_PRACTICES table exists"""
        assert DOMAIN_BEST_PRACTICES is not None
        assert isinstance(DOMAIN_BEST_PRACTICES, dict)
        assert len(DOMAIN_BEST_PRACTICES) > 0

    def test_domain_best_practices_has_default(self) -> None:
        """Test default domain exists"""
        assert "default" in DOMAIN_BEST_PRACTICES

    def test_scale_recommendations_exists(self) -> None:
        """Test SCALE_RECOMMENDATIONS table exists"""
        assert SCALE_RECOMMENDATIONS is not None
        assert isinstance(SCALE_RECOMMENDATIONS, dict)
        assert "startup" in SCALE_RECOMMENDATIONS
        assert "enterprise" in SCALE_RECOMMENDATIONS

    def test_language_best_practices_exists(self) -> None:
        """Test LANGUAGE_BEST_PRACTICES table exists"""
        assert LANGUAGE_BEST_PRACTICES is not None
        assert isinstance(LANGUAGE_BEST_PRACTICES, dict)
        assert "python" in LANGUAGE_BEST_PRACTICES

    def test_security_stance_requirements_exists(self) -> None:
        """Test SECURITY_STANCE_REQUIREMENTS table exists"""
        assert SECURITY_STANCE_REQUIREMENTS is not None
        assert isinstance(SECURITY_STANCE_REQUIREMENTS, dict)
        assert "standard" in SECURITY_STANCE_REQUIREMENTS
        assert "paranoid" in SECURITY_STANCE_REQUIREMENTS

    def test_monitoring_level_requirements_exists(self) -> None:
        """Test MONITORING_LEVEL_REQUIREMENTS table exists"""
        assert MONITORING_LEVEL_REQUIREMENTS is not None
        assert isinstance(MONITORING_LEVEL_REQUIREMENTS, dict)
        assert "basic" in MONITORING_LEVEL_REQUIREMENTS
        assert "full-observability" in MONITORING_LEVEL_REQUIREMENTS

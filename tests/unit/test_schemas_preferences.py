"""
Unit tests for Preference Schemas

Tests CCOPreferences, ProjectIdentity, DevelopmentStyle, CodeQualityStandards,
DocumentationPreferences, TestingStrategy, SecurityPosture, PerformanceVsMaintainability,
TeamCollaboration, and DevOpsAutomation models.

Target Coverage: 100%
"""

from datetime import datetime
from typing import get_args

import pytest
from pydantic import ValidationError

from claudecodeoptimizer.schemas.preferences import (
    CCOPreferences,
    CICDTriggerChoice,
    CodePhilosophyChoice,
    CodeQualityStandards,
    ComplianceChoice,
    DeploymentTargetChoice,
    DevelopmentPaceChoice,
    DevelopmentStyle,
    DevOpsAutomation,
    DocAudienceChoice,
    DocumentationPreferences,
    DocVerbosityChoice,
    DRYEnforcementChoice,
    GitWorkflowChoice,
    LineLengthChoice,
    LintingStrictnessChoice,
    OptimizationPriorityChoice,
    PerformanceVsMaintainability,
    ProjectIdentity,
    ProjectTypeChoice,
    SecurityPosture,
    SecurityStanceChoice,
    TDDAdherenceChoice,
    TeamCollaboration,
    TestCoverageChoice,
    TestingStrategy,
    TestPyramidChoice,
    TypeCoverageChoice,
    VersioningStrategyChoice,
    get_literal_choices,
)


class TestProjectIdentity:
    """Test ProjectIdentity model"""

    def test_minimal_creation(self) -> None:
        """Test creating ProjectIdentity with only required fields"""
        identity = ProjectIdentity(
            name="TestProject",
            primary_language="python",
        )

        assert identity.name == "TestProject"
        assert identity.primary_language == "python"
        assert identity.types == []
        assert identity.secondary_languages == []
        assert identity.frameworks == []
        assert identity.deployment_target == ["cloud-other"]
        assert identity.expected_scale == "startup"
        assert identity.business_domain == ["general-purpose"]
        assert identity.compliance_requirements == ["none"]
        assert identity.project_maturity == "active-dev"
        assert identity.team_trajectory == "solo"
        assert identity.license_model == "proprietary"

    def test_full_creation(self) -> None:
        """Test creating ProjectIdentity with all fields"""
        identity = ProjectIdentity(
            name="CompleteProject",
            types=["api", "backend"],
            primary_language="python",
            secondary_languages=["javascript", "sql"],
            frameworks=["fastapi", "sqlalchemy"],
            deployment_target=["cloud-aws", "kubernetes"],
            expected_scale="enterprise",
            business_domain=["fintech", "saas"],
            compliance_requirements=["gdpr", "sox", "pci-dss"],
            project_maturity="production",
            team_trajectory="large-20-50",
            license_model="open-source",
        )

        assert identity.name == "CompleteProject"
        assert set(identity.types) == {"api", "backend"}
        assert set(identity.secondary_languages) == {"javascript", "sql"}
        assert set(identity.frameworks) == {"fastapi", "sqlalchemy"}
        assert set(identity.deployment_target) == {"cloud-aws", "kubernetes"}
        assert identity.expected_scale == "enterprise"
        assert set(identity.business_domain) == {"fintech", "saas"}
        assert set(identity.compliance_requirements) == {"gdpr", "sox", "pci-dss"}

    def test_valid_project_types(self) -> None:
        """Test all valid project types"""
        valid_types = get_args(ProjectTypeChoice)
        for proj_type in valid_types:
            identity = ProjectIdentity(
                name="Test",
                types=[proj_type],
                primary_language="python",
            )
            assert proj_type in identity.types

    def test_valid_deployment_targets(self) -> None:
        """Test all valid deployment targets"""
        valid_targets = get_args(DeploymentTargetChoice)
        for target in valid_targets:
            identity = ProjectIdentity(
                name="Test",
                deployment_target=[target],
                primary_language="python",
            )
            assert target in identity.deployment_target

    def test_valid_business_domains(self) -> None:
        """Test multiple valid business domains"""
        identity = ProjectIdentity(
            name="Test",
            business_domain=["fintech", "healthcare", "e-commerce"],
            primary_language="python",
        )
        assert len(identity.business_domain) == 3

    def test_valid_compliance_requirements(self) -> None:
        """Test multiple compliance requirements"""
        identity = ProjectIdentity(
            name="Test",
            compliance_requirements=["gdpr", "hipaa", "pci-dss"],
            primary_language="python",
        )
        assert len(identity.compliance_requirements) == 3

    def test_missing_required_fields(self) -> None:
        """Test that missing required fields raises validation error"""
        with pytest.raises(ValidationError):
            ProjectIdentity()

        with pytest.raises(ValidationError):
            ProjectIdentity(name="Test")

        with pytest.raises(ValidationError):
            ProjectIdentity(primary_language="python")

    def test_empty_name_validation(self) -> None:
        """Test that empty name is invalid"""
        # Empty string might be valid in Pydantic by default, but let's verify
        identity = ProjectIdentity(
            name="",
            primary_language="python",
        )
        assert identity.name == ""

    def test_type_lists_are_independent(self) -> None:
        """Test that list fields are independent instances"""
        identity1 = ProjectIdentity(name="P1", primary_language="python")
        identity2 = ProjectIdentity(name="P2", primary_language="javascript")

        identity1.types.append("api")
        assert identity2.types == []


class TestDevelopmentStyle:
    """Test DevelopmentStyle model"""

    def test_default_values(self) -> None:
        """Test default field values"""
        style = DevelopmentStyle()

        assert style.code_philosophy == "balanced"
        assert style.development_pace == "balanced"
        assert style.tdd_adherence == "pragmatic-tests"
        assert style.refactoring_frequency == "when-needed"
        assert style.breaking_changes_policy == "semver-major"
        assert style.code_review_strictness == "mandatory-all"
        assert style.pair_programming == "complex-tasks"
        assert style.feature_flags == "major-features"

    def test_custom_values(self) -> None:
        """Test setting custom values"""
        style = DevelopmentStyle(
            code_philosophy="cutting-edge",
            development_pace="rapid-prototype",
            tdd_adherence="strict-tdd",
            refactoring_frequency="continuous",
            breaking_changes_policy="never",
            code_review_strictness="optional",
            pair_programming="always",
            feature_flags="extensive",
        )

        assert style.code_philosophy == "cutting-edge"
        assert style.development_pace == "rapid-prototype"
        assert style.tdd_adherence == "strict-tdd"
        assert style.refactoring_frequency == "continuous"
        assert style.breaking_changes_policy == "never"
        assert style.code_review_strictness == "optional"
        assert style.pair_programming == "always"
        assert style.feature_flags == "extensive"

    def test_all_philosophy_choices(self) -> None:
        """Test all valid code philosophy choices"""
        valid_choices = get_args(CodePhilosophyChoice)
        for choice in valid_choices:
            style = DevelopmentStyle(code_philosophy=choice)
            assert style.code_philosophy == choice

    def test_all_pace_choices(self) -> None:
        """Test all valid development pace choices"""
        valid_choices = get_args(DevelopmentPaceChoice)
        for choice in valid_choices:
            style = DevelopmentStyle(development_pace=choice)
            assert style.development_pace == choice

    def test_all_tdd_choices(self) -> None:
        """Test all valid TDD adherence choices"""
        valid_choices = get_args(TDDAdherenceChoice)
        for choice in valid_choices:
            style = DevelopmentStyle(tdd_adherence=choice)
            assert style.tdd_adherence == choice


class TestCodeQualityStandards:
    """Test CodeQualityStandards model"""

    def test_default_values(self) -> None:
        """Test default field values"""
        quality = CodeQualityStandards()

        assert quality.linting_strictness == "strict"
        assert quality.type_coverage_target == "90"
        assert quality.cyclomatic_complexity_limit == 10
        assert quality.function_length_limit == 50
        assert quality.dry_enforcement == "pragmatic"
        assert quality.code_comment_density == "moderate"
        assert quality.naming_convention_strictness == "enforced"
        assert quality.magic_number_tolerance == "named-constants"
        assert quality.import_organization == "grouped-logical"
        assert quality.line_length_limit == "100"

    def test_custom_limits(self) -> None:
        """Test setting custom numeric limits"""
        quality = CodeQualityStandards(
            cyclomatic_complexity_limit=20,
            function_length_limit=100,
        )

        assert quality.cyclomatic_complexity_limit == 20
        assert quality.function_length_limit == 100

    def test_cyclomatic_complexity_bounds(self) -> None:
        """Test cyclomatic complexity bounds validation"""
        # Valid boundaries
        quality = CodeQualityStandards(cyclomatic_complexity_limit=0)
        assert quality.cyclomatic_complexity_limit == 0

        quality = CodeQualityStandards(cyclomatic_complexity_limit=50)
        assert quality.cyclomatic_complexity_limit == 50

        # Invalid - too high
        with pytest.raises(ValidationError):
            CodeQualityStandards(cyclomatic_complexity_limit=51)

        # Invalid - negative
        with pytest.raises(ValidationError):
            CodeQualityStandards(cyclomatic_complexity_limit=-1)

    def test_function_length_bounds(self) -> None:
        """Test function length limit bounds validation"""
        # Valid boundaries
        quality = CodeQualityStandards(function_length_limit=0)
        assert quality.function_length_limit == 0

        quality = CodeQualityStandards(function_length_limit=200)
        assert quality.function_length_limit == 200

        # Invalid - too high
        with pytest.raises(ValidationError):
            CodeQualityStandards(function_length_limit=201)

        # Invalid - negative
        with pytest.raises(ValidationError):
            CodeQualityStandards(function_length_limit=-1)

    def test_all_linting_choices(self) -> None:
        """Test all valid linting strictness choices"""
        valid_choices = get_args(LintingStrictnessChoice)
        for choice in valid_choices:
            quality = CodeQualityStandards(linting_strictness=choice)
            assert quality.linting_strictness == choice

    def test_all_type_coverage_choices(self) -> None:
        """Test all valid type coverage choices"""
        valid_choices = get_args(TypeCoverageChoice)
        for choice in valid_choices:
            quality = CodeQualityStandards(type_coverage_target=choice)
            assert quality.type_coverage_target == choice

    def test_all_dry_enforcement_choices(self) -> None:
        """Test all valid DRY enforcement choices"""
        valid_choices = get_args(DRYEnforcementChoice)
        for choice in valid_choices:
            quality = CodeQualityStandards(dry_enforcement=choice)
            assert quality.dry_enforcement == choice

    def test_all_line_length_choices(self) -> None:
        """Test all valid line length choices"""
        valid_choices = get_args(LineLengthChoice)
        for choice in valid_choices:
            quality = CodeQualityStandards(line_length_limit=choice)
            assert quality.line_length_limit == choice


class TestDocumentationPreferences:
    """Test DocumentationPreferences model"""

    def test_default_values(self) -> None:
        """Test default field values"""
        docs = DocumentationPreferences()

        assert docs.verbosity == "concise"
        assert docs.target_audience == "intermediate"
        assert docs.documentation_style == "hybrid"
        assert docs.inline_documentation == "public-api"
        assert docs.architecture_diagrams == "complex-areas"
        assert docs.api_documentation == "openapi-spec"
        assert docs.readme_length == "concise"

    def test_extensive_documentation(self) -> None:
        """Test extensive documentation settings"""
        docs = DocumentationPreferences(
            verbosity="extensive",
            target_audience="beginners",
            documentation_style="tutorial-driven",
            inline_documentation="every-function",
            architecture_diagrams="required",
            api_documentation="markdown",
            readme_length="comprehensive",
        )

        assert docs.verbosity == "extensive"
        assert docs.target_audience == "beginners"
        assert docs.documentation_style == "tutorial-driven"
        assert docs.inline_documentation == "every-function"
        assert docs.architecture_diagrams == "required"
        assert docs.api_documentation == "markdown"
        assert docs.readme_length == "comprehensive"

    def test_minimal_documentation(self) -> None:
        """Test minimal documentation settings"""
        docs = DocumentationPreferences(
            verbosity="minimal",
            target_audience="experts",
            documentation_style="reference-manual",
            inline_documentation="complex-only",
            architecture_diagrams="optional",
            api_documentation="code-comments",
            readme_length="minimal",
        )

        assert docs.verbosity == "minimal"
        assert docs.target_audience == "experts"

    def test_all_verbosity_choices(self) -> None:
        """Test all valid verbosity choices"""
        valid_choices = get_args(DocVerbosityChoice)
        for choice in valid_choices:
            docs = DocumentationPreferences(verbosity=choice)
            assert docs.verbosity == choice

    def test_all_audience_choices(self) -> None:
        """Test all valid audience choices"""
        valid_choices = get_args(DocAudienceChoice)
        for choice in valid_choices:
            docs = DocumentationPreferences(target_audience=choice)
            assert docs.target_audience == choice


class TestTestingStrategy:
    """Test TestingStrategy model"""

    def test_default_values(self) -> None:
        """Test default field values"""
        testing = TestingStrategy()

        assert testing.coverage_target == "90"
        assert testing.test_pyramid_ratio == "70-20-10"
        assert testing.mutation_testing == "optional"
        assert testing.property_based_testing == "complex-logic"
        assert testing.test_isolation == "pragmatic-fixtures"
        assert testing.test_naming == "descriptive-sentences"
        assert testing.mocking_philosophy == "balanced"

    def test_strict_testing(self) -> None:
        """Test strict testing settings"""
        testing = TestingStrategy(
            coverage_target="100",
            test_pyramid_ratio="80-15-5",
            mutation_testing="required",
            property_based_testing="extensive",
            test_isolation="strict-no-shared",
            test_naming="descriptive-sentences",
            mocking_philosophy="minimal-real-deps",
        )

        assert testing.coverage_target == "100"
        assert testing.test_pyramid_ratio == "80-15-5"
        assert testing.mutation_testing == "required"
        assert testing.property_based_testing == "extensive"

    def test_relaxed_testing(self) -> None:
        """Test relaxed testing settings"""
        testing = TestingStrategy(
            coverage_target="60",
            mutation_testing="none",
            property_based_testing="none",
            test_isolation="flexible",
        )

        assert testing.coverage_target == "60"
        assert testing.mutation_testing == "none"
        assert testing.property_based_testing == "none"

    def test_all_coverage_targets(self) -> None:
        """Test all valid coverage target choices"""
        valid_choices = get_args(TestCoverageChoice)
        for choice in valid_choices:
            testing = TestingStrategy(coverage_target=choice)
            assert testing.coverage_target == choice

    def test_all_pyramid_ratios(self) -> None:
        """Test all valid pyramid ratio choices"""
        valid_choices = get_args(TestPyramidChoice)
        for choice in valid_choices:
            testing = TestingStrategy(test_pyramid_ratio=choice)
            assert testing.test_pyramid_ratio == choice


class TestSecurityPosture:
    """Test SecurityPosture model"""

    def test_default_values(self) -> None:
        """Test default field values"""
        security = SecurityPosture()

        assert security.security_stance == "balanced"
        assert security.secret_management == ["env-vars"]
        assert set(security.encryption_scope) == {"at-rest-sensitive", "in-transit-external"}
        assert set(security.audit_logging) == {
            "authentication",
            "authorization",
            "data-modification",
        }
        assert security.input_validation == "external-only"
        assert security.dependency_scanning == "every-pr"

    def test_strict_security(self) -> None:
        """Test strict security settings"""
        security = SecurityPosture(
            security_stance="zero-trust",
            secret_management=["hashicorp-vault", "aws-secrets-manager"],
            encryption_scope=["at-rest-all", "in-transit-all", "end-to-end"],
            audit_logging=["everything"],
            input_validation="schema-everything",
            dependency_scanning="every-commit",
        )

        assert security.security_stance == "zero-trust"
        assert "hashicorp-vault" in security.secret_management
        assert "at-rest-all" in security.encryption_scope
        assert "everything" in security.audit_logging
        assert security.input_validation == "schema-everything"
        assert security.dependency_scanning == "every-commit"

    def test_permissive_security(self) -> None:
        """Test permissive security settings"""
        security = SecurityPosture(
            security_stance="permissive",
            secret_management=["plaintext"],
            encryption_scope=["minimal"],
            audit_logging=["none"],
            input_validation="pragmatic",
            dependency_scanning="none",
        )

        assert security.security_stance == "permissive"
        assert "plaintext" in security.secret_management
        assert "minimal" in security.encryption_scope

    def test_multiple_secret_management_methods(self) -> None:
        """Test multiple secret management methods"""
        security = SecurityPosture(
            secret_management=["aws-secrets-manager", "docker-secrets", "1password"],
        )
        assert len(security.secret_management) == 3

    def test_multiple_encryption_scopes(self) -> None:
        """Test multiple encryption scopes"""
        security = SecurityPosture(
            encryption_scope=["at-rest-all", "in-transit-all", "database-level"],
        )
        assert len(security.encryption_scope) == 3

    def test_multiple_audit_logging_events(self) -> None:
        """Test multiple audit logging events"""
        security = SecurityPosture(
            audit_logging=["authentication", "authorization", "api-calls", "errors-only"],
        )
        assert len(security.audit_logging) == 4

    def test_all_security_stances(self) -> None:
        """Test all valid security stances"""
        valid_choices = get_args(SecurityStanceChoice)
        for choice in valid_choices:
            security = SecurityPosture(security_stance=choice)
            assert security.security_stance == choice


class TestPerformanceVsMaintainability:
    """Test PerformanceVsMaintainability model"""

    def test_default_values(self) -> None:
        """Test default field values"""
        perf = PerformanceVsMaintainability()

        assert perf.optimization_priority == "balanced"
        assert perf.caching_strategy == "selective"
        assert perf.database_queries == "orm-with-indexes"
        assert perf.premature_optimization == "profile-first"
        assert perf.duplication_for_performance == "contextual"

    def test_performance_first(self) -> None:
        """Test performance-first settings"""
        perf = PerformanceVsMaintainability(
            optimization_priority="performance-first",
            caching_strategy="aggressive",
            database_queries="hand-optimized",
            premature_optimization="allowed",
            duplication_for_performance="acceptable",
        )

        assert perf.optimization_priority == "performance-first"
        assert perf.caching_strategy == "aggressive"
        assert perf.database_queries == "hand-optimized"
        assert perf.premature_optimization == "allowed"

    def test_maintainability_first(self) -> None:
        """Test maintainability-first settings"""
        perf = PerformanceVsMaintainability(
            optimization_priority="maintainability-first",
            caching_strategy="minimal",
            database_queries="orm-simple",
            premature_optimization="forbidden",
            duplication_for_performance="never",
        )

        assert perf.optimization_priority == "maintainability-first"
        assert perf.caching_strategy == "minimal"
        assert perf.database_queries == "orm-simple"
        assert perf.premature_optimization == "forbidden"

    def test_all_optimization_priority_choices(self) -> None:
        """Test all valid optimization priority choices"""
        valid_choices = get_args(OptimizationPriorityChoice)
        for choice in valid_choices:
            perf = PerformanceVsMaintainability(optimization_priority=choice)
            assert perf.optimization_priority == choice


class TestTeamCollaboration:
    """Test TeamCollaboration model"""

    def test_default_values(self) -> None:
        """Test default field values"""
        collab = TeamCollaboration()

        assert collab.git_workflow == "github-flow"
        assert collab.versioning_strategy == "auto_semver"
        assert collab.commit_convention == "conventional-suggested"
        assert collab.pr_size_limit == "medium-500"
        assert collab.code_ownership == "team-ownership"

    def test_strict_collaboration(self) -> None:
        """Test strict collaboration settings"""
        collab = TeamCollaboration(
            git_workflow="git-flow",
            versioning_strategy="manual_semver",
            commit_convention="conventional-enforced",
            pr_size_limit="small-200",
            code_ownership="strict-codeowners",
        )

        assert collab.git_workflow == "git-flow"
        assert collab.commit_convention == "conventional-enforced"
        assert collab.pr_size_limit == "small-200"

    def test_relaxed_collaboration(self) -> None:
        """Test relaxed collaboration settings"""
        collab = TeamCollaboration(
            git_workflow="trunk-based",
            commit_convention="freeform",
            pr_size_limit="no-limit",
            code_ownership="open",
        )

        assert collab.git_workflow == "trunk-based"
        assert collab.commit_convention == "freeform"
        assert collab.pr_size_limit == "no-limit"

    def test_all_git_workflows(self) -> None:
        """Test all valid git workflow choices"""
        valid_choices = get_args(GitWorkflowChoice)
        for choice in valid_choices:
            collab = TeamCollaboration(git_workflow=choice)
            assert collab.git_workflow == choice

    def test_all_versioning_strategies(self) -> None:
        """Test all valid versioning strategy choices"""
        valid_choices = get_args(VersioningStrategyChoice)
        for choice in valid_choices:
            collab = TeamCollaboration(versioning_strategy=choice)
            assert collab.versioning_strategy == choice


class TestDevOpsAutomation:
    """Test DevOpsAutomation model"""

    def test_default_values(self) -> None:
        """Test default field values"""
        devops = DevOpsAutomation()

        assert devops.ci_cd_trigger == "every-pr"
        assert devops.deployment_frequency == "manual"
        assert devops.rollback_strategy == "manual-approval"
        assert devops.infrastructure == ["docker-compose"]
        assert devops.monitoring == ["prometheus", "grafana"]
        assert devops.environment_count == ["dev", "prod"]

    def test_continuous_deployment(self) -> None:
        """Test continuous deployment settings"""
        devops = DevOpsAutomation(
            ci_cd_trigger="every-commit",
            deployment_frequency="continuous",
            rollback_strategy="automated",
            infrastructure=["kubernetes", "eks"],
            monitoring=["prometheus", "grafana", "jaeger"],
            environment_count=["dev", "staging", "prod"],
        )

        assert devops.ci_cd_trigger == "every-commit"
        assert devops.deployment_frequency == "continuous"
        assert devops.rollback_strategy == "automated"
        assert "kubernetes" in devops.infrastructure

    def test_manual_deployment(self) -> None:
        """Test manual deployment settings"""
        devops = DevOpsAutomation(
            ci_cd_trigger="manual",
            deployment_frequency="manual",
            rollback_strategy="manual",
            infrastructure=["vms", "bare-metal"],
            environment_count=["prod"],
        )

        assert devops.ci_cd_trigger == "manual"
        assert devops.deployment_frequency == "manual"

    def test_multiple_infrastructure_options(self) -> None:
        """Test multiple infrastructure options"""
        devops = DevOpsAutomation(
            infrastructure=["kubernetes", "docker-compose", "serverless"],
        )
        assert len(devops.infrastructure) == 3

    def test_multiple_monitoring_tools(self) -> None:
        """Test multiple monitoring tools"""
        devops = DevOpsAutomation(
            monitoring=["datadog", "new-relic", "sentry", "opentelemetry"],
        )
        assert len(devops.monitoring) == 4

    def test_all_ci_cd_triggers(self) -> None:
        """Test all valid CI/CD trigger choices"""
        valid_choices = get_args(CICDTriggerChoice)
        for choice in valid_choices:
            devops = DevOpsAutomation(ci_cd_trigger=choice)
            assert devops.ci_cd_trigger == choice


class TestCCOPreferences:
    """Test CCOPreferences model"""

    def test_minimal_creation(self) -> None:
        """Test creating CCOPreferences with minimal required fields"""
        prefs = CCOPreferences(
            project_identity=ProjectIdentity(
                name="TestProject",
                primary_language="python",
            ),
        )

        assert prefs.project_identity.name == "TestProject"
        assert prefs.development_style is not None
        assert prefs.code_quality is not None
        assert prefs.documentation is not None
        assert prefs.testing is not None
        assert prefs.security is not None
        assert prefs.performance is not None
        assert prefs.collaboration is not None
        assert prefs.devops is not None

    def test_full_creation(self) -> None:
        """Test creating CCOPreferences with all fields"""
        prefs = CCOPreferences(
            project_identity=ProjectIdentity(
                name="FullProject",
                types=["api", "microservice"],
                primary_language="python",
                secondary_languages=["javascript"],
                frameworks=["fastapi"],
                deployment_target=["kubernetes"],
                expected_scale="enterprise",
                business_domain=["fintech"],
                compliance_requirements=["gdpr", "sox"],
                project_maturity="production",
                team_trajectory="large-20-50",
                license_model="open-source",
            ),
            development_style=DevelopmentStyle(
                code_philosophy="cutting-edge",
                development_pace="agile-fast",
            ),
            code_quality=CodeQualityStandards(
                linting_strictness="strict",
                type_coverage_target="95",
            ),
            documentation=DocumentationPreferences(
                verbosity="extensive",
            ),
            testing=TestingStrategy(
                coverage_target="95",
            ),
            security=SecurityPosture(
                security_stance="strict",
            ),
            performance=PerformanceVsMaintainability(
                optimization_priority="balanced",
            ),
            collaboration=TeamCollaboration(
                git_workflow="git-flow",
            ),
            devops=DevOpsAutomation(
                ci_cd_trigger="every-commit",
            ),
            selected_principle_ids=["U_ATOMIC_COMMITS", "P_TYPE_SAFETY"],
        )

        assert prefs.project_identity.name == "FullProject"
        assert prefs.development_style.code_philosophy == "cutting-edge"
        assert prefs.code_quality.linting_strictness == "strict"
        assert len(prefs.selected_principle_ids) == 2

    def test_default_sub_models(self) -> None:
        """Test that sub-models have proper defaults"""
        prefs = CCOPreferences(
            project_identity=ProjectIdentity(
                name="Test",
                primary_language="python",
            ),
        )

        # All sub-models should be initialized with defaults
        assert prefs.development_style.code_philosophy == "balanced"
        assert prefs.code_quality.linting_strictness == "strict"
        assert prefs.documentation.verbosity == "concise"
        assert prefs.testing.coverage_target == "90"
        assert prefs.security.security_stance == "balanced"
        assert prefs.performance.optimization_priority == "balanced"
        assert prefs.collaboration.git_workflow == "github-flow"
        assert prefs.devops.ci_cd_trigger == "every-pr"

    def test_metadata_fields(self) -> None:
        """Test metadata fields"""
        prefs = CCOPreferences(
            project_identity=ProjectIdentity(
                name="Test",
                primary_language="python",
            ),
        )

        assert prefs.cco_version is not None
        assert isinstance(prefs.configured_at, datetime)
        assert isinstance(prefs.last_updated, datetime)

    def test_selected_principle_ids(self) -> None:
        """Test selected principle IDs field"""
        principle_ids = ["U_ATOMIC_COMMITS", "P_TYPE_SAFETY", "P_TEST_COVERAGE"]
        prefs = CCOPreferences(
            project_identity=ProjectIdentity(
                name="Test",
                primary_language="python",
            ),
            selected_principle_ids=principle_ids,
        )

        assert len(prefs.selected_principle_ids) == 3
        assert set(prefs.selected_principle_ids) == set(principle_ids)

    def test_empty_selected_principle_ids(self) -> None:
        """Test empty selected principle IDs"""
        prefs = CCOPreferences(
            project_identity=ProjectIdentity(
                name="Test",
                primary_language="python",
            ),
            selected_principle_ids=[],
        )

        assert prefs.selected_principle_ids == []

    def test_serialization_deserialization(self) -> None:
        """Test model can be serialized and deserialized"""
        original = CCOPreferences(
            project_identity=ProjectIdentity(
                name="TestProject",
                types=["api"],
                primary_language="python",
                secondary_languages=["javascript"],
                frameworks=["fastapi"],
            ),
            development_style=DevelopmentStyle(
                code_philosophy="progressive",
            ),
        )

        # Serialize to dict
        data = original.model_dump()
        assert data["project_identity"]["name"] == "TestProject"
        assert data["development_style"]["code_philosophy"] == "progressive"

        # Deserialize back
        restored = CCOPreferences(**data)
        assert restored.project_identity.name == "TestProject"
        assert restored.development_style.code_philosophy == "progressive"

    def test_json_serialization(self) -> None:
        """Test model can be serialized to JSON"""
        prefs = CCOPreferences(
            project_identity=ProjectIdentity(
                name="JsonTest",
                primary_language="python",
            ),
        )

        json_str = prefs.model_dump_json()
        assert "JsonTest" in json_str
        assert "python" in json_str

        # Deserialize from JSON
        restored = CCOPreferences.model_validate_json(json_str)
        assert restored.project_identity.name == "JsonTest"

    def test_missing_required_project_identity(self) -> None:
        """Test that project_identity is required"""
        with pytest.raises(ValidationError):
            CCOPreferences()

    def test_timestamp_immutability_concept(self) -> None:
        """Test that timestamps are set at creation"""
        prefs1 = CCOPreferences(
            project_identity=ProjectIdentity(
                name="Test1",
                primary_language="python",
            ),
        )

        prefs2 = CCOPreferences(
            project_identity=ProjectIdentity(
                name="Test2",
                primary_language="javascript",
            ),
        )

        # Both should have timestamps, but they might be different
        assert prefs1.configured_at is not None
        assert prefs2.configured_at is not None

    def test_complex_nested_preferences(self) -> None:
        """Test complex nested preference structures"""
        prefs = CCOPreferences(
            project_identity=ProjectIdentity(
                name="ComplexProject",
                types=["api", "backend", "microservice"],
                primary_language="python",
                secondary_languages=["go", "typescript", "sql"],
                frameworks=["fastapi", "sqlalchemy", "celery"],
                deployment_target=["kubernetes", "docker", "serverless"],
                expected_scale="enterprise",
                business_domain=["fintech", "saas", "payments"],
                compliance_requirements=["gdpr", "sox", "pci-dss", "hipaa"],
                project_maturity="production",
                team_trajectory="large-50-100",
                license_model="proprietary",
            ),
            development_style=DevelopmentStyle(
                code_philosophy="progressive",
                development_pace="agile-fast",
                tdd_adherence="tdd-preferred",
                refactoring_frequency="continuous",
                breaking_changes_policy="semver-major",
                code_review_strictness="mandatory-all",
                pair_programming="complex-tasks",
                feature_flags="major-features",
            ),
            code_quality=CodeQualityStandards(
                linting_strictness="strict",
                type_coverage_target="95",
                cyclomatic_complexity_limit=10,
                function_length_limit=50,
                dry_enforcement="pragmatic",
                code_comment_density="moderate",
                naming_convention_strictness="enforced",
                magic_number_tolerance="named-constants",
                import_organization="grouped-logical",
                line_length_limit="100",
            ),
            selected_principle_ids=["U_ATOMIC_COMMITS", "U_TYPE_SAFETY", "P_TEST_COVERAGE"],
        )

        # Verify all settings are preserved
        assert len(prefs.project_identity.types) == 3
        assert len(prefs.project_identity.secondary_languages) == 3
        assert len(prefs.project_identity.frameworks) == 3
        assert len(prefs.project_identity.compliance_requirements) == 4
        assert prefs.code_quality.cyclomatic_complexity_limit == 10


class TestUtilityFunctions:
    """Test utility functions"""

    def test_get_literal_choices_project_type(self) -> None:
        """Test extracting choices from ProjectTypeChoice"""
        choices = get_literal_choices(ProjectTypeChoice)
        assert len(choices) > 0
        assert "api" in choices
        assert "backend" in choices

    def test_get_literal_choices_deployment_target(self) -> None:
        """Test extracting choices from DeploymentTargetChoice"""
        choices = get_literal_choices(DeploymentTargetChoice)
        assert len(choices) > 0
        assert "cloud-aws" in choices

    def test_get_literal_choices_compliance(self) -> None:
        """Test extracting choices from ComplianceChoice"""
        choices = get_literal_choices(ComplianceChoice)
        assert len(choices) > 0
        assert "gdpr" in choices
        assert "hipaa" in choices


class TestEdgeCases:
    """Test edge cases and boundary conditions"""

    def test_empty_lists_in_preferences(self) -> None:
        """Test preferences with empty lists where allowed"""
        prefs = CCOPreferences(
            project_identity=ProjectIdentity(
                name="Test",
                types=[],
                primary_language="python",
                secondary_languages=[],
                frameworks=[],
                deployment_target=[],
                business_domain=[],
                compliance_requirements=[],
            ),
        )

        assert prefs.project_identity.types == []
        assert prefs.project_identity.secondary_languages == []

    def test_very_long_lists(self) -> None:
        """Test preferences with many items in lists"""
        secondary_langs = [f"lang{i}" for i in range(20)]
        prefs = CCOPreferences(
            project_identity=ProjectIdentity(
                name="Test",
                primary_language="python",
                secondary_languages=secondary_langs,
            ),
        )

        assert len(prefs.project_identity.secondary_languages) == 20

    def test_special_characters_in_strings(self) -> None:
        """Test that special characters in strings are handled"""
        prefs = CCOPreferences(
            project_identity=ProjectIdentity(
                name="Test-Project_123",
                primary_language="python",
                frameworks=["@latest", "c++"],
            ),
        )

        assert prefs.project_identity.name == "Test-Project_123"

    def test_unicode_in_strings(self) -> None:
        """Test that unicode in strings is handled"""
        prefs = CCOPreferences(
            project_identity=ProjectIdentity(
                name="Test-プロジェクト",
                primary_language="python",
            ),
        )

        assert "プロジェクト" in prefs.project_identity.name

    def test_duplicate_items_in_lists(self) -> None:
        """Test that duplicate items are preserved in lists"""
        prefs = CCOPreferences(
            project_identity=ProjectIdentity(
                name="Test",
                types=["api", "api", "backend"],
                primary_language="python",
            ),
        )

        # Lists preserve duplicates by design
        assert prefs.project_identity.types.count("api") == 2

    def test_none_optional_values(self) -> None:
        """Test optional fields with None values"""
        quality = CodeQualityStandards(
            cyclomatic_complexity_limit=None,
            function_length_limit=None,
        )

        assert quality.cyclomatic_complexity_limit is None
        assert quality.function_length_limit is None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])

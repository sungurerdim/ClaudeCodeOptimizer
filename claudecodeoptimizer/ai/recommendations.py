"""
CCO 2.5 Universal Recommendation Engine

100% rule-based and data-driven recommendation system.
Works across all domains, scales, and technology stacks.

Design principles:
- Zero hardcoded project-specific logic
- All recommendations derive from lookup tables + rules
- Confidence scores based on evidence strength
- Transparent reasoning with citations
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional

from .. import __version__ as cco_version

# ============================================================================
# DATA MODELS
# ============================================================================


class ConfidenceLevel(Enum):
    """Recommendation confidence levels."""

    VERY_HIGH = 0.95  # Direct evidence + industry standard
    HIGH = 0.85  # Strong evidence or clear pattern
    MEDIUM = 0.70  # Inference from multiple signals
    LOW = 0.50  # Weak signal or default recommendation


@dataclass
class Recommendation:
    """Single recommendation with reasoning and confidence."""

    category: str  # e.g., "security", "testing", "devops"
    title: str
    description: str
    priority: str  # "critical", "high", "medium", "low"
    confidence: float
    reasoning: List[str]  # Why this recommendation was made
    evidence: List[str]  # What detection results support this
    citations: List[str]  # Industry standards / best practices
    implementation_notes: Optional[str] = None
    estimated_effort: Optional[str] = None  # "1h", "1d", "1w", "1m"


@dataclass
class RecommendationBundle:
    """Complete set of recommendations for a project."""

    project_identity: List[Recommendation]
    code_quality: List[Recommendation]
    testing: List[Recommendation]
    security: List[Recommendation]
    devops: List[Recommendation]
    infrastructure: List[Recommendation]
    metadata: Dict[str, Any] = field(default_factory=dict)


# ============================================================================
# UNIVERSAL BEST PRACTICE KNOWLEDGE BASE
# ============================================================================

DOMAIN_BEST_PRACTICES = {
    "fintech": {
        "security_stance": "paranoid",
        "audit_logging": "comprehensive",
        "test_coverage_min": 95,
        "encryption_scope": "everything",
        "compliance_requirements": ["pci-dss", "sox", "gdpr"],
        "monitoring_level": "full-observability",
        "incident_response": "mandatory",
        "data_retention_policy": "regulated",
        "auth_requirements": ["mfa", "session-timeout", "ip-whitelisting"],
        "code_review_threshold": "all-changes",
        "deployment_validation": ["canary", "blue-green"],
        "backup_frequency": "real-time",
        "disaster_recovery_rto": "minutes",
    },
    "healthcare": {
        "security_stance": "paranoid",
        "encryption_scope": "everything",
        "test_coverage_min": 90,
        "compliance_requirements": ["hipaa", "hitech", "gdpr"],
        "audit_logging": "comprehensive",
        "data_retention_policy": "regulated",
        "access_control": "role-based-strict",
        "phi_handling": "zero-disk",
        "auth_requirements": ["mfa", "audit-trail"],
        "monitoring_level": "full-observability",
        "incident_response": "mandatory",
        "backup_frequency": "hourly",
    },
    "e-commerce": {
        "security_stance": "standard",
        "test_coverage_min": 80,
        "caching_strategy": "aggressive",
        "monitoring_level": "full-observability",
        "performance_budget": "strict",
        "scalability_requirements": ["horizontal", "cdn"],
        "payment_security": ["pci-dss"],
        "session_management": "distributed",
        "inventory_consistency": "eventual-strong-hybrid",
        "search_optimization": "required",
        "ab_testing": "recommended",
    },
    "saas": {
        "security_stance": "standard",
        "test_coverage_min": 85,
        "monitoring_level": "full-observability",
        "multi_tenancy": "isolation-required",
        "auth_requirements": ["sso", "oauth2"],
        "rate_limiting": "per-tenant",
        "feature_flags": "recommended",
        "analytics": "user-behavior",
        "scalability_requirements": ["horizontal", "multi-region"],
        "deployment_validation": ["canary"],
    },
    "gaming": {
        "security_stance": "standard",
        "test_coverage_min": 70,
        "performance_budget": "strict",
        "real_time_requirements": "low-latency",
        "scalability_requirements": ["horizontal", "edge-computing"],
        "anti_cheat": "server-authoritative",
        "matchmaking": "skill-based",
        "monitoring_level": "performance-focused",
        "caching_strategy": "aggressive",
    },
    "iot": {
        "security_stance": "device-hardened",
        "test_coverage_min": 85,
        "edge_computing": "required",
        "offline_capability": "required",
        "device_management": "remote-updates",
        "telemetry": "comprehensive",
        "power_optimization": "required",
        "network_resilience": "intermittent-connectivity",
        "security_requirements": ["device-auth", "secure-boot"],
    },
    "ai-ml": {
        "security_stance": "standard",
        "test_coverage_min": 75,
        "data_versioning": "required",
        "model_versioning": "required",
        "experiment_tracking": "required",
        "monitoring_level": "model-performance",
        "scalability_requirements": ["gpu-acceleration", "distributed-training"],
        "reproducibility": "strict",
        "bias_detection": "recommended",
        "explainability": "recommended",
    },
    "api": {
        "security_stance": "standard",
        "test_coverage_min": 85,
        "versioning_strategy": "semantic",
        "rate_limiting": "required",
        "auth_requirements": ["api-keys", "oauth2"],
        "documentation": "openapi",
        "monitoring_level": "api-metrics",
        "caching_strategy": "conditional",
        "cors_policy": "restrictive",
    },
    "mobile": {
        "security_stance": "standard",
        "test_coverage_min": 80,
        "offline_capability": "recommended",
        "bundle_size_optimization": "strict",
        "performance_budget": "strict",
        "analytics": "crash-reporting",
        "deployment_validation": ["staged-rollout"],
        "auth_requirements": ["biometric-optional"],
        "battery_optimization": "required",
    },
    "default": {
        "security_stance": "standard",
        "test_coverage_min": 80,
        "monitoring_level": "basic",
        "backup_frequency": "daily",
        "deployment_validation": ["smoke-tests"],
    },
}

SCALE_RECOMMENDATIONS = {
    "hobby": {
        "infrastructure": "serverless-or-paas",
        "ci_cd": "basic",
        "monitoring": "free-tier",
        "cost_optimization": "priority",
        "team_size": 1,
        "deployment_frequency": "manual-ok",
        "test_automation": "basic",
        "documentation_level": "readme-only",
        "security_tooling": "free-tools",
    },
    "startup": {
        "infrastructure": "managed-services",
        "ci_cd": "automated-basic",
        "monitoring": "essential-metrics",
        "cost_optimization": "important",
        "team_size": "1-10",
        "deployment_frequency": "daily",
        "test_automation": "unit-integration",
        "documentation_level": "api-docs",
        "security_tooling": "sast-dependency-scan",
        "scalability_requirements": ["vertical-first"],
    },
    "growth": {
        "infrastructure": "hybrid-managed-custom",
        "ci_cd": "automated-advanced",
        "monitoring": "full-observability",
        "cost_optimization": "balanced",
        "team_size": "10-50",
        "deployment_frequency": "continuous",
        "test_automation": "comprehensive",
        "documentation_level": "technical-specs",
        "security_tooling": "sast-dast-dependency-scan",
        "scalability_requirements": ["horizontal", "multi-region"],
        "incident_response": "runbooks",
    },
    "enterprise": {
        "infrastructure": "multi-cloud-hybrid",
        "ci_cd": "enterprise-pipeline",
        "monitoring": "full-observability-apm",
        "cost_optimization": "chargeback-model",
        "team_size": "50+",
        "deployment_frequency": "continuous-safe",
        "test_automation": "comprehensive-e2e",
        "documentation_level": "complete-compliance",
        "security_tooling": "enterprise-suite",
        "scalability_requirements": ["horizontal", "multi-region", "multi-cloud"],
        "incident_response": "formal-process",
        "compliance_requirements": ["soc2", "iso27001"],
        "disaster_recovery_rto": "minutes",
        "backup_frequency": "real-time",
    },
}

LANGUAGE_BEST_PRACTICES = {
    "python": {
        "formatter": "black",
        "linter": "ruff",
        "type_checker": "mypy",
        "test_framework": "pytest",
        "dependency_management": "poetry-or-uv",
        "security_scanner": "bandit",
        "package_vulnerabilities": "safety",
        "code_complexity": "radon",
        "import_sorting": "isort",
    },
    "javascript": {
        "formatter": "prettier",
        "linter": "eslint",
        "type_checker": "typescript",
        "test_framework": "jest-or-vitest",
        "dependency_management": "npm-or-pnpm",
        "security_scanner": "npm-audit",
        "bundle_analyzer": "webpack-bundle-analyzer",
    },
    "typescript": {
        "formatter": "prettier",
        "linter": "eslint-typescript",
        "test_framework": "jest-or-vitest",
        "dependency_management": "npm-or-pnpm",
        "type_coverage": "strict-mode",
    },
    "go": {
        "formatter": "gofmt",
        "linter": "golangci-lint",
        "test_framework": "testing",
        "dependency_management": "go-modules",
        "security_scanner": "gosec",
    },
    "rust": {
        "formatter": "rustfmt",
        "linter": "clippy",
        "test_framework": "cargo-test",
        "dependency_management": "cargo",
        "security_scanner": "cargo-audit",
    },
    "java": {
        "formatter": "google-java-format",
        "linter": "checkstyle",
        "test_framework": "junit5",
        "dependency_management": "maven-or-gradle",
        "security_scanner": "spotbugs",
        "static_analysis": "sonarqube",
    },
}

SECURITY_STANCE_REQUIREMENTS = {
    "paranoid": {
        "encryption_at_rest": "mandatory",
        "encryption_in_transit": "mandatory-tls13",
        "secret_management": "vault-or-managed",
        "mfa": "mandatory",
        "audit_logging": "comprehensive",
        "penetration_testing": "quarterly",
        "security_training": "mandatory",
        "incident_response_plan": "documented-tested",
        "zero_trust": "recommended",
        "threat_modeling": "mandatory",
    },
    "device-hardened": {
        "secure_boot": "mandatory",
        "firmware_signing": "mandatory",
        "device_attestation": "mandatory",
        "ota_updates": "signed-encrypted",
        "tamper_detection": "recommended",
    },
    "standard": {
        "encryption_at_rest": "recommended",
        "encryption_in_transit": "mandatory-tls12",
        "secret_management": "env-vars-or-vault",
        "mfa": "recommended",
        "audit_logging": "basic",
        "penetration_testing": "annual",
        "security_training": "recommended",
    },
}

MONITORING_LEVEL_REQUIREMENTS = {
    "full-observability": {
        "metrics": "prometheus-compatible",
        "logs": "structured-centralized",
        "traces": "distributed-tracing",
        "apm": "recommended",
        "dashboards": "grafana-or-equivalent",
        "alerting": "multi-channel",
        "slo_tracking": "recommended",
    },
    "full-observability-apm": {
        "metrics": "prometheus-compatible",
        "logs": "structured-centralized",
        "traces": "distributed-tracing",
        "apm": "mandatory",
        "dashboards": "grafana-or-equivalent",
        "alerting": "multi-channel-oncall",
        "slo_tracking": "mandatory",
        "error_tracking": "sentry-or-equivalent",
    },
    "api-metrics": {
        "metrics": "api-latency-throughput-errors",
        "rate_limiting_monitoring": "mandatory",
        "endpoint_health": "per-endpoint",
        "client_tracking": "api-key-level",
    },
    "model-performance": {
        "metrics": "accuracy-drift-latency",
        "data_quality": "monitoring",
        "prediction_logging": "sample-based",
        "model_versioning": "tracking",
    },
    "performance-focused": {
        "metrics": "latency-fps-memory",
        "profiling": "continuous",
        "player_experience": "tracking",
    },
    "basic": {
        "metrics": "cpu-memory-disk",
        "logs": "file-based",
        "uptime_monitoring": "ping-checks",
        "alerting": "email",
    },
}

# ============================================================================
# RECOMMENDATION ENGINE
# ============================================================================


class RecommendationEngine:
    """Universal recommendation engine - 100% data-driven."""

    def __init__(self, detection_results: Dict[str, Any]) -> None:
        """
        Initialize engine with detection results.

        Args:
            detection_results: Output from DetectionEngine
        """
        self.detection = detection_results
        self.domain = detection_results.get("project_identity", {}).get("domain", "default")
        self.scale = detection_results.get("project_identity", {}).get("scale", "startup")
        self.language = detection_results.get("project_identity", {}).get(
            "primary_language",
            "python",
        )

        # Lookup tables
        self.domain_practices = DOMAIN_BEST_PRACTICES.get(
            self.domain,
            DOMAIN_BEST_PRACTICES["default"],
        )
        self.scale_practices = SCALE_RECOMMENDATIONS.get(
            self.scale,
            SCALE_RECOMMENDATIONS["startup"],
        )
        self.language_practices = LANGUAGE_BEST_PRACTICES.get(
            self.language,
            LANGUAGE_BEST_PRACTICES["python"],
        )

    def _calculate_confidence(
        self,
        has_direct_evidence: bool,
        signal_strength: str = "strong",
        is_inference: bool = False,
    ) -> float:
        """
        Calculate recommendation confidence based on evidence.

        Args:
            has_direct_evidence: Direct detection result supports this
            signal_strength: "strong", "medium", "weak"
            is_inference: True if extrapolating from indirect signals

        Returns:
            Confidence score 0.0-1.0
        """
        if has_direct_evidence and signal_strength == "strong":
            base = ConfidenceLevel.VERY_HIGH.value
        elif has_direct_evidence:
            base = ConfidenceLevel.HIGH.value
        elif signal_strength == "medium":
            base = ConfidenceLevel.MEDIUM.value
        else:
            base = ConfidenceLevel.LOW.value

        # Reduce confidence for inferences
        if is_inference:
            base *= 0.85

        return base

    def recommend_project_identity(self) -> List[Recommendation]:
        """Recommendations for improving project identity detection."""
        recommendations = []

        identity = self.detection.get("project_identity", {})

        # Missing project type
        if not identity.get("type") or identity["type"] == "unknown":
            recommendations.append(
                Recommendation(
                    category="project-identity",
                    title="Define project type explicitly",
                    description="Add project type to pyproject.toml or package.json metadata",
                    priority="medium",
                    confidence=self._calculate_confidence(True, "strong"),
                    reasoning=[
                        "Project type detection failed or returned 'unknown'",
                        "Explicit type declaration improves tooling compatibility",
                        "Enables better dependency and build tool recommendations",
                    ],
                    evidence=[
                        f"Detected type: {identity.get('type', 'unknown')}",
                    ],
                    citations=[
                        "PEP 621 - Python project metadata",
                        "NPM package.json specification",
                    ],
                    implementation_notes="Add 'type' field to project metadata",
                    estimated_effort="15m",
                ),
            )

        # Missing domain
        if not identity.get("domain") or identity["domain"] == "general":
            recommendations.append(
                Recommendation(
                    category="project-identity",
                    title="Specify application domain",
                    description="Add domain classification for tailored recommendations",
                    priority="low",
                    confidence=self._calculate_confidence(False, "medium", is_inference=True),
                    reasoning=[
                        "Domain-specific best practices improve code quality",
                        "Enables compliance and security recommendations",
                        "CCO can suggest domain-appropriate tooling",
                    ],
                    evidence=[
                        f"Current domain: {identity.get('domain', 'general')}",
                    ],
                    citations=[
                        "CCO 2.5 domain classification system",
                    ],
                    implementation_notes="Add domain tag in .cco/manifest.json",
                    estimated_effort="5m",
                ),
            )

        # Unclear scale
        if not identity.get("scale"):
            recommendations.append(
                Recommendation(
                    category="project-identity",
                    title="Define project scale",
                    description="Specify scale (hobby/startup/growth/enterprise) for appropriate tooling",
                    priority="medium",
                    confidence=self._calculate_confidence(False, "strong"),
                    reasoning=[
                        "Scale determines infrastructure and tooling needs",
                        "Prevents over-engineering for small projects",
                        "Ensures enterprise projects meet compliance requirements",
                    ],
                    evidence=[
                        f"Team size: {identity.get('team_size', 'unknown')}",
                        f"Deployment frequency: {identity.get('deployment_frequency', 'unknown')}",
                    ],
                    citations=[
                        "CCO 2.5 scale classification",
                    ],
                    implementation_notes="Add scale to .cco/manifest.json based on team size and deployment needs",
                    estimated_effort="10m",
                ),
            )

        return recommendations

    def recommend_code_quality(self) -> List[Recommendation]:
        """Recommendations for code quality improvements."""
        recommendations = []

        code_quality = self.detection.get("code_quality", {})

        # Missing formatter
        if not code_quality.get("formatter"):
            expected_formatter = self.language_practices.get("formatter")
            recommendations.append(
                Recommendation(
                    category="code-quality",
                    title=f"Configure {expected_formatter} for code formatting",
                    description=f"Add {expected_formatter} to maintain consistent code style",
                    priority="high",
                    confidence=self._calculate_confidence(True, "strong"),
                    reasoning=[
                        f"No formatter detected for {self.language} project",
                        f"{expected_formatter} is the industry standard for {self.language}",
                        "Automated formatting reduces code review friction",
                    ],
                    evidence=[
                        f"Language: {self.language}",
                        "No formatter configuration found",
                    ],
                    citations=[
                        f"{self.language.title()} formatting best practices",
                        f"{expected_formatter} official documentation",
                    ],
                    implementation_notes=f"Install {expected_formatter} and add to pre-commit hooks",
                    estimated_effort="30m",
                ),
            )

        # Missing linter
        if not code_quality.get("linter"):
            expected_linter = self.language_practices.get("linter")
            recommendations.append(
                Recommendation(
                    category="code-quality",
                    title=f"Configure {expected_linter} for linting",
                    description=f"Add {expected_linter} to catch code quality issues",
                    priority="high",
                    confidence=self._calculate_confidence(True, "strong"),
                    reasoning=[
                        f"No linter detected for {self.language} project",
                        f"{expected_linter} is the recommended linter for {self.language}",
                        "Linting catches bugs and enforces best practices",
                    ],
                    evidence=[
                        f"Language: {self.language}",
                        "No linter configuration found",
                    ],
                    citations=[
                        f"{expected_linter} best practices",
                    ],
                    implementation_notes=f"Install {expected_linter} and configure rules",
                    estimated_effort="1h",
                ),
            )

        # Missing type checker
        if not code_quality.get("type_checker"):
            expected_checker = self.language_practices.get("type_checker")
            if expected_checker:
                recommendations.append(
                    Recommendation(
                        category="code-quality",
                        title=f"Enable {expected_checker} for type checking",
                        description=f"Add static type checking with {expected_checker}",
                        priority="medium",
                        confidence=self._calculate_confidence(True, "medium"),
                        reasoning=[
                            "Type checking catches bugs before runtime",
                            "Improves IDE autocomplete and refactoring",
                            f"{expected_checker} is standard for {self.language}",
                        ],
                        evidence=[
                            f"Language: {self.language}",
                            "No type checker found",
                        ],
                        citations=[
                            f"{expected_checker} documentation",
                        ],
                        implementation_notes=f"Install {expected_checker} and add type hints gradually",
                        estimated_effort="2h initial setup + ongoing",
                    ),
                )

        return recommendations

    def recommend_testing(self) -> List[Recommendation]:
        """Recommendations for testing strategy."""
        recommendations = []

        testing = self.detection.get("testing", {})
        current_coverage = testing.get("test_coverage_percent", 0)
        min_coverage = self.domain_practices.get("test_coverage_min", 80)

        # Missing test framework
        if not testing.get("test_framework"):
            expected_framework = self.language_practices.get("test_framework")
            recommendations.append(
                Recommendation(
                    category="testing",
                    title=f"Set up {expected_framework} for testing",
                    description=f"Configure {expected_framework} as the test framework",
                    priority="critical",
                    confidence=self._calculate_confidence(True, "strong"),
                    reasoning=[
                        "No test framework detected",
                        f"{expected_framework} is the standard for {self.language}",
                        "Testing is essential for code reliability",
                    ],
                    evidence=[
                        f"Language: {self.language}",
                        "No test files found",
                    ],
                    citations=[
                        f"{expected_framework} best practices",
                    ],
                    implementation_notes=f"Install {expected_framework} and create test/ directory",
                    estimated_effort="1h",
                ),
            )

        # Low coverage
        if current_coverage < min_coverage:
            recommendations.append(
                Recommendation(
                    category="testing",
                    title=f"Increase test coverage to {min_coverage}%",
                    description=f"Current coverage ({current_coverage}%) below {self.domain} domain standard ({min_coverage}%)",
                    priority="high" if current_coverage < min_coverage * 0.7 else "medium",
                    confidence=self._calculate_confidence(True, "strong"),
                    reasoning=[
                        f"{self.domain.title()} projects require {min_coverage}% minimum coverage",
                        "Higher coverage reduces production bugs",
                        "Domain compliance may require specific coverage thresholds",
                    ],
                    evidence=[
                        f"Current coverage: {current_coverage}%",
                        f"Domain: {self.domain}",
                        f"Minimum required: {min_coverage}%",
                    ],
                    citations=[
                        f"{self.domain.title()} testing best practices",
                    ],
                    implementation_notes="Focus on critical paths first, then edge cases",
                    estimated_effort=f"{int((min_coverage - current_coverage) / 10)}d",
                ),
            )

        # Missing test types
        testing.get("has_unit_tests", False)
        has_integration = testing.get("has_integration_tests", False)
        has_e2e = testing.get("has_e2e_tests", False)

        if not has_integration and self.scale in ["growth", "enterprise"]:
            recommendations.append(
                Recommendation(
                    category="testing",
                    title="Add integration tests",
                    description="Test component interactions and external dependencies",
                    priority="high",
                    confidence=self._calculate_confidence(False, "strong"),
                    reasoning=[
                        f"{self.scale.title()} projects require integration testing",
                        "Integration tests catch system-level issues",
                        "Validates API contracts and database interactions",
                    ],
                    evidence=[
                        f"Scale: {self.scale}",
                        "No integration tests found",
                    ],
                    citations=[
                        "Testing pyramid best practices",
                    ],
                    implementation_notes="Start with critical API endpoints and database operations",
                    estimated_effort="3d",
                ),
            )

        if not has_e2e and self.scale == "enterprise":
            recommendations.append(
                Recommendation(
                    category="testing",
                    title="Add end-to-end tests",
                    description="Test complete user workflows",
                    priority="medium",
                    confidence=self._calculate_confidence(False, "medium"),
                    reasoning=[
                        "Enterprise projects benefit from E2E validation",
                        "Catches integration issues across services",
                        "Validates user-facing functionality",
                    ],
                    evidence=[
                        f"Scale: {self.scale}",
                        "No E2E tests found",
                    ],
                    citations=[
                        "Enterprise testing strategies",
                    ],
                    implementation_notes="Focus on critical user journeys",
                    estimated_effort="1w",
                ),
            )

        return recommendations

    def recommend_security(self) -> List[Recommendation]:
        """Recommendations for security improvements."""
        recommendations = []

        security = self.detection.get("security", {})
        stance = self.domain_practices.get("security_stance", "standard")
        stance_reqs = SECURITY_STANCE_REQUIREMENTS.get(stance, {})

        # Encryption at rest
        if stance_reqs.get("encryption_at_rest") == "mandatory":
            has_encryption = security.get("encryption_at_rest", False)
            if not has_encryption:
                recommendations.append(
                    Recommendation(
                        category="security",
                        title="Enable encryption at rest",
                        description="Encrypt sensitive data stored in databases and file systems",
                        priority="critical",
                        confidence=self._calculate_confidence(True, "strong"),
                        reasoning=[
                            f"{self.domain.title()} domain requires encryption at rest",
                            "Protects data in case of physical breach",
                            "Required for compliance standards",
                        ],
                        evidence=[
                            f"Domain: {self.domain}",
                            f"Security stance: {stance}",
                            "No encryption detected",
                        ],
                        citations=[
                            "OWASP cryptographic storage cheatsheet",
                            f"{', '.join(self.domain_practices.get('compliance_requirements', []))}",
                        ],
                        implementation_notes="Use database native encryption or application-level encryption",
                        estimated_effort="1d",
                    ),
                )

        # Secret management
        secret_mgmt_req = stance_reqs.get("secret_management")
        current_secret_mgmt = security.get("secret_management_tool")

        if secret_mgmt_req == "vault-or-managed" and not current_secret_mgmt:  # noqa: S105
            recommendations.append(
                Recommendation(
                    category="security",
                    title="Implement secret management solution",
                    description="Use HashiCorp Vault or cloud-native secret manager",
                    priority="critical",
                    confidence=self._calculate_confidence(True, "strong"),
                    reasoning=[
                        f"{stance.title()} security stance requires vault-based secrets",
                        "Environment variables insufficient for sensitive data",
                        "Enables secret rotation and audit trails",
                    ],
                    evidence=[
                        f"Security stance: {stance}",
                        "No secret management tool detected",
                    ],
                    citations=[
                        "OWASP secrets management cheatsheet",
                        "HashiCorp Vault best practices",
                    ],
                    implementation_notes="Consider cloud provider managed services first (AWS Secrets Manager, GCP Secret Manager)",
                    estimated_effort="2d",
                ),
            )

        # MFA
        if stance_reqs.get("mfa") == "mandatory":
            has_mfa = security.get("mfa_enabled", False)
            if not has_mfa:
                recommendations.append(
                    Recommendation(
                        category="security",
                        title="Implement multi-factor authentication",
                        description="Require MFA for all user accounts",
                        priority="critical",
                        confidence=self._calculate_confidence(False, "strong"),
                        reasoning=[
                            f"{self.domain.title()} requires MFA for account security",
                            "Prevents account takeover attacks",
                            "Required by compliance standards",
                        ],
                        evidence=[
                            f"Domain: {self.domain}",
                            "No MFA implementation found",
                        ],
                        citations=[
                            "NIST SP 800-63B authentication guidelines",
                            f"{', '.join(self.domain_practices.get('compliance_requirements', []))}",
                        ],
                        implementation_notes="Support TOTP (Google Authenticator) and SMS as backup",
                        estimated_effort="3d",
                    ),
                )

        # Audit logging
        audit_req = self.domain_practices.get("audit_logging")
        has_audit = security.get("audit_logging_enabled", False)

        if audit_req == "comprehensive" and not has_audit:
            recommendations.append(
                Recommendation(
                    category="security",
                    title="Enable comprehensive audit logging",
                    description="Log all security-relevant events (auth, data access, config changes)",
                    priority="high",
                    confidence=self._calculate_confidence(True, "strong"),
                    reasoning=[
                        f"{self.domain.title()} requires comprehensive audit trails",
                        "Essential for security investigations",
                        "Required for compliance certifications",
                    ],
                    evidence=[
                        f"Domain: {self.domain}",
                        "No audit logging detected",
                    ],
                    citations=[
                        "OWASP logging cheatsheet",
                        "SOC 2 audit logging requirements",
                    ],
                    implementation_notes="Log: authentication events, data access, permission changes, config changes",
                    estimated_effort="2d",
                ),
            )

        # Dependency scanning
        has_dep_scan = security.get("dependency_scanning", False)
        if not has_dep_scan:
            recommendations.append(
                Recommendation(
                    category="security",
                    title="Enable dependency vulnerability scanning",
                    description=f"Use {self.language_practices.get('package_vulnerabilities', 'automated scanner')} to detect vulnerable dependencies",
                    priority="high",
                    confidence=self._calculate_confidence(True, "strong"),
                    reasoning=[
                        "Third-party dependencies are a common attack vector",
                        "Automated scanning catches known CVEs",
                        "Should run on every dependency change",
                    ],
                    evidence=[
                        f"Language: {self.language}",
                        "No dependency scanning detected",
                    ],
                    citations=[
                        "OWASP Dependency-Check",
                        "Snyk vulnerability database",
                    ],
                    implementation_notes=f"Add {self.language_practices.get('package_vulnerabilities')} to CI/CD pipeline",
                    estimated_effort="1h",
                ),
            )

        return recommendations

    def recommend_devops(self) -> List[Recommendation]:
        """Recommendations for DevOps and CI/CD."""
        recommendations = []

        devops = self.detection.get("devops", {})
        ci_level = self.scale_practices.get("ci_cd")

        # Missing CI/CD
        if not devops.get("ci_cd_platform"):
            recommendations.append(
                Recommendation(
                    category="devops",
                    title="Set up CI/CD pipeline",
                    description=f"Configure {ci_level} continuous integration and deployment",
                    priority="high",
                    confidence=self._calculate_confidence(True, "strong"),
                    reasoning=[
                        f"{self.scale.title()} projects require {ci_level} CI/CD",
                        "Automates testing and deployment",
                        "Reduces human error in releases",
                    ],
                    evidence=[
                        f"Scale: {self.scale}",
                        "No CI/CD platform detected",
                    ],
                    citations=[
                        "GitHub Actions best practices",
                        "GitLab CI/CD documentation",
                    ],
                    implementation_notes="Start with automated tests on PR, then add deployment",
                    estimated_effort="1d",
                ),
            )

        # Deployment validation
        deploy_validation = self.domain_practices.get("deployment_validation", [])
        current_validation = devops.get("deployment_strategy", [])

        for validation in deploy_validation:
            if validation not in current_validation:
                recommendations.append(
                    Recommendation(
                        category="devops",
                        title=f"Implement {validation} deployments",
                        description=f"Add {validation} deployment strategy for safer releases",
                        priority="high" if self.scale in ["growth", "enterprise"] else "medium",
                        confidence=self._calculate_confidence(False, "medium"),
                        reasoning=[
                            f"{self.domain.title()} projects benefit from {validation}",
                            "Reduces blast radius of bad deployments",
                            "Enables fast rollback",
                        ],
                        evidence=[
                            f"Domain: {self.domain}",
                            f"Current strategy: {', '.join(current_validation) or 'unknown'}",
                        ],
                        citations=[
                            f"{validation} deployment best practices",
                        ],
                        implementation_notes="Requires feature flag system or traffic routing",
                        estimated_effort="1w",
                    ),
                )

        # Monitoring
        monitoring_level = self.domain_practices.get(
            "monitoring_level",
            self.scale_practices.get("monitoring"),
        )
        monitoring_reqs = MONITORING_LEVEL_REQUIREMENTS.get(monitoring_level, {})

        has_metrics = devops.get("monitoring", {}).get("metrics", False)
        devops.get("monitoring", {}).get("logs", False)
        has_traces = devops.get("monitoring", {}).get("traces", False)

        if monitoring_reqs.get("metrics") and not has_metrics:
            recommendations.append(
                Recommendation(
                    category="devops",
                    title=f"Set up metrics collection ({monitoring_reqs['metrics']})",
                    description="Implement application and infrastructure metrics",
                    priority="high",
                    confidence=self._calculate_confidence(True, "strong"),
                    reasoning=[
                        f"{monitoring_level} monitoring requires metrics",
                        "Essential for debugging production issues",
                        "Enables proactive alerting",
                    ],
                    evidence=[
                        f"Monitoring level: {monitoring_level}",
                        "No metrics system detected",
                    ],
                    citations=[
                        "Prometheus best practices",
                        "Google SRE monitoring patterns",
                    ],
                    implementation_notes=f"Use {monitoring_reqs['metrics']} for metrics collection",
                    estimated_effort="2d",
                ),
            )

        if monitoring_reqs.get("traces") and not has_traces:
            recommendations.append(
                Recommendation(
                    category="devops",
                    title="Enable distributed tracing",
                    description="Implement OpenTelemetry or similar tracing",
                    priority="medium",
                    confidence=self._calculate_confidence(False, "medium"),
                    reasoning=[
                        f"{monitoring_level} monitoring includes distributed tracing",
                        "Traces show request flow across services",
                        "Essential for debugging microservices",
                    ],
                    evidence=[
                        f"Monitoring level: {monitoring_level}",
                        "No tracing detected",
                    ],
                    citations=[
                        "OpenTelemetry documentation",
                        "Distributed tracing best practices",
                    ],
                    implementation_notes="Start with high-level spans, then add detail",
                    estimated_effort="3d",
                ),
            )

        return recommendations

    def recommend_infrastructure(self) -> List[Recommendation]:
        """Recommendations for infrastructure setup."""
        recommendations = []

        infrastructure = self.detection.get("infrastructure", {})
        self.scale_practices.get("infrastructure")

        # Containerization
        has_docker = infrastructure.get("containerization", {}).get("docker", False)
        if not has_docker and self.scale in ["growth", "enterprise"]:
            recommendations.append(
                Recommendation(
                    category="infrastructure",
                    title="Containerize application with Docker",
                    description="Create Dockerfile and docker-compose.yml for consistent environments",
                    priority="high",
                    confidence=self._calculate_confidence(True, "strong"),
                    reasoning=[
                        f"{self.scale.title()} projects benefit from containerization",
                        "Ensures consistent dev/prod environments",
                        "Simplifies deployment and scaling",
                    ],
                    evidence=[
                        f"Scale: {self.scale}",
                        "No Docker configuration found",
                    ],
                    citations=[
                        "Docker best practices",
                        "12-factor app methodology",
                    ],
                    implementation_notes="Start with multi-stage builds for smaller images",
                    estimated_effort="1d",
                ),
            )

        # Orchestration
        needs_k8s = self.scale == "enterprise" or (
            self.scale == "growth"
            and "horizontal" in self.domain_practices.get("scalability_requirements", [])
        )
        has_k8s = infrastructure.get("orchestration", {}).get("kubernetes", False)

        if needs_k8s and not has_k8s:
            recommendations.append(
                Recommendation(
                    category="infrastructure",
                    title="Set up Kubernetes orchestration",
                    description="Deploy to Kubernetes for horizontal scaling and high availability",
                    priority="medium",
                    confidence=self._calculate_confidence(False, "medium", is_inference=True),
                    reasoning=[
                        f"{self.scale.title()} projects with horizontal scaling need orchestration",
                        "Kubernetes provides self-healing and auto-scaling",
                        "Industry standard for cloud-native apps",
                    ],
                    evidence=[
                        f"Scale: {self.scale}",
                        f"Scalability requirements: {self.domain_practices.get('scalability_requirements', [])}",
                    ],
                    citations=[
                        "Kubernetes best practices",
                        "CNCF landscape",
                    ],
                    implementation_notes="Consider managed Kubernetes (GKE, EKS, AKS) first",
                    estimated_effort="2w",
                ),
            )

        # Database
        db_config = infrastructure.get("database", {})
        if not db_config:
            recommendations.append(
                Recommendation(
                    category="infrastructure",
                    title="Define database strategy",
                    description="Document database choice and configuration",
                    priority="medium",
                    confidence=self._calculate_confidence(True, "medium"),
                    reasoning=[
                        "Database is critical infrastructure component",
                        "Should be explicitly defined in IaC or docs",
                        "Enables backup and disaster recovery planning",
                    ],
                    evidence=[
                        "No database configuration detected",
                    ],
                    citations=[
                        "Database selection guide",
                    ],
                    implementation_notes="Consider managed databases for easier operations",
                    estimated_effort="4h",
                ),
            )

        # Backup strategy
        backup_freq = self.domain_practices.get("backup_frequency")
        has_backup = infrastructure.get("backup_strategy", False)

        if backup_freq and not has_backup:
            recommendations.append(
                Recommendation(
                    category="infrastructure",
                    title=f"Implement {backup_freq} backup strategy",
                    description="Set up automated backups with retention policy",
                    priority="critical" if backup_freq in ["real-time", "hourly"] else "high",
                    confidence=self._calculate_confidence(True, "strong"),
                    reasoning=[
                        f"{self.domain.title()} requires {backup_freq} backups",
                        "Protects against data loss",
                        "Required for disaster recovery",
                    ],
                    evidence=[
                        f"Domain: {self.domain}",
                        f"Required frequency: {backup_freq}",
                        "No backup strategy detected",
                    ],
                    citations=[
                        "3-2-1 backup rule",
                        "Disaster recovery best practices",
                    ],
                    implementation_notes="Test restore procedures regularly",
                    estimated_effort="1d",
                ),
            )

        return recommendations

    def generate_full_recommendations(self) -> RecommendationBundle:
        """
        Generate complete recommendation bundle.

        Returns:
            RecommendationBundle with all recommendations
        """
        return RecommendationBundle(
            project_identity=self.recommend_project_identity(),
            code_quality=self.recommend_code_quality(),
            testing=self.recommend_testing(),
            security=self.recommend_security(),
            devops=self.recommend_devops(),
            infrastructure=self.recommend_infrastructure(),
            metadata={
                "domain": self.domain,
                "scale": self.scale,
                "language": self.language,
                "total_recommendations": sum(
                    [
                        len(self.recommend_project_identity()),
                        len(self.recommend_code_quality()),
                        len(self.recommend_testing()),
                        len(self.recommend_security()),
                        len(self.recommend_devops()),
                        len(self.recommend_infrastructure()),
                    ],
                ),
                "engine_version": cco_version,
            },
        )


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================


def prioritize_recommendations(bundle: RecommendationBundle) -> List[Recommendation]:
    """
    Sort all recommendations by priority and confidence.

    Args:
        bundle: Complete recommendation bundle

    Returns:
        Flat list of recommendations sorted by priority/confidence
    """
    all_recs = (
        bundle.project_identity
        + bundle.code_quality
        + bundle.testing
        + bundle.security
        + bundle.devops
        + bundle.infrastructure
    )

    priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}

    return sorted(
        all_recs,
        key=lambda r: (priority_order[r.priority], -r.confidence),
    )


def filter_recommendations(
    bundle: RecommendationBundle,
    min_confidence: float = 0.0,
    categories: Optional[List[str]] = None,
    priorities: Optional[List[str]] = None,
) -> List[Recommendation]:
    """
    Filter recommendations by criteria.

    Args:
        bundle: Complete recommendation bundle
        min_confidence: Minimum confidence threshold (0.0-1.0)
        categories: List of categories to include (e.g., ["security", "testing"])
        priorities: List of priorities to include (e.g., ["critical", "high"])

    Returns:
        Filtered list of recommendations
    """
    all_recs = prioritize_recommendations(bundle)

    filtered = [r for r in all_recs if r.confidence >= min_confidence]

    if categories:
        filtered = [r for r in filtered if r.category in categories]

    if priorities:
        filtered = [r for r in filtered if r.priority in priorities]

    return filtered


def format_recommendation_markdown(rec: Recommendation) -> str:
    """
    Format single recommendation as markdown.

    Args:
        rec: Recommendation to format

    Returns:
        Markdown string
    """
    md = f"### {rec.title}\n\n"
    md += f"**Category:** {rec.category}  \n"
    md += f"**Priority:** {rec.priority.upper()}  \n"
    md += f"**Confidence:** {rec.confidence:.0%}\n\n"
    md += f"{rec.description}\n\n"

    if rec.reasoning:
        md += "**Reasoning:**\n"
        for reason in rec.reasoning:
            md += f"- {reason}\n"
        md += "\n"

    if rec.evidence:
        md += "**Evidence:**\n"
        for evidence in rec.evidence:
            md += f"- {evidence}\n"
        md += "\n"

    if rec.citations:
        md += "**References:**\n"
        for citation in rec.citations:
            md += f"- {citation}\n"
        md += "\n"

    if rec.implementation_notes:
        md += f"**Implementation:** {rec.implementation_notes}\n\n"

    if rec.estimated_effort:
        md += f"**Estimated effort:** {rec.estimated_effort}\n\n"

    md += "---\n\n"

    return md

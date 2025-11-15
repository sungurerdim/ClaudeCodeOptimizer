"""
Dynamic Principle Selection - CCO 3.0

Selects applicable development principles based on user preferences.
Generates PRINCIPLES.md for @mention in Claude Code.
"""

from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, TypeVar

from .constants import MIN_COVERAGE_PERCENTAGE

T = TypeVar("T")


class PrincipleSelector:
    """
    Select applicable principles based on user preferences.

    Reads 52 principles from knowledge base, filters based on:
    - User preferences (team size, security stance, etc.)
    - Project type and language
    - Compliance requirements

    Generates PRINCIPLES.md for Claude Code @mention.
    """

    def __init__(self, preferences: Dict[str, Any]) -> None:
        """
        Initialize selector with user preferences.

        Args:
            preferences: User preferences dictionary from CCOPreferences.dict()
        """
        self.preferences = preferences
        self.all_principles = self._load_principles()

    def _load_principles(self) -> List[Dict[str, Any]]:
        """Load all principles from .md files"""
        from .principle_md_loader import load_all_principles

        principles_dir = Path(__file__).parent.parent.parent / "content" / "principles"
        principles = load_all_principles(principles_dir)

        # Deduplicate by ID (defense mechanism)
        seen_ids = set()
        deduplicated = []

        for principle in principles:
            pid = principle.get("id")
            if pid not in seen_ids:
                seen_ids.add(pid)
                deduplicated.append(principle)

        return deduplicated

    def select_applicable(self) -> List[Dict[str, Any]]:
        """
        Select principles that apply to this project.

        Returns:
            List of applicable principle dictionaries, sorted by severity
        """
        applicable = []

        for principle in self.all_principles:
            if self._is_applicable(principle):
                # Add enforcement level based on preferences
                principle = self._add_enforcement_level(principle)
                applicable.append(principle)

        return self._sort_by_priority(applicable)

    def _is_applicable(self, principle: Dict[str, Any]) -> bool:
        """
        Check if a principle applies to this project.

        Evaluates:
        - User-selected principle IDs (if provided)
        - Severity vs linting strictness
        - Category vs project characteristics
        - Project type matching
        - Language compatibility
        - Preference conditions
        - Team size requirements

        Returns:
            True if principle should be enforced
        """
        # If user has pre-selected specific principles, only use those
        selected_ids = self.preferences.get("selected_principle_ids", [])
        if selected_ids:
            return principle.get("id") in selected_ids

        # Check severity vs linting strictness
        if not self._check_severity_match(principle):
            return False

        # Check category relevance
        if not self._check_category_relevance(principle):
            return False

        applicability = principle.get("applicability", {})

        # Check project type matching
        project_types = applicability.get("project_types", ["all"])
        if project_types != ["all"]:
            # Get detected project types from preferences
            detected_types_raw = self._get_nested_value(self.preferences, "project_identity.types")
            detected_types = detected_types_raw if isinstance(detected_types_raw, list) else []
            # Check if any detected type matches required types (exact match)
            if not any(dtype in project_types for dtype in detected_types):
                return False

        # Check preference-based conditions
        conditions = applicability.get("preference_conditions", [])
        for condition in conditions:
            if not self._evaluate_condition(condition):
                return False

        # Check team size exclusions
        if not self._check_team_size(principle):
            return False

        # Check security stance requirements
        if not self._check_security_stance(principle):
            return False

        return True

    def _evaluate_condition(self, condition: Dict[str, Any]) -> bool:
        """
        Evaluate a single preference condition.

        Condition format:
        {
            "path": "code_quality.linting_strictness",
            "operator": "in",
            "values": ["strict", "pedantic"]
        }
        """
        path = condition.get("path", "")
        operator = condition.get("operator", "in")
        values = condition.get("values", [])

        # Get preference value
        pref_value = self._get_nested_value(self.preferences, path)
        if pref_value is None:
            return False

        # Evaluate operator
        if operator == "in":
            return pref_value in values
        elif operator == "not_in":
            return pref_value not in values
        elif operator == "contains_any":
            if isinstance(pref_value, list):
                return any(v in values for v in pref_value)
            return pref_value in values
        elif operator == ">=":
            try:
                # Handle percentage strings like "90"
                pref_int = int(str(pref_value).replace("%", ""))
                threshold = int(str(values[0]).replace("%", ""))
                return pref_int >= threshold
            except (ValueError, TypeError):
                return False
        elif operator == "<=":
            try:
                pref_int = int(str(pref_value).replace("%", ""))
                threshold = int(str(values[0]).replace("%", ""))
                return pref_int <= threshold
            except (ValueError, TypeError):
                return False

        return True

    def _get_nested_value(self, obj: dict[str, Any] | object, path: str) -> object | None:
        """
        Get value from nested path.

        Example: "code_quality.linting_strictness"
        """
        if not path:
            return None

        parts = path.split(".")
        current = obj

        for part in parts:
            if isinstance(current, dict):
                current = current.get(part)
            elif hasattr(current, part):
                current = getattr(current, part)
            else:
                return None

            if current is None:
                return None

        return current

    def _check_team_size(self, principle: Dict[str, Any]) -> bool:
        """Check if principle applies to current team size"""
        # Get team size from preferences
        team_size = self._get_nested_value(self.preferences, "project_identity.team_trajectory")

        # Some principles don't apply to solo devs
        team_only_ids = [
            "P_MICROSERVICES_SERVICE_MESH",
            "P_CQRS_PATTERN",
            "P_CIRCUIT_BREAKER_PATTERN",
        ]  # Complex architecture patterns
        if principle["id"] in team_only_ids and team_size == "solo":
            return False

        return True

    def _check_security_stance(self, principle: Dict[str, Any]) -> bool:
        """Check if principle applies based on security stance"""
        category = principle.get("category", "")
        if category != "security_privacy":
            return True  # Non-security principles always apply

        # Get security stance
        stance = self._get_nested_value(self.preferences, "security.security_stance")

        # High security principles require strict stance
        high_security_ids = [
            "P_CONTAINER_SECURITY",
            "P_K8S_SECURITY",
            "P_ZERO_TRUST",
            "P_PRIVACY_COMPLIANCE",
        ]
        if principle["id"] in high_security_ids:
            return stance in ["zero-trust", "paranoid", "very-strict", "strict"]

        return True

    def _check_severity_match(self, principle: Dict[str, Any]) -> bool:
        """
        Check if principle importance matches linting strictness.

        Uses weight (5-10) and severity to determine if principle applies.
        Weight represents principle importance across all contexts.

        Filters based on strictness:
        - paranoid/pedantic: All principles (weight >= 5)
        - strict: Core + important (weight >= 8) → ~40% of total
        - standard: Essential (weight >= 9) → ~20% of total
        - moderate/relaxed: Critical only (weight >= 10) → ~10% of total

        Weight thresholds are fixed, but resulting count scales with available principles.

        Security Override: If security_stance is strict/very-strict and principle
        is security-related (severity high/critical), lower threshold to 8.
        """
        weight = principle.get("weight", 5)
        severity = principle.get("severity", "medium")
        category = principle.get("category", "")
        strictness = self._get_nested_value(self.preferences, "code_quality.linting_strictness")
        security_stance = self._get_nested_value(self.preferences, "security.security_stance")

        # Map strictness to minimum weight threshold
        # NOTE: Thresholds are fixed, but available principles may vary
        weight_thresholds = {
            "paranoid": 5,  # All principles
            "pedantic": 6,  # Most principles
            "strict": 8,  # Core + important
            "standard": 9,  # Essential
            "moderate": 10,  # Critical only
            "relaxed": 10,  # Critical only
        }

        strictness_str = str(strictness) if strictness is not None else "standard"
        min_weight = weight_thresholds.get(strictness_str, 9)

        # Security override: For API/web projects or high security stance,
        # lower threshold for security principles to weight >= 8
        project_types_raw = self._get_nested_value(self.preferences, "project_identity.types")
        project_types = project_types_raw if isinstance(project_types_raw, list) else []
        is_api_or_web = any(
            pt in ["api", "web", "web-app", "microservice", "backend", "api_service"]
            for pt in project_types
        )
        is_high_security = security_stance in ["strict", "very-strict", "balanced"]

        if is_api_or_web or is_high_security:
            is_security = category in ["security_privacy", "api_design"] or severity in [
                "high",
                "critical",
            ]
            if is_security and weight >= 8:
                return True  # Accept all high+ security principles for APIs/web/microservices

        return weight >= min_weight

    def _check_category_relevance(self, principle: Dict[str, Any]) -> bool:
        """
        Check if principle category is relevant to project characteristics.

        Filters based on:
        - Team size (solo vs team)
        - Project maturity (prototype vs production)
        - Security stance
        """
        category = principle.get("category", "")

        # Git workflow principles - less relevant for solo devs
        # NOTE: Only filter git-workflow related principles, not all project-specific
        git_workflow_principles = [
            "P_BRANCHING_STRATEGY",
            "P_PR_GUIDELINES",
            "P_REBASE_VS_MERGE_STRATEGY",
            "P_COMMIT_MESSAGE_CONVENTIONS",
        ]
        if category == "project-specific" and principle["id"] in git_workflow_principles:
            team_size = self._get_nested_value(self.preferences, "project_identity.team_trajectory")
            if team_size == "solo":
                # Only keep essential git principles for solo devs
                return principle["id"] in ["P_COMMIT_MESSAGE_CONVENTIONS"]

        # Operations principles - less relevant for early stage
        # NOTE: Only filter non-critical operations, keep critical principles
        operations_principles = [
            "P_CONFIGURATION_AS_CODE",
            "P_GITOPS_PRACTICES",
            "P_GRACEFUL_SHUTDOWN",
            "P_HEALTH_CHECKS",
            "P_IAC_GITOPS",
            "P_INCIDENT_RESPONSE_READINESS",
            "P_OBSERVABILITY_WITH_OTEL",
        ]
        if category == "project-specific" and principle["id"] in operations_principles:
            maturity = self._get_nested_value(self.preferences, "project_identity.project_maturity")
            if maturity in ["prototype", "mvp"]:
                # Only keep critical operations principles
                severity = principle.get("severity", "low")
                return severity == "critical"

        # Architecture principles - some only relevant for larger teams
        if category == "architecture":
            team_size = self._get_nested_value(self.preferences, "project_identity.team_trajectory")
            if team_size == "solo":
                # Exclude complex architecture patterns for solo
                exclude_for_solo = [
                    "P_MICROSERVICES_SERVICE_MESH",
                    "P_CQRS_PATTERN",
                    "P_CIRCUIT_BREAKER_PATTERN",
                ]
                if principle["id"] in exclude_for_solo:
                    return False

        return True

    def _add_enforcement_level(self, principle: Dict[str, Any]) -> Dict[str, Any]:
        """Add enforcement level based on preferences"""
        principle = principle.copy()

        # Get linting strictness
        strictness = self._get_nested_value(self.preferences, "code_quality.linting_strictness")

        # Map to enforcement level
        enforcement_map = {
            "paranoid": "MUST - No exceptions",
            "pedantic": "MUST - No exceptions",
            "strict": "SHOULD - Requires justification",
            "standard": "SHOULD - Use best judgment",
            "moderate": "RECOMMENDED - Optional",
            "relaxed": "OPTIONAL",
        }

        strictness_str = str(strictness) if strictness is not None else "standard"
        principle["enforcement"] = enforcement_map.get(strictness_str, "RECOMMENDED")

        return principle

    def _sort_by_priority(self, principles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Sort principles by severity and ID"""
        severity_order = {
            "critical": 0,
            "high": 1,
            "medium": 2,
            "low": 3,
        }

        return sorted(
            principles,
            key=lambda p: (
                severity_order.get(p.get("severity", "low"), 4),
                p.get("id", ""),
            ),
        )

    def get_skipped_principles(self) -> List[Dict[str, Any]]:
        """Get list of principles that don't apply"""
        applicable_ids = {p["id"] for p in self.select_applicable()}
        all_ids = {p["id"] for p in self.all_principles}
        skipped_ids = all_ids - applicable_ids

        skipped = []
        for principle in self.all_principles:
            if principle["id"] in skipped_ids:
                # Add reason for skipping
                principle = principle.copy()
                principle["skip_reason"] = self._get_skip_reason(principle)
                skipped.append(principle)

        return sorted(skipped, key=lambda p: p["id"])

    def _get_skip_reason(self, principle: Dict[str, Any]) -> str:
        """Determine why a principle was skipped"""
        # Check team size
        team_size = self._get_nested_value(self.preferences, "project_identity.team_trajectory")
        if (
            principle["id"]
            in ["P_MICROSERVICES_SERVICE_MESH", "P_CQRS_PATTERN", "P_CIRCUIT_BREAKER_PATTERN"]
            and team_size == "solo"
        ):
            return f"Solo developer (team_trajectory = '{team_size}')"

        # Check security stance
        stance = self._get_nested_value(self.preferences, "security.security_stance")
        if principle.get("category") == "security_privacy":
            if principle["id"] in [
                "P_CONTAINER_SECURITY",
                "P_K8S_SECURITY",
                "P_ZERO_TRUST",
                "P_PRIVACY_COMPLIANCE",
            ]:
                if stance not in ["zero-trust", "paranoid", "very-strict", "strict"]:
                    return f"Security stance too permissive (security_stance = '{stance}')"

        # Check testing coverage
        coverage = self._get_nested_value(self.preferences, "testing.coverage_target")
        if principle["id"] in ["P_PROPERTY_TESTING"]:  # Mutation/property testing
            try:
                cov_int = int(str(coverage).replace("%", ""))
                if cov_int < MIN_COVERAGE_PERCENTAGE:
                    return f"Coverage target too low (coverage_target = '{coverage}%')"
            except (ValueError, TypeError):
                pass

        # Check linting strictness
        strictness = self._get_nested_value(self.preferences, "code_quality.linting_strictness")
        if strictness in ["disabled", "relaxed"]:
            if principle.get("severity") in ["high", "critical"]:
                return f"Linting too relaxed (linting_strictness = '{strictness}')"

        return "Does not match project preferences"

    def generate_statistics(self) -> Dict[str, Any]:
        """Generate statistics about principle selection"""
        applicable = self.select_applicable()

        # Count by severity
        by_severity = {
            "critical": len([p for p in applicable if p.get("severity") == "critical"]),
            "high": len([p for p in applicable if p.get("severity") == "high"]),
            "medium": len([p for p in applicable if p.get("severity") == "medium"]),
            "low": len([p for p in applicable if p.get("severity") == "low"]),
        }

        # Count by category
        by_category: dict[str, int] = {}
        for p in applicable:
            cat = p.get("category", "unknown")
            by_category[cat] = by_category.get(cat, 0) + 1

        return {
            "total_principles": len(self.all_principles),
            "applicable_count": len(applicable),
            "skipped_count": len(self.all_principles) - len(applicable),
            "by_severity": by_severity,
            "by_category": by_category,
            "coverage_percentage": round(len(applicable) / len(self.all_principles) * 100, 1),
        }

    def generate_principles_md(self, output_path: Path) -> Dict[str, Any]:
        """
        Generate PRINCIPLES.md file.

        Args:
            output_path: Path to write PRINCIPLES.md

        Returns:
            Dictionary with generation stats
        """
        applicable = self.select_applicable()
        skipped = self.get_skipped_principles()
        stats = self.generate_statistics()

        # Group by severity
        by_severity = {
            "critical": [p for p in applicable if p.get("severity") == "critical"],
            "high": [p for p in applicable if p.get("severity") == "high"],
            "medium": [p for p in applicable if p.get("severity") == "medium"],
            "low": [p for p in applicable if p.get("severity") == "low"],
        }

        # Generate content
        content = self._render_principles_md(by_severity, skipped, stats)

        # REMOVED: Backup creation - No backups needed (file deprecated)
        # PRINCIPLES.md file itself is deprecated in new architecture

        # Write file
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(content, encoding="utf-8")

        return {
            "success": True,
            "principles_file": str(output_path),
            "applicable_count": len(applicable),
            "total_count": len(self.all_principles),
            "stats": stats,
        }

    def _render_principles_md(
        self,
        by_severity: Dict[str, List[Dict[str, Any]]],
        skipped: List[Dict[str, Any]],
        stats: Dict[str, Any],
    ) -> str:
        """
        Render PRINCIPLES.md content in progressive disclosure format.

        New format (U_NO_OVERENGINEERING):
        - Core principles only (~500 tokens)
        - Links to category files for full details
        - 10x token reduction
        """
        lines = []

        # Header
        lines.append("# Development Principles")
        lines.append("")
        lines.append(f"**Generated**: {datetime.now().strftime('%Y-%m-%d')}")
        lines.append(f"**Total Principles**: {stats['total_principles']} (across all categories)")
        lines.append("**Core Principles**: 3 (always loaded)")
        lines.append("")
        lines.append("---")
        lines.append("")

        # Core principles section
        lines.append("## Quick Reference (Core Principles - Always Apply)")
        lines.append("")
        lines.append("These principles are **MANDATORY** and apply to **ALL work, ALWAYS**.")
        lines.append("")

        # Get core universal principles (fail-fast, evidence-based, no overengineering)
        core_principle_ids = ["U_FAIL_FAST", "U_EVIDENCE_BASED", "U_NO_OVERENGINEERING"]
        all_applicable = []
        for severity_list in by_severity.values():
            all_applicable.extend(severity_list)

        for core_id in core_principle_ids:
            principle = next((p for p in all_applicable if p["id"] == core_id), None)
            if not principle:
                # Try loading from all principles if not in applicable
                principle = next((p for p in self.all_principles if p["id"] == core_id), None)

            if principle:
                lines.append(f"### {principle['id']}: {principle['title']} ⚠️")
                lines.append("")
                lines.append(principle.get("description", ""))
                lines.append("")

                # Key rules
                rules = principle.get("rules", [])
                if rules:
                    lines.append("**Key Rules**:")
                    for rule in rules[:3]:  # Max 3 rules
                        lines.append(f"- {rule.get('description', '')}")
                    lines.append("")

                # Example
                examples = principle.get("examples", {})
                if examples:
                    lines.append("**Example**:")
                    lines.append("```python")
                    if "good" in examples and examples["good"]:
                        lines.append("# ✅ Good")
                        # Decode escaped newlines from JSON (\\n -> actual newline)
                        good_example = examples["good"][0].replace("\\n", "\n")
                        for line in good_example.split("\n"):
                            lines.append(line)
                    if "bad" in examples and examples["bad"]:
                        lines.append("")
                        lines.append("# ❌ Bad")
                        # Decode escaped newlines from JSON (\\n -> actual newline)
                        bad_example = examples["bad"][0].replace("\\n", "\n")
                        for line in bad_example.split("\n"):
                            lines.append(line)
                    lines.append("```")
                    lines.append("")

                lines.append("---")
                lines.append("")

        # Category links section
        lines.append("## Full Principles by Category")
        lines.append("")
        lines.append("For detailed principles, see category-specific documents:")
        lines.append("")

        # Category metadata from knowledge base
        category_info = {
            "core": ("Core Principles", 3, "Always loaded"),
            "code_quality": (
                "Code Quality",
                14,
                "DRY, type safety, immutability, precision, version management",
            ),
            "security_privacy": (
                "Security & Privacy",
                19,
                "Encryption, zero-trust, privacy-first, auth, secrets, input validation",
            ),
            "testing": ("Testing", 6, "Test pyramid, coverage, isolation, integration, CI gates"),
            "architecture": (
                "Architecture",
                10,
                "Event-driven, microservices, separation of concerns, patterns",
            ),
            "performance": (
                "Performance",
                5,
                "Caching, async I/O, database optimization, lazy loading",
            ),
            "operations": (
                "Operational Excellence",
                10,
                "IaC, observability, health checks, config as code",
            ),
            "git_workflow": (
                "Git Workflow",
                5,
                "Commit conventions, branching, PR guidelines, versioning",
            ),
            "api_design": ("API Design", 2, "RESTful conventions, versioning, error handling"),
        }

        for cat_id, (cat_name, count, description) in category_info.items():
            filename = cat_id.replace("_", "-")
            # Use global path (zero-pollution)
            global_path = f"~/.cco/principles/{filename}.md"
            lines.append(f"- **[{cat_name}]({global_path})** - {count} principles")
            lines.append(f"  - {description}")
        lines.append("")
        lines.append("**Note**: All category files stored globally in `~/.cco/principles/`")
        lines.append("")
        lines.append("---")
        lines.append("")

        # Token optimization section
        lines.append("## Token Optimization")
        lines.append("")
        lines.append("**Progressive Disclosure Strategy**:")
        lines.append("- **Core principles** loaded by default: ~500 tokens")
        lines.append("- **Category-specific** principles loaded on-demand: ~500-2000 tokens each")
        lines.append("- **Total available**: ~8000 tokens (all categories)")
        lines.append("")
        lines.append("**Reduction**: 16x (8000 → 500 tokens for typical usage)")
        lines.append("")
        lines.append(
            "Category-specific principles load automatically when running relevant commands:"
        )
        lines.append("- `/cco-audit code` → loads Code Quality principles")
        lines.append("- `/cco-audit security` → loads Security principles")
        lines.append("- `/cco-test` → loads Testing principles")
        lines.append("- `/cco-analyze` → loads Architecture principles")
        lines.append("- `/cco-optimize` → loads Performance principles")
        lines.append("")
        lines.append("---")
        lines.append("")

        # Usage guide
        lines.append("## Using These Principles")
        lines.append("")
        lines.append("### In Claude Code")
        lines.append("")
        lines.append("Reference this file in any conversation:")
        lines.append("```")
        lines.append("@PRINCIPLES.md  # Load core principles")
        lines.append("@PRINCIPLES.md Check if this code follows our principles")
        lines.append("@PRINCIPLES.md What principle applies to error handling?")
        lines.append("```")
        lines.append("")
        lines.append("For category-specific principles:")
        lines.append("```")
        lines.append("@~/.cco/principles/security.md  # Load security principles")
        lines.append("@~/.cco/principles/testing.md   # Load testing principles")
        lines.append("```")
        lines.append("")
        lines.append("### In Commands")
        lines.append("")
        lines.append("All CCO commands use these principles:")
        lines.append("- `/cco-audit code` - Check code quality principles")
        lines.append("- `/cco-audit security` - Check security principles")
        lines.append("- `/cco-audit all` - Check all applicable principles")
        lines.append("- `/cco-fix` - Auto-fix violations")
        lines.append("")
        lines.append("### Updating Principles")
        lines.append("")
        lines.append("Your principles are based on project detection. To update:")
        lines.append("")
        lines.append("1. **Regenerate**: Run `/cco-init` (interactive or quick mode)")
        lines.append("2. **Review changes**: Check `git diff PRINCIPLES.md`")
        lines.append("")
        lines.append(
            "Note: CCO is stateless - no config files to edit. Principles selected based on live codebase analysis."
        )
        lines.append("")
        lines.append("---")
        lines.append("")

        # Footer
        lines.append("*Auto-generated by ClaudeCodeOptimizer*")
        lines.append(f"*Principle Database: {stats['total_principles']} total principles*")
        lines.append("*Reference with: @PRINCIPLES.md*")

        return "\n".join(lines)

    def generate_category_files(self, docs_path: Path) -> Dict[str, Any]:
        """
        Generate category-specific principle files in ~/.cco/principles/

        Args:
            docs_path: Path to ~/.cco/principles/ directory

        Returns:
            Dictionary with generation stats
        """
        # Category metadata
        categories = {
            "core": "Core Principles",
            "code_quality": "Code Quality Principles",
            "security_privacy": "Security & Privacy Principles",
            "testing": "Testing Principles",
            "architecture": "Architecture Principles",
            "performance": "Performance Principles",
            "operations": "Operational Excellence Principles",
            "git_workflow": "Git Workflow Principles",
            "api_design": "API Design Principles",
        }

        # Create docs_path if doesn't exist
        docs_path.mkdir(parents=True, exist_ok=True)

        generated_files = []
        severity_emoji = {
            "critical": "🔴",
            "high": "🟠",
            "medium": "🟡",
            "low": "🟢",
        }

        for category_id, category_name in categories.items():
            # Get principles for this category
            if category_id == "core":
                # Core universal principles: fail-fast, evidence-based, no overengineering
                principles = [
                    p
                    for p in self.all_principles
                    if p["id"] in ["U_FAIL_FAST", "U_EVIDENCE_BASED", "U_NO_OVERENGINEERING"]
                ]
            else:
                principles = [p for p in self.all_principles if p.get("category") == category_id]

            if not principles:
                continue

            # Sort by ID
            principles = sorted(principles, key=lambda p: p["id"])

            # Generate file content
            lines = []
            lines.append(f"# {category_name}")
            lines.append("")
            lines.append(f"**Generated**: {datetime.now().strftime('%Y-%m-%d')}")
            lines.append(f"**Principle Count**: {len(principles)}")
            lines.append("")
            lines.append("---")
            lines.append("")

            for p in principles:
                # Principle header
                emoji = severity_emoji.get(p.get("severity", "low"), "🟢")
                lines.append(f"### {p['id']}: {p['title']} {emoji}")
                lines.append("")
                lines.append(f"**Severity**: {p.get('severity', 'low').title()}")
                lines.append("")
                lines.append(p.get("description", ""))
                lines.append("")

                # Languages (if specified)
                languages = p.get("applicability", {}).get("languages", [])
                if languages and languages != ["all"]:
                    langs_str = ", ".join(languages)
                    lines.append(f"**Languages**: {langs_str}")
                    lines.append("")

                # Rules
                rules = p.get("rules", [])
                if rules:
                    lines.append("**Rules**:")
                    for rule in rules[:5]:  # Max 5 rules
                        lines.append(f"- {rule.get('description', '')}")
                    lines.append("")

                # Examples
                examples = p.get("examples", {})
                if examples:
                    if "bad" in examples and examples["bad"]:
                        lines.append("**❌ Bad**:")
                        lines.append("```")
                        lines.append(examples["bad"][0])
                        lines.append("```")
                        lines.append("")

                    if "good" in examples and examples["good"]:
                        lines.append("**✅ Good**:")
                        lines.append("```")
                        lines.append(examples["good"][0])
                        lines.append("```")
                        lines.append("")

                lines.append("---")
                lines.append("")

            # Footer
            lines.append("---")
            lines.append("")
            lines.append(
                "**Loading**: These principles load automatically when running relevant commands"
            )
            lines.append("")
            lines.append(
                "**Reference**: Use `@PRINCIPLES.md` to load core principles, or reference this file directly"
            )

            # Write file
            filename = category_id.replace("_", "-") + ".md"
            file_path = docs_path / filename
            file_path.write_text("\n".join(lines), encoding="utf-8")
            generated_files.append(str(file_path))

        return {
            "success": True,
            "generated_files": generated_files,
            "file_count": len(generated_files),
        }

    # REMOVED: _create_backup() - No backups needed with stateless architecture
    # PRINCIPLES.md file deprecated - using individual principle files in ~/.cco/principles/


# Utility function for easy access
def generate_principles_from_preferences(
    preferences: Dict[str, Any],
    output_path: Path,
) -> Dict[str, Any]:
    """
    Convenience function to generate PRINCIPLES.md.

    Args:
        preferences: User preferences dictionary
        output_path: Path to write PRINCIPLES.md

    Returns:
        Generation result with stats
    """
    selector = PrincipleSelector(preferences)
    return selector.generate_principles_md(output_path)

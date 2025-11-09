"""
Cascading AI Recommendation Engine

Generates context-aware recommendations for each decision point.
Uses accumulated answers from previous questions to provide
personalized suggestions.

Key principle: Each recommendation builds on previous decisions.
"""

from typing import Dict

from .models import AnswerContext


class RecommendationEngine:
    """Generate AI recommendations based on context"""

    def __init__(self) -> None:
        """Initialize recommendation engine"""
        pass

    # ========================================================================
    # TIER 1: Fundamental Decisions
    # ========================================================================

    def recommend_project_purpose(self, context: AnswerContext) -> str:
        """Recommend project types based on detected frameworks/structure"""
        sys = context.system
        detected = sys.detected_project_types

        if detected:
            types_str = ", ".join(detected)
            return f"💡 Detected: {types_str}"

        # Infer from frameworks
        if any(fw in sys.detected_frameworks for fw in ["fastapi", "flask", "django-rest"]):
            return "💡 API/Backend frameworks detected → Consider 'API/Backend Service'"

        if any(fw in sys.detected_frameworks for fw in ["react", "vue", "next", "nuxt"]):
            return "💡 Web frameworks detected → Consider 'Web Application'"

        if sys.file_count < 20:
            return "💡 Small project → Likely 'CLI Tool' or 'Library/SDK'"

        return "💡 Select all that apply - projects can serve multiple purposes"

    def recommend_team_dynamics(self, context: AnswerContext) -> str:
        """Recommend team size based on git history"""
        sys = context.system

        # TODO: Actually check git log for contributors
        # For now, use simple heuristic
        if sys.is_git_repo and sys.has_ci:
            return "💡 CI detected → Likely team collaboration (Small Team or larger)"

        return "💡 Solo: Just you | Small Team: 2-5 people close collaboration"

    def recommend_project_maturity(self, context: AnswerContext) -> str:
        """Recommend maturity stage based on project signals"""
        sys = context.system

        if not sys.has_tests and sys.file_count < 50:
            return "💡 No tests, small codebase → Likely 'Prototype/POC'"

        if sys.has_tests and not sys.has_ci:
            return "💡 Has tests but no CI → Likely 'MVP/Early Development'"

        if sys.has_tests and sys.has_ci:
            return "💡 Tests + CI detected → Likely 'Active Development' or 'Production'"

        return "💡 Choose based on stability requirements and user dependence"

    def recommend_development_philosophy(self, context: AnswerContext) -> str:
        """Recommend philosophy based on maturity and team"""
        maturity = context.maturity

        if maturity == "prototype":
            return "💡 Prototype stage → 'Move Fast & Iterate' recommended"

        if maturity in ["production", "mature"]:
            return "💡 Production system → 'Quality-First & Thorough' recommended"

        return "💡 Most projects benefit from 'Balanced & Pragmatic' approach"

    # ========================================================================
    # TIER 2: Strategy Decisions
    # ========================================================================

    def recommend_principle_strategy(self, context: AnswerContext) -> str:
        """Recommend principle selection strategy"""
        team = context.team_size
        maturity = context.maturity
        philosophy = context.philosophy

        # Quality-first always wants comprehensive
        if philosophy == "quality_first":
            return "💡 Quality-first philosophy → 'Comprehensive/Strict' recommended"

        # Fast iteration wants minimal
        if philosophy == "move_fast" or maturity == "prototype":
            return "💡 Fast iteration focus → 'Minimal/Pragmatic' recommended"

        # Large teams benefit from strict
        if team in ["growing_team", "large_org"]:
            return "💡 Larger team → 'Comprehensive/Strict' helps coordination"

        # Default: recommended preset
        return "💡 'Recommended Preset' balances quality and pragmatism for your context"

    def recommend_testing_approach(self, context: AnswerContext) -> str:
        """Recommend testing strategy"""
        maturity = context.maturity
        philosophy = context.philosophy
        sys = context.system

        # No tests detected
        if not sys.has_tests:
            if maturity == "prototype":
                return "💡 Prototype + no tests → 'No Tests Yet' is normal"
            else:
                return "💡 No tests detected → Start with 'Critical Paths Only'"

        # Quality-first wants comprehensive
        if philosophy == "quality_first":
            return "💡 Quality-first approach → 'Comprehensive Testing' recommended"

        # Production systems need good coverage
        if maturity in ["production", "mature"]:
            return "💡 Production system → 'Balanced Testing' or 'Comprehensive' recommended"

        # Default balanced
        return "💡 'Balanced Testing' offers best ROI for most projects"

    def recommend_security_stance(self, context: AnswerContext) -> str:
        """Recommend security posture"""
        project_types = context.project_types
        maturity = context.maturity

        # APIs need good security
        if any(t in project_types for t in ["api", "backend", "web_app"]):
            return "💡 API/Web app → 'Production Security' recommended for external-facing systems"

        # Production systems need security
        if maturity in ["production", "mature"]:
            return "💡 Production system → 'Production Security' recommended"

        # Prototypes can start simple
        if maturity == "prototype":
            return "💡 Prototype → 'Standard Security' sufficient, upgrade later"

        return "💡 'Production Security' recommended for most production systems"

    def recommend_documentation_level(self, context: AnswerContext) -> str:
        """Recommend documentation level"""
        project_types = context.project_types
        team = context.team_size

        # Libraries need extensive docs
        if "library" in project_types or "sdk" in project_types:
            return "💡 Library/SDK → 'Comprehensive' docs essential for users"

        # Solo devs can be minimal
        if team == "solo":
            return "💡 Solo developer → 'Minimal' often sufficient, saves time"

        # Teams benefit from practical docs
        if team in ["small_team", "growing_team"]:
            return "💡 Team project → 'Practical' docs help collaboration"

        return "💡 'Practical' balances usefulness and time investment"

    def recommend_git_workflow(self, context: AnswerContext) -> str:
        """Recommend Git workflow based on team size and maturity"""
        team = context.team_size
        maturity = context.maturity

        # Solo developers
        if team == "solo":
            return "💡 Solo developer → 'Main-Only' recommended (simple, fast)"

        # Large teams
        if team in ["large_org"]:
            return "💡 Large team → 'Git Flow' recommended (formal process, structured releases)"

        # Small/medium teams
        if team in ["small_team", "growing_team"]:
            if maturity in ["production", "mature"]:
                return "💡 Production system + team → 'Git Flow' for stability"
            return "💡 Small team → 'GitHub Flow' recommended (balanced approach)"

        # Default
        return "💡 'GitHub Flow' balances structure and agility for most teams"

    # ========================================================================
    # TIER 3: Tactical Decisions
    # ========================================================================

    def recommend_tool_preference(self, category: str, tools: list, context: AnswerContext) -> str:
        """Recommend specific tool from competing options"""
        from .tool_comparison import ToolComparator

        comparator = ToolComparator(tools)
        comparison = comparator.analyze_category(category)

        if not comparison:
            return f"💡 {tools[0]} detected"

        recommended = comparison.recommended
        reason = comparison.reason

        detected_str = ", ".join(comparison.tools)
        return f"💡 You have: {detected_str}\n   Recommend: {recommended} → {reason}"

    def recommend_commands(self, context: AnswerContext) -> Dict[str, str]:
        """
        Recommend which commands to enable based on context.

        Returns dict: {command_id: reason}
        """
        recommendations = {}
        sys = context.system
        maturity = context.maturity
        philosophy = context.philosophy
        testing = context.testing_approach
        security = context.security_stance

        # Core commands (always recommended)
        recommendations["cco-status"] = "Core: Quick health check"
        recommendations["cco-config"] = "Core: Manage configuration"

        # Audit commands
        if philosophy in ["balanced", "quality_first"] or maturity in [
            "production",
            "mature",
        ]:
            recommendations["cco-audit"] = "Your context: Regular codebase reviews valuable"

        # Analysis
        if maturity in ["mvp", "active_dev"]:
            recommendations["cco-analyze"] = "Your context: Growing codebase benefits from analysis"

        # Fix commands
        if sys.existing_tools:  # Has linters/formatters
            recommendations["cco-fix"] = "Detected tools: Auto-fix saves time"

        # Code optimization
        if sys.file_count > 100 or sys.line_count > 5000:
            recommendations["cco-optimize-code"] = "Large codebase: Remove unused code"

        # Dependencies
        if len(sys.existing_tools) > 5:
            recommendations["cco-optimize-deps"] = "Many tools: Check for outdated dependencies"

        # Testing
        if testing in ["balanced", "comprehensive"]:
            recommendations["cco-generate"] = "Testing focus: Generate tests/fixtures"

        # Security
        if security in ["production", "high"]:
            recommendations["cco-scan-secrets"] = "Security focus: Scan for exposed secrets"
            recommendations["cco-fix-security"] = "Security focus: Auto-fix vulnerabilities"

        # Docker
        if "docker" in sys.existing_tools:
            recommendations["cco-optimize-docker"] = "Docker detected: Optimize Dockerfiles"

        return recommendations

    # ========================================================================
    # Main Recommendation Generator
    # ========================================================================

    def generate_recommendation(self, question_id: str, context: AnswerContext) -> str:
        """
        Generate contextual recommendation for any question.

        Args:
            question_id: ID of the decision point
            context: Current answer context

        Returns:
            Recommendation string (or empty if none)
        """
        # Map question IDs to recommendation methods
        generators = {
            # TIER 1
            "project_purpose": self.recommend_project_purpose,
            "team_dynamics": self.recommend_team_dynamics,
            "project_maturity": self.recommend_project_maturity,
            "development_philosophy": self.recommend_development_philosophy,
            # TIER 2
            "principle_strategy": self.recommend_principle_strategy,
            "testing_approach": self.recommend_testing_approach,
            "security_stance": self.recommend_security_stance,
            "documentation_level": self.recommend_documentation_level,
            "git_workflow": self.recommend_git_workflow,
        }

        generator = generators.get(question_id)
        if generator:
            try:
                return generator(context)
            except Exception as e:
                # Fallback if recommendation fails
                return f"💡 Recommendation unavailable: {e}"

        return ""

    # ========================================================================
    # Helper: Explain Why Question Matters
    # ========================================================================

    def explain_question_importance(self, question_id: str, context: AnswerContext) -> str:
        """
        Explain why we're asking this question given the context.

        This helps users understand the decision tree flow.
        """
        explanations = {
            "project_purpose": "🎯 Understanding your project type helps us recommend relevant principles and tools",
            "team_dynamics": "👥 Team size affects collaboration practices, review processes, and tooling needs",
            "project_maturity": "📈 Project stage determines quality requirements and appropriate trade-offs",
            "development_philosophy": "⚡ Your approach shapes all tactical decisions: speed vs quality, testing depth, etc.",
            "principle_strategy": "📋 This determines how many principles to enforce (minimal, balanced, or comprehensive)",
            "testing_approach": "🧪 Testing strategy affects principle selection, CI/CD setup, and quality expectations",
            "security_stance": "🔒 Security needs determine validation strictness, audit requirements, and best practices",
            "documentation_level": "📝 Documentation choices affect time investment and collaboration effectiveness",
            "git_workflow": "🔀 Git workflow determines branching strategy, code review process, and release management",
        }

        return explanations.get(question_id, "")


# Convenience functions
def get_recommendation(question_id: str, context: AnswerContext) -> str:
    """Get AI recommendation for a question"""
    engine = RecommendationEngine()
    return engine.generate_recommendation(question_id, context)


def explain_why(question_id: str, context: AnswerContext) -> str:
    """Explain why we're asking this question"""
    engine = RecommendationEngine()
    return engine.explain_question_importance(question_id, context)


def recommend_commands(context: AnswerContext) -> Dict[str, str]:
    """Get command recommendations"""
    engine = RecommendationEngine()
    return engine.recommend_commands(context)

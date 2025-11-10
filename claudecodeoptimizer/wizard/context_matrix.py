"""
Context Matrix - Team-Aware Recommendation Engine

Multi-factor recommendation system based on team_size × maturity × philosophy.

Pattern from CCO P0.8: Context-aware configuration
"""

from typing import Dict, List

from .models import AnswerContext, Option


class ContextMatrix:
    """Context-aware recommendation engine for wizard decisions"""

    def recommend_versioning_strategy(
        self, team_size: str, maturity: str, has_ci: bool
    ) -> Dict:
        """
        Recommend versioning strategy based on context.

        Args:
            team_size: "solo", "small_team", "large_org"
            maturity: "prototype", "mvp", "production", "legacy"
            has_ci: Whether CI/CD is configured

        Returns:
            Dict with strategy, reason, alternatives
        """
        # Solo developer: Zero overhead automation
        if team_size == "solo":
            return {
                "strategy": "auto_semver",
                "reason": "Zero overhead - automatic versioning from commit messages",
                "alternatives": {
                    "manual_semver": "If you prefer explicit control",
                    "calver": "For date-based releases",
                },
            }

        # Small team: PR-based with peer review
        if team_size == "small_team":
            if has_ci and maturity in ["production", "legacy"]:
                return {
                    "strategy": "pr_based_semver",
                    "reason": "Automated versioning triggered by PR merge",
                    "alternatives": {
                        "auto_semver": "Less overhead but no review gate",
                        "manual_semver": "More control but more overhead",
                    },
                }
            else:
                return {
                    "strategy": "auto_semver",
                    "reason": "Automated versioning - upgrade to PR-based when you add CI",
                    "alternatives": {
                        "manual_semver": "If you prefer explicit control",
                    },
                }

        # Large organization: Manual with release managers
        if team_size == "large_org":
            return {
                "strategy": "manual_semver",
                "reason": "Controlled releases by release managers",
                "alternatives": {
                    "pr_based_semver": "If you have strong automation",
                },
            }

        # Default: auto_semver
        return {
            "strategy": "auto_semver",
            "reason": "Balanced approach for most projects",
            "alternatives": {},
        }

    def recommend_principle_intensity(
        self, team_size: str, maturity: str, philosophy: str
    ) -> Dict:
        """
        Recommend how many principles to apply.

        Args:
            team_size: "solo", "small_team", "large_org"
            maturity: "prototype", "mvp", "production", "legacy"
            philosophy: "move_fast", "balanced", "quality_first"

        Returns:
            Dict with intensity, principle_count, categories, reason
        """
        # Calculate intensity score (1-10)
        score = 5  # Base score

        # Team size impact
        if team_size == "solo":
            score += 0
        elif team_size == "small_team":
            score += 1
        elif team_size == "large_org":
            score += 3

        # Maturity impact
        if maturity == "prototype":
            score -= 2
        elif maturity == "mvp":
            score += 0
        elif maturity in ["production", "legacy"]:
            score += 2

        # Philosophy impact
        if philosophy == "move_fast":
            score -= 1
        elif philosophy == "balanced":
            score += 0
        elif philosophy == "quality_first":
            score += 2

        # Clamp to 1-10
        score = max(1, min(10, score))

        # Map score to intensity level and principle categories
        if score <= 3:
            intensity = "minimal"
            categories = ["core"]
            principle_count = "5-10"
        elif score <= 6:
            intensity = "recommended"
            categories = ["core", "code-quality", "security"]
            principle_count = "20-30"
        elif score <= 8:
            intensity = "comprehensive"
            categories = [
                "core",
                "code-quality",
                "security",
                "testing",
                "architecture",
            ]
            principle_count = "40-50"
        else:
            intensity = "maximum"
            categories = ["all"]
            principle_count = "70+"

        return {
            "intensity": intensity,
            "principle_count": principle_count,
            "categories": categories,
            "score": score,
            "reason": self._get_principle_intensity_reason(
                team_size, maturity, philosophy, intensity
            ),
        }

    def _get_principle_intensity_reason(
        self, team_size: str, maturity: str, philosophy: str, intensity: str
    ) -> str:
        """Get human-readable reason for principle intensity"""
        reasons = []

        if intensity == "minimal":
            reasons.append("Focus on core principles only")
            if maturity == "prototype":
                reasons.append("Prototype phase - minimize overhead")
            if philosophy == "move_fast":
                reasons.append("Move fast - avoid over-engineering")

        elif intensity == "recommended":
            reasons.append("Balanced approach for most projects")
            if team_size == "small_team":
                reasons.append("Team collaboration requires more structure")
            if maturity == "mvp":
                reasons.append("MVP phase - establish good practices")

        elif intensity == "comprehensive":
            reasons.append("Strong foundation for production systems")
            if maturity in ["production", "legacy"]:
                reasons.append("Production system needs robust practices")
            if team_size == "large_org":
                reasons.append("Large team requires comprehensive standards")

        else:  # maximum
            reasons.append("Maximum quality and rigor")
            if philosophy == "quality_first":
                reasons.append("Quality-first philosophy demands excellence")

        return " - ".join(reasons)

    def recommend_precommit_hooks(self, team_size: str, has_ci: bool) -> List[str]:
        """
        Recommend pre-commit hooks based on team size and CI.

        Args:
            team_size: "solo", "small_team", "large_org"
            has_ci: Whether CI/CD is configured

        Returns:
            List of recommended hook IDs
        """
        hooks = []

        # Everyone needs formatting and secrets detection
        hooks.extend(["format", "secrets"])

        # Teams need linting
        if team_size in ["small_team", "large_org"]:
            hooks.append("lint")

        # Large teams need type checking
        if team_size == "large_org":
            hooks.append("type-check")

        # If no CI, add testing to pre-commit
        if not has_ci and team_size != "solo":
            hooks.append("test")

        return hooks

    def recommend_git_workflow(
        self, team_size: str, maturity: str, has_ci: bool
    ) -> Dict:
        """
        Recommend git workflow based on context.

        Args:
            team_size: "solo", "small_team", "large_org"
            maturity: "prototype", "mvp", "production", "legacy"
            has_ci: Whether CI/CD is configured

        Returns:
            Dict with workflow, reason, alternatives
        """
        # Solo developer: Keep it simple
        if team_size == "solo":
            return {
                "workflow": "main_only",
                "reason": "Simple and fast - no overhead",
                "alternatives": {
                    "github_flow": "If you want feature branches",
                },
            }

        # Small team: GitHub Flow
        if team_size == "small_team":
            if has_ci:
                return {
                    "workflow": "github_flow",
                    "reason": "Feature branches + PRs with CI checks",
                    "alternatives": {
                        "main_only": "Less overhead but less safe",
                        "git_flow": "If you need release branches",
                    },
                }
            else:
                return {
                    "workflow": "main_only",
                    "reason": "Simple workflow - upgrade to GitHub Flow when you add CI",
                    "alternatives": {
                        "github_flow": "Better with CI/CD",
                    },
                }

        # Large organization: Git Flow or Trunk-Based
        if team_size == "large_org":
            if maturity in ["production", "legacy"]:
                return {
                    "workflow": "git_flow",
                    "reason": "Structured releases with develop/release branches",
                    "alternatives": {
                        "trunk_based": "If you have mature CI/CD and test automation",
                    },
                }
            else:
                return {
                    "workflow": "github_flow",
                    "reason": "Flexible for growing teams",
                    "alternatives": {
                        "git_flow": "When you need formal release process",
                    },
                }

        # Default
        return {
            "workflow": "github_flow",
            "reason": "Balanced workflow for most teams",
            "alternatives": {},
        }

    def recommend_testing_approach(
        self, team_size: str, maturity: str, philosophy: str
    ) -> Dict:
        """
        Recommend testing approach based on context.

        Args:
            team_size: "solo", "small_team", "large_org"
            maturity: "prototype", "mvp", "production", "legacy"
            philosophy: "move_fast", "balanced", "quality_first"

        Returns:
            Dict with approach, coverage_target, reason
        """
        # Prototype + move fast = minimal testing
        if maturity == "prototype" and philosophy == "move_fast":
            return {
                "approach": "critical_paths",
                "coverage_target": "30-50%",
                "reason": "Test critical paths only - iterate fast",
            }

        # Production + quality first = comprehensive testing
        if maturity in ["production", "legacy"] and philosophy == "quality_first":
            return {
                "approach": "comprehensive",
                "coverage_target": "90%+",
                "reason": "Production system with quality focus demands high coverage",
            }

        # Large org = balanced testing required
        if team_size == "large_org":
            return {
                "approach": "balanced",
                "coverage_target": "80%",
                "reason": "Large teams need reliable test coverage",
            }

        # MVP or small team = balanced approach
        if maturity in ["mvp", "production"] or team_size == "small_team":
            return {
                "approach": "balanced",
                "coverage_target": "70-80%",
                "reason": "Balanced testing for sustainable development",
            }

        # Default: critical paths
        return {
            "approach": "critical_paths",
            "coverage_target": "50-70%",
            "reason": "Focus on critical functionality",
        }

    def get_team_specific_note(self, option: Option, context: AnswerContext) -> str:
        """
        Get team-specific note for an option.

        Args:
            option: Option object
            context: Current answer context

        Returns:
            Team-specific note or empty string
        """
        if not context.has_answer("team_dynamics"):
            return ""

        team_size = context.team_size

        # Check if option has recommended_for tags
        if not hasattr(option, "recommended_for") or not option.recommended_for:
            return ""

        # Check if this option is recommended for this team size
        if team_size in option.recommended_for:
            return f"✓ Perfect for {self._humanize_team_size(team_size)}"

        # Check if this option is recommended for a different team size
        if "solo" in option.recommended_for and team_size != "solo":
            return "⚠️ Designed for solo developers - may be too simple for teams"

        if "large_org" in option.recommended_for and team_size == "solo":
            return "⚠️ Overhead may be too high for solo projects"

        if "small_team" in option.recommended_for and team_size == "large_org":
            return "⚠️ May not scale to large organizations"

        return ""

    def _humanize_team_size(self, team_size: str) -> str:
        """Convert team_size ID to human-readable form"""
        mapping = {
            "solo": "solo developers",
            "small_team": "small teams (2-10 people)",
            "large_org": "large organizations (10+ people)",
        }
        return mapping.get(team_size, team_size)

    def get_maturity_specific_note(
        self, option: Option, context: AnswerContext
    ) -> str:
        """Get maturity-specific note for an option"""
        if not context.has_answer("project_maturity"):
            return ""

        maturity = context.maturity

        if not hasattr(option, "recommended_for") or not option.recommended_for:
            return ""

        # Check maturity recommendations
        if maturity in option.recommended_for:
            return f"✓ Suitable for {maturity} projects"

        if "prototype" in option.recommended_for and maturity in [
            "production",
            "legacy",
        ]:
            return "⚠️ May be too lightweight for production systems"

        if "production" in option.recommended_for and maturity == "prototype":
            return "⚠️ May be overkill for prototypes"

        return ""

    def get_philosophy_specific_note(
        self, option: Option, context: AnswerContext
    ) -> str:
        """Get philosophy-specific note for an option"""
        if not context.has_answer("development_philosophy"):
            return ""

        philosophy = context.philosophy

        if not hasattr(option, "recommended_for") or not option.recommended_for:
            return ""

        # Check philosophy recommendations
        if philosophy in option.recommended_for:
            philosophy_map = {
                "move_fast": "fast iteration",
                "balanced": "balanced development",
                "quality_first": "quality-first approach",
            }
            return f"✓ Aligned with {philosophy_map.get(philosophy, philosophy)}"

        return ""

    def calculate_recommendation_score(
        self, option: Option, context: AnswerContext
    ) -> int:
        """
        Calculate recommendation score for an option (0-100).

        Args:
            option: Option to score
            context: Current answer context

        Returns:
            Score from 0 (not recommended) to 100 (highly recommended)
        """
        score = 50  # Base score

        if not hasattr(option, "recommended_for") or not option.recommended_for:
            return score

        # Check team size match (+30 points)
        if context.has_answer("team_dynamics"):
            if context.team_size in option.recommended_for:
                score += 30

        # Check maturity match (+20 points)
        if context.has_answer("project_maturity"):
            if context.maturity in option.recommended_for:
                score += 20

        # Check philosophy match (+15 points)
        if context.has_answer("development_philosophy"):
            if context.philosophy in option.recommended_for:
                score += 15

        # Check CI/CD match (+10 points)
        if "has_ci" in option.recommended_for and context.system.has_ci:
            score += 10

        # Check git match (+5 points)
        if "has_git" in option.recommended_for and context.system.is_git_repo:
            score += 5

        return min(100, score)

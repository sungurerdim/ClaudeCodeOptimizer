"""
UI Adapter for Claude Code Integration

Provides rich interactive UI when running in Claude Code context,
with automatic fallback to basic terminal prompts.

Pattern from CCO P0.8: Context-aware UI adaptation
"""

import os
from typing import Any, Dict, List, Literal, Optional

from .models import AnswerContext, DecisionPoint, Option


class ClaudeCodeUIAdapter:
    """Adapter for Claude Code AskUserQuestion tool"""

    def __init__(self, mode: Optional[Literal["terminal", "claude_code"]] = None):
        """
        Initialize UI adapter.

        Args:
            mode: Force specific mode (None = auto-detect)
        """
        if mode is None:
            # Auto-detect if running in Claude Code
            mode = self._detect_claude_code_context()

        self.mode = mode

    def _detect_claude_code_context(self) -> Literal["terminal", "claude_code"]:
        """
        Detect if running in Claude Code context.

        Returns:
            "claude_code" if in Claude Code, else "terminal"
        """
        # Claude Code sets specific environment variables
        # Check for common indicators
        indicators = [
            os.getenv("CLAUDE_CODE") == "1",
            os.getenv("ANTHROPIC_CLI") is not None,
            os.getenv("CLAUDE_SESSION") is not None,
        ]

        if any(indicators):
            return "claude_code"

        return "terminal"

    def ask_decision(
        self, decision: DecisionPoint, context: AnswerContext
    ) -> Any:
        """
        Ask user with context-aware UI.

        Args:
            decision: DecisionPoint to present
            context: Current answer context

        Returns:
            User's answer (str or List[str] for multi-select)
        """
        if self.mode == "claude_code":
            return self._ask_via_claude_tool(decision, context)
        else:
            return self._ask_via_terminal(decision, context)

    def _ask_via_claude_tool(
        self, decision: DecisionPoint, context: AnswerContext
    ) -> Any:
        """
        Use AskUserQuestion tool with rich formatting.

        Args:
            decision: DecisionPoint to present
            context: Current answer context

        Returns:
            User's answer
        """
        # Build question data structure for AskUserQuestion tool
        question_data = {
            "question": decision.question,
            "header": self._format_header(decision, context),
            "options": self._build_rich_options(decision, context),
            "multiSelect": decision.multi_select,
        }

        # In real implementation, this would call the AskUserQuestion tool
        # For now, we simulate with terminal fallback
        # The actual tool call would be made by Claude Code itself
        print("\n[Claude Code UI Adapter]")
        print(f"Question: {question_data['question']}")
        print(f"Header: {question_data['header']}")
        print(f"Multi-Select: {question_data['multiSelect']}")
        print("\nOptions:")
        for i, opt in enumerate(question_data["options"], 1):
            print(f"{i}. {opt['label']}")
            print(f"   {opt['description']}")

        # This is a placeholder - in actual use, Claude Code would handle this
        return self._ask_via_terminal(decision, context)

    def _ask_via_terminal(
        self, decision: DecisionPoint, context: AnswerContext
    ) -> Any:
        """
        Fallback to basic terminal UI.

        Args:
            decision: DecisionPoint to present
            context: Current answer context

        Returns:
            User's answer
        """
        print(f"\n{decision.question}")

        # Show AI hint if available
        ai_hint = decision.get_ai_hint(context)
        if ai_hint:
            print(f"\n💡 AI Suggestion: {ai_hint}")

        # Show options with context awareness
        for i, opt in enumerate(decision.options, 1):
            is_recommended = self._is_recommended_for_context(opt, context)
            marker = "⭐" if is_recommended else "  "
            print(f"{marker} {i}. {opt.label}")
            print(f"      {opt.description}")

            # Show trade-offs if available
            if hasattr(opt, "trade_offs") and opt.trade_offs:
                print(f"      ⚖️  {opt.trade_offs}")

            # Show team-specific note
            team_note = self._get_team_specific_note(opt, context)
            if team_note:
                print(f"      👥 {team_note}")

        # Get user input
        if decision.multi_select:
            print(
                "\nEnter selections (comma-separated, e.g., '1,3,4') or press Enter for recommended:"
            )
        else:
            print("\nEnter selection (1-{}) or press Enter for recommended:".format(
                len(decision.options)
            ))

        while True:
            user_input = input("> ").strip()

            # Empty input = use recommended
            if not user_input:
                recommended = decision.get_recommended_option(context)
                if recommended:
                    return recommended

            try:
                if decision.multi_select:
                    # Parse comma-separated indices
                    indices = [int(x.strip()) - 1 for x in user_input.split(",")]
                    selected = [
                        decision.options[i].value
                        for i in indices
                        if 0 <= i < len(decision.options)
                    ]
                    if selected and decision.validate_answer(selected):
                        return selected
                else:
                    # Single selection
                    index = int(user_input) - 1
                    if 0 <= index < len(decision.options):
                        answer = decision.options[index].value
                        if decision.validate_answer(answer):
                            return answer
            except (ValueError, IndexError):
                pass

            print("Invalid selection. Please try again.")

    def _format_header(self, decision: DecisionPoint, context: AnswerContext) -> str:
        """
        Format header for rich UI.

        Args:
            decision: DecisionPoint
            context: Current answer context

        Returns:
            Header string (max 12 chars)
        """
        # Use category as header, truncate if needed
        header = decision.category.replace("_", " ").title()
        if len(header) > 12:
            header = header[:12]
        return header

    def _build_rich_options(
        self, decision: DecisionPoint, context: AnswerContext
    ) -> List[Dict[str, str]]:
        """
        Build options with context-aware descriptions.

        Args:
            decision: DecisionPoint
            context: Current answer context

        Returns:
            List of option dicts with label and description
        """
        options = []
        for opt in decision.options:
            is_recommended = self._is_recommended_for_context(opt, context)
            description = self._build_context_description(
                opt, context, is_recommended
            )

            label = opt.label
            if is_recommended:
                label = f"{label} ⭐"

            options.append({"label": label, "description": description})

        return options

    def _build_context_description(
        self, option: Option, context: AnswerContext, is_recommended: bool
    ) -> str:
        """
        Build rich description with team-specific notes.

        Args:
            option: Option object
            context: Current answer context
            is_recommended: Whether option is recommended for context

        Returns:
            Rich description string
        """
        parts = [option.description]

        # Add recommendation reason
        if is_recommended:
            reason = self._get_recommendation_reason(option, context)
            if reason:
                parts.append(f"✓ {reason}")

        # Add trade-offs
        if hasattr(option, "trade_offs") and option.trade_offs:
            parts.append(f"⚖️ {option.trade_offs}")

        # Add team-specific note
        team_note = self._get_team_specific_note(option, context)
        if team_note:
            parts.append(f"👥 {team_note}")

        # Add time investment if available
        if hasattr(option, "time_investment") and option.time_investment:
            parts.append(f"⏱️ {option.time_investment}")

        # Add effects if available
        if hasattr(option, "effects") and option.effects:
            parts.append(f"📋 {option.effects}")

        return "\n".join(parts)

    def _is_recommended_for_context(
        self, option: Option, context: AnswerContext
    ) -> bool:
        """
        Check if option is recommended for current context.

        Args:
            option: Option to check
            context: Current answer context

        Returns:
            True if recommended
        """
        if not hasattr(option, "recommended_for") or not option.recommended_for:
            return False

        # Check if any recommended_for tags match current context
        context_tags = self._get_context_tags(context)
        return bool(set(option.recommended_for) & context_tags)

    def _get_context_tags(self, context: AnswerContext) -> set:
        """
        Get context tags from current answers.

        Args:
            context: Current answer context

        Returns:
            Set of context tags
        """
        tags = set()

        # Add team size tag
        if context.has_answer("team_dynamics"):
            tags.add(context.team_size)

        # Add maturity tag
        if context.has_answer("project_maturity"):
            tags.add(context.maturity)

        # Add philosophy tag
        if context.has_answer("development_philosophy"):
            tags.add(context.philosophy)

        # Add project type tags
        if context.has_answer("project_purpose"):
            project_types = context.project_types
            if isinstance(project_types, list):
                tags.update(project_types)
            else:
                tags.add(project_types)

        # Add CI/CD tag if detected
        if context.system.has_ci:
            tags.add("has_ci")

        # Add git tag if detected
        if context.system.is_git_repo:
            tags.add("has_git")

        return tags

    def _get_recommendation_reason(
        self, option: Option, context: AnswerContext
    ) -> str:
        """
        Get reason why option is recommended.

        Args:
            option: Recommended option
            context: Current answer context

        Returns:
            Reason string
        """
        if not hasattr(option, "recommended_for") or not option.recommended_for:
            return ""

        # Match recommendation to context
        if "solo" in option.recommended_for and context.team_size == "solo":
            return "Ideal for solo developers"
        if "small_team" in option.recommended_for and context.team_size == "small_team":
            return "Perfect for small teams"
        if "large_org" in option.recommended_for and context.team_size == "large_org":
            return "Recommended for large organizations"

        if "prototype" in option.recommended_for and context.maturity == "prototype":
            return "Good for prototypes"
        if "production" in option.recommended_for and context.maturity == "production":
            return "Production-ready choice"

        if "has_ci" in option.recommended_for and context.system.has_ci:
            return "Integrates with your CI/CD"

        return "Recommended for your project"

    def _get_team_specific_note(self, option: Option, context: AnswerContext) -> str:
        """
        Get team-specific note for option.

        Args:
            option: Option object
            context: Current answer context

        Returns:
            Team-specific note or empty string
        """
        team_size = context.team_size if context.has_answer("team_dynamics") else None

        if not team_size:
            return ""

        # Check if this option might be overkill or too minimal
        if team_size == "solo":
            if hasattr(option, "recommended_for") and "large_org" in option.recommended_for:
                return "May be overkill for solo projects"

        if team_size == "large_org":
            if hasattr(option, "recommended_for") and "solo" in option.recommended_for:
                return "Consider more robust alternatives for large teams"

        return ""

    def show_progress(self, current: int, total: int, message: str) -> None:
        """
        Show progress indicator.

        Args:
            current: Current step number
            total: Total number of steps
            message: Progress message
        """
        if self.mode == "claude_code":
            # In Claude Code, use rich UI
            percentage = int((current / total) * 100)
            bar_length = 20
            filled = int((current / total) * bar_length)
            bar = "█" * filled + "░" * (bar_length - filled)
            print(f"\n[{bar}] {percentage}% - {message}")
        else:
            # Terminal: simple counter
            print(f"\n[{current}/{total}] {message}")

    def show_summary(self, context: AnswerContext) -> None:
        """
        Show summary of selected options.

        Args:
            context: Final answer context
        """
        print("\n" + "=" * 60)
        print("Configuration Summary")
        print("=" * 60)

        for key, value in context.answers.items():
            # Format key
            formatted_key = key.replace("_", " ").title()

            # Format value
            if isinstance(value, list):
                formatted_value = ", ".join(str(v) for v in value)
            else:
                formatted_value = str(value)

            print(f"{formatted_key:30} : {formatted_value}")

        print("=" * 60)

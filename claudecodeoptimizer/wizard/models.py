"""
Core Models for CCO Wizard Decision Tree

Defines the structure for hierarchical decision-making process.
Both Interactive and Quick modes use the same decision tree.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, List, Literal, Optional


@dataclass
class Option:
    """
    A single option within a decision point.

    Used in both Interactive mode (displayed to user) and Quick mode (AI selects).
    """

    value: str  # Internal value (e.g., "solo", "small_team")
    label: str  # Display label for user (e.g., "Solo Developer")
    description: str  # Detailed explanation
    recommended_for: List[str] = field(default_factory=list)  # Context tags
    effects: str = ""  # What happens if selected
    time_investment: str = ""  # Optional: time/effort indication
    trade_offs: str = ""  # Optional: pros/cons

    def __post_init__(self):
        """Validate option data"""
        if not self.value or not self.label:
            raise ValueError("Option must have value and label")


@dataclass
class DecisionPoint:
    """
    A single decision point in the wizard flow.

    Works identically in both Interactive and Quick modes:
    - Interactive: Ask user with options
    - Quick: Use auto_strategy to decide

    Decisions are organized in tiers (0-4) for logical ordering.
    """

    id: str  # Unique ID (e.g., "project_purpose")
    tier: int  # 0=system, 1=fundamental, 2=strategy, 3=tactical, 4=system-specific
    category: str  # Grouping (e.g., "project_identity")
    question: str  # Question to ask user (Interactive mode)
    options: List[Option]  # Available choices
    multi_select: bool = False  # Allow multiple selections?

    # AI decision strategy for Quick mode
    auto_strategy: Optional[Callable[[Any], Any]] = None

    # Contextual help
    why_this_question: str = ""  # Why we're asking this
    ai_hint_generator: Optional[Callable[[Any], str]] = None  # Context-aware hint

    # Conditional logic
    skip_if: Optional[Callable[[Dict[str, Any]], bool]] = None  # Skip question if...
    required_for: List[str] = field(default_factory=list)  # Required for these features

    # Validation
    validator: Optional[Callable[[Any], bool]] = None

    def should_ask(self, context: Dict[str, Any]) -> bool:
        """Check if this question should be asked given current context"""
        if self.skip_if:
            return not self.skip_if(context)
        return True

    def get_ai_hint(self, context: Any) -> str:
        """Get contextual AI hint based on previous answers"""
        if self.ai_hint_generator:
            return self.ai_hint_generator(context)
        return ""

    def get_recommended_option(self, context: Any) -> Optional[str]:
        """Get AI-recommended option value based on context"""
        if self.auto_strategy:
            result = self.auto_strategy(context)
            if isinstance(result, list):
                return result  # Multi-select
            return result
        return None

    def validate_answer(self, answer: Any) -> bool:
        """Validate user/AI answer"""
        if self.validator:
            return self.validator(answer)

        # Default validation
        if self.multi_select:
            if not isinstance(answer, list):
                return False
            return all(
                any(opt.value == val for opt in self.options) for val in answer
            )
        else:
            return any(opt.value == answer for opt in self.options)


@dataclass
class SystemContext:
    """
    Automatically detected system information (TIER 0).

    This information is detected silently and influences all decisions.
    Both modes use identical detection.
    """

    # Operating System
    os_type: Literal["windows", "macos", "linux"]
    os_version: str
    os_platform: str  # win32, darwin, linux

    # Terminal Environment
    shell_type: str  # powershell, bash, zsh, fish, cmd
    terminal_emulator: str  # windows-terminal, iterm2, gnome-terminal, etc.
    color_support: bool
    unicode_support: bool

    # Locale & Language
    system_locale: str  # en_US, tr_TR
    detected_language: str  # en, tr
    encoding: str  # utf-8, cp1252

    # Development Environment
    python_version: str
    python_executable: str
    pip_version: str
    git_installed: bool
    git_user_name: Optional[str] = None
    git_user_email: Optional[str] = None

    # Editor/IDE Detection
    detected_editors: List[str] = field(default_factory=list)
    active_editor: Optional[str] = None  # From $EDITOR or process

    # Project Context (from UniversalDetector)
    project_root: Path = Path.cwd()
    is_git_repo: bool = False
    existing_tools: List[str] = field(default_factory=list)
    file_count: int = 0
    line_count: int = 0
    has_tests: bool = False
    has_ci: bool = False
    detected_languages: List[str] = field(default_factory=list)
    detected_frameworks: List[str] = field(default_factory=list)
    detected_project_types: List[str] = field(default_factory=list)

    def get_shell_syntax(self) -> Literal["powershell", "bash"]:
        """Get appropriate shell syntax for commands"""
        if self.os_type == "windows":
            return "powershell"
        return "bash"

    def get_path_separator(self) -> str:
        """Get OS-appropriate path separator"""
        return "\\" if self.os_type == "windows" else "/"

    def supports_unicode(self) -> bool:
        """Check if terminal supports unicode characters"""
        return self.unicode_support and self.encoding.lower() == "utf-8"

    def get_progress_chars(self) -> Dict[str, str]:
        """Get appropriate progress/status characters"""
        if self.supports_unicode():
            return {
                "check": "✓",
                "cross": "✗",
                "arrow": "→",
                "bullet": "•",
                "progress": "█▓▒░",
            }
        else:
            return {
                "check": "[OK]",
                "cross": "[X]",
                "arrow": "->",
                "bullet": "*",
                "progress": "####",
            }


@dataclass
class AnswerContext:
    """
    Accumulated answers from all decision points.

    Used for cascading AI recommendations and conditional logic.
    """

    system: SystemContext
    answers: Dict[str, Any] = field(default_factory=dict)

    # Convenience accessors for common paths
    @property
    def project_types(self) -> List[str]:
        return self.answers.get("project_purpose", [])

    @property
    def team_size(self) -> str:
        return self.answers.get("team_dynamics", "solo")

    @property
    def maturity(self) -> str:
        return self.answers.get("project_maturity", "prototype")

    @property
    def philosophy(self) -> str:
        return self.answers.get("development_philosophy", "balanced")

    @property
    def principle_strategy(self) -> str:
        return self.answers.get("principle_strategy", "recommended")

    @property
    def testing_approach(self) -> str:
        return self.answers.get("testing_approach", "no_tests")

    @property
    def security_stance(self) -> str:
        return self.answers.get("security_stance", "standard")

    @property
    def documentation_level(self) -> str:
        return self.answers.get("documentation_level", "minimal")

    @property
    def git_workflow(self) -> str:
        return self.answers.get("git_workflow", "main_only")

    def get(self, key: str, default: Any = None) -> Any:
        """Get answer by key with default"""
        return self.answers.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Set answer"""
        self.answers[key] = value

    def has_answer(self, key: str) -> bool:
        """Check if answer exists"""
        return key in self.answers


@dataclass
class WizardResult:
    """
    Final result of wizard execution.

    Contains all decisions, selected principles, and commands.
    """

    success: bool
    mode: Literal["interactive", "quick"]
    system_context: SystemContext
    answers: Dict[str, Any]
    selected_principles: List[str] = field(default_factory=list)
    selected_commands: List[str] = field(default_factory=list)
    skipped_questions: List[str] = field(default_factory=list)
    duration_seconds: float = 0.0
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "success": self.success,
            "mode": self.mode,
            "answers": self.answers,
            "selected_principles": self.selected_principles,
            "selected_commands": self.selected_commands,
            "skipped_questions": self.skipped_questions,
            "duration_seconds": self.duration_seconds,
            "error": self.error,
        }


@dataclass
class ToolComparison:
    """
    Comparison between competing tools (e.g., ruff vs black).

    Used in TIER 3 tactical decisions when multiple tools detected.
    """

    category: str  # e.g., "formatter", "linter", "test_framework"
    tools: List[str]  # Detected tools in this category
    recommended: str  # Recommended tool
    reason: str  # Why this tool is recommended
    alternatives: Dict[str, str] = field(
        default_factory=dict
    )  # Other options with reasons


# Type aliases for clarity
DecisionValue = Any  # str | List[str] | int | bool
AutoStrategy = Callable[[AnswerContext], DecisionValue]
AIHintGenerator = Callable[[AnswerContext], str]
SkipCondition = Callable[[Dict[str, Any]], bool]
Validator = Callable[[DecisionValue], bool]

"""
Constants for ClaudeCodeOptimizer.

Centralized location for all magic numbers and configuration values.
Follows U_DRY (DRY Enforcement) - single source of truth.
"""

# File Permissions
EXECUTABLE_PERMISSION = 0o755  # Unix executable file permission

# Pagination
DEFAULT_PAGE_SIZE = 15  # Default number of items per page in wizard

# Thresholds
SERVICE_COUNT_THRESHOLD_MEDIUM = 2  # Threshold for medium-sized service architecture
SERVICE_COUNT_THRESHOLD_LARGE = 3  # Threshold for large-sized service architecture

# Display Limits (U_DRY - DRY Enforcement)
TOP_ITEMS_DISPLAY = {
    "languages": 10,
    "frameworks": 10,
    "tools": 15,
    "project_types": 3,
    "principles": 15,
    "commands": 10,
}

# Confidence Scores
MIN_CONFIDENCE_THRESHOLD = 0.5  # Minimum confidence for auto-selection
HIGH_CONFIDENCE_THRESHOLD = 0.8  # High confidence threshold
CONFIDENCE_SCALE = 100  # Scale for converting 0-1 confidence to 0-100 percentage

# Git
DEFAULT_BRANCH_NAMES = ["main", "master", "develop"]  # Common default branch names

# Coverage
MINIMAL_TEST_COVERAGE_TARGET = 50  # Minimal test coverage for projects without tests
DEFAULT_TEST_COVERAGE_TARGET = 80  # Default test coverage percentage target
HIGH_TEST_COVERAGE_TARGET = 90  # High test coverage percentage target

# Timeouts (seconds)
DEFAULT_COMMAND_TIMEOUT = 300  # 5 minutes default timeout for commands
SHORT_COMMAND_TIMEOUT = 60  # 1 minute for quick operations

# Retention
SESSION_RETENTION_DAYS = 90  # Days to keep session history
MAX_AUDIT_HISTORY = 100  # Maximum number of audit history entries to keep

# Validation
MAX_PRINCIPLE_NAME_LENGTH = 100  # Maximum length for principle names
MAX_COMMAND_NAME_LENGTH = 50  # Maximum length for command names

# Display
MAX_DISPLAY_LINES = 50  # Maximum lines to display in output before truncating
DEFAULT_TERMINAL_WIDTH = 80  # Default terminal width for formatting
SEPARATOR_WIDTH = 80  # Width of separator lines in console output (standardized to 80)

# Detection Confidence Thresholds (U_DRY - DRY Enforcement)
DETECTION_CONFIDENCE_LOW = 0.3  # Low confidence threshold for detection
DETECTION_CONFIDENCE_MEDIUM = 0.4  # Medium confidence threshold
DETECTION_CONFIDENCE_STANDARD = 0.5  # Standard confidence threshold
DETECTION_CONFIDENCE_HIGH = 0.6  # High confidence threshold
DETECTION_CONFIDENCE_VERY_HIGH = 0.8  # Very high confidence threshold

# Detection Sampling
CONTENT_SAMPLE_LIMIT = 20  # Maximum files to sample for content detection
PATTERN_MATCH_LIMIT = 10  # Maximum pattern matches to collect

# Command Parsing
MARKDOWN_SECTION_COUNT = 3  # Expected sections in command markdown (metadata, description, content)
MIN_CLI_ARGS = 2  # Minimum CLI arguments required

# Coverage Requirements
MIN_COVERAGE_PERCENTAGE = 90  # Minimum acceptable coverage percentage

# History and State Management
AUDIT_TREND_WINDOW = 10  # Number of audit entries to analyze for trends
AUDIT_RECENT_COUNT = 5  # Number of recent audits for trend calculation

# Codebase Size Thresholds
SMALL_CODEBASE_THRESHOLD = 100  # Files count for small codebase
MEDIUM_CODEBASE_THRESHOLD = 500  # Files count for medium codebase
LARGE_CODEBASE_THRESHOLD = 1000  # Files count for large/enterprise codebase

# UI Configuration
UI_HEADING_LEVEL_SECONDARY = 2  # Secondary heading level in UI

# Wizard Configuration
EXPECTED_WIZARD_QUESTIONS = 58  # Expected total questions in wizard validation

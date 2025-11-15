"""Project analyzer for ClaudeCodeOptimizer."""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

# Import Universal Detector for comprehensive analysis
from ..ai.detection import ProjectAnalysisReport, UniversalDetector
from .constants import (
    DETECTION_CONFIDENCE_HIGH,
    DETECTION_CONFIDENCE_VERY_HIGH,
    TOP_ITEMS_DISPLAY,
)
from .utils import format_confidence

# Framework Hierarchy: Maps parent frameworks to their sub-dependencies
# If parent is detected, children are filtered out to avoid clutter
FRAMEWORK_HIERARCHY = {
    # Python
    "fastapi": ["starlette"],  # FastAPI uses Starlette internally
    "django": ["django-rest-framework"],  # Optional: DRF extends Django
    # JavaScript/TypeScript
    "next": ["react"],  # Next.js uses React
    "nuxt": ["vue"],  # Nuxt uses Vue
    "express": ["connect"],  # Express uses Connect middleware
    "nestjs": ["express", "fastapi"],  # NestJS can use Express or Fastify
    # Others can be added as needed
}


class ProjectAnalyzer:
    """Analyzes projects to detect language, framework, and structure."""

    def __init__(self, project_root: Path) -> None:
        self.project_root = project_root
        self.universal_detector = UniversalDetector(str(project_root))

    def analyze(self) -> Dict[str, Any]:
        """
        Perform comprehensive project analysis using Universal Detector.

        This provides detailed analysis including:
        - Multi-language detection with confidence scores
        - Framework detection with evidence
        - Tool detection (Docker, CI/CD, linters, etc.)
        - Project type classification
        - Codebase patterns and metrics
        - Statistical analysis

        Returns:
            Comprehensive analysis results
        """
        # Run Universal Detector for comprehensive analysis
        detection_report = self.universal_detector.analyze()

        # Build enhanced analysis
        analysis = {
            # Core detection results
            "languages": self._process_languages(detection_report),
            "frameworks": self._process_frameworks(detection_report),
            "tools": self._process_tools(detection_report),
            "project_types": self._process_project_types(detection_report),
            # Enhanced analysis
            "primary_language": self._get_primary_language(detection_report),
            "primary_framework": self._get_primary_framework(detection_report),
            "primary_type": self._get_primary_type(detection_report),
            # Structural analysis
            "structure": self._analyze_structure(),
            "codebase_patterns": detection_report.codebase_patterns,
            "statistics": self._generate_statistics(detection_report),
            # Dependencies
            "dependencies": self._detect_dependencies(),
            # Feature flags
            "has_tests": detection_report.codebase_patterns.get("has_tests", False),
            "has_docker": detection_report.codebase_patterns.get("has_docker", False),
            "has_ci_cd": detection_report.codebase_patterns.get("has_ci_cd", False),
            "has_git": self._has_git(),
            # Recommendations
            "commands": self._recommend_commands(detection_report),
            "suggestions": self._generate_suggestions(detection_report),
            # Metadata
            "analysis_duration_ms": detection_report.analysis_duration_ms,
            "analyzed_at": detection_report.analyzed_at,
            "confidence_level": self._calculate_confidence(detection_report),
        }

        return analysis

    def _process_languages(self, report: ProjectAnalysisReport) -> List[Dict[str, Any]]:
        """Process language detection results."""
        return [
            {
                "name": lang.detected_value,
                "confidence": format_confidence(lang.confidence, 1),
                "evidence": lang.evidence,
            }
            for lang in report.languages
        ]

    def _process_frameworks(self, report: ProjectAnalysisReport) -> List[Dict[str, Any]]:
        """
        Process framework detection results.

        Filters out sub-dependencies based on FRAMEWORK_HIERARCHY.
        For example, if FastAPI is detected, Starlette is hidden.
        """
        # First, collect all detected frameworks
        all_frameworks = [
            {
                "name": fw.detected_value,
                "confidence": format_confidence(fw.confidence, 1),
                "evidence": fw.evidence,
            }
            for fw in report.frameworks
        ]

        # Extract framework names for hierarchy check
        detected_names = {str(fw["name"]).lower() for fw in all_frameworks}

        # Filter out sub-dependencies
        filtered_frameworks = []
        for fw in all_frameworks:
            fw_name = str(fw["name"]).lower()

            # Check if this framework is a child of any detected parent
            is_child = False
            for parent, children in FRAMEWORK_HIERARCHY.items():
                if parent in detected_names and fw_name in [c.lower() for c in children]:
                    is_child = True
                    break

            # Only include if not a child dependency
            if not is_child:
                filtered_frameworks.append(fw)

        return filtered_frameworks

    def _process_tools(self, report: ProjectAnalysisReport) -> List[Dict[str, Any]]:
        """Process tool detection results."""
        return [
            {
                "name": tool.detected_value,
                "confidence": format_confidence(tool.confidence, 1),
                "evidence": tool.evidence,
            }
            for tool in report.tools
        ]

    def _process_project_types(self, report: ProjectAnalysisReport) -> List[Dict[str, Any]]:
        """Process project type detection results."""
        return [
            {
                "type": ptype.detected_value,
                "confidence": format_confidence(ptype.confidence, 1),
                "evidence": ptype.evidence,
            }
            for ptype in report.project_types
        ]

    def _get_primary_language(self, report: ProjectAnalysisReport) -> Optional[str]:
        """Get primary language (highest confidence)."""
        if report.languages:
            return report.languages[0].detected_value
        return None

    def _get_primary_framework(self, report: ProjectAnalysisReport) -> Optional[str]:
        """Get primary framework (highest confidence)."""
        if report.frameworks:
            return report.frameworks[0].detected_value
        return None

    def _get_primary_type(self, report: ProjectAnalysisReport) -> Optional[str]:
        """Get primary project type (highest confidence)."""
        if report.project_types:
            return report.project_types[0].detected_value
        return None

    def _generate_statistics(self, report: ProjectAnalysisReport) -> Dict[str, Any]:
        """Generate statistical analysis."""
        patterns = report.codebase_patterns

        return {
            "total_files": patterns.get("total_files", 0),
            "source_files": patterns.get("source_files_count", 0),
            "config_files": patterns.get("config_files_count", 0),
            "extension_distribution": patterns.get("extension_distribution", {}),
            "languages_count": len(report.languages),
            "frameworks_count": len(report.frameworks),
            "tools_count": len(report.tools),
        }

    def _calculate_confidence(self, report: ProjectAnalysisReport) -> str:
        """Calculate overall confidence level of analysis."""
        # Calculate average confidence across all detections
        all_confidences = []

        for lang in report.languages[: TOP_ITEMS_DISPLAY["languages"]]:
            all_confidences.append(lang.confidence)
        for fw in report.frameworks[: TOP_ITEMS_DISPLAY["frameworks"]]:
            all_confidences.append(fw.confidence)
        for tool in report.tools[: TOP_ITEMS_DISPLAY["tools"]]:
            all_confidences.append(tool.confidence)

        if not all_confidences:
            return "low"

        avg_confidence = sum(all_confidences) / len(all_confidences)

        if avg_confidence >= DETECTION_CONFIDENCE_VERY_HIGH:
            return "high"
        elif avg_confidence >= DETECTION_CONFIDENCE_HIGH:
            return "medium"
        else:
            return "low"

    def _generate_suggestions(self, report: ProjectAnalysisReport) -> List[str]:
        """Generate intelligent suggestions based on analysis."""
        suggestions = []
        patterns = report.codebase_patterns

        # Test suggestions
        if not patterns.get("has_tests"):
            suggestions.append("Consider adding automated tests to improve code quality")

        # CI/CD suggestions
        if not patterns.get("has_ci_cd") and patterns.get("has_git"):
            suggestions.append("Set up CI/CD pipeline for automated testing and deployment")

        # Docker suggestions
        if not patterns.get("has_docker") and report.project_types:
            if any(pt.detected_value == "api" for pt in report.project_types):
                suggestions.append("Consider containerizing your API with Docker")

        # Linting suggestions
        has_linter = any(
            tool.detected_value in ["black", "ruff", "eslint", "prettier"] for tool in report.tools
        )
        if not has_linter:
            primary_lang = self._get_primary_language(report)
            if primary_lang == "python":
                suggestions.append(
                    "Add code formatters like black and ruff for consistent code style",
                )
            elif primary_lang in ["javascript", "typescript"]:
                suggestions.append("Add eslint and prettier for code quality and formatting")

        # Type checking suggestions
        has_typechecker = any(
            tool.detected_value in ["mypy", "typescript"] for tool in report.tools
        )
        if not has_typechecker:
            primary_lang = self._get_primary_language(report)
            if primary_lang == "python":
                suggestions.append("Add mypy for static type checking")

        return suggestions

    def _recommend_commands(self, report: ProjectAnalysisReport) -> List[str]:
        """Recommend CCO commands based on comprehensive analysis."""
        commands = [
            "cco-status",
            "cco-audit-code",
            "cco-fix-code",
        ]

        primary_lang = self._get_primary_language(report)
        primary_type = self._get_primary_type(report)

        # Language-specific commands
        if primary_lang == "python":
            # Check if tools are available
            has_black = any(t.detected_value == "black" for t in report.tools)
            has_ruff = any(t.detected_value == "ruff" for t in report.tools)
            has_mypy = any(t.detected_value == "mypy" for t in report.tools)

            if has_black or has_ruff:
                commands.append("cco-format")
            if has_ruff:
                commands.append("cco-lint")
            if has_mypy:
                commands.append("cco-typecheck")

        elif primary_lang in ["javascript", "typescript"]:
            has_eslint = any(t.detected_value == "eslint" for t in report.tools)
            has_prettier = any(t.detected_value == "prettier" for t in report.tools)

            if has_prettier:
                commands.append("cco-format")
            if has_eslint:
                commands.append("cco-lint")

        # Type-specific commands
        if primary_type == "api":
            commands.extend(["cco-test-api", "cco-audit-security"])

        # Test commands
        if report.codebase_patterns.get("has_tests"):
            commands.append("cco-test")

        # Docker commands
        if report.codebase_patterns.get("has_docker"):
            commands.append("cco-docker")

        # Git commands
        if report.codebase_patterns.get("has_git"):
            commands.append("cco-git")

        return list(set(commands))  # Remove duplicates

    def _analyze_structure(self) -> Dict[str, Any]:
        """Analyze project structure."""
        total_files = 0
        total_dirs = 0
        main_directories: list[str] = []
        config_files: list[str] = []

        # Count files and directories
        for item in self.project_root.rglob("*"):
            if item.is_file():
                total_files += 1
            elif item.is_dir():
                total_dirs += 1

        # Find main directories (top-level only)
        for item in self.project_root.iterdir():
            if item.is_dir() and not item.name.startswith("."):
                main_directories.append(item.name)

        # Find config files
        config_patterns = [
            "*.json",
            "*.yml",
            "*.yaml",
            "*.toml",
            "*.ini",
            ".env*",
        ]
        for pattern in config_patterns:
            for config_file in self.project_root.glob(pattern):
                if config_file.is_file():
                    config_files.append(config_file.name)

        structure = {
            "total_files": total_files,
            "total_dirs": total_dirs,
            "main_directories": main_directories,
            "config_files": config_files,
        }

        return structure

    def _detect_dependencies(self) -> Dict[str, List[str]]:
        """Detect project dependencies."""
        dependencies = {}

        # Python
        requirements_txt = self.project_root / "requirements.txt"
        if requirements_txt.exists():
            try:
                deps = requirements_txt.read_text().strip().split("\n")
                dependencies["python"] = [d.split("==")[0] for d in deps if d]
            except Exception:
                dependencies["python"] = []

        # JavaScript
        package_json = self.project_root / "package.json"
        if package_json.exists():
            try:
                data = json.loads(package_json.read_text())
                dependencies["javascript"] = list(data.get("dependencies", {}).keys())
            except Exception:
                dependencies["javascript"] = []

        return dependencies

    def _has_tests(self) -> bool:
        """Check if project has tests."""
        test_indicators = ["test", "tests", "spec", "__tests__"]

        for indicator in test_indicators:
            if list(self.project_root.rglob(f"*{indicator}*")):
                return True

        return False

    def _has_docker(self) -> bool:
        """Check if project uses Docker."""
        return (self.project_root / "Dockerfile").exists() or (
            self.project_root / "docker-compose.yml"
        ).exists()

    def _has_git(self) -> bool:
        """Check if project uses Git."""
        return (self.project_root / ".git").exists()

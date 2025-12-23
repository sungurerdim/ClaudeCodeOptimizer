"""
Test executor for CCO benchmarks.

Runs projects through ccbox (vanilla and cco modes) and collects results.

ccbox behavior:
- Mounts current working directory as project root
- --bare flag runs without CCO rules (vanilla)
- Default (no flag) runs with CCO rules (ccbox:base image)
"""

import json
import os
import subprocess
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

from .metrics import CodeAnalyzer, Metrics, calculate_overall_score, compare_metrics


@dataclass
class ExecutionResult:
    """Result of a single test execution."""

    project_id: str
    variant: str  # "cco" or "vanilla"
    success: bool
    metrics: Metrics | None
    score: float
    generation_time_seconds: float
    prompt_used: str
    error_message: str = ""
    output_dir: str = ""
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> dict[str, Any]:
        return {
            "project_id": self.project_id,
            "variant": self.variant,
            "success": self.success,
            "metrics": self.metrics.to_dict() if self.metrics else None,
            "score": self.score,
            "generation_time_seconds": self.generation_time_seconds,
            "prompt_used": self.prompt_used,
            "error_message": self.error_message,
            "output_dir": self.output_dir,
            "timestamp": self.timestamp,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "ExecutionResult":
        metrics_data = data.pop("metrics", None)
        metrics = Metrics.from_dict(metrics_data) if metrics_data else None
        return cls(metrics=metrics, **data)


@dataclass
class BenchmarkResult:
    """Full benchmark result comparing CCO vs Vanilla."""

    project_id: str
    project_name: str
    categories: list[str]
    complexity: str
    cco_result: ExecutionResult
    vanilla_result: ExecutionResult
    comparison: dict[str, Any]
    verdict: str
    score_difference: float
    prompt_used: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> dict[str, Any]:
        return {
            "project_id": self.project_id,
            "project_name": self.project_name,
            "categories": self.categories,
            "complexity": self.complexity,
            "cco_result": self.cco_result.to_dict(),
            "vanilla_result": self.vanilla_result.to_dict(),
            "comparison": self.comparison,
            "verdict": self.verdict,
            "score_difference": self.score_difference,
            "prompt_used": self.prompt_used,
            "timestamp": self.timestamp,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "BenchmarkResult":
        cco_data = data.pop("cco_result")
        vanilla_data = data.pop("vanilla_result")
        result = cls(
            cco_result=ExecutionResult.from_dict(cco_data),
            vanilla_result=ExecutionResult.from_dict(vanilla_data),
            **data,
        )
        return result


class ProjectConfig:
    """Configuration for a benchmark project."""

    def __init__(self, project_dir: Path):
        self.project_dir = project_dir
        self.prompt_file = project_dir / "PROMPT.md"
        self.spec_file = project_dir / "SPEC.md"
        self._load()

    def _load(self) -> None:
        """Load project configuration from SPEC.md."""
        self.id = self.project_dir.name
        self.name = self.id.replace("_", " ").title()
        self.categories: list[str] = []
        self.complexity = "Medium"

        if self.spec_file.exists():
            content = self.spec_file.read_text(encoding="utf-8")
            # Parse categories
            for line in content.splitlines():
                if line.startswith("- ") and ":" in line:
                    cat = line.strip("- ").strip()
                    if any(c in cat for c in [":", "::"]):
                        self.categories.append(cat)
                elif "Complexity:" in line:
                    self.complexity = line.split(":")[-1].strip()

        if self.prompt_file.exists():
            self.prompt = self.prompt_file.read_text(encoding="utf-8")
        else:
            self.prompt = ""


class TestExecutor:
    """Executes benchmark tests using ccbox.

    ccbox mounts the current working directory as project root.
    We create isolated directories for each test run and cd into them.
    """

    def __init__(self, output_base: Path, ccbox_cmd: str = "ccbox", timeout_seconds: int = 600):
        self.output_base = output_base
        self.ccbox_cmd = ccbox_cmd
        self.timeout = timeout_seconds
        self.output_base.mkdir(parents=True, exist_ok=True)

    def run_project(
        self, config: ProjectConfig, variant: str, model: str = "opus"
    ) -> ExecutionResult:
        """Run a single project variant.

        Creates an isolated directory, cd's into it, and runs ccbox.
        ccbox will mount this directory and generate code there.
        """
        # Create isolated project directory
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        project_dir = self.output_base / f"{config.id}_{variant}_{timestamp}"
        project_dir.mkdir(parents=True, exist_ok=True)

        # Save prompt for reference
        prompt_file = project_dir / "_benchmark_prompt.md"
        prompt_file.write_text(config.prompt, encoding="utf-8")

        # Build ccbox command
        cmd = [self.ccbox_cmd]

        # Project directory (ccbox -C flag)
        cmd.extend(["-C", str(project_dir)])

        # Variant-specific flags
        if variant == "vanilla":
            cmd.append("--bare")  # No CCO rules
        # else: default ccbox:base with CCO rules

        # Common flags
        cmd.extend(
            [
                "--yes",  # Non-interactive mode
                "--model",
                model,  # Model selection
                "--prompt",
                config.prompt,  # Pass prompt
            ]
        )

        start_time = time.time()

        try:
            # Run ccbox with -C pointing to project directory
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.timeout,
                env={**os.environ, "CLAUDE_MODEL": model},
                encoding="utf-8",
                errors="replace",
            )

            generation_time = time.time() - start_time
            success = result.returncode == 0

            # Save ccbox output for debugging
            (project_dir / "_ccbox_stdout.log").write_text(result.stdout, encoding="utf-8")
            (project_dir / "_ccbox_stderr.log").write_text(result.stderr, encoding="utf-8")

            # Analyze generated code (ccbox creates files in project_dir)
            # Exclude our benchmark metadata files
            analyzer = CodeAnalyzer(project_dir)
            metrics = analyzer.analyze()
            metrics.name = config.name
            metrics.variant = variant
            metrics.generation_time_seconds = generation_time
            score = calculate_overall_score(metrics)

            return ExecutionResult(
                project_id=config.id,
                variant=variant,
                success=success,
                metrics=metrics,
                score=round(score, 1),
                generation_time_seconds=round(generation_time, 2),
                prompt_used=config.prompt,
                output_dir=str(project_dir),
                error_message="" if success else result.stderr[:500],
            )

        except subprocess.TimeoutExpired:
            generation_time = time.time() - start_time
            return ExecutionResult(
                project_id=config.id,
                variant=variant,
                success=False,
                metrics=None,
                score=0.0,
                generation_time_seconds=round(generation_time, 2),
                prompt_used=config.prompt,
                output_dir=str(project_dir),
                error_message=f"Timeout after {self.timeout} seconds",
            )
        except FileNotFoundError:
            return ExecutionResult(
                project_id=config.id,
                variant=variant,
                success=False,
                metrics=None,
                score=0.0,
                generation_time_seconds=0.0,
                prompt_used=config.prompt,
                output_dir=str(project_dir),
                error_message=f"ccbox command not found: {self.ccbox_cmd}",
            )
        except Exception as e:
            generation_time = time.time() - start_time
            return ExecutionResult(
                project_id=config.id,
                variant=variant,
                success=False,
                metrics=None,
                score=0.0,
                generation_time_seconds=round(generation_time, 2),
                prompt_used=config.prompt,
                output_dir=str(project_dir),
                error_message=str(e),
            )

    def run_benchmark(self, config: ProjectConfig, model: str = "opus") -> BenchmarkResult:
        """Run full benchmark (both variants) for a project."""
        # Run vanilla first
        vanilla_result = self.run_project(config, "vanilla", model)

        # Run CCO version
        cco_result = self.run_project(config, "cco", model)

        # Compare results
        if cco_result.metrics and vanilla_result.metrics:
            comparison = compare_metrics(cco_result.metrics, vanilla_result.metrics)
        else:
            comparison = {
                "comparisons": [],
                "cco_wins": 0,
                "vanilla_wins": 0,
                "ties": 0,
                "cco_score": cco_result.score,
                "vanilla_score": vanilla_result.score,
                "score_diff": cco_result.score - vanilla_result.score,
            }

        # Determine verdict
        diff = comparison["score_diff"]
        if diff >= 15:
            verdict = "Strong CCO Advantage"
        elif diff >= 5:
            verdict = "Moderate CCO Advantage"
        elif diff >= -5:
            verdict = "Mixed Results"
        elif diff >= -15:
            verdict = "Moderate Vanilla Advantage"
        else:
            verdict = "Strong Vanilla Advantage"

        return BenchmarkResult(
            project_id=config.id,
            project_name=config.name,
            categories=config.categories,
            complexity=config.complexity,
            cco_result=cco_result,
            vanilla_result=vanilla_result,
            comparison=comparison,
            verdict=verdict,
            score_difference=round(diff, 1),
            prompt_used=config.prompt,
        )


class ResultsManager:
    """Manages benchmark results storage and retrieval."""

    def __init__(self, results_dir: Path):
        self.results_dir = results_dir
        self.results_dir.mkdir(parents=True, exist_ok=True)

    def save_result(self, result: BenchmarkResult) -> Path:
        """Save a benchmark result to JSON."""
        filename = f"{result.project_id}_{result.timestamp.replace(':', '-')}.json"
        filepath = self.results_dir / filename

        filepath.write_text(json.dumps(result.to_dict(), indent=2), encoding="utf-8")
        return filepath

    def load_result(self, filepath: Path) -> BenchmarkResult:
        """Load a benchmark result from JSON."""
        data = json.loads(filepath.read_text(encoding="utf-8"))
        return BenchmarkResult.from_dict(data)

    def list_results(self) -> list[Path]:
        """List all saved results."""
        return sorted(self.results_dir.glob("*.json"), reverse=True)

    def get_latest_results(self, limit: int = 10) -> list[BenchmarkResult]:
        """Get the most recent results."""
        files = self.list_results()[:limit]
        return [self.load_result(f) for f in files]

    def get_summary(self) -> dict[str, Any]:
        """Get summary statistics across all results."""
        results = [self.load_result(f) for f in self.list_results()]

        if not results:
            return {"total_runs": 0}

        cco_wins = sum(1 for r in results if r.score_difference > 5)
        vanilla_wins = sum(1 for r in results if r.score_difference < -5)
        mixed = len(results) - cco_wins - vanilla_wins

        avg_cco_score = sum(r.cco_result.score for r in results) / len(results)
        avg_vanilla_score = sum(r.vanilla_result.score for r in results) / len(results)
        avg_diff = sum(r.score_difference for r in results) / len(results)

        return {
            "total_runs": len(results),
            "cco_wins": cco_wins,
            "vanilla_wins": vanilla_wins,
            "mixed": mixed,
            "avg_cco_score": round(avg_cco_score, 1),
            "avg_vanilla_score": round(avg_vanilla_score, 1),
            "avg_difference": round(avg_diff, 1),
            "by_project": self._group_by_project(results),
        }

    def _group_by_project(self, results: list[BenchmarkResult]) -> dict[str, Any]:
        """Group results by project."""
        grouped: dict[str, list[BenchmarkResult]] = {}
        for r in results:
            if r.project_id not in grouped:
                grouped[r.project_id] = []
            grouped[r.project_id].append(r)

        summary = {}
        for project_id, project_results in grouped.items():
            avg_diff = sum(r.score_difference for r in project_results) / len(project_results)
            summary[project_id] = {
                "runs": len(project_results),
                "avg_difference": round(avg_diff, 1),
                "latest_verdict": project_results[0].verdict,
            }

        return summary


def discover_projects(projects_dir: Path) -> list[ProjectConfig]:
    """Discover all benchmark projects."""
    projects = []
    for subdir in sorted(projects_dir.iterdir()):
        if subdir.is_dir() and (subdir / "PROMPT.md").exists():
            projects.append(ProjectConfig(subdir))
    return projects

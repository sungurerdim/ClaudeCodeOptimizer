"""
CCO Benchmark - Web UI Server

FastAPI server for the benchmark dashboard.
"""

import asyncio
import logging
import shutil
import subprocess
import sys
import traceback
from collections import deque
from datetime import datetime
from pathlib import Path
from typing import Any

from fastapi import BackgroundTasks, FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from ..runner import (
    BenchmarkResult,
    ProjectConfig,
    ResultsManager,
    TestExecutor,
    discover_projects,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("cco-benchmark")

# Configuration
BENCHMARK_DIR = Path(__file__).parent.parent
PROJECTS_DIR = BENCHMARK_DIR / "projects"
RESULTS_DIR = BENCHMARK_DIR / "results"
OUTPUT_DIR = BENCHMARK_DIR / "output"
STATIC_DIR = Path(__file__).parent / "static"


# ============== Activity Log ==============


class ActivityLog:
    """Activity log for tracking operations (shown in UI)."""

    def __init__(self, max_entries: int = 100) -> None:
        self._entries: deque[dict[str, str]] = deque(maxlen=max_entries)

    def add(self, message: str, level: str = "info") -> None:
        """Add an entry to the activity log."""
        entry = {
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "message": message,
            "level": level,
        }
        self._entries.append(entry)
        logger.info(f"[{level.upper()}] {message}")

    def get_entries(self, limit: int = 50) -> list[dict[str, str]]:
        """Get recent log entries (newest first)."""
        entries = list(self._entries)
        return list(reversed(entries[-limit:]))

    def clear(self) -> None:
        """Clear all log entries."""
        self._entries.clear()


activity_log = ActivityLog()


def log_activity(message: str, level: str = "info") -> None:
    """Log an activity message."""
    activity_log.add(message, level)


# ============== System Check ==============


def check_system_dependencies() -> dict[str, Any]:
    """Check if required dependencies are installed."""
    result = {
        "python": {
            "installed": True,
            "version": sys.version.split()[0],
            "path": sys.executable,
        },
        "ccbox": {
            "installed": False,
            "version": None,
            "path": None,
        },
        "ready": False,
    }

    # Check ccbox
    ccbox_path = shutil.which("ccbox")
    if ccbox_path:
        result["ccbox"]["installed"] = True
        result["ccbox"]["path"] = ccbox_path
        try:
            version_output = subprocess.run(
                ["ccbox", "--version"],
                capture_output=True,
                text=True,
                timeout=5,
                encoding="utf-8",
                errors="replace",
            )
            if version_output.returncode == 0:
                result["ccbox"]["version"] = version_output.stdout.strip().split()[-1]
        except Exception:
            pass

    result["ready"] = result["python"]["installed"] and result["ccbox"]["installed"]
    return result


# ============== Initialize App ==============

app = FastAPI(title="CCO Benchmark", version="1.0.0")
results_manager = ResultsManager(RESULTS_DIR)

# Track running tests
running_tests: dict[str, dict[str, Any]] = {}

# Track installation status
install_status: dict[str, Any] = {"installing": False, "package": None, "output": ""}


# ============== Exception Handlers ==============


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Global exception handler for unhandled errors."""
    logger.error(f"Unhandled exception on {request.method} {request.url.path}")
    logger.error(f"Exception: {type(exc).__name__}: {exc}")
    logger.error(traceback.format_exc())
    log_activity(f"Error: {type(exc).__name__}: {exc}", "error")
    return JSONResponse(
        status_code=500,
        content={
            "detail": f"Internal server error: {type(exc).__name__}: {str(exc)}",
            "path": request.url.path,
        },
    )


# ============== Models ==============


class RunTestRequest(BaseModel):
    project_ids: list[str]
    model: str = "opus"


class TestStatus(BaseModel):
    project_id: str
    status: str  # "pending", "running_vanilla", "running_cco", "completed", "failed"
    progress: int  # 0-100
    current_variant: str | None = None
    error: str | None = None
    result: dict | None = None


# ============== API Routes ==============


@app.get("/health")
async def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy", "service": "cco-benchmark"}


@app.get("/api/system")
async def get_system_status() -> dict[str, Any]:
    """Get system status and dependency checks."""
    deps = check_system_dependencies()
    return {
        "dependencies": deps,
        "ready": deps["ready"],
        "installing": install_status["installing"],
        "install_package": install_status["package"],
    }


@app.post("/api/install/{package}")
async def install_package(package: str, background_tasks: BackgroundTasks) -> dict[str, str]:
    """Install a Python package via pip."""
    allowed_packages = ["ccbox"]  # Whitelist

    if package not in allowed_packages:
        raise HTTPException(400, f"Package not allowed: {package}")

    if install_status["installing"]:
        raise HTTPException(409, "Installation already in progress")

    install_status["installing"] = True
    install_status["package"] = package
    install_status["output"] = ""

    log_activity(f"Starting installation of {package}...", "info")
    background_tasks.add_task(run_pip_install, package)

    return {"message": f"Installing {package}...", "status": "started"}


async def run_pip_install(package: str) -> None:
    """Run pip install in background."""
    try:
        result = await asyncio.to_thread(
            subprocess.run,
            [sys.executable, "-m", "pip", "install", package, "-q"],
            capture_output=True,
            text=True,
            timeout=300,
            encoding="utf-8",
            errors="replace",
        )
        install_status["output"] = result.stdout + result.stderr
        if result.returncode == 0:
            log_activity(f"Successfully installed {package}", "success")
        else:
            log_activity(f"Failed to install {package}: {result.stderr}", "error")
    except Exception as e:
        log_activity(f"Installation error: {e}", "error")
        install_status["output"] = str(e)
    finally:
        install_status["installing"] = False
        install_status["package"] = None


@app.get("/api/install/status")
async def get_install_status() -> dict[str, Any]:
    """Get current installation status."""
    return {
        "installing": install_status["installing"],
        "package": install_status["package"],
        "output": install_status["output"],
    }


@app.get("/api/activity")
async def get_activity(limit: int = 20) -> list[dict[str, str]]:
    """Get recent activity log entries."""
    return activity_log.get_entries(limit)


@app.get("/api/projects")
async def list_projects() -> list[dict[str, Any]]:
    """List all available benchmark projects."""
    projects = discover_projects(PROJECTS_DIR)
    return [
        {
            "id": p.id,
            "name": p.name,
            "categories": p.categories,
            "complexity": p.complexity,
            "has_prompt": bool(p.prompt),
        }
        for p in projects
    ]


@app.get("/api/projects/{project_id}")
async def get_project(project_id: str) -> dict[str, Any]:
    """Get project details including prompt."""
    project_dir = PROJECTS_DIR / project_id
    if not project_dir.exists():
        raise HTTPException(404, f"Project not found: {project_id}")

    config = ProjectConfig(project_dir)
    return {
        "id": config.id,
        "name": config.name,
        "categories": config.categories,
        "complexity": config.complexity,
        "prompt": config.prompt,
        "spec": (project_dir / "SPEC.md").read_text(encoding="utf-8")
        if (project_dir / "SPEC.md").exists()
        else "",
    }


@app.get("/api/projects/{project_id}/prompt")
async def get_project_prompt(project_id: str) -> dict[str, str]:
    """Get project prompt text (for copying)."""
    project_dir = PROJECTS_DIR / project_id
    if not project_dir.exists():
        raise HTTPException(404, f"Project not found: {project_id}")

    config = ProjectConfig(project_dir)
    return {"prompt": config.prompt}


@app.post("/api/run")
async def run_tests(request: RunTestRequest, background_tasks: BackgroundTasks) -> dict[str, str]:
    """Start benchmark tests for selected projects."""
    run_id = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Initialize status for all projects
    for project_id in request.project_ids:
        running_tests[f"{run_id}_{project_id}"] = {
            "project_id": project_id,
            "status": "pending",
            "progress": 0,
            "current_variant": None,
            "error": None,
            "result": None,
            "started_at": datetime.now().isoformat(),
        }

    # Start background execution
    background_tasks.add_task(execute_tests_background, run_id, request.project_ids, request.model)

    return {"run_id": run_id, "message": f"Started {len(request.project_ids)} tests"}


async def execute_tests_background(run_id: str, project_ids: list[str], model: str) -> None:
    """Execute tests in background."""
    executor = TestExecutor(OUTPUT_DIR)
    log_activity(f"Starting benchmark run: {len(project_ids)} project(s)", "info")

    for project_id in project_ids:
        key = f"{run_id}_{project_id}"
        project_dir = PROJECTS_DIR / project_id

        if not project_dir.exists():
            running_tests[key]["status"] = "failed"
            running_tests[key]["error"] = f"Project not found: {project_id}"
            log_activity(f"Project not found: {project_id}", "error")
            continue

        config = ProjectConfig(project_dir)
        log_activity(f"Testing project: {config.name}", "info")

        try:
            # Run vanilla
            running_tests[key]["status"] = "running_vanilla"
            running_tests[key]["current_variant"] = "vanilla"
            running_tests[key]["progress"] = 25
            log_activity(f"Running vanilla variant for {config.name}...", "info")

            vanilla_result = await asyncio.to_thread(executor.run_project, config, "vanilla", model)

            if not vanilla_result.success:
                log_activity(
                    f"Vanilla failed (exit={vanilla_result.exit_code}): {vanilla_result.error_message}",
                    "warning",
                )
                if vanilla_result.command:
                    log_activity(f"  Command: {vanilla_result.command}", "warning")
                if vanilla_result.stderr_excerpt:
                    log_activity(f"  Stderr: {vanilla_result.stderr_excerpt[:200]}", "warning")

            running_tests[key]["progress"] = 50

            # Run CCO (two phases: setup + test)
            running_tests[key]["status"] = "running_cco"
            running_tests[key]["current_variant"] = "cco"
            running_tests[key]["progress"] = 60
            log_activity(f"Running CCO variant for {config.name} (setup + test)...", "info")

            cco_result = await asyncio.to_thread(executor.run_project, config, "cco", model)

            running_tests[key]["progress"] = 90

            if not cco_result.success:
                log_activity(
                    f"CCO failed (exit={cco_result.exit_code}): {cco_result.error_message}",
                    "warning",
                )
                if cco_result.command:
                    log_activity(f"  Command: {cco_result.command}", "warning")
                if cco_result.stderr_excerpt:
                    log_activity(f"  Stderr: {cco_result.stderr_excerpt[:200]}", "warning")

            # Build full benchmark result
            from ..runner import compare_metrics

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

            benchmark_result = BenchmarkResult(
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

            # Save result
            results_manager.save_result(benchmark_result)

            running_tests[key]["status"] = "completed"
            running_tests[key]["progress"] = 100
            running_tests[key]["result"] = benchmark_result.to_dict()
            log_activity(f"Completed: {config.name} - {verdict} (diff: {diff:+.1f})", "success")

        except Exception as e:
            running_tests[key]["status"] = "failed"
            running_tests[key]["error"] = str(e)
            log_activity(f"Failed: {project_id} - {e}", "error")

    log_activity("Benchmark run completed", "success")


@app.get("/api/status/{run_id}")
async def get_run_status(run_id: str) -> list[dict[str, Any]]:
    """Get status of all tests in a run."""
    statuses = []
    for key, status in running_tests.items():
        if key.startswith(f"{run_id}_"):
            statuses.append(status)
    return statuses


@app.get("/api/status/{run_id}/{project_id}")
async def get_test_status(run_id: str, project_id: str) -> dict[str, Any]:
    """Get status of a specific test."""
    key = f"{run_id}_{project_id}"
    if key not in running_tests:
        raise HTTPException(404, "Test not found")
    return running_tests[key]


@app.get("/api/results")
async def list_results(limit: int = 20) -> list[dict[str, Any]]:
    """List saved benchmark results."""
    files = results_manager.list_results()[:limit]
    results = []
    for f in files:
        try:
            result = results_manager.load_result(f)
            results.append(
                {
                    "filename": f.name,
                    "project_id": result.project_id,
                    "project_name": result.project_name,
                    "verdict": result.verdict,
                    "score_difference": result.score_difference,
                    "cco_score": result.cco_result.score,
                    "vanilla_score": result.vanilla_result.score,
                    "cco_time": result.cco_result.generation_time_seconds,
                    "vanilla_time": result.vanilla_result.generation_time_seconds,
                    "timestamp": result.timestamp,
                }
            )
        except Exception:
            pass
    return results


@app.get("/api/results/{filename}")
async def get_result(filename: str) -> dict[str, Any]:
    """Get a specific result by filename."""
    filepath = RESULTS_DIR / filename
    if not filepath.exists():
        raise HTTPException(404, "Result not found")

    result = results_manager.load_result(filepath)
    return result.to_dict()


@app.get("/api/summary")
async def get_summary() -> dict[str, Any]:
    """Get summary statistics."""
    return results_manager.get_summary()


@app.delete("/api/results/{filename}")
async def delete_result(filename: str) -> dict[str, str]:
    """Delete a result file."""
    filepath = RESULTS_DIR / filename
    if not filepath.exists():
        raise HTTPException(404, "Result not found")

    filepath.unlink()
    return {"message": f"Deleted {filename}"}


# ============== Static Files & HTML ==============

# Serve static files
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


@app.get("/", response_class=HTMLResponse)
async def index():
    """Serve main dashboard page."""
    html_file = Path(__file__).parent / "templates" / "index.html"
    if html_file.exists():
        return HTMLResponse(html_file.read_text(encoding="utf-8"))
    return HTMLResponse("<h1>CCO Benchmark Suite</h1><p>Templates not found</p>")


# ============== Main ==============


def main():
    """Run the server."""
    import uvicorn

    # Disable ANSI colors for Windows CMD compatibility
    log_config = uvicorn.config.LOGGING_CONFIG
    log_config["formatters"]["access"]["fmt"] = "%(asctime)s - %(message)s"
    log_config["formatters"]["default"]["fmt"] = "%(asctime)s - %(levelname)s - %(message)s"
    log_config["formatters"]["access"]["use_colors"] = False
    log_config["formatters"]["default"]["use_colors"] = False

    print("Starting CCO Benchmark Suite server...")
    print("Open http://localhost:8765 in your browser")
    uvicorn.run(app, host="127.0.0.1", port=8765, log_config=log_config)


if __name__ == "__main__":
    main()

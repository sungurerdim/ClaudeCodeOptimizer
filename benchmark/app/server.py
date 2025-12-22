"""
CCO Benchmark - Web UI Server

FastAPI server for the benchmark dashboard.
"""

import asyncio
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi import BackgroundTasks, FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from runner import (
    BenchmarkResult,
    ProjectConfig,
    ResultsManager,
    TestExecutor,
    discover_projects,
)

# Configuration
BENCHMARK_DIR = Path(__file__).parent.parent
PROJECTS_DIR = BENCHMARK_DIR / "projects"
RESULTS_DIR = BENCHMARK_DIR / "results"
OUTPUT_DIR = BENCHMARK_DIR / "output"
STATIC_DIR = Path(__file__).parent / "static"

# Initialize
app = FastAPI(title="CCO Benchmark", version="1.0.0")
results_manager = ResultsManager(RESULTS_DIR)

# Track running tests
running_tests: dict[str, dict[str, Any]] = {}


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
        "spec": (project_dir / "SPEC.md").read_text() if (project_dir / "SPEC.md").exists() else "",
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

    for project_id in project_ids:
        key = f"{run_id}_{project_id}"
        project_dir = PROJECTS_DIR / project_id

        if not project_dir.exists():
            running_tests[key]["status"] = "failed"
            running_tests[key]["error"] = f"Project not found: {project_id}"
            continue

        config = ProjectConfig(project_dir)

        try:
            # Run vanilla
            running_tests[key]["status"] = "running_vanilla"
            running_tests[key]["current_variant"] = "vanilla"
            running_tests[key]["progress"] = 25

            vanilla_result = await asyncio.to_thread(executor.run_project, config, "vanilla", model)

            running_tests[key]["progress"] = 50

            # Run CCO
            running_tests[key]["status"] = "running_cco"
            running_tests[key]["current_variant"] = "cco"
            running_tests[key]["progress"] = 75

            cco_result = await asyncio.to_thread(executor.run_project, config, "cco", model)

            # Build full benchmark result
            from runner import compare_metrics

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

        except Exception as e:
            running_tests[key]["status"] = "failed"
            running_tests[key]["error"] = str(e)


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
        return HTMLResponse(html_file.read_text())
    return HTMLResponse("<h1>CCO Benchmark Suite</h1><p>Templates not found</p>")


# ============== Main ==============


def main():
    """Run the server."""
    import uvicorn

    print("Starting CCO Benchmark Suite server...")
    print("Open http://localhost:8765 in your browser")
    uvicorn.run(app, host="0.0.0.0", port=8765)


if __name__ == "__main__":
    main()

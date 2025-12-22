"""
CCO Benchmark CLI Entry Point.

Usage:
    python -m benchmark              # Start web UI
    python -m benchmark --cli        # CLI mode
    python -m benchmark --analyze    # Analyze existing results
"""

import argparse
import sys
from pathlib import Path

SUITE_DIR = Path(__file__).parent
PROJECTS_DIR = SUITE_DIR / "projects"
RESULTS_DIR = SUITE_DIR / "results"


def cli_list_projects():
    """List available projects."""
    from runner import discover_projects

    projects = discover_projects(PROJECTS_DIR)
    print("\nAvailable Benchmark Projects:")
    print("-" * 60)

    for p in projects:
        cats = ", ".join(p.categories[:3])
        if len(p.categories) > 3:
            cats += f" +{len(p.categories) - 3}"
        print(f"  {p.id:<25} [{p.complexity:^8}]  {cats}")

    print(f"\nTotal: {len(projects)} projects")


def cli_run(project_id: str, variant: str, model: str):
    """Run a single benchmark."""
    from runner import ProjectConfig, TestExecutor

    project_dir = PROJECTS_DIR / project_id
    if not project_dir.exists():
        print(f"Error: Project not found: {project_id}")
        sys.exit(1)

    config = ProjectConfig(project_dir)
    executor = TestExecutor(SUITE_DIR / "output")

    print(f"\nRunning {project_id} ({variant})...")
    result = executor.run_project(config, variant, model)

    print(f"\nResult: {'Success' if result.success else 'Failed'}")
    print(f"Score: {result.score}")
    print(f"Time: {result.generation_time_seconds:.1f}s")

    if result.metrics:
        print("\nMetrics:")
        print(f"  LOC: {result.metrics.total_loc}")
        print(f"  Functions: {result.metrics.functions + result.metrics.methods}")
        print(f"  Type Coverage: {result.metrics.type_coverage_pct:.1f}%")
        print(f"  Anti-patterns: {result.metrics.bare_excepts + result.metrics.silent_passes}")

    if result.error_message:
        print(f"\nError: {result.error_message}")


def cli_compare(project_id: str, model: str):
    """Run full comparison benchmark."""
    from runner import ProjectConfig, ResultsManager, TestExecutor

    project_dir = PROJECTS_DIR / project_id
    if not project_dir.exists():
        print(f"Error: Project not found: {project_id}")
        sys.exit(1)

    config = ProjectConfig(project_dir)
    executor = TestExecutor(SUITE_DIR / "output")
    results_manager = ResultsManager(RESULTS_DIR)

    print(f"\n{'=' * 60}")
    print(f"  CCO BENCHMARK: {config.name}")
    print(f"{'=' * 60}\n")

    result = executor.run_benchmark(config, model)

    # Print results
    print(f"\n{'=' * 60}")
    print("  RESULTS")
    print(f"{'=' * 60}")
    print(f"\n  CCO Score:     {result.cco_result.score}")
    print(f"  Vanilla Score: {result.vanilla_result.score}")
    print(f"  Difference:    {'+' if result.score_difference > 0 else ''}{result.score_difference}")
    print(f"\n  VERDICT: {result.verdict}")

    print("\n  Timing:")
    print(f"    CCO:     {result.cco_result.generation_time_seconds:.1f}s")
    print(f"    Vanilla: {result.vanilla_result.generation_time_seconds:.1f}s")

    # Save result
    filepath = results_manager.save_result(result)
    print(f"\n  Result saved: {filepath.name}")


def cli_summary():
    """Show summary statistics."""
    from runner import ResultsManager

    results_manager = ResultsManager(RESULTS_DIR)
    summary = results_manager.get_summary()

    if summary["total_runs"] == 0:
        print("\nNo benchmark results found.")
        return

    print(f"\n{'=' * 60}")
    print("  CCO BENCHMARK SUMMARY")
    print(f"{'=' * 60}")
    print(f"\n  Total Runs: {summary['total_runs']}")
    print(f"  CCO Wins:   {summary['cco_wins']}")
    print(f"  Vanilla:    {summary['vanilla_wins']}")
    print(f"  Mixed:      {summary['mixed']}")
    print("\n  Average Scores:")
    print(f"    CCO:        {summary['avg_cco_score']}")
    print(f"    Vanilla:    {summary['avg_vanilla_score']}")
    print(
        f"    Difference: {'+' if summary['avg_difference'] > 0 else ''}{summary['avg_difference']}"
    )


def start_server():
    """Start the web UI server."""
    from app.server import main

    main()


def main():
    parser = argparse.ArgumentParser(
        description="CCO Benchmark",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m benchmark                        # Start web UI
  python -m benchmark --list                 # List projects
  python -m benchmark --run 01_rest_api      # Full benchmark
  python -m benchmark --summary              # Show summary
        """,
    )

    parser.add_argument("--cli", action="store_true", help="CLI mode (no web UI)")
    parser.add_argument("--list", action="store_true", help="List available projects")
    parser.add_argument("--run", metavar="PROJECT", help="Run benchmark for project")
    parser.add_argument(
        "--variant",
        choices=["cco", "vanilla", "both"],
        default="both",
        help="Which variant to run (default: both)",
    )
    parser.add_argument("--model", default="opus", help="Model to use (default: opus)")
    parser.add_argument("--summary", action="store_true", help="Show summary statistics")
    parser.add_argument("--port", type=int, default=8765, help="Web UI port")

    args = parser.parse_args()

    if args.list:
        cli_list_projects()
    elif args.run:
        if args.variant == "both":
            cli_compare(args.run, args.model)
        else:
            cli_run(args.run, args.variant, args.model)
    elif args.summary:
        cli_summary()
    else:
        start_server()


if __name__ == "__main__":
    main()

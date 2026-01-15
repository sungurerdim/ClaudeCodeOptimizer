"""AI-powered blind code evaluation using Claude via ccbox."""

from __future__ import annotations

import json
import logging
import random
import re
import subprocess
import threading
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

# Path to comparison prompt template
COMPARISON_PROMPT_FILE = "comparison-prompt.md"

# 10 universal evaluation dimensions with weights (total: 100%)
# Applies to all project types: libraries, CLIs, services, etc.
DIMENSIONS: list[tuple[str, int]] = [
    ("functional_completeness", 15),  # Does it implement all requirements?
    ("correctness_robustness", 14),  # Does it work correctly and handle errors?
    ("architecture", 12),  # Is it well-structured with clean dependencies?
    ("code_quality", 12),  # Is it readable, maintainable, well-crafted?
    ("security", 10),  # Is it safe from vulnerabilities?
    ("type_safety", 10),  # Are types used effectively?
    ("testing", 10),  # Is it tested or testable?
    ("maintainability", 9),  # Is it easy to modify and extend?
    ("performance", 4),  # Are there obvious inefficiencies?
    ("best_practices", 4),  # Does it follow modern conventions?
]

# Grade thresholds for weighted overall score (0-100)
GRADE_THRESHOLDS: list[tuple[int, str]] = [
    (97, "A+"),
    (93, "A"),
    (90, "A-"),
    (87, "B+"),
    (83, "B"),
    (80, "B-"),
    (77, "C+"),
    (73, "C"),
    (70, "C-"),
    (60, "D"),
    (0, "F"),
]


def calculate_weighted_score(variant: VariantResult) -> float:
    """
    Calculate weighted overall score from dimension scores.

    Each dimension is scored 0-100 and contributes based on its weight.
    Formula: sum(dimension_score * weight) / 100

    Returns:
        Weighted overall score (0-100)
    """
    total = 0.0
    for dim_name, weight in DIMENSIONS:
        dim_score = getattr(variant, dim_name, DimensionScore())
        total += dim_score.score * weight
    return round(total / 100, 1)


def calculate_grade(score: float) -> str:
    """
    Calculate letter grade from weighted score.

    Args:
        score: Weighted overall score (0-100)

    Returns:
        Letter grade (A+ through F)
    """
    for threshold, grade in GRADE_THRESHOLDS:
        if score >= threshold:
            return grade
    return "F"


@dataclass
class DimensionScore:
    """Score for a single evaluation dimension."""

    score: int = 0
    evidence: str = ""


@dataclass
class VariantResult:
    """Complete evaluation result for one variant."""

    functional_completeness: DimensionScore = field(default_factory=DimensionScore)
    correctness_robustness: DimensionScore = field(default_factory=DimensionScore)
    architecture: DimensionScore = field(default_factory=DimensionScore)
    code_quality: DimensionScore = field(default_factory=DimensionScore)
    security: DimensionScore = field(default_factory=DimensionScore)
    type_safety: DimensionScore = field(default_factory=DimensionScore)
    testing: DimensionScore = field(default_factory=DimensionScore)
    maintainability: DimensionScore = field(default_factory=DimensionScore)
    performance: DimensionScore = field(default_factory=DimensionScore)
    best_practices: DimensionScore = field(default_factory=DimensionScore)
    anti_patterns_found: list[str] = field(default_factory=list)
    overall_score: int = 0
    grade: str = "?"
    strengths: list[str] = field(default_factory=list)
    weaknesses: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "functional_completeness": {
                "score": self.functional_completeness.score,
                "evidence": self.functional_completeness.evidence,
            },
            "correctness_robustness": {
                "score": self.correctness_robustness.score,
                "evidence": self.correctness_robustness.evidence,
            },
            "architecture": {
                "score": self.architecture.score,
                "evidence": self.architecture.evidence,
            },
            "code_quality": {
                "score": self.code_quality.score,
                "evidence": self.code_quality.evidence,
            },
            "security": {
                "score": self.security.score,
                "evidence": self.security.evidence,
            },
            "type_safety": {
                "score": self.type_safety.score,
                "evidence": self.type_safety.evidence,
            },
            "testing": {
                "score": self.testing.score,
                "evidence": self.testing.evidence,
            },
            "maintainability": {
                "score": self.maintainability.score,
                "evidence": self.maintainability.evidence,
            },
            "performance": {
                "score": self.performance.score,
                "evidence": self.performance.evidence,
            },
            "best_practices": {
                "score": self.best_practices.score,
                "evidence": self.best_practices.evidence,
            },
            "anti_patterns_found": self.anti_patterns_found,
            "overall_score": self.overall_score,
            "grade": self.grade,
            "strengths": self.strengths,
            "weaknesses": self.weaknesses,
        }


@dataclass
class DimensionComparison:
    """Comparison result for a single dimension."""

    dimension: str = ""
    weight: int = 0  # Weight percentage (0-100)
    winner: str = "tie"
    diff: int = 0
    cco_score: int = 0
    vanilla_score: int = 0
    cco_weighted: float = 0.0  # Weighted contribution to total
    vanilla_weighted: float = 0.0  # Weighted contribution to total


@dataclass
class ExecutiveSummaryItem:
    """A single executive summary insight."""

    topic: str = ""
    winner: str = ""  # "cco", "vanilla", or "tie"
    insight: str = ""


@dataclass
class AIComparisonResult:
    """Complete AI comparison result."""

    cco: VariantResult = field(default_factory=VariantResult)
    vanilla: VariantResult = field(default_factory=VariantResult)
    winner: str = "tie"
    margin: str = "negligible"
    score_difference: int = 0
    verdict: str = "Mixed Results"
    dimension_breakdown: list[DimensionComparison] = field(default_factory=list)
    key_differences: list[str] = field(default_factory=list)
    executive_summary: list[ExecutiveSummaryItem] = field(default_factory=list)
    recommendation: str = ""
    blind_assignment: str = ""  # "cco=a" or "cco=b" for transparency
    raw_response: str = ""
    error: str | None = None
    # Metadata
    duration_seconds: float = 0.0
    timestamp: str = ""
    report_file: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON response."""
        # Calculate dimension wins (weighted and unweighted)
        cco_wins = sum(1 for d in self.dimension_breakdown if d.winner == "cco")
        vanilla_wins = sum(1 for d in self.dimension_breakdown if d.winner == "vanilla")
        ties = sum(1 for d in self.dimension_breakdown if d.winner == "tie")

        # Calculate weighted wins (dimensions where one side won, weighted by importance)
        cco_weighted_wins = sum(d.weight for d in self.dimension_breakdown if d.winner == "cco")
        vanilla_weighted_wins = sum(
            d.weight for d in self.dimension_breakdown if d.winner == "vanilla"
        )

        # Build executive summary with weighted info
        diff = abs(self.score_difference)
        if self.winner == "cco":
            impact = f"CCO improved code quality by {diff} points ({self.cco.grade} vs {self.vanilla.grade})."
        elif self.winner == "vanilla":
            impact = f"Vanilla performed better by {diff} points ({self.vanilla.grade} vs {self.cco.grade})."
        else:
            impact = f"Both implementations are essentially equal ({self.cco.grade})."

        exec_summary = (
            f"{self.verdict}. {impact} "
            f"CCO won {cco_wins}/10 dimensions ({cco_weighted_wins}% weight), "
            f"Vanilla won {vanilla_wins}/10 ({vanilla_weighted_wins}% weight), {ties} tied. "
            f"{self.recommendation}"
        )

        return {
            # Executive summary - brief text overview
            "executive_summary_text": exec_summary,
            # Executive summary - top 5 practical insights (NEW)
            "executive_summary": [
                {"topic": item.topic, "winner": item.winner, "insight": item.insight}
                for item in self.executive_summary
            ],
            # Quick stats
            "summary": {
                "cco_score": self.cco.overall_score,
                "vanilla_score": self.vanilla.overall_score,
                "difference": self.score_difference,
                "cco_grade": self.cco.grade,
                "vanilla_grade": self.vanilla.grade,
                "winner": self.winner,
                "verdict": self.verdict,
                "dimension_wins": f"CCO {cco_wins} - Vanilla {vanilla_wins} - Tie {ties}",
                "weighted_dimension_wins": f"CCO {cco_weighted_wins}% - Vanilla {vanilla_weighted_wins}%",
            },
            "cco": self.cco.to_dict(),
            "vanilla": self.vanilla.to_dict(),
            "comparison": {
                "winner": self.winner,
                "margin": self.margin,
                "score_difference": self.score_difference,
                "verdict": self.verdict,
                "dimension_breakdown": [
                    {
                        "dimension": d.dimension,
                        "weight": d.weight,
                        "winner": d.winner,
                        "diff": d.diff,
                        "cco_score": d.cco_score,
                        "vanilla_score": d.vanilla_score,
                        "cco_weighted": d.cco_weighted,
                        "vanilla_weighted": d.vanilla_weighted,
                    }
                    for d in self.dimension_breakdown
                ],
                "key_differences": self.key_differences,
                "executive_summary": [
                    {"topic": item.topic, "winner": item.winner, "insight": item.insight}
                    for item in self.executive_summary
                ],
                "recommendation": self.recommendation,
                "blind_assignment": self.blind_assignment,
            },
            "raw_response": self.raw_response if self.error else None,
            "error": self.error,
            # Metadata
            "duration_seconds": self.duration_seconds,
            "timestamp": self.timestamp,
            "report_file": self.report_file,
        }


def parse_dimension_score(data: dict[str, Any]) -> DimensionScore:
    """Parse a dimension score from JSON."""
    return DimensionScore(
        score=int(data.get("score", 0)),
        evidence=str(data.get("evidence", data.get("notes", ""))),
    )


def parse_variant(data: dict[str, Any]) -> VariantResult:
    """Parse a variant result from JSON."""
    return VariantResult(
        functional_completeness=parse_dimension_score(data.get("functional_completeness", {})),
        correctness_robustness=parse_dimension_score(data.get("correctness_robustness", {})),
        architecture=parse_dimension_score(data.get("architecture", {})),
        code_quality=parse_dimension_score(data.get("code_quality", {})),
        security=parse_dimension_score(data.get("security", {})),
        type_safety=parse_dimension_score(data.get("type_safety", {})),
        testing=parse_dimension_score(data.get("testing", {})),
        maintainability=parse_dimension_score(data.get("maintainability", {})),
        performance=parse_dimension_score(data.get("performance", {})),
        best_practices=parse_dimension_score(data.get("best_practices", {})),
        anti_patterns_found=list(data.get("anti_patterns_found", []))[:10],
        overall_score=int(data.get("overall_score", 0)),
        grade=str(data.get("grade", "?")),
        strengths=list(data.get("strengths", []))[:5],
        weaknesses=list(data.get("weaknesses", []))[:5],
    )


def calculate_ai_verdict(cco_score: int, vanilla_score: int) -> tuple[str, str, str]:
    """
    Calculate winner, margin, and verdict from scores for AI comparison.

    Note: This is separate from metrics.calculate_verdict() which takes a single
    score_diff and returns only a verdict string. This function is specific to
    AI evaluation and returns a tuple with winner, margin, and verdict.

    Returns:
        (winner, margin, verdict) tuple
    """
    diff = cco_score - vanilla_score
    abs_diff = abs(diff)

    if abs_diff < 3:
        return "tie", "negligible", "Essentially Equal"

    # Determine margin based on score difference thresholds
    if abs_diff < 8:
        margin = "slight"
    elif abs_diff < 15:
        margin = "moderate"
    elif abs_diff < 25:
        margin = "significant"
    else:
        margin = "decisive"

    # Build verdict from margin and winner
    winner = "cco" if diff > 0 else "vanilla"
    winner_label = "CCO" if diff > 0 else "Vanilla"
    verdict_prefix = {
        "slight": "Slight",
        "moderate": "Moderate",
        "significant": "Significant",
        "decisive": "Strong",
    }
    verdict = f"{verdict_prefix[margin]} {winner_label} Advantage"

    return winner, margin, verdict


def extract_ai_content(response: str) -> str:
    """
    Extract the actual AI content from various output formats.

    Handles:
    - stream-json format: multiple JSON objects per line, extract from type="result"
    - Plain text with markdown code blocks
    - Plain JSON
    """
    lines = response.strip().split("\n")

    # Try stream-json format first: look for type="result" line
    for line in reversed(lines):  # Start from end for efficiency
        line = line.strip()
        if not line or not line.startswith("{"):
            continue
        try:
            obj = json.loads(line)
            if obj.get("type") == "result":
                # Found the result object, extract the actual content
                content = obj.get("result", "")
                if content:
                    return content
        except json.JSONDecodeError:
            continue

    # Not stream-json, return original
    return response


def parse_ai_response(response: str, cco_is_a: bool) -> AIComparisonResult:
    """
    Parse the AI response JSON into structured result.

    Args:
        response: Raw AI response text
        cco_is_a: If True, implementation_a is CCO; otherwise implementation_b is CCO
    """
    result = AIComparisonResult(raw_response=response)
    result.blind_assignment = "cco=a" if cco_is_a else "cco=b"

    # Extract actual content from stream-json or other formats
    cleaned = extract_ai_content(response)

    try:
        # Remove markdown code blocks if present (handles ```json or ``` anywhere)
        # Pattern to match ```json ... ``` or ``` ... ``` blocks
        code_block_pattern = r"```(?:json)?\s*\n?([\s\S]*?)\n?```"
        code_block_match = re.search(code_block_pattern, cleaned)
        if code_block_match:
            cleaned = code_block_match.group(1).strip()
        elif cleaned.startswith("```"):
            # Fallback: simple line-based extraction
            lines = cleaned.split("\n")
            start = 1 if lines[0].startswith("```") else 0
            end = -1 if lines[-1].strip() == "```" else len(lines)
            cleaned = "\n".join(lines[start:end])

        # Find JSON object boundaries (handles text before/after JSON)
        start_idx = cleaned.find("{")
        end_idx = cleaned.rfind("}") + 1
        if start_idx >= 0 and end_idx > start_idx:
            cleaned = cleaned[start_idx:end_idx]
        else:
            # No JSON found at all
            raise json.JSONDecodeError("No JSON object found in response", cleaned, 0)

        data = json.loads(cleaned)

        # Parse variants based on blind assignment
        impl_a = data.get("implementation_a", {})
        impl_b = data.get("implementation_b", {})

        if cco_is_a:
            result.cco = parse_variant(impl_a)
            result.vanilla = parse_variant(impl_b)
        else:
            result.cco = parse_variant(impl_b)
            result.vanilla = parse_variant(impl_a)

        # Calculate weighted overall scores (don't trust AI's math)
        cco_weighted_total = calculate_weighted_score(result.cco)
        vanilla_weighted_total = calculate_weighted_score(result.vanilla)

        # Override AI's overall_score with our weighted calculation
        result.cco.overall_score = int(cco_weighted_total)
        result.vanilla.overall_score = int(vanilla_weighted_total)

        # Calculate grades from weighted scores
        result.cco.grade = calculate_grade(cco_weighted_total)
        result.vanilla.grade = calculate_grade(vanilla_weighted_total)

        # Build dimension breakdown with weights
        for dim_name, weight in DIMENSIONS:
            cco_dim = getattr(result.cco, dim_name, DimensionScore())
            vanilla_dim = getattr(result.vanilla, dim_name, DimensionScore())
            cco_score = cco_dim.score
            vanilla_score = vanilla_dim.score
            diff = cco_score - vanilla_score

            # Calculate weighted contributions
            cco_weighted = round(cco_score * weight / 100, 2)
            vanilla_weighted = round(vanilla_score * weight / 100, 2)

            if abs(diff) < 3:
                dim_winner = "tie"
            elif diff > 0:
                dim_winner = "cco"
            else:
                dim_winner = "vanilla"

            result.dimension_breakdown.append(
                DimensionComparison(
                    dimension=dim_name,
                    weight=weight,
                    winner=dim_winner,
                    diff=diff,
                    cco_score=cco_score,
                    vanilla_score=vanilla_score,
                    cco_weighted=cco_weighted,
                    vanilla_weighted=vanilla_weighted,
                )
            )

        # Calculate overall verdict from already-rounded scores for UI consistency
        result.score_difference = result.cco.overall_score - result.vanilla.overall_score
        result.winner, result.margin, result.verdict = calculate_ai_verdict(
            int(cco_weighted_total), int(vanilla_weighted_total)
        )

        # Parse comparison section
        comp = data.get("comparison", {})

        # Map A/B winner to cco/vanilla
        raw_winner = comp.get("winner", "tie")
        if raw_winner == "a":
            result.winner = "cco" if cco_is_a else "vanilla"
        elif raw_winner == "b":
            result.winner = "vanilla" if cco_is_a else "cco"
        # else keep calculated winner

        result.margin = comp.get("margin", result.margin)
        result.key_differences = comp.get("key_differences", [])[:5]
        result.recommendation = comp.get("recommendation", "")

        # Parse executive summary with practical insights
        exec_summary_raw = comp.get("executive_summary", [])
        for item in exec_summary_raw[:5]:  # Limit to 5 items
            if isinstance(item, dict):
                # Map A/B winner to cco/vanilla
                raw_winner = item.get("winner", "tie")
                if raw_winner == "a":
                    mapped_winner = "cco" if cco_is_a else "vanilla"
                elif raw_winner == "b":
                    mapped_winner = "vanilla" if cco_is_a else "cco"
                else:
                    mapped_winner = raw_winner

                result.executive_summary.append(
                    ExecutiveSummaryItem(
                        topic=item.get("topic", ""),
                        winner=mapped_winner,
                        insight=item.get("insight", ""),
                    )
                )

        # Recalculate verdict based on final winner
        if result.winner == "tie":
            result.verdict = "Essentially Equal"
        elif result.winner == "cco":
            if result.margin == "slight":
                result.verdict = "Slight CCO Advantage"
            elif result.margin == "moderate":
                result.verdict = "Moderate CCO Advantage"
            elif result.margin == "significant":
                result.verdict = "Significant CCO Advantage"
            else:
                result.verdict = "Strong CCO Advantage"
        else:
            if result.margin == "slight":
                result.verdict = "Slight Vanilla Advantage"
            elif result.margin == "moderate":
                result.verdict = "Moderate Vanilla Advantage"
            elif result.margin == "significant":
                result.verdict = "Significant Vanilla Advantage"
            else:
                result.verdict = "Strong Vanilla Advantage"

        # Clear raw_response on success
        result.raw_response = ""

    except json.JSONDecodeError as e:
        # Check if AI returned plain text instead of JSON
        has_json_markers = "{" in cleaned and "}" in cleaned
        if not has_json_markers:
            result.error = (
                "AI returned plain text instead of required JSON format. "
                "The evaluator may have ignored the JSON output instruction."
            )
            logger.error("AI returned plain text instead of JSON")
            logger.error(f"AI response (first 500 chars): {cleaned[:500]}")
        else:
            result.error = f"Failed to parse AI response as JSON: {e}"
            # Log the cleaned/extracted content, not raw response (which may have non-JSON prefix)
            logger.error(f"JSON parse error: {e}")
            logger.error(f"Extracted content (first 1500 chars): {cleaned[:1500]}")
        # Store extracted content (cleaner than raw response with debug prefixes)
        result.raw_response = cleaned[:5000] if cleaned else response[:5000]
    except Exception as e:
        result.error = f"Error processing response: {e}"
        logger.error(f"Processing error: {e}")
        result.raw_response = cleaned[:5000] if cleaned else response[:5000]

    return result


def run_ai_comparison(
    project_id: str,
    output_dir: Path,
    suite_dir: Path,
    original_prompt: str,
    timeout: int = 600,
) -> AIComparisonResult:
    """
    Run blind AI comparison using ccbox vanilla mode.

    The implementations are randomly assigned to A/B to ensure
    unbiased evaluation. The evaluator doesn't know which is CCO.

    Args:
        project_id: The project identifier
        output_dir: Path to benchmark output directory
        suite_dir: Path to benchmark suite directory
        original_prompt: The original prompt used to generate both variants
        timeout: Timeout in seconds for ccbox execution

    Returns:
        AIComparisonResult with comparison data or error
    """
    cco_dir = output_dir / f"{project_id}_cco"
    vanilla_dir = output_dir / f"{project_id}_vanilla"

    # Verify both directories exist
    if not cco_dir.exists():
        return AIComparisonResult(error=f"CCO output not found: {cco_dir}")
    if not vanilla_dir.exists():
        return AIComparisonResult(error=f"Vanilla output not found: {vanilla_dir}")

    # Load comparison prompt content
    comparison_prompt_path = suite_dir / COMPARISON_PROMPT_FILE
    if not comparison_prompt_path.exists():
        return AIComparisonResult(error=f"Comparison prompt not found: {comparison_prompt_path}")

    try:
        comparison_criteria = comparison_prompt_path.read_text(encoding="utf-8")
    except Exception as e:
        return AIComparisonResult(error=f"Failed to read comparison prompt: {e}")

    # BLIND ASSIGNMENT: Randomly assign which is A and which is B
    cco_is_a = random.choice([True, False])  # noqa: S311 - not for crypto

    if cco_is_a:
        dir_a = cco_dir.name
        dir_b = vanilla_dir.name
    else:
        dir_a = vanilla_dir.name
        dir_b = cco_dir.name

    logger.info(f"Blind assignment for {project_id}: A={dir_a}, B={dir_b} (cco_is_a={cco_is_a})")

    # Write comparison instructions to output_dir (once)
    comparison_prompt_dest = output_dir / "comparison-prompt.md"
    if not comparison_prompt_dest.exists():
        try:
            comparison_prompt_dest.write_text(comparison_criteria, encoding="utf-8")
        except Exception as e:
            return AIComparisonResult(error=f"Failed to copy comparison prompt: {e}")

    # Original prompt is already in each project folder as _benchmark_prompt.md
    # Reference the one in dir_a (both should have the same prompt)
    original_prompt_ref = f"{dir_a}/_benchmark_prompt.md"

    # Minimal -p prompt referencing files
    short_prompt = (
        f"Compare {dir_a}/ vs {dir_b}/ using comparison-prompt.md. "
        f"Original task: {original_prompt_ref}"
    )

    try:
        # Run ccbox from the output directory in vanilla/bare mode
        # Using same parameters as executor for consistency:
        # -U: unrestricted mode (no CPU/I/O soft limits for benchmarking)
        # -y: unattended mode (deps=ALL, stack=auto-detect, no prompts)
        # -dd: debug logging (stream output)
        # -C: working directory
        # --bare: no CCO rules (vanilla mode for unbiased evaluation)
        # -m: model selection
        # -p: prompt (also enables --print mode for non-interactive)
        cmd = [
            "ccbox",
            "-U",  # Unrestricted mode for consistent benchmarking
            "-y",
            "-dd",
            "-C",
            str(output_dir),
            "--bare",
            "-m",
            "opus",
            "-p",
            short_prompt,
        ]

        logger.info(f"Running blind AI comparison for {project_id}")
        logger.debug(f"Command: {' '.join(cmd)}")
        start_time = time.time()

        # Use Popen for streaming output
        # stdin=DEVNULL prevents ccbox from waiting for user input
        process = subprocess.Popen(
            cmd,
            cwd=str(output_dir),
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
        )

        # Collect output with streaming
        stdout_lines: list[str] = []
        stderr_lines: list[str] = []
        lock = threading.Lock()

        def read_stream(stream: Any, buffer: list[str], stream_name: str) -> None:
            """Read stream and log lines.

            Preserves original line endings for accurate output reconstruction.
            """
            try:
                for line in iter(stream.readline, ""):
                    if not line:
                        break
                    with lock:
                        buffer.append(line)  # Preserve original newlines
                    # Log each line with AI prefix (stripped for display)
                    line_stripped = line.rstrip()
                    if line_stripped:
                        # stderr logged as error, stdout as info
                        if stream_name == "stderr":
                            logger.error(f"[AI] {line_stripped[:200]}")
                        else:
                            logger.info(f"[AI] {line_stripped[:200]}")
            except Exception as e:
                logger.debug(f"Stream read error ({stream_name}): {e}")

        # Start reader threads
        stdout_thread = threading.Thread(
            target=read_stream, args=(process.stdout, stdout_lines, "stdout"), daemon=True
        )
        stderr_thread = threading.Thread(
            target=read_stream, args=(process.stderr, stderr_lines, "stderr"), daemon=True
        )
        stdout_thread.start()
        stderr_thread.start()

        # Wait for completion with timeout
        try:
            process.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            process.kill()
            return AIComparisonResult(
                error=f"AI evaluation timed out after {timeout}s. Try again or reduce code size."
            )

        # Wait for threads to finish
        stdout_thread.join(timeout=5)
        stderr_thread.join(timeout=5)

        duration = time.time() - start_time
        # Join without adding extra newlines (lines already have them)
        stdout = "".join(stdout_lines)
        stderr = "".join(stderr_lines)

        if process.returncode != 0:
            error_parts = []
            if stderr:
                error_parts.append(f"stderr: {stderr[:500]}")
            if stdout:
                error_parts.append(f"stdout: {stdout[:500]}")
            error_msg = " | ".join(error_parts) if error_parts else "No output captured"

            logger.error(f"ccbox failed for {project_id}: code={process.returncode}, {error_msg}")
            return AIComparisonResult(
                error=f"ccbox exited with code {process.returncode}: {error_msg}",
                raw_response=stdout[:2000] if stdout else "",
            )

        # Parse the response with blind assignment mapping
        result = parse_ai_response(stdout, cco_is_a)

        # Add metadata - save to _ai_comparisons/ subfolder (consistent with server.py)
        ai_results_dir = output_dir / "_ai_comparisons"
        ai_results_dir.mkdir(exist_ok=True)
        result_file = ai_results_dir / f"{project_id}.json"
        result.duration_seconds = duration
        result.timestamp = datetime.now(timezone.utc).isoformat()
        result.report_file = str(result_file)

        # Save result to file
        try:
            result_file.write_text(json.dumps(result.to_dict(), indent=2), encoding="utf-8")
        except Exception as e:
            logger.warning(f"Failed to save comparison result: {e}")

        logger.info(
            f"AI comparison complete for {project_id}: {result.verdict} "
            f"(CCO: {result.cco.overall_score}, Vanilla: {result.vanilla.overall_score}, "
            f"duration: {duration:.1f}s, report: {result_file.name})"
        )
        return result

    except FileNotFoundError:
        return AIComparisonResult(error="ccbox command not found. Install with: pip install ccbox")
    except Exception as e:
        logger.exception("AI comparison failed")
        return AIComparisonResult(error=f"AI evaluation failed: {e}")


# =============================================================================
# V2 Single Variant Analysis (for new benchmark flow)
# =============================================================================

SINGLE_VARIANT_PROMPT_FILE = "single-variant-prompt.md"


def run_single_variant_ai_analysis(
    project_id: str,
    variant_dir: Path,
    variant: str,
    original_prompt: str,
    suite_dir: Path,
    timeout: int = 600,
) -> dict[str, Any]:
    """
    Run AI-powered analysis of a SINGLE variant (not comparison).

    This is used in the new V2 benchmark flow where vanilla and CCO are
    analyzed independently, then compared using pre-computed results.

    Uses the same 10-dimension evaluation framework but for one implementation.
    Returns scores, evidence, anti-patterns, best practices for that variant.

    Args:
        project_id: The project identifier
        variant_dir: Path to the variant output directory
        variant: "vanilla" or "cco"
        original_prompt: The original prompt used to generate the code
        suite_dir: Path to benchmark suite directory
        timeout: Timeout in seconds for ccbox execution

    Returns:
        Dict with dimension scores, overall_score, grade, strengths, weaknesses
    """
    if not variant_dir.exists():
        return {"error": f"Variant directory not found: {variant_dir}", "overall_score": 0}

    # Load single variant prompt content
    prompt_path = suite_dir / SINGLE_VARIANT_PROMPT_FILE
    if not prompt_path.exists():
        # Fall back to generating inline prompt if file doesn't exist
        logger.warning(f"Single variant prompt not found: {prompt_path}, using inline prompt")
        analysis_prompt = _generate_inline_single_variant_prompt()
    else:
        try:
            analysis_prompt = prompt_path.read_text(encoding="utf-8")
        except Exception as e:
            return {"error": f"Failed to read single variant prompt: {e}", "overall_score": 0}

    # Write the prompt to the variant directory for reference
    prompt_dest = variant_dir / "_analysis_prompt.md"
    try:
        prompt_dest.write_text(analysis_prompt, encoding="utf-8")
    except Exception as e:
        logger.warning(f"Failed to write analysis prompt: {e}")

    # Short prompt for ccbox
    short_prompt = (
        "Analyze the code in this directory using _analysis_prompt.md. "
        "Original task: _benchmark_prompt.md"
    )

    try:
        # Run ccbox in vanilla/bare mode for unbiased analysis
        cmd = [
            "ccbox",
            "-U",  # Unrestricted mode
            "-y",  # Unattended mode
            "-dd",  # Debug logging
            "-C", str(variant_dir),
            "--bare",  # No CCO rules (unbiased)
            "-m", "opus",
            "-p", short_prompt,
        ]

        logger.info(f"Running AI analysis for {project_id}/{variant}")
        start_time = time.time()

        # Use Popen for streaming
        process = subprocess.Popen(
            cmd,
            cwd=str(variant_dir),
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
        )

        # Collect output with streaming
        stdout_lines: list[str] = []
        stderr_lines: list[str] = []
        lock = threading.Lock()

        def read_stream(stream: Any, buffer: list[str], stream_name: str) -> None:
            try:
                for line in iter(stream.readline, ""):
                    if not line:
                        break
                    with lock:
                        buffer.append(line)
                    line_stripped = line.rstrip()
                    if line_stripped:
                        if stream_name == "stderr":
                            logger.error(f"[AI:{variant}] {line_stripped[:200]}")
                        else:
                            logger.info(f"[AI:{variant}] {line_stripped[:200]}")
            except Exception as e:
                logger.debug(f"Stream read error ({stream_name}): {e}")

        stdout_thread = threading.Thread(
            target=read_stream, args=(process.stdout, stdout_lines, "stdout"), daemon=True
        )
        stderr_thread = threading.Thread(
            target=read_stream, args=(process.stderr, stderr_lines, "stderr"), daemon=True
        )
        stdout_thread.start()
        stderr_thread.start()

        try:
            process.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            process.kill()
            return {"error": f"AI analysis timed out after {timeout}s", "overall_score": 0}

        stdout_thread.join(timeout=5)
        stderr_thread.join(timeout=5)

        duration = time.time() - start_time
        stdout = "".join(stdout_lines)

        if process.returncode != 0:
            stderr = "".join(stderr_lines)
            return {
                "error": f"ccbox exited with code {process.returncode}",
                "stderr": stderr[:500],
                "overall_score": 0,
            }

        # Parse the response
        result = _parse_single_variant_response(stdout)
        result["duration_seconds"] = round(duration, 1)
        result["variant"] = variant
        result["project_id"] = project_id

        logger.info(
            f"AI analysis complete for {project_id}/{variant}: "
            f"score={result.get('overall_score', 0)}, grade={result.get('grade', '?')}, "
            f"duration={duration:.1f}s"
        )
        return result

    except FileNotFoundError:
        return {"error": "ccbox command not found", "overall_score": 0}
    except Exception as e:
        logger.exception(f"AI analysis failed for {project_id}/{variant}")
        return {"error": f"AI analysis failed: {e}", "overall_score": 0}


def _parse_single_variant_response(response: str) -> dict[str, Any]:
    """Parse the AI response for single variant analysis."""
    result: dict[str, Any] = {
        "overall_score": 0,
        "grade": "?",
        "strengths": [],
        "weaknesses": [],
        "anti_patterns_found": [],
    }

    # Extract actual content from stream-json or other formats
    cleaned = extract_ai_content(response)

    try:
        # Remove markdown code blocks if present
        code_block_pattern = r"```(?:json)?\s*\n?([\s\S]*?)\n?```"
        code_block_match = re.search(code_block_pattern, cleaned)
        if code_block_match:
            cleaned = code_block_match.group(1).strip()

        # Find JSON object boundaries
        start_idx = cleaned.find("{")
        end_idx = cleaned.rfind("}") + 1
        if start_idx >= 0 and end_idx > start_idx:
            cleaned = cleaned[start_idx:end_idx]
        else:
            result["error"] = "No JSON object found in response"
            result["raw_response"] = response[:2000]
            return result

        data = json.loads(cleaned)

        # Parse dimension scores
        for dim_name, _weight in DIMENSIONS:
            dim_data = data.get(dim_name, {})
            if isinstance(dim_data, dict):
                result[dim_name] = {
                    "score": int(dim_data.get("score", 0)),
                    "evidence": str(dim_data.get("evidence", dim_data.get("notes", ""))),
                }
            else:
                result[dim_name] = {"score": 0, "evidence": ""}

        # Calculate weighted overall score
        total = 0.0
        for dim_name, weight in DIMENSIONS:
            dim_score = result.get(dim_name, {}).get("score", 0)
            total += dim_score * weight
        result["overall_score"] = int(round(total / 100))

        # Calculate grade
        result["grade"] = calculate_grade(result["overall_score"])

        # Parse additional fields
        result["strengths"] = list(data.get("strengths", []))[:5]
        result["weaknesses"] = list(data.get("weaknesses", []))[:5]
        result["anti_patterns_found"] = list(data.get("anti_patterns_found", []))[:10]
        result["language_detected"] = data.get("language_detected", "Unknown")

    except json.JSONDecodeError as e:
        result["error"] = f"Failed to parse AI response: {e}"
        result["raw_response"] = cleaned[:2000]
    except Exception as e:
        result["error"] = f"Error processing response: {e}"
        result["raw_response"] = cleaned[:2000] if cleaned else response[:2000]

    return result


def _generate_inline_single_variant_prompt() -> str:
    """Generate an inline prompt for single variant analysis when file is missing."""
    dimensions_text = "\n".join(
        f"- {dim} (weight: {weight}%)" for dim, weight in DIMENSIONS
    )
    return f"""# Single Implementation Code Analysis

Analyze the code in this directory and evaluate it across 10 dimensions.

## Instructions

1. Read ALL code files in this directory
2. Evaluate each dimension on a 0-100 scale
3. Provide evidence for each score (file:line references)
4. Identify strengths and weaknesses
5. List any anti-patterns found

## Evaluation Dimensions (with weights)

{dimensions_text}

## Output Format

Return a single JSON object (no markdown code blocks):

{{
  "language_detected": "Python/TypeScript/Go/etc",
  "functional_completeness": {{"score": 85, "evidence": "Implements 8/10 requirements. Missing X at file:line"}},
  "correctness_robustness": {{"score": 80, "evidence": "Good error handling at file:line"}},
  "architecture": {{"score": 75, "evidence": "Clean separation at file:line"}},
  "code_quality": {{"score": 80, "evidence": "Readable code, good naming"}},
  "security": {{"score": 70, "evidence": "Input validation at file:line"}},
  "type_safety": {{"score": 85, "evidence": "Strong typing at file:line"}},
  "testing": {{"score": 60, "evidence": "Basic tests at file:line"}},
  "maintainability": {{"score": 75, "evidence": "Modular structure"}},
  "performance": {{"score": 80, "evidence": "Efficient algorithms"}},
  "best_practices": {{"score": 75, "evidence": "Modern patterns used"}},
  "strengths": ["Clean architecture", "Good test coverage"],
  "weaknesses": ["Missing input validation", "No error handling in X"],
  "anti_patterns_found": ["Bare except at file:line", "God class at file:line"]
}}

CRITICAL:
- Output ONLY the JSON object, no other text
- Do NOT wrap in markdown code blocks
- Score each dimension 0-100 based on evidence
- Reference specific files and line numbers
"""

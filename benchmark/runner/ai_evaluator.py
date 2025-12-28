"""AI-powered blind code evaluation using Claude via ccbox."""

from __future__ import annotations

import json
import logging
import random
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

# Path to comparison prompt template
COMPARISON_PROMPT_FILE = "comparison-prompt.md"

# 10 evaluation dimensions with weights
DIMENSIONS = [
    ("functional_completeness", 15),
    ("architecture_design", 12),
    ("code_quality", 12),
    ("robustness", 12),
    ("security", 12),
    ("maintainability", 10),
    ("type_safety", 8),
    ("testing", 7),
    ("performance", 6),
    ("best_practices", 6),
]


@dataclass
class DimensionScore:
    """Score for a single evaluation dimension."""

    score: int = 0
    evidence: str = ""


@dataclass
class VariantResult:
    """Complete evaluation result for one variant."""

    functional_completeness: DimensionScore = field(default_factory=DimensionScore)
    architecture_design: DimensionScore = field(default_factory=DimensionScore)
    code_quality: DimensionScore = field(default_factory=DimensionScore)
    robustness: DimensionScore = field(default_factory=DimensionScore)
    security: DimensionScore = field(default_factory=DimensionScore)
    maintainability: DimensionScore = field(default_factory=DimensionScore)
    type_safety: DimensionScore = field(default_factory=DimensionScore)
    testing: DimensionScore = field(default_factory=DimensionScore)
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
            "architecture_design": {
                "score": self.architecture_design.score,
                "evidence": self.architecture_design.evidence,
            },
            "code_quality": {
                "score": self.code_quality.score,
                "evidence": self.code_quality.evidence,
            },
            "robustness": {
                "score": self.robustness.score,
                "evidence": self.robustness.evidence,
            },
            "security": {
                "score": self.security.score,
                "evidence": self.security.evidence,
            },
            "maintainability": {
                "score": self.maintainability.score,
                "evidence": self.maintainability.evidence,
            },
            "type_safety": {
                "score": self.type_safety.score,
                "evidence": self.type_safety.evidence,
            },
            "testing": {
                "score": self.testing.score,
                "evidence": self.testing.evidence,
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
    winner: str = "tie"
    diff: int = 0
    cco_score: int = 0
    vanilla_score: int = 0


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
    recommendation: str = ""
    blind_assignment: str = ""  # "cco=a" or "cco=b" for transparency
    raw_response: str = ""
    error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON response."""
        return {
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
                        "winner": d.winner,
                        "diff": d.diff,
                        "cco_score": d.cco_score,
                        "vanilla_score": d.vanilla_score,
                    }
                    for d in self.dimension_breakdown
                ],
                "key_differences": self.key_differences,
                "recommendation": self.recommendation,
                "blind_assignment": self.blind_assignment,
            },
            "raw_response": self.raw_response if self.error else None,
            "error": self.error,
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
        architecture_design=parse_dimension_score(data.get("architecture_design", {})),
        code_quality=parse_dimension_score(data.get("code_quality", {})),
        robustness=parse_dimension_score(data.get("robustness", {})),
        security=parse_dimension_score(data.get("security", {})),
        maintainability=parse_dimension_score(data.get("maintainability", {})),
        type_safety=parse_dimension_score(data.get("type_safety", {})),
        testing=parse_dimension_score(data.get("testing", {})),
        performance=parse_dimension_score(data.get("performance", {})),
        best_practices=parse_dimension_score(data.get("best_practices", {})),
        anti_patterns_found=list(data.get("anti_patterns_found", []))[:10],
        overall_score=int(data.get("overall_score", 0)),
        grade=str(data.get("grade", "?")),
        strengths=list(data.get("strengths", []))[:5],
        weaknesses=list(data.get("weaknesses", []))[:5],
    )


def calculate_verdict(cco_score: int, vanilla_score: int) -> tuple[str, str, str]:
    """
    Calculate winner, margin, and verdict from scores.

    Returns:
        (winner, margin, verdict) tuple
    """
    diff = cco_score - vanilla_score

    if abs(diff) < 3:
        return "tie", "negligible", "Essentially Equal"
    elif abs(diff) < 8:
        margin = "slight"
    elif abs(diff) < 15:
        margin = "moderate"
    elif abs(diff) < 25:
        margin = "significant"
    else:
        margin = "decisive"

    if diff > 0:
        winner = "cco"
        if margin == "slight":
            verdict = "Slight CCO Advantage"
        elif margin == "moderate":
            verdict = "Moderate CCO Advantage"
        elif margin == "significant":
            verdict = "Significant CCO Advantage"
        else:
            verdict = "Strong CCO Advantage"
    else:
        winner = "vanilla"
        if margin == "slight":
            verdict = "Slight Vanilla Advantage"
        elif margin == "moderate":
            verdict = "Moderate Vanilla Advantage"
        elif margin == "significant":
            verdict = "Significant Vanilla Advantage"
        else:
            verdict = "Strong Vanilla Advantage"

    return winner, margin, verdict


def parse_ai_response(response: str, cco_is_a: bool) -> AIComparisonResult:
    """
    Parse the AI response JSON into structured result.

    Args:
        response: Raw AI response text
        cco_is_a: If True, implementation_a is CCO; otherwise implementation_b is CCO
    """
    result = AIComparisonResult(raw_response=response)
    result.blind_assignment = "cco=a" if cco_is_a else "cco=b"

    try:
        # Extract JSON from response
        cleaned = response.strip()

        # Remove markdown code blocks if present
        if cleaned.startswith("```"):
            lines = cleaned.split("\n")
            start = 1 if lines[0].startswith("```") else 0
            end = -1 if lines[-1].strip() == "```" else len(lines)
            cleaned = "\n".join(lines[start:end])

        # Find JSON object boundaries
        start_idx = cleaned.find("{")
        end_idx = cleaned.rfind("}") + 1
        if start_idx >= 0 and end_idx > start_idx:
            cleaned = cleaned[start_idx:end_idx]

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

        # Build dimension breakdown
        for dim_name, _ in DIMENSIONS:
            cco_dim = getattr(result.cco, dim_name, DimensionScore())
            vanilla_dim = getattr(result.vanilla, dim_name, DimensionScore())
            cco_score = cco_dim.score
            vanilla_score = vanilla_dim.score
            diff = cco_score - vanilla_score

            if abs(diff) < 3:
                dim_winner = "tie"
            elif diff > 0:
                dim_winner = "cco"
            else:
                dim_winner = "vanilla"

            result.dimension_breakdown.append(
                DimensionComparison(
                    dimension=dim_name,
                    winner=dim_winner,
                    diff=diff,
                    cco_score=cco_score,
                    vanilla_score=vanilla_score,
                )
            )

        # Calculate overall verdict
        result.score_difference = result.cco.overall_score - result.vanilla.overall_score
        result.winner, result.margin, result.verdict = calculate_verdict(
            result.cco.overall_score, result.vanilla.overall_score
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
        result.error = f"Failed to parse AI response as JSON: {e}"
        logger.error(f"JSON parse error: {e}\nResponse: {response[:1000]}")
    except Exception as e:
        result.error = f"Error processing response: {e}"
        logger.error(f"Processing error: {e}")

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
    cco_is_a = random.choice([True, False])

    if cco_is_a:
        dir_a = cco_dir.name
        dir_b = vanilla_dir.name
    else:
        dir_a = vanilla_dir.name
        dir_b = cco_dir.name

    logger.info(f"Blind assignment for {project_id}: A={dir_a}, B={dir_b} (cco_is_a={cco_is_a})")

    # Build the ccbox prompt with blind labels
    ccbox_prompt = f"""You are performing a BLIND code comparison. You do not know which implementation
used any specific tools or processes. Evaluate purely on code quality.

## The Implementations

- **Implementation A**: {dir_a}/
- **Implementation B**: {dir_b}/

## Original Prompt Given to Generate Both

---
{original_prompt}
---

## Evaluation Instructions

{comparison_criteria}
"""

    try:
        # Run ccbox from the output directory in vanilla/bare mode
        cmd = [
            "ccbox",
            "-m",
            "opus",
            "--bare",
            "-p",
            ccbox_prompt,
            "--dangerously-skip-permissions",
        ]

        logger.info(f"Running blind AI comparison for {project_id}")

        proc = subprocess.run(
            cmd,
            cwd=str(output_dir),
            capture_output=True,
            text=True,
            timeout=timeout,
            encoding="utf-8",
            errors="replace",
        )

        if proc.returncode != 0:
            error_msg = proc.stderr[:500] if proc.stderr else "Unknown error"
            return AIComparisonResult(
                error=f"ccbox exited with code {proc.returncode}: {error_msg}",
                raw_response=proc.stdout[:2000] if proc.stdout else "",
            )

        # Parse the response with blind assignment mapping
        result = parse_ai_response(proc.stdout, cco_is_a)

        logger.info(
            f"AI comparison complete for {project_id}: {result.verdict} "
            f"(CCO: {result.cco.overall_score}, Vanilla: {result.vanilla.overall_score}, "
            f"blind={result.blind_assignment})"
        )
        return result

    except subprocess.TimeoutExpired:
        return AIComparisonResult(
            error=f"AI evaluation timed out after {timeout}s. Try again or reduce code size."
        )
    except FileNotFoundError:
        return AIComparisonResult(error="ccbox command not found. Install with: pip install ccbox")
    except Exception as e:
        logger.exception("AI comparison failed")
        return AIComparisonResult(error=f"AI evaluation failed: {e}")

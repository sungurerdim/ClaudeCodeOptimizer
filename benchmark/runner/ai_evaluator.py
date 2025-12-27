"""AI-powered code evaluation using Claude via ccbox (vanilla mode)."""

from __future__ import annotations

import json
import logging
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

# Path to comparison prompt template (relative to benchmark/suite/)
COMPARISON_PROMPT_FILE = "comparison-prompt.md"


@dataclass
class DimensionResult:
    """Result for a single evaluation dimension."""

    score: int = 0
    notes: str = ""


@dataclass
class VariantResult:
    """Complete evaluation result for one variant."""

    prompt_compliance: DimensionResult = field(default_factory=DimensionResult)
    code_quality: DimensionResult = field(default_factory=DimensionResult)
    robustness: DimensionResult = field(default_factory=DimensionResult)
    security: DimensionResult = field(default_factory=DimensionResult)
    best_practices: DimensionResult = field(default_factory=DimensionResult)
    overall_score: int = 0
    grade: str = "?"
    strengths: list[str] = field(default_factory=list)
    weaknesses: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "prompt_compliance": {
                "score": self.prompt_compliance.score,
                "notes": self.prompt_compliance.notes,
            },
            "code_quality": {
                "score": self.code_quality.score,
                "notes": self.code_quality.notes,
            },
            "robustness": {
                "score": self.robustness.score,
                "notes": self.robustness.notes,
            },
            "security": {
                "score": self.security.score,
                "notes": self.security.notes,
            },
            "best_practices": {
                "score": self.best_practices.score,
                "notes": self.best_practices.notes,
            },
            "overall_score": self.overall_score,
            "grade": self.grade,
            "strengths": self.strengths,
            "weaknesses": self.weaknesses,
        }


@dataclass
class AIComparisonResult:
    """Complete AI comparison result."""

    cco: VariantResult = field(default_factory=VariantResult)
    vanilla: VariantResult = field(default_factory=VariantResult)
    winner: str = "tie"
    margin: str = "negligible"
    verdict: str = "Mixed Results"
    key_differences: list[str] = field(default_factory=list)
    recommendation: str = ""
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
                "verdict": self.verdict,
                "key_differences": self.key_differences,
                "recommendation": self.recommendation,
            },
            "raw_response": self.raw_response if self.error else None,
            "error": self.error,
        }


def parse_dimension(data: dict[str, Any]) -> DimensionResult:
    """Parse a dimension result from JSON."""
    return DimensionResult(
        score=int(data.get("score", 0)),
        notes=str(data.get("notes", "")),
    )


def parse_variant(data: dict[str, Any]) -> VariantResult:
    """Parse a variant result from JSON."""
    return VariantResult(
        prompt_compliance=parse_dimension(data.get("prompt_compliance", {})),
        code_quality=parse_dimension(data.get("code_quality", {})),
        robustness=parse_dimension(data.get("robustness", {})),
        security=parse_dimension(data.get("security", {})),
        best_practices=parse_dimension(data.get("best_practices", {})),
        overall_score=int(data.get("overall_score", 0)),
        grade=str(data.get("grade", "?")),
        strengths=list(data.get("strengths", []))[:5],
        weaknesses=list(data.get("weaknesses", []))[:5],
    )


def parse_ai_response(response: str) -> AIComparisonResult:
    """Parse the AI response JSON into structured result."""
    result = AIComparisonResult(raw_response=response)

    try:
        # Try to extract JSON from response
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

        # Parse variants
        if "cco" in data:
            result.cco = parse_variant(data["cco"])
        if "vanilla" in data:
            result.vanilla = parse_variant(data["vanilla"])

        # Parse comparison
        comp = data.get("comparison", {})
        result.winner = comp.get("winner", "tie")
        result.margin = comp.get("margin", "negligible")
        result.verdict = comp.get("verdict", "Mixed Results")
        result.key_differences = comp.get("key_differences", [])[:5]
        result.recommendation = comp.get("recommendation", "")

        # Clear raw_response on success to save space
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
    Run AI comparison using ccbox vanilla mode.

    Args:
        project_id: The project identifier
        output_dir: Path to benchmark/suite/output
        suite_dir: Path to benchmark/suite
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

    # Verify comparison prompt exists
    comparison_prompt_path = suite_dir / COMPARISON_PROMPT_FILE
    if not comparison_prompt_path.exists():
        return AIComparisonResult(error=f"Comparison prompt not found: {comparison_prompt_path}")

    # Build the ccbox prompt
    # ccbox will be run from the output directory so it can access both variant folders
    ccbox_prompt = f"""Compare the two code implementations in these directories:
- CCO variant: {cco_dir.name}/
- Vanilla variant: {vanilla_dir.name}/

Original prompt that was given to generate both:
---
{original_prompt}
---

Evaluate according to the criteria in {comparison_prompt_path.name} and return the JSON response format specified there.
"""

    try:
        # Run ccbox from the output directory
        # Using -p flag to pass the prompt directly
        cmd = ["ccbox", "-p", ccbox_prompt, "--dangerously-skip-permissions"]

        logger.info(f"Running AI comparison for {project_id}")
        logger.debug(f"Command: {' '.join(cmd[:3])}...")

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
                raw_response=proc.stdout[:1000] if proc.stdout else "",
            )

        # Parse the response
        result = parse_ai_response(proc.stdout)
        logger.info(
            f"AI comparison complete: {result.winner} "
            f"(CCO: {result.cco.overall_score}, Vanilla: {result.vanilla.overall_score})"
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

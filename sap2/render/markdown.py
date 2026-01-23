"""
sap2/render/markdown.py

Markdown rendering for SAP² outputs.

Presentation-only:
- No applicability logic
- No decoding logic
- No heuristics

Consumes already-computed artifacts and prints a human-readable report.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping


def write_markdown(path: str | Path, text: str) -> Path:
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")
    return out.resolve()


def render_pipeline_run(
    run: Any,
    *,
    title: str = "SAP² Report",
) -> str:
    """
    Render a PipelineRunResult-like object.

    We intentionally avoid tight coupling: we access attributes conservatively.
    Expected fields on `run`:
      - sat_source: str
      - matrix_schema_version: str
      - channels: Dict[channel_name, PipelineChannelResult-like]

    Expected fields on channel result:
      - applicability: Dict[method_id, ApplicabilityReport-like]
      - experiments: Dict[method_id, ExperimentResult-like]
    """
    lines: list[str] = []
    lines.append(f"# {title}")
    lines.append("")

    sat_source = getattr(run, "sat_source", None)
    matrix_ver = getattr(run, "matrix_schema_version", None)

    if sat_source is not None:
        lines.append(f"- SAT source: `{sat_source}`")
    if matrix_ver is not None:
        lines.append(f"- Matrix schema_version: `{matrix_ver}`")
    if sat_source is not None or matrix_ver is not None:
        lines.append("")

    channels = getattr(run, "channels", {}) or {}
    if not channels:
        lines.append("_No channels produced._")
        lines.append("")
        return "\n".join(lines)

    for channel_name, ch in channels.items():
        lines.append(f"## Channel: {channel_name}")
        lines.append("")

        reports = getattr(ch, "applicability", {}) or {}
        experiments = getattr(ch, "experiments", {}) or {}

        if reports:
            lines.append("### Applicability")
            lines.append("")
            lines.append("| method_id | status | missing_required | unstable_required |")
            lines.append("|---|---:|---:|---:|")

            for method_id in sorted(reports.keys()):
                rep = reports[method_id]
                status = _get(rep, "status", "?")
                # Use correct field names from ApplicabilityReport
                missing = _len(_get(rep, "missing_inputs", {}))
                unstable = _len(_get(rep, "unstable_inputs", {}))
                lines.append(f"| `{method_id}` | `{status}` | {missing} | {unstable} |")

            lines.append("")
        else:
            lines.append("_No applicability reports._")
            lines.append("")

        if experiments:
            lines.append("### Experiments")
            lines.append("")
            lines.append("| method_id | status | diagnostics |")
            lines.append("|---|---:|---|")

            for method_id in sorted(experiments.keys()):
                exp = experiments[method_id]
                status = _get(exp, "status", "?")
                diags = _get(exp, "diagnostics", [])
                diag_str = "; ".join(str(d) for d in diags) if diags else ""
                lines.append(f"| `{method_id}` | `{status}` | {diag_str} |")

            lines.append("")

            # Hypotheses summary (cross-decoder)
            hyp_lines = _render_hypotheses_summary(experiments)
            if hyp_lines:
                lines.append("### Hypotheses Summary")
                lines.append("")
                lines.extend(hyp_lines)
        else:
            lines.append("_No experiments executed._")
            lines.append("")

    return "\n".join(lines)


def _render_hypotheses_summary(experiments: Mapping[str, Any]) -> list[str]:
    """
    Render a cross-decoder hypotheses summary.

    Expects each ExperimentResult to optionally expose:
      exp.artifacts["hypotheses"] : List[Dict]

    Presentation-only: no new decoding or scoring is performed.
    """
    lines: list[str] = []

    for method_id in sorted(experiments.keys()):
        exp = experiments[method_id]
        artifacts = _get(exp, "artifacts", {}) or {}
        hypotheses = artifacts.get("hypotheses")

        if not hypotheses:
            continue

        lines.append(f"**{method_id}**")

        # Limit to top 3 hypotheses to keep report readable
        for idx, h in enumerate(hypotheses[:3], start=1):
            level = h.get("level", "?")
            rep = h.get("representation", "")
            scores = h.get("scores", {}) or {}
            params = h.get("parameters", {}) or {}
            notes = h.get("notes", []) or []

            # Pick one primary score if available (deterministic choice: first key sorted)
            score_str = ""
            if scores:
                k = sorted(scores.keys())[0]
                try:
                    score_str = f"{k}={float(scores[k]):.3f}"
                except Exception:
                    score_str = f"{k}={scores[k]}"

            preview = str(rep).replace("\n", " ")
            if len(preview) > 80:
                preview = preview[:77] + "..."

            lines.append(f"- Hypothesis #{idx} [{level}]" + (f" ({score_str})" if score_str else ""))
            lines.append(f"  - preview: `{preview}`")

            if params:
                param_str = ", ".join(f"{k}={v}" for k, v in params.items())
                lines.append(f"  - parameters: {param_str}")

            if notes:
                lines.append(f"  - notes: {', '.join(str(n) for n in notes)}")

        lines.append("")

    return lines


def _get(obj: Any, key: str, default: Any) -> Any:
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


def _len(x: Any) -> int:
    try:
        return len(x)
    except Exception:
        return 0

"""
sap2/render/markdown.py

Markdown rendering helpers for SAP² outputs.

This module must remain presentation-only:
- no applicability logic
- no decoding logic
- no heuristics

It produces a human-readable report from already-computed artifacts.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, Mapping, Optional


def write_markdown(path: str | Path, text: str) -> Path:
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")
    return out.resolve()


def render_report(
    *,
    title: str,
    sat_source: Optional[str] = None,
    matrix_schema_version: Optional[str] = None,
    applicability_by_channel: Mapping[str, Mapping[str, Any]],
    experiments_by_channel: Optional[Mapping[str, Mapping[str, Any]]] = None,
) -> str:
    """
    Render a human-readable report.

    Inputs are intentionally generic mappings so this renderer does not couple tightly
    to a specific PipelineRunResult shape (which you may still be stabilizing).

    Expected mapping contents:
    - applicability_by_channel[channel][method_id] = ApplicabilityReport-like object (or dict)
    - experiments_by_channel[channel][method_id] = ExperimentResult-like object (or dict)
    """
    lines: list[str] = []
    lines.append(f"# {title}")
    lines.append("")

    if sat_source is not None:
        lines.append(f"- SAT source: `{sat_source}`")
    if matrix_schema_version is not None:
        lines.append(f"- Matrix schema_version: `{matrix_schema_version}`")
    if sat_source is not None or matrix_schema_version is not None:
        lines.append("")

    experiments_by_channel = experiments_by_channel or {}

    for channel, reports in applicability_by_channel.items():
        lines.append(f"## Channel: {channel}")
        lines.append("")

        if not reports:
            lines.append("_No applicability reports._")
            lines.append("")
            continue

        # Applicability summary table
        lines.append("| method_id | status | required_missing | required_unstable |")
        lines.append("|---|---:|---:|---:|")

        for method_id, rep in sorted(reports.items(), key=lambda x: x[0]):
            status = _get(rep, "status", default="?")
            missing = _len(_get(rep, "missing_required", default=[]))
            unstable = _len(_get(rep, "unstable_required", default=[]))
            lines.append(f"| `{method_id}` | `{status}` | {missing} | {unstable} |")

        lines.append("")

        # Experiments (if any)
        exp_for_channel: Dict[str, Any] = dict(experiments_by_channel.get(channel, {}) or {})
        if exp_for_channel:
            lines.append("### Experiments")
            lines.append("")
            lines.append("| method_id | status | diagnostics |")
            lines.append("|---|---:|---|")

            for method_id, exp in sorted(exp_for_channel.items(), key=lambda x: x[0]):
                status = _get(exp, "status", default="?")
                diags = _get(exp, "diagnostics", default=[])
                diag_str = "; ".join(str(d) for d in diags) if diags else ""
                lines.append(f"| `{method_id}` | `{status}` | {diag_str} |")

            lines.append("")

    return "\n".join(lines)


def _get(obj: Any, key: str, default: Any) -> Any:
    """
    Extract a field from either a dict-like object or a dataclass-like object.
    """
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


def _len(x: Any) -> int:
    try:
        return len(x)
    except Exception:
        return 0

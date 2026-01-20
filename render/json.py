"""
sap2/render/json.py

JSON rendering helpers for SAP² outputs.

This module must remain presentation-only:
- no applicability logic
- no decoding logic
- no heuristics

It focuses on robust serialization of dataclasses and enums.
"""

from __future__ import annotations

import json
from dataclasses import is_dataclass, asdict
from enum import Enum
from pathlib import Path
from typing import Any, Mapping, Sequence


def to_jsonable(obj: Any) -> Any:
    """
    Convert common SAP² objects (dataclasses, enums, paths) into JSON-serializable structures.

    This function is deliberately conservative:
    - It never invents values.
    - It only transforms representation.
    """
    if obj is None:
        return None

    if isinstance(obj, (str, int, float, bool)):
        return obj

    if isinstance(obj, Path):
        return str(obj)

    if isinstance(obj, Enum):
        return obj.value

    if is_dataclass(obj):
        # asdict recursively converts nested dataclasses, but may keep Enums; post-process after.
        return to_jsonable(asdict(obj))

    if isinstance(obj, Mapping):
        return {str(k): to_jsonable(v) for k, v in obj.items()}

    if isinstance(obj, (list, tuple)):
        return [to_jsonable(v) for v in obj]

    if isinstance(obj, Sequence) and not isinstance(obj, (str, bytes, bytearray)):
        return [to_jsonable(v) for v in obj]

    # Fallback: last-resort string representation (explicit and inspectable)
    return str(obj)


def write_json(path: str | Path, payload: Any, *, indent: int = 2) -> Path:
    """
    Write a JSON file to `path`.

    Returns the resolved Path to the written file.
    """
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)

    data = to_jsonable(payload)

    with out.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=indent, sort_keys=True)

    return out.resolve()


def write_json_bundle(output_dir: str | Path, name: str, payload: Any) -> Path:
    """
    Convenience helper: writes <output_dir>/<name>.json
    """
    output_dir = Path(output_dir)
    return write_json(output_dir / f"{name}.json", payload)

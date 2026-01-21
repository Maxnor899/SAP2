#!/usr/bin/env python3
"""
SAP² entry point.

Runs the SAP² pipeline end-to-end and exports results
(JSON + Markdown).

This script contains:
- configuration (paths, parameters)
- no logic
"""

from pathlib import Path

from sap2.applicability.params import ApplicabilityParams
from sap2.engine.export import run_and_export


def main() -> None:
    # --- Paths ---
    root = Path(__file__).parent

    sat_path = root / "results.json"        # or wherever your SAT results live
    matrices_dir = root / "matrices"        # directory with _index.yaml etc.
    out_dir = root / "out"

    # --- Applicability parameters ---
    params = ApplicabilityParams(
        min_event_count=3,
        min_interval_count=3,
        min_symbol_count=5,
        min_vector_length=10,
        min_matrix_shape=(2, 2),
        require_relation_pairs=True,
    )

    # --- Optional decoder parameters ---
    decoder_params_by_method = {
        # "duration_based_morse_like": {
        #     "dot_max": 0.12,
        #     "dash_min": 0.20,
        # }
    }

    run_and_export(
        sat_path=sat_path,
        matrices_dir=matrices_dir,
        params=params,
        out_dir=out_dir,
        decoder_params_by_method=decoder_params_by_method,
        report_title="SAP² Analysis Report",
    )


if __name__ == "__main__":
    main()

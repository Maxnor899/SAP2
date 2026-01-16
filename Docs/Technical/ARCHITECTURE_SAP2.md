# SAP² — Architecture

## Purpose of this document

This document defines the **software architecture** of SAP² (Small Audio Post-Processor).

It explains:
- the intended module boundaries,
- the data contracts between components,
- the execution pipeline,
- and the constraints that preserve methodological rigor.

This is an architecture document, not an implementation guide.

---

## 1. Core idea

SAP² operates **only on measurements** produced by upstream tools (primarily Small Audio Toolkit / SAT).

SAP² is responsible for:
1. Loading structured measurement outputs (`results.json` and optionally `config_used.json`)
2. Building **typed intermediate inputs** (the “input grammar”)
3. Checking **structural applicability** of decoding methods
4. Attempting decoding **only when justified**
5. Producing transparent outputs (reports + machine-readable artifacts)

SAP² does not:
- process raw audio,
- generate measurements,
- infer meaning or intent.

---

## 2. Separation of concerns

SAP² is designed around strict separation of responsibilities:

- **I/O**: load, validate, normalize inputs
- **Model**: typed in-memory representations of SAT results and SAP² inputs
- **Grammar builders**: construct input families (E, Δ, S, V, M, R)
- **Applicability**: decide whether a decoding method can be attempted (with reasons)
- **Decoders**: attempt decoding, producing experiments and diagnostics
- **Engine**: orchestrate the pipeline and enforce ordering
- **Render**: produce reports and exports
- **Tests**: verify contracts, reproducibility, and refusal cases

No component should “reach across” layers.

---

## 3. Repository layout

Recommended layout (Python package `sap2`):

```
SAP2/
├── README.md
├── docs/
│   └── (documentation set)
├── pyproject.toml
├── sap2/
│   ├── __init__.py
│   ├── cli.py
│   ├── io/
│   │   ├── load_sat.py
│   │   └── validation.py
│   ├── model/
│   │   ├── sat_results.py
│   │   ├── inputs.py
│   │   ├── applicability.py
│   │   └── experiments.py
│   ├── grammar/
│   │   ├── registry.py
│   │   └── builders/
│   │       ├── events.py
│   │       ├── intervals.py
│   │       ├── symbols.py
│   │       ├── vectors.py
│   │       ├── matrices.py
│   │       └── relations.py
│   ├── applicability/
│   │   ├── matrix.py
│   │   ├── checks.py
│   │   └── diagnostics.py
│   ├── decoders/
│   │   ├── base.py
│   │   ├── registry.py
│   │   └── (decoders live here)
│   ├── engine/
│   │   ├── pipeline.py
│   │   ├── provenance.py
│   │   └── experiment_runner.py
│   └── render/
│       ├── markdown.py
│       └── json.py
└── tests/
    └── (unit tests)
```

The exact file names can change, but the **boundaries must remain**.

---

## 4. Data model contracts

### 4.1 `SatResults` (normalized measurement input)

`SatResults` is a typed representation of the upstream `results.json`.

Minimum responsibilities:
- hold metadata (sample rate, channels, duration, tool version if available)
- expose method results by name and channel
- provide a stable access API even if SAT output evolves

It should support both:
- `path/to/results.json`
- `path/to/output_dir/` (where results.json is found inside)

### 4.2 `InputBundle` (SAP² input grammar instance)

`InputBundle` aggregates the six input families:

- **E** (events)
- **Δ** (intervals/durations)
- **S** (symbol streams)
- **V** (feature vectors / stats)
- **M** (matrices / fields)
- **R** (relations / inter-channel)

Each family must support explicit states:
- **present** with data
- **missing** with a reason
- **ambiguous/unstable** with diagnostics

### 4.3 `ApplicabilityReport`

For a given decoder candidate:

- `status`: one of
  - `applicable`
  - `missing_inputs`
  - `underconstrained`
  - `ambiguous`
  - `not_applicable`
- `required_inputs`: set of grammar families
- `reasons`: list of factual reasons
- `supporting_metrics`: optional numeric evidence (no scores)

### 4.4 `ExperimentResult`

Represents a decoding attempt:

- decoder name + version
- parameters used
- inputs referenced (provenance)
- output artifacts (symbol streams, frames, bits, etc.)
- diagnostics (instability, sensitivity, failure explanations)
- outcome classification:
  - `produced_output`
  - `failed_cleanly`
  - `aborted_not_applicable`

No experiment result may claim semantic meaning.

---

## 5. Pipeline (execution order)

SAP² enforces a strict pipeline:

1. **Load**
   - load `results.json` (+ optional `config_used.json`)
   - normalize to `SatResults`
2. **Build inputs**
   - run grammar builders to produce `InputBundle`
3. **Check applicability**
   - for each decoder, compute `ApplicabilityReport`
4. **Attempt decoding**
   - only for `applicable` (and optionally `underconstrained` if user forces)
5. **Render outputs**
   - write machine artifacts + a human report

The pipeline must be deterministic given the same inputs and parameters.

---

## 6. Plugin registries

Two registries are central to extensibility:

### 6.1 Grammar builder registry

- builders declare which family they produce (E/Δ/S/V/M/R)
- builders declare which SAT measurements they require
- builders return a `BuildResult` (present/missing/unstable + provenance)

### 6.2 Decoder registry

- decoders declare required input families
- each decoder implements:
  - `applicable(bundle) -> ApplicabilityReport`
  - `decode(bundle, params) -> ExperimentResult`

Decoders must not generate missing inputs.
They may only refuse or proceed with explicit assumptions.

---

## 7. CLI (minimum viable interface)

A minimal CLI should support:

- `sap2 run <path>`
  - where `<path>` is `results.json` or a SAT output directory
- options:
  - `--out <dir>` output directory
  - `--only <decoder1,decoder2>` restrict to a subset
  - `--channels <left,right,difference>` restrict channels
  - `--force` allow running `underconstrained` experiments (explicitly marked)

The CLI must never hide assumptions.

---

## 8. Output structure

Suggested output layout:

```
sap2_output/
├── inputs/
│   ├── events.json
│   ├── intervals.json
│   ├── symbols.json
│   ├── vectors.json
│   ├── matrices.meta.json
│   └── relations.json
├── applicability.json
├── experiments.json
└── report.md
```

Notes:
- exporting full matrices may be expensive; metadata-only is acceptable initially.
- every exported artifact should include provenance fields.

---

## 9. Testing strategy

SAP² should be tested primarily on **contracts and refusal behavior**.

Recommended test categories:

- loading/normalization of SAT outputs
- builders produce correct present/missing states
- applicability matrix consistency (required inputs enforced)
- decoders never run when required inputs are missing
- deterministic outputs given fixed inputs and parameters
- regression tests on known SAT results fixtures

Tests should prefer small fixtures to avoid heavy runtime.

---

## 10. Non-goals (architectural constraints)

Architecture must explicitly prevent:

- decoding without applicability checks
- hidden scoring or probability labels
- semantic interpretation
- SAT coupling (no SAT imports or runtime dependency required)

SAP² may be compatible with SAT outputs, but must remain logically independent.

---

## 11. Future integration (optional)

A later, optional integration may add a SAT-side helper that:
- generates SAT protocols to produce inputs needed by specific SAP² decoders

This must remain a separate tool or optional module to preserve SAT neutrality.

---

## Summary

SAP² is a two-stage reasoning system built on top of measurement outputs:

- **SAT measures**
- **SAP² builds typed inputs**
- **SAP² checks applicability**
- **SAP² attempts decoding as constrained experiments**
- **SAP² reports outcomes and limits**

The architecture enforces methodological boundaries by construction.

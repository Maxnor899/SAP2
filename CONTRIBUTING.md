# Contributing to SAP² (Small Audio Post-Processor)

Thank you for your interest in contributing to SAP².

SAP² is a **research-oriented, methodology-first** project. Its goal is to reason about the
**structural decodability** of audio-derived measurements, strictly separated from
interpretation, meaning, or intent.

Before contributing, please make sure you understand and accept the project's philosophical
and methodological constraints.

---

## 1. Core principles (non-negotiable)

By contributing to SAP², you agree to respect the following principles:

### Measurement is not interpretation
- SAP² never processes raw audio.
- SAP² operates only on measured outputs (typically `results.json`).
- No contribution may infer meaning, intent, or message content.

### Decodability is structural
- Decoding is considered only as a *structural compatibility problem*.
- Absence of decodability is a valid and expected outcome.
- Ambiguity must be reported, never resolved implicitly.

### Known methods only
- All decoding methods must be documented, historically used, or academically described.
- Speculative, narrative, or ad-hoc decoding approaches are out of scope.

### Explicit assumptions
- All thresholds, parameters, and assumptions must be explicit.
- No hidden heuristics, no magic numbers, no silent fallbacks.

### Human interpretation stays external
- SAP² does not automate interpretation.
- Any meaning derived from outputs is a human responsibility, outside the tool.

Contributions that violate these principles will be rejected.

---

## 2. What you can contribute

Valid contributions include:

- Bug fixes
- Improvements to architectural clarity
- Grammar builders (E, Δ, S, V, M, R), with explicit provenance
- Applicability checks and diagnostics
- Decoders implemented as **constrained experiments**
- Documentation improvements
- Tests that strengthen refusal, failure, and non-result cases

---

## 3. What you must NOT contribute

The following are explicitly out of scope:

- Automatic message detection
- Claims of hidden communication
- Probabilistic intent inference
- Semantic or narrative interpretation
- Ranking or scoring of decoding results
- “This probably means…” logic

If in doubt: **don’t guess — refuse or document uncertainty**.

---

## 4. Architectural discipline

All contributions must respect the documented SAP² architecture:

- One module, one responsibility
- Clear separation between I/O, grammar, applicability, decoding, and rendering
- No coupling with SAT runtime logic
- Deterministic behavior given fixed inputs and parameters

Code that breaks architectural boundaries will be rejected, even if it “works”.

---

## 5. Code quality requirements

SAP² prioritizes clarity and traceability over cleverness.

### Mandatory rules
- Readability over conciseness
- Explicit variable and function names
- No magic numbers
- Defensive input validation
- Clear error messages explaining *why* processing stops

### Comments
- Non-trivial logic must be commented
- Comments explain **why**, not just **what**
- Methodological choices must be justified

### Style
- Follow consistent style (e.g. PEP 8 for Python)
- One file, one responsibility
- Favor composition over inheritance

---

## 6. Tests and reproducibility

Contributions should include tests when applicable.

Tests should focus on:
- Input validation
- Presence / absence / ambiguity of inputs
- Applicability refusal behavior
- Deterministic outputs
- Regression protection

Silent failures are not acceptable.

---

## 7. Pull request guidelines

When opening a pull request:

- Clearly state **what problem** is addressed
- Explain **why** the change respects SAP² methodology
- Document assumptions and limitations
- Reference relevant documentation files if applicable

PRs that blur measurement, reasoning, and interpretation will be rejected.

---

## 8. Issue reporting

When opening an issue:

- Be explicit about observed behavior
- Provide minimal reproducible inputs if possible
- Distinguish bugs from methodological limitations

Remember: “no result” is often the correct result.

---

## 9. Final note

SAP² is designed to **fail clearly and honestly**.

Contributions are valued not for producing results,
but for strengthening methodological rigor.

If your change makes SAP² more cautious, more explicit,
or better at refusing unsupported conclusions,
you are probably going in the right direction.

Thank you for contributing responsibly.

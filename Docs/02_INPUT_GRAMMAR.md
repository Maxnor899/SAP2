# SAP² — Input Grammar

## Purpose of this document

This document defines the **formal grammar of inputs** used by SAP².

It describes the **types of observable structures** that decoding methods may require,
independently of any specific signal, protocol, or interpretation.

The goal is to establish a **shared vocabulary** between:
- decoding methods,
- analysis results (`results.json`),
- and upstream observation protocols.

This grammar describes **forms**, not meanings.

---

## Design principles

The input grammar follows a small number of strict principles:

- Inputs are **observable**, not inferred.
- Inputs are **typed** and **explicitly defined**.
- Inputs are **independent of interpretation**.
- Inputs may be **incomplete, ambiguous, or absent**.
- Absence of an input is a valid state.

---

## Overview of input families

SAP² groups all possible decoding inputs into six fundamental families:

1. Event-based inputs  
2. Interval and duration inputs  
3. Symbolic sequence inputs  
4. Vector and statistical inputs  
5. Matrix and field inputs  
6. Relational and inter-channel inputs  

Each family is described below with its formal properties.

---

## 1. Event-based inputs

### Definition

An **event** is a discrete occurrence localized in time.

Events may originate from:
- pulse detection
- threshold crossings
- transient detection
- segmentation boundaries

### Canonical form

```
E = {t₁, t₂, t₃, …}
```

Where each `tᵢ` is a time index (samples or seconds).

### Required properties

- strict temporal ordering
- known time reference
- explicit origin (how the event was detected)

### Notes

Events carry **no semantic meaning**.
They only indicate *that something happened at a given time*.

---

## 2. Interval and duration inputs

### Definition

An **interval** is the temporal distance between two events.

### Canonical form

```
Δ = {t₂ − t₁, t₃ − t₂, …}
```

Intervals may be expressed:
- in samples
- in seconds
- as normalized ratios

### Required properties

- consistent unit
- defined reference if normalized
- stability assessment when possible

### Notes

Many decoding methods rely on **relative durations**, not absolute ones.

---

## 3. Symbolic sequence inputs

### Definition

A **symbolic sequence** is a discretized representation of events or intervals.

### Canonical form

```
S = [s₁, s₂, s₃, …]
```

Where each `sᵢ` belongs to a finite alphabet.

### Examples

- binary symbols: `{0, 1}`
- duration classes: `{short, long}`
- categorical labels: `{A, B, C}`

### Required properties

- explicit discretization rule
- documented thresholds or clustering method
- reversible mapping when possible

### Notes

Symbolic sequences do **not** imply language, encoding, or intent.

---

## 4. Vector and statistical inputs

### Definition

A **vector input** represents a set of numerical descriptors associated with a region,
band, or segment.

### Canonical form

```
V = [v₁, v₂, …, vₙ]
```

### Examples

- energy per frequency band
- entropy values
- modulation indices
- stability scores

### Required properties

- defined dimensionality
- measurement units
- aggregation method (mean, median, distribution)

### Notes

These inputs describe **spaces of variation**, not symbols.

---

## 5. Matrix and field inputs

### Definition

A **matrix input** represents structured data varying along two or more axes.

### Canonical form

```
M(t, f)
```

### Examples

- spectrograms (STFT)
- constant-Q transforms
- time–frequency stability maps

### Required properties

- axis definitions
- resolution parameters
- normalization rules

### Notes

Patterns in matrices are **observations**, not messages.

---

## 6. Relational and inter-channel inputs

### Definition

A **relational input** describes relationships between multiple signals or components.

### Examples

- cross-correlation
- phase difference
- time delay between channels
- L − R difference signals

### Required properties

- reference channels
- symmetry or asymmetry definition
- temporal or spectral alignment

### Notes

Relational inputs are especially sensitive to configuration choices.

---

## Absence and ambiguity

SAP² explicitly recognizes that:

- an expected input may be absent,
- an input may exist but be unstable,
- multiple incompatible inputs may coexist.

These states must be represented explicitly.

Ambiguity is **not resolved automatically**.

---

## Relation to decoding methods

Each decoding method described in `01_DECODING_METHODS.md`:
- requires a specific subset of these input families,
- imposes constraints on their properties,
- may reject ambiguous or insufficient inputs.

The mapping between methods and inputs is formalized in the next document.

---

## Summary

This grammar defines **what can be observed and described**,
not what should be decoded.

By constraining the form of inputs,
SAP² constrains the space of plausible decoding attempts.

Meaning remains outside the scope of this document.

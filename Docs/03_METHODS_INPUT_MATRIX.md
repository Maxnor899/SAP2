# SAP² — Decoding Methods ↔ Input Matrix

## Purpose of this document

This document establishes a **formal mapping between decoding methods and required input types**,
as defined in `01_DECODING_METHODS.md` and `02_INPUT_GRAMMAR.md`.

Its role is to make explicit:
- which input families are **required**,
- which are **optional**,
- and which are **not applicable**
for each decoding method.

This matrix is **descriptive**, not prescriptive.
It does not imply that a method *should* be applied — only whether it *can be considered*.

---

## Reading the matrix

Each decoding method is evaluated against the following input families:

- **E** — Event-based inputs  
- **Δ** — Interval / duration inputs  
- **S** — Symbolic sequences  
- **V** — Vector / statistical inputs  
- **M** — Matrix / field inputs  
- **R** — Relational / inter-channel inputs  

Legend:
- **R** = Required  
- **O** = Optional  
- **–** = Not applicable  

---

## I. Time-domain decoding methods

| Method                               | E | Δ | S | V | M | R |
|--------------------------------------|---|---|---|---|---|---|
| Duration-based (Morse-like)           | R | R | O | – | – | – |
| Pulse presence / absence              | R | O | R | – | – | – |
| Pulse duration binary                 | R | R | R | – | – | – |
| Temporal ratio encoding               | R | R | O | – | – | – |
| Frame-based temporal encoding         | R | R | O | – | – | – |
| Clock + data temporal encoding        | R | R | O | – | – | – |

---

## II. Frequency-domain decoding methods

| Method                               | E | Δ | S | V | M | R |
|--------------------------------------|---|---|---|---|---|---|
| Frequency presence (FSK-like)         | – | – | O | R | O | – |
| Frequency displacement                | – | – | O | R | O | – |
| Harmonic structure encoding           | – | – | – | R | O | – |
| Spectral stability encoding           | – | – | – | R | R | – |

---

## III. Time–frequency decoding methods

| Method                               | E | Δ | S | V | M | R |
|--------------------------------------|---|---|---|---|---|---|
| STFT pattern encoding                | – | – | – | O | R | – |
| Multi-band temporal encoding          | R | R | O | R | O | – |
| Multi-scale (wavelet) encoding        | – | – | – | O | R | – |

---

## IV. Modulation-based decoding methods

| Method                               | E | Δ | S | V | M | R |
|--------------------------------------|---|---|---|---|---|---|
| Amplitude modulation (AM)             | O | R | O | R | – | – |
| Frequency modulation (FM)             | O | R | O | R | – | – |
| Phase modulation                      | – | – | O | R | – | R |

---

## V. Inter-channel decoding methods

| Method                               | E | Δ | S | V | M | R |
|--------------------------------------|---|---|---|---|---|---|
| Left–right difference encoding        | – | – | – | R | O | R |
| Inter-channel time delay              | R | R | – | O | – | R |
| Inter-channel phase encoding          | – | – | – | O | – | R |

---

## VI. Statistical and residual approaches

| Method                               | E | Δ | S | V | M | R |
|--------------------------------------|---|---|---|---|---|---|
| Entropy-based encoding                | – | – | – | R | O | – |
| Redundancy / compressibility encoding | – | – | – | R | – | – |
| Residual / noise-floor encoding       | – | – | – | O | O | – |

---

## Interpretation constraints

This matrix **does not imply**:
- that required inputs are present,
- that inputs are sufficient,
- that decoding will succeed.

It only defines **structural compatibility**.

Multiple methods may appear compatible simultaneously.
No ranking or selection is performed automatically.

---

## Relation to upstream analysis

This matrix allows one to:

- identify which **SAT analyses** are needed to produce inputs,
- design **observation protocols** accordingly,
- explain why certain decoding methods are excluded.

It acts as a bridge between **measurement design** and **decoding reasoning**.

---

## Summary

This matrix formalizes the relationship between:
- known decoding methods,
- and observable input structures.

By making requirements explicit,
SAP² reduces speculative decoding attempts
and enforces methodological clarity.

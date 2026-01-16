# SAP² — Decoding Methods Catalog

## Purpose of this document

This document provides a **structured and exhaustive overview of known audio decoding methods**
that are documented in technical literature, telecommunications practice, watermarking research,
and historical usage.

This catalog does **not** describe implementations.
It does **not** claim applicability.
It does **not** imply the presence of encoded content.

Its sole purpose is to enumerate **what decoding approaches exist**,
so that their **input requirements** can later be formalized.

---

## Scope and constraints

Only methods that satisfy at least one of the following criteria are included:

- documented in signal processing or telecommunications literature
- historically used in real communication systems
- formally described in watermarking or steganography research
- reducible to explicit, testable input structures

Speculative, narrative, or purely interpretative approaches are explicitly excluded.

---

## I. Time-domain decoding methods

### 1. Duration-based encoding (Morse-like)

**Principle**  
Information is encoded in the **relative duration** of events and silences.

**Examples**
- Morse code
- short / long pulse systems
- rhythmic signaling

**Typical carriers**
- pulse trains
- amplitude envelope crossings
- silence segmentation

---

### 2. Pulse presence / absence encoding

**Principle**  
Information is encoded as the **presence or absence of an event** within a fixed temporal window.

**Examples**
- simple binary pulse systems
- impulse-based signaling

**Typical carriers**
- transient detection
- thresholded envelopes

---

### 3. Pulse duration binary encoding

**Principle**  
Binary states are encoded using **different pulse lengths**.

**Examples**
- long pulse = 1, short pulse = 0
- inverted mappings

---

### 4. Temporal ratio encoding

**Principle**  
Information is encoded in **ratios between consecutive durations**, not absolute time.

**Properties**
- robust to tempo changes
- invariant under time scaling

---

### 5. Frame-based temporal encoding

**Principle**  
Signals are structured into **repeating temporal frames** containing data fields.

**Examples**
- simple framing protocols
- beacon-style transmissions

---

### 6. Clock + data temporal encoding

**Principle**  
A stable temporal reference (clock) exists alongside data events aligned to it.

**Examples**
- Manchester-like encoding
- NRZ-like signaling

---

## II. Frequency-domain decoding methods

### 7. Frequency presence encoding (FSK-like)

**Principle**  
Information is encoded by the **presence of specific frequencies**.

**Examples**
- Frequency Shift Keying (FSK)
- multi-tone signaling

---

### 8. Frequency displacement encoding

**Principle**  
Small, controlled **frequency shifts** carry information.

**Common use**
- audio watermarking

---

### 9. Harmonic structure encoding

**Principle**  
Information is encoded in **harmonic relationships** rather than absolute frequencies.

---

### 10. Spectral stability encoding

**Principle**  
Persistent, unusually stable frequency bands act as carriers.

---

## III. Time–frequency decoding methods

### 11. STFT pattern encoding

**Principle**  
Information appears as **spatio-temporal patterns** in spectrograms.

**Common use**
- modern watermarking schemes

---

### 12. Multi-band temporal encoding

**Principle**  
Separate frequency bands each carry **independent temporal sequences**.

---

### 13. Multi-scale (wavelet) encoding

**Principle**  
Information is distributed across **multiple time scales**.

---

## IV. Modulation-based decoding methods

### 14. Amplitude modulation (AM) encoding

**Principle**  
Information is carried by **slow variations of amplitude**.

---

### 15. Frequency modulation (FM) encoding

**Principle**  
Information is carried by **slow variations of instantaneous frequency**.

---

### 16. Phase modulation encoding

**Principle**  
Information is carried by **phase variations**, often imperceptible.

---

## V. Inter-channel decoding methods

### 17. Left–right difference encoding

**Principle**  
Information is encoded in the **difference between channels**.

---

### 18. Inter-channel time delay encoding

**Principle**  
Controlled delays between channels carry information.

---

### 19. Inter-channel phase encoding

**Principle**  
Relative phase relationships between channels act as carriers.

---

## VI. Statistical and residual decoding approaches

### 20. Entropy-based encoding

**Principle**  
Information is represented by **changes in local entropy**.

---

### 21. Redundancy / compressibility encoding

**Principle**  
Information appears as variations in **compressibility**.

---

### 22. Residual / noise-floor encoding

**Principle**  
Information is embedded in **residual signals** after subtraction or filtering.

---

## Important note

This catalog does **not** imply that any of these methods are applicable to a given signal.

Applicability depends entirely on:
- the availability of required inputs,
- the stability of observed structures,
- and explicit methodological assumptions.

These questions are addressed in subsequent documents.

---

## Next steps

This catalog serves as the foundation for:

- defining the **grammar of decoding inputs**
- constructing the **methods ↔ inputs matrix**
- deriving observation protocols upstream

Decoding itself remains intentionally out of scope.

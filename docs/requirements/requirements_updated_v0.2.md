# Requirements Specification — Beta Function Calculator (D2 · Problem 7)

**Baseline:** v0.2 (frozen for D2) · supersedes v0.1 · **Standard:** ISO/IEC/IEEE 29148
**Function:** F6 — real Beta Function `B(x, y)`, domain `x > 0, y > 0`
**Basis for update (Problem 7):** the D2/Problem 5 from-scratch build + Tkinter GUI.
**Informed by:** persona "Maya Fernandes" ([`docs/persona.md`](../persona.md)); v0.1
baseline ([`requirements_baseline_v0.1.md`](requirements_baseline_v0.1.md)).

Problem 7 asks to *modify the D1 requirements based on the D2 implementation and give
an updated list*. The v0.1 statement style, ID scheme, priority (M/S/C), and
verification methods (T/I/A/D) are retained (decision D-006). This document lists the
**updated full baseline** and, in §4, a **change log** recording exactly what changed and
why, per requirement.

---

## 1. What the D2 build changed (summary)

Implementing from scratch and adding a GUI surfaced changes that were **discovered
through implementation**, not guessed:

1. The UI is now a **Tkinter GUI** (was a CLI). Prompts became **labels**; "another
   calculation without restart" and "exit" are now GUI affordances. → POR-01 revised;
   FR-04/FR-05 re-scoped; new **UI-01** (keyboard operability).
2. The mathematics is **from scratch** — no `math` library. → new **IMPL-01**; ACC-01
   re-validated against the from-scratch primitives (worst rel. err. 1.17×10⁻¹⁴,
   unchanged).
3. Errors are raised as a **typed exception hierarchy** with helpful messages. →
   ERR-01 strengthened; REL-01 re-scoped to "no unhandled exception reaches the GUI".
4. A **numerical-range failure** path (`NumericalRangeError`) makes REL-02 explicit
   rather than implicit.
5. The magnitude cap A-04 (`1e4`) was **retained** (re-validated: all 36 boundary
   inputs finite), closing the "revisit in D2" note on A-04/A-05.

No requirement was deleted; superseded statements are marked in §4 (history preserved,
per X-02).

---

## 2. Requirements (updated baseline v0.2)

| ID | Requirement (shall statement) | Rationale / trace | Pri | Verify | Δ vs v0.1 |
|----|-------------------------------|-------------------|-----|--------|-----------|
| **FR-01** | The system shall accept two real-number inputs, `x` and `y`, from the user via labelled GUI fields. | G1 | M | D | reworded (GUI) |
| **FR-02** | Given valid inputs, the system shall compute `B(x, y)`. | G1, G2 | M | T | — |
| **FR-03** | After a computation, the system shall display the numeric result in the result area. | G1, G2 | M | D | reworded (GUI) |
| **FR-04** | The system shall let the user perform another calculation without restarting, by editing the fields or pressing Clear. | repeated use | M | D | reworded (GUI) |
| **FR-05** | The system shall let the user exit by closing the window. | basic control | M | D | reworded (GUI) |
| **VAL-01** | When `x ≤ 0` or `y ≤ 0`, the system shall reject the input and not compute a result. | domain; G3, N1; D-001 | M | T | — |
| **VAL-02** | When an input is non-numeric or non-finite, the system shall reject it and not compute a result. | robust input; N1 | M | T | +non-finite |
| **VAL-03** | When an input field is empty, the system shall report which field is missing and not compute. | robust input; N4 | M | T | reworded (GUI) |
| **VAL-04** | When an input magnitude exceeds the supported bound (`> 1×10⁴`), the system shall reject it with a range message. | testable behaviour; N2 | S | T | — |
| **ACC-01** | For inputs `0 < x, y ≤ 50`, the system shall return a result whose relative error is ≤ 1×10⁻⁶ vs `reference_values.csv`, **using the from-scratch implementation**. | trustworthy; G1, G2 | M | T | scope: from-scratch |
| **ACC-02** | The system shall display the result to 6 significant figures and shall not imply more precision than achieved. | honest precision; N3 | M | I | — |
| **ACC-03** | The system shall convey status and errors by text (a leading word/glyph), not by colour alone, in a readable form. | accessibility; N5 | M | I | S→M (promoted) |
| **REL-01** | For any input, the system shall not terminate with, or display, an unhandled exception; expected failures are caught as typed `BetaError`s. | robustness; N2 | M | T | strengthened |
| **REL-02** | When the true value is a finite double, the system shall return it; otherwise it shall raise `NumericalRangeError` rather than return `inf`/`nan`. | Gamma-overflow; N2 | M | T | explicit failure path |
| **REL-03** | The computation shall terminate within bounded work (fixed-length series/loops, early-exit scaling). | termination | M | A | +elementary loops |
| **PERF-01** | For inputs in the supported range, the system shall return a result within 1 second on a typical laptop. | responsiveness; G1 | S | T | — |
| **USE-01** | The system shall label each input field in plain language and state the valid domain (`> 0`) at the point of input. | low CLI comfort; N1, N4; G3 | M | I | reworded (GUI) |
| **USE-02** | The system shall provide concise usage instructions accessible from the interface (Help / F1). | N4 | S | I | reworded (GUI) |
| **ERR-01** | On any rejected input or computation failure, the system shall show a specific message stating what was wrong and how to correct it. | cryptic-error pain; N1, N2 | M | T | — |
| **POR-01** | The system shall run from a standard terminal using a Python 3 command (`python3 src/gui.py`), without requiring an IDE. | portability; task constraint | M | D | CLI→GUI entry |
| **DOC-01** | The system shall document the supported domain and key assumptions in the Help window and README. | transparency; G3, N1 | S | I | +README |
| **IMPL-01** | The mathematical computation shall be implemented from scratch: no built-in/library mathematical functions (only I/O, arithmetic, UI, exception facilities). | Problem 5 mandate; D-008 | M | T,I | **new** |
| **UI-01** | The GUI shall be operable by keyboard alone: logical tab order, initial focus, Enter to calculate, Escape to clear. | accessibility; N4, N5 | M | D | **new** |
| **ERR-02** | The system shall raise distinct exception types for input errors vs numerical errors so the UI can respond appropriately. | maintainable error handling; Problem 5 | S | I,T | **new** |

**Count:** 24 requirements (was 21): +IMPL-01, +UI-01, +ERR-02; all v0.1 IDs retained.

---

## 3. Assumptions register (v0.2)

| ID | Assumption | Basis / change |
|----|-----------|----------------|
| A-01 | Supported domain is `x > 0` and `y > 0` (real). | D-001 — unchanged (confirm with professor). |
| A-02 | Inputs and output are real decimal numbers. | D-002 — unchanged. |
| A-03 | Single local user, one calculation at a time. | unchanged. |
| A-04 | Supported input magnitude bound `x, y ≤ 1×10⁴`. | **Confirmed for D2** — all 36 boundary inputs finite (REL-02). |
| A-05 | Accuracy tolerance rel. err. ≤ 1×10⁻⁶ over `0 < x,y ≤ 50`. | **Re-validated on the from-scratch build** — worst 1.17×10⁻¹⁴. |
| A-06 | "Typical current laptop" = consumer machine from ~the last 5 years. | unchanged. |
| A-07 | Elementary primitives (`ln`,`exp`,`sin`) are accurate to ≤ 1×10⁻¹² and this suffices for ACC-01. | **new** — verified (ACC-03p): ≤ 6×10⁻¹⁵. |

**Out of scope (D2):** complex arguments, analytic continuation to `x ≤ 0`/`y ≤ 0`,
the incomplete/regularized Beta, batch input, persistence, and the PEP-8/tooling/unit-test
concerns deferred to D3.

---

## 4. Change log (v0.1 → v0.2), per requirement

| Req | Change | Reason (discovered through implementation?) |
|---|---|---|
| FR-01/03/04/05, USE-01/02 | CLI prompts/commands → GUI labels/affordances. | Yes — UI moved to Tkinter (Problem 5). |
| VAL-02 | now also rejects non-finite (`inf`/`nan`) text. | Yes — `float('inf')` parses; needed an explicit guard. |
| ACC-01, A-05 | re-scoped to the from-scratch build and re-validated. | Yes — required by Problem 5; accuracy held. |
| ACC-03 | priority S → **M**. | Design: accessibility is a first-class GUI concern (persona N5). |
| REL-01 | "no unhandled exception" → "…reaches/leaves the GUI; typed catch". | Yes — GUI event loop must never show a traceback. |
| REL-02 | added explicit `NumericalRangeError` instead of silent non-finite. | Yes — needed a defined failure signal for the GUI. |
| REL-03 | now also covers the elementary series/scaling loops. | Yes — new subordinate functions introduced. |
| POR-01 | entry point `src/cli.py` → `src/gui.py`. | Yes — GUI is the D2 deliverable UI. |
| DOC-01 | assumptions now also documented in the README. | Problem 6 (README) added. |
| **IMPL-01** | new requirement. | Yes — Problem 5 "from scratch" mandate. |
| **UI-01** | new requirement. | Yes — keyboard operability emerged from GUI design. |
| **ERR-02** | new requirement. | Yes — typed exception hierarchy emerged in implementation. |

**Retired:** none. **Superseded wording** is preserved in v0.1; this baseline is
frozen as **v0.2** for D2. Every changed requirement has a rationale; no feature is
listed as required unless it is in this baseline.

---

## 5. Persona coverage (unchanged drivers, updated requirement links)

| Persona driver | Requirements (v0.2) |
|---|---|
| G1 quick trustworthy value | FR-01, FR-02, FR-03, ACC-01, PERF-01 |
| G2 verify coursework | FR-02, ACC-01 |
| G3 understand valid inputs | VAL-01, USE-01, DOC-01 |
| N1 unsure of valid range | VAL-01, USE-01, ERR-01, DOC-01 |
| N2 cryptic errors / wrong `inf` | REL-01, REL-02, ERR-01, ERR-02, VAL-04 |
| N3 honest precision | ACC-02 |
| N4 low CLI comfort | USE-01, USE-02, VAL-03, UI-01 |
| N5 accessibility | ACC-03, UI-01 |
| N6 no code/library for one value | POR-01 |

Every requirement has a unique ID, a rationale, and a verification method; every
high-priority persona need is covered. ✔

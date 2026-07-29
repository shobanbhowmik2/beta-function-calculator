# Requirements Specification — Beta Function Calculator (D1 · Problem 2)

**Baseline:** v0.1 (frozen for D1) · **Standard:** ISO/IEC/IEEE 29148 guidance
**Function:** F6 — real Beta Function `B(x, y)`, domain `x > 0, y > 0`
**Informed by:** persona "Maya Fernandes" ([`docs/persona.md`](../persona.md)) — needs G1–G3, N1–N6.

---

## 1. Requirement statement style (D1-P2.1)

Requirements follow the 29148 recommended imperative pattern:

> **[Condition]** the **system** **shall** **[action]** **[object]** **[constraint]**.

- Modal verb **shall** = mandatory. Each statement is **singular** (one testable claim).
- **Identifier scheme** (category-prefixed, zero-padded):
  `FR` functional · `VAL` input/domain validation · `ACC` accuracy/numeric ·
  `USE` usability · `REL` reliability · `PERF` performance · `ERR` error handling ·
  `POR` portability · `DOC` documentation.
- **Priority:** `M` must-have · `S` should-have · `C` could-have.
- **Verification method:** `T` test · `I` inspection · `A` analysis · `D` demonstration.

---

## 2. Requirements

| ID | Requirement (shall statement) | Rationale / persona trace | Pri | Verify |
|----|-------------------------------|---------------------------|-----|--------|
| **FR-01** | The system shall accept two real-number inputs, `x` and `y`, from the user. | Core function; G1 | M | D |
| **FR-02** | Given valid inputs, the system shall compute `B(x, y)`. | Core function; G1, G2 | M | T |
| **FR-03** | After a computation, the system shall display the numeric result to the user. | G1, G2 | M | D |
| **FR-04** | The system shall let the user perform another calculation without restarting the program. | Repeated use; task list | M | D |
| **FR-05** | The system shall provide a defined command to exit the program. | Basic control | M | D |
| **VAL-01** | When `x ≤ 0` or `y ≤ 0`, the system shall reject the input and not compute a result. | Domain `x,y>0`; G3, N1; D-001 | M | T |
| **VAL-02** | When an input is non-numeric, the system shall reject it and not compute a result. | Robust input; N1 | M | T |
| **VAL-03** | When an input is empty/missing, the system shall reject it and prompt again. | Robust input; N4 | M | T |
| **VAL-04** | When an input's magnitude exceeds the supported bound (`x` or `y` > 1×10⁴), the system shall reject it with a range message rather than attempt the computation. | Bounded, testable behaviour; N2 | S | T |
| **ACC-01** | For inputs `0 < x, y ≤ 50`, the system shall return a result whose relative error is ≤ 1×10⁻⁶ compared with the trusted reference values in `reference_values.csv`. | Trustworthy result; G1, G2; measurable | M | T |
| **ACC-02** | The system shall display the result to a documented precision (6 significant figures) and shall not present more digits than the achieved accuracy supports. | Honest precision; N3 | M | I |
| **REL-01** | For any input in the supported range, the system shall not terminate with an unhandled exception. | Robustness; N2 | M | T |
| **REL-02** | When the true value is representable as a finite double, the system shall not return a non-finite value (`inf`/`nan`) for supported inputs. | Gamma-overflow risk; N2; research §5 | M | T |
| **REL-03** | The computation shall terminate within a bounded amount of work (a defined maximum iteration/subdivision limit) for every supported input. | Guaranteed termination; research §5 | M | A |
| **PERF-01** | For inputs in the supported range, the system shall return a result within 1 second on a typical current laptop. | Responsiveness; G1 | S | T |
| **USE-01** | The system shall present each input prompt in plain language and shall state the valid domain (`x > 0`, `y > 0`) at the point of input. | Low CLI comfort; N1, N4; G3 | M | I |
| **USE-02** | The system shall provide concise usage instructions accessible from the interface. | N4 | S | I |
| **ERR-01** | On any rejected input or computation failure, the system shall show a specific message stating what was wrong and how to correct it. | Cryptic-error pain; N2, N1 | M | T |
| **ACC-03** | The system shall convey status and errors by text (not by colour alone) and in a readable form. | Accessibility; N5 | S | I |
| **POR-01** | The system shall run from a standard terminal using a Python 3 command, without requiring an IDE. | Portability; task/D2 constraint | M | D |
| **DOC-01** | The system shall document, in user-facing help, the supported domain and the key assumptions. | Transparency; G3, N1 | S | I |

---

## 3. Assumptions register (separate from requirements)

| ID | Assumption | Basis |
|----|-----------|-------|
| A-01 | Supported domain is `x > 0` and `y > 0` (real). | D-001 — **confirm with professor** |
| A-02 | Inputs and output are real decimal numbers (no complex/symbolic). | D-002 |
| A-03 | Single local user, one calculation at a time (no concurrency, no persistence). | Scope |
| A-04 | Supported input magnitude bound is `x, y ≤ 1×10⁴` for D1; may be revised in D2. | Testability (VAL-04) |
| A-05 | Target accuracy tolerance is relative error ≤ 1×10⁻⁶ over `0 < x,y ≤ 50`. | ACC-01; revisit after from-scratch build (D2) |
| A-06 | "Typical current laptop" for PERF-01 = a consumer machine from ~the last 5 years. | PERF-01 measurability |

**Out of scope (D1):** complex arguments, analytic continuation to `x ≤ 0`/`y ≤ 0`,
the incomplete/regularized Beta, batch input, and a GUI (GUI arrives in D2).

---

## 4. Requirements quality review (D1-P2.3)

Checked against 29148 characteristics: *necessary, unambiguous, complete, singular,
feasible, verifiable, consistent*.

| Check | Finding | Resolution |
|-------|---------|------------|
| Unambiguous / verifiable | "accurate", "fast", "helpful" were initially vague. | Quantified: ACC-01 (≤1e-6 rel. err.), PERF-01 (<1 s), ERR-01 (what+how). |
| Singular | An early draft combined "compute and display" in one statement. | Split into FR-02 (compute) and FR-03 (display). |
| Consistent | REL-02 (no `inf`) vs ACC-01 (tolerance) could conflict for huge inputs. | Bounded by VAL-04 (reject `>1e4`) + A-04, so the ranges don't collide. |
| Feasible | ACC-01 at 1e-6 must hold for the **from-scratch** D2 build too, not just D1. | Flagged in A-05 to re-validate after D2; achievable with log-domain evaluation. |
| Complete | Accessibility need N5 had no requirement. | Added ACC-03. |
| Necessary | No requirement lacks a persona/scope rationale. | Every row has a rationale; VAL-04/A-04 justified by testability. |
| Domain consistency | Domain in requirements matches A-01/D-001. | Consistent (pending professor confirmation of A-01). |

**No known contradiction remains.** All high-priority persona needs (G1–G3, N1–N5) are
represented. **Baseline frozen as v0.1 for D1.**

---

## 5. Persona coverage summary (traceability)

| Persona driver | Requirements |
|---|---|
| G1 quick trustworthy value | FR-01, FR-02, FR-03, ACC-01, PERF-01 |
| G2 verify coursework | FR-02, ACC-01 |
| G3 understand valid inputs | VAL-01, USE-01, DOC-01 |
| N1 unsure of valid range | VAL-01, USE-01, ERR-01, DOC-01 |
| N2 cryptic errors / wrong `inf` | REL-01, REL-02, ERR-01, VAL-04 |
| N3 honest precision | ACC-02 |
| N4 low CLI comfort | USE-01, USE-02, VAL-03 |
| N5 accessibility | ACC-03 |
| N6 no code/library for one value | POR-01 (runs standalone) |

Every requirement has a unique ID, a rationale, and a verification method; every
high-priority persona need is covered. ✔

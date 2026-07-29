# D2 Verification Matrix (Problem 5.6)

**Scope:** the Deliverable 2 from-scratch build (`src/elementary.py`,
`src/beta_core.py`, `src/validation.py`) and the Tkinter GUI (`src/gui.py`)
against the updated requirements baseline
[`requirements_updated_v0.2.md`](requirements/requirements_updated_v0.2.md).
**Method key (29148):** `T` test · `I` inspection · `A` analysis · `D` demonstration.

**Evidence sources**
- **H** — automated harness [`tests/verify_d2.py`](../tests/verify_d2.py) → **27/27 checks pass** (re-runnable; exits non-zero on regression).
- **S** — rendered GUI states in [`docs/screenshots/`](screenshots/) (`gui_valid`, `gui_domain`, `gui_nonnumeric`).
- **C** — code inspection of the `src/` modules.
- **R** — trusted reference table [`reference_values.csv`](reference_values.csv).

---

## 1. Requirement → demo case → result

| Req | Method | Demo case | Expected | Observed | Result | Src |
|-----|:------:|-----------|----------|----------|:------:|:---:|
| **IMPL-01** | T,I | scan shipped `src/*.py` for `import math`/numpy/scipy | none | none (clean) | ✅ | H,C |
| **IMPL-01** | T | `elementary.exp/ln/sin` vs `math` oracle | rel err ≤ 1e-12 | worst 5.6e-15 (exp) | ✅ | H |
| **FR-01** | D | enter x=2, y=3 in GUI fields | both accepted | computed | ✅ | S |
| **FR-02** | T | B(1,1); B(2,3) | 1 ; 1/12 | 1 ; 0.0833333 | ✅ | H,R |
| **FR-02** | T | symmetry B(2.3,5.1)=B(5.1,2.3) | equal | rel diff 0 | ✅ | H |
| **FR-03** | D | result shown after Calculate | numeric line in Result area | `B(2, 3) = 0.0833333` | ✅ | S |
| **FR-04** | D | Clear then recompute | clean state, no restart | fields cleared, focus x | ✅ | H(GUI-06),S |
| **VAL-01** | T | x=0 ; y=−2 | `DomainError`, no compute | raised + helpful | ✅ | H,S |
| **VAL-02** | T | x=`abc` ; x=`inf` | `NonNumericError`/`NonFiniteError` | raised + helpful | ✅ | H |
| **VAL-03** | T | x empty | `EmptyInputError`, names field | raised + helpful | ✅ | H,S |
| **VAL-04** | T | x=1e6 (>1e4) | `RangeError` | raised + helpful | ✅ | H,S |
| **ACC-01** | T | 18 reference values (0<x,y≤50) | rel err ≤ 1e-6 each | **worst 1.17e-14** | ✅ | H,R |
| **ACC-01** | T | B(0.2,0.3) near-singular corner | 7.74848 | 7.74848 | ✅ | H,R |
| **ACC-02** | I | display B(2,3) | 6 sig figs | `0.0833333` | ✅ | H,C |
| **ACC-03** | I | status conveyance | text word+glyph, not colour alone | "Result:"/"Out of domain:" prefixes | ✅ | S,C |
| **REL-01** | T | 10 malformed inputs | only typed `BetaError`s | clean (no other exception) | ✅ | H |
| **REL-01** | T | GUI: 5 invalid cases | no traceback shown | specific status each | ✅ | H(GUI),S |
| **REL-02** | T | 36 large/small supported inputs | all finite | all finite | ✅ | H |
| **REL-02** | I | `NumericalRangeError` path | raisable on non-finite | present + raised in `beta` | ✅ | C |
| **REL-03** | A | Lanczos + elementary loops | bounded work | fixed 8-term Lanczos; series early-exit | ✅ | H,C |
| **PERF-01** | T | 50 000 computations | < 1 s/call | **7.8e-3 ms/call** | ✅ | H |
| **USE-01** | I | field labels | state domain `> 0` | "x (must be > 0)" + hint | ✅ | S,C |
| **USE-02** | I | Help / F1 | usage shown | Help window with definition+keys | ✅ | C,S |
| **ERR-01** | T | non-numeric x | says what + how | "…is not a number. Enter a decimal…" | ✅ | H |
| **ERR-02** | I,T | distinct exception types | input vs numerical separated | `InputError` vs `NumericalError` trees | ✅ | H,C |
| **POR-01** | D | `python3 -c` build GUI, compute | exit 0, result shown | exit 0, `0.0833333` | ✅ | H |
| **UI-01** | D | keyboard: focus, Tab, Enter, Esc | operable without mouse | initial focus x; Enter=calc; Esc=clear | ✅ | C(bindings) |
| **DOC-01** | I | Help + README | domain + assumptions stated | both document `x,y>0` | ✅ | C |

**Summary:** all 24 v0.2 requirements demonstrated; **27/27** machine-checkable checks
pass in `tests/verify_d2.py`. Worst accuracy error **1.17×10⁻¹⁴**, unchanged from D1 —
the from-scratch reimplementation cost nothing in accuracy.

> Regenerate any time with: `python3 tests/verify_d2.py`

---

## 2. Known limitations (honest disclosure)

1. **Domain `x > 0, y > 0` only** (D-001, A-01) — no analytic continuation or complex
   arguments. Scope boundary, pending professor confirmation.
2. **Magnitude cap `x, y ≤ 1×10⁴`** (VAL-04, A-04). Confirmed for D2 (all boundary
   inputs finite); values above are rejected by design.
3. **Underflow to `0.0` for very large near-equal inputs** (e.g. `B(1e4, 1e4)`), whose
   true value is below the smallest positive double. `0.0` is the correct finite double,
   not an error; ACC-01 is validated only to `x,y ≤ 50`.
4. **Accuracy bounded by the Lanczos g=7 set** (~15 digits) and by the elementary-function
   series (verified ≤ 6×10⁻¹⁵). A wrong coefficient would silently reduce accuracy —
   guarded by the ACC-01 regression check.
5. **GUI screenshots are layout renders** reproducing the exact widgets and status
   strings of `src/gui.py` (checks GUI-01…GUI-06); a live grab is blocked headlessly.
   The genuine window is shown in the Zoom demo.
6. **PERF-01 measured on the development machine** — huge margin, but "typical laptop"
   (A-06) is not independently benchmarked.

**No known correctness defect within the supported domain.** Every limitation is a
documented scope boundary or assumption (D-001/D-004/D-007/D-008, A-01/A-04/A-05/A-06).

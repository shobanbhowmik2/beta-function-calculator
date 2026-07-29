# D1 Verification Matrix (Problem 4.3)

**Scope:** Deliverable 1 prototype `src/cli.py` (Algorithm B — Gamma identity, log-domain
Lanczos `lnΓ`) against the frozen requirements baseline
[`requirements_baseline_v0.1.md`](requirements/requirements_baseline_v0.1.md).
**Method key (29148):** `T` test · `I` inspection · `A` analysis · `D` demonstration.

**Evidence sources**
- **H** — automated harness [`tests/verify_d1.py`](../tests/verify_d1.py) → **15/15 checks pass** (re-runnable).
- **S** — captured terminal transcripts in [`docs/screenshots/`](screenshots/) (`run_valid`, `run_boundary`, `run_invalid`) + [`sample_runs.md`](screenshots/sample_runs.md).
- **C** — code inspection of `src/cli.py`.
- **R** — trusted reference table [`reference_values.csv`](reference_values.csv).

---

## 1. Requirement → demo case → result vs reference

| Req | Method | Demo case | Expected (reference) | Observed | Result | Src |
|-----|:------:|-----------|----------------------|----------|:------:|:---:|
| **FR-01** | D | Enter x=2, y=3 at prompts | both accepted as reals | accepted; computed | ✅ | S |
| **FR-02** | T | Compute B(1,1); B(2,3) | 1 ; 1/12 | 1 ; 0.0833333 | ✅ | H,R |
| **FR-03** | D | Result shown after compute | numeric line displayed | `B(2, 3) = 0.0833333` | ✅ | S |
| **FR-04** | D | Two calculations, no restart | second prompt appears | valid run does 3 in a row | ✅ | S |
| **FR-05** | D | Enter `q` | program exits cleanly | `Goodbye.`, exit 0 | ✅ | S,H |
| **VAL-01** | T | x=0 ; x=−2 | rejected, not computed | rejected w/ domain message | ✅ | H,S |
| **VAL-02** | T | x=`abc` | rejected, not computed | "…is not a number…" | ✅ | H,S |
| **VAL-03** | T | x=empty | reject + reprompt | "x was empty…" | ✅ | H,S |
| **VAL-04** | T | x=1e6 (>1e4) | range message, no compute | "…exceeds the supported bound…" | ✅ | H,S |
| **ACC-01** | T | 18 reference values, 0<x,y≤50 | rel err ≤ 1e-6 each | **worst rel err 1.17e-14** | ✅ | H,R |
| **ACC-01** | T | B(0.2,0.3) singular corner | 7.748481 | 7.74848 | ✅ | H,R |
| **ACC-02** | I | Display precision of B(2,3) | 6 significant figures | `0.0833333` (6 s.f.) | ✅ | H,C |
| **REL-01** | T | 10 malformed inputs in a row | no unhandled exception | 0 crashes | ✅ | H,S |
| **REL-02** | T | 36 large/small supported inputs | all finite (no inf/nan) | all finite | ✅ | H |
| **REL-03** | A | Lanczos `lnΓ` loop | bounded work | fixed 8-iteration loop, no growth | ✅ | H,C |
| **PERF-01** | T | 100 000 computations | < 1 s per computation | **0.0000013 s/call** | ✅ | H |
| **USE-01** | I | Each input prompt | states domain `> 0` | `x (> 0):` / `y (> 0):` | ✅ | S,C |
| **USE-02** | I | `h` command | usage instructions shown | help block lists range+commands | ✅ | S |
| **ERR-01** | T | non-numeric x | says what + how to fix | "…not a number. Enter a decimal…" | ✅ | H,S |
| **ACC-03** | I | Status/error conveyance | text, not colour alone | all messages plain text | ✅ | S,C |
| **POR-01** | D | `python3 src/cli.py` (no IDE) | runs, exit 0, prints result | exit 0, result seen | ✅ | H,S |
| **DOC-01** | I | `h` help content | states domain + assumptions | help states domain + "real inputs only" | ✅ | S |

**Summary:** all 20 D1 requirements demonstrated; 15 machine-checkable ones pass in
`tests/verify_d1.py` (15/15). Worst observed accuracy error is **1.17×10⁻¹⁴**, eight
orders of magnitude inside the ACC-01 tolerance of 1×10⁻⁶.

> Regenerate the evidence any time with: `python3 tests/verify_d1.py`
> (exits non-zero if any check regresses).

---

## 2. Known limitations (honest disclosure)

1. **Domain is `x > 0, y > 0` only.** No analytic continuation to `x ≤ 0` / `y ≤ 0`
   (poles of Γ) and no complex arguments. This is a *scope* decision (D-001, A-01),
   still pending professor confirmation — not a defect, but a documented boundary.
2. **Magnitude cap `x, y ≤ 1×10⁴` (VAL-04/A-04).** Chosen for testable, overflow-free
   behaviour in D1. Values above the cap are rejected rather than attempted; the cap
   may be revised in D2.
3. **Accuracy is bounded by the Lanczos g=7 coefficient set** (~15 significant digits).
   Verified excellent over the tested range, but a wrong/low-precision coefficient table
   would silently reduce accuracy — the D2 from-scratch build must re-validate.
4. **Rejected Algorithm A is not shipped.** The Euler-quadrature path fails ACC-01 near
   singular endpoints (B(0.2,0.3): rel err ≈ 2.7×10⁻³) and was deliberately excluded
   from the CLI; only Algorithm B is exercised here.
5. **D1 prototype uses `math` primitives** (`log`, `exp`, `sin`, `π`). These are the
   only borrowed pieces (no `math.gamma`/`lgamma`/`beta`) and are flagged for
   from-scratch reimplementation in D2 — see
   [`d2_from_scratch_notes.md`](algorithms/d2_from_scratch_notes.md).
6. **ACC-01 range validated to `0 < x,y ≤ 50` against the reference table.** Inputs
   between 50 and the 1e4 cap compute finite results but are outside the table's trusted
   coverage (A-05 flags re-validation after the D2 build).
7. **Reference values are themselves lgamma-verified**, so the ACC-01 check confirms
   agreement with a trusted numerical baseline, not with independent arbitrary-precision
   arithmetic. Adequate for D1; noted for transparency.
8. **PERF-01 measured on this development machine.** The 1.3 µs/call figure gives a huge
   margin under the 1 s requirement, but "typical laptop" (A-06) timing is not
   independently benchmarked.

**No known correctness defect within the supported domain.** Every listed limitation is
a scope boundary or a documented assumption, each traceable to a decision (D-001/D-004/
D-007) or an assumption (A-01/A-04/A-05/A-06).

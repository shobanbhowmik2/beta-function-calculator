# GAI / LLM Prompt Log — SOEN 6011 F6 Beta Function

Per course constraint **C-03**, every problem must use one or more public GAI (LLM)
tools with **CASTROFF**-based prompts, and record the prompt type, an example prompt,
and an explanation/evaluation of the output. (Cross-deliverable task X-03.)

The ready-to-use CASTROFF prompts live in
[`SOEN_6011_F6_D1_Prompts.md`](../../../SOEN_6011_F6_D1_Prompts.md). Log each actual use
below.

---

## Log template (copy per use)

### <Problem ID> — <short title>
- **Date:**
- **GAI tool (name + version/date):**
- **Prompt type:** (e.g. generative / transformational / decision-support / comparative / review)
- **CASTROFF sections used:** TASK · RESTRICTIONS · OUTPUT FORMAT · AUDIENCE (note any others)
- **Exact prompt submitted:** (paste verbatim, including any pasted prior-problem content)
- **Output summary:**
- **Critical evaluation:** what was accepted / rejected / corrected, and why
- **Verification:** how the output was independently checked (reference values, standard, requirement, reasoning)
- **Attribution:** any non-original content cited (link to `references.bib` key)

---

## Entries

### D1-P1 — Persona
- **Date:** 2026-07-14
- **GAI tool (name + version/date):** Claude (Opus 4.8) via Claude Code — _confirm/adjust to the exact tool + version you present with._
- **Prompt type:** Generative + decision-support (template comparison → persona).
- **CASTROFF sections used:** TASK · RESTRICTIONS · OUTPUT FORMAT · AUDIENCE (see the P1 prompt in `SOEN_6011_F6_D1_Prompts.md`, with the F6 research context supplied).
- **Exact prompt submitted:** the Problem 1 CASTROFF prompt (template comparison of ≥3 persona styles against stated criteria, then a goal-directed persona for a Beta-function user, with evidence/assumption labelling). Full text in the prompts file.
- **Output summary:** (1) comparison of Goal-directed / Role-based / Proto templates → recommended goal-directed, trimmed to one page, grafting proto's explicit assumption labels; (2) persona "Maya Fernandes" with goals G1–G3, needs N1–N6, a usage scenario, and a needs→requirements table.
- **Critical evaluation:**
  - *Accepted:* the goal-directed choice (best requirement traceability), the assumption-labelling idea, and the needs→requirements mapping.
  - *Adjusted / to review:* age/education/screen-reader use are **assumptions [A]** — confirm they are reasonable for your intended user; tighten any attribute you can't defend.
  - *Rejected:* none material; excluded irrelevant biographical detail deliberately.
- **Verification:** persona needs cross-checked against the domain research (§4 applications, §5 numerical risks) so each pain point is technically grounded; traceability gate (≥5) satisfied with 7 mappings.
- **Attribution:** persona-template concepts (goal-directed / proto) attributable to Cooper and the proto-persona practice — **add a citation to `references.bib`** if you reference them in the report.

> **Your action:** re-read the persona, replace any assumption you don't endorse, and
> write one or two sentences of your own critical assessment so this reflects your
> judgement, not only the tool's output.

### D1-P2 — Requirements
- **Date:** 2026-07-15
- **GAI tool (name + version/date):** Claude (Opus 4.8) via Claude Code — _confirm to your presented tool._
- **Prompt type:** Transformational (persona needs → verifiable requirements) + review.
- **CASTROFF sections used:** TASK · RESTRICTIONS · OUTPUT FORMAT · AUDIENCE (P2 prompt in `SOEN_6011_F6_D1_Prompts.md`, with the finalized persona pasted in).
- **Exact prompt submitted:** the Problem 2 CASTROFF prompt with persona G1–G3 / N1–N6 supplied; requested 29148-style statements, ID scheme, priorities, verification methods, a separate assumptions list, and a quality-review pass.
- **Output summary:** 21 requirements across FR/VAL/ACC/USE/REL/PERF/ERR/POR/DOC with persona traces, priorities, and verification methods; a 6-row assumptions register; a 7-check quality review; a persona-coverage table. Baseline frozen v0.1.
- **Critical evaluation:**
  - *Accepted:* the ID scheme, quantified tolerance (ACC-01 ≤1e-6), and the split of compute/display into FR-02/FR-03.
  - *Adjusted / to review:* the numeric bounds are **assumptions** — the magnitude cap (A-04, 1e4), the tolerance range (A-05, ≤50), and PERF-01 (<1 s) are defensible defaults you should confirm you can meet with the from-scratch D2 build.
  - *Rejected:* no requirement that prescribes an algorithm (kept algorithm-neutral per the prompt restriction).
- **Verification:** each requirement checked for a verification method and singularity; consistency conflict (REL-02 vs ACC-01) resolved via VAL-04; accessibility gap (N5) closed with ACC-03.
- **Attribution:** ISO/IEC/IEEE 29148 (`iso29148` in `references.bib`).

> **Your action:** confirm the numeric thresholds (A-04/A-05/PERF-01) are ones you can
> defend, and add your own one-line critical assessment.

### D1-P3 — Two algorithms
- **Date:** 2026-07-15
- **GAI tool (name + version/date):** Claude (Opus 4.8) via Claude Code — _confirm to your presented tool._
- **Prompt type:** Generative + comparative (two independent, language-neutral algorithms).
- **CASTROFF sections used:** TASK · RESTRICTIONS · OUTPUT FORMAT · AUDIENCE (P3 prompt in `SOEN_6011_F6_D1_Prompts.md`, with requirement IDs ACC-01/VAL-01/REL-02/REL-03 supplied).
- **Exact prompt submitted:** the Problem 3 CASTROFF prompt — Algorithm A = adaptive-Simpson quadrature of the Euler integral with endpoint handling; Algorithm B = Gamma identity via a Lanczos `lnΓ` in the log domain; each with pre/postconditions, termination safeguard, complexity, weaknesses, and a worked trace.
- **Output summary:** two established-format pseudocode listings + a "How A and B differ" table, in `docs/algorithms/algorithms_pseudocode.md`.
- **Critical evaluation:**
  - *Accepted:* both listings and the comparison; log-domain form of B (satisfies REL-02).
  - *Verified independently (not just trusted):* implemented both in Python and compared to `math.lgamma` reference — B matches to ~10 digits everywhere; A degrades near singular endpoints (B(0.2,0.3): 7.7277 vs 7.7485, rel. err ≈ 2.7e-3, **fails ACC-01**). This empirical result is cited in the weaknesses and drives P4.
  - *Rejected:* no Python syntax in the pseudocode (kept language-neutral per the restriction).
- **Verification:** numeric check script (see reference values) across 8 cases incl. integer, half-integer, large, and near-singular inputs.
- **Attribution:** Lanczos approximation (add a source to `references.bib` before the report); adaptive Simpson is standard numerical analysis.

> **Your action:** add a source for the Lanczos coefficients to `references.bib`, and
> add your own one-line critical note.

### D1-P4 — Selection + CLI
- **Date:** 2026-07-15
- **GAI tool (name + version/date):** Claude (Opus 4.8) via Claude Code — _confirm to your presented tool._
- **Prompt type:** Decision-support (algorithm-selection mind map) + generative (Python CLI with a textual UI).
- **CASTROFF sections used:** TASK · RESTRICTIONS · OUTPUT FORMAT · AUDIENCE (P4 prompt in `SOEN_6011_F6_D1_Prompts.md`, with both Problem 3 algorithms pasted in).
- **Exact prompt submitted:** the Problem 4 CASTROFF prompt — Step 1 selection via a mind map comparing Algorithm A (Euler adaptive Simpson) and Algorithm B (Gamma identity, log-domain Lanczos `lnΓ`) against accuracy, domain coverage, numerical stability, implementation effort, D2 from-scratch fit, performance, and explainability; Step 2 a Python 3 CLI implementing the selected algorithm with I/O separated from compute, validation, and helpful errors.
- **Output summary:**
  - Selection mind map → `docs/mindmaps/algorithm_selection.dot` (+ `.png`, `.pdf`). **Selected Algorithm B; rejected A for this stage.**
  - CLI → `src/cli.py`: pure compute core (`beta`/`beta_ln`/`ln_gamma`) separated from a console I/O layer; validation for empty/non-numeric/≤0/over-cap; per-error helpful messages; result shown to 6 sig figs.
  - Sample runs (valid / boundary / invalid) → `docs/screenshots/` (`.txt` transcripts + rendered `.png`), plus `sample_runs.md`.
  - D2 from-scratch note → `docs/algorithms/d2_from_scratch_notes.md`.
- **Critical evaluation:**
  - *Accepted:* the selection of B — it is the **only** candidate meeting ACC-01 uniformly while also satisfying REL-02 (log-domain, no overflow), REL-03 (fixed loop), and PERF-01 (O(1)). The compute/I/O separation was kept for testability and D2 reuse.
  - *Verified independently (not just trusted):* ran the CLI's core against all 18 trusted values in `reference_values.csv` — **18/18 within ACC-01**, worst relative error **1.2×10⁻¹⁴**. This includes B(0.2, 0.3) = 7.74848, the near-singular case where Algorithm A had failed ACC-01 in P3 — direct evidence for rejecting A.
  - *Adjusted:* implemented `lnΓ` via the Lanczos series by hand (using only `log`/`exp`/`sin`/π) rather than calling `math.lgamma`, so the D2 "from-scratch" obligation is honest and scoped to three elementary primitives (documented in `MATH_CALLS_TO_REPLACE` and `d2_from_scratch_notes.md`).
  - *Rejected:* no library `gamma`/`lgamma`/`beta` call (would defeat the D2 exercise); no colour-only status output (ACC-03).
- **Verification:** reference-value check script (18 cases) + three captured terminal sessions exercising every VAL/REL/ERR path with no unhandled traceback (Gate ✔).
- **Attribution:** Lanczos approximation coefficients (g=7) — add the Lanczos source to `references.bib` (flagged in P3). Adaptive Simpson (rejected candidate) is standard numerical analysis.

> **Your action:** confirm the presented GAI tool/version; skim `src/cli.py` and the
> selection mind map, and add one or two sentences of your own critical assessment of
> the A-vs-B decision so it reflects your judgement, not only the tool's output.

---

## Deliverable 2 entries

The ready-to-use D2 CASTROFF prompts live in
[`SOEN_6011_F6_D2_Prompts.md`](../../../SOEN_6011_F6_D2_Prompts.md).

### D2-P5 — From-scratch implementation + Tkinter GUI
- **Date:** 2026-07-24
- **GAI tool (name + version/date):** Claude (Opus 4.8) via Claude Code — _confirm to your presented tool._
- **Prompt type:** Generative + transformational (refactor D1 to from-scratch) + design (GUI).
- **CASTROFF sections used:** TASK · RESTRICTIONS · OUTPUT FORMAT · AUDIENCE (P5 prompt in `SOEN_6011_F6_D2_Prompts.md`, with `src/cli.py` and `MATH_CALLS_TO_REPLACE` supplied).
- **Exact prompt submitted:** the Problem 5 CASTROFF prompt — (1) freeze the from-scratch boundary and classify every dependency; (2) reimplement `ln`/`exp`/`sin`/π from scratch with range reduction + series, keeping the Lanczos `lnΓ` and log-domain Beta; (3) wireframe then implement a Tkinter GUI with a typed exception hierarchy and helpful messages, I/O separated from the numerical core.
- **Output summary:** modularised source — `elementary.py` (from-scratch primitives), `beta_core.py` (pure core, imports only `elementary`), `validation.py`, `exceptions.py` (typed hierarchy), `gui.py` (Tkinter); boundary doc, elementary-functions derivations, GUI wireframe; verification harness `tests/verify_d2.py`.
- **Critical evaluation:**
  - *Accepted:* the range-reduction-plus-series design for each primitive; the `BetaError` hierarchy; keeping `cli.py` as a frozen D1 baseline; the compute/UI separation.
  - *Verified independently (not just trusted):* ran `tests/verify_d2.py` — the shipped modules import no `math`/numpy/scipy (IMPL-01), the hand-written `exp`/`ln`/`sin` match `math` to ≤ 6×10⁻¹⁵, and the Beta core reproduces the D1 accuracy **exactly** (worst ACC-01 rel err 1.17×10⁻¹⁴, 18/18); the GUI handlers report the correct status for the valid case and all four invalid classes with no traceback (GUI-01…06). **27/27 checks pass.**
  - *Adjusted:* implemented `floor`/`round`/`is_finite`/`abs` by hand (sign tests + casts) rather than calling `math.floor` etc., so the boundary is honest; `2^k` scaling uses repeated multiplication with early over/underflow exit (bounded work, REL-03).
  - *Rejected:* any use of `math`/`numpy`/`scipy`/`mpmath` in shipped code; colour-only status (ACC-03); CORDIC/minimax (unnecessary complexity, D-009).
- **Verification:** `python3 tests/verify_d2.py` (27/27) + rendered GUI states + code inspection. See `docs/verification_matrix_d2.md`.
- **Attribution:** elementary-function evaluation (Muller); range reduction (Cody & Waite); Lanczos `lnΓ` (Lanczos; Press et al.); Tkinter (Python docs) — all in `references.bib`.

> **Your action:** run `python3 src/gui.py` yourself, try a few inputs live, skim
> `elementary.py`, and add one or two sentences of your own critical assessment of the
> from-scratch trade-off so it reflects your judgement.

### D2-P6 — Public repository, commits, README
- **Date:** 2026-07-24
- **GAI tool (name + version/date):** Claude (Opus 4.8) via Claude Code — _confirm to your presented tool._
- **Prompt type:** Advisory / generative (repo hygiene, commit strategy, README authoring).
- **CASTROFF sections used:** TASK · RESTRICTIONS · OUTPUT FORMAT · AUDIENCE (P6 prompt).
- **Exact prompt submitted:** the Problem 6 CASTROFF prompt — propose a `.gitignore`, an incremental commit sequence with imperative high-quality messages (one cohesive change each), and a README that lets a fresh user run the app.
- **Output summary:** `.gitignore` (pycache, `.DS_Store`, build artefacts, zips); an 11-commit incremental history separating scaffold / elementary / core / validation+exceptions / GUI / tests / docs / requirements / report / slides; a full README (purpose, definition, run command, examples, screenshots, error guide, structure, version, attribution).
- **Critical evaluation:**
  - *Accepted:* the incremental commit plan and the README structure.
  - *Adjusted:* the actual **public publish step is left to the author** — creating a public repo and pushing under a personal GitHub account is an outward-facing action requiring the author's credentials and consent. Local commits were made; exact `gh`/`git remote`/`push` commands are provided in the README and execution steps, and the author pastes the resulting URL into the README/report placeholder.
  - *Rejected:* squashing everything into one "final upload" commit (would hide the evolution required by Problem 6).
- **Verification:** `git log` shows the incremental history; a fresh clone runs `python3 src/gui.py` using only the README.
- **Attribution:** commit-message conventions (Keep a Changelog; conventional imperative subjects) noted in README/CHANGELOG.

> **Your action:** create the public repo, push, and paste the URL into `README.md` and
> the report where marked `<PUBLIC-REPO-URL>`; confirm it loads while logged out.

### D2-P7 — Updated requirements
- **Date:** 2026-07-24
- **GAI tool (name + version/date):** Claude (Opus 4.8) via Claude Code — _confirm to your presented tool._
- **Prompt type:** Transformational + review (evolve the v0.1 baseline from the D2 build).
- **CASTROFF sections used:** TASK · RESTRICTIONS · OUTPUT FORMAT · AUDIENCE (P7 prompt, with the v0.1 baseline and the actual D2 behaviour supplied).
- **Exact prompt submitted:** the Problem 7 CASTROFF prompt — compare each v0.1 requirement to the observed D2 behaviour; add/revise for the GUI, the from-scratch mandate, typed exceptions, and the explicit numerical-range failure; retire nothing silently; assign a new baseline version with a per-requirement change log.
- **Output summary:** `requirements_updated_v0.2.md` — 24 requirements (all v0.1 IDs kept; +IMPL-01, +UI-01, +ERR-02), an updated assumptions register (A-04/A-05 confirmed, +A-07), a §4 change log with reasons, and refreshed persona coverage. Baseline frozen v0.2.
- **Critical evaluation:**
  - *Accepted:* keeping all v0.1 IDs for traceability; recording which changes were *discovered through implementation*.
  - *Adjusted:* promoted ACC-03 to must-have (accessibility is first-class for the GUI); made REL-02 raise `NumericalRangeError` rather than describe a silent guard.
  - *Rejected:* deleting obsolete CLI requirements outright (superseded wording preserved in v0.1 instead).
- **Verification:** every v0.2 requirement mapped to a check in `docs/verification_matrix_d2.md`; each change traced to a decision (D-008…D-012) or observed behaviour.
- **Attribution:** ISO/IEC/IEEE 29148 (`iso29148`).

> **Your action:** confirm the promoted/added requirements reflect what you actually
> built and are ones you can defend; add your own one-line critical note.

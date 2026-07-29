# Changelog

All notable changes to this project are documented here. Format loosely follows
[Keep a Changelog](https://keepachangelog.com/); versions follow Semantic Versioning
(applied formally in D3).

## [0.2.0] — 2026-07-24 — Deliverable 2

### Added
- From-scratch elementary functions (`src/elementary.py`): `ln`, `exp`, `sin`, the
  constant `PI`, and `is_finite`, via range reduction + convergent series — no `math`
  library (Problem 5).
- Pure numerical core (`src/beta_core.py`) importing only `elementary`; raises
  `DomainError`/`NumericalRangeError`.
- Typed exception hierarchy (`src/exceptions.py`): `BetaError` → input/domain/range/
  numerical subclasses, each with a user-facing message.
- Shared input validation and result formatting (`src/validation.py`).
- Tkinter GUI (`src/gui.py`): labelled fields with domain hints, Calculate/Clear/Help,
  keyboard-first operation (focus, Tab, Enter, Escape, F1), and text-based status that
  does not rely on colour alone.
- D2 verification harness (`tests/verify_d2.py`, 27/27) and verification matrix.
- Docs: from-scratch boundary, elementary-function derivations, GUI wireframe, updated
  requirements baseline **v0.2**, D2 CASTROFF prompts, and GAI-log entries.

### Changed
- Requirements evolved v0.1 → v0.2 (Problem 7): GUI rewording; ACC-03 promoted to
  must-have; REL-02 now raises an explicit `NumericalRangeError`; added IMPL-01, UI-01,
  ERR-02. All original identifiers retained.
- README rewritten for D2 (run command, from-scratch explanation, error guide, structure).

### Retained
- `src/cli.py` — the Deliverable 1 command-line prototype, kept as a reference/regression
  baseline. Beta accuracy is unchanged (worst relative error 1.17×10⁻¹⁴).

## [0.1.0] — 2026-07-15 — Deliverable 1

### Added
- Repository scaffold, decision log, GAI prompt log, and bibliography.
- Research notes, persona (Maya Fernandes), requirements baseline v0.1, two algorithms in
  pseudocode, algorithm-selection mind map, and the CLI prototype (`src/cli.py`,
  Algorithm B) with a verification matrix and harness (`tests/verify_d1.py`, 15/15).

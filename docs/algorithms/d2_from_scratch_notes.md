# Deliverable 2 — "From-Scratch" Boundary (Problem 5.1, frozen)

**Problem 5 rule.** *Apart from functions related to input, output, arithmetic,
and user-interface design, the implementation is prohibited from using any
built-in or library functions provided by Python.* This document is the frozen
interpretation of that rule for F6 (decision **D-008**), the dependency
inventory, and the list of subordinate functions implemented manually.

---

## 1. Dependency inventory of the D1 prototype (`src/cli.py`)

The D1 CLI implements the **selected Algorithm B** (Gamma identity, log-domain
Lanczos `lnΓ`). Its Beta-specific logic (Lanczos series, log-domain combination,
validation) was **already hand-written**; only elementary primitives were
borrowed from `math`.

| `math` call | Used in | Role | D2 from-scratch replacement |
|-------------|---------|------|-----------------------------|
| `math.log` | `ln_gamma` (Lanczos + reflection) | natural logarithm | `elementary.ln` — range reduction `x = m·2^e` + atanh series |
| `math.exp` | `beta` (final `exp` of log-sum) | exponential | `elementary.exp` — range reduction `x = k·ln2 + r` + Taylor series |
| `math.sin` | `ln_gamma` reflection (z < 0.5) | reflection formula | `elementary.sin` — argument reduction + Taylor series |
| `math.pi` (constant) | reflection formula | π | `elementary.PI` — hard-coded correctly-rounded double |
| `math.isfinite` | REL-02 guard | overflow/NaN check | `elementary.is_finite` — IEEE comparison, not numerical work |

No call to `math.gamma`, `math.lgamma`, or any `beta` was ever used — those
would defeat the exercise.

## 2. Classification of every facility the D2 build uses

**Retained (explicitly permitted categories):**

| Facility | Category | Justification |
|---|---|---|
| `+ - * / // % **(int)`, comparisons | **arithmetic** | Core permitted category. `**` used only with an integer exponent (repeated multiplication). |
| `int(...)`, `float(...)` casts | **arithmetic / input parsing** | Numeric conversion and text→number parsing (input). No mathematics performed. |
| `str.strip`, f-string formatting | **input / output** | Reading fields and presenting results (`format_result`). |
| `tkinter`, `tkinter.ttk` | **user-interface design** | Explicitly required by Problem 5 ("GUI using Tkinter"). |
| `Exception` / `raise` / class defs | **language + UI** | Exception handling is explicitly required by Problem 5. |
| `range`, `while`, `for` | **language control flow** | Not mathematical functions. |

**Prohibited and therefore reimplemented (subordinate functions):**

| Subordinate function | Module | Method | Accuracy (vs. oracle) |
|---|---|---|---|
| `ln(x)` | `elementary.py` | range reduction + atanh series | worst rel. err. ≤ 6×10⁻¹⁶ |
| `exp(x)` | `elementary.py` | range reduction + Taylor series | worst rel. err. ≤ 6×10⁻¹⁵ |
| `sin(x)` | `elementary.py` | argument reduction + Taylor series | worst abs. err. ≤ 9×10⁻¹⁶ |
| `|x|`, `floor`, `round`, `is_finite` | `elementary.py` | sign/compare/cast only | exact |

Derivations and pseudocode: [`elementary_functions.md`](elementary_functions.md).

## 3. Verification of the boundary

`tests/verify_d2.py` check **IMPL-01** scans every shipped source file
(`elementary`, `beta_core`, `validation`, `gui`, `exceptions`) and fails if any
of them imports `math`, `numpy`, `scipy`, `mpmath`, or `cmath`. The accuracy of
each reimplemented primitive is confirmed against Python's `math` **used only as
a test oracle** (never imported by shipped code). Result: **27/27 checks pass**;
the Beta core reproduces the D1 accuracy exactly (worst ACC-01 rel. err.
**1.17×10⁻¹⁴**).

## 4. Consequence

The from-scratch effort reduced to three elementary functions (`ln`, `exp`,
`sin`) plus the constant π and a finiteness test — exactly the trade-off
recorded against Algorithm B in the selection mind map (decision **D-004**),
accepted because B is the only candidate meeting ACC-01 uniformly. The Lanczos
coefficient sum and the `B = exp(lnΓ(x)+lnΓ(y)−lnΓ(x+y))` combination are
original code carried over from D1 unchanged.

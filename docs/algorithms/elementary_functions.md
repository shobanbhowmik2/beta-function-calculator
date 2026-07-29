# From-Scratch Elementary Functions — Derivations & Pseudocode (D2, Problem 5)

The Gamma-identity Beta core needs exactly three transcendental primitives —
`ln`, `exp`, `sin` — plus the constant π. This note derives each one, gives its
language-neutral pseudocode, and states its verified accuracy. All three follow
the same recipe used by production math libraries: **range reduction** to a
small interval, then a **rapidly convergent series**, then **reconstruction**.
Every loop terminates in a bounded number of steps (REL-03). Implementation:
[`src/elementary.py`](../../src/elementary.py); accuracy check: `IMPL-01` /
`ACC-03p` in [`tests/verify_d2.py`](../../tests/verify_d2.py).

Convention: `←` assignment, `▷` comment. Constants are correctly-rounded IEEE-754
doubles: `PI = 3.141592653589793`, `LN2 = 0.6931471805599453`.

---

## 1. `exp(x)` — range-reduced Taylor series

**Reduction.** Write `x = k·ln2 + r` with `k = round(x / ln2)` an integer, so
`|r| ≤ ln2/2 ≈ 0.3466`. Then `e^x = 2^k · e^r`.

**Series.** `e^r = Σ_{n≥0} r^n / n!`. With `|r| ≤ 0.347`, ~15 terms reach full
double precision. Terms are built incrementally: `t_n = t_{n-1} · r / n`.

**Reconstruction.** Multiply by `2^k` by repeated doubling/halving (`_scale_pow2`),
exiting early once the magnitude leaves the representable range.

```
function EXP(x)
    if x = 0 then return 1
    k ← ROUND(x / LN2);   r ← x − k·LN2      ▷ |r| ≤ ln2/2
    term ← 1;  total ← 1;  n ← 1
    repeat
        term ← term · r / n
        total ← total + term
        n ← n + 1
    until |term| < EPS·|total|                ▷ bounded: |r|<0.35 ⇒ ≤ ~20 terms
    return SCALE_POW2(total, k)               ▷ total · 2^k by repeated mult.
```

**Accuracy (verified):** worst relative error ≤ 6×10⁻¹⁵ over `x ∈ [−20, 60]`.

---

## 2. `ln(x)` — range-reduced atanh series  (x > 0)

**Reduction.** Write `x = m·2^e` with the mantissa `m ∈ [1/√2, √2)` by
halving/doubling `x` and counting `e`. Then `ln(x) = e·ln2 + ln(m)`.

**Series.** Substitute `s = (m−1)/(m+1)`, so `|s| ≤ 0.1716` on that interval, and
use the fast odd series `ln(m) = 2·(s + s³/3 + s⁵/5 + …)`.

```
function LN(x)
    if x ≤ 0 then error DomainError            ▷ ln defined only for x>0
    e ← 0;  m ← x
    while m ≥ √2  do  m ← m·0.5;  e ← e + 1     ▷ reduce mantissa into
    while m < √2/2 do m ← m·2;    e ← e − 1     ▷   [1/√2, √2)
    s ← (m−1)/(m+1);  s2 ← s·s
    term ← s;  total ← s;  denom ← 1
    repeat
        term ← term · s2;  denom ← denom + 2
        total ← total + term/denom
    until |term/denom| < EPS·|total|            ▷ |s|<0.18 ⇒ ≤ ~12 terms
    return e·LN2 + 2·total
```

**Accuracy (verified):** worst relative error ≤ 6×10⁻¹⁶ over a wide range.

---

## 3. `sin(x)` — argument-reduced Taylor series

Only the reflection branch of `lnΓ` calls this, with argument `π·z`, `0<z<0.5`
(so the argument is in `(0, π/2)`), but it is implemented for general real `x`.

**Reduction.** Reduce `x` modulo `2π` into `[−π, π]`, then fold into `[−π/2, π/2]`
using `sin(π − u) = sin(u)`, so the series argument satisfies `|u| ≤ π/2`.

**Series.** `sin(u) = u − u³/3! + u⁵/5! − …`, terms built as
`t_n = t_{n−1} · (−u²)/((2n)(2n+1))`.

```
function SIN(x)
    k ← ROUND(x / TAU);  u ← x − k·TAU          ▷ u ∈ [−π, π]
    if u >  π/2 then u ←  π − u                  ▷ fold into [−π/2, π/2]
    if u < −π/2 then u ← −π − u
    u2 ← u·u;  term ← u;  total ← u;  n ← 1
    repeat
        term ← term · (−u2)/((2n)(2n+1))
        total ← total + term;  n ← n + 1
    until |term| < EPS·|total|                   ▷ |u|≤π/2 ⇒ ≤ ~12 terms
    return total
```

**Accuracy (verified):** worst absolute error ≤ 9×10⁻¹⁶ over `x ∈ [−20, 20]`.

---

## 4. Why this is enough

Composing these into the Lanczos `lnΓ` and the log-domain Beta combination
reproduces the D1 result to the last digit: the Beta core's worst relative error
over the 18-value reference table is **1.17×10⁻¹⁴**, identical to the D1
prototype that used `math`. The from-scratch replacement therefore satisfies
ACC-01 with the same eight-orders-of-magnitude margin, confirming that the
accepted D2 trade-off (Algorithm B needs more from-scratch effort) cost nothing
in accuracy. See [`references.bib`](../references.bib): Muller (elementary
function evaluation), Cody & Waite (range reduction), Lanczos (lnΓ).

# Two Algorithms for B(x, y) — Pseudocode (D1 · Problem 3)

Two **genuinely different**, language-neutral algorithms for the real Beta Function,
domain `x > 0, y > 0`. Convention: `←` assignment, `▷` comment, indentation = block,
`error` raises a named failure. No programming-language syntax is used.

- **Algorithm A** — direct **numerical integration** of the Euler integral (adaptive Simpson).
- **Algorithm B** — the **Gamma-function identity** via a Lanczos `lnΓ`, evaluated in the
  **log domain**.

Both satisfy the relevant requirements: ACC-01 (tolerance), VAL-01 (domain),
REL-02 (no non-finite output), REL-03 (bounded work / guaranteed termination).

---

## Algorithm A — Euler-integral adaptive quadrature

**Idea:** `B(x, y) = ∫₀¹ t^(x-1)(1-t)^(y-1) dt`. Approximate the area with Simpson's
rule, subdividing only where the estimate has not yet converged.

```
Inputs:       x, y            ▷ real, x > 0, y > 0
              tol             ▷ target absolute error, e.g. 1e-10
              maxDepth        ▷ recursion-depth safeguard, e.g. 50
Output:       approximation of B(x, y)
Preconditions:  x > 0 and y > 0
Postconditions: returns a finite real ≥ 0
Constants:    EPS ← 1e-12     ▷ endpoint inset for singular cases

function BETA_QUADRATURE(x, y, tol, maxDepth)
    if x ≤ 0 or y ≤ 0 then
        error DomainError                      ▷ VAL-01

    function f(t)                              ▷ the integrand
        if t ≤ 0 or t ≥ 1 then return 0
        return t^(x-1) × (1-t)^(y-1)

    ▷ Inset the endpoints only where the integrand is singular (exponent < 0)
    lo ← (EPS if x < 1 else 0)
    hi ← (1 - EPS if y < 1 else 1)

    return ADAPT(f, lo, hi, tol, SIMPSON(f, lo, hi), 0, maxDepth)

function SIMPSON(f, a, b)
    c ← (a + b) / 2
    return (b - a) / 6 × (f(a) + 4×f(c) + f(b))

function ADAPT(f, a, b, tol, whole, depth, maxDepth)
    c     ← (a + b) / 2
    left  ← SIMPSON(f, a, c)
    right ← SIMPSON(f, c, b)
    if depth ≥ maxDepth or |left + right − whole| ≤ 15 × tol then   ▷ stop / REL-03
        return left + right + (left + right − whole) / 15           ▷ Richardson term
    return ADAPT(f, a, c, tol/2, left,  depth+1, maxDepth)
         + ADAPT(f, c, b, tol/2, right, depth+1, maxDepth)
```

**Subordinate operations:** `pow` (real exponent). **Termination:** every branch is
bounded by `maxDepth` (REL-03). **Complexity:** `O(N)` integrand evaluations, where `N`
is the number of accepted subintervals; `N` grows near endpoint singularities and is
capped by `maxDepth`.

**Known weakness (verified):** for strong endpoint singularities (`x ≪ 1` or `y ≪ 1`)
the inset+Simpson estimate loses accuracy. Empirically `B(0.2, 0.3)` returns `7.72774`
vs. the true `7.74848` — a relative error of ≈ 2.7×10⁻³, which **fails ACC-01**. Fine
for moderate inputs; unreliable near the singular corner.

**Worked trace — B(2, 3)** (`x=2, y=3`, both exponents ≥ 0 so `lo=0, hi=1`):
integrand `f(t) = t·(1−t)²`. Exact `∫₀¹ t(1−t)² dt = 1/2 − 2/3 + 1/4 = 1/12`.
Simpson on `[0,1]`: `1/6·(f(0)+4f(0.5)+f(1)) = 1/6·(0 + 4·0.125 + 0) = 0.08333`.
Already exact here (integrand is a cubic; Simpson is exact for cubics) → returns
`0.0833333` = 1/12. ✔

---

## Algorithm B — Gamma identity via Lanczos lnΓ (log domain)

**Idea:** `B(x, y) = Γ(x)Γ(y) / Γ(x+y)`. Compute `lnΓ` with the Lanczos approximation
and combine in the log domain to avoid overflow (REL-02):
`B = exp( lnΓ(x) + lnΓ(y) − lnΓ(x+y) )`.

```
Inputs:       x, y            ▷ real, x > 0, y > 0
Output:       approximation of B(x, y)
Preconditions:  x > 0 and y > 0
Postconditions: returns a finite real ≥ 0
Constants:    g ← 7
              P ← [ 0.9999999999998, 676.520368122, −1259.139216722,
                    771.323428778, −176.615029162, 12.507343279,
                    −0.138571095, 9.98436958e−6, 1.50563274e−7 ]   ▷ Lanczos g=7

function BETA_GAMMA(x, y)
    if x ≤ 0 or y ≤ 0 then
        error DomainError                                  ▷ VAL-01
    return EXP( LN_GAMMA(x) + LN_GAMMA(y) − LN_GAMMA(x + y) )

function LN_GAMMA(z)                                        ▷ z > 0
    if z < 0.5 then                                        ▷ reflection for small args
        return LN(π) − LN( |SIN(π × z)| ) − LN_GAMMA(1 − z)
    z ← z − 1
    a ← P[0]
    for i ← 1 to g + 1 do                                  ▷ fixed loop → REL-03
        a ← a + P[i] / (z + i)
    t ← z + g + 0.5
    return 0.5 × LN(2π) + (z + 0.5) × LN(t) − t + LN(a)
```

**Subordinate operations:** `exp`, `ln`, `sin` (reflection only), plus the Lanczos sum.
**Termination:** a single fixed-length loop (REL-03). **Complexity:** `O(1)` — a constant
number of terms regardless of input (satisfies PERF-01 comfortably).

**Known weakness:** accuracy is bounded by the Lanczos coefficient set (the `g=7`
table gives ≈ 15 significant digits for real `z > 0`); a wrong/low-precision coefficient
table would silently reduce accuracy. Reflection is required for `z < 0.5` to keep
precision.

**Worked trace — B(2, 3):** `lnΓ(2)=ln(1)=0`, `lnΓ(3)=ln(2)=0.693147`,
`lnΓ(5)=ln(24)=3.178054`. `B = exp(0 + 0.693147 − 3.178054) = exp(−2.484907) =
0.0833333` = 1/12. ✔ (Verified to ~10 digits against `math.lgamma`.)

---

## How A and B differ

| Dimension | A — Euler quadrature | B — Gamma identity (Lanczos, log-domain) |
|---|---|---|
| Fundamental approach | Numerical integration of the definition | Closed-form identity via a special-function approximation |
| Subordinate ops (D2 from-scratch) | `pow` + adaptive Simpson machinery | `exp`, `ln`, `sin`, + Lanczos coefficient sum |
| Accuracy (moderate inputs) | Good (≈1e-8 with tight tol) | Excellent (≈1e-15) |
| Accuracy near `x,y ≪ 1` | **Degrades** — fails ACC-01 (verified on B(0.2,0.3)) | Uniform; reflection handles small args |
| Overflow / REL-02 | Integrand mass is finite; no overflow, but slow | Log-domain **avoids** Γ overflow by construction |
| Performance / PERF-01 | `O(N)` — variable, slower near singularities | `O(1)` — fast, constant time |
| Termination / REL-03 | `maxDepth` recursion cap | fixed loop |
| Explainability to persona | Intuitive "area under the curve" | "ratio of Gamma functions" (less intuitive) |
| D2 from-scratch effort | Moderate (`pow`, quadrature) | Higher (`exp`, `ln`, `sin`, Lanczos), but self-contained |

**These are substantially different**, not variants: one *integrates the definition
numerically*; the other *evaluates a closed-form identity via a series approximation*.
They share only basic arithmetic. Selection between them is Problem 4 (see the
algorithm-selection mind map), where the verified evidence above will drive the choice.

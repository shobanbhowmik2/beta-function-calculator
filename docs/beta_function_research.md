# Beta Function B(x, y) — Research Notes (D1 · Step 1)

Purpose: build enough mathematical and application understanding to write the persona
and requirements responsibly, and to establish trusted reference values for verifying
the implementation later. Scope: **real** Beta Function, domain **x > 0, y > 0**
(pending professor confirmation — see decision D-001).

> All decimal values below are approximations of the exact closed forms shown beside
> them. Closed forms (fractions and multiples of π) are exact and safe to use as test
> oracles. The two non-closed-form values (B(10,10), B(0.2,0.3)) were **verified with
> `math.lgamma`** — `B = exp(lnΓ(x)+lnΓ(y)−lnΓ(x+y))`.
>
> Note: `lgamma` is used here **only to generate trusted oracle values for testing**;
> it is not part of the delivered implementation. The D2 "from scratch" prohibition
> applies to the product code, not to independently establishing expected test results.

---

## 1. Definitions

**Euler integral (first kind):**
```
B(x, y) = ∫₀¹ t^(x-1) · (1 - t)^(y-1) dt,     x > 0, y > 0
```
The integral converges (is finite) precisely when x > 0 and y > 0.

**Gamma-function identity:**
```
B(x, y) = Γ(x) · Γ(y) / Γ(x + y)
```
This is the most common computational route, but note the overflow risk in §5.

**Trigonometric form (useful for verification):**
```
B(x, y) = 2 · ∫₀^{π/2} (sin θ)^(2x-1) · (cos θ)^(2y-1) dθ
```

---

## 2. Key properties and identities

- **Symmetry:** `B(x, y) = B(y, x)`. (Lets us always compute with, say, the larger
  argument in a chosen position for stability.)
- **Unit argument:** `B(x, 1) = 1/x`  and  `B(1, y) = 1/y`.
- **Integer case (factorials):** for positive integers m, n,
  `B(m, n) = (m-1)! (n-1)! / (m+n-1)!`.
- **Recurrence:** `B(x, y+1) = B(x, y) · y/(x+y)`  and  `B(x+1, y) = B(x, y) · x/(x+y)`.
- **Additive:** `B(x, y) = B(x+1, y) + B(x, y+1)`.
- **Relation to binomial coefficient:** `1 / ((n+1)·B(k+1, n-k+1)) = C(n, k)`.

---

## 3. Reference values (test oracles)

Exact closed forms first (safe), then a purely-numeric stress case.

| x | y | Exact form | Decimal (approx.) | Why it's a good test |
|---|---|-----------|-------------------|----------------------|
| 1 | 1 | 1 | 1.000000000 | Trivial base case |
| 1 | 2 | 1/2 | 0.500000000 | `B(1,y)=1/y` |
| 2 | 1 | 1/2 | 0.500000000 | Symmetry check vs (1,2) |
| 2 | 2 | 1/6 | 0.166666667 | Small integers |
| 2 | 3 | 1/12 | 0.083333333 | Given in the task plan |
| 3 | 2 | 1/12 | 0.083333333 | Symmetry check vs (2,3) |
| 2 | 4 | 1/20 | 0.050000000 | Integer factorial form |
| 3 | 3 | 1/30 | 0.033333333 | Integer factorial form |
| 4 | 3 | 1/60 | 0.016666667 | Larger integers |
| 5 | 3 | 1/105 | 0.009523810 | Larger integers |
| 0.5 | 0.5 | π | 3.141592654 | Half-integers; `Γ(½)²=π` |
| 0.5 | 1 | 2 | 2.000000000 | `B(1,y)=1/y` → 1/0.5 |
| 0.5 | 2 | 4/3 | 1.333333333 | Half-integer × integer |
| 1.5 | 0.5 | π/2 | 1.570796327 | Half-integers |
| 1.5 | 1.5 | π/8 | 0.392699082 | Half-integers |
| 2.5 | 1.5 | π/16 | 0.196349541 | Half-integers, x+y=4 |
| 10 | 10 | (9!)²/19! | 1.0825088224469 × 10⁻⁶ | Small result / large args → log-domain needed |
| 0.2 | 0.3 | — | 7.748481388737 | Endpoint-singularity stress (both < 1) |

Derivations of the half-integer cases (for the report):
`B(0.5,0.5)=Γ(½)²/Γ(1)=π`; `B(1.5,1.5)=(√π/2)²/Γ(3)=(π/4)/2=π/8`;
`B(2.5,1.5)=((3/4)√π)((1/2)√π)/Γ(4)=(3π/8)/6=π/16`.

---

## 4. Applications / user contexts (feeds the persona)

- **Statistics / Bayesian inference:** normalizing constant of the **Beta distribution**
  `Beta(α, β)`; conjugate prior for the binomial/Bernoulli parameter.
- **Order statistics:** distribution of the k-th order statistic of a uniform sample.
- **Combinatorics:** binomial coefficients via the integer identity above.
- **Physics:** the Veneziano amplitude (early string theory) is a Beta function.
- **Numerical analysis / probability:** appears in Student-t, F, and χ² distributions
  (via the regularized incomplete Beta), so a Beta primitive is a common building block.

Two realistic user contexts (for the persona, task D1-P1.3):
1. A **statistics / data-science student** computing Beta-distribution normalizing
   constants or checking coursework, wanting a quick trustworthy value without SciPy.
2. An **engineering / research assistant** needing occasional special-function values
   and unsure which inputs are valid, who values clear error messages over raw speed.

---

## 5. Numerical risks (feeds requirements, algorithms, error handling)

- **Endpoint singularities:** the integrand `t^(x-1)(1-t)^(y-1)` diverges at `t=0` when
  `x < 1`, and at `t=1` when `y < 1`. The integral is still finite (integrable
  singularity), but **naïve fixed-step quadrature loses accuracy** near the ends. →
  motivates adaptive quadrature, a variable transform, or the Gamma route.
- **Overflow via the Gamma identity:** `Γ(x)`, `Γ(y)`, and `Γ(x+y)` each overflow for
  moderately large arguments (e.g. `Γ(171)` overflows IEEE double) **even when the ratio
  `B(x,y)` is perfectly representable**. → compute in the **log domain**:
  `B(x,y) = exp( lnΓ(x) + lnΓ(y) − lnΓ(x+y) )`.
- **Underflow:** `B(x,y)` becomes extremely small for large `x+y` (see B(10,10) above);
  formatting must not imply more precision than achieved.
- **Slow convergence:** quadrature near singular endpoints may need many subdivisions →
  requires a maximum-work safeguard and a convergence/tolerance stopping rule.
- **Precision loss / cancellation:** less severe here than in series methods, but result
  formatting should state the achieved precision honestly.
- **Invalid domain:** `x ≤ 0` or `y ≤ 0` (poles of Γ at non-positive integers; integral
  diverges) must be rejected with a helpful message, not silently returned.

Implication for D2 "from scratch": whichever route is chosen, the subordinate functions
(`exp`, `ln`, `pow`, and `Γ`/`lnΓ` or the quadrature machinery) will have to be
implemented manually, since library special functions are prohibited.

---

## 6. Sources to cite (see `references.bib`)

- ISO/IEC/IEEE 29148 (requirements) — already in `.bib`.
- Abramowitz & Stegun, *Handbook of Mathematical Functions* — Beta/Gamma definitions
  and tables (already in `.bib`).
- **NIST DLMF** (Digital Library of Mathematical Functions), §5.12 (Beta function) —
  **[add to `.bib` and cite]**.
- A numerical-methods reference for adaptive quadrature and a Lanczos-approximation
  source will be needed once the algorithm is chosen (P3/P4).

> **Status:** all reference values in `reference_values.csv` are trusted — closed forms
> are exact, and B(10,10) and B(0.2,0.3) were verified with `math.lgamma`. When the
> algorithm is chosen (P3/P4), add the specific quadrature and Lanczos-approximation
> sources to `references.bib`.

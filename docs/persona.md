# Primary Persona — Beta Function Calculator (D1 · Problem 1)

**Template chosen:** Goal-directed (Cooper-style), trimmed to a one-page card, with
proto-persona-style **explicit labelling of evidence vs. assumption**. Selection is
justified in the mind map: [`docs/mindmaps/persona_template_selection.png`](mindmaps/persona_template_selection.png)
(editable source: `persona_template_selection.dot`). See decision **D-005**.

> **Evidence basis:** No interviews were conducted, so this is a *synthesised* persona.
> Each attribute is tagged **[E]** evidence-based (from the domain research and typical
> user contexts), **[S]** reasonable synthesis, or **[A]** explicit assumption.
> The persona does **not** claim to be a real interviewed person.

---

## Persona card

| Field | Value |
|---|---|
| **Name** | Maya Fernandes |
| **Pronouns** | she/her |
| **Age** | 24 **[A]** |
| **Role** | MSc Statistics / Data Science student; part-time research assistant **[S]** |
| **Experience** | Strong in statistics & calculus; comfortable with formulas; *moderate* Python; *low* comfort with special-function libraries and the command line **[S]** |
| **Education** | BSc Mathematics; currently in a graduate statistics program **[A]** |
| **Environment** | Personal laptop (macOS/Windows); works in spreadsheets and occasional Jupyter notebooks; not a software developer **[S]** |
| **Platforms/tools** | Excel/Google Sheets, some Python; avoids installing heavy libraries (e.g. SciPy) for a one-off value **[S]** |

### Goals **[E/S]**
- **G1** Get a **quick, trustworthy** value of `B(x, y)` (e.g. a Beta-distribution
  normalizing constant) without writing code. **[E]** — from research §4 applications.
- **G2** **Verify coursework / hand calculations** against a reliable tool. **[S]**
- **G3** Understand **which inputs are valid** so she trusts the result. **[E]** — the
  domain `x>0, y>0` is a real source of confusion (research §5).

### Typical tasks **[S]**
- Compute `B(α, β)` for Beta-distribution parameters while doing assignments.
- Spot-check a value she derived by hand (e.g. `B(2,3)=1/12`).
- Occasionally try fractional inputs (e.g. `B(0.5, 0.5)=π`).

### Needs & pain points **[E/S]**
- **N1** Doesn't know the valid input range; unsure if `0` or negative values are
  allowed. **[E]**
- **N2** Existing tools give **cryptic errors** or, worse, wrong/`inf` values for large
  inputs. **[E]** — the Gamma-overflow risk (research §5).
- **N3** Wants results **stated to a clear precision**, not misleadingly many digits. **[S]**
- **N4** Low command-line comfort — needs **plain labels and instructions**, not
  cryptic symbols. **[S]**
- **N5** Occasionally uses a screen reader / larger fonts; needs **feedback that isn't
  colour-only** and is readable. **[A]**
- **N6** Doesn't want to install a library or write code for a single value. **[S]**

### Usage scenario **[S]**
> Maya is checking a Bayesian statistics assignment. She needs the normalizing
> constant `1/B(2, 5)` for a `Beta(2,5)` prior. She opens the calculator, reads the hint
> that both inputs must be greater than 0, enters `x = 2` and `y = 5`, and reads
> `B(2,5) = 0.0119048` with a stated precision. She then tries `x = 0` by mistake and
> gets a clear message — "x must be greater than 0" — instead of a crash, corrects it,
> and moves on. She never had to open a Python interpreter.

---

## Traceability: persona needs → requirements (≥5 required)

These seed the Problem 2 requirements (IDs are provisional until P2 freezes them).

| Persona driver | Implied requirement (provisional ID) |
|---|---|
| G3, N1 | **VAL-01 / DOC-01** — reject `x ≤ 0` or `y ≤ 0`; show the valid domain as an on-screen hint |
| G1, G2 | **FR-01 / ACC-01** — compute `B(x,y)` and display it within a stated, measurable tolerance |
| N2 | **REL-01** — handle large/asymmetric inputs without returning `inf`/crashing (log-domain evaluation) |
| N3 | **ACC-02** — display the result to a documented precision; don't imply false precision |
| N4 | **USE-01** — plain-language prompts/labels and concise instructions |
| N5 | **ACC-03 (accessibility)** — feedback not conveyed by colour alone; readable output |
| N2, N1 | **ERR-01** — helpful, specific error messages (what went wrong + how to fix) |

**Gate check:** 7 needs/pains trace to requirements (≥5 required). ✔

---

## Attributes deliberately excluded
Hobbies, family, favourite brands, exact location, and personality quirks — none affect
the design of a single-function calculator (kept concise per the chosen template).

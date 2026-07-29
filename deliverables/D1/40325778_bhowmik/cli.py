#!/usr/bin/env python3
"""Beta Function Calculator — Deliverable 1 command-line prototype (SOEN 6011, F6).

Computes the real Beta function B(x, y) for x > 0, y > 0 using the *Gamma-function
identity* (Algorithm B from docs/algorithms/algorithms_pseudocode.md):

    B(x, y) = Gamma(x) * Gamma(y) / Gamma(x + y)

evaluated in the log domain via a Lanczos ln-Gamma approximation:

    B(x, y) = exp( lnGamma(x) + lnGamma(y) - lnGamma(x + y) )

Algorithm B was selected over Algorithm A (adaptive-Simpson quadrature of the Euler
integral) in Problem 4: it is accurate uniformly across the domain, runs in O(1)
time, and avoids Gamma overflow by construction, whereas A fails the ACC-01
tolerance near singular endpoints (verified on B(0.2, 0.3)). See the
algorithm-selection mind map in docs/mindmaps/.

Design note (29148 traceability): the computation core (`beta`, `beta_ln`,
`ln_gamma`) is deliberately kept free of any input/output code so it can be tested
independently (FR-02, ACC-01) and reused unchanged by the Deliverable 2 GUI. All
console interaction lives in the "I/O layer" section at the bottom.

D2 "from-scratch" note: this D1 prototype leans on three `math` primitives inside
`ln_gamma` — `math.log`, `math.exp`, and `math.sin` — plus the constant `math.pi`.
Those (and nothing else about the Beta computation) are what Deliverable 2 must
reimplement from scratch; the Lanczos series and the log-domain combination are
already hand-written here. See `MATH_CALLS_TO_REPLACE` and
docs/algorithms/algorithms_pseudocode.md.
"""

import math
import sys

# --------------------------------------------------------------------------- #
#  Documented constants (trace to the requirements baseline v0.1)             #
# --------------------------------------------------------------------------- #

DOMAIN_MIN = 0.0          # strict lower bound: x, y must be > 0            (VAL-01)
MAGNITUDE_CAP = 1.0e4     # supported magnitude bound: x, y <= 1e4  (VAL-04, A-04)
DISPLAY_SIG_FIGS = 6      # result shown to 6 significant figures    (ACC-02, D-007)

# `math` calls the Deliverable-2 "from scratch" build must replace. Documented
# here (DOC-01) so the obligation is explicit and greppable.
MATH_CALLS_TO_REPLACE = ("math.log", "math.exp", "math.sin", "math.pi")

# Lanczos coefficients, g = 7 (gives ~15 significant digits for real z > 0).
_LANCZOS_G = 7
_LANCZOS_P = (
    0.99999999999980993,
    676.5203681218851,
    -1259.1392167224028,
    771.32342877765313,
    -176.61502916214059,
    12.507343278686905,
    -0.13857109526572012,
    9.9843695780195716e-6,
    1.5056327351493116e-7,
)


# --------------------------------------------------------------------------- #
#  Computation core  —  NO input/output here (independently testable)         #
# --------------------------------------------------------------------------- #

def ln_gamma(z):
    """Natural log of Gamma(z) via the Lanczos approximation (g = 7).

    Uses the reflection formula for z < 0.5 to keep precision for small
    positive arguments. Only elementary primitives (log, exp, sin, pi) are
    used, so this is the single function Deliverable 2 must rebuild from
    scratch. `z` is assumed > 0 (guaranteed by the caller's domain check).
    """
    if z < 0.5:
        # Reflection: Gamma(z) * Gamma(1-z) = pi / sin(pi z).
        return math.log(math.pi / math.sin(math.pi * z)) - ln_gamma(1.0 - z)
    z -= 1.0
    a = _LANCZOS_P[0]
    for i in range(1, _LANCZOS_G + 2):          # fixed-length loop -> REL-03
        a += _LANCZOS_P[i] / (z + i)
    t = z + _LANCZOS_G + 0.5
    return 0.5 * math.log(2.0 * math.pi) + (z + 0.5) * math.log(t) - t + math.log(a)


def beta_ln(x, y):
    """Natural log of B(x, y). Log-domain form avoids Gamma overflow (REL-02)."""
    return ln_gamma(x) + ln_gamma(y) - ln_gamma(x + y)


def beta(x, y):
    """Real Beta function B(x, y) for x > 0, y > 0 (Algorithm B).

    Pure computation: raises ValueError for out-of-domain input and returns a
    finite non-negative float otherwise. Terminates in O(1) work (REL-03).
    """
    if x <= DOMAIN_MIN or y <= DOMAIN_MIN:
        raise ValueError("domain is x > 0 and y > 0")
    return math.exp(beta_ln(x, y))


# --------------------------------------------------------------------------- #
#  Input validation  —  turns raw text into a valid float or a clear reason   #
# --------------------------------------------------------------------------- #

class InputError(Exception):
    """Raised for user input that fails validation; message is user-facing."""


def parse_operand(raw, name):
    """Validate one operand string and return a float, else raise InputError.

    Enforces, in order: non-empty (VAL-03), numeric (VAL-02), positive
    (VAL-01), and within the magnitude cap (VAL-04). Every message says what
    was wrong and how to fix it (ERR-01), in text only (ACC-03).
    """
    text = raw.strip()
    if not text:
        raise InputError(f"{name} was empty. Enter a number greater than 0, e.g. 2.5")
    try:
        value = float(text)
    except ValueError:
        raise InputError(
            f"{name} = {raw!r} is not a number. Enter a decimal value, e.g. 2.5"
        )
    if not math.isfinite(value):
        raise InputError(f"{name} must be a finite number, not {raw!r}.")
    if value <= DOMAIN_MIN:
        raise InputError(
            f"{name} = {value:g} is outside the domain. This calculator supports "
            f"x > 0 and y > 0 only."
        )
    if value > MAGNITUDE_CAP:
        raise InputError(
            f"{name} = {value:g} exceeds the supported bound of {MAGNITUDE_CAP:g}. "
            f"Enter a value in (0, {MAGNITUDE_CAP:g}]."
        )
    return value


def format_result(value):
    """Format B(x, y) to the documented precision (6 sig figs, ACC-02)."""
    return f"{value:.{DISPLAY_SIG_FIGS}g}"


# --------------------------------------------------------------------------- #
#  I/O layer  —  console interaction only; delegates to the core above        #
# --------------------------------------------------------------------------- #

BANNER = """\
Beta Function Calculator  (SOEN 6011 F6, Deliverable 1 prototype)
Computes B(x, y) = integral_0^1 t^(x-1) (1-t)^(y-1) dt  for  x > 0, y > 0.
"""

HELP = f"""\
How to use:
  * Enter a value for x, then for y. Both must be real and > 0
    (supported range: 0 < x, y <= {MAGNITUDE_CAP:g}).
  * The result B(x, y) is shown to {DISPLAY_SIG_FIGS} significant figures.
  * Commands (at any prompt): 'h' help, 'q' quit.
Assumptions: real inputs only; domain x > 0, y > 0 (no analytic continuation).
Method: Gamma-identity via Lanczos ln-Gamma, evaluated in the log domain.
"""


def _read(prompt, stream):
    """Read one line, echoing the prompt. Returns None at end-of-input (EOF)."""
    sys.stdout.write(prompt)
    sys.stdout.flush()
    line = stream.readline()
    if line == "":            # EOF (Ctrl-D or piped input exhausted)
        return None
    return line.rstrip("\n")


def _read_operand(name, stream):
    """Prompt for one operand until it is valid, or a command / EOF ends it.

    Returns the float value, or the string 'quit' if the user asked to exit
    (or EOF was reached). Re-prompts on invalid input (FR-04, USE-01, VAL-03).
    """
    prompt = f"  {name} (> 0): "
    while True:
        raw = _read(prompt, stream)
        if raw is None:
            return "quit"
        cmd = raw.strip().lower()
        if cmd in ("q", "quit", "exit"):
            return "quit"
        if cmd in ("h", "help", "?"):
            sys.stdout.write(HELP)
            continue
        try:
            return parse_operand(raw, name)
        except InputError as err:
            # Helpful, specific message instead of a crash (ERR-01, REL-01).
            sys.stdout.write(f"  ! {err}\n")


def main(argv=None, stream=None):
    """Run the interactive calculator loop. Returns a process exit code."""
    stream = stream if stream is not None else sys.stdin
    sys.stdout.write(BANNER)
    sys.stdout.write("Type 'h' for help or 'q' to quit at any prompt.\n\n")

    while True:
        x = _read_operand("x", stream)
        if x == "quit":
            break
        y = _read_operand("y", stream)
        if y == "quit":
            break
        try:
            result = beta(x, y)
        except ValueError as err:
            # Defensive: the core rejected the input (should be pre-validated).
            sys.stdout.write(f"  ! Could not compute B(x, y): {err}\n\n")
            continue
        if not math.isfinite(result):        # guards REL-02
            sys.stdout.write(
                "  ! Result is not a finite number for these inputs; "
                "try smaller magnitudes.\n\n"
            )
            continue
        sys.stdout.write(
            f"  B({x:g}, {y:g}) = {format_result(result)}"
            f"   (to {DISPLAY_SIG_FIGS} significant figures)\n\n"
        )

    sys.stdout.write("Goodbye.\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

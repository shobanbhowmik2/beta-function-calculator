#!/usr/bin/env python3
"""From-scratch numerical core for the real Beta function B(x, y) (SOEN 6011, F6).

Deliverable 2, Problem 5. Computes

    B(x, y) = Gamma(x) * Gamma(y) / Gamma(x + y)     (Algorithm B, decision D-004)

in the log domain to avoid Gamma overflow (REL-02):

    B(x, y) = exp( lnGamma(x) + lnGamma(y) - lnGamma(x + y) ).

``lnGamma`` uses the Lanczos approximation (g = 7), which gives ~15 significant
digits for real z > 0, with the reflection formula for small arguments. The D1
prototype (``src/cli.py``) computed the same series but leaned on Python's
``math`` module for ln/exp/sin/pi. This module removes that dependency: it
imports **only** the hand-written elementary functions in ``elementary`` and
therefore performs no mathematics through a prohibited library call.

The core is intentionally free of any input/output or GUI code so it can be
tested in isolation (see ``tests/verify_d2.py``) and reused by both ``gui.py``
and ``cli.py``. It signals problems by raising the typed exceptions in
``exceptions``; it never prints.
"""

import elementary as el
from exceptions import DomainError, NumericalRangeError

# --------------------------------------------------------------------------- #
#  Documented constants (trace to the requirements baseline).                  #
# --------------------------------------------------------------------------- #

DOMAIN_MIN = 0.0          # strict lower bound: x, y must be > 0            (VAL-01)
MAGNITUDE_CAP = 1.0e4     # supported magnitude bound: x, y <= 1e4  (VAL-04, A-04)

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

# ln(2*pi) precomputed with the from-scratch logarithm (not a library call), so
# the Lanczos formula's constant term needs no runtime work.
_LN_TAU = el.ln(el.TAU)


# --------------------------------------------------------------------------- #
#  Computation core — NO input/output here (independently testable).          #
# --------------------------------------------------------------------------- #

def ln_gamma(z):
    """Natural log of Gamma(z) via the Lanczos approximation (g = 7).

    Uses the reflection formula Gamma(z)Gamma(1-z) = pi / sin(pi z) for z < 0.5
    to keep precision for small positive arguments. Only the from-scratch
    ``elementary`` primitives (ln, exp, sin, PI) are used. ``z`` is assumed > 0,
    which the public ``beta`` guarantees before calling.
    """
    if z < 0.5:
        # Reflection: lnGamma(z) = ln(pi) - ln(sin(pi z)) - lnGamma(1 - z).
        sin_term = el.sin(el.PI * z)
        return el.ln(el.PI) - el.ln(el.absolute(sin_term)) - ln_gamma(1.0 - z)

    z -= 1.0
    a = _LANCZOS_P[0]
    for i in range(1, _LANCZOS_G + 2):          # fixed-length loop -> REL-03
        a += _LANCZOS_P[i] / (z + i)
    t = z + _LANCZOS_G + 0.5
    return 0.5 * _LN_TAU + (z + 0.5) * el.ln(t) - t + el.ln(a)


def beta_ln(x, y):
    """Natural log of B(x, y). Log-domain form avoids Gamma overflow (REL-02)."""
    return ln_gamma(x) + ln_gamma(y) - ln_gamma(x + y)


def beta(x, y):
    """Real Beta function B(x, y) for x > 0, y > 0 (Algorithm B).

    Pure computation. Raises:

    * ``DomainError``          if x <= 0 or y <= 0 (VAL-01);
    * ``NumericalRangeError``  if the result is not a finite double (REL-02).

    Otherwise returns a finite, non-negative float in O(1) work (REL-03).
    """
    if x <= DOMAIN_MIN or y <= DOMAIN_MIN:
        raise DomainError(
            "The Beta function is only supported for x > 0 and y > 0. "
            "Please enter positive values for both x and y."
        )
    result = el.exp(beta_ln(x, y))
    if not el.is_finite(result):
        raise NumericalRangeError(
            "The result is too large or too small to represent as a finite "
            "number for these inputs. Try values with smaller magnitude."
        )
    return result

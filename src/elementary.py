#!/usr/bin/env python3
"""From-scratch elementary functions for the Beta Function Calculator (D2, F6).

Deliverable 2 (Problem 5) requires the function to be implemented "from
scratch": apart from input/output, arithmetic, and UI facilities, no built-in
or library functions may be used. The selected algorithm (Algorithm B, the
Gamma identity via a Lanczos ``lnGamma`` in the log domain) reduces the entire
mathematical dependency to three elementary primitives plus the constant pi:

    ln(x)      natural logarithm            (was math.log)
    exp(x)     exponential                  (was math.exp)
    sin(x)     sine, reflection formula     (was math.sin)
    PI         the constant pi              (was math.pi)

This module reimplements all four using nothing but arithmetic operators
(+ - * / // % and comparisons), integer/float casts for range reduction, and
Python control flow. **It never imports ``math`` (or any library that performs
the mathematics for us).** The accuracy of each routine is validated against a
trusted reference in ``tests/verify_d2.py``; the derivations are documented in
``docs/algorithms/elementary_functions.md``.

Every loop has a fixed or provably bounded iteration count (requirement
REL-03): the Taylor/atanh series stop when the next term is below the working
precision, and the power-of-two scaling stops as soon as the value under/
overflows the double-precision range.
"""

# --------------------------------------------------------------------------- #
#  Hard-coded constants (correctly rounded IEEE-754 doubles).                  #
#  These are *values*, not computed by a prohibited library call.             #
# --------------------------------------------------------------------------- #

PI = 3.141592653589793        # pi
TAU = 6.283185307179586       # 2*pi
HALF_PI = 1.5707963267948966  # pi/2
LN2 = 0.6931471805599453      # ln(2), the range-reduction step for exp/ln

# Series stop threshold: relative size below which the next term cannot change
# a double-precision result. 1e-18 is just under one ULP at magnitude 1.
_EPS = 1.0e-18

# Range-reduction bounds for ln: keep the mantissa in [1/sqrt(2), sqrt(2)) so
# the atanh series argument s = (m-1)/(m+1) satisfies |s| <= 0.1716 (fast).
_SQRT2 = 1.4142135623730951
_SQRT1_2 = 0.7071067811865476


# --------------------------------------------------------------------------- #
#  Small arithmetic helpers (implemented rather than borrowed).                #
# --------------------------------------------------------------------------- #

def absolute(value):
    """Absolute value of a real number (|value|), by sign test only."""
    return -value if value < 0.0 else value


def floor_int(value):
    """Largest integer <= value, returned as a Python int.

    ``int(value)`` truncates toward zero (an arithmetic cast); we correct
    downward for negatives so the result is a true floor.
    """
    truncated = int(value)
    if value < 0.0 and float(truncated) != value:
        truncated -= 1
    return truncated


def round_int(value):
    """Nearest integer to value (round half up), as a Python int."""
    return floor_int(value + 0.5)


def is_finite(value):
    """True iff value is neither an infinity nor a NaN.

    Uses only IEEE comparison identities, no library call: NaN is the only
    value not equal to itself, and the infinities are detected by comparison
    against a number at the top of the double range.
    """
    if value != value:                 # NaN
        return False
    if value > 1.7976931348623157e308:  # +inf
        return False
    if value < -1.7976931348623157e308:  # -inf
        return False
    return True


# --------------------------------------------------------------------------- #
#  exp(x) — range-reduced Taylor series.                                       #
# --------------------------------------------------------------------------- #

def _scale_pow2(value, k):
    """Return value * 2**k for integer k, using only multiplication/division.

    Doubling/halving in a loop, with an early exit as soon as the magnitude
    leaves the representable range (so the loop is effectively bounded to the
    ~1100 steps between overflow and underflow, satisfying REL-03).
    """
    if k > 0:
        while k > 0:
            value *= 2.0
            k -= 1
            if not is_finite(value) or value == 0.0:
                break
    elif k < 0:
        while k < 0:
            value *= 0.5
            k += 1
            if value == 0.0:
                break
    return value


def exp(x):
    """Exponential e**x for a real x, accurate to full double precision.

    Range reduction: write x = k*ln2 + r with k an integer and |r| <= ln2/2,
    so that e**x = 2**k * e**r and the Taylor series for e**r converges in a
    handful of terms. ``2**k`` is applied by repeated doubling (``_scale_pow2``).
    """
    if x != x:                     # NaN in -> NaN out (defensive)
        return x
    if x == 0.0:
        return 1.0

    # k = round(x / ln2); r = x - k*ln2  ->  |r| <= ln2/2 ~ 0.3466
    k = round_int(x / LN2)
    r = x - k * LN2

    # Taylor series e**r = sum_{n>=0} r**n / n!  (term_{n} = term_{n-1} * r / n)
    term = 1.0
    total = 1.0
    n = 1
    while True:
        term *= r / n
        total += term
        if absolute(term) < _EPS * absolute(total):
            break
        n += 1

    return _scale_pow2(total, k)


# --------------------------------------------------------------------------- #
#  ln(x) — range-reduced atanh series.                                         #
# --------------------------------------------------------------------------- #

def ln(x):
    """Natural logarithm ln(x) for x > 0, accurate to full double precision.

    Range reduction: write x = m * 2**e with the mantissa m in
    [1/sqrt(2), sqrt(2)), so ln(x) = e*ln2 + ln(m). On that interval the
    substitution s = (m-1)/(m+1) gives the rapidly convergent series
    ln(m) = 2*(s + s**3/3 + s**5/5 + ...), with |s| <= 0.1716.

    Raises ``ValueError`` for x <= 0 (the domain of ln); callers guarantee a
    positive argument, so this only fires on an internal logic error.
    """
    if x <= 0.0:
        raise ValueError("ln is defined only for x > 0")

    # Reduce the mantissa into [1/sqrt(2), sqrt(2)) by halving/doubling.
    e = 0
    m = x
    while m >= _SQRT2:
        m *= 0.5
        e += 1
    while m < _SQRT1_2:
        m *= 2.0
        e -= 1

    # atanh series for ln(m).
    s = (m - 1.0) / (m + 1.0)
    s2 = s * s
    term = s          # s**(2n+1) running term, starting at n = 0
    total = s
    denom = 1         # 2n+1
    while True:
        term *= s2
        denom += 2
        delta = term / denom
        total += delta
        if absolute(delta) < _EPS * absolute(total) + _EPS:
            break

    return e * LN2 + 2.0 * total


# --------------------------------------------------------------------------- #
#  sin(x) — argument-reduced Taylor series.                                    #
# --------------------------------------------------------------------------- #

def sin(x):
    """Sine of x (radians), accurate to full double precision.

    Only needed by the ``lnGamma`` reflection formula, where the argument is
    pi*z with 0 < z < 0.5 (so 0 < arg < pi/2), but implemented for a general
    real x. Reduce x modulo 2*pi into [-pi, pi], fold into [-pi/2, pi/2] via
    sin(pi - x) = sin(x), then sum the Taylor series
    sin(u) = u - u**3/3! + u**5/5! - ...
    """
    if x != x:                    # NaN in -> NaN out
        return x

    # Reduce modulo 2*pi into [-pi, pi].
    k = round_int(x / TAU)
    u = x - k * TAU
    # Fold into [-pi/2, pi/2] using sin(pi - u) = sin(u).
    if u > HALF_PI:
        u = PI - u
    elif u < -HALF_PI:
        u = -PI - u

    # Taylor series; term_{n} = term_{n-1} * (-u**2) / ((2n)(2n+1)).
    u2 = u * u
    term = u
    total = u
    n = 1
    while True:
        term *= -u2 / ((2 * n) * (2 * n + 1))
        total += term
        if absolute(term) < _EPS * (absolute(total) + _EPS):
            break
        n += 1

    return total

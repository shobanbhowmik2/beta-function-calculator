#!/usr/bin/env python3
"""Input validation and result formatting for the Beta Function Calculator (D2).

Turns the raw text a user types into a validated ``float`` — or into a typed,
helpful exception from ``exceptions``. This layer sits between the UI (console
or Tkinter) and the pure numerical core (``beta_core``), so both front-ends
share exactly one validation policy and one set of messages (ERR-01).

Validation order, per field, mirrors the requirements:

    1. non-empty            (VAL-03  -> EmptyInputError)
    2. parses as a number   (VAL-02  -> NonNumericError)
    3. finite               (VAL-02  -> NonFiniteError)
    4. strictly positive    (VAL-01  -> DomainError)
    5. within magnitude cap (VAL-04  -> RangeError)

Only input/output/arithmetic facilities are used here, so this file has no
bearing on the "from scratch" mathematical boundary.
"""

from beta_core import DOMAIN_MIN, MAGNITUDE_CAP
from elementary import is_finite
from exceptions import (
    DomainError,
    EmptyInputError,
    NonFiniteError,
    NonNumericError,
    RangeError,
)

DISPLAY_SIG_FIGS = 6      # result shown to 6 significant figures    (ACC-02, D-007)


def parse_operand(raw, name):
    """Validate one operand string and return a float, else raise a BetaError.

    ``name`` is the field label ("x" or "y") woven into every message so the
    user knows which field to fix. Each message says what was wrong *and* how
    to correct it (ERR-01).
    """
    text = raw.strip()

    if not text:
        raise EmptyInputError(
            f"{name} is empty. Enter a number greater than 0, for example 2.5."
        )

    try:
        value = float(text)
    except ValueError:
        raise NonNumericError(
            f"{name} = '{raw}' is not a number. Enter a decimal value such as "
            f"2, 0.5 or 3.75."
        )

    if not is_finite(value):
        raise NonFiniteError(
            f"{name} = '{raw}' is not a finite number. Enter an ordinary "
            f"decimal value such as 2.5 (not 'inf' or 'nan')."
        )

    if value <= DOMAIN_MIN:
        raise DomainError(
            f"{name} = {value:g} is outside the supported domain. This "
            f"calculator supports x > 0 and y > 0 only, so {name} must be "
            f"greater than 0."
        )

    if value > MAGNITUDE_CAP:
        raise RangeError(
            f"{name} = {value:g} exceeds the supported bound of "
            f"{MAGNITUDE_CAP:g}. Enter a value in the range 0 < {name} <= "
            f"{MAGNITUDE_CAP:g}."
        )

    return value


def format_result(value):
    """Format B(x, y) to the documented precision (6 significant figures).

    Kept to the achieved accuracy so the display never implies more precision
    than the method supports (ACC-02).
    """
    return f"{value:.{DISPLAY_SIG_FIGS}g}"

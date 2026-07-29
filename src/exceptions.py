#!/usr/bin/env python3
"""Custom exception hierarchy for the Beta Function Calculator (SOEN 6011, F6, D2).

Deliverable 2 requires explicit exception handling with *helpful* messages
(Problem 5). Rather than raise bare ``ValueError``s, the numerical core and the
input layer raise the typed exceptions defined here. Two properties matter:

* Every exception carries a user-facing ``message`` that states **what went
  wrong and how to fix it** (requirement ERR-01).
* The hierarchy lets the GUI catch categories separately (bad input vs. a
  numerical failure) and react appropriately, while a single ``except
  BetaError`` still guarantees no unhandled traceback reaches the user
  (REL-01).

Design note: these classes are deliberately free of any GUI or console code so
the numerical core stays independently testable (see ``beta_core`` and
``tests/verify_d2.py``).
"""


class BetaError(Exception):
    """Base class for every error this application raises deliberately.

    Catching ``BetaError`` catches all *expected* failures (bad input or a
    numerical limit) while letting genuinely unexpected programming errors
    propagate during development. The string form is the user-facing message.
    """

    def __init__(self, message):
        super().__init__(message)
        self.message = message


# --------------------------------------------------------------------------- #
#  Input / validation errors  (raised by validation.py before any computation) #
# --------------------------------------------------------------------------- #

class InputError(BetaError):
    """Base for anything wrong with the *text* the user supplied."""


class EmptyInputError(InputError):
    """A required field (x or y) was left blank (VAL-03)."""


class NonNumericError(InputError):
    """A field did not parse as a real decimal number (VAL-02)."""


class NonFiniteError(InputError):
    """A field parsed to a non-finite value such as ``inf`` or ``nan`` (VAL-02)."""


# --------------------------------------------------------------------------- #
#  Domain / range errors  (the value is a number, but not one we support)      #
# --------------------------------------------------------------------------- #

class DomainError(BetaError):
    """An input is outside the supported mathematical domain x > 0, y > 0
    (VAL-01). Raised by the numerical core and by validation."""


class RangeError(BetaError):
    """An input is numeric and positive but exceeds the supported magnitude
    bound (VAL-04), where results are no longer validated."""


# --------------------------------------------------------------------------- #
#  Numerical errors  (raised by the computation core, not the input layer)     #
# --------------------------------------------------------------------------- #

class NumericalError(BetaError):
    """Base for failures that occur *during* the computation itself."""


class NumericalRangeError(NumericalError):
    """The true result is not representable as a finite double for these
    inputs (overflow / underflow beyond the format), so no trustworthy value
    can be returned (REL-02)."""


class ConvergenceError(NumericalError):
    """A bounded iterative routine reached its work limit without meeting the
    accuracy target (REL-03). Present for completeness and future algorithms;
    the shipped Gamma-identity core terminates in fixed work and does not
    normally raise it."""

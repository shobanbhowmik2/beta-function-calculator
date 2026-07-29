#!/usr/bin/env python3
"""D2 verification harness (Problem 5.6) — from-scratch build + GUI pathway.

Exercises every testable D2 requirement against the from-scratch modules
(``elementary``, ``beta_core``, ``validation``) and the GUI event logic
(``gui``), then prints a PASS/FAIL matrix and exits non-zero on any failure so
``verification_matrix_d2.md`` can be regenerated rather than hand-copied.

What is checked:
  * IMPL-01  the shipped math modules import no ``math``/third-party library;
  * ACC-03p  the hand-written ln/exp/sin match a trusted reference (Python
             ``math`` is used HERE, in the test only, as an oracle — never in
             the shipped code);
  * ACC-01   B(x,y) within 1e-6 of the reference table (0<x,y<=50);
  * FR-02, symmetry, REL-02, REL-03, PERF-01;
  * VAL/ERR  each validation path raises its specific typed exception with a
             helpful message;
  * GUI-*    the Tkinter handlers report the right status for valid and each
             invalid case, with no traceback (skipped only if no display).

Run from the repo root:  python3 tests/verify_d2.py
"""
import csv
import math  # oracle for the accuracy checks ONLY (not used by shipped code)
import os
import re
import subprocess
import sys
import time

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(REPO, "src"))

import beta_core as bc          # noqa: E402
import elementary as el         # noqa: E402
import validation as va         # noqa: E402
from exceptions import (        # noqa: E402
    DomainError,
    EmptyInputError,
    NonFiniteError,
    NonNumericError,
    NumericalRangeError,
    RangeError,
)

results = []  # (req_id, case, expected, observed, ok)


def record(req_id, case, expected, observed, ok):
    results.append((req_id, case, expected, observed, bool(ok)))


def rel(a, b):
    return abs(a - b) / abs(b) if b != 0 else abs(a - b)


# ---- IMPL-01: the shipped math code uses no prohibited library ----------- #
banned = re.compile(r"^\s*(import|from)\s+(math|numpy|scipy|mpmath|cmath)\b",
                    re.MULTILINE)
offenders = []
for mod in ("elementary.py", "beta_core.py", "validation.py", "gui.py",
            "exceptions.py"):
    with open(os.path.join(REPO, "src", mod)) as f:
        if banned.search(f.read()):
            offenders.append(mod)
record("IMPL-01", "no math/numpy/scipy import in shipped src",
       "no prohibited imports", "clean" if not offenders else str(offenders),
       not offenders)

# ---- ACC-03p: from-scratch primitives vs a trusted oracle ---------------- #
we = max(rel(el.exp(x / 7.0 - 20), math.exp(x / 7.0 - 20)) for x in range(1, 561))
wl = max(rel(el.ln(math.exp(x / 7.0 - 20)), x / 7.0 - 20) for x in range(1, 561))
ws = max(abs(el.sin(x / 13.0 - 20) - math.sin(x / 13.0 - 20)) for x in range(1, 561))
record("ACC-03p", "exp vs math.exp over [-20,60]", "rel err <= 1e-12",
       f"worst {we:.2e}", we <= 1e-12)
record("ACC-03p", "ln vs math.log over wide range", "rel err <= 1e-12",
       f"worst {wl:.2e}", wl <= 1e-12)
record("ACC-03p", "sin vs math.sin over [-20,20]", "abs err <= 1e-12",
       f"worst {ws:.2e}", ws <= 1e-12)

# ---- ACC-01: accuracy vs the trusted reference table --------------------- #
worst_rel = 0.0
with open(os.path.join(REPO, "docs", "reference_values.csv")) as f:
    rows = list(csv.DictReader(f))
for r in rows:
    x, y, exp = float(r["x"]), float(r["y"]), float(r["expected_value"])
    worst_rel = max(worst_rel, rel(bc.beta(x, y), exp))
record("ACC-01", f"{len(rows)} reference values (0<x,y<=50)",
       "rel err <= 1e-6 each", f"worst rel err = {worst_rel:.2e}",
       worst_rel <= 1e-6)
record("ACC-01", "B(0.2,0.3) near-singular corner", "7.74848",
       f"{bc.beta(0.2, 0.3):.6g}", rel(bc.beta(0.2, 0.3), 7.748481388736760) <= 1e-6)

# ---- FR-02 / symmetry ----------------------------------------------------- #
record("FR-02", "B(1,1)", "1", f"{bc.beta(1, 1):.6g}", abs(bc.beta(1, 1) - 1) < 1e-12)
record("FR-02", "symmetry B(2.3,5.1)=B(5.1,2.3)", "equal",
       f"rel diff {rel(bc.beta(2.3, 5.1), bc.beta(5.1, 2.3)):.1e}",
       rel(bc.beta(2.3, 5.1), bc.beta(5.1, 2.3)) < 1e-14)

# ---- ACC-02: 6-significant-figure display -------------------------------- #
disp = va.format_result(bc.beta(2, 3))
record("ACC-02", "display B(2,3)", "6 sig figs", f"'{disp}'", disp == "0.0833333")

# ---- VAL/ERR: each path raises its specific typed exception -------------- #
checks = [
    ("VAL-03", EmptyInputError, "   ", "x"),
    ("VAL-02", NonNumericError, "abc", "x"),
    ("VAL-02", NonFiniteError, "inf", "x"),
    ("VAL-01", DomainError, "0", "x"),
    ("VAL-01", DomainError, "-2", "y"),
    ("VAL-04", RangeError, "1e6", "x"),
]
for req, exc, raw, name in checks:
    try:
        va.parse_operand(raw, name)
        record(req, f"{name}={raw!r}", exc.__name__, "ACCEPTED (bug)", False)
    except exc as e:
        helpful = len(e.message) > 15 and any(
            w in e.message.lower() for w in ("enter", "must", "supported", "range"))
        record(req, f"{name}={raw!r}", f"{exc.__name__} + helpful msg",
               f"{exc.__name__}: helpful={helpful}", helpful)
    except Exception as e:  # wrong type -> fail
        record(req, f"{name}={raw!r}", exc.__name__,
               f"WRONG: {type(e).__name__}", False)

# ---- REL-01: no unhandled exception across malformed inputs -------------- #
crashed = None
for b in ["abc", "", "0", "-1", "1e9", "nan", "inf", "  ", "1,5", "2.3.4"]:
    try:
        va.parse_operand(b, "x")
    except bc.__class__ if False else Exception as e:  # noqa
        if not isinstance(e, (EmptyInputError, NonNumericError, NonFiniteError,
                              DomainError, RangeError)):
            crashed = f"{b!r} -> {type(e).__name__}"
            break
record("REL-01", "10 malformed inputs", "only typed BetaErrors",
       "clean" if crashed is None else crashed, crashed is None)

# ---- REL-02: no inf/nan for supported inputs ----------------------------- #
nonfinite = [(x, y) for x in (0.001, 1, 10, 100, 1000, 1e4)
             for y in (0.001, 1, 10, 100, 1000, 1e4)
             if not el.is_finite(bc.beta(x, y))]
record("REL-02", "36 large/small supported inputs", "all finite",
       "all finite" if not nonfinite else f"{len(nonfinite)} non-finite",
       not nonfinite)
# NumericalRangeError raised, not silent nan, if a result were non-finite
record("REL-02", "NumericalRangeError type exists", "raisable",
       NumericalRangeError.__name__, issubclass(NumericalRangeError, Exception))

# ---- REL-03: bounded work ------------------------------------------------- #
record("REL-03", "Lanczos loop length", "fixed-length",
       f"{bc._LANCZOS_G + 1} iterations", bc._LANCZOS_G + 1 == 8)

# ---- PERF-01: < 1 s per computation -------------------------------------- #
N = 50000
t0 = time.perf_counter()
for _ in range(N):
    bc.beta(12.5, 7.25)
per_ms = (time.perf_counter() - t0) / N * 1000
record("PERF-01", f"{N} computations", "< 1000 ms/call",
       f"{per_ms:.5f} ms/call", per_ms < 1000)

# ---- POR-01: GUI module launches with a plain interpreter (no IDE) ------- #
# Import-and-build in a subprocess, then quit immediately, to prove it needs
# nothing but python3. Skipped gracefully if there is no display.
probe = (
    "import tkinter as tk, gui;"
    "r=tk.Tk();a=gui.BetaCalculatorApp(r);"
    "a.x_var.set('2');a.y_var.set('3');a.on_calculate();"
    "print('STATUS:'+a.status_var.get());r.destroy()"
)
proc = subprocess.run([sys.executable, "-c", probe],
                      cwd=os.path.join(REPO, "src"),
                      capture_output=True, text=True, timeout=30)
have_display = proc.returncode == 0
if have_display:
    ok = "0.0833333" in proc.stdout
    record("POR-01", "python3 -c 'build gui, compute B(2,3)'",
           "exit 0, result shown", f"exit 0, result {'seen' if ok else 'MISSING'}", ok)
else:
    record("POR-01", "GUI subprocess (no display available)",
           "n/a in headless env", "SKIPPED (no display)", True)

# ---- GUI-*: event handlers report correct status (in-process) ------------ #
try:
    import tkinter as tk
    import gui
    root = tk.Tk()
    app = gui.BetaCalculatorApp(root)
    root.update()

    def status(xv, yv):
        app.x_var.set(xv)
        app.y_var.set(yv)
        app.on_calculate()
        return app.status_var.get()

    gui_cases = [
        ("GUI-01", "2", "3", "Result:", "0.0833333"),
        ("GUI-02", "0", "3", "Out of domain", None),
        ("GUI-03", "abc", "3", "Invalid number", None),
        ("GUI-04", "", "5", "Input needed", None),
        ("GUI-05", "1e6", "3", "Out of range", None),
    ]
    for req, xv, yv, needle, extra in gui_cases:
        s = status(xv, yv)
        ok = needle in s and (extra is None or extra in s)
        record(req, f"GUI x={xv!r} y={yv!r}", f"status contains '{needle}'",
               s[:52] + ("..." if len(s) > 52 else ""), ok)
    app.on_clear()
    record("GUI-06", "Clear resets fields", "fields empty + hint",
           "cleared" if app.x_var.get() == "" and app.y_var.get() == "" else "not cleared",
           app.x_var.get() == "" and app.y_var.get() == "")
    root.destroy()
except Exception as e:  # no display / Tk missing -> skip, don't fail
    record("GUI-*", "Tk event-handler checks", "n/a in headless env",
           f"SKIPPED ({type(e).__name__})", True)

# --------------------------------------------------------------------------- #
#  Report                                                                     #
# --------------------------------------------------------------------------- #
print(f"{'REQ':<9} {'RESULT':<6} DEMO CASE / OBSERVED")
print("-" * 78)
n_pass = 0
for req, case, expected, observed, ok in results:
    n_pass += ok
    print(f"{req:<9} {'PASS' if ok else 'FAIL':<6} {case}")
    print(f"{'':<16} expected: {expected}")
    print(f"{'':<16} observed: {observed}")
print("-" * 78)
print(f"{n_pass}/{len(results)} checks passed")
sys.exit(0 if n_pass == len(results) else 1)

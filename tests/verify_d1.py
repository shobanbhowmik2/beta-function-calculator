#!/usr/bin/env python3
"""D1 verification harness (Problem 4.3) — requirement -> demo case -> result.

Exercises every *testable* requirement in requirements_baseline_v0.1.md against
the CLI's compute core and validation layer, plus a timing check for PERF-01 and
a subprocess check for POR-01 (runs from a terminal). Prints a PASS/FAIL matrix
and exits non-zero if anything fails, so the verification_matrix.md figures can
be regenerated and trusted rather than hand-copied.

Run from the repo root:  python3 tests/verify_d1.py
"""
import csv
import os
import subprocess
import sys
import time

REPO = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, os.path.join(REPO, "src"))

import cli  # noqa: E402  (path set above)

results = []  # (req_id, demo_case, expected, observed, ok)


def record(req_id, case, expected, observed, ok):
    results.append((req_id, case, expected, observed, bool(ok)))


def expect_input_error(req_id, case, raw, name="x"):
    """A validation requirement passes when parse_operand rejects `raw`."""
    try:
        cli.parse_operand(raw, name)
        record(req_id, case, "rejected", "ACCEPTED (bug)", False)
    except cli.InputError as e:
        record(req_id, case, "rejected w/ message", f"rejected: {str(e)[:38]}...", True)


# ---- ACC-01: accuracy vs the trusted reference table --------------------- #
worst_rel = 0.0
with open(os.path.join(REPO, "docs", "reference_values.csv")) as f:
    rows = list(csv.DictReader(f))
for r in rows:
    x, y, exp = float(r["x"]), float(r["y"]), float(r["expected_value"])
    got = cli.beta(x, y)
    rel = abs(got - exp) / abs(exp)
    worst_rel = max(worst_rel, rel)
record("ACC-01", f"{len(rows)} reference values (0<x,y<=50)",
       "rel err <= 1e-6 each", f"worst rel err = {worst_rel:.2e}", worst_rel <= 1e-6)

# spotlight case: the near-singular corner where Algorithm A failed
xb, yb = 0.2, 0.3
gotb = cli.beta(xb, yb)
refb = 7.748481388736760
record("ACC-01", "B(0.2,0.3) near-singular (A failed here)",
       f"{refb:.6g}", f"{gotb:.6g}", abs(gotb - refb) / refb <= 1e-6)

# ---- ACC-02: 6-significant-figure display -------------------------------- #
disp = cli.format_result(cli.beta(2, 3))
record("ACC-02", "display B(2,3)", "6 sig figs", f"'{disp}'",
       disp == "0.0833333")

# ---- FR-02: compute a known value ---------------------------------------- #
record("FR-02", "B(1,1)", "1", f"{cli.beta(1, 1):.6g}", abs(cli.beta(1, 1) - 1) < 1e-12)

# ---- VAL-01/02/03/04: input validation ----------------------------------- #
expect_input_error("VAL-01", "x = 0", "0")
expect_input_error("VAL-01", "x = -2", "-2")
expect_input_error("VAL-02", "x = 'abc'", "abc")
expect_input_error("VAL-03", "x = '' (empty)", "   ")
expect_input_error("VAL-04", "x = 1e6 (over cap)", "1e6")

# ---- REL-01: no unhandled exception across a batch of bad inputs --------- #
bad = ["abc", "", "0", "-1", "1e9", "nan", "inf", "  ", "1,5", "2.3.4"]
crashed = None
for b in bad:
    try:
        cli.parse_operand(b, "x")
    except cli.InputError:
        pass
    except Exception as e:  # any non-InputError is a crash
        crashed = f"{b!r} -> {type(e).__name__}"
        break
record("REL-01", f"{len(bad)} malformed inputs", "no unhandled exception",
       "none" if crashed is None else crashed, crashed is None)

# ---- REL-02: no inf/nan for supported inputs (incl. large) --------------- #
import math  # noqa: E402
nonfinite = []
for x in (0.001, 1, 10, 100, 1000, 1e4):
    for y in (0.001, 1, 10, 100, 1000, 1e4):
        v = cli.beta(x, y)
        if not math.isfinite(v):
            nonfinite.append((x, y, v))
record("REL-02", "36 large/small supported inputs", "all finite",
       "all finite" if not nonfinite else f"{len(nonfinite)} non-finite", not nonfinite)

# ---- REL-03: bounded work — Lanczos loop is fixed-length ----------------- #
iters = cli._LANCZOS_G + 1
record("REL-03", "Lanczos ln-Gamma loop", "fixed-length loop",
       f"{iters} iterations, no recursion growth (z>=0.5)", iters == 8)

# ---- PERF-01: < 1 s per computation -------------------------------------- #
N = 100000
t0 = time.perf_counter()
for _ in range(N):
    cli.beta(12.5, 7.25)
per_call_ms = (time.perf_counter() - t0) / N * 1000
record("PERF-01", f"{N} computations, per-call time", "< 1000 ms",
       f"{per_call_ms:.5f} ms/call", per_call_ms < 1000)

# ---- POR-01: runs from a terminal via python3 (subprocess, no IDE) ------- #
proc = subprocess.run(
    [sys.executable, os.path.join(REPO, "src", "cli.py")],
    input="2\n3\nq\n", capture_output=True, text=True, timeout=10,
)
ok_por = proc.returncode == 0 and "0.0833333" in proc.stdout
record("POR-01", "python3 src/cli.py (piped: 2,3,q)",
       "exit 0, prints result", f"exit {proc.returncode}, result {'seen' if '0.0833333' in proc.stdout else 'MISSING'}",
       ok_por)

# ---- ERR-01: messages state what + how ----------------------------------- #
try:
    cli.parse_operand("abc", "x")
    msg = ""
except cli.InputError as e:
    msg = str(e)
record("ERR-01", "message for non-numeric x", "names problem + fix",
       "'... not a number. Enter a decimal ...'" if "not a number" in msg and "Enter" in msg else msg,
       "not a number" in msg and "Enter" in msg)

# --------------------------------------------------------------------------- #
#  Report                                                                     #
# --------------------------------------------------------------------------- #
print(f"{'REQ':<8} {'RESULT':<6} DEMO CASE / OBSERVED")
print("-" * 78)
n_pass = 0
for req, case, expected, observed, ok in results:
    n_pass += ok
    print(f"{req:<8} {'PASS' if ok else 'FAIL':<6} {case}")
    print(f"{'':<15} expected: {expected}")
    print(f"{'':<15} observed: {observed}")
print("-" * 78)
print(f"{n_pass}/{len(results)} checks passed")
sys.exit(0 if n_pass == len(results) else 1)

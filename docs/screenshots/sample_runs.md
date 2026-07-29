# CLI Sample Runs — Beta Function Calculator (D1 · Problem 4)

Genuine transcripts of `src/cli.py`, captured through a pseudo-terminal (so typed
input is echoed exactly as in a real session) and rendered to PNG for the report.
Reproduce with the helpers in this folder:

```
# exact command a user runs:
python3 src/cli.py

# how these transcripts were captured (from docs/screenshots/):
python3 _capture.py "2" "3" "0.5" "0.5" "10" "10" "q"      > run_valid.txt
python3 _capture.py "0.2" "0.3" "0.001" "5" "10000" "1" "h" "q" > run_boundary.txt
python3 _capture.py "abc" "0" "-2" "3" "" "1e6" "2" "2.5" "q"   > run_invalid.txt
python3 _render.py run_valid.txt run_valid.png            # etc.
```

| Figure | Transcript | Demonstrates |
|--------|-----------|--------------|
| `run_valid.png` | `run_valid.txt` | Valid cases: B(2,3)=0.0833333, B(0.5,0.5)=3.14159 (π), B(10,10)=1.08251e-6 |
| `run_boundary.png` | `run_boundary.txt` | Boundary/near-singular: B(0.2,0.3)=7.74848 (where Algorithm A failed), tiny x=0.001, magnitude cap x=10000, `h` help |
| `run_invalid.png` | `run_invalid.txt` | Non-numeric, zero, negative, empty, over-cap — each rejected with a specific message, no traceback (REL-01, ERR-01) |

## Requirement demonstration (Gate: runs from terminal, no unhandled crash ✔)

- **FR-01/02/03** accept x, y → compute → display: all valid runs.
- **FR-04** repeat without restart; **FR-05** `q` to exit: all runs.
- **VAL-01** x≤0 rejected (`0`, `-2`); **VAL-02** non-numeric (`abc`);
  **VAL-03** empty input; **VAL-04** over-cap (`1e6`). — `run_invalid.txt`.
- **ACC-01** 18/18 reference values within 1e-6 (worst 1.2e-14); **ACC-02** 6 sig figs.
- **REL-01** no unhandled exception on any invalid input; **REL-02** no inf/nan;
  **REL-03** fixed Lanczos loop terminates.
- **USE-01** domain stated at each prompt; **USE-02/DOC-01** `h` help lists domain
  and assumptions; **ACC-03** text-only status (no colour dependence).
- **POR-01** runs from a plain terminal with `python3 src/cli.py`.

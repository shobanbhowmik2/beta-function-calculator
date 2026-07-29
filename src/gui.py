#!/usr/bin/env python3
"""Tkinter graphical user interface for the Beta Function Calculator (D2, F6).

Deliverable 2, Problem 5 (GUI). A single-window Tkinter front-end over the
from-scratch numerical core (``beta_core``) and the shared validation layer
(``validation``). It is intentionally thin: every event handler parses,
validates, calls the pure core, formats, and reports — no mathematics lives
here.

Design (traceable to the persona "Maya Fernandes" and the requirements):

* Meaningful labels state the domain at the point of input -- "x  (must be > 0)"
  (USE-01, DOC-01).
* Keyboard-first: Tab order x -> y -> Calculate -> Clear, initial focus on x,
  Enter anywhere computes, Escape clears (UI-01, accessibility).
* Status and errors are conveyed by **text**, with a word prefix ("Result:",
  "Input needed:", "Cannot compute:") and an icon glyph, never by colour alone
  (ACC-03). Colour is used only as a redundant cue.
* Each expected failure (empty / non-numeric / out-of-domain / over-range /
  numerical) is caught by its own message; no traceback ever reaches the user
  (REL-01, ERR-01).

Runs with a plain interpreter and no IDE (POR-01):

    python3 src/gui.py
"""

import tkinter as tk
from tkinter import ttk

from beta_core import MAGNITUDE_CAP, beta
from exceptions import (
    BetaError,
    DomainError,
    EmptyInputError,
    InputError,
    NonFiniteError,
    NonNumericError,
    NumericalError,
    RangeError,
)
from validation import format_result, parse_operand

APP_TITLE = "Beta Function Calculator"
VERSION = "0.2.0"

# Redundant colour cues (text/glyph already carry the meaning -> ACC-03).
COLOR_OK = "#1a7f37"
COLOR_ERR = "#b3261e"
COLOR_INFO = "#3b3b3b"

HELP_TEXT = (
    "Beta Function  B(x, y) = ∫₀¹ tˣ⁻¹ (1−t)ʸ⁻¹ dt "
    "= Γ(x)Γ(y) / Γ(x+y)\n\n"
    "• Enter a value for x and for y. Both must be real and greater than 0\n"
    f"  (supported range: 0 < x, y ≤ {MAGNITUDE_CAP:g}).\n"
    "• Press Calculate (or Enter) to compute; the result is shown to 6\n"
    "  significant figures.\n"
    "• Press Clear (or Escape) to reset the fields.\n\n"
    "The function is symmetric: B(x, y) = B(y, x). Values are computed from\n"
    "scratch via the Gamma identity (log-domain Lanczos lnΓ); no math library\n"
    "is used for the computation.\n\n"
    "Assumptions: real inputs only; domain x > 0, y > 0 (no analytic\n"
    "continuation to zero or negative arguments)."
)


class BetaCalculatorApp:
    """The application window and its event handlers."""

    def __init__(self, root):
        self.root = root
        root.title(f"{APP_TITLE}  v{VERSION}")
        root.minsize(460, 300)
        root.columnconfigure(0, weight=1)

        self._build_widgets()
        self._bind_keys()
        self.x_entry.focus_set()          # initial focus (keyboard-first)

    # ------------------------------------------------------------------ build
    def _build_widgets(self):
        pad = {"padx": 10, "pady": 6}

        header = ttk.Label(
            self.root,
            text="Beta Function  B(x, y)",
            font=("TkDefaultFont", 15, "bold"),
        )
        header.grid(row=0, column=0, sticky="w", **pad)

        subtitle = ttk.Label(
            self.root,
            text="Computes B(x, y) = Γ(x)Γ(y) / Γ(x+y) for x > 0, y > 0.",
            foreground=COLOR_INFO,
        )
        subtitle.grid(row=1, column=0, sticky="w", padx=10)

        # --- input frame ---------------------------------------------------
        form = ttk.LabelFrame(self.root, text="Inputs")
        form.grid(row=2, column=0, sticky="ew", **pad)
        form.columnconfigure(1, weight=1)

        ttk.Label(form, text="x  (must be > 0):").grid(
            row=0, column=0, sticky="w", padx=8, pady=8
        )
        self.x_var = tk.StringVar()
        self.x_entry = ttk.Entry(form, textvariable=self.x_var, width=24)
        self.x_entry.grid(row=0, column=1, sticky="ew", padx=8, pady=8)

        ttk.Label(form, text="y  (must be > 0):").grid(
            row=1, column=0, sticky="w", padx=8, pady=8
        )
        self.y_var = tk.StringVar()
        self.y_entry = ttk.Entry(form, textvariable=self.y_var, width=24)
        self.y_entry.grid(row=1, column=1, sticky="ew", padx=8, pady=8)

        hint = ttk.Label(
            form,
            text=f"Supported range: 0 < x, y ≤ {MAGNITUDE_CAP:g}.  "
            "Example: x = 2, y = 3.",
            foreground=COLOR_INFO,
            font=("TkDefaultFont", 10),
        )
        hint.grid(row=2, column=0, columnspan=2, sticky="w", padx=8)

        # --- buttons -------------------------------------------------------
        buttons = ttk.Frame(self.root)
        buttons.grid(row=3, column=0, sticky="ew", **pad)
        self.calc_btn = ttk.Button(
            buttons, text="Calculate", command=self.on_calculate
        )
        self.calc_btn.grid(row=0, column=0, padx=(0, 8))
        self.clear_btn = ttk.Button(buttons, text="Clear", command=self.on_clear)
        self.clear_btn.grid(row=0, column=1, padx=(0, 8))
        self.help_btn = ttk.Button(buttons, text="Help", command=self.on_help)
        self.help_btn.grid(row=0, column=2)

        # --- result / status ----------------------------------------------
        result_frame = ttk.LabelFrame(self.root, text="Result")
        result_frame.grid(row=4, column=0, sticky="ew", **pad)
        result_frame.columnconfigure(0, weight=1)

        # Status prefix carries meaning as text (ACC-03); colour is redundant.
        self.status_var = tk.StringVar(
            value="Enter x and y, then press Calculate."
        )
        self.status = ttk.Label(
            result_frame,
            textvariable=self.status_var,
            wraplength=420,
            justify="left",
            foreground=COLOR_INFO,
            font=("TkDefaultFont", 12),
        )
        self.status.grid(row=0, column=0, sticky="w", padx=8, pady=10)

        self.root.rowconfigure(4, weight=1)

    def _bind_keys(self):
        # Enter computes from anywhere; Escape clears (keyboard-first UX).
        self.root.bind("<Return>", lambda _event: self.on_calculate())
        self.root.bind("<KP_Enter>", lambda _event: self.on_calculate())
        self.root.bind("<Escape>", lambda _event: self.on_clear())
        self.root.bind("<F1>", lambda _event: self.on_help())

    # --------------------------------------------------------------- helpers
    def _set_status(self, prefix, message, colour):
        """Show a status line whose meaning is in the *text*, colour redundant."""
        self.status_var.set(f"{prefix} {message}")
        self.status.configure(foreground=colour)

    # ---------------------------------------------------------- event handlers
    def on_calculate(self):
        """Parse -> validate -> compute -> format -> report, handling each
        expected failure with its own helpful message (never a traceback)."""
        try:
            x = parse_operand(self.x_var.get(), "x")
            y = parse_operand(self.y_var.get(), "y")
        except EmptyInputError as err:
            self._set_status("ℹ Input needed:", err.message, COLOR_ERR)
            return
        except (NonNumericError, NonFiniteError) as err:
            self._set_status("✗ Invalid number:", err.message, COLOR_ERR)
            return
        except DomainError as err:
            self._set_status("✗ Out of domain:", err.message, COLOR_ERR)
            return
        except RangeError as err:
            self._set_status("✗ Out of range:", err.message, COLOR_ERR)
            return
        except InputError as err:                     # any other input problem
            self._set_status("✗ Invalid input:", err.message, COLOR_ERR)
            return

        try:
            value = beta(x, y)
        except DomainError as err:                    # defensive (pre-validated)
            self._set_status("✗ Out of domain:", err.message, COLOR_ERR)
            return
        except NumericalError as err:
            self._set_status("✗ Cannot compute:", err.message, COLOR_ERR)
            return
        except BetaError as err:                      # catch-all: no traceback
            self._set_status("✗ Cannot compute:", err.message, COLOR_ERR)
            return

        self._set_status(
            "✓ Result:",
            f"B({x:g}, {y:g}) = {format_result(value)}   "
            "(to 6 significant figures)",
            COLOR_OK,
        )

    def on_clear(self):
        """Reset to a predictable clean state and return focus to x."""
        self.x_var.set("")
        self.y_var.set("")
        self._set_status(
            "ℹ", "Cleared. Enter x and y, then press Calculate.", COLOR_INFO
        )
        self.x_entry.focus_set()

    def on_help(self):
        """Open a modal help window describing the function, domain, and keys."""
        top = tk.Toplevel(self.root)
        top.title("Help — Beta Function Calculator")
        top.transient(self.root)
        top.resizable(False, False)
        ttk.Label(
            top, text=HELP_TEXT, justify="left", padding=14,
            font=("TkDefaultFont", 11),
        ).grid(row=0, column=0)
        close = ttk.Button(top, text="Close", command=top.destroy)
        close.grid(row=1, column=0, pady=(0, 12))
        close.focus_set()
        top.bind("<Escape>", lambda _event: top.destroy())


def main():
    """Launch the GUI. Returns 0 on a clean close."""
    root = tk.Tk()
    BetaCalculatorApp(root)
    root.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

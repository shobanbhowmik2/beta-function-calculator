# Tkinter GUI Wireframe & Design Rationale (D2, Problem 5.4)

Wireframe produced **before** coding `src/gui.py` (decision **D-010**). It fixes
the layout, the widget set, and the interaction model, all traced to the persona
"Maya Fernandes" and the requirements.

## Wireframe

```
┌───────────────────────────────────────────────────────────┐
│ ● ● ●        Beta Function Calculator  v0.2.0               │  title bar
├───────────────────────────────────────────────────────────┤
│  Beta Function  B(x, y)                                     │  header (bold)
│  Computes B(x, y) = Γ(x)Γ(y) / Γ(x+y) for x > 0, y > 0.     │  subtitle
│                                                             │
│  ┌─ Inputs ────────────────────────────────────────────┐   │
│  │  x  (must be > 0):   [ 2________________________ ]   │   │  labelled entry
│  │  y  (must be > 0):   [ 3________________________ ]   │   │  labelled entry
│  │  Supported range: 0 < x, y ≤ 10000.  Example: 2, 3. │   │  inline hint
│  └─────────────────────────────────────────────────────┘   │
│                                                             │
│  [ Calculate ]  [ Clear ]  [ Help ]                         │  actions
│                                                             │
│  ┌─ Result ────────────────────────────────────────────┐   │
│  │  ✓ Result: B(2, 3) = 0.0833333 (to 6 sig. figures)  │   │  status line
│  └─────────────────────────────────────────────────────┘   │
└───────────────────────────────────────────────────────────┘
```

## Widget → requirement / persona trace

| Widget | Purpose | Trace |
|---|---|---|
| `x`, `y` labelled entries | accept two reals | FR-01; persona G1 |
| Label text "must be > 0" + inline range hint | state the valid domain at the point of input | USE-01, DOC-01; persona N1, N4 |
| **Calculate** (primary) | compute and show B(x,y) | FR-02, FR-03; G1, G2 |
| **Clear** | reset to a clean state, no restart | FR-04; N4 |
| **Help** (modal) | concise usage + definition + assumptions | USE-02, DOC-01; N4 |
| Result/status line | show result *or* a specific error, as text | FR-03, ERR-01, ACC-03; N2, N3, N5 |

## Interaction model

* **Initial focus** on the `x` field; **Tab order** x → y → Calculate → Clear → Help.
* **Enter** (main or keypad) computes from anywhere; **Escape** clears; **F1** opens Help.
* A first-time user can infer the required action from the labels alone.
* Window is **resizable**; the entry row and result area stretch (`columnconfigure`,
  `sticky="ew"`); nothing clips at normal scaling.

## Accessibility (ACC-03, anticipating D3)

* Status meaning is carried by a **leading word** ("Result:", "Out of domain:",
  "Input needed:", "Invalid number:", "Out of range:", "Cannot compute:") **and**
  a glyph — colour (green/red/grey) is only a redundant cue, never the sole signal.
* Plain-language labels and messages; no colour-only state; readable default fonts;
  keyboard operable end-to-end.

## Error-state examples (rendered)

* Valid: [`screenshots/gui_valid.png`](screenshots/gui_valid.png)
* Out of domain (x = 0): [`screenshots/gui_domain.png`](screenshots/gui_domain.png)
* Non-numeric (x = "abc"): [`screenshots/gui_nonnumeric.png`](screenshots/gui_nonnumeric.png)

> These figures are layout renders that reproduce the exact widgets and status
> strings emitted by `src/gui.py` (verified in `tests/verify_d2.py`, checks
> GUI-01…GUI-06); the live window is shown in the Zoom demonstration.

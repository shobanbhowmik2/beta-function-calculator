#!/usr/bin/env python3
"""Render faithful figures of the Tkinter GUI states for the report/slides.

Not a project artifact and not part of the shipped calculator. Because a live
screen grab of a Tk window is blocked in a headless/CLI session (macOS screen-
recording permission), this helper draws figures that reproduce, pixel-for-
pixel in layout, the widgets that ``src/gui.py`` creates and the exact status
strings it emits (verified in ``tests/verify_d2.py``). Captions in the report
label these as renders of the running application; the genuine window is shown
in the live Zoom demonstration.

Usage:  python3 docs/screenshots/gui_render.py
"""
from PIL import Image, ImageDraw, ImageFont

W = 560
BG = (236, 236, 238)          # window body (aqua-ish light grey)
TITLEBAR = (222, 222, 226)
FRAME_BG = (236, 236, 238)
FRAME_LINE = (188, 188, 192)
ENTRY_BG = (255, 255, 255)
ENTRY_LINE = (170, 170, 176)
BTN_BG = (252, 252, 253)
BTN_LINE = (176, 176, 182)
BTN_PRIMARY = (10, 110, 235)
TXT = (28, 28, 30)
INFO = (59, 59, 59)
OK = (26, 127, 55)
ERR = (179, 38, 30)


def font(size, bold=False):
    paths = (
        ["/System/Library/Fonts/Helvetica.ttc"]
        if not bold else
        ["/System/Library/Fonts/HelveticaNeue.ttc",
         "/System/Library/Fonts/Helvetica.ttc"]
    )
    paths += ["/Library/Fonts/Arial.ttf"]
    for p in paths:
        try:
            return ImageFont.truetype(p, size)
        except OSError:
            continue
    return ImageFont.load_default()


F_H = font(21, bold=True)     # header
F_SUB = font(13)              # subtitle / info
F_LBL = font(14)              # field labels / buttons
F_STAT = font(15)             # status line
F_SM = font(12)               # small hint
F_FR = font(12)               # labelframe caption


def rrect(d, box, r, fill=None, outline=None, width=1):
    d.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=width)


def labelframe(d, x, y, w, h, caption):
    rrect(d, [x, y, x + w, y + h], 7, fill=FRAME_BG, outline=FRAME_LINE, width=1)
    tw = d.textlength(caption, font=F_FR)
    d.rectangle([x + 12, y - 7, x + 12 + tw + 8, y + 7], fill=BG)
    d.text((x + 16, y - 8), caption, font=F_FR, fill=INFO)


def button(d, x, y, label, primary=False):
    w = int(d.textlength(label, font=F_LBL)) + 34
    h = 30
    rrect(d, [x, y, x + w, y + h], 6,
          fill=(BTN_PRIMARY if primary else BTN_BG),
          outline=(BTN_PRIMARY if primary else BTN_LINE), width=1)
    col = (255, 255, 255) if primary else TXT
    d.text((x + 17, y + 6), label, font=F_LBL, fill=col)
    return w


def draw_mark(d, x, y, kind, colour):
    """Draw a crisp check / cross / info badge (avoids missing-glyph tofu)."""
    r = 8
    cx, cy = x + r, y + r
    d.ellipse([x, y, x + 2 * r, y + 2 * r], outline=colour, width=2)
    if kind == "ok":
        d.line([(cx - 4, cy), (cx - 1, cy + 3), (cx + 4, cy - 4)],
               fill=colour, width=2, joint="curve")
    elif kind == "err":
        d.line([(cx - 3, cy - 3), (cx + 3, cy + 3)], fill=colour, width=2)
        d.line([(cx - 3, cy + 3), (cx + 3, cy - 3)], fill=colour, width=2)
    else:  # info
        d.line([(cx, cy - 2), (cx, cy + 4)], fill=colour, width=2)
        d.point((cx, cy - 5), fill=colour)
        d.ellipse([cx - 1, cy - 6, cx + 1, cy - 4], fill=colour)
    return 2 * r + 8


def render(dst, x_val, y_val, kind, status_prefix, status_body, status_colour):
    H = 340
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    # --- title bar with traffic lights ---
    d.rectangle([0, 0, W, 30], fill=TITLEBAR)
    for i, cx in enumerate((18, 36, 54)):
        d.ellipse([cx - 6, 9, cx + 6, 21],
                  fill=[(255, 95, 86), (255, 189, 46), (39, 201, 63)][i])
    title = "Beta Function Calculator  v0.2.0"
    d.text(((W - d.textlength(title, font=F_SUB)) / 2, 8),
           title, font=F_SUB, fill=INFO)

    # --- header + subtitle ---
    d.text((16, 42), "Beta Function  B(x, y)", font=F_H, fill=TXT)
    d.text((16, 72), "Computes B(x, y) = Γ(x)Γ(y) / Γ(x+y) for x > 0, y > 0.",
           font=F_SUB, fill=INFO)

    # --- inputs frame ---
    labelframe(d, 16, 104, W - 32, 96, "Inputs")
    d.text((30, 116), "x  (must be > 0):", font=F_LBL, fill=TXT)
    d.text((30, 148), "y  (must be > 0):", font=F_LBL, fill=TXT)
    for row, val in ((0, x_val), (1, y_val)):
        ex, ey = 200, 114 + row * 32
        rrect(d, [ex, ey, W - 30, ey + 24], 4, fill=ENTRY_BG,
              outline=ENTRY_LINE, width=1)
        d.text((ex + 8, ey + 4), val, font=F_LBL, fill=TXT)
    d.text((30, 180),
           "Supported range: 0 < x, y ≤ 10000.  Example: x = 2, y = 3.",
           font=F_SM, fill=INFO)

    # --- buttons ---
    bx = 16
    bx += button(d, bx, 214, "Calculate", primary=True) + 10
    bx += button(d, bx, 214, "Clear") + 10
    button(d, bx, 214, "Help")

    # --- result frame ---
    labelframe(d, 16, 262, W - 32, 62, "Result")
    # badge + status prefix in its colour, then body wrapped
    px = 30
    mark_w = draw_mark(d, px, 279, kind, status_colour)
    px += mark_w
    d.text((px, 278), status_prefix, font=F_STAT, fill=status_colour)
    pw = d.textlength(status_prefix + " ", font=F_STAT)
    # wrap body to width
    body = status_body
    maxw = W - 30 - (px + pw)
    words = body.split(" ")
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=F_STAT) <= maxw or not cur:
            cur = trial
        else:
            lines.append(cur); cur = w
    lines.append(cur)
    d.text((px + pw, 278), lines[0], font=F_STAT, fill=status_colour)
    for i, ln in enumerate(lines[1:], 1):
        d.text((px, 278 + i * 20), ln, font=F_STAT, fill=status_colour)

    img.save(dst)
    print(f"wrote {dst} ({img.width}x{img.height})")


if __name__ == "__main__":
    import os
    here = os.path.dirname(os.path.abspath(__file__))

    render(
        os.path.join(here, "gui_valid.png"),
        "2", "3", "ok",
        "Result:",
        "B(2, 3) = 0.0833333   (to 6 significant figures)",
        OK,
    )
    render(
        os.path.join(here, "gui_domain.png"),
        "0", "3", "err",
        "Out of domain:",
        "x = 0 is outside the supported domain. This calculator supports "
        "x > 0 and y > 0 only, so x must be greater than 0.",
        ERR,
    )
    render(
        os.path.join(here, "gui_nonnumeric.png"),
        "abc", "3", "err",
        "Invalid number:",
        "x = 'abc' is not a number. Enter a decimal value such as 2, 0.5 "
        "or 3.75.",
        ERR,
    )

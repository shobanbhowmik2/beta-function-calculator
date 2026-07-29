#!/usr/bin/env python3
"""Render a captured .txt transcript to a terminal-style .png (report figure).

Not a project artifact -- a helper that turns the genuine transcripts produced
by _capture.py into images for the LaTeX report/slides. Prompt lines and error
lines are tinted for readability; the text itself is the verbatim transcript.
"""
import sys
from PIL import Image, ImageDraw, ImageFont

BG = (30, 30, 38)
FG = (220, 220, 220)
PROMPT = (120, 200, 255)   # x/y prompt lines
GOOD = (150, 220, 150)     # result lines
BAD = (245, 150, 150)      # error lines
DIM = (140, 140, 150)      # banner/help
TITLE_BAR = (52, 52, 62)

PADDING = 22
LINE_H = 22
FONT_SIZE = 15


def load_font():
    for path in (
        "/System/Library/Fonts/Menlo.ttc",
        "/System/Library/Fonts/Monaco.ttf",
        "/Library/Fonts/Courier New.ttf",
    ):
        try:
            return ImageFont.truetype(path, FONT_SIZE)
        except OSError:
            continue
    return ImageFont.load_default()


def colour_for(line):
    s = line.strip()
    if s.startswith("!") or "! " in line[:6]:
        return BAD
    if s.startswith("B(") or ") =" in line and "significant" in line:
        return GOOD
    if s.startswith("x (> 0)") or s.startswith("y (> 0)"):
        return PROMPT
    if s.startswith("$"):
        return (255, 255, 255)
    if any(s.startswith(p) for p in ("Beta Function", "Computes", "Type '", "How to", "*", "Assumptions", "Method", "(", "Goodbye")):
        return DIM
    return FG


def render(src, dst):
    with open(src) as f:
        lines = f.read().split("\n")
    font = load_font()
    char_w = font.getbbox("M")[2] or 9
    width = PADDING * 2 + char_w * (max((len(l) for l in lines), default=40) + 2)
    top_bar = 30
    height = top_bar + PADDING * 2 + LINE_H * len(lines)

    img = Image.new("RGB", (int(width), int(height)), BG)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, width, top_bar], fill=TITLE_BAR)
    for i, cx in enumerate((16, 32, 48)):
        d.ellipse([cx - 6, 9, cx + 6, 21], fill=[(255, 95, 86), (255, 189, 46), (39, 201, 63)][i])
    d.text((70, 7), "Terminal — beta-function-calculator", font=font, fill=DIM)

    y = top_bar + PADDING
    for line in lines:
        d.text((PADDING, y), line, font=font, fill=colour_for(line))
        y += LINE_H
    img.save(dst)
    print(f"wrote {dst}  ({img.width}x{img.height})")


if __name__ == "__main__":
    render(sys.argv[1], sys.argv[2])

#!/usr/bin/env python3
"""Generate SVG label sheets for Cricut Print Then Cut."""

import argparse
import math
import sys
from pathlib import Path

MM_TO_PX = 96 / 25.4

# Cricut Print Then Cut usable area
PTC_WIDTH_MM  = 235.0
PTC_HEIGHT_MM = 171.0

PAPER_SIZES = {
    "letter": (215.9, 279.4),
    "legal":  (215.9, 355.6),
    "a3":     (297.0, 420.0),
    "a4":     (210.0, 297.0),
    "a5":     (148.0, 210.0),
}


def mm(value):
    return value * MM_TO_PX


def generate_sheet(labels, label_w_mm, label_h_mm, gap_mm,
                   border_color, border_width_mm,
                   font_size_mm, font_family,
                   cols, rows, sheet_index, total_sheets,
                   page_margin_mm):
    """Return SVG string for one sheet of labels."""

    lw = mm(label_w_mm)
    lh = mm(label_h_mm)
    gap = mm(gap_mm)
    bw = mm(border_width_mm)
    margin = mm(page_margin_mm)

    grid_w = cols * lw + (cols - 1) * gap
    grid_h = rows * lh + (rows - 1) * gap
    sheet_w = grid_w + 2 * margin
    sheet_h = grid_h + 2 * margin

    font_size = mm(font_size_mm)

    items = []
    for i, text in enumerate(labels):
        row = i // cols
        col = i % cols
        x = margin + col * (lw + gap)
        y = margin + row * (lh + gap)
        cx = x + lw / 2
        cy = y + lh / 2

        # Escape XML special characters
        safe = text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

        items.append(
            f'  <rect x="{x:.4f}" y="{y:.4f}" width="{lw:.4f}" height="{lh:.4f}"'
            f' fill="white" stroke="{border_color}" stroke-width="{bw:.4f}"/>\n'
            f'  <text x="{cx:.4f}" y="{cy:.4f}"'
            f' font-family="{font_family}" font-size="{font_size:.4f}"'
            f' text-anchor="middle" dominant-baseline="middle"'
            f' fill="black">{safe}</text>'
        )

    sheet_label = f"Sheet {sheet_index + 1} of {total_sheets}" if total_sheets > 1 else ""
    comment = (f"  <!-- {label_w_mm}x{label_h_mm}mm labels | {len(labels)} labels"
               f" | {page_margin_mm}mm page margin{' | ' + sheet_label if sheet_label else ''} -->")

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg"
     width="{sheet_w:.4f}" height="{sheet_h:.4f}"
     viewBox="0 0 {sheet_w:.4f} {sheet_h:.4f}">
{comment}
{chr(10).join(items)}
</svg>
"""


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate SVG label sheets for Cricut Print Then Cut.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Input file: one label per line.",
    )

    parser.add_argument("input", metavar="LABELS_FILE",
                        help="Text file with one label per line")

    parser.add_argument("--label-width",  "-W", type=float, required=True, metavar="MM",
                        help="Label width in mm")
    parser.add_argument("--label-height", "-H", type=float, required=True, metavar="MM",
                        help="Label height in mm")

    parser.add_argument("--gap", type=float, default=1.5, metavar="MM",
                        help="Gap between labels in mm (default: 1.5)")
    parser.add_argument("--border-color", default="#888888", metavar="COLOR",
                        help="Border color (default: #888888)")
    parser.add_argument("--border-width", type=float, default=0.2, metavar="MM",
                        help="Border width in mm (default: 0.2)")
    parser.add_argument("--font-size", type=float, metavar="MM",
                        help="Font size in mm (default: 60%% of label height)")
    parser.add_argument("--font-family", default="Helvetica, Arial, sans-serif",
                        metavar="FONT", help="Font family (default: Helvetica, Arial, sans-serif)")

    parser.add_argument("--page-margin", type=float, default=5.0, metavar="MM",
                        help="Minimum margin from sheet edge in mm (default: 5.0)")
    parser.add_argument("--output", "-o", metavar="PREFIX",
                        help="Output filename prefix (default: based on input filename)")

    return parser.parse_args()


def main():
    args = parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"error: file not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    lines = input_path.read_text(encoding="utf-8").splitlines()
    labels = [l.strip() for l in lines if l.strip()]

    if not labels:
        print("error: no labels found in input file", file=sys.stderr)
        sys.exit(1)

    label_w = args.label_width
    label_h = args.label_height
    gap = args.gap

    page_margin = args.page_margin
    avail_w = PTC_WIDTH_MM - 2 * page_margin
    avail_h = PTC_HEIGHT_MM - 2 * page_margin
    cols = max(1, int((avail_w + gap) / (label_w + gap)))
    rows = max(1, int((avail_h + gap) / (label_h + gap)))
    per_sheet = cols * rows

    font_size = args.font_size if args.font_size else label_h * 0.6

    prefix = args.output or input_path.stem

    total_sheets = math.ceil(len(labels) / per_sheet)

    for s in range(total_sheets):
        chunk = labels[s * per_sheet : (s + 1) * per_sheet]
        svg = generate_sheet(
            chunk, label_w, label_h, gap,
            args.border_color, args.border_width,
            font_size, args.font_family,
            cols, rows, s, total_sheets,
            page_margin,
        )
        if total_sheets == 1:
            out = f"{prefix}.svg"
        else:
            out = f"{prefix}_sheet{s + 1:02d}.svg"

        Path(out).write_text(svg, encoding="utf-8")
        print(f"Wrote {out}  ({len(chunk)} labels, {cols}×{rows} grid)")

    print(f"\n{len(labels)} labels across {total_sheets} sheet(s)  |  {per_sheet} labels/sheet ({cols} cols × {rows} rows)")


if __name__ == "__main__":
    main()

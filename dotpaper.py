#!/usr/bin/env python3
"""Generate SVG dot paper for printing."""

import argparse
import sys

MM_TO_PX = 96 / 25.4  # CSS/SVG standard: 96 DPI

PAPER_SIZES = {
    "letter": (215.9, 279.4),
    "legal":  (215.9, 355.6),
    "a3":     (297.0, 420.0),
    "a4":     (210.0, 297.0),
    "a5":     (148.0, 210.0),
}


def mm(value):
    return value * MM_TO_PX


def generate_svg(width_mm, height_mm, spacing_x_mm, spacing_y_mm,
                 dot_radius_mm, margin_mm, dot_color):
    w = mm(width_mm)
    h = mm(height_mm)
    r = mm(dot_radius_mm)
    margin = mm(margin_mm)

    x_start = margin
    y_start = margin
    x_end = w - margin
    y_end = h - margin

    spacing_x = mm(spacing_x_mm)
    spacing_y = mm(spacing_y_mm)

    dots = []
    y = y_start
    while y <= y_end + 1e-9:
        x = x_start
        while x <= x_end + 1e-9:
            dots.append(f'  <circle cx="{x:.4f}" cy="{y:.4f}" r="{r:.4f}"/>')
            x += spacing_x
        y += spacing_y

    dot_count = len(dots)
    dots_svg = "\n".join(dots)

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg"
     width="{w:.4f}" height="{h:.4f}"
     viewBox="0 0 {w:.4f} {h:.4f}">
  <!-- {width_mm}x{height_mm}mm | spacing {spacing_x_mm}x{spacing_y_mm}mm | {dot_count} dots -->
  <g fill="{dot_color}" stroke="none">
{dots_svg}
  </g>
</svg>
"""


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate SVG dot paper for printing.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"Paper presets: {', '.join(PAPER_SIZES)}",
    )

    size_group = parser.add_mutually_exclusive_group()
    size_group.add_argument(
        "--paper", choices=PAPER_SIZES,
        help="Paper size preset (default: letter)",
    )
    size_group.add_argument(
        "--size", nargs=2, metavar=("W", "H"), type=float,
        help="Custom paper size in mm (e.g. --size 100 150)",
    )

    parser.add_argument(
        "--spacing", type=float, metavar="MM",
        help="Dot spacing in mm for both axes (overridden by --spacing-x/y)",
    )
    parser.add_argument("--spacing-x", type=float, metavar="MM", help="Horizontal dot spacing in mm")
    parser.add_argument("--spacing-y", type=float, metavar="MM", help="Vertical dot spacing in mm")
    parser.add_argument("--dot-size", type=float, default=0.3, metavar="MM", help="Dot radius in mm (default: 0.3)")
    parser.add_argument("--margin", type=float, default=10.0, metavar="MM", help="Page margin in mm (default: 10)")
    parser.add_argument("--color", default="#b0b0b0", metavar="COLOR", help="Dot color (default: #b0b0b0)")
    parser.add_argument("--output", "-o", metavar="FILE", help="Output file (default: stdout)")

    return parser.parse_args()


def main():
    args = parse_args()

    if args.size:
        width_mm, height_mm = args.size
    elif args.paper:
        width_mm, height_mm = PAPER_SIZES[args.paper]
    else:
        width_mm, height_mm = PAPER_SIZES["letter"]

    default_spacing = 5.0
    base = args.spacing if args.spacing is not None else default_spacing
    spacing_x = args.spacing_x if args.spacing_x is not None else base
    spacing_y = args.spacing_y if args.spacing_y is not None else base

    if spacing_x <= 0 or spacing_y <= 0:
        print("error: spacing must be positive", file=sys.stderr)
        sys.exit(1)
    if args.dot_size <= 0:
        print("error: dot size must be positive", file=sys.stderr)
        sys.exit(1)

    svg = generate_svg(
        width_mm, height_mm,
        spacing_x, spacing_y,
        args.dot_size,
        args.margin,
        args.color,
    )

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(svg)
        print(f"Wrote {args.output}")
    else:
        sys.stdout.write(svg)


if __name__ == "__main__":
    main()

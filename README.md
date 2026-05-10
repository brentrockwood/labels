# labels

Python scripts for generating printable SVG files for paper crafts and labeling.

## Scripts

### `dotpaper.py` — Dot grid paper

Generates a dot grid SVG sized for any paper format.

```
python3 dotpaper.py [options] -o output.svg
```

| Option | Default | Description |
|---|---|---|
| `--paper {letter,legal,a3,a4,a5}` | `letter` | Paper size preset |
| `--size W H` | — | Custom paper size in mm (mutually exclusive with `--paper`) |
| `--spacing MM` | `5.0` | Dot spacing for both axes |
| `--spacing-x MM` | — | Horizontal dot spacing (overrides `--spacing`) |
| `--spacing-y MM` | — | Vertical dot spacing (overrides `--spacing`) |
| `--dot-size MM` | `0.3` | Dot radius |
| `--margin MM` | `10` | Page margin |
| `--color COLOR` | `#b0b0b0` | Dot color |
| `--output / -o FILE` | stdout | Output file |

**Examples:**

```bash
# Letter-size sheet, 5mm grid
python3 dotpaper.py --paper letter -o dots.svg

# A4 with a tighter grid
python3 dotpaper.py --paper a4 --spacing 3.5 -o dots_a4.svg

# Custom size, different X and Y spacing
python3 dotpaper.py --size 100 150 --spacing-x 5 --spacing-y 8 -o dots_custom.svg
```

---

### `labels.py` — Label sheets for Cricut Print Then Cut

Generates SVG label sheets from a plain text file. Designed for the
[Cricut Print Then Cut](https://help.cricut.com/hc/en-us/articles/360012279773)
workflow: import the SVG into Cricut Design Space, print, then cut.

Labels are auto-arranged in a grid sized to fit within the Cricut Print Then Cut
area (~235 × 171 mm). If the label list exceeds one sheet, multiple numbered SVGs
are generated automatically.

**Input file format:** plain text, one label per line.

```
python3 labels.py LABELS_FILE --label-width MM --label-height MM [options]
```

| Option | Default | Description |
|---|---|---|
| `--label-width / -W MM` | *(required)* | Label width in mm |
| `--label-height / -H MM` | *(required)* | Label height in mm |
| `--gap MM` | `1.5` | Gap between labels |
| `--border-color COLOR` | `#888888` | Border color |
| `--border-width MM` | `0.2` | Border stroke width |
| `--font-size MM` | 60% of height | Font size |
| `--font-family FONT` | `Helvetica, Arial, sans-serif` | Font family |
| `--output / -o PREFIX` | input filename stem | Output file prefix |

**Examples:**

```bash
# 5×15mm labels from a text file
python3 labels.py items.txt --label-width 15 --label-height 5

# Larger labels with a custom output prefix
python3 labels.py items.txt -W 30 -H 10 -o labels/run1

# Darker border, larger font
python3 labels.py items.txt -W 25 -H 8 --border-color "#333" --font-size 5
```

**Print Then Cut workflow:**

1. Generate the SVG with `labels.py`
2. Open [Cricut Design Space](https://design.cricut.com) and import the SVG
3. Set the operation to **Print Then Cut**
4. Send to printer — Design Space adds registration marks automatically
5. Feed the printed sheet into the Cricut to cut

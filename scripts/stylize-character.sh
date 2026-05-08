#!/bin/bash

set -euo pipefail

# Cut out the subject from a photo and add a white outline.
# Output is a PNG with alpha channel — ready to drop into a template scene.
#
# Usage:
#   stylize-character.sh INPUT OUTPUT [--outline-width N] [--outline-color HEX]
#
# Examples:
#   stylize-character.sh ./mia.jpg ./mia-stylized.png
#   stylize-character.sh ./mia.jpg ./mia-stylized.png --outline-width 8 --outline-color "#ffffff"
#
# Cutout strategy (in order):
#   1. remove.bg API   (if REMOVE_BG_API_KEY is set, best quality)
#   2. rembg locally   (Python package, offline, free; install: pip install rembg)
#
# Outline strategy:
#   PIL alpha-channel dilation → fill with outline color → composite under original.
#
# Requires: python3, PIL/Pillow. For local cutout fallback: rembg.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REMOVE_BG_SCRIPT="$SCRIPT_DIR/remove-bg.sh"

INPUT=""
OUTPUT=""
OUTLINE_WIDTH="${DEAR_OUTLINE_WIDTH:-6}"
OUTLINE_COLOR="${DEAR_OUTLINE_COLOR:-#ffffff}"

while [ $# -gt 0 ]; do
  case "$1" in
    --outline-width)
      OUTLINE_WIDTH="${2:-}"
      shift 2
      ;;
    --outline-color)
      OUTLINE_COLOR="${2:-}"
      shift 2
      ;;
    -h|--help)
      sed -n '6,18p' "$0"
      exit 0
      ;;
    *)
      if [ -z "$INPUT" ]; then
        INPUT="$1"
      elif [ -z "$OUTPUT" ]; then
        OUTPUT="$1"
      else
        echo "Unexpected argument: $1" >&2
        exit 1
      fi
      shift
      ;;
  esac
done

if [ -z "$INPUT" ] || [ -z "$OUTPUT" ]; then
  echo "Usage: stylize-character.sh INPUT OUTPUT [--outline-width N] [--outline-color HEX]" >&2
  exit 1
fi

if [ ! -f "$INPUT" ]; then
  echo "Input file not found: $INPUT" >&2
  exit 1
fi

OUT_DIR="$(dirname "$OUTPUT")"
mkdir -p "$OUT_DIR"

# Step 1: cutout into a temp PNG with alpha.
TMPDIR_X="$(mktemp -d)"
trap 'rm -rf "$TMPDIR_X"' EXIT
CUTOUT_PATH="$TMPDIR_X/cutout.png"

cutout_done=0

# Try remove.bg API first if key is present.
if [ -n "${REMOVE_BG_API_KEY:-}" ] && [ -x "$REMOVE_BG_SCRIPT" ]; then
  if "$REMOVE_BG_SCRIPT" "$INPUT" "$CUTOUT_PATH" >/dev/null 2>&1; then
    cutout_done=1
  else
    echo "remove.bg failed; falling back to rembg" >&2
  fi
fi

# Fallback: local rembg.
if [ "$cutout_done" -eq 0 ]; then
  if python3 -c "import rembg" >/dev/null 2>&1; then
    python3 - "$INPUT" "$CUTOUT_PATH" <<'PY'
import sys
from rembg import remove
from PIL import Image

inp, out = sys.argv[1], sys.argv[2]
with Image.open(inp) as im:
    im = im.convert("RGBA")
    result = remove(im)
    result.save(out, "PNG")
PY
    cutout_done=1
  fi
fi

if [ "$cutout_done" -eq 0 ]; then
  echo "No cutout backend available." >&2
  echo "Either set REMOVE_BG_API_KEY, or: pip install rembg pillow" >&2
  exit 1
fi

# Step 2: add white (or specified) outline by alpha-dilation.
python3 - "$CUTOUT_PATH" "$OUTPUT" "$OUTLINE_WIDTH" "$OUTLINE_COLOR" <<'PY'
import sys
from PIL import Image, ImageFilter

cutout_path, output_path, outline_width_s, outline_color = sys.argv[1:5]
outline_width = int(outline_width_s)

def parse_hex(c):
    c = c.lstrip("#")
    if len(c) == 3:
        c = "".join(ch * 2 for ch in c)
    if len(c) != 6:
        raise SystemExit(f"Invalid outline color: {c}")
    return tuple(int(c[i:i+2], 16) for i in (0, 2, 4))

r, g, b = parse_hex(outline_color)

img = Image.open(cutout_path).convert("RGBA")
alpha = img.split()[-1]

if outline_width <= 0:
    img.save(output_path, "PNG")
    raise SystemExit(0)

# Dilate alpha by `outline_width` pixels.
# MaxFilter with size 2*radius+1; do iterations of small filters since
# Pillow's MaxFilter sizes max out at 9 for stability.
dilated = alpha
remaining = outline_width
while remaining > 0:
    step = min(remaining, 4)
    dilated = dilated.filter(ImageFilter.MaxFilter(2 * step + 1))
    remaining -= step

# Build a colored layer that's only visible where dilated alpha is non-zero.
outline_layer = Image.new("RGBA", img.size, (r, g, b, 0))
outline_layer.putalpha(dilated)

# Composite original on top of outline.
result = Image.alpha_composite(outline_layer, img)
result.save(output_path, "PNG")
PY

echo "$OUTPUT"

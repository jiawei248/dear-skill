#!/bin/bash

set -euo pipefail

# Usage: remove-bg.sh <input-image> <output-image> [api-key]

INPUT_IMAGE="${1:-}"
OUTPUT_IMAGE="${2:-}"
API_KEY="${3:-${REMOVE_BG_API_KEY:-}}"
CURL_BIN="${REMOVE_BG_CURL_BIN:-curl}"

if [ -z "$INPUT_IMAGE" ] || [ -z "$OUTPUT_IMAGE" ]; then
  echo "Usage: remove-bg.sh <input-image> <output-image> [api-key]" >&2
  exit 1
fi

if [ -z "$API_KEY" ]; then
  echo "No remove.bg API key. Set REMOVE_BG_API_KEY or pass as arg 3." >&2
  exit 1
fi

if [ ! -f "$INPUT_IMAGE" ]; then
  echo "Input file not found: $INPUT_IMAGE" >&2
  exit 1
fi

HTTP_CODE="$(
  "$CURL_BIN" -sS -o "$OUTPUT_IMAGE" -w "%{http_code}" \
    -X POST "https://api.remove.bg/v1.0/removebg" \
    -H "X-Api-Key: $API_KEY" \
    -F "image_file=@$INPUT_IMAGE" \
    -F "size=auto"
)"

if [ "$HTTP_CODE" != "200" ]; then
  echo "remove.bg API returned HTTP $HTTP_CODE" >&2
  if [ -f "$OUTPUT_IMAGE" ]; then
    python3 - "$OUTPUT_IMAGE" <<'PY' >&2
from pathlib import Path
import sys

path = Path(sys.argv[1])
try:
    text = path.read_text(encoding="utf-8").strip()
except Exception:
    raise SystemExit(0)

if text:
    print(text[:4000])
PY
    rm -f "$OUTPUT_IMAGE"
  fi
  exit 1
fi

echo "$OUTPUT_IMAGE"

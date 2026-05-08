#!/bin/bash
set -euo pipefail

# Usage: fetch-music.sh <query> <output-path> [max-duration-seconds] [setup-state-file]
# Example: fetch-music.sh "warm piano loop" ./music.mp3 30 ./setup-state.json
# Returns the output path on success, empty on failure.

QUERY="${1:-}"
OUTPUT="${2:-}"
MAX_DUR="${3:-30}"
SETUP_STATE="${4:-}"

if [ -z "$QUERY" ] || [ -z "$OUTPUT" ]; then
  echo "Usage: fetch-music.sh <query> <output-path> [max-duration] [setup-state]" >&2
  exit 1
fi

# Try to get API token from setup-state or environment
API_TOKEN=""
if [ -n "$SETUP_STATE" ] && [ -f "$SETUP_STATE" ]; then
  API_TOKEN="$(python3 -c "
import json, sys
from pathlib import Path
try:
    d = json.loads(Path(sys.argv[1]).read_text())
    t = d.get('tools', {}).get('freesound', {})
    print(t.get('api_key', '') or t.get('token', ''))
except: print('')
" "$SETUP_STATE")"
fi

if [ -z "$API_TOKEN" ] && [ -n "${FREESOUND_API_KEY:-}" ]; then
  API_TOKEN="$FREESOUND_API_KEY"
fi

if [ -z "$API_TOKEN" ]; then
  echo "" # empty = no token, caller should fallback
  exit 0
fi

# Search Freesound with progressive query simplification
# If the full query returns no results, try with fewer words
search_freesound() {
  local q="$1"
  local url="https://freesound.org/apiv2/search/text/?query=$(echo "$q" | tr ' ' '+')&fields=id,name,duration,previews&page_size=10&token=${API_TOKEN}"
  curl -s "$url" | python3 -c "
import json, sys
max_dur = float(sys.argv[1])
d = json.load(sys.stdin)
for r in d.get('results', []):
    if 5 <= r['duration'] <= max_dur:
        url = r.get('previews', {}).get('preview-hq-mp3', '')
        if url:
            print(url)
            break
" "$MAX_DUR" 2>/dev/null || true
}

PREVIEW_URL="$(search_freesound "$QUERY")"

# If no results, progressively drop words from the end and retry
if [ -z "$PREVIEW_URL" ]; then
  WORDS=($QUERY)
  WORD_COUNT=${#WORDS[@]}
  while [ -z "$PREVIEW_URL" ] && [ "$WORD_COUNT" -gt 1 ]; do
    WORD_COUNT=$((WORD_COUNT - 1))
    SHORTER_QUERY="${WORDS[@]:0:$WORD_COUNT}"
    PREVIEW_URL="$(search_freesound "$SHORTER_QUERY")"
  done
fi

if [ -z "$PREVIEW_URL" ]; then
  echo "" # empty = nothing found even after simplification
  exit 0
fi

# Filename sanity check — reject alert/notification sounds
FILENAME="$(basename "$PREVIEW_URL")"
if echo "$FILENAME" | grep -qiE 'alert|bell|notif|alarm|siren|horn|beep|click|ring|train|whistle'; then
  # Suspicious filename, likely not background music. Try next result or fallback.
  echo ""
  exit 0
fi

# Download preview
curl -s "$PREVIEW_URL" -o "$OUTPUT" 2>/dev/null

if [ -f "$OUTPUT" ] && [ -s "$OUTPUT" ]; then
  echo "$OUTPUT"
else
  echo ""
fi

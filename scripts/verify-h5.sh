#!/bin/bash
set -euo pipefail

usage() {
  echo "Usage: verify-h5.sh <index.html>" >&2
  echo "Verifies a local H5 gift with lightweight static checks and prints Claude Code / Playwright browser steps." >&2
}

INDEX_HTML="${1:-}"
if [ -z "$INDEX_HTML" ] || [ "$INDEX_HTML" = "--help" ] || [ "$INDEX_HTML" = "-h" ]; then
  usage
  exit 1
fi

if [ ! -f "$INDEX_HTML" ]; then
  echo "H5 file not found: $INDEX_HTML" >&2
  exit 1
fi

case "$INDEX_HTML" in
  *.html) ;;
  *) echo "Expected an .html file: $INDEX_HTML" >&2; exit 1 ;;
esac

ABS_PATH="$(python3 - "$INDEX_HTML" <<'PY'
from pathlib import Path
import sys
print(Path(sys.argv[1]).resolve())
PY
)"
DIR="$(dirname "$ABS_PATH")"
FILE="$(basename "$ABS_PATH")"

python3 - "$ABS_PATH" <<'PY'
from pathlib import Path
import re
import sys
html = Path(sys.argv[1]).read_text(encoding="utf-8", errors="ignore")
if not re.search(r"<html[\s>]", html, re.I):
    raise SystemExit("missing <html> tag")
if not re.search(r"<body[\s>]", html, re.I):
    raise SystemExit("missing <body> tag")
if "</script>" not in html and "<script" not in html:
    print("warning: no script tags found; this may be expected for static gifts", file=sys.stderr)
PY

cat <<EOF
Static H5 checks passed for: $ABS_PATH

Claude Code / Playwright verification flow:
1. Start a local server:
   python3 -m http.server 4173 --directory "$DIR"
2. Open the page:
   http://127.0.0.1:4173/$FILE
3. In Claude Code, use browser/Playwright tooling to:
   - browser_navigate to the local URL
   - browser_snapshot after load
   - inspect console errors
   - click/tap the main interactive elements
   - test a mobile viewport such as 390x844
4. If Playwright CLI is available, a quick smoke command is:
   npx playwright open "http://127.0.0.1:4173/$FILE"
EOF

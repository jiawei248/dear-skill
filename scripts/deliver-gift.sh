#!/bin/bash

set -euo pipefail

# Deliver an H5 gift file. If a hosting domain is provided, deploy it and print
# the public URL. Otherwise, print the local absolute path.
#
# Usage:
#   deliver-gift.sh <html-file> [--domain DOMAIN] [--provider PROVIDER]
#
# Or via environment:
#   DEAR_HOST_DOMAIN=mygift.surge.sh DEAR_HOST_PROVIDER=surge deliver-gift.sh <html-file>
#
# Examples:
#   deliver-gift.sh ./gifts/2026-05-06-mom/index.html
#   deliver-gift.sh ./gifts/2026-05-06-mom/index.html --domain mygift.surge.sh
#
# Output: a single JSON line describing the delivery result.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEPLOY_SCRIPT="$SCRIPT_DIR/deploy.sh"

HTML_FILE=""
DOMAIN="${DEAR_HOST_DOMAIN:-}"
PROVIDER="${DEAR_HOST_PROVIDER:-surge}"

while [ $# -gt 0 ]; do
  case "$1" in
    --domain)
      DOMAIN="${2:-}"
      shift 2
      ;;
    --provider)
      PROVIDER="${2:-}"
      shift 2
      ;;
    -h|--help)
      sed -n '6,18p' "$0"
      exit 0
      ;;
    *)
      if [ -z "$HTML_FILE" ]; then
        HTML_FILE="$1"
      else
        echo "Unexpected argument: $1" >&2
        exit 1
      fi
      shift
      ;;
  esac
done

if [ -z "$HTML_FILE" ]; then
  echo "Usage: deliver-gift.sh <html-file> [--domain DOMAIN] [--provider PROVIDER]" >&2
  exit 1
fi

if [ ! -f "$HTML_FILE" ]; then
  echo "HTML file not found: $HTML_FILE" >&2
  exit 1
fi

HTML_FILE_ABS="$(python3 -c 'import os,sys; print(os.path.abspath(sys.argv[1]))' "$HTML_FILE")"

print_result() {
  python3 - "$@" <<'PY'
import json
import sys

delivery_mode, url, html_file, provider, domain, warning = sys.argv[1:]
print(
    json.dumps(
        {
            "delivery_mode": delivery_mode,
            "url": url,
            "html_file": html_file,
            "provider": provider,
            "domain": domain,
            "warning": warning,
        },
        ensure_ascii=True,
    )
)
PY
}

if [ -z "$DOMAIN" ]; then
  print_result "local_file" "" "$HTML_FILE_ABS" "" "" ""
  exit 0
fi

if [ ! -x "$DEPLOY_SCRIPT" ]; then
  print_result "local_file" "" "$HTML_FILE_ABS" "" "" "deploy_script_not_executable"
  exit 0
fi

if DEPLOY_OUTPUT="$("$DEPLOY_SCRIPT" "$HTML_FILE_ABS" "$DOMAIN" "$PROVIDER" 2>&1)"; then
  DEPLOY_URL="$(python3 -c 'import sys; lines=[line.strip() for line in sys.stdin.read().splitlines() if line.strip()]; urls=[line for line in lines if line.startswith(("http://", "https://"))]; print(urls[-1] if urls else (lines[-1] if lines else ""))' <<<"$DEPLOY_OUTPUT")"
  if [[ "$DEPLOY_URL" != http://* && "$DEPLOY_URL" != https://* ]]; then
    DEPLOY_WARNING="$(printf '%s' "$DEPLOY_OUTPUT" | python3 -c 'import sys; print(sys.stdin.read().strip().replace("\n", " | "))')"
    print_result "local_file" "" "$HTML_FILE_ABS" "" "" "deploy_output_missing_url: $DEPLOY_WARNING"
    exit 0
  fi
  print_result "hosted_url" "$DEPLOY_URL" "$HTML_FILE_ABS" "$PROVIDER" "$DOMAIN" ""
  exit 0
fi

DEPLOY_WARNING="$(printf '%s' "$DEPLOY_OUTPUT" | python3 -c 'import sys; print(sys.stdin.read().strip().replace("\n", " | "))')"
print_result "local_file" "" "$HTML_FILE_ABS" "" "" "deploy_failed: $DEPLOY_WARNING"
exit 0

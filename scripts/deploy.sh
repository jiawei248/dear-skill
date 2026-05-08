#!/bin/bash

set -euo pipefail

# Usage: deploy.sh <html-file> <domain> [provider]
# Example: deploy.sh ./gift.html your-gifts.surge.sh surge

HTML_FILE="${1:-}"
DOMAIN="${2:-}"
PROVIDER="${3:-surge}"
SURGE_DEPLOY_MAX_ATTEMPTS="${SURGE_DEPLOY_MAX_ATTEMPTS:-2}"
SURGE_DEPLOY_RETRY_DELAY_SECONDS="${SURGE_DEPLOY_RETRY_DELAY_SECONDS:-3}"

if [ -z "$HTML_FILE" ] || [ -z "$DOMAIN" ]; then
  echo "Usage: deploy.sh <html-file> <domain> [provider]" >&2
  exit 1
fi

if [ ! -f "$HTML_FILE" ]; then
  echo "HTML file not found: $HTML_FILE" >&2
  exit 1
fi

case "$PROVIDER" in
  surge)
    if ! command -v surge >/dev/null 2>&1; then
      echo "surge is not installed. Run: npm install -g surge" >&2
      exit 1
    fi

    TMPDIR="$(mktemp -d)"
    trap 'rm -rf "$TMPDIR"' EXIT
    cp "$HTML_FILE" "$TMPDIR/index.html"
    ATTEMPT=1

    while [ "$ATTEMPT" -le "$SURGE_DEPLOY_MAX_ATTEMPTS" ]; do
      set +e
      SURGE_OUTPUT="$(surge "$TMPDIR" --domain "$DOMAIN" 2>&1)"
      STATUS=$?
      set -e

      if [ "$STATUS" -eq 0 ]; then
        printf '%s\n' "$SURGE_OUTPUT"
        echo "https://$DOMAIN"
        exit 0
      fi
      printf '%s\n' "$SURGE_OUTPUT" >&2

      if [ "$ATTEMPT" -lt "$SURGE_DEPLOY_MAX_ATTEMPTS" ]; then
        echo "surge deploy attempt $ATTEMPT failed; retrying in ${SURGE_DEPLOY_RETRY_DELAY_SECONDS}s..." >&2
        sleep "$SURGE_DEPLOY_RETRY_DELAY_SECONDS"
      else
        echo "surge deploy failed after ${SURGE_DEPLOY_MAX_ATTEMPTS} attempts" >&2
        exit "$STATUS"
      fi

      ATTEMPT=$((ATTEMPT + 1))
    done
    ;;
  *)
    echo "Unsupported provider: $PROVIDER" >&2
    exit 1
    ;;
esac

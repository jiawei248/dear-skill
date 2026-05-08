#!/bin/bash
set -euo pipefail

# Fetch an asset bundle — either an existing per-category bundle from the asset
# manifest, or a template's base/ bundle from its own template.json.
#
# Usage:
#   fetch-asset-bundle.sh <bundle-key> [base-dir] [manifest-path]
#       ↑ legacy per-category path; reads references/asset-manifest.json.
#       Example: fetch-asset-bundle.sh "image-examples/meme-sticker"
#
#   fetch-asset-bundle.sh --template <template-id> [base-dir]
#       ↑ template path; reads assets/templates/<id>/template.json,
#       downloads asset_bundle.url (verifying optional sha256),
#       and extracts into assets/templates/<id>/base/.
#       Example: fetch-asset-bundle.sh --template paper-house
#
#   fetch-asset-bundle.sh --refresh-template <template-id> [base-dir]
#       ↑ same as --template, but refreshes even when cached assets exist.
#
# Prints the extracted target directory on success.

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# --- Template mode -----------------------------------------------------------
if [ "${1:-}" = "--template" ] || [ "${1:-}" = "--refresh-template" ]; then
  TEMPLATE_MODE="${1:-}"
  TEMPLATE_ID="${2:-}"
  BASE_DIR="${3:-}"
  if [ -z "$TEMPLATE_ID" ]; then
    echo "Usage: fetch-asset-bundle.sh --template <template-id> [base-dir]" >&2
    echo "       fetch-asset-bundle.sh --refresh-template <template-id> [base-dir]" >&2
    exit 1
  fi

  if [ -z "$BASE_DIR" ]; then
    BASE_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
  fi

  TEMPLATE_DIR="$BASE_DIR/assets/templates/$TEMPLATE_ID"
  TEMPLATE_JSON="$TEMPLATE_DIR/template.json"

  if [ ! -f "$TEMPLATE_JSON" ]; then
    echo "template manifest not found: $TEMPLATE_JSON" >&2
    exit 1
  fi

  read_field() {
    python3 - "$TEMPLATE_JSON" "$1" <<'PY'
import json, sys
from pathlib import Path
data = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
bundle = data.get("asset_bundle") or {}
print(bundle.get(sys.argv[2], "") or "")
PY
  }

  BUNDLE_URL="$(read_field url)"
  BUNDLE_SHA256="$(read_field sha256)"
  BUNDLE_LOCAL_PATH="$(read_field local_path)"
  if [ -z "$BUNDLE_LOCAL_PATH" ]; then
    BUNDLE_LOCAL_PATH="base/"
  fi

  TARGET_DIR="$TEMPLATE_DIR/${BUNDLE_LOCAL_PATH%/}"
  MARKER_PATH="$TARGET_DIR/.bundle-sha256"

  if [ -z "$BUNDLE_URL" ]; then
    echo "template '$TEMPLATE_ID' has no asset_bundle.url set in template.json." >&2
    echo "See $TEMPLATE_DIR/RELEASE.md for how to create the bundle and fill in the URL." >&2
    exit 1
  fi

  if [ "$TEMPLATE_MODE" = "--template" ] && [ -d "$TARGET_DIR" ] && [ -n "$(ls -A "$TARGET_DIR" 2>/dev/null || true)" ]; then
    if [ -n "$BUNDLE_SHA256" ] && [ -f "$MARKER_PATH" ] && [ "$(tr -d '[:space:]' < "$MARKER_PATH")" = "$BUNDLE_SHA256" ]; then
      printf '%s
' "$TARGET_DIR"
      exit 0
    fi
    if [ -z "$BUNDLE_SHA256" ]; then
      printf '%s
' "$TARGET_DIR"
      exit 0
    fi
    echo "refreshing $TEMPLATE_ID asset bundle because cached marker is missing or stale" >&2
  fi

  tmpdir="$(mktemp -d)"
  trap 'rm -rf "$tmpdir"' EXIT
  zip_path="$tmpdir/bundle.zip"
  extract_dir="$tmpdir/extracted"
  mkdir -p "$extract_dir"

  echo "fetching $TEMPLATE_ID asset bundle from $BUNDLE_URL..." >&2
  case "$BUNDLE_URL" in
    http://*|https://*)
      curl -fSL --progress-bar "$BUNDLE_URL" -o "$zip_path"
      ;;
    *)
      cp "$BUNDLE_URL" "$zip_path"
      ;;
  esac

  if [ -n "$BUNDLE_SHA256" ]; then
    if command -v shasum >/dev/null 2>&1; then
      actual="$(shasum -a 256 "$zip_path" | awk '{print $1}')"
    else
      actual="$(sha256sum "$zip_path" | awk '{print $1}')"
    fi
    if [ "$actual" != "$BUNDLE_SHA256" ]; then
      echo "sha256 mismatch for $TEMPLATE_ID bundle" >&2
      echo "  expected: $BUNDLE_SHA256" >&2
      echo "  actual:   $actual" >&2
      exit 1
    fi
  fi

  unzip -oq "$zip_path" -d "$extract_dir"
  rm -rf "$TARGET_DIR"
  mkdir -p "$(dirname "$TARGET_DIR")"
  mv "$extract_dir" "$TARGET_DIR"
  if [ -n "$BUNDLE_SHA256" ]; then
    printf '%s
' "$BUNDLE_SHA256" > "$MARKER_PATH"
  fi
  printf '%s
' "$TARGET_DIR"
  exit 0
fi

# --- Legacy per-category mode ------------------------------------------------
BUNDLE_KEY="${1:-}"
BASE_DIR="${2:-}"
MANIFEST_PATH="${3:-}"

if [ -z "$BUNDLE_KEY" ]; then
  echo "Usage:" >&2
  echo "  fetch-asset-bundle.sh <bundle-key> [base-dir] [manifest-path]" >&2
  echo "  fetch-asset-bundle.sh --template <template-id> [base-dir]" >&2
  echo "  fetch-asset-bundle.sh --refresh-template <template-id> [base-dir]" >&2
  exit 1
fi

if [ -z "$BASE_DIR" ]; then
  BASE_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
fi

if [ -z "$MANIFEST_PATH" ]; then
  MANIFEST_PATH="$BASE_DIR/references/asset-manifest.json"
fi

if [ ! -f "$MANIFEST_PATH" ]; then
  echo "asset manifest not found: $MANIFEST_PATH" >&2
  exit 1
fi

bundle_url="$(python3 - "$MANIFEST_PATH" "$BUNDLE_KEY" <<'PY'
import json
import sys
from pathlib import Path

manifest = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
print(manifest.get(sys.argv[2], ""))
PY
)"

if [ -z "$bundle_url" ]; then
  echo "bundle key not found in manifest: $BUNDLE_KEY" >&2
  exit 1
fi

target_dir=""
case "$BUNDLE_KEY" in
  audio)
    target_dir="$BASE_DIR/assets/audio"
    ;;
  image-examples/*)
    target_dir="$BASE_DIR/assets/examples/$BUNDLE_KEY"
    ;;
  examples/*)
    target_dir="$BASE_DIR/assets/$BUNDLE_KEY"
    ;;
  *)
    echo "unsupported bundle key: $BUNDLE_KEY" >&2
    exit 1
    ;;
esac

if [ -d "$target_dir" ] && [ -n "$(ls -A "$target_dir" 2>/dev/null || true)" ]; then
  printf '%s\n' "$target_dir"
  exit 0
fi

mkdir -p "$target_dir"
tmpdir="$(mktemp -d)"
trap 'rm -rf "$tmpdir"' EXIT
zip_path="$tmpdir/bundle.zip"

case "$bundle_url" in
  http://*|https://*)
    curl -fsSL "$bundle_url" -o "$zip_path"
    ;;
  *)
    cp "$bundle_url" "$zip_path"
    ;;
esac

unzip -oq "$zip_path" -d "$target_dir"
printf '%s\n' "$target_dir"

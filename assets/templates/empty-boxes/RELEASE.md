# Publishing the empty-boxes Asset Bundle

The box, sticker, font, identity-reference, and example generated-photo assets are too large to ship directly in the skill repo. They live as a GitHub Release asset and are fetched on demand with:

```bash
./scripts/fetch-asset-bundle.sh --template empty-boxes
```

## Bundle Layout

The zip root must contain:

```text
boxes/
stickers/
fonts/
figures/
generated/
```

Do not include `.git/`, `.DS_Store`, `__pycache__/`, temporary work files, API-key documents, or local environment files.

## Step 1 — Stage the bundle locally

```bash
SRC=~/Desktop/empty_boxes
STAGE=/tmp/empty-boxes-bundle-v1
rm -rf "$STAGE"
mkdir -p "$STAGE"
cp -R "$SRC/boxes" "$STAGE/boxes"
cp -R "$SRC/stickers" "$STAGE/stickers"
cp -R "$SRC/fonts" "$STAGE/fonts"
cp -R "$SRC/figures" "$STAGE/figures"
cp -R "$SRC/generated" "$STAGE/generated"
find "$STAGE" -name ".DS_Store" -delete
find "$STAGE" -name "__pycache__" -type d -prune -exec rm -rf {} +
du -sh "$STAGE"
```

Expected staged size: about 110-125 MB.

## Step 2 — Zip it

```bash
cd "$STAGE"
zip -r /tmp/empty-boxes-v1.zip . -x "*.DS_Store" "*/__pycache__/*"
ls -lh /tmp/empty-boxes-v1.zip
```

## Step 3 — Compute sha256

```bash
shasum -a 256 /tmp/empty-boxes-v1.zip
```

Copy the 64-character hash into `template.json.asset_bundle.sha256`.

## Step 4 — Create the GitHub Release

Create a release with:

- tag: `assets-empty-boxes-v1`
- title: `empty-boxes asset bundle v1`
- asset: `/tmp/empty-boxes-v1.zip`

With GitHub CLI:

```bash
gh release create assets-empty-boxes-v1 /tmp/empty-boxes-v1.zip \
  --repo jiawei248/dear-skill \
  --title "empty-boxes asset bundle v1" \
  --notes "Boxes, stickers, fonts, reference figures, and example generated photos for the empty-boxes template."
```

The direct URL should be:

```text
https://github.com/jiawei248/dear-skill/releases/download/assets-empty-boxes-v1/empty-boxes-v1.zip
```

## Step 5 — Test the fetch

After updating `template.json`, run:

```bash
rm -rf assets/templates/empty-boxes/base
./scripts/fetch-asset-bundle.sh --template empty-boxes
```

The script verifies the hash, extracts into `assets/templates/empty-boxes/base/`, and writes `.bundle-sha256`.

## Updating the Bundle

For asset changes, publish a new release tag and zip:

- `assets-empty-boxes-v2`
- `empty-boxes-v2.zip`

Then update `template.json.asset_bundle.url`, `sha256`, and `size_mb`.

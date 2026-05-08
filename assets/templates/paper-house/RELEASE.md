# Publishing the paper-house Asset Bundle

The bundled stickers + fonts + reference examples (~170 MB total) are too big to ship in the skill repo itself. They live as a **GitHub Release asset** and are fetched once, on demand, the first time a gift uses this template. This doc walks you through uploading the bundle and wiring the URL back into `template.json`.

## Prerequisites

- A GitHub repo where you host the `dear` skill. If you haven't pushed it yet, create one now (public or private — both work; public is simpler for unauthenticated downloads).
- The `night-four-assets/` folder on your machine with the final sticker library, fonts, and example references.

## Step 1 — Stage the bundle locally

Make a clean staging folder matching the layout the skill expects (`base/stickers/...`, `base/fonts/...`, `base/reference/...`).

```bash
cd ~/Desktop
SRC=~/Desktop/night-four-assets
STAGE=~/Desktop/paper-house-bundle-v1
rm -rf "$STAGE"
mkdir -p "$STAGE/stickers" "$STAGE/fonts" "$STAGE/reference"

# Stickers — everything from each sticker category
cp -R "$SRC/stickers"/* "$STAGE/stickers/"

# Fonts
cp "$SRC/fonts"/*.ttf "$STAGE/fonts/"

# Reference examples — scene backgrounds, wall/floor, room sprites, character refs, story cards
cp "$SRC"/scene_*.jpg "$SRC"/scene_*.png "$STAGE/reference/" 2>/dev/null || true
cp "$SRC"/{kitchen,rooftop,karaoke,couch}_{left,right,floor}.jpg "$STAGE/reference/"
mkdir -p "$STAGE/reference/kitchen" "$STAGE/reference/rooftop" "$STAGE/reference/karaoke" "$STAGE/reference/couch"
cp "$SRC"/kitchen/*.png  "$STAGE/reference/kitchen/"
cp "$SRC"/rooftop/*.png  "$STAGE/reference/rooftop/"
cp "$SRC"/karaoke/*.png  "$STAGE/reference/karaoke/"
cp "$SRC"/couch/*.png    "$STAGE/reference/couch/"
cp "$SRC"/ref_boy.jpg "$SRC"/ref_girl.jpg "$STAGE/reference/"
mkdir -p "$STAGE/reference/story_cards/generated"
cp "$SRC"/story_cards/generated/*.png "$STAGE/reference/story_cards/generated/" 2>/dev/null || true

du -sh "$STAGE"
```

Expected total: about 140-180 MB.

## Step 2 — Zip it

```bash
cd "$STAGE"
zip -r ~/Desktop/paper-house-v1.zip . -x '*.DS_Store'
ls -lh ~/Desktop/paper-house-v1.zip
```

## Step 3 — Compute sha256

```bash
shasum -a 256 ~/Desktop/paper-house-v1.zip
```

Copy the 64-char hex string. Keep it.

## Step 4 — Create a GitHub Release and upload the zip

1. Go to your `dear` skill repo on GitHub → **Releases** → **Draft a new release**.
2. **Choose a tag** → type a new tag named exactly `assets-paper-house-v1` and click "Create new tag".
3. **Release title**: `paper-house asset bundle v1` (anything readable; not used by the skill).
4. **Description**: optional — you can note bundle size and contents for future you.
5. **Attach binaries**: drag `~/Desktop/paper-house-v1.zip` into the "Attach binaries" area. Wait for it to finish uploading.
6. **Publish release** (not "Save draft").

The direct download URL will now be:

```
https://github.com/<your-user>/<your-repo>/releases/download/assets-paper-house-v1/paper-house-v1.zip
```

Replace `<your-user>` and `<your-repo>` with your actual values. You can confirm the URL by right-clicking the zip in the release view and copying the link.

## Step 5 — Wire the URL and sha256 into `template.json`

Open `assets/templates/paper-house/template.json` and set:

```json
"asset_bundle": {
  "local_path": "base/",
  "url": "https://github.com/<your-user>/<your-repo>/releases/download/assets-paper-house-v1/paper-house-v1.zip",
  "sha256": "<the 64-char hex you copied in step 3>",
  "size_mb_estimated": 170,
  ...
}
```

Commit and push.

## Step 6 — Test the fetch

On another machine or after deleting the local `base/` dir, run:

```bash
./scripts/fetch-asset-bundle.sh --template paper-house
```

It will:
1. Read `url` and `sha256` from `template.json`.
2. Download the zip with progress output to stderr.
3. Verify the sha256.
4. Unzip into `assets/templates/paper-house/base/`.
5. Print the extracted directory on stdout.

After success, subsequent calls no-op and just print the existing directory.

## Updating the bundle (e.g. adding more stickers)

When you want to add to the bundle:

1. Re-stage locally with the new assets, zip as `paper-house-v2.zip`, and compute a new sha256.
2. Create a new release tagged `assets-paper-house-v2`, upload the new zip.
3. Update `template.json` with the new URL and sha256.
4. Users who already have the old `base/` will NOT auto-refresh (the fetch script skips when `base/` is non-empty). That's intentional — no silent re-downloads. To force a refresh, you or the user can:

```bash
rm -rf assets/templates/paper-house/base
./scripts/fetch-asset-bundle.sh --template paper-house
```

## Private repo note

If your `dear` repo is private, GitHub Release asset URLs require an auth token. For a private setup, either:

- Make just the release asset public by hosting it as a **public gist** or on **S3 / R2 / Cloudflare**, and put that URL in `template.json`; or
- Add a `GH_TOKEN` env var flow in `fetch-asset-bundle.sh` (not included by default — keep the skill unauthenticated for public use).

For the default path (public repo), no auth is needed.

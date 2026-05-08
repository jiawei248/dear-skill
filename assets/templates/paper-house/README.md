# paper-house

A scroll-through WebGL diorama of four small rooms that share a central corner. Click the hero item in each room to reveal a handwritten memory card. Each room has its own Apple Music preview, lyric-wave text, falling-word confetti, and custom decorations.

Best for: anniversaries, partners, very close friends, mother's day, love-letter-as-H5, graduation gifts — anything where a shared period or a single shared evening can be split into four emotional beats.

## Where to look

| File | What it is |
|---|---|
| `template.json` | Slot schema, hotspot layout, asset bundle URL, dependencies — the machine-readable contract |
| `SPEC.md` | Human-readable production spec: the 8 production rules, asset manifest, per-gift checklist, failure modes |
| `RELEASE.md` | How to build + publish the `base/` asset bundle as a GitHub Release |
| `template-source/` | Canonical golden HTML, `build.py`, patch scripts, story-card generation pipeline — do not modify |
| `base/` | Downloaded on first use from GitHub Release; holds the sticker library, fonts, and reference example images (~170 MB) |

## Status

- ✅ Template authored; canonical HTML is `template-source/night-four-the-turn.html`
- ✅ Production spec written (`SPEC.md`)
- ✅ Slot schema defined (`template.json`)
- ⏳ Waiting for user to run the steps in `RELEASE.md` and fill `asset_bundle.url` + `sha256` into `template.json`

Once `RELEASE.md` is done, agents can run `scripts/fetch-asset-bundle.sh --template paper-house` and start producing gifts.

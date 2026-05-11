# empty-boxes

An interactive Three.js loop of collectible boxes that turn into dense handmade memory collages. Users scroll, drag, or use keyboard navigation to rotate through tin cases, a refrigerator, a shopping basket, a library cardboard box, and other container-shaped scenes.

Best for: anniversaries, partners, close friends, birthdays, 520 gifts, and playful everyday-ritual gifts where specific shared objects matter: snacks, cold drinks, library slips, tiny trip souvenirs, apology notes, or repeated phrases.

## Where to look

| File | What it is |
|---|---|
| `template.json` | Slot schema, asset bundle URL, runtime config contract, and activation disclosure |
| `SPEC.md` | Production rules for box-fitted photos, sticker clusters, grounded copy, and verification |
| `RELEASE.md` | How to stage, zip, and publish the asset bundle as a GitHub Release |
| `template-source/tincase-box-loop.html` | Canonical authored H5; read-only source |
| `template-source/build.py` | Runtime builder that injects `window.EMPTY_BOXES_GIFT_CONFIG` and writes a standalone output HTML |
| `base/` | Downloaded on first use from GitHub Release; holds boxes, stickers, fonts, identity references, and example generated photos |

## Status

- Template authored; canonical HTML is `template-source/tincase-box-loop.html`
- Production + content spec written (`SPEC.md`)
- Slot schema defined (`template.json`)
- Runtime builder implemented (`template-source/build.py`)
- Asset bundle v1 prepared for GitHub Release and wired in `template.json`

Before making a gift, read `SPEC.md` end-to-end. The most important rule is physical fit: photos and stickers must belong to the container they are placed inside, and the final gift copy should use the user's habitual language with the recipient.

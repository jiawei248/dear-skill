# folder

An interactive H5 archive made from layered file folders. The page starts as a stack of four folders, then the lead folder opens into a tactile spread of papers, tape, photos, stickers, captions, and one specific story note.

Best for: anniversaries, partners, close friends, 520 gifts, birthdays, and relationship chapters where the material can be filed as small records: an errand, a shared ritual, a saved line, a quiet promise, or a future plan.

## Where to look

| File | What it is |
|---|---|
| `template.json` | Slot schema, asset bundle URL, runtime config contract, and activation disclosure |
| `SPEC.md` | Production rules for physical folder structure, layered paper/photo composition, grounded copy, and verification |
| `RELEASE.md` | How to stage, zip, and publish the asset bundle as a GitHub Release |
| `template-source/520-folder-gift.html` | Canonical authored H5; read-only source |
| `template-source/build.py` | Runtime builder that injects `window.FOLDER_GIFT_CONFIG` and writes a standalone output HTML |
| `base/` | Downloaded on first use from GitHub Release; holds generated examples, vendor JS, stickers, papers, tapes, frames, and fonts |

## Status

- Template authored; canonical HTML is `template-source/520-folder-gift.html`
- Production + content spec written (`SPEC.md`)
- Slot schema defined (`template.json`)
- Runtime builder implemented (`template-source/build.py`)
- Asset bundle v1 prepared for GitHub Release and wired in `template.json`

Before making a gift, read `SPEC.md` end-to-end. The most important rule is physical believability: the folder must keep its front cover, back cover, and smoothly connected tab, while photos, paper bases, tapes, and stickers feel layered inside the folder instead of floating around it.

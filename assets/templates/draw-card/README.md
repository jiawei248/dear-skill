# draw-card

A retro 3D gacha-machine H5 that turns a short wish into a saveable collectible card. The page starts with lyric rain and a pixel-photo carousel, opens a wish form, slides the request card into the machine, then asks the recipient to turn the side knob to draw the final card.

Best for: playful fan gifts, concert memories, birthdays, close friends, idol-postcard surprises, inside jokes, and light confessions where the emotional object is a card, lyric, color, or fandom cue.

## Where to look

| File | What it is |
|---|---|
| `template.json` | Slot schema, asset bundle URL, runtime config contract, and activation disclosure |
| `SPEC.md` | Production rules for card-machine copy, photo/sticker replacement, lyric handling, and verification |
| `RELEASE.md` | How to stage, zip, and publish the asset bundle as a GitHub Release |
| `template-source/retro-gacha-card.html` | Canonical authored H5; read-only source |
| `template-source/build.py` | Runtime builder that injects `window.DRAW_CARD_GIFT_CONFIG` and writes a standalone output HTML |
| `base/` | Downloaded on first use from GitHub Release; holds card photos, stickers, lyrics, carousel data, and reference assets |

## Status

- Template authored; canonical HTML is `template-source/retro-gacha-card.html`
- Production + content spec written (`SPEC.md`)
- Slot schema defined (`template.json`)
- Runtime builder implemented (`template-source/build.py`)
- Asset bundle v1 packaged and wired in `template.json`

Before making a gift, read `SPEC.md` end-to-end. The most important rule is specificity: the machine should draw a card around one concrete lyric, color, joke, concert, or phrase, and final gift-facing copy should use the user's habitual language with the recipient.

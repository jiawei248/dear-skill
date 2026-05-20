# draw-card — Template Spec

This document is the source of truth for producing a `draw-card` gift. The design principle behind every rule: **the machine should draw one meaningful card, not a random fan-art shuffle.**

## 0. What This Template Is

`draw-card` is a playful H5 built with Three.js, React, canvas drawing, and a retro gacha-machine metaphor. The page contains:

- neon lyric rain behind the scene
- a pixelated photo carousel on the machine screen
- a wish form for lyric, color, style, card style, and memo
- a request card that slides into the machine
- a draggable side knob
- a generated canvas card preview that can be saved as PNG

The canonical output is `template-source/retro-gacha-card.html`. The builder reads `filled-slots.json`, injects `window.DRAW_CARD_GIFT_CONFIG`, inlines available local assets, and writes a separate gift `index.html`.

## 1. Ready Scope

The ready version supports:

- using the bundled Eason card photos, carousel photos, stickers, lyrics, and sticker references
- overriding visible UI copy and default wish-form values
- replacing lyric rain lines from text or `lyrics.txt`
- replacing carousel photos, wish-card photos, card stickers, and decor stickers
- overriding style chips, card style chips, card template definitions, and sticker groups
- building a single output HTML without modifying the canonical HTML

It does not include an automatic card-design solver. The agent is responsible for choosing grounded text, appropriate media, and verifying that the final card renders.

## 2. The 7 Production Rules

### Rule 1 — Pick one card thesis

Before choosing photos or stickers, decide what the machine is drawing. Good theses:

- "a concert-night encouragement card built around the line the recipient keeps quoting"
- "a birthday hype card in the recipient's favorite blue"
- "a playful movie-ticket card for the friend who keeps sending stage clips"
- "a tiny comfort card that turns one lyric into a saved object"

Weak theses:

- "fan vibes"
- "cute cards"
- "make it pretty"
- "our memories"

### Rule 2 — Keep fandom language respectful

If the subject is a public figure, keep the copy playful and fandom-aware. Do not write as if the public figure personally knows the recipient unless the user explicitly provided that context. The card can feel delighted, dramatic, or funny without inventing intimacy.

### Rule 3 — Lyric use must be short and intentional

Use short user-provided lyric lines or original lines composed from the brief. Do not paste long copyrighted lyric blocks. The lyric rain works best with 8-18 short lines; each line should be readable while falling across desktop and mobile.

### Rule 4 — Photos must survive pixelation and crop

Carousel photos are pixelated and animated, so faces and gestures need strong silhouettes. Wish-card photos should leave enough margin for overlays, paper slips, stickers, and lyric text. Avoid photos where the key expression is at the extreme edge.

### Rule 5 — Stickers support the card style

Decor stickers should be selected as small semantic groups:

- stage/concert: clap board, light, camera, star
- sweet/playful: soda, ramune, sparkle, cute face
- travel/night: airplane, planet, blue accent
- soft letter: quieter stickers, lower opacity, fewer items

Avoid unrelated sticker scatter. Do not cover eyes, the main lyric, or the center of the saveable card.

### Rule 6 — Gift-facing text follows the user's language

Technical documentation is English, but gift copy is not. Use the user's natural language and address form for:

- modal title and labels
- default lyric and memo examples
- machine button copy
- toast text after delivery
- saved card filename prefix when useful

Do not default to English if the user's material is Chinese, mixed Chinese/English, or another language.

### Rule 7 — Verify the H5 in a browser

Before delivery:

- build into a separate gift folder
- open the output with a local server or `scripts/verify-h5.sh`
- confirm the 3D machine renders
- click the wish button, submit a wish, and turn the side knob
- confirm the final card preview appears and the save link works
- inspect mobile width for overlapping modal text and knob hint text
- inspect console output for failed local assets

If network is unavailable, CDN scripts may not load; report that browser verification was blocked by dependency loading rather than pretending the H5 is verified.

## 3. Slot Mapping Contract

### `recipient_material`

Use this to extract the recipient, relationship, occasion, language habit, concrete details, colors, lyrics, jokes, photos, and available source images.

### `draw_card_story_plan`

Produce one compact plan with:

- `subject_name`
- `recipient_address`
- `occasion`
- `core_lyric_or_phrase`
- `visual_language`
- `card_emotion`

This plan prevents the card machine from becoming a generic visual toy.

### `background_lyrics`

Maps to `window.DRAW_CARD_GIFT_CONFIG.lyrics`. The builder accepts:

```json
{
  "lyrics": [
    "今天只做一件事",
    "晚霞替你签收"
  ]
}
```

or:

```json
{
  "background_lyrics": {
    "text": "1）今天只做一件事\n2）晚霞替你签收"
  }
}
```

If no slot is provided, the builder uses `lyrics.txt` from the workdir or fetched `base/`.

### `carousel_photos`

Maps to `window.DRAW_CARD_GIFT_CONFIG.carouselPhotos`. Values may be asset paths such as:

```json
{
  "carousel_photos": [
    "draw-card-work/轮播图/01.jpg",
    "draw-card-work/轮播图/02.jpg"
  ]
}
```

The builder strips the `draw-card-work/` prefix and inlines files from the workdir or fetched bundle.

### `wish_card_photos`

Maps to `window.DRAW_CARD_GIFT_CONFIG.wishPhotos`. These are the hero images used inside the saveable card canvas. Keep the photo pool coherent; do not mix unrelated styles unless the card thesis calls for collage chaos.

### `character_sticker_set`

Maps to `window.DRAW_CARD_GIFT_CONFIG.wishStickers`. Bundled stickers are available at `base/generated_stickers/all/`. Custom stickers should keep a consistent circular mascot style and transparent PNG output.

### `decor_sticker_picks`

Maps to `window.DRAW_CARD_GIFT_CONFIG.decorStickers` and optionally `decorStickerGroups`. Pick a small group that matches the card style.

### `wish_copy`

Maps to `window.DRAW_CARD_GIFT_CONFIG.copy`, `wishDefaults`, `easonStyleOptions`, and `cardStyleOptions`.

Example:

```json
{
  "draw_card_copy": {
    "panelTitle": "给小予抽一张今晚的卡",
    "lyricLabel": "一句你们都知道的歌词",
    "memoPlaceholder": "演唱会 / 蓝色 / 想让 TA 笑",
    "machineButton": "投递小愿望",
    "delivered": "小卡已经进槽了，转一下旋钮"
  },
  "wish_defaults": {
    "lyric": "今天只做一件事",
    "theme_color": "#7fded8",
    "eason_style": "温柔暴击",
    "card_style": "文艺信笺"
  }
}
```

### `draw_card_runtime_overrides`

Use this for advanced edits: `cardTemplates`, `wishStyleCandidates`, `decorStickerGroups`, style chips, and media lists. Keep replacement card templates inside the 512x728 canvas coordinate system.

## 4. Runtime Builder Contract

Command:

```bash
python3 assets/templates/draw-card/template-source/build.py \
  --slots ./gifts/<date>-<recipient>/draw-card-work/filled-slots.json \
  --workdir ./gifts/<date>-<recipient>/draw-card-work \
  --out ./gifts/<date>-<recipient>/index.html
```

The builder:

1. reads `filled-slots.json`
2. normalizes copy, defaults, lyrics, media lists, sticker lists, and override groups
3. resolves assets from the workdir, `assets/templates/draw-card/base/`, or `template-source/`
4. injects `window.DRAW_CARD_GIFT_CONFIG`
5. writes `draw-card-work/runtime_config.json`
6. writes the final `index.html`

It does not modify `template-source/retro-gacha-card.html`.

Asset paths may be written either relative to the workdir (`card_materials/card_photo_01.jpg`) or with the documented workdir prefix (`draw-card-work/card_materials/card_photo_01.jpg`). The builder strips the `draw-card-work/` prefix before inlining, so the final single-file HTML does not keep fragile local relative paths.

## 5. Per-Gift Checklist

- [ ] The card machine has one clear thesis.
- [ ] Visible copy uses the user's habitual language with the recipient.
- [ ] Lyrics are short, intentional, and not a pasted long copyrighted block.
- [ ] Photos are crop-safe after pixelation and overlays.
- [ ] Stickers support the chosen card style and avoid covering key content.
- [ ] Default form values feel personal and grounded.
- [ ] The final H5 opens, renders the 3D machine, accepts a wish, turns the knob, and saves the card.

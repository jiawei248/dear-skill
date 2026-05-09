# Bouquet Template Spec

This spec describes how dear should treat the `bouquet` template.

## Ready Scope

The `bouquet` template is a ready, first-class dear template: it is discoverable through the template registry, uses an external asset bundle for large visual assets, maps user material into bouquet-specific slots, and builds a standalone H5 through `template-source/build.py`.

The canonical HTML is read-only: `template-source/mothers-day-blue-bouquet.html` is copied from the source project and should not be modified directly. Runtime work happens through `template-source/build.py`, which reads filled slots and writes a separate gift `index.html`.

## User-Facing Opening

When the user activates this template, briefly explain:

> 这是一束可以互动调整的花：flowers can be dragged, gems can be freely added, paper-card positions can move, and cards can be edited interactively with AI.

Ask for any desired flowers, color palette, and recipient material. The user may drag screenshots, photos, chat excerpts, or text into the conversation. Card text should stay tightly grounded in the user's supplied language and details, similar to the `paper-house` standard.

## Asset Bundle

The template's large visual assets live in an asset bundle, not in the normal repo tree.

Bundle layout:

```text
bouquet-v1/
├── flowers/
├── greenery/
├── gems/
├── fonts/
└── reference/
    └── original-png/
```

Runtime fetch:

```bash
scripts/fetch-asset-bundle.sh --template bouquet
```

The bundle should be refreshed by publishing `assets-bouquet-v2`, updating `template.json.asset_bundle.url`, and updating `template.json.asset_bundle.sha256`. The fetch script compares `base/.bundle-sha256` against the manifest and re-fetches on mismatch.

## Material Style Contract

Built-in and generated flowers should preserve the existing style:

- transparent cutout PNGs
- soft film texture
- painterly floral shapes
- occasional gem-like highlights or jewelry accents
- gentle blue / violet / pastel compatibility unless the user asks for another palette

Users can add new flowers and gems later. Generated additions may use a general image generation model, but must use the existing bundle's flowers and original references as style anchors.


## Slot Mapping Contract

The bouquet manifest follows the common template schema where possible, with bouquet-specific details in supplemental fields. Slot matching should fill these slots before the build step.

### `recipient_material`

Accept photos, chat_screenshots, social_screenshots, text, and notes. Card text must stay close to the user's supplied original language and details: screenshots, quoted phrases, visible facts, relationship specifics, and the user's stated intent. Do not write generic blessing copy that could fit anyone.

### `bouquet_style_direction`

Resolve the bouquet's color_palette, emotional_tone, occasion, and recipient_language. The user can specify preferences such as:

- “想要蓝紫色”
- “想要更像夏天”
- “白玫瑰 + 蓝宝石”
- “不要太母亲节，像朋友之间的礼物”

If the user gives no palette, infer one from the recipient material and the existing blue/pastel bouquet mood.

### `flower_picks`

Use `library_subpaths: ["flowers/", "greenery/"]`, choose within the count_range, and keep placement in the bouquet-canvas zone. The default runtime mapping writes selected or generated assets to `bouquet-work/flowers/{n}.png`.

Style rules:

- film-textured floral cutouts
- transparent PNG with soft hand-cut edges
- flowers may include gem or subtle sparkle accents
- must stay close to existing bouquet asset texture, not clean generic AI stickers

Extension policy: users may add new florals later. New flowers can be generated with a general image generation model, but must reference `base/flowers/` and `base/reference/original-png/` for texture, edge quality, color behavior, and gem/glimmer accents.

### `gem_picks`

Use `library_subpaths: ["gems/"]`. Gems can be freely added to the canvas as decoration, emotional markers, and visual rhythm around flowers and paper cards.

### `card_notes`

Use `type: ai_text` with `per_card: true`. Each card carries one concrete memory or emotion. It must quote or closely adapt user-provided original language, details, screenshot content, or relationship facts. Avoid generic lines such as “愿你天天开心” unless the user explicitly asks for that wording. The user can ask “这张改得更像我说话”, and the card should be revised interactively.

### `layout_editing_contract`

At activation, tell the user:

- flowers can be dragged
- gems can be freely added
- paper card positions can be changed
- card content can be revised interactively with AI

This is part of the template experience, not an implementation detail.

## Runtime Slot Mapping

- `recipient_material` supplies the facts, quotes, screenshots, and language for card text.
- `bouquet_style_direction` captures color palette, occasion, and emotional tone.
- `flower_picks` maps to bundle flowers/greenery.
- `gem_picks` maps to bundle gems.
- `card_notes` maps to small editable paper notes.

## Runtime Builder Contract

`template-source/build.py` reads `filled-slots.json`, normalizes bouquet slots, and injects a single `window.BOUQUET_GIFT_CONFIG` script into the generated `index.html`. The builder does not modify the canonical HTML source; it only reads `template-source/mothers-day-blue-bouquet.html` and writes the requested `--out` file.

Runtime config fields:

- `style` captures `color_palette`, `emotional_tone`, `occasion`, and `recipient_language` from `bouquet_style_direction`.
- `catalog` optionally narrows or extends the flower palette shown in the H5.
- `gemCatalog` optionally narrows or extends the gem palette shown in the H5.
- `layout.stems` seeds the initial draggable flowers.
- `layout.placedGems` seeds the initial freely placed gems.
- `cards` maps flower catalog ids to paper-card label/title/text and optional card positions.
- `giftCopy` sets the visible recipient line and primary gift-card message.

The default H5 remains openable without injected config. When config is present, it overrides only the relevant runtime data and preserves the existing drag, gem placement, note modal, save, and mobile scaling behavior.

The generated `index.html` should be standalone: selected flower and gem assets are inlined as data URLs, and missing optional font files must not cause browser console errors.

Verification for every generated bouquet H5:

```bash
scripts/verify-h5.sh ./gifts/<slug>/index.html
```

Then open the page in a browser or Playwright and check that the page loads, flowers render and can be dragged in edit mode, gems can be added, paper-card chips are readable and movable, card text opens in the modal, the 390x844 mobile viewport is not visually cropped, and the console has no errors.

## Build Contract

`template-source/build.py` accepts:

```bash
python3 assets/templates/bouquet/template-source/build.py \
  --slots ./gifts/<slug>/bouquet-work/filled-slots.json \
  --workdir ./gifts/<slug>/bouquet-work \
  --out ./gifts/<slug>/index.html
```

The final gift output is `index.html`. The canonical source HTML remains read-only.

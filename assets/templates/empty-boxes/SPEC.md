# empty-boxes — Template Spec

This document is the source of truth for producing an `empty-boxes` gift. The design principle behind every rule: **the container is not a frame; it is the memory's physical logic.**

## 0. What This Template Is

`empty-boxes` is a playful H5 built with Three.js, Preact, p5.js, and canvas compositing. The page shows a looping vertical carousel of collectible boxes. Some boxes are plain container assets; the featured boxes become canvas-rendered collages made from:

- a container asset such as a tin case, refrigerator, shopping basket, or cardboard box
- generated or processed photos
- cutout figures
- sticker clusters
- tape, paper, labels, number beads, receipts, and handwritten notes
- background gem stickers and floating labels around the 3D loop

The canonical output is `template-source/tincase-box-loop.html`. The builder reads `filled-slots.json`, injects `window.EMPTY_BOXES_GIFT_CONFIG`, inlines available local assets, and writes a separate gift `index.html`.

## 1. Ready Scope

The ready version supports:

- using the bundled canonical boxes, stickers, fonts, and example generated photos
- overriding chrome labels, ambient gems, box assets, and per-box collage layers
- replacing default collage assets with generated per-gift photos
- editing a layer by id through `collages.<box_id>.layersById`
- replacing an entire collage through `collages.<box_id>.layers`
- building a standalone `index.html` without modifying the canonical HTML

It does not include an automatic semantic layout solver. The agent is responsible for choosing good layers and verifying the composition.

## 2. The 7 Production Rules

### Rule 1 — Each box needs a focused theme

Every featured box must have one clear theme and a few grounded details. Good themes:

- "the night we put the argument in the fridge"
- "the snack run where the cart filled itself"
- "the rainy library table and the bookmark line"
- "the small trip where the sea wind became a ticket stub"

Weak themes:

- "our memories"
- "sweet couple moments"
- "things you like"
- "birthday vibes"

Use the user's material to select a memory anchor: a quote, nickname, object, date, place, food, gesture, screenshot line, or repeated habit. If the material is thin, make fewer boxes and write smaller notes.

### Rule 2 — Photos must fit the container geometry

The photo shape and pose must match the physical container.

Refrigerator:
- Treat the fridge as a vertically divided object. If it reads as three shelves or layers, use one photo or figure per shelf, or a main photo plus two shelf-height cutouts.
- Stagger figures left/right across shelves so the composition feels placed by hand.
- Food and cold-drink stickers belong on or near shelves, magnets, and notes; they should not float randomly over the whole fridge.

Shopping basket:
- Use a top-down or slightly overhead photo, or a person leaning on / holding the basket rim.
- Keep snacks, drinks, produce, receipts, and checkout labels grouped inside the basket shape.
- A figure can overlap the rim, but should feel supported by the basket, not pasted on top of it.

Library/cardboard box:
- Use paper frames, slips, coffee, glasses, stamps, tabs, and bookish labels.
- Photos can be tucked under paper or inside a frame; do not leave frame stickers empty.

Tin case / travel box:
- Use travel receipts, film photos, tickets, small objects, and labels as one packed keepsake tray.
- Main photo and souvenirs should feel like they were saved in the same box.

### Rule 3 — Sticker clusters must form readable motifs

Stickers should gather into 2-4 organic clusters per box:

- a dessert shelf
- a checkout snack pile
- a paper-slip corner
- a travel keepsake tray
- a cold-drink apology cluster

Avoid evenly scattering single stickers across the whole container. A good cluster has overlap, scale variation, and semantic relation. A bad cluster looks like confetti.

All stickers should stay within the visual bounds of the container unless a layer is intentionally outside decoration, such as a receipt floating behind the box. When using rotated stickers, check the whole rotated bounding box, not only the center point.

### Rule 4 — Notes and captions use the user's language

Technical documentation is English, but gift copy is not. The final visible text must use the language and tone the user naturally uses with the recipient.

Rules:
- Use the user's address form: nickname, "mom", "宝", "小A", "Ren", etc.
- Echo exact short phrases from the user's material when they carry emotional value.
- Keep the text specific. "You always ask whether I will like this snack" is better than "you are thoughtful."
- Do not over-romanticize a casual friendship or over-casualize a serious apology.

### Rule 5 — Frames and containers cannot be empty

Any sticker or layer that visually implies an inner surface must be filled:

- photo frames
- polaroids
- TV screens
- notebook windows
- library cards
- shopping basket compartments
- refrigerator shelves

If a frame sticker is selected, pair it with an inner photo, paper layer, or label. Empty frames make the template feel unfinished.

### Rule 6 — Identity must stay consistent

When the user provides photos:

- preserve recognizable face structure, hair, age, skin tone, and styling across all generated photos
- keep the same protagonist(s) across boxes unless the story explicitly changes
- avoid stiff studio poses; this template wants candid, Fujifilm-like memory photos

When photos are unavailable:

- generate consistent non-specific characters
- keep clothing palette and body proportions stable
- do not pretend the generated people are exact likenesses

### Rule 7 — Verify the H5 in a browser

Before delivery:

- build into a separate gift folder
- open the output with a local server or `scripts/verify-h5.sh`
- confirm Three.js renders the rotating loop
- confirm the active number changes when scrolling or dragging
- confirm featured collages load and no major image is blank
- inspect mobile width for overlapping labels
- inspect console output for failed local assets

If network is unavailable, the CDN scripts may not load; in that case, report that browser verification was blocked by dependency loading rather than pretending the H5 is verified.

## 3. Slot Mapping Contract

### `recipient_material`

Use this to extract the recipient, relationship, occasion, language habit, concrete details, quotes, photos, and available source images.

### `box_story_plan`

Produce 3-8 box plans. Each plan must include:

- `box_id`
- `container`
- `theme`
- `memory_anchor`
- `quoted_or_echoed_detail`
- `visual_motif`

Do this before choosing stickers. The story plan prevents the collage from becoming generic decoration.

### `box_surface_selection`

Choose container images from `base/boxes/`. Match physical shape to story:

- `box_3.jpeg`: refrigerator / cold-storage / domestic repair
- `box_4.png`: shopping basket / grocery / snack run
- `box_5.png`: cardboard/library/paper archive
- `box_1.png`: tin-case keepsake / travel / first trip

Other bundled boxes can be used as plain loop items or custom collage bases when the story fits.

### `box_photo_generation`

Generate or process photos for each featured box. Prompts should include:

- identity references when available
- exact box type and physical placement target
- scene/backdrop
- moment/gesture
- composition constraints
- crop safety
- things to avoid: readable text, watermark, extra people, distorted hands, empty faces

For the refrigerator example, prefer shelf-height vertical figure cutouts and a horizontal couple photo. For the shopping basket, prefer a cart-rim cutout or overhead couple photo.

### `sticker_cluster_picks`

Pick semantically related stickers from the bundled library. The default library includes food, decorations, frames, electronic devices, gems, and dolls. Food and supermarket stickers are especially important for refrigerator and shopping-basket boxes.

### `box_collages`

This slot maps directly into `window.EMPTY_BOXES_GIFT_CONFIG.collages`.

Use `layersById` for small edits:

```json
{
  "box_collages": {
    "fridgeConflict": {
      "assets": {
        "coupleKitchen": "empty-boxes-work/generated/fridge/photos/couple.jpg"
      },
      "layersById": {
        "main-couple-photo": {
          "caption": "把冷战放进冰箱"
        },
        "fridge-note": {
          "note": {
            "lines": ["那晚我们都停了一下，", "先把坏情绪冷藏。"],
            "sign": "下次也慢一点，好好说。"
          }
        }
      }
    }
  }
}
```

Use `layers` for a full replacement. Layer coordinates are in the collage canvas coordinate system. `x` and `y` are centers except for `type=box`, which uses top-left `x/y`.

### `gift_copy`

Maps to the background labels. This is visible gift text, so use the user's natural language.

### `ambient_gems`

Optional background gem replacements. Keep them quiet; the boxes should stay visually dominant.

## 4. Runtime Builder Contract

Command:

```bash
python3 assets/templates/empty-boxes/template-source/build.py \
  --slots ./gifts/<date>-<recipient>/empty-boxes-work/filled-slots.json \
  --workdir ./gifts/<date>-<recipient>/empty-boxes-work \
  --out ./gifts/<date>-<recipient>/index.html
```

The builder:

1. reads `filled-slots.json`
2. normalizes chrome labels, optional box assets, ambient gems, and collage overrides
3. resolves assets from the workdir, `assets/templates/empty-boxes/base/`, or `template-source/`
4. injects `window.EMPTY_BOXES_GIFT_CONFIG`
5. writes `empty-boxes-work/runtime_config.json`
6. writes the final `index.html`

It does not modify `template-source/tincase-box-loop.html`.

Asset paths may be written either relative to the workdir (`generated/fridge/photos/couple.jpg`) or with the documented workdir prefix (`empty-boxes-work/generated/fridge/photos/couple.jpg`). The builder strips the `empty-boxes-work/` prefix before inlining, so the final single-file HTML does not keep fragile local relative paths. The builder also accepts both the manifest slot name `box_surface_selection` and the legacy override name `box_assets` for custom loop box surfaces.

## 5. Per-Gift Checklist

- [ ] The gift has 3-8 boxes, or fewer if the material is intentionally sparse.
- [ ] Every featured box has a focused theme and a concrete memory anchor.
- [ ] Photos match container subdivisions and do not fight the box shape.
- [ ] Refrigerator shelves / basket areas / frame windows are not empty.
- [ ] Stickers are grouped into readable motifs and stay inside bounds.
- [ ] Captions and notes use the user's habitual language with the recipient.
- [ ] No generic filler replaces available specific details.
- [ ] The final H5 opens, renders, rotates, and works on mobile width.

## 6. Failure Modes

| Failure | Fix |
|---|---|
| Stickers look randomly scattered | Reduce count and group them around a motif |
| Figure crosses refrigerator shelves awkwardly | Regenerate or crop to shelf-height figures |
| Shopping basket looks like a flat scrapbook | Add basket-rim interaction, overhead perspective, and snack clusters inside the basket |
| Text feels generic | Return to `recipient_material`; quote or echo a real phrase |
| Frame sticker is empty | Add an inner photo, paper, or label layer |
| Output HTML has missing images | Fetch the asset bundle or place generated assets under the build workdir |

# Templates

A **template** is a pre-designed gift shape that the user can fill with their own context. Templates exist for two reasons:

1. The user already knows what they want — a specific concept that's been done well — and just needs to personalize it
2. Some gift shapes are visually elaborate enough that producing them from scratch every time would be expensive, slow, or unstable

When a template is used, the skill bypasses the from-scratch creative pipeline (Stage 1 / 2 / 2.5 / Format Selection) and goes straight to filling the template's slots with the user's content.

## How Template Mode Differs From the Default Flow

| Default flow (creative path) | Template mode |
|---|---|
| User provides recipient + moment context | User picks a template + provides recipient context |
| Stage 1: editorial judgment decides weight + direction | **Skipped** — template encodes both |
| Stage 2 + 2.5: synthesis + 5 concept candidates | **Skipped** — concept is the template |
| Format Selection | **Skipped** — template's format is fixed |
| Stage 3: visual strategy | **Reduced** — template's visual is fixed; only per-gift assets are planned |
| Stage 4: rendering from concept | **Replaced** by template build pipeline |

Template mode is closer to "visualization-only" than to a full gift, but with one key difference: **the matching of user content to template slots is itself a creative act** done by the skill.

## Template Discovery

Available templates live in `{baseDir}/assets/templates/<template-id>/`. Each subdirectory containing a `template.json` is an installed template.

To list available templates, scan that directory and read each `template.json`'s `name`, `description`, and `best_for` fields.

When the user asks for templates (e.g. "list templates", "show me templates", or the same intent in another language), the skill responds with a brief list:

```
Available templates:

📦 paper-house — Night in Four Acts
   An interactive layered scene of 4 small rooms. Click items to reveal memories.
   Best for: anniversaries, partners, very-close-friends, love-letter-as-H5.

💐 bouquet — Cyber Trophy Bouquet
   给妈妈做一张赛博奖杯花束插画，每一朵花都藏着一个你们的故事。
   Best for: birthdays, Mother's Day, thank-you gifts, friend comfort, anniversaries.

🧺 empty-boxes — Tin-Case Memory Loop
   A rotating loop of collectible boxes: fridge shelves, shopping baskets, cardboard boxes, and tin cases become dense grounded memory collages.
   Best for: partners, 520, birthdays, close friends, everyday rituals, snack runs, small reconciliations.

🗂 folder — Layered Memory Archive
   Four believable file folders open into layered papers, varied photo formats, tapes, stickers, captions, and grounded chapter notes.
   Best for: partners, 520, birthdays, close friends, relationship chapters, saved quotes, future plans.

🎴 draw-card — Retro Gacha Wish Machine
   A neon 3D card-drawing machine: fill a lyric/memo wish card, slide it into the slot, turn the knob, and save the drawn card.
   Best for: fan gifts, concert memories, birthdays, close friends, idol-postcard surprises, playful jokes.
```

If the user asks for details on one, read the rest of its `template.json` and show `slots` summary.

## Template Triggering

Three triggers, all valid:

### Explicit
```
/dear --template paper-house ~/Desktop/for-mia/
/dear use the paper-house template for Mia with ~/Desktop/for-mia/
/dear --template bouquet 给妈妈做一束可以拖动的花
/dear 用 bouquet 模板给朋友做一份生日礼物
/dear --template empty-boxes 给 TA 做一个零食购物篮回忆盒
/dear --template folder 给 TA 做一组可以打开的回忆文件夹
/dear --template draw-card 给 TA 做一台可以抽小卡的复古许愿机
```
Skill detects an explicit template id or manifest alias, loads `template.json`, jumps to slot-matching.

### Browse → Pick
```
/dear show me templates
  → skill lists templates
  → user: use paper-house
  → skill: Put your material in a folder and send me the path, or paste/attach it here.
```

### Implicit Recommendation (Optional)
During a normal creative-path run, at Format Selection the skill scans the template registry. If a template's `best_for` and `tone` strongly match the locked concept, the skill may say:

> I just realized paper-house is almost exactly this idea: four small rooms with clickable memories. Want to use that? It'll be more stable than building from scratch, and it already has a rich sticker/room system.

If the user says yes, switch to template mode. If no, continue the creative path.

Never force this recommendation — it's an offer, not a redirect.

## The `template.json` Manifest

Every template directory MUST contain a `template.json` with this shape:

```json
{
  "id": "<short-slug, matches dirname>",
  "name": "<human-friendly title>",
  "description": "<one paragraph: what this template is, what experience it delivers>",
  "preview": "preview.jpg",
  "best_for": ["anniversary", "partner", "..."],
  "tone": ["intimate", "warm", "..."],
  "format": "h5" | "image" | "text",
  "approx_size_mb": <number>,

  "slots": [ ... see Slot Types below ... ],

  "asset_bundle": {
    "local_path": "base/",
    "url": "https://github.com/<user>/<repo>/releases/download/<tag>/<file>.zip",
    "sha256": "<optional, recommended>",
    "size_mb": <number>
  },

  "build_script": "build.py",
  "build_contract": {
    "input": "filled-slots.json",
    "output": "index.html"
  }
}
```

### Slot Types

Slots describe **what content the template needs and where it comes from**. There are five canonical slot types:

#### `ai_generated_image`
The skill generates a brand-new image at gift-time, sized to the slot.

```json
{
  "id": "kitchen_wall_left",
  "type": "ai_generated_image",
  "aspect_ratio": "9:16",
  "approx_size": [720, 1280],
  "prompt_hint": "wall of a small intimate apartment kitchen at night, warm lamp light from off-screen, painterly storybook style",
  "style_anchor": "{baseDir}/assets/templates/paper-house/style-reference.jpg",
  "consistency_group": "paper-house-room-walls"
}
```

Notes:
- `prompt_hint` is the SEED — slot-matching may enrich it with user-context details
- `style_anchor` is an optional reference image the generation prompt should anchor on, for visual consistency across slots in the same template
- `consistency_group` lets the skill pass the same seed/style across related slots so that all walls in the same template look like one world
- Keep base slot fields aligned with the common schema. Put template-specific details in supplemental fields such as `template_notes`, `runtime_mapping`, or `physical_rules` instead of inventing alternate names for common concepts.
- The skill uses the existing image-generation path (`render-image.sh` or in-Claude image generation when available)

#### `sticker_picks`
The skill picks N stickers from the template's library based on the user's recipient context. N is variable — the AI chooses how many fit visually.

```json
{
  "id": "kitchen_decorations",
  "type": "sticker_picks",
  "library_subpaths": ["stickers/food/", "stickers/plants/", "stickers/pets/"],
  "count_range": [3, 8],
  "placement_zone": "kitchen_floor_area",
  "selection_hint": "things that suggest cooking together — utensils, food, a small plant on the counter"
}
```

Notes:
- `library_subpaths` are paths inside the template's `base/` bundle
- `count_range` is a soft hint — the skill picks based on what looks good
- `placement_zone` corresponds to a named region in the template HTML
- Stickers are PNGs with alpha; the skill positions them with the template's layout logic

#### `user_image_processed`
The user provides a photo; the skill processes it through a deterministic pipeline (no generation).

```json
{
  "id": "character_portrait",
  "type": "user_image_processed",
  "count": "1-2",
  "required": false,
  "purpose": "A photo of TA (and optionally the user) used as the character figure in each scene.",
  "pipeline": [
    {"step": "stylize-character", "params": {"outline_width": 6, "outline_color": "#ffffff"}}
  ],
  "fallback_when_missing": "skip"
}
```

The `pipeline` is a list of `{step, params}` operations. Available steps:
- `stylize-character` — runs `scripts/stylize-character.sh` (cutout + outline)
- `crop-to-aspect` — crops to a given aspect ratio
- (more can be added)

`fallback_when_missing` controls behavior when the user provides no photo:
- `skip` — the slot is empty, character figure is omitted
- `default` — use a default asset bundled in `base/`

#### `ai_text`
AI-written text, generated from the recipient brief and any user-provided source material.

```json
{
  "id": "kitchen_lyrics",
  "type": "ai_text",
  "lines": 2,
  "max_chars_per_line": 70,
  "style_hint": "lyrics-like, intimate, present-tense, in the language the user uses with the recipient",
  "source_priority": [
    "user_provided_song_lyrics",
    "ai_pick_from_song_in_recipient_brief",
    "ai_compose_from_memories"
  ],
  "scene_id": "kitchen"
}
```

`source_priority` is the search order:
1. If the user provides explicit lyrics for this slot, use them verbatim
2. Else, if the recipient brief mentions a specific song, AI picks 2 fitting lines from it
3. Else, AI composes 2 original lines from the user's memories that fit this scene

#### `hotspot_map`
Clickable interactive zones inside a scene, each tied to a memory popup.

```json
{
  "id": "scene_hotspots",
  "type": "hotspot_map",
  "scenes": {
    "kitchen": [
      {"hotspot_id": "stove", "label": "stove"},
      {"hotspot_id": "fridge", "label": "fridge"},
      {"hotspot_id": "mug", "label": "mug"}
    ],
    "rooftop": [
      {"hotspot_id": "telescope", "label": "telescope"},
      {"hotspot_id": "fence", "label": "fence"}
    ]
  },
  "popup_contract": {
    "max_chars": 80,
    "tone": "specific, personal, not abstract",
    "source": "ai_assigns_memories_to_hotspots"
  }
}
```

The skill maps each user memory snippet to the hotspot whose label feels closest, optionally consulting the user during the edit loop.

## Asset Bundle Convention (OSS)

For templates with > ~5MB of skeleton assets, do NOT bundle assets in the skill repo. Use the `asset_bundle` URL pattern.

### Recommended host: GitHub Release assets

GitHub Release assets are free, have a 2GB per-file limit, and serve fast direct download URLs.

To prepare a bundle:
1. Organize the template's skeleton assets in a folder, in the directory layout the template's `build.py` expects
2. Zip it: `cd folder && zip -r ../bundle.zip .`
3. On GitHub: Releases → Create a new release → tag `assets-<template-id>-v1`
4. Drag the zip into the release asset uploader → Publish
5. The download URL is: `https://github.com/<user>/<repo>/releases/download/<tag>/<file>.zip`
6. Compute sha256: `shasum -a 256 bundle.zip` and put it in `template.json`

To version up assets (e.g. add 50 new stickers):
- Cut a new release (`assets-<id>-v2`) with the new zip
- Update `template.json`'s `url` and `sha256`
- Users will re-fetch on next use

### How the skill fetches a bundle

When entering template mode the skill checks `assets/templates/<id>/base/.bundle-sha256` against `template.json.asset_bundle.sha256`.

1. If `base/` is non-empty and `.bundle-sha256` matches the manifest, reuse the cached bundle.
2. If `base/` is missing, empty, missing `.bundle-sha256`, or has a mismatched sha, download the zip to a temp file.
3. Verify sha256 when present.
4. Unzip into a temp directory first, then replace `assets/templates/<id>/base/` and write `base/.bundle-sha256`.
5. If the user explicitly requests a refresh, run `scripts/fetch-asset-bundle.sh --refresh-template <id>` to force replacement even when the marker matches.

`scripts/fetch-asset-bundle.sh` is the runtime entry. It supports both the existing per-category bundle pattern and template bundles via `--template <id>` / `--refresh-template <id>`.

## The Slot-Matching Flow

This is the new "Stage 0.5" specific to template mode. It happens after intake and before build.

```
Read template.json
   ↓
Read all user material from intake (folder, brief, attached images)
   ↓
For each slot in template.json:
   - ai_generated_image:    queue for generation; consult recipient brief to enrich prompt
   - sticker_picks:         scan recipient brief for matches against stickers in declared library_subpaths
   - user_image_processed:  find matching photo in intake, queue for pipeline run
   - ai_text:               apply source_priority chain
   - hotspot_map:           pull memory snippets from notes/chat, score each against each hotspot label, assign best matches
   ↓
Show the user a "fill preview" — markdown-formatted list of every filled slot with its content
   ↓
Enter the natural-language edit loop (see below)
   ↓
On user "ok" / "yes" / "go" / equivalent in the user's language → run template build_script
```

### The Fill Preview

Show the user a clear, scannable preview before building. Example:

```
I'm planning to fill paper-house for Mia like this:

🍳 kitchen
   Main scene: regenerated (painterly nighttime apartment kitchen)
   Stickers: bowl, steam-cloud, plant, blue-mug, pot, oven-mitt (6 picked from food/plants/)
   Lyric-prose:
     "fall back into place, tender is the night"
     "falling through the atmosphere, it was just you and me"
   Clickable items:
     · stove → "the first tomato pasta I cooked for you, and you somehow ate three bowls"
     · fridge → "you saw the expired yogurt and laughed for way too long"
     · mug → "the blue mug you quietly stole from me"

🌆 rooftop
   ...

Character: mia-IMG_2341.jpg → cutout + white outline

---
Should I start building from this, or do you want to adjust anything?
```

### The Natural-Language Edit Loop

Accept any of:
- "ok" / "yes" / "go" / equivalent in the user's language → proceed to build
- Anything that mentions a specific slot to change → re-fill that slot, show updated preview, ask again
- Anything ambiguous → ask one short clarifying question

Examples and how to interpret:

| User says | Skill interprets |
|---|---|
| "change the kitchen lyrics" | re-fill `kitchen_lyrics` slot, possibly with a different song or original composition |
| "replace the stove memory with ___" | replace specific hotspot popup text |
| "I don't want to use this song" | mark `user_provided_song_lyrics` as cleared, regenerate all `ai_text` slots that depend on it |
| "use Mia's 0087 photo instead" | switch `character_portrait` source, re-run pipeline |
| "the rooftop stickers feel too sparse" | re-pick `rooftop_decorations` with higher count |
| "the whole thing feels too cold" | broader feedback — adjust style hints across multiple slots |

After every edit, re-show only the changed slots in the preview, not the whole thing.

Never use structured commands (`/edit`, `--slot`). User speaks naturally; skill parses.

The loop has no hard turn limit. It ends when the user says they're ready.

## Build Pipeline

Each template provides a `build.py` (or whatever script its `build_script` field points to). Contract:

**Input**: a single `filled-slots.json` file in the working dir, containing every slot's resolved value:
```json
{
  "kitchen_wall_left": {"resolved_path": "/tmp/dear-build-x/kitchen_wall_left.png"},
  "kitchen_decorations": {"resolved_paths": ["...stove.png", "...pot.png", ...]},
  "kitchen_lyrics": {"lines": ["fall back into place...", "falling through..."]},
  "scene_hotspots": {"kitchen": [{"hotspot_id": "stove", "popup": "the first dinner we cooked..."}, ...]},
  ...
}
```

**Output**: a single `index.html` in the working dir's `./gifts/<date>-<recipient-slug>/` folder, with all assets base64-inlined (per the existing single-file H5 rule).

Invoke builders with explicit runtime paths when supported:

```bash
python3 <template-dir>/<build_script> \
  --slots ./gifts/<date>-<recipient-slug>/<template-id>-work/filled-slots.json \
  --workdir ./gifts/<date>-<recipient-slug>/<template-id>-work/ \
  --out ./gifts/<date>-<recipient-slug>/index.html
```

A template builder must treat authored template files as read-only. Per-gift content is read from `filled-slots.json` and `--workdir`; the only HTML it writes is the `--out` file. For templates with generated assets, prefer a single `<template-id>-work/` staging directory under the gift folder so the final artifact and intermediate assets do not mix.

The skill orchestrates: prepares filled-slots.json → invokes build.py → moves output to the gift folder → continues to delivery.

## Where Each Slot Type's Asset Comes From

| Slot type | Comes from | Cost |
|---|---|---|
| `ai_generated_image` | Image generation API at gift-time | High per-gift cost; bounded by number of slots |
| `sticker_picks` | Template's bundled `base/stickers/` (downloaded once from OSS) | Zero per-gift |
| `user_image_processed` | User's intake folder | Local processing only (cutout + outline) |
| `ai_text` | Claude in-context | Cheap |
| `hotspot_map` | Claude in-context, mapping user memories to template-defined zones | Cheap |

The intent: **stickers are bundled (free per use), walls/floors are AI-generated (variable per use), text is Claude (cheap), character is local processing (deterministic)**. No generic web image search — that breaks visual cohesion.

## Adding New Templates

To add a template:

1. Create `assets/templates/<id>/`
2. Write `template.json` following the schema above
3. Write `template.html` with placeholder zones the build script will fill
4. Write `build.py` that reads `filled-slots.json` and emits `index.html`
5. Stage skeleton assets (stickers, optional defaults) into a folder mirroring the structure declared in `library_subpaths`
6. Zip + upload to GitHub Release as described above
7. Add the URL and sha256 back to `template.json.asset_bundle`
8. Add a one-paragraph entry to this file under "Available Templates" below

The skill needs no code changes per new template — it reads `template.json` and obeys.

## Available Templates

### `paper-house` — Night in Four Acts

A WebGL scroll-through diorama of four small rooms that share a central corner. Each room gets its own Apple Music preview, lyric-wave text, falling-word confetti, custom decorations picked from a bundled sticker library, and exactly one clickable hero item that opens a handwritten memory card. Designed for anniversaries, partners, very-close-friends, mother's day gifts, love-letters-as-H5 — anywhere a shared period or a single evening splits naturally into four emotional beats.

**The four scenes can be re-themed per gift** (library / supermarket / park / studio / boba-shop / wherever fits the relationship), as long as each feels like a small enclosed space. The scene IDs (`kitchen`/`rooftop`/`karaoke`/`couch`) stay as stable slot keys; only the visual and textual content changes per gift.

Canonical authored HTML: `{baseDir}/assets/templates/paper-house/template-source/night-four-the-turn.html`.

Production + content spec (8 production rules, content organization principles, asset manifest, per-gift checklist, failure modes): `{baseDir}/assets/templates/paper-house/SPEC.md`. **Read this end-to-end before attempting to produce a paper-house gift.** The content principles are what keep the gift specific, factual, matched to the user's language style, and not over-romanticized.

Asset bundle: ~149 MB zip / ~156 MB extracted: stickers, fonts, and reference examples, fetched once via `scripts/fetch-asset-bundle.sh --template paper-house`. The bundle URL and sha256 live in `template.json.asset_bundle`.

Format: `h5`. Status: ready.

### `draw-card` — Retro Gacha Wish Machine

A Three.js retro card-drawing machine with neon lyric rain, a pixel-photo carousel, a wish form, a card-slot animation, a draggable knob, and a saveable generated card. It is designed for playful fan gifts, concert memories, birthdays, idol-postcard surprises, close friends, and light confessions where a lyric, color, joke, or memo can become the card's central object.

Use this template when the gift should feel like drawing a collectible card rather than reading a letter or opening an archive. The key production rule is specificity: choose one card thesis, keep lyrics short, make photos crop-safe for pixelation and overlays, select stickers that support the card style, and write visible copy in the user's habitual language with the recipient.

Canonical authored HTML: `{baseDir}/assets/templates/draw-card/template-source/retro-gacha-card.html`.

Production + content spec: `{baseDir}/assets/templates/draw-card/SPEC.md`. **Read this before producing a draw-card gift.** It contains the card-thesis rules, lyric limits, sticker-selection rules, and the language rule.

Preview: `{baseDir}/assets/templates/draw-card/preview.jpg`.

Asset bundle: ~24 MB zip / ~31 MB extracted with card photos, carousel photos, stickers, lyrics, and reference assets, fetched once via `scripts/fetch-asset-bundle.sh --template draw-card`. The bundle URL and sha256 live in `template.json.asset_bundle`.

Format: `h5`. Status: ready.

### `bouquet` — Cyber Trophy Bouquet

给妈妈做一张赛博奖杯花束插画，每一朵花都藏着一个你们的故事。适合生日、母亲节、感谢、朋友安慰、纪念日。

Users can choose built-in flowers/gems or ask for new florals when image generation is available. The gift is still evidence-based: paper-card text should quote or closely echo user-provided screenshots, notes, or relationship details.

Canonical authored HTML: `{baseDir}/assets/templates/bouquet/template-source/mothers-day-blue-bouquet.html`.

Production + content spec: `{baseDir}/assets/templates/bouquet/SPEC.md`.

Preview: `{baseDir}/assets/templates/bouquet/preview.jpg`.

Asset bundle: ~97 MB zip with flowers, greenery, gems, fonts, and references, fetched once via `scripts/fetch-asset-bundle.sh --template bouquet`. The bundle URL and sha256 live in `template.json.asset_bundle`.

Format: `h5`. Status: ready.

### `empty-boxes` — Tin-Case Memory Loop

A Three.js loop of collectible containers that become handmade memory collages. Featured boxes can be a three-layer refrigerator, shopping basket, library cardboard box, tin case, or another container whose physical shape frames the memory. Each box can hold generated photos, cutout figures, sticker clusters, tape, labels, number beads, receipts, and handwritten notes.

Use this template when the relationship material contains concrete everyday objects: snacks, cold drinks, grocery trips, apology notes, book slips, ticket stubs, small trips, inside-joke objects, or repeated phrases. The key production rule is physical fit: a refrigerator should use shelf-height photos and food/magnet clusters; a shopping basket should use supermarket/snack stickers and a person leaning on or holding the basket; sticker groups must stay inside the container and form readable motifs rather than scattered decoration.

Canonical authored HTML: `{baseDir}/assets/templates/empty-boxes/template-source/tincase-box-loop.html`.

Production + content spec: `{baseDir}/assets/templates/empty-boxes/SPEC.md`. **Read this before producing an empty-boxes gift.** It contains the box-fit rules, sticker-cluster rules, and the language rule: final gift text follows the user's habitual language with the recipient.

Preview: `{baseDir}/assets/templates/empty-boxes/preview.jpg`.

Asset bundle: ~113 MB zip with boxes, stickers, fonts, reference figures, and example generated photos, fetched once via `scripts/fetch-asset-bundle.sh --template empty-boxes`. The bundle URL and sha256 live in `template.json.asset_bundle`.

Format: `h5`. Status: ready.

### `folder` — Layered Memory Archive

An interactive archive of four file folders. Each folder keeps a physically believable back cover, front cover, and smoothly connected tab, then layers prepared base papers, tapes, varied photo formats, stickers, captions, and one grounded story note. The lead folder opens into a larger spread with a Three.js folder-opening animation.

Use this template when the relationship material naturally forms chapters: a shared errand, a quiet ritual, a saved quote, a recurring place, a half-finished plan, or a small future promise. The key production rule is physical folder logic: the tab must remain connected to the shell; paper, tape, stickers, and photos should feel held by the folder; photo formats should vary across strips, grids, polaroids, framed photos, and small bordered photos; visible gift copy must use the user's habitual language with the recipient.

Canonical authored HTML: `{baseDir}/assets/templates/folder/template-source/520-folder-gift.html`.

Production + content spec: `{baseDir}/assets/templates/folder/SPEC.md`. **Read this before producing a folder gift.** It contains the folder-shell rules, paper/tape usage rules, sticker-cluster rules, and the language rule.

Preview: `{baseDir}/assets/templates/folder/preview.jpg`.

Asset bundle: ~139 MB extracted with generated examples, vendor JS, stickers, papers, tapes, frames, and fonts, fetched once via `scripts/fetch-asset-bundle.sh --template folder`. The bundle URL and sha256 live in `template.json.asset_bundle`.

Format: `h5`. Status: ready.

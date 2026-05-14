# folder — Template Spec

This document is the source of truth for producing a `folder` gift. The design principle behind every rule: **the archive is physical before it is decorative.**

## 0. What This Template Is

`folder` is an interactive H5 archive. The first view shows a stack of file folders with visible back covers, front covers, connected tabs, and paper/photo layers. The lead folder opens into a larger spread containing:

- prepared paper bases, notes, cards, clipped papers, tapes, and torn paper scraps
- generated or processed photos in several formats: vertical film strip, four-grid, polaroid, framed photo, bordered mini photo, and receipt-like photo
- sticker clusters from decorations, study utilities, frames, and electronic devices
- folder tabs, captions, archive labels, and one short story body
- a Three.js folder-opening animation backed by the bundled vendor runtime

The canonical output is `template-source/520-folder-gift.html`. The builder reads `filled-slots.json`, injects `window.FOLDER_GIFT_CONFIG`, inlines available local assets, and writes a separate gift `index.html`.

## 1. Ready Scope

The ready version supports:

- using the bundled canonical folder shell, papers, stickers, fonts, vendor JS, and example generated photos
- overriding archive title lines, folder tabs, opened-folder title/meta/captions/story text
- replacing default photos, paper bases, tapes, and stickers through selector-based image replacements
- editing thumbnail folder layout, opened-folder layout, and closed-preview layout
- building a standalone `index.html` without modifying the canonical HTML

It does not include an automatic semantic layout solver. The agent is responsible for choosing good assets, writing grounded copy, keeping each layer within physical bounds, and verifying the composition.

## 2. The 8 Production Rules

### Rule 1 — Preserve the file-folder body

Every folder must read as a real folder:

- a broad body with common file-folder proportions
- a visible back cover and front cover
- a tab that is smoothly connected to the body, not pasted on as a separate badge
- enough front-cover surface to feel like the folder could hold papers

Do not flatten the shell into a rectangle. Do not detach the tab. Do not hide the front/back cover relationship under decorative assets.

### Rule 2 — Each folder needs one larger theme

Each folder is a chapter with evidence. Good themes:

- "the supermarket errand where one snack became a shorthand"
- "the half-earphone ritual"
- "the night-message archive"
- "future plans as saved papers"

Weak themes:

- "our memories"
- "cute moments"
- "love"
- "birthday vibes"

Use the user's material to select a memory anchor: a quote, nickname, date, place, food, object, song, screenshot line, or repeated habit. If the material is thin, make fewer folders and make the notes smaller.

### Rule 3 — Vary photo formats with intention

The template is strongest when the archive uses mixed photo forms:

- vertical three-strip for small sequence memories
- four-grid for a chapter with several objects or moments
- polaroid for a hero memory
- framed photo for a calmer record
- bordered mini photo for a tucked-away detail
- receipt-like photo for an errand, shop, desk, or paper-record chapter

Do not fill every folder with the same polaroid. Each photo format should match the chapter's physical logic and emotional weight.

### Rule 4 — Use the bundled base papers and tapes

Prefer assets from `base/stickers/base/` and `base/stickers/tapes_papers/` for:

- writing surfaces
- photo backgrounds
- torn-note layers
- tape strips holding a photo
- grid/lined record paper
- depth behind captions or story copy

Do not redraw all papers from scratch in SVG when a prepared material asset already exists. The point is to make the archive feel handmade and layered, not clean and synthetic.

### Rule 5 — Sticker groups must stay bounded and meaningful

Stickers should stay inside the folder shell or the opened spread unless they are intentionally taped to the outside cover.

Cluster stickers into 1-3 semantic groups:

- a receipt corner with a clip and paper scrap
- two tapes holding a photo edge
- a small device/object cluster near a quote
- a desk-note stack
- a charm or label group that marks the chapter

Avoid isolated, evenly distributed stickers. A good folder has paper gravity; a bad folder looks sprinkled.

### Rule 6 — Frames and paper containers cannot be empty

Any asset that implies an inner surface must contain something:

- frames
- polaroids
- screens
- note cards
- grid papers
- clipboard surfaces
- folder windows

Pair these with a photo, caption, quote, or paper layer. Empty containers make the gift look unfinished.

### Rule 7 — Gift-facing text follows the user's language

Technical documentation is English, but final gift copy is not. Visible text must use the language, writing system, nickname, and warmth level the user naturally uses with the recipient.

Rules:

- Use the user's address form: nickname, "mom", "宝", "小A", "Ren", etc.
- Echo exact short phrases from the user's material when they carry emotional value.
- Keep the text specific. "You guessed the QQ candy before I said it" is better than "we have tacit understanding."
- Do not over-romanticize a casual friendship or over-casualize a serious anniversary/apology.

### Rule 8 — Verify the H5 and keep the source immutable

Before delivery:

- build into a separate gift folder
- confirm `template-source/520-folder-gift.html` was not modified by the build
- open the generated `index.html` with a local server or browser
- confirm the folder stack renders, the lead folder opens, the spread animation appears, and no major image is blank
- inspect mobile width for tab/caption overlap
- inspect console output for missing local assets

The builder writes only the requested output file and `folder-work/runtime_config.json`. The canonical source stays read-only for gift production.

## 3. Slot Mapping Contract

### `recipient_material`

Use this to extract the recipient, relationship, occasion, language habit, concrete details, quotes, photos, and available source images.

### `folder_story_plan`

Produce 3-6 folder plans. Each plan must include:

- `folder_id`
- `chapter_theme`
- `memory_anchor`
- `quoted_or_echoed_detail`
- `visual_motif`
- `tab_title`
- `tab_subtitle`

Do this before choosing photos or stickers. The story plan prevents the archive from becoming generic scrapbook decoration.

### `folder_physical_contract`

Preserve the canonical folder shell: back cover, front cover, lip, connected tab, side-specific tab placement, and open-spread geometry. If layout is edited, papers and stickers may move, but the shell must keep file-folder proportions.

### `folder_photo_generation`

Generate or process photos for each folder. Prompts should include:

- identity references when available
- exact photo format target
- scene/backdrop
- moment/gesture
- crop safety
- what must remain uncovered by tape/stickers
- things to avoid: readable fake text, watermark, extra people, distorted hands, empty faces

Use at least two different photo formats across the archive. The opened folder should have a hero photo and supporting smaller photos.

### `folder_base_and_paper_picks`

Pick paper and tape assets from `base/stickers/base/` and `base/stickers/tapes_papers/`. These assets are the preferred surfaces for text and photo layering. Use them before drawing replacement papers in CSS/SVG.

### `folder_element_picks`

Pick semantically related stickers from decorations, study utilities, frames, and electronic devices. Keep them grouped and physically attached to the paper/photo structure.

### `folder_copy`

Maps to `window.FOLDER_GIFT_CONFIG.archive`, `tabs`, and `openedFolder`.

Example:

```json
{
  "folder_copy": {
    "archive": {
      "titleLines": ["FILED UNDER: US", "05/20/2026", "LOCATION: SHANGHAI"],
      "note": "我把那些很小、但一想起来就会发光的瞬间，夹进了四个文件夹里。"
    },
    "tabs": [
      {"row": "row1", "title": "01 默契", "subtitle": "一整间超市都变成答案"}
    ],
    "openedFolder": {
      "title": "CHAPTER 01",
      "meta": "520 / SHANGHAI",
      "storyHeading": "关于默契这件小事",
      "storyBodyHtml": "你问我猜猜最想买什么，我脱口而出的那一秒，<mark>旺仔 QQ 糖</mark>就变成了我们的小暗号。"
    }
  }
}
```

### `folder_runtime_overrides`

Use selector-based image replacements for photos, papers, and stickers:

```json
{
  "folder_images": {
    ".row1 .photo-main": "folder-work/assets/generated/row1/hero.jpg",
    ".open-quad .quad-grid img:nth-child(2)": "folder-work/assets/generated/row1/aisle.jpg",
    "[data-open-layout='torn_quote_receipt']": "folder-work/stickers/row1/papers/receipt.png"
  },
  "folder_runtime_overrides": {
    "openLayoutConfig": {
      "main_story_paper": {"x": "13%", "y": "61%", "w": "73%"}
    }
  }
}
```

Use layout overrides only when needed. After every override, check rotated bounds and mobile layout.

## 4. Runtime Builder Contract

Command:

```bash
python3 assets/templates/folder/template-source/build.py \
  --slots ./gifts/<date>-<recipient>/folder-work/filled-slots.json \
  --workdir ./gifts/<date>-<recipient>/folder-work \
  --out ./gifts/<date>-<recipient>/index.html
```

The builder:

1. reads `filled-slots.json`
2. normalizes archive copy, tabs, opened-folder copy, selector image replacements, selector text replacements, and layout overrides
3. inlines assets from the gift workdir, fetched `base/`, or `template-source/`
4. injects `window.FOLDER_GIFT_CONFIG`
5. writes `folder-work/runtime_config.json`
6. writes only the requested output HTML

Supported asset path prefixes:

- `folder-work/assets/generated/...`
- `folder-work/stickers/...`
- `assets/...`
- `stickers/...`
- `fonts/...`

Use `folder-work/...` for per-gift generated assets so the final gift folder remains tidy.

## 5. Pre-Delivery Checklist

- [ ] Asset bundle fetched with `scripts/fetch-asset-bundle.sh --template folder`
- [ ] `folder_story_plan` has 3-6 concrete chapter plans
- [ ] Folder shell still has back cover, front cover, and connected tab
- [ ] Photo formats vary across the archive
- [ ] Paper/tape/base assets are used for surfaces and depth
- [ ] Sticker clusters stay bounded and grouped
- [ ] Visible gift copy uses the user's habitual language
- [ ] Builder output is a separate `index.html`
- [ ] Browser/mobile verification completed or the blocking reason is reported

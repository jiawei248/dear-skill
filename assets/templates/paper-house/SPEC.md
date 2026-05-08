# paper-house — Template Spec

This document is the source-of-truth for how an agent produces a `paper-house` gift. Read it end-to-end before running the build. The design principle behind every rule: **preserve the template's visual identity; personalize the content on top.**

---

## 0. What This Template Is

A WebGL scroll-through diorama of **four small rooms that share a central corner**. The whole scene renders in Three.js inside a single HTML file. Each room has:

- An eyebrow date/kicker, a title, and a narrator-voice `note`
- A 30-second Apple Music preview that loops inside that room
- Two long undulating "wave" sentences of lyric-prose at the top of the room
- ~22-28 short phrases that fall like confetti from the wave band
- Flat wall & floor textures clothing the left wall, right wall, and floor
- A figure sprite (1 or 2) showing the protagonists inside the room
- 5-7 decoration stickers placed in 3D coordinates inside the quadrant
- Exactly ONE clickable hero sticker that opens a handwritten memory card

Four hero cards unlock across the four rooms. Each card is a warm hand-made memory note written to the recipient, wrapped in a generated photo-collage of the hero object with the protagonists.

The canonical output is `template-source/night-four-the-turn.html`. Open it in a browser when you want to see what "good" looks like.

---

## 1. The 8 Production Rules

### Rule 1 — Visual identity is fixed; content is personal

On every gift, these are the same:

- Room geometry, camera paths, snap angles
- Wavy lyric layout logic, falling-word particle system
- Font stack, card layout families (`layout-note` / `layout-split` / `layout-diagonal` / `layout-triangle`)
- Background particle sky (warm drifting starfield)
- Interaction model (click a hero sticker → card opens)
- The existence of exactly 4 rooms that share 1 corner

On every gift, these are **re-made from scratch for the recipient**:

- Wall textures (2 per room), floor texture (1 per room) — AI-generated per gift
- Decoration stickers (5-7 per room) — chosen from the bundled library
- Character figure art (1-2 per room) — AI-generated or processed from user photos
- Song per room — looked up via iTunes Search API
- Two lyric-prose sentences per room — AI-composed using user memories + song phrase quote
- Falling words per room — AI-derived from user memories
- Hero sticker pick — one per room, chosen to anchor a real memory
- Story-card images (1 per room) — AI-generated identity-preserving composites
- Memory card text, title, kicker, paper color, accent color, decal picks

> If the user's intake material is thin, the gift should STILL personalize everything above. Thin material means smaller, more specific anchors — not generic filler. See `references/gifting-ethics.md` § "What to do with sparse material".

### Rule 2 — Physical correctness of AI-generated images

Walls and floor:
- A wall texture shows ONLY what is painted-or-hung on that wall surface. **No receding perspective into a deep room.** The 3D engine already supplies perspective; the texture must be flat content.
- 3D detail painted onto the wall — a window frame with carved depth, a picture in a frame, a hanging lamp, a clock, a wall shelf — is welcome. What's not welcome: "a room that recedes into the distance."
- Left-wall and right-wall of one room MUST read as the same room: identical lighting direction, identical palette, identical era, identical material style. Generate them in one consistent-group pass.
- Floor is viewed top-down; it usually tiles or reads as a continuous ground plane.

Character figures (when AI-generated to supplement or replace user photos):
- If the user gave reference photo(s), the generated figure MUST preserve recognizable identity: face structure, hair, skin tone, clothing style. Not "a person" — "this person".
- Across 4 rooms the protagonist(s) must read as the SAME people: matching body proportions, consistent clothing palette, continuous wardrobe.
- When adding user photos directly (not generated), run them through `scripts/stylize-character.sh` (cutout + white outline, keep only the core person).

Story cards (the images inside memory popups):
- The hero object must be rendered correctly with attachments. **Common physics errors to avoid**:
  - A fridge door floating without hinge contact with the fridge body.
  - A chess board with missing grid rows or non-square cells.
  - A suitcase with wheels on the wrong side or missing a handle.
  - A photo frame whose inner content is empty or shows only the cardboard back.
- The protagonist(s) must be visible, recognizably the same identity as in the room figure, doing a specific micro-activity with the hero object.
- Palette and lighting must match the room's color palette (see `ROOMS[scene].palette` in the canonical HTML).
- Leave ~25% clean blank space in a predictable region (right edge, lower right, etc.) for the handwritten Chinese text overlay that the HTML layer adds.

### Rule 3 — Lyric layout aesthetics

The two long sentence lines and the falling-word confetti are the most visible typography in the whole gift. They must feel handwritten-on-a-wave, never typeset-on-a-grid.

Font and size:
- Both sentence lines and all falling words use the **same font family and same base size**.
- Glow intensity (text-shadow blur + alpha) is identical across the sentence and the falling words. No exception.

Baseline undulation:
- Each sentence is laid out along a gentle wave. The MIDDLE of the sentence (near the center of the room-facing banner) should be **closer to horizontal** — subtler rise/fall.
- The LEFT and RIGHT EDGES of the sentence should have more pronounced undulation.
- Keep the maximum vertical deviation bounded — this is a shallow wave, not a sine curve at amplitude 1.

Horizontal layout:
- Character horizontal positions must be slightly varied (jittered by a few pixels each). Never evenly spaced.
- Left-right symmetry is NOT required — the line should feel layered and asymmetric, not centered like a banner.

Falling words (the confetti):
- Each word is a **complete meaningful short phrase**, 2-6 CJK characters typically (up to ~10). Never a broken chunk of a longer thought ("低头切菜" is good; "切菜的时" is forbidden).
- Roughly 60% of the words must be concrete specifics drawn from the user's memories ("番茄香气", "你回头", "递过碗"). Roughly 40% can be general mood tokens ("很轻很久", "再靠近一点").
- Rotation per word: **random angle in [-20°, +20°]**. Never 0°. Never beyond ±20°. Rotation is per-word and may be regenerated on reload.
- Drift speed/direction: use the canonical HTML's existing physics. Do not modify.

### Rule 4 — Scene consistency and character handling

Each of the four rooms must feel like **a single cohesive world**: wall, floor, sticker pack, figure, song, lyrics, falling words — all tuned to the same palette and same emotional temperature. A room that mixes a library-style wall with a nightclub-style floor fails this rule.

The four rooms DO NOT have to be actual home rooms. Any four "small-room-like" spaces in the real world are valid:
- Library nook / bookshop aisle
- Supermarket produce section / convenience store
- Park bench area / rooftop garden
- Bus seat / subway car corner
- Café window seat / boba-shop
- Studio / dance classroom / art room
- Car interior / boat cabin

Constraint: the scene must feel **enclosed enough to read as a small space**. Open landscapes (a mountain vista, a beach) don't work — they break the diorama idea.

Picking the 4 scenes: if the user's intake material suggests four different places that were meaningful in the relationship, map each scene onto one of those places. The original scene IDs (`kitchen`/`rooftop`/`karaoke`/`couch`) stay fixed because they are referenced throughout the HTML — only the visual theming changes. Think of them as stable slot keys, not content.

Per-room figure rules:
- 1 or 2 figures per room. The canonical rooftop has 2; the others have 1. You MAY adjust to 1-2 based on the room's emotional beat.
- **Cutout + white outline** for all direct user photos (`scripts/stylize-character.sh`). Keep only the core person; trim aggressive backgrounds, clothing that bleeds into environment, etc.
- Some foreground decoration stickers may intentionally **occlude** parts of the figure — this is the correct depth trick and makes the diorama feel layered.
- If a chosen sticker is a photo frame, picture frame, calendar with a photo window, a polaroid, a TV screen, or any container meant to hold content: you MUST add an inner-content sticker on top of it. Empty frames are forbidden.

### Rule 5 — The four rooms' physical geometry

The four rooms are arranged in a 3D cross sharing the origin corner:
- `WALL_LEN = 2.5` — length of each radial wall from origin to outer edge
- `WALL_H = 2.4` — wall height
- `WALL_THK = 0.04` — wall thickness
- Room centers: kitchen `(-3.55, 1.35, 0)`, rooftop `(3.55, 1.35, 0)`, karaoke `(-3.55, -1.45, 0)`, couch `(3.55, -1.45, 0)`
- Each room's INNER corner is the same point. Adjacent rooms share their common wall.

**Do not alter any of these values.** The camera logic, snap angles, sticker coordinate system, lyric layout, particle system all assume this geometry. Any change cascades unpredictably.

### Rule 6 — Songs and lyric composition (copyright-safe)

Per-room song selection:
- Input to the AI: scene mood + user memories + (optional) user-specified song for this scene. If the user supplied a specific song, use it. Otherwise AI picks based on emotional match.
- Resolution: query iTunes Search API: `https://itunes.apple.com/search?term=<title>+<artist>&entity=song&limit=5`. No auth key required.
- Embed into HTML: the song's `trackName`, `artistName`, and `previewUrl` (the 30-second m4a) — exactly as the canonical `ROOMS[].song` object.

Copyright safety:
- Only the Apple-hosted 30-second preview URL is embedded. Do NOT download-and-rehost that audio.
- Lyrics written into the HTML are NOT the song's original lyrics. They are the user's own narrator-voice reflections composed by the AI.
- A single short phrase (**up to ~12 CJK chars**) MAY be lightly quoted from the song in the form: `[Artist]《[Song Title]》里那句「quoted phrase」`. This is a fair-use-sized quotation; the rest of the sentence (~95%) must be original text grounded in the user's memories.
- NEVER generate full verses, full choruses, or paraphrase multiple consecutive lines of any copyrighted song. NEVER output anything that reads as a translation or close paraphrase of a copyrighted lyric block.
- The two sentences per scene should each be ~80-140 CJK chars (proportional in other languages). They should feel like the user speaking about the moment, not like song lyrics reprinted.

### Rule 7 — Background particles

The canonical HTML has four layered starfield systems drifting slowly behind the rooms:

| Layer | Count | Radius | Size | Opacity | Color | y-bias |
|---|---|---|---|---|---|---|
| 1 | 1300 | 16-30 | 0.9 | 0.66 | `0xfff7dd` | 0.1 |
| 2 | 920 | 10-19 | 0.72 | 0.56 | `0xffd39a` | -0.15 |
| 3 | 680 | 12-24 | 1.05 | 0.34 | `0xffb47e` | -0.8 |
| 4 | 140 (clustered) | — | 0.65 | 0.10 | `0xffe1a8` | — |

These are clearly visible, warm, and well-distributed — they carry atmosphere between rooms during camera snaps. **Do not reduce density or dim them.** They are part of the template's visual identity.

### Rule 8 — Local dependencies the agent installs on demand

The build pipeline relies on:

- **Python 3.9+** (macOS default works)
- A local virtualenv: `python3 -m venv .venv && source .venv/bin/activate`
- pip packages:
  - Character cutout: `rembg onnxruntime Pillow opencv-python numpy`
  - Story-card generation (via litellm): `requests urllib3 Pillow`
  - Image processing (white outline, crop): `Pillow`
- rembg model: `isnet-general-use` (~170MB). rembg auto-downloads this to `~/.u2net` on first run.

The agent should install these ON DEMAND when a step that needs them is about to run — do not install upfront. For example:
- Only download rembg when the user actually provides photos needing cutout.
- Only install litellm/requests stack when generating story cards.

Tell the user what's about to be installed (one brief line) before running pip, so they can interrupt if they'd rather not touch their local env. Prefer running inside a fresh `.venv` at `./gifts/<date>-<recipient-slug>/.venv/` scoped to this one gift so nothing pollutes the user's globals.

---

## 2. Asset Manifest

What exists where, and what is new per gift.

### Installed with the skill (in `template-source/`)

These files ship with the skill and are never modified per gift. They are the authored template.

| Path | Role |
|---|---|
| `template-source/night-four-the-turn.html` | Canonical golden output (23 MB, all assets inlined). Use as reference for layout / palette / lyric wave / particle settings. |
| `template-source/build.py` | Rebuilds the HTML from an authored source HTML + asset directory. Modify data, not this file's logic. |
| `template-source/patch_*.py` | Historical patches showing HOW visual decisions were made (depth layers, earphone lines, hide-inactive-rooms, etc.). Read for understanding; re-running them is optional. |
| `template-source/scripts/batch_cutout_new_stickers.py` | Pipeline for turning raw assets into sticker PNGs (rembg + alpha clean + trim). Use when adding NEW stickers not in the bundle. |
| `template-source/scripts/generate_story_cards_litellm.py` | Per-gift story card image generator. Reads `story_cards/prompts/story_card_image_prompts.json`, calls an image model via litellm, outputs 4 cards. |
| `template-source/scripts/polish_generated_story_cards.py` | Post-process pass over the 4 cards (grading, grain, edges). |
| `template-source/scripts/build_story_card_draft_assets.py` | Builds placeholder draft cards if generation is deferred. |
| `template-source/story_cards/prompts/story_card_image_prompts.json` | The per-room prompt structure for story-card generation. Copy and rewrite per gift — do not edit in place. |

### Downloaded from OSS on first use (→ `base/`)

Fetched once via `scripts/fetch-asset-bundle.sh --template paper-house`. Cached forever after.

| Path | Contents |
|---|---|
| `base/stickers/decorations/*.png` | ~165 decoration stickers (hearts, notes, ribbons, tags, tape, stars, etc.) |
| `base/stickers/food/*.png` | ~29 food stickers (dishes, cakes, drinks, fruit) |
| `base/stickers/furnitures/*.png` | ~76 furniture stickers (fridges, sofas, lamps, desks, etc.) |
| `base/stickers/household_goods/*.png` | ~74 household-goods stickers (mugs, clocks, pillows, cameras, etc.) |
| `base/stickers/music_player/*.png` | ~14 music-player stickers (microphone, jukebox, boombox, vinyl) |
| `base/stickers/pets/*.png` | ~24 pet stickers (cats, dogs, small animals) |
| `base/stickers/plants/*.png` | ~14 plant stickers (potted plants, flowers, branches) |
| `base/stickers/transportation/*.png` | ~5 transportation stickers (suitcases, bikes, trains) |
| `base/fonts/*.ttf` | 3 handwritten CJK fonts: 荷塘月色手写体, 我爱万伟伟手写体, 张穸洛浮生楷体 |
| `base/reference/scene_*.{jpg,png}` | Example scene backgrounds (mood & palette reference) |
| `base/reference/{room}_{left,right,floor}.jpg` | Example wall/floor textures (physical-constraint reference for AI-generated walls) |
| `base/reference/{room}/{1..6}.png, player.png` | Example room sprite sets (the original characters placed in the canonical HTML) |
| `base/reference/ref_boy.jpg, ref_girl.jpg` | Example character-identity references |
| `base/reference/story_cards/generated/*.png` | Example story-card images |

Total bundle size: ~170 MB.

### Generated per gift (in the working gift folder)

Produced fresh every time. Written to `./gifts/<YYYY-MM-DD>-<recipient-slug>/`.

| Path | How produced |
|---|---|
| `{scene_id}_left.jpg`, `{scene_id}_right.jpg`, `{scene_id}_floor.jpg` | Image generation, per Rule 2 physical rules |
| `scene_{scene_id}.png` (1 or 2 per room) | Image generation from user-photo identity references |
| `{scene_id}/1..6.png`, `{scene_id}/player.png` | Picked from `base/stickers/*` based on user-memory match; renamed + optionally cutout-polished |
| `story_cards/generated/{scene_id}-{item}.png` | Image generation via `template-source/scripts/generate_story_cards_litellm.py` with per-gift prompts |
| `story_cards/prompts/story_card_image_prompts.json` | Copy of the template's prompts JSON with text replaced per gift |
| `index.html` | Final output, single-file, from `template-source/build.py` |

---

## 3. Per-Gift Production Checklist

When the user picks `paper-house`, walk through these steps in order. Slot Matching (Stage 0.5 in the main flow) covers steps 2-7.

**1. Ensure `base/` is present.** If missing, run:
```
scripts/fetch-asset-bundle.sh --template paper-house
```

**2. Decide scene themes** (Rule 4). For each of the 4 scene IDs, pick a re-themed scene if the user's context strongly suggests different places; otherwise keep the original kitchen/rooftop/karaoke/couch. Write the `theme`, `eyebrow`, `note`, and `palette` for each room. Palettes should preserve the contrast structure of the canonical ROOMS[].palette (bg / wall2 / floor / ink / accent / glow / figureA / figureB).

**3. Resolve 4 songs** (Rule 6). For each scene, choose a song (user-provided or AI-picked), query iTunes Search API, grab `previewUrl`, `trackName`, `artistName`.

**4. Compose lyrics + falling words** (Rules 3, 6). Per scene: 2 narrator-voice sentences (~80-140 CJK chars each), each containing at most one short (~12 char) song-quote, each grounded in a specific user memory. Then 22-28 falling-word phrases, 60% specific and 40% mood, each a complete short phrase.

**5. Pick hero items + decoration stickers** (Rule 4). Per scene: exactly 1 hero sticker (kitchen_4 fridge, rooftop_1 suitcase, karaoke_3 camera, couch_6 chess are the canonical slots — pick different sticker numbers or different categories if user memories clearly point elsewhere). Then 5-7 supporting decoration stickers, occlusion-friendly, picked from appropriate categories based on the room's theme and user context.

**6. Generate walls + floor** (Rule 2). For each scene, generate left wall, right wall, floor as ONE consistency group. Follow the style anchor from `base/reference/scene_{scene_id}.jpg` for palette and mood. Enforce the flat-wall-content rule.

**7. Generate figure sprites + story cards** (Rules 2, 4). 
- For figure sprites: either (a) use a user photo run through `scripts/stylize-character.sh` or (b) generate an AI composition preserving the user-photo identity.
- For story cards: copy `template-source/story_cards/prompts/story_card_image_prompts.json`, rewrite each card's prompt with the per-gift hero object, room palette, protagonist identity, and 2-3 supporting sticker references, then run the generation pipeline.

**8. Compose card text + decals** (Rule 1, see also `references/gifting-ethics.md`). Per card: title, kicker, paper/accent hex colors matching the room palette, 3-4 overlay decals (stickers with x/y/w/r positioning), and a handwritten memory text of 60-110 CJK chars grounded in a specific detail from the user's intake. Pick ONE layout per card from the four options (note / split / diagonal / triangle).

**9. Assemble `filled-slots.json` + run `build.py`**. The build script reads filled-slots.json, assembles the final HTML with all assets base64-inlined, and writes it to the gift folder.

**10. Deliver.** Either open locally or push via `scripts/deliver-gift.sh --domain <surge-subdomain>`.

---

## 4. Dependencies — Installation on Demand

The agent should NOT pre-install anything. When a step needs a dependency:

1. Tell the user in one brief line: `需要安装一下 rembg 做人像抠图 (~180MB with model)，装完继续`.
2. Create (or activate) a local venv scoped to this gift: `python3 -m venv ./gifts/<slug>/.venv && source ./gifts/<slug>/.venv/bin/activate`.
3. `pip install <packages>`.
4. Run the step.

Dependency groups:

| When | Install |
|---|---|
| First cutout of a user photo | `rembg onnxruntime Pillow opencv-python numpy` |
| First story-card generation | `requests urllib3 Pillow` |
| White-outline post-process | `Pillow` (usually already present) |

The isnet-general-use rembg model (~170MB) downloads automatically on first call. Tell the user to expect a ~1 min delay the first time.

---

## 5. Failure Modes and Fallbacks

- **No reference photo of the recipient**: generate 4 consistent-but-non-specific figures across all rooms. Document this explicitly to the user in the fill preview.
- **iTunes search fails for a chosen song**: fall back to the user's specified song, or if they specified nothing, AI picks a different song with the same mood and re-queries.
- **Image generation fails mid-flight**: retry once with a slightly relaxed prompt, then fall back to a lightweight composition — never deliver a gift with a missing wall/floor/story-card.
- **Hero sticker user-suggested has no physical fit with the canonical layout slot**: keep the user's sticker choice but re-place it at a reasonable coordinate within the DECOR_LAYOUT schema rather than forcing a bad slot.
- **User's lyric request would require large copyrighted quotation**: respond honestly — offer the same emotional beat written as original text with a ≤12-char quoted phrase, or offer a different song whose already-quotable phrase matches.

---

## 6. What NOT to Do

- Do not modify `template-source/night-four-the-turn.html` or any of the `patch_*.py` files. They are frozen golden references.
- Do not bundle generated user content (photos, memories, names) into the skill — it always stays in the user's gift folder, locally.
- Do not add new sticker categories to the bundled library in a way that isn't versioned via GitHub Release. If you add stickers during a gift run, save them to the user's gift folder, not to the skill install.
- Do not quote more than ~12 chars of any copyrighted song.
- Do not generate walls/floors that depict a 3D receding room.
- Do not generate figures that don't resemble the recipient when a reference photo was provided.
- Do not render empty photo frames / empty content containers.
- Do not promise outputs that rely on models or keys the user hasn't set up. Before generation steps, verify keys and give a clean fallback if missing.

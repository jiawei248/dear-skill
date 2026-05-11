# Stage 3: Visual Strategy


When the chosen format is H5 and the concept involves user interaction (tap, swipe, reveal, unlock sequences), also read `{baseDir}/references/h5-interaction-design.md` for animation and emotion escalation guidelines.

#### Image-Specific Brief Enrichment

If the chosen format is `image`, the synthesis brief should additionally include:

- `scene_description`
- `image_genre`
- `style_hint`
- `aspect_ratio_hint`
- `text_overlay_spec` when text should appear inside the image

Use image output when a single generated frame can carry the whole anchor-plus-return pair.

Before locking `image_genre`, first read `{baseDir}/references/image-genre-chooser.md` and use it to make a fast first-pass genre decision.

The image brief should be concrete about:

- the scene or subject
- the emotional treatment
- the genre choice, such as `meme-sticker`, `mood-photo`, `proxy-character-scene`, `emotion-poster`, `borrowed-media-layout`, or `surreal-film`
- the exact style direction, not just a vague adjective
- whether text belongs inside the image at all

If text is used inside the image, specify:

- the exact wording
- the language, which should match the user's dominant interaction language with the skill
- the placement
- the approximate size
- the font feel or styling direction

Text should feel naturally integrated with the image rather than pasted on top. Avoid layouts that are likely to produce broken text structure, especially for Chinese.

Keep text short whenever possible. Avoid long paragraphs or dense blocks of Chinese text inside generated images unless there is a very strong reason and the layout is simple enough to survive generation.

Default to a mobile-friendly `9:16` aspect ratio unless another composition clearly serves the return better.

### User Portrait Integration

If `user_portrait.available` is true in setup state, the synthesis brief may include the user's appearance description when it materially improves the gift.

Appropriate uses:

- OC-style gifts referencing the user's generated avatar
- mirror, portrait, or self-seeing gifts
- anniversary, onboarding, or milestone gifts where the user's presence is part of the emotional return

Inappropriate uses:

- every single gift, because overuse weakens the effect
- gifts where the user's appearance is irrelevant to the thesis
- dropping the raw selfie into the artifact without creative transformation

When using the portrait in an image or H5 gift, prefer the OC version in `user_portrait.oc_path` when available, or create a new stylized transformation, rather than relying on the raw photo directly.

The stored `user_portrait.description` may be injected into prompts or briefs as character guidance without loading the actual image file every time.

### Character Identity in Generated Images

Do not read or apply stored character/persona context by default. This skill is recipient-centered: the user's material, the recipient relationship, and the current gift thesis should drive the output before any recurring persona files.

Only use stored character identity when the user explicitly asks for a recurring character, the recipient brief names an OC/avatar/persona, or the concept would be impossible to render correctly without a previously established character form.

When stored character identity is explicitly relevant:

1. Read `./user-portrait/` metadata and any OC definitions from the recipient brief or supplied user context first; consult `./setup-state.json` or `./user-taste-profile.json` only when they contain the requested recurring character data.
2. Use the established character forms rather than improvising generic stand-ins:
   - the user's `human_form` and or `nonhuman_form`
   - the skill's `human_form` and or `nonhuman_form`
3. Carry specific character identity details into the image brief and final prompt:
   - species
   - color
   - distinguishing features
   - scene role or relationship role
4. If the narrative implies a specific point of view, make the composition match that POV instead of defaulting to a generic third-person overview.

Examples:

- if the user is established as a golden-colored puppy, do not replace them with an arbitrary dog
- if the skill is established as a red fox, do not silently swap in another animal form
- if the concept is `the user noticing the recipient`, compose from the user's caring perspective or another composition that clearly preserves that relationship, rather than an unrelated overhead scene

Do not generate generic animals or people when established character identities already exist. Users will notice if their character form changes from gift to gift.

### Character Rendering Strategy (Avoiding Uncanny Results)

When the user or agent persona involves a fantastical, humorous, or mixed description, the rendering must capture the SPIRIT — never produce a literal hybrid creature that looks ugly or uncanny.

**Two representation modes:**

**Mode A: Human-figure-based**
Use when the description implies human attractiveness or stature (e.g. "189cm handsome shrimp guy", "tall guy who looks like Takeshi Kaneshiro").
Strategy: human figure as the main body + non-human elements as accessories/motifs.
- "189 handsome shrimp" → tall attractive guy in a shrimp-themed hoodie, NOT a literal shrimp-human hybrid
- "looks like a movie star" → stylized attractive character silhouette, NOT a photorealistic face

**Mode B: Creature-based**
Use when the description IS an animal or cute creature (e.g. "little fox", "round fluffy cat", "soft bunny").
Strategy: cute anthropomorphized creature, maintaining cuteness.
- "little fox" → adorable fox character with expressive eyes
- "round cat" → chibi/SD style cat figure

**Universal rules:**
- Respect the user's configured gender (he/she/they)
- cute > accurate > literal. A cute interpretation that captures the spirit is always better than a faithful but ugly literal rendering.
- If the generated result looks uncanny, ugly, or horrifying → it is WRONG. Regenerate with a softer interpretation.
- When storing character rendering info, include both raw description AND rendering strategy:
  ```json
  {
    "raw": "189cm handsome shrimp",
    "mode": "human-figure-based",
    "rendering_guide": "Tall attractive male figure with shrimp-themed accessories. Never render as literal shrimp-human hybrid.",
    "gender": "male"
  }
  ```

### Gift Complexity Assessment

After the creative concept is locked, assess whether it can be executed in one agent turn or needs multi-step orchestration.

`Light gift`:

- the default for ordinary lightweight gifts
- one image generation call or zero
- simple H5 with code-only rendering or one background image
- no post-processing such as background removal
- no multi-asset assembly that would materially increase execution risk

`Rich gift`:

- needs `2` or more generated image assets
- needs background removal on generated images
- needs a complex H5 with multiple scenes, states, or tightly tuned animation work
- needs both generated assets and refined code, such as a game with custom sprites
- cannot be meaningfully simplified without losing the core appeal of the concept

Use rich gift mode when:

- a manual request explicitly asks for something elaborate
- a milestone, anniversary, or unusually important gift justifies extra effort

Do not use rich gift mode when:

- the concept can be simplified without losing its punch

If rich gift mode is needed, prepare a richer execution brief rather than trying to rush the whole thing inside one fragile turn.

- If the chosen format is non-`h5`, hand the work to a spawned sub-agent or follow-on execution session when that reduces execution risk.
- If the chosen format is `h5`, keep execution in the main session and use the incremental rendering workflow from `stage4-visualization.md` instead of spawning.

### Stage 3: Visual Strategy

Choose the most fitting expressive mode for the already-selected creative concept before generating the final artifact.

If the chosen format is `image` or `text`, the H5-specific mandatory checklist below is not required in full. Instead, use Stage 3 to choose the format-specific rendering direction, then confirm the relevant brief fields in the `Pre-Visualization Check`.

Before choosing a pattern, complete this mandatory checklist:

1. Read `{baseDir}/references/gift-mechanics.md`.
2. Read `{baseDir}/references/pattern-boundaries.md`.
3. Read at least one pattern card from `{baseDir}/references/pattern-cards/` that might fit today's brief.
4. If that pattern card has a corresponding template in `{baseDir}/assets/templates/`, open and read the `index.html`.
5. If that pattern card depends on binary reference images from `{baseDir}/assets/examples/` and they are missing locally, fetch the needed bundle first via `{baseDir}/scripts/fetch-asset-bundle.sh`, then inspect them.

If the chosen format is `h5`, do not proceed to Stage 4 without completing steps `1` through `3`. Steps `4` and `5` are mandatory whenever the relevant assets exist.

If the chosen format is `image` or `text`, still read `{baseDir}/references/gift-mechanics.md` and `{baseDir}/references/pattern-boundaries.md`, but you do not need to force the brief through an H5 pattern card or template unless that reference genuinely helps the chosen concept.

When `./user-taste-profile.json` exists, use it during visual strategy only when the current gift brief makes the user's taste or recurring character context directly relevant:

- read `aesthetics_baseline` to calibrate the visual quality bar when the user asks for their own taste to guide the piece
- read `style_exposure` to avoid visual repetition beyond the short `recent_gifts` window
- read `user_character` and skill character data only when characters appear by explicit request or by concept necessity

Departure check after reading the pattern and any relevant template:

- if the chosen format is `h5`, what is this concept's unique visual metaphor, not the template's metaphor
- if the chosen format is `h5`, what is the center object of this piece, not the template's center object
- if the chosen format is `h5`, if someone who has seen the template heard this plan, would they say "that is basically the same composition"
- if the chosen format is `h5` and the honest answer is yes, rethink before continuing
- if the chosen format is `image`, what single generated frame, genre, and subject treatment will carry the return most clearly

Decide:

- which pattern best fits the brief when the chosen format is `h5`
- which image genre best fits the brief when the chosen format is `image`, after a first-pass check through `{baseDir}/references/image-genre-chooser.md`
- what the planned `output_shape` is, reusing the categories in `{baseDir}/references/editorial-judgment.md` when they fit and defining a new stable high-level label when they do not
- what the planned `visual_style` label is, such as `dark-terminal`, `dark-cinematic`, `light-warm`, `colorful-playful`, `minimal-poster`, `pixel-retro`, `photographic`, or a stable custom label
- whether the piece should be code-first, image-first, or hybrid
- whether the gift should be one screen, a micro interaction, or a short scroll story
- whether the tone should be visually calm, warm, playful, satirical, dreamy, or commemorative
- whether important source quotes or image cues should be made directly visible in the artifact
- whether the chosen pattern should amplify comfort, recognition, humor, release, or delight

### Asset Plan

After choosing the format, pattern or genre, and creative concept, decide what assets this gift needs before rendering begins.

#### For `h5` gifts

Before defaulting to pure code, actively consider whether generated image assets would meaningfully elevate the gift's quality and user delight.

**Default mindset: prefer generated images aggressively.** Most H5 gifts look measurably better with at least one generated image providing atmosphere, scene, or character — combined with code for interaction. Do NOT default to "I'll draw it with code" when the element needs beauty, atmosphere, or organic form.

**The code-vs-image decision is NOT about difficulty — it's about visual quality ceiling:**
- Code ceiling for a cloud: a white ellipse cluster. Looks like a diagram.
- Image ceiling for a cloud: a painterly atmospheric cloud with depth, light, and texture. Looks like art.
- Code ceiling for a room: rectangles with gradients. Looks like a wireframe.
- Image ceiling for a room: a warm space with materials, shadows, and character. Looks like a place.

When in doubt, generate the image. The compositing cost (base64 embed, remove-bg if needed) is small compared to the quality uplift. Use `{baseDir}/scripts/render-image.sh` for generation and `{baseDir}/scripts/remove-bg.sh` when the image needs to be layered on a transparent background over code elements.

Generated images can serve as:
- full-screen background (atmosphere, scene, environment)
- layered backgrounds for crossfade/transition effects (e.g. two scenes that blend as user interacts — control each image's CSS opacity from JavaScript based on slider value, scroll position, or touch)
- character sprites or object assets composited on top
- texture or material references that code alone struggles to produce

`Pure code` is still the right choice when:
- the concept is generative art (particles, math-driven)
- the concept is text-forward (kinetic text, terminal)
- the concept is UI-driven (fake apps, dashboards)
- adding images would not meaningfully improve the result

**Engine expectation for pure-code H5:**
Even when images are not needed, "pure code" does NOT mean "pure CSS." For any H5 gift involving organic motion, particles, physics, atmosphere, or continuous animation, use p5.js or another canvas/WebGL engine. CSS-only H5 is acceptable ONLY for:
- Borrowed-media document simulations (fake reports, tickets, forms) where static/minimal-motion IS the aesthetic
- UI mockups (fake apps, fake OS screens) where the design IS the gift
- Simple card layouts where text precision is the primary value

If you find yourself building an "atmospheric" or "emotional" H5 with only CSS @keyframes and no canvas element — you are building the wrong thing. Use p5.js.

**Typography as craft signal:**
Do not accept default font rendering. Every H5 gift should make an intentional typography choice:
- Load a specific web font via Google Fonts CDN (acceptable per html-spec.md)
- Choose the font to match the emotional register: Space Mono for industrial/tech, serif for literary/poetic, rounded sans-serif for warm/playful
- Set letter-spacing intentionally: loose (1-3px) for calm/spacious, tight (-0.5px) for urgent/dense
- Use at least 3 distinct text size levels: display (title), body, caption/label

`Single background image` is often a good default for:
- atmospheric or scene-based gifts
- any gift where a "place" or "environment" matters
- gifts where emotional tone needs photographic or illustrated warmth that CSS gradients cannot match

`Multiple image assets` for richer experiences:
- crossfade between two scenes (e.g. slider between two moods/worlds — layer as HTML img elements behind a transparent p5.js canvas, control opacity via JS)
- card faces, pages, revealed objects
- before/after, parallel states
- character + environment compositing

**Ask before every H5 gift:** "Would a generated image background or asset meaningfully improve the user's experience? If yes, generate it."

The best H5 gifts combine: generated image quality + code interaction precision. One beautiful scene + one clean interaction layer + one controlled motion system.

#### Background Asset Strategy for H5

H5 gifts default to code-rendered backgrounds (CSS gradients, patterns). But for atmospheric or emotional gifts, a generated background image can dramatically improve visual quality.

Consider generating a background image when:
- the concept has a strong visual metaphor (tree, ocean, sky, room, landscape)
- pure CSS cannot achieve the desired atmosphere (watercolor, painterly, photographic)
- the gift's emotional register is contemplative, poetic, or cinematic (not playful/game-like)

How to generate:
1. Use the image generation pipeline (render-image.sh or direct API call) to generate a background-only image — no text, no UI elements, just the atmosphere or scene
2. Keep the prompt focused on mood and texture, not on specific layout elements
3. Generate at a resolution that works as a full-bleed mobile background (9:16 or 3:4)
4. Base64-encode and embed as a CSS background-image
5. Layer the interactive H5 elements on top with semi-transparent backgrounds so the generated image shows through

This approach combines the visual richness of AI image generation with the text precision and interactivity of H5 code.

**Also consider generating mid-ground component images:**
Beyond full-bleed backgrounds, individual objects and decorative components often benefit from image generation + background removal compositing:
- A lamp, cup, plant, or desk object that appears in the scene → generate as sprite, remove background, layer into H5
- An ornate frame, window, or border that CSS cannot make beautiful → generate, remove-bg, use as positioned layer
- A character or creature that appears in the scene → generate, remove-bg, composite
- A texture or material swatch (wood grain, paper, fabric) → generate a patch, tile or stretch as CSS background-image

The workflow: generate with render-image.sh → remove background with remove-bg.sh if needed → base64 embed into HTML → position with CSS/canvas → add code-driven animation, particles, and interaction on top.

This "image skeleton + code animation" pattern consistently produces the highest quality H5 gifts because each layer does what it does best: images handle beauty, code handles motion.

Do NOT generate backgrounds for:
- game/puzzle gifts (keep clean and digital)
- document/borrowed-media gifts (CSS textures are more authentic)
- gifts where the visual metaphor is abstract or UI-based

#### For `image` gifts

The image is the output.

No separate asset plan is needed.

#### Asset Plan Summary Format

State the plan in one line:

- `assets: none (pure code h5)`
- `assets: 1 background image (airport rain scene)`
- `assets: 3 card face images (parallel universes)`

#### Background Removal

When a generated image needs to be composited onto an H5 scene instead of used as a full-bleed background, it will often need background removal.

Use `{baseDir}/scripts/remove-bg.sh`:

- input: generated PNG or JPG
- output: transparent PNG
- API key source: `tools.remove_bg.api_key` in setup state or `REMOVE_BG_API_KEY` from the environment

State in the asset plan which images need background removal, for example:

- `assets: 1 building sprite (generate + remove bg)`
- `assets: 2 cat sprites (generate + remove bg) + 1 background scene`

Background removal is usually needed when:

- the image will be layered on top of other visuals
- transparency matters for compositing
- the generated image has a visible white or colored background that should disappear

Background removal is usually not needed when:

- the image is used as a full-width or full-bleed background
- the image is sent directly as the final result, such as `image`

Use these references:

- `{baseDir}/references/gift-format-chooser.md`
- `{baseDir}/references/pattern-cards/`
- `{baseDir}/references/pattern-boundaries.md`
- `{baseDir}/references/gift-mechanics.md`
- `{baseDir}/references/editorial-judgment.md`
- `{baseDir}/references/html-spec.md`
- `{baseDir}/references/image-integration.md`
- `{baseDir}/references/image-genre-chooser.md`
- `{baseDir}/references/visual-strategy-contract.json`
- `{baseDir}/assets/templates/`
- `{baseDir}/assets/examples/`

When using those references:

- do not copy a pattern or template literally just because it seems close
- feel free to widen or shift a pattern's apparent use case if the deeper emotional logic still fits
- borrow only part of a template when that is enough
- do not reject a pattern just because it has no template yet
- use screenshots or reference images when they communicate the form better than code would
- combine pattern logic, mechanics, or treatments when a hybrid result fits the brief better
- treat existing examples as strong references that still require editorial judgment
- do not force the brief into a named pattern if a cleaner custom form would be better
- use progressive disclosure rather than scanning the full library in depth at once

After completing the checklist, you may:

- use the pattern you read as-is
- adapt or remix it
- hybridize multiple patterns
- invent a completely new form

Reading the library is mandatory. Following the library literally is not. The goal is informed creativity, not constrained creativity.

### Pre-Visualization Check

Before rendering the final artifact:

- state the creative concept in one sentence
- confirm that the concept sounds like something the user has probably never received before
- if the concept is only `a nice [format] with [content]` and has no real twist, stop and go back to Stage `2.5`
- confirm that you have read `{baseDir}/references/gift-mechanics.md`
- confirm that you have read `{baseDir}/references/pattern-boundaries.md`
- confirm that you have read at least one relevant pattern card
- if the chosen format is `h5` and a relevant template exists, confirm that you have read its actual code
- if the chosen format is `h5`, state in one sentence why the chosen pattern fits the brief
- if the chosen format is `h5`, state the piece's own visual metaphor, center object, and scene in language that is clearly distinct from the template you referenced
- if the chosen format is `h5`, confirm that the planned output has a distinct visual identity from the referenced template. Templates are quality benchmarks and mechanical references, not compositions to reproduce.
- if the chosen format is `h5` and you reused a template engine, explicitly state what is different from the source template in:
  - visual metaphor
  - center object
  - composition
- if the chosen format is `h5` and no template was used, confirm that the plan still departs clearly from the pattern card's default or most obvious example framing
- if the chosen format is `h5`, compare the planned visual sophistication against the templates in `{baseDir}/assets/templates/`
- if the chosen format is `h5` and the planned output would look less polished than the relevant templates, simplify or rethink the concept before proceeding
- state the chosen format, and check whether `3` or more of the last `5` gifts used this same format; if so, explain why this time it is still the right choice
- explain why the chosen format serves the concept better than the nearest alternative format
- state the planned `content_direction`, and if `./gift-history.jsonl` exists, check whether the recent `witness` / `portrait` / `comfort` cluster is overused; if so, explain the deliberate corrective shift or the strong reason not to shift
- state the planned `visual_style`, and check whether it has already appeared more than `2` times in the last `5` gifts
- if the last `2` gifts both used `dark-*` visual styles, explain why this gift should stay dark or choose a lighter or more colorful style instead
- if the chosen format is `image`, confirm the chosen `image_genre`, `scene_description`, `style_hint`, and `aspect_ratio_hint`
- if the chosen format is `image` and text appears inside the image, confirm the exact wording, language, placement, approximate size, and font feel
- if the chosen format is `image`, confirm that any text treatment is likely to render naturally rather than producing broken or chaotic typography
- if the chosen format is `image`, confirm that on-image text is as short as possible, especially for Chinese
- state the asset plan: how many images, if any, need to be generated before rendering, and what each one is for
- if the asset plan includes generated images, confirm that those generated images genuinely improve the concept over pure code, still-only, or native format rendering
- state the gift thesis in one sentence, including both anchor and return
- confirm which one or two synthesis slots are central and which remaining slots are only context
- confirm that the thesis gives the user something they did not already fully have, rather than only replaying the source event
- state the planned `output_shape`, and check whether it is overused in `recent_gifts`
- if the planned `output_shape` is custom, confirm that it names a reusable high-level family rather than a one-off decorative description
- if the planned `output_shape` has already appeared too often recently, choose a more distinct form unless repetition is itself meaningful
- if too many slots are competing for equal attention, simplify before proceeding

If any mandatory Stage 3 checklist step was skipped, stop and go back to Stage 3.


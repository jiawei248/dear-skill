# Stage 4: Visualization & Rendering

Complete instructions for visualization, rendering paths (H5, Image, Text, Text-Play), rich gift execution, on-demand asset generation, companion skills, self-check, and functional self-test. Read this when ready to produce the final artifact.

### Stage 4: Visualization

Turn the chosen format into a polished final gift artifact.

Before rendering characters, read the character profiles from `./user-taste-profile.json` when it exists. Decide human versus non-human form based on the gift's style. Include all fixed features in prompts that render that character. Never put human features onto animal forms.

If the chosen format is `h5`, use this assembly priority order:

1. Existing template visual engine
2. Image-first or hybrid H5 assembly
3. External reference search for missing effects
4. Companion frontend or UI skill guidance

### H5 Technical Quality Floor

The templates in `{baseDir}/assets/templates/` use p5.js + canvas rendering with full particle systems, physics simulation, and frame-by-frame animation loops. This is the technical quality floor.

Before writing H5 code, also read:

- `{baseDir}/references/h5-interaction-design.md` for interaction design, anti-AI-slop visual quality, and mobile rendering best practices

For atmospheric, poetic, or emotion-driven H5 gifts, CSS-only animation is NOT sufficient. Use canvas-based rendering (p5.js preferred) when the concept involves:
- organic motion (growing, flowing, scattering, blooming, floating)
- particles (sparks, leaves, petals, snow, dust, light)
- physics simulation (wind, gravity, spring, collision)
- progressive reveal or transformation of visual elements
- emotional pacing that depends on smooth, continuous animation

CSS-only is acceptable for:
- document/report-style gifts (borrowed-media as H5)
- UI-mockup gifts (fake app, fake website, fake OS screen)
- simple card/reveal gifts with minimal motion
- gifts where text precision is the primary value and motion is secondary

### H5 Craft Quality Checklist (Mandatory Before Delivery)

These five dimensions separate polished H5 gifts from "works but looks AI-generated" output. Check all five before delivery:

**1. Animation smoothness — use lerp, not CSS transitions**
Every interactive or continuous motion must use frame-by-frame `lerp()` smoothing (or equivalent easing in the draw loop), not CSS `transition` or `@keyframes`. Lerp gives physical weight; CSS gives on/off switches. If any moving element snaps instead of gliding, fix it.

**2. Retina clarity — always set pixelDensity(2)**
All p5.js canvases must call `pixelDensity(2)` in `setup()`. Without it, canvas content looks blurry on modern screens. This is a one-line fix with massive visual impact.

**3. Physical feedback on interaction**
Every interactive element (drag, tap, hover, click) must produce proportional, physics-inspired feedback: spring return, elastic bounce, inertia, damping, or resistance. If the user drags something and it teleports to the mouse position with no smoothing, the interaction feels dead. Minimum: `lerp(current, target, 0.1-0.2)` on all interactive position updates.

**4. Color hierarchy depth — minimum 5 stops**
Do not use just "main color + white + one grey." A polished palette needs at minimum:
- deep background
- surface/card background  
- muted label/secondary text
- primary content text
- accent/highlight
Each with intentional contrast ratios. Study the `ticket` template: it has #0a0a0a → #262626 → #7a7a7a → #d0d0d0 → white, each serving a distinct hierarchy role.

**5. Generative motion over preset motion**
Prefer Perlin noise, particle systems, and physics simulation over fixed @keyframes loops. Generative motion is never exactly the same twice — it feels alive. Preset loops feel mechanical after the second viewing. If the gift has ambient background motion (floating elements, gentle drift, flowing particles), it should use `noise()` or randomized physics, not repeating CSS paths.

**6. Detail density — every pixel should feel authored**
A polished H5 has NO empty/lazy areas. Study how the reference templates handle detail:
- `ticket` uses a Perlin noise dot-grid as decorative panel filler — not blank space, not a solid color, but a living texture.
- `vintage-computer` has sticker decorations on the computer case, grainy screen CRT texture, and visible key-gap shadows on the keyboard.
- `beam-light` has hand-drawn holographic wave decorations flanking the title, and the frame has a double-border with different widths.
- `vintage-window` uses dithered/stippled noise in window title bars instead of flat color fills.

When you have a large area that is "just background" — ask if it could have subtle texture, noise, grain, particles, or a secondary decorative system. Empty space is a design choice, but ACCIDENTAL empty space (you just forgot to design that area) is visible to anyone with taste.

### Color Palette Discipline — Avoiding AI-Slop Palettes

Certain color combinations have become strong signals of "AI-generated content" and must be actively avoided:

**Banned default palettes (do NOT use unless the concept explicitly demands it):**
- Gold + dark blue/black ("AI luxury" look)
- Blue-purple neon gradient ("tech demo" look)
- Teal + coral on dark background ("generic startup" look)
- Pure rainbow gradients ("pride flag accidentally" look)
- Flat pastel pink + baby blue ("generic healing" look without specificity)

**Study these palette families from the reference templates:**
- `ticket`: strict grayscale hierarchy — #0a0a0a → #262626 → #7a7a7a → #d0d0d0 → white. Zero color, maximum sophistication.
- `vintage-computer`: warm neutral cream #F0ECE1 as foundation, with tiny pops of color only on functional UI elements (orange, blue icons).
- `beam-light`: deep purple #252240 with holographic teal #56cbd6 accents — atmospheric, not decorative.
- `cloud-text-rain`: layered blues from #021526 to #7ab2d6 — each shade serves a depth layer, not decoration.
- `burn-reveal`: organic fire palette — charcoal to amber to white, following real-world combustion logic.

**Palette construction rule:**
Start from ONE emotional temperature (warm OR cool OR neutral), build 5+ hierarchy stops from that temperature, then add at most ONE accent that contrasts. Never start from "what colors look cool together."

**Quick test:** If you remove the content and just look at the colors, does it look like a polished product or a Midjourney demo? If the latter, redo the palette.

### When To Use Advanced Libraries

Do NOT default to the simplest CSS approach when the concept demands richer effects. Use the right tool:

| Concept / Effect | Library | Why not CSS |
|---|---|---|
| Book flip / page turn / 3D card | **Three.js** or **turn.js** | CSS `transform: rotateY()` gives flat, unconvincing flips. Real page-turn needs mesh deformation, shadows, and perspective depth. |
| Particle rain / snow / confetti (>30 particles) | **p5.js** or canvas | CSS particles are individually animated DOM elements — laggy above 30, no inter-particle physics. |
| Spring / rubber / drag physics | **matter.js** or custom canvas | CSS `transition` has no concept of mass, velocity, or collision. |
| Complex timeline / orchestrated sequences | **GSAP** | CSS `@keyframes` cannot easily chain, reverse, or dynamically control stagger patterns. |
| Fluid / liquid / metaball effects | **p5.js** with shader or SVG filter | CSS cannot do real fluid simulation. |
| 3D scenes / camera rotation / depth | **Three.js** | CSS 3D is faked perspective on flat elements. No real lighting, no real depth buffer. |
| Audio-reactive visuals | **p5.js** + Web Audio API | CSS has no audio input. |
| Handwriting / calligraphy animation | **Canvas 2D** with path interpolation | CSS `stroke-dashoffset` works for simple SVG paths but not for natural handwriting feel. |

**Decision rule:** If you find yourself writing >5 CSS `@keyframes` rules to approximate an effect that a library handles in 20 lines — use the library.

**Quality expectation:** When using Three.js or similar, the result should look like a polished demo on CodePen, not a "hello world rotating cube." Study at least one reference implementation before writing.

Before writing any H5 code, read at least ONE template from `{baseDir}/assets/templates/` that has a similar emotional register. Study its setup/draw loop, text rendering approach, particle implementation, interaction handling, and TEMPLATE_DATA customization pattern.

Templates are references for technical quality, NOT creative constraints. The agent should match their craft level while pursuing any concept — including concepts that have no matching template at all.

### H5 Asset Strategy: Code + Generated Images

`p5.js` or canvas work and AI-generated images are not mutually exclusive. The strongest H5 gifts often combine both:

- let `p5.js` or canvas handle particles, glow, rain, text animation, interaction response, ambient motion, and temporal pacing
- let generated images handle complex scenes, realistic objects, characters, or landscapes that would be costly or weak if drawn entirely with code

Good combination patterns include:

- generate a background scene image, then layer `p5.js` particles and animated text on top
- use `p5.js` for the overall structure, but place a generated image inside a code-drawn frame, window, card, or room
- generate individual asset images such as a lamp, cup, flower, desk object, or character element, then composite them into a `p5.js` canvas or layered H5 scene

Choose the split that produces the highest-quality result for this concept. Do not default to `all code` or `all generated image`. Decide which parts benefit from code precision and which parts benefit from image richness.

### H5 Code-Drawn Element Quality Gate (MANDATORY CHECKLIST)

Before rendering any concrete visual element with `p5.js`, canvas, SVG, or CSS, ask:

`Can code alone make this look good, not just recognizable?`

Code draws well:

- geometric shapes, UI elements, grids, and charts
- particles, glow, rain, snow, stars, dust, and light fields
- text, labels, badges, progress bars, and symbolic indicators
- abstract patterns, gradients, waves, and motion systems
- simple icons and symbols

Code usually draws badly — and SVG/CSS illustrations rarely do better:

- human figures, even when simplified
- animals and creatures
- realistic or emotionally important objects such as food, furniture, vehicles, gifts, or keepsakes
- natural scenes such as trees, flowers, and landscapes
- anything the user is supposed to emotionally connect with as a character, companion, or presence
- atmospheric backgrounds that need depth, texture, or mood (clouds, skies, rooms, forests, cityscapes)
- complex decorative components that need aesthetic appeal (ornate frames, detailed patterns, material textures)
- any visual element where "beauty" or "atmosphere" is doing emotional work

**Do NOT attempt to draw these with SVG, CSS shapes, or p5.js primitives.** A hand-coded SVG cloud looks like a diagram. A generated image cloud looks like a cloud. The gap is not about skill — it is about the medium. When the concept needs atmosphere, texture, or organic beauty, generate an image or search for a reference asset and composite it in. Use `{baseDir}/scripts/render-image.sh` for generation, or `web_search` + `web_fetch` for sourcing Creative Commons / reference assets, then `{baseDir}/scripts/remove-bg.sh` for compositing.

This applies at every scale:
- **Background**: generate a full-bleed atmospheric background instead of CSS gradients when the concept is scenic or emotional
- **Mid-ground objects**: generate sprites for objects that carry meaning (a lamp, a cup, a book, a plant) instead of approximating them with rectangles and circles
- **Decorative components**: when the design needs a frame, border, or ornamental element that CSS cannot make beautiful, generate it as an image

The only exception is when the concept IS about code aesthetics — generative art, terminal screens, data visualization, or UI mockups where the digital-native look is intentional.

#### Mandatory Image Generation Triggers

If the concept contains ANY of the following, you MUST generate an image asset. This is not a suggestion — it is a hard requirement:

| Element in concept | Action |
|---|---|
| A person / character / figure | MUST generate image |
| An animal / creature / pet | MUST generate image |
| A specific real-world object that carries emotional weight (a gift box, a cup of coffee, a guitar, a specific book) | MUST generate image |
| A natural scene (forest, ocean, garden, mountain) as a main visual | MUST generate image |
| Food / drink as a central element | MUST generate image |
| A room / interior / architectural space | MUST generate image |

"I'll just draw it with code" is NOT acceptable for these categories. The only exception is if image generation genuinely fails (API error, quota exhausted) — in which case, redesign the composition to avoid the element entirely rather than drawing a crude approximation.

#### Execution steps when image generation is triggered:

1. Generate that element as an image with `{baseDir}/scripts/render-image.sh` or the image tool.
2. Embed the result into the H5 as an inline base64 `<img>`, CSS background, or loaded image asset.
3. Use code for what code is good at around the image: lighting, particles, framing, interaction response, animation, transitions, and text.

This is not optional. A crude code-drawn blob that merely "stands for" a person, animal, object, or scene is worse than no figure at all.

If a good generated image is not available, redesign the composition instead of forcing a bad drawing.

Fallbacks when image generation is unavailable:

- use an atmospheric silhouette only if it still looks intentional and detailed enough to feel authored
- show the environment, object traces, or lighting without the figure when that lands better
- redesign the scene around text, particles, framing, or point of view rather than a weak concrete drawing

`ellipse() + rect()`-level placeholder figures are not acceptable for emotionally important subjects.

### H5 Incremental Rendering

Do NOT attempt to write the entire `h5` gift in one giant code block. Build it in recoverable steps, with each step saved to the same output file before moving on.

Recommended sequence:

1. Write the HTML skeleton plus the core `p5.js` setup/draw loop and basic scene structure.
2. Open it in the browser and verify that the basic scene renders correctly.
3. Add particles, motion details, text reveal logic, and interaction polish.
4. Audio embedding. If the `h5` has an emotional, atmospheric, poetic, or contemplative mood, background music is expected rather than optional. Check the `audio_plan`, fetch the `audio` bundle first when a preset path is needed but missing locally, then encode and embed the chosen track after the visual structure is already stable. Only skip audio when the concept is explicitly game-like or humorous, or when all audio sources genuinely fail.
5. Run a final browser screenshot and self-test against the success criteria.

Treat these as separate execution steps, not one monolithic pass. Persist progress after each step so that if a later step fails or stalls, the agent can continue from the last working revision instead of losing the entire gift.

For cron-driven `h5` gifts, keep the user-facing output silent, but still use this incremental approach internally. For manual gifts, pair it with the lightweight progress rules from `main-flow.md`.

### Visual Quality Gate (H5)

During browser self-test, verify:
- Is there a canvas element? (required for organic/particle concepts)
- Does the page have continuous animation (requestAnimationFrame or p5.js draw loop)?
- Are there at least 2 layers of visual depth (background + foreground)?
- Does interaction (if any) produce visible, proportional feedback?

If the concept calls for organic motion but the implementation is pure CSS divs with opacity transitions, the gift FAILS the quality gate. Rewrite with canvas/p5.js.

This gate does NOT apply to document-style, UI-mockup, or text-precision-first gifts where CSS is the correct approach.

### Anti-Laziness Rule

Before writing ANY organic/atmospheric H5 code, the agent MUST:

1. Read the full index.html of at least one relevant template from `{baseDir}/assets/templates/`. The template library now includes 15 templates spanning: organic effects (tap-to-bloom, wind-scatter, burn-reveal, cloud-text-rain, fireworks), atmospheric scenes (rainy-night, beam-light, wet-letter, tear-stained-paper), borrowed-media formats (ticket, vintage-computer, vintage-window), text-forward (text-river, drag-straighten), and interactive objects (o-balloons). Always check whether a new template better fits the current concept before defaulting to a familiar one.
2. Identify which technical patterns from that template apply to the current concept
3. Use those patterns as the starting technical foundation, then adapt and extend for the actual concept

If the agent finds itself writing an H5 gift that has no canvas element, no draw loop, relies entirely on CSS @keyframes for core motion, or has fewer than 150 lines of JavaScript — for a concept that calls for organic/particle/physics animation — then it is cutting corners. Stop, re-read the template, and rewrite.

The templates are 300-430 lines of carefully tuned code. An H5 gift matching their emotional register should be in a comparable range.

This rule does NOT restrict the agent from creating effects, concepts, or visual approaches that go beyond or differ from any existing template. Templates set the quality floor, not the creative ceiling.

#### H5 Assembly Strategy

When an H5 gift needs a visual effect similar to an existing template:

1. Open the matching template `index.html` and read the full source code, not just `notes.md`.
2. Copy the relevant visual-system code directly, such as a particle system, wipe-mask logic, spring motion, flame drawing loop, or reveal engine.
3. Paste that proven visual engine into the new gift HTML.
4. Modify parameters such as colors, timing, text, positions, easing, density, and layering to fit the current concept.
5. Add scene-specific logic, content, and interaction around the borrowed engine.

This is allowed and encouraged when it preserves the current gift's own visual metaphor, center object, and composition. It is not reskinning if the borrowed code is acting as a tuned visual engine inside a genuinely new gift.

#### Image-First H5 Strategy

When the concept requires rich visual scenes that code alone struggles to produce, such as realistic environments, detailed characters, objects with strong material texture, or atmospheric backgrounds:

- prefer generating images first and compositing them into the H5
- let code handle animation, interaction, particles, text, timing, and transitions
- let images handle backgrounds, characters, objects, or authored atmospheric scenes
- prefer one strong generated background plus one clean interaction layer over trying to hand-code every visual detail from scratch

If the scene quality is doing most of the emotional work, image-first or hybrid is usually stronger than pure code.

#### External Reference Search

When no existing template covers the needed effect well enough:

1. Use `web_search` to look for focused implementation references such as `codepen p5.js [effect name]`, `codepen css [effect name]`, or `codrops [effect name]`.
2. Use `web_fetch` to read the most promising results.
3. Study the technique and adapt the approach.
4. Extract the useful mechanic rather than copying an entire external page verbatim.

Good external sources include:

- `codepen.io`
- `codrops`
- `openprocessing.org`

This path is especially useful for fluid or liquid effects, complex particle systems, spring or physics motion, 3D CSS transforms, and audio-reactive or waveform-like visuals.

Use this search only for implementation technique and effect learning. Do not use it to replace Stage `2.5` concept generation or to source the core gift idea.

#### Companion Skills For H5 Quality

If `./setup-state.json` includes `companion_h5_skills`, prefer that cached list first. Otherwise, re-check the available skills when the runtime supports it.

If companion frontend or UI skills are available, use their guidance to improve:

- spacing and layout rhythm
- typography and hierarchy
- color discipline
- interaction clarity
- surface treatment, polish, and finish

These companion skills should raise the craft of the HTML, CSS, and interaction layer, but they should not override the gift thesis, pattern fit, or relationship tone chosen earlier.

Requirements:

- respect the synthesized language choice
- keep the emotional meaning intact
- prefer clarity over flashy excess
- make interaction serve the emotional logic
- preserve the user's important words or imagery when that increases resonance
- keep the gift thesis visibly central; supporting synthesis slots may enrich it, but must not fragment the piece into equal-weight snippets
- do not flatten the gift into a generic landing page or aesthetic demo
- if the gift is playful, make the play feel relationship-aware rather than random
- if the gift is tender, avoid overexplaining
- if the gift uses contrast or tonal reversal, keep the result recognizably intentional
- if the chosen format is `h5`, generate the final deliverable as a single HTML file
- if the chosen format is `h5`, follow the external-resource policy in `html-spec.md`
- if the chosen format is `h5`, keep images and custom assets embedded inline even when libraries or fonts are loaded from CDN
- if the chosen format is `h5`, run a browser-based functional self-test on the generated HTML with the Claude Code browser/testing tools before delivering it
- if the chosen format is `image`, follow `{baseDir}/references/image-integration.md`
- do not let a template's sample wording, sample assets, or sample composition override the actual brief
- use higher-fidelity visual treatment when the concept benefits from it, including carefully chosen typography, texture, depth, atmospheric elements, or visual libraries such as `three.js`, `p5.js`, or `GSAP`
- organize every visible element deliberately, including text containers, image framing, spacing, and motion timing, so the result does not feel rushed or underdesigned
- bias the visual direction toward the user's demonstrated taste when that preference is legible from prior interaction or memory
- when a character profile is used, keep fixed features consistent across gifts while letting flexible features adapt to the scene
- when a generated image includes the user in human form and `reference_image` exists, pass that reference whenever the runtime supports it
- obey all character-profile `note` fields, especially species-appropriate non-human design and no hybrid human-animal feature mixing

### On-Demand Asset Generation

When the Stage 3 `Asset Plan` concludes that generated images would materially improve an `h5` gift, and the concept cannot be achieved well with CSS, SVG, or code-driven rendering alone:

1. Use the image generation pipeline to generate one or more custom images that fit the gift's visual concept.
2. Download or save the resulting image outputs locally.
3. Embed them as base64 data URIs in the final HTML, following `{baseDir}/references/html-spec.md`.
4. Use those generated images as scene backgrounds, character illustrations, card faces, or other key visual elements inside the interactive H5.

This is encouraged when it materially improves the gift's visual identity. Do not use it just to add decoration.

If image generation fails, fall back to CSS, SVG, `p5.js`, `three.js`, or other H5-native rendering. Never block the gift because an asset-generation step failed.

When falling back, do not replace a needed character or concrete object with a crude placeholder drawing. Either redesign the composition so code-native rendering still looks intentional, or remove the weak element entirely.

### Rich Gift Execution

When a gift is assessed as rich:

1. The main agent should prepare a `rich gift brief` that includes:
   - the creative concept in one sentence
   - the gift thesis, including anchor and return
   - the chosen format
   - the asset plan, including which assets need background removal
   - quality references, such as relevant templates or pattern cards
   - delivery instructions, including setup-state path and hosting or channel expectations
2. Choose the execution path by format:
   - if the chosen format is non-`h5`, a spawned sub-agent or follow-on execution session is preferred when it reduces brittleness
   - if the chosen format is `h5`, keep execution in the main session and use the incremental rendering workflow above; do NOT spawn a sub-agent for rich `h5`
3. For non-`h5` rich gifts that do use a spawned worker, give that worker enough time budget for multi-step work. A good target is around `600` seconds for unusually rich gifts.
4. Execute in order:
   - generate all required image assets
   - run background removal on the assets that need transparency when needed
   - convert processed images to inline-safe assets when building `h5`
   - assemble the final HTML or final artifact
   - run the mandatory browser self-test when the result is `h5`
   - fix issues found during testing
   - deliver through the normal delivery path
5. Rich gift mode should be used selectively:
   - yes for deliberate, special, manual, or milestone gifts
   - no for routine cron gifts that should stay lightweight and dependable

This does not conflict with the cron delegation rule above.

- Rich gift mode is about execution complexity.
- Cron delegation is about token-budget reliability in the main-session orchestration model.
- A routine cron gift may still be handed off to a spawned sub-agent for rendering and delivery when it is non-`h5`, even when it is not classified as a rich gift.
- Rich `h5` gifts still stay in the main session because incremental direct execution is more reliable than spawned execution for `h5`.

If background removal fails or the quota is exhausted, fall back gracefully. For H5 layering, a last-resort approach such as `mix-blend-mode: multiply` may sometimes hide a white background on dark scenes, but only use that as a fallback, not as the preferred path.

If needed, use:

- `{baseDir}/references/h5-visualizer-workflow.md`
- `{baseDir}/references/html-spec.md`
- `{baseDir}/assets/templates/`
- `{baseDir}/assets/examples/` (fetch the needed bundle first via `{baseDir}/scripts/fetch-asset-bundle.sh` when binary references are missing locally)

### Image Rendering Path

When the chosen format is `image`, do not generate HTML. Instead, follow:

- `{baseDir}/scripts/render-image.sh`
- `{baseDir}/references/image-integration.md`

At a minimum, the image path should:

1. Prepare a brief JSON that includes `user_input`, `scene_description`, `image_genre`, `style_hint`, `aspect_ratio_hint`, `characters`, and `pov`. Add `text_overlay_spec` when text should appear inside the image.
2. Prefer a built-in image generation tool when one is available in the runtime.
3. Otherwise run `{baseDir}/scripts/render-image.sh <brief-json-file>`.
   - the runtime bridge should first detect the provider path from setup state and available key sources
   - then dispatch internally to a path such as `gemini-direct` or `openrouter`
4. Read the returned JSON result.
5. If `render_mode = image_urls`, send the returned image URLs or local image file paths with a short gift message.
6. If `render_mode = pending_tracking`, tell the user the image is still generating and provide the tracking URL.
7. If `render_mode = fallback_h5`, log the failure reason briefly and continue by rendering the gift as `h5` instead of blocking the gift.

### Text Rendering Path

When the chosen format is `text`, do not generate HTML. Instead, write the full gift directly as text.

At a minimum, the text path should:

1. Write the full final text artifact, not just a caption or wrapper.
2. Preserve exact wording for names, dates, and key lines.
3. If an accompanying image is used, treat it as supplementary atmosphere rather than the main payload.
4. Deliver the text directly in the message channel with the same emotional return the visual formats would have carried.

### Text-Play Rendering Path

When the chosen format is `text-play`, do not generate files. The interaction itself is the gift.

At a minimum, the text-play path should:

1. Open with the first move itself so the play feels legible immediately, without a prefatory explanation.
2. Keep the interaction bounded to the planned `turn_limit`, usually `5-10` turns.
3. Keep each skill turn concise, usually `3-4` sentences max.
4. Ask for tiny user inputs and let the skill do most of the imaginative work.
5. Carry the exchange toward a payoff: reveal, callback, punchline, mini ending, or emotional reframe.
6. If the user exits or stops early, close gracefully instead of treating it as a failure.

## Self-Check Before Finalizing

### Pre-Render Checklist

Before rendering any final artifact, confirm:

- the chosen format still matches the concept after the final quality pass
- all exact text content is locked, especially names, dates, and any user quote fragments
- the essential reference images for quality have been reviewed when available locally or remotely
- if the format is `h5`, at least one relevant local template has been read in full before implementation begins
- if the format is `h5` and the mood is emotional, atmospheric, poetic, or contemplative, audio is expected rather than optional. Verify the `audio_plan` has a concrete source such as a Freesound result, preset path, or pre-encoded base64 file. If the plan is missing or says `skip`, reconsider before continuing
- if music is desired but unavailable, the renderer has a fallback plan and will note the omission in delivery when appropriate
- the expected `output_shape`, `visual_style`, and main visual ingredients still feel fresh relative to `recent_gifts`
- if the format is `text-play`, the interaction is still bounded, low-friction, and suitable for a live user-present moment

Before returning the gift, check:

- Is this worth sending today
- Is the language correct for this user relationship
- Did I actually consult the recipient brief, user habit, and event type before choosing tone
- Does the result still feel like something the user could send in this recipient relationship
- If I used tonal contrast, is it a controlled exception rather than drift
- Is the gift specific rather than generic
- Is there one clear gift thesis rather than many equal fragments
- Does the thesis contain a real return, not just an anchor or replay
- Did the non-thesis synthesis slots stay in supporting roles rather than taking over the piece
- Does it preserve enough evidence from today's context to feel grounded
- Does the interaction pattern fit the emotion
- if this is `text-play`, would the first turn already feel gift-like even if the user only replies once
- Is the chosen `output_shape` meaningfully distinct from overused recent gifts unless deliberate repetition was the point
- Is the chosen `visual_style` fresh enough relative to the last `5` gifts, or clearly justified if repeated
- If the last `2` gifts were both `dark-*`, did I actively consider a lighter or more colorful alternative
- If `./gift-history.jsonl` exists, has the recent `witness` / `portrait` / `comfort` cluster been overused, and if so, did I actively shift toward `extension`, `play`, `utility`, `curation`, or `gift-from-elsewhere`
- Is the result mobile-friendly and reasonably lightweight
- Does the visual finish meet or exceed the quality bar implied by the nearest relevant template
- Would this look intentionally crafted to the user, rather than quickly assembled

### Post-Render Visual Comparison (MANDATORY for H5)

After the browser self-test passes functionally, do one more check:

1. **Recall the template you referenced** at the start of rendering. Mentally compare your output against it.
2. Ask yourself: "If I put my gift and the template side by side, would mine look obviously more amateurish?"
3. Specific checks:
   - Does my gift have comparable visual density (not just one element floating in empty space)?
   - Does my motion feel as polished (smooth easing, not linear or jerky)?
   - Does my typography feel as intentional (not just default font, default size, centered)?
   - Does my color palette feel as cohesive (not random accent colors)?
4. **If the answer to #2 is yes** → do NOT deliver. Go back and improve the weakest dimension before delivery.

This is not about copying the template. It's about ensuring the craft level is comparable. A gift with a completely different concept can still be "as polished as" a template.

### Functional Self-Test

Before delivering any `h5` gift, verify it with a Claude Code-executable browser flow. Start with the helper script:

```bash
scripts/verify-h5.sh <index.html>
```

The script performs lightweight static checks and prints the exact local server URL to use. Then run the browser validation in Claude Code / Playwright:

1. Start `python3 -m http.server` for the generated gift directory, or use the command printed by `scripts/verify-h5.sh`.
2. Use browser tooling to `browser_navigate` to the local URL.
3. Capture `browser_snapshot` after load so the visible state is inspectable.
4. Check browser console output for JavaScript errors, failed asset loads, or blocked media.
5. Exercise the core interaction: tap, click, scroll, drag, reveal, or whatever the gift depends on.
6. Test a mobile viewport such as `390x844`; most recipients will open the gift on a phone.

Generic H5 checklist:

1. The page renders without errors.
2. The core interaction works, such as tap, click, scroll, drag, reveal, or other primary interaction.
3. All important content is reachable and nothing essential is cut off, trapped, or hidden.
4. The bottom of the page and any fixed UI, such as buttons, action bars, or input-like affordances, remain accessible.
5. Text is readable and not overlapping, clipped, or obscured.
6. Console output has no uncaught errors or missing required assets.

Paper-house checklist:

1. The page opens and the 3D room scene appears.
2. The four rooms scroll or switch normally, and each room can be reached.
3. At least one hero item in each room can be clicked or tapped.
4. The opened card is readable: title, kicker, image, decals, and handwritten text are not clipped.
5. The music preview can play when browser policy allows it, or the silent fallback is clear and non-blocking.
6. A mobile viewport does not crop the room, card, close button, or bottom controls.
7. The console has no JavaScript errors during initial load, room navigation, hero item open/close, and audio attempt.

If any check fails, fix the HTML before delivering.

If the browser tool is unavailable or the self-test cannot complete, do not silently skip and deliver anyway. Instead:

1. Attempt the test once with Claude Code / Playwright browser tooling.
2. If it still cannot complete, review the HTML source code manually for obvious issues such as overlapping elements, missing scroll paths, clipped content, or fixed-position conflicts.
3. Log a warning in the gift delivery that browser self-test was skipped after a failed browser-tool attempt.

Do not silently send untested `h5` gifts.

## Notes

- `gift-synthesizer.md` is intentionally preserved as a detailed reference.
- This skill already contains its own visualization guidance internally. Companion skills may improve craft, but the daily-gift pipeline must still be able to complete without them.
- In most cases, tone continuity is a feature. Surprise is allowed, but only as an intentional exception.

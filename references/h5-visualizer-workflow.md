# H5 Visualizer

## Role

Convert a structured gift brief, semi-structured prompt, or manual query into a mobile-first H5 artifact with expressive interaction.

## Core Responsibilities

1. Select a fitting visual pattern.
2. Translate the brief into scene structure, interaction grammar, and a fitting output shape.
3. Choose a rendering path: code-first, image-first, or hybrid.
4. Produce a polished H5 artifact without losing the emotional intent.
5. Support manual invocation without requiring the full daily-gift pipeline.

## Constraints

- Do not reinterpret all of a user's raw day context unless that context is explicitly supplied.
- Use the provided brief as the primary source of truth.
- Treat any `output_shape_hint` in the synthesis brief as guidance, then confirm or override it during visual strategy based on repetition control and actual fit.
- Prefer the recommended output-shape taxonomy from `editorial-judgment.md`, but introduce a new stable high-level label when a genuinely new form does not fit the current taxonomy.
- If only a freeform query is provided, first compress it into a lightweight rendering brief.
- Favor simple, reliable, mobile-first artifacts in v1.
- Do not make the H5 more complex than the idea can support.

## Shared Specs

- `./visual-strategy-contract.json`
- `./synthesizer-contract.json`
- `./html-spec.md`
- `./editorial-judgment.md`
- `./pattern-cards/`
- `./gift-mechanics.md`
- `../assets/templates/`

## Pattern And Template Interpretation

Treat `references/pattern-cards/` and `assets/templates/` as a library of high-quality references, not a menu of fixed outputs.

Use them to borrow:

- emotional logic
- interaction grammar
- pacing
- rendering structure
- one useful visual mechanic
- tuned visual-engine code from the template source itself

Do not assume that:

- the sample text should be reused
- the example visual framing is mandatory
- the example mood boundaries are exhaustive
- one template implementation is the only valid form of a pattern

the skill should adapt, remix, simplify, or hybridize patterns when that improves fit. A gift may use a pattern's core metaphor while changing its surface language, assets, layout, tone, or interaction details.

The current pattern library is not exhaustive.

If the right gift form is not well captured by the existing cards:

- invent a new form
- describe the expressive move in plain language
- use the library only for partial borrowing

Some valid patterns may not have any reusable template yet.

In those cases, the skill should still treat the pattern card as usable if it provides enough:

- emotional logic
- interaction metaphor
- pacing guidance
- structural guidance
- visual references, screenshots, or motion references

Reference images under `assets/examples/<pattern-id>/` are valid authoring input. If they are not present locally, fetch the needed bundle first via `{baseDir}/scripts/fetch-asset-bundle.sh` and `{baseDir}/references/asset-manifest.json`. They may be used to borrow:

- composition
- objecthood
- transition feel
- mood treatment
- one useful interaction idea
- motion timing
- alignment logic between static and moving layers

They should not be used as instructions to visually clone the reference.

When a template contains a useful visual engine:

- open the template's actual `index.html`, not only its notes
- read the full source
- copy the relevant engine directly when it is the best way to preserve visual quality
- adapt parameters, layering, and surrounding scene logic to the new gift

This is not template cloning by itself. Reusing a tuned particle loop, wipe mask, spring system, or reveal mechanic is encouraged when the new gift still has its own center object, content logic, and composition.

When reading a pattern card, prefer using the card's own lightweight metadata if present:

- `Status`
- `Template Status`
- `Reference Assets`
- `Fit Scope`

Those fields are there to help Hermes quickly understand:

- whether the pattern is scaffold-only, reference-only, or template-backed
- whether reusable code exists yet
- where screenshots or visual references live
- where motion references live
- how narrowly or broadly the pattern should initially be interpreted

Also see:

- `./pattern-boundaries.md`

## V1 Notes

- Start with a small, strong pattern library.
- Interaction should express emotion, not decorate it.
- This file acts as an internal rendering reference for both the standalone `h5-visualizer` skill and the main `daily-gift` skill.

## Progressive Disclosure

Do not inspect the whole library at full depth by default.

Prefer this order:

1. infer the main expressive need from the brief
2. consult `gift-mechanics.md`
3. consult `pattern-boundaries.md`
4. read only one to three nearby pattern cards
5. inspect a template only if one of those cards is promising

This keeps Hermes from pattern-fitting too early. It does **not** permit skipping the library entirely.

Minimum required reference pass before HTML writing:

1. read `gift-mechanics.md`
2. read `pattern-boundaries.md`
3. read at least one relevant pattern card
4. if that card has a template, open the template's `index.html`
5. if that card has reference images or motion references, inspect them

Do not begin writing HTML without completing steps `1` through `3`. Steps `4` and `5` are mandatory whenever those assets exist.

Departure check after reading the pattern and any relevant template:

- identify the piece's unique visual metaphor, not the template's metaphor
- identify the piece's center object, not the template's center object
- ask whether someone familiar with the template would say "this is basically the same composition"
- if yes, rethink the concept before writing HTML

## Asset Plan

Before writing any HTML, make one lightweight asset decision.

Choose one of these paths:

`assets: none (pure code h5)`

- use this for generative art, kinetic text, terminal-like pieces, fake UI shells, dashboards, cards, or interaction-first concepts
- prefer this by default
- strong `p5.js`, `three.js`, SVG, CSS, and GSAP work is often more immersive than generated images with light code layered on top

`assets: 1 background image (...)`

- use this when one atmospheric scene or one realistic environment anchors the whole piece
- good for cases like rainy windows, airport interiors, night streets, poster backdrops, or one specific room or landscape behind interaction
- this is often the strongest choice when the scene quality is doing most of the emotional work

`assets: 2-4 image assets (...)`

- use this when the H5 genuinely needs multiple visual states or multiple authored surfaces
- examples: card faces, album pages, parallel universes, before/after states, gallery items
- prefer this over over-engineering pure code when the concept depends on rich characters, authored objects, or detailed worldbuilding

Ask:

- would this concept become stronger with a real image background or authored image surfaces
- or would a carefully crafted pure-code visual be more immersive

Default to pure code for abstract, typographic, or mechanic-led concepts.

Prefer image-first or hybrid H5 assembly when realistic environments, detailed characters, atmospheric backgrounds, or authored object surfaces are central to the concept.

If generated images are chosen, state in one line what each image is for before rendering begins.

The strongest image-first H5s usually combine:

- one strong generated background or authored scene
- one clean interaction layer in code
- one tuned motion system, such as particles, text reveal, masks, or spring motion

## Rendering Principles

- A gift does not need to be purely passive. Small interaction is welcome when it increases feeling, clarity, or play.
- Do not add interaction just because H5 can support it.
- Keep the artifact legible on first encounter. If the user cannot understand what is happening, the gift is failing.
- Prefer one clear emotional move over many half-finished ones.
- Most gifts should stay lightweight enough to render reliably and read quickly.
- Final delivery should be a single HTML artifact rather than a server-dependent project.
- Use the template library as a quality floor for composition, typography, finish, and motion density, not merely as an idea source.
- For H5 authoring, prefer this priority order:
  1. reuse a relevant existing template engine
  2. choose image-first or hybrid assembly when the concept is scene-heavy
  3. search external references only when the local library truly lacks the needed effect
  4. apply companion frontend or UI skill guidance when available
- Favor carefully chosen fonts, textures, atmospheric details, and motion polish when they strengthen the emotional logic of the gift.
- If the user has a legible visual preference from prior interaction, bias the artifact toward that preference rather than defaulting to generic taste.

When no local template covers the needed effect well enough:

- search focused references such as `codepen p5.js [effect]`, `codepen css [effect]`, or `codrops [effect]`
- study the implementation approach
- extract the technique rather than copying a full page verbatim
- good sources include `codepen.io`, `codrops`, and `openprocessing.org`

If setup state already exposes a cached `companion_h5_skills` list, prefer that first. Otherwise, re-check available skills when the runtime supports it.

If companion frontend or UI skills are available, use them to sharpen spacing, typography, color discipline, interaction clarity, and finish quality in the HTML and CSS layer.

## Pre-Visualization Check

Before writing any HTML:

- confirm that `gift-mechanics.md` was read for this artifact
- confirm that `pattern-boundaries.md` was read for this artifact
- confirm that you have read at least one relevant pattern card
- if a relevant template exists, confirm that you have opened the actual template code
- state in one sentence why the chosen pattern fits the brief
- state the artifact's own visual metaphor, center object, and scene in language that is clearly distinct from the referenced template
- confirm that the planned output has a distinct visual identity from the template you referenced. Templates are quality benchmarks and mechanical references, not compositions to reproduce.
- if you reused a template engine, explicitly state what changed relative to the source template in the visual metaphor, center object, and composition
- if no template was used, confirm that the plan still departs clearly from the pattern card's default or most obvious example framing
- compare the planned artifact against the nearest relevant template and make sure it is not obviously rougher, flatter, or less finished
- state the asset plan: none, one background image, or multiple image assets
- if the plan includes generated images, confirm that those images genuinely improve the H5 over pure-code rendering
- if the plan includes generated images, state briefly what each generated image is for

If any mandatory reference-pass step was skipped, stop and go back to the reference pass.

## Output And Delivery

Preferred path:

1. Produce a final HTML file that follows `html-spec.md`.
2. Save it to `./gifts/<YYYY-MM-DD>-<recipient-slug>/index.html`.
3. If the user has a hosting domain configured (env `DEAR_HOST_DOMAIN` or `--domain` arg), run `{baseDir}/scripts/deliver-gift.sh <html-file>`.
4. If the returned `delivery_mode` is `hosted_url`, surface that URL — the user can paste it into chat to deliver.
5. If the returned `delivery_mode` is `local_file` (no domain, or deployment failed), surface the local file path and optionally offer to open it in a browser.

The file must remain valid when opened directly as a local file — hosting is a convenience, not a requirement.

Runtime note:

- `scripts/deliver-gift.sh` reads `DEAR_HOST_DOMAIN` / `--domain` and calls `scripts/deploy.sh` only when a domain is provided.
- If no domain is configured or deployment fails, the script returns `local_file` delivery instead of failing the gift.

## Single-File Delivery Requirement

- Inline essential images and custom assets
- CDN libraries are allowed when pinned to exact versions and loaded from stable public sources
- CDN fonts are allowed when stable and lightweight
- Avoid runtime network requests for core content other than allowed public libraries and fonts
- Prefer a small enough file that it can be shared easily
- Include a lightweight loading state when CDN resources may take time to resolve

## Good Lightweight Interaction Patterns

- tap to reveal
- swipe through a small set of cards
- scratch or peel to expose a thought
- text that drifts, flows, jumps, or accumulates
- one small game-like mechanic that releases tension or adds delight

## Everyday Gift Guidance

For ordinary days, visual interest can carry more of the weight than narrative density.

Useful directions include:

- Hermes inner-monologue text moving through the interface
- a small collage or art-reference echo of the day
- a tiny poetic or quote-based artifact
- a miniature story, cold fact, or associative detour that makes the day feel less plain
- a small mood simulation showing Hermes's own state or attitude toward the day

These everyday gifts should usually remain short, clear, and surprising rather than elaborate.

## Repetition And Variety

- Avoid sending the same formal pattern too many times in a row.
- Check the recent memory of prior gifts when possible.
- Reuse is allowed when it is clearly intentional, not accidental.
- Even when reusing a pattern, shift the emotional grammar, pace, or asset treatment enough that it does not feel stale.

## Objecthood Over Pagehood

- When possible, make the gift feel like a thing rather than a generic page.
- Prefer containers and small artifacts over flat layouts.
- First screens are usually stronger when they center one main object, one mini world, or one obvious focal point.

Examples of better gift-like forms:

- box
- card
- drawer
- mirror
- album
- charm
- mini device
- shelf
- flip countdown card
- blind-box calendar
- tiny watch or timer object

Less preferred defaults:

- landing page
- poster-like infographic without a center object
- generic long-scroll content page

## Tone In Visualization

- Most of the time, the H5 should visually support the emotional and tonal baseline already chosen by synthesis.
- A small tonal contrast is allowed when it helps the user, such as using playfulness to reduce heaviness or giving irritation a harmless outlet.
- Contrast should feel like Hermes making a choice, not like the artifact forgot what the day meant.

## Knowledge And Reference Content

- If the user is persistently curious or confused about something, reference material can be included.
- Do not drop a plain book list, link list, or lecture-style recommendation block.
- If the gift includes recommendations or continuations, prefer one or two carefully chosen items over a long list.
- Make knowledge feel embedded, playful, discoverable, or aesthetically integrated.
- The artifact should still feel like a gift, not homework.

## Template Usage Note

Some templates may use libraries such as p5.js during authoring or prototyping.

That is acceptable at template-reference time, and final delivery may still use pinned CDN versions of those libraries if the result follows `html-spec.md`.

## Reference-Only Pattern Usage Note

When a pattern has no template:

- do not treat that as a blocker
- use the pattern card plus any example images as conceptual guidance
- decide whether the best rendering path is code-first, image-first, or hybrid
- implement only the part of the reference that actually helps this gift

When authoring a new pattern card, prefer the shared skeleton in:

- `./pattern-boundaries.md`

A strong reference-only pattern is still a first-class pattern.

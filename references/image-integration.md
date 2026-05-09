# Image Integration

## Overview

Daily gift can optionally generate single-image gifts such as stickers, mood images, posters, proxy-character scenes, surreal stills, collages, or other image-first returns.

Use image output when the selected `gift_mode` or hybrid format decision points to `image`.

Current scope:

- setup and configuration are wired
- the runtime entry point exists
- image key detection and provider selection are wired
- provider-specific execution currently supports both `openrouter` and `gemini-direct`
- base64 image responses may be decoded and saved as local files when the provider does not return a plain URL
- all failures remain soft failures and should return `fallback_h5` instead of blocking the gift

## Runtime Entry Point

Use:

- `{baseDir}/scripts/render-image.sh <brief-json-file>`

The script is the runtime bridge for the image path.

At this stage it should:

- read image configuration from setup state
- detect the provider/runtime path based on setup configuration and available key sources rather than assuming one fixed provider
- dispatch internally to a provider path such as `gemini-direct` or `openrouter`
- validate the image brief shape
- call the actual provider API when a supported path is available
- decode base64 image payloads into local files when needed
- return structured JSON
- fall back cleanly to `h5` when provider execution fails or no usable credentials are available

Current internal runtime shape:

1. provider detection
2. provider-path dispatch
3. provider-specific execution
4. decode or normalize returned images
5. soft fallback when needed

## Prompt Hygiene

Image generation models treat ALL text in the prompt as potential visual content. Before sending any prompt to the image API:

- Remove all file names, paths, and technical references (e.g. `image_0.png`, `/tmp/output.jpg`, `base64`)
- Remove all internal variable names or API field names
- Remove all English technical instructions that are not part of the desired image content
- If referencing a user's image as input, do NOT mention the filename in the scene description — the API handles image attachment separately
- Double-check: would every word in this prompt make sense as something visible in the final image? If not, remove it.

This prevents the model from rendering debug text, filenames, or technical artifacts inside the generated image.

## Language Matching

When the user and the recipient communicate in Chinese, ALL text that appears inside the generated image must be Chinese — unless English is deliberately part of the concept (e.g. a fake English-language newspaper).

In the scene_description and text_overlay_spec, explicitly state: "All visible text in the image must be in Chinese (简体中文)."

The prompt itself may use English for scene/style instructions (image models often understand English prompts better), but any quoted text that should appear in the final image must be written in Chinese within the prompt.

Example:
- Bad: "Temperature display: 'Annoyed 23°'"
- Good: "Temperature display: '心烦 23°'"

## Post-Render Language Verification

After generation, verify the actual visible language before treating the image as complete.

This is mandatory whenever:

- the image includes any visible text
- the concept depends on Chinese wording being readable
- the borrowed-media shell or poster logic would break if the text language is wrong

Checks:

- is the visible text in the intended language
- are key words legible rather than garbled
- does the generated text match the concept closely enough to preserve the return

If the answer is no:

- retry once with stricter language instructions if the image format still makes sense
- reduce or simplify on-image text if the concept can survive with less
- switch to `h5` or direct `text` if exact wording is essential

Do not knowingly deliver an image whose visible language is wrong for the user or whose text corruption destroys the return.

## Brief File Contract

Pass a JSON file that contains at least:

- `user_input`
- `scene_description`
- `image_genre`
- `style_hint`
- `aspect_ratio_hint`
- `characters`: array of character descriptions appearing in the image, each carrying species, color, distinguishing features, and role in the scene; pull these from `./user-portrait/` metadata plus any OC definitions in the recipient brief, the supplied user context, setup-state, or taste-profile when relevant
- `pov`: whose perspective the image represents, such as `hermes watching user`, `user self-view`, or `third-person`; the composition should match this rather than drifting into a generic default angle
- `text_overlay_spec` when text should appear inside the image

When established character identities exist, include them explicitly in the prompt. Do not collapse them into generic `dog`, `fox`, `girl`, or `person` wording if the gift depends on recurring OC identity or a specific relationship viewpoint.

Recommended result contract:

```json
{
  "render_mode": "image_urls",
  "image_urls": ["https://.../gift.png"],
  "tracking_url": "",
  "provider": "openrouter",
  "provider_path": "openrouter",
  "model": "google/gemini-3.1-flash-image-preview",
  "genre": "mood-photo",
  "fallback_reason": "",
  "warning": ""
}
```

`image_urls` may contain either:

- remote provider URLs
- local absolute file paths created by decoding returned base64 image data into `./generated-images/`

Both are valid delivery artifacts. The caller should not assume the result is always an `https://` URL.

Possible `render_mode` values:

- `image_urls`
- `pending_tracking`
- `fallback_h5`

## Setup Requirements

Store these values in `./setup-state.json` when image mode or hybrid mode is enabled:

- `gift_mode`
- `image.enabled`
- `image.provider`
- `image.model`
- `image.api_key_source` or `image.api_key`

### Default Image Model Strategy

If `image.model` is already configured in setup-state, use it.

The runtime should pass that configured model through as-is rather than hardcoding one exact accepted model name inside `render-image.sh`.

If no image model is configured, silently detect the best approved default from the available key path and persist it back to setup-state. Do not ask the user to choose from a comparison table during setup.

Current default policy:

- start with `openai/gpt-5.4-image-2` (best photographic realism, material texture, and text rendering)
- if `gpt-5.4-image-2` fails or is unavailable, fall back to `openai/gpt-image-1`
- if no OpenAI image model works, fall back to `google/gemini-3.1-flash-image-preview`
- detect supported image-generation keys in a fixed order and use the first one found
- if a chosen model is rejected at generation time, fall back to the next approved option rather than stopping to ask the user about model routing

Persist the detected `provider`, `model`, and exact `api_key_source` so later runs stay stable instead of redetecting on every gift.

Provider may vary depending on where the user configured access to that model:

- direct Gemini or Google path using `GEMINI_API_KEY` or `GOOGLE_API_KEY`
- routed provider path such as `openrouter` using `OPENROUTER_API_KEY`

Prefer storing an environment variable source rather than a raw secret when possible.

If the user does not know which provider path to choose, the skill should prefer the most direct working path it can detect from configured key sources rather than forcing the user to understand the routing details.

That means:

- use `gemini-direct` when a direct Gemini or Google key path is the clearest working route
- use `openrouter` when the user has configured access through `OPENROUTER_API_KEY`
- keep this decision inside the runtime bridge rather than asking the user to reason about implementation details unless setup is ambiguous

Recommended setup-state mapping when keys are auto-detected:

- `OPENROUTER_API_KEY` -> write `image.provider = openrouter` and `image.api_key_source = OPENROUTER_API_KEY`
- `GEMINI_API_KEY` -> write `image.provider = gemini-direct` and `image.api_key_source = GEMINI_API_KEY`
- `GOOGLE_API_KEY` -> write `image.provider = gemini-direct` and `image.api_key_source = GOOGLE_API_KEY`

Persist the detected `provider` and the exact detected `api_key_source`. Do not ask the user to choose between these routes when runtime context already makes the answer clear.

### API Key Detection Order

During setup or first image generation, silently check for these environment variables in order:

1. `OPENROUTER_API_KEY` -> use the OpenRouter path
2. `GEMINI_API_KEY` -> use the Gemini direct path
3. `GOOGLE_API_KEY` -> use the Google AI path

Use the first one found.

If none are found:

- note in setup-state that image generation is currently unavailable
- during onboarding setup, one casual non-technical ask is allowed before the first gift; see `{baseDir}/references/main-flow.md`
- continue supporting `text` and `h5` gifts without image generation

Only the keys listed above are supported for image generation.

When using `OPENROUTER_API_KEY`, the OpenRouter path supports both OpenAI image models (`openai/gpt-5.4-image-2`, `openai/gpt-image-1`) and Gemini models. No separate `OPENAI_API_KEY` is needed for image generation through OpenRouter.

Outside of the single onboarding ask described in setup flow, do not prompt the user for image API keys.

Exception:

- a rare, lightweight reminder is allowed in user-present runs when image capability is still missing and the current gift would be materially stronger as an image; see `{baseDir}/references/main-flow.md`
- do not interrupt artifact generation once the user has already asked the skill to proceed

See also:

- `{baseDir}/setup-state.example.json`

## Provider Execution Notes

### `openrouter`

Use:

- `POST https://openrouter.ai/api/v1/chat/completions`

Recommended request shape:

- `model = google/gemini-3.1-flash-image-preview`
- `modalities = ["image", "text"]`
- one user message containing the final prompt
- include `image_config.aspect_ratio` when `aspect_ratio_hint` is present

Expected response shape:

- generated images usually appear in `choices[0].message.images[]`
- image data may be a remote URL
- image data may also be a base64 data URL such as `data:image/png;base64,...`

If the provider returns base64 data, decode it to a local file and return that local path in `image_urls`.

### `gemini-direct`

Use the Gemini image generation REST API directly, for example:

- `POST https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-flash-image-preview:generateContent`

Recommended request shape:

- authenticate with `x-goog-api-key`
- send `contents[].parts[].text` with the final prompt

Expected response shape:

- generated image bytes may appear in `candidates[].content.parts[].inline_data`
- `inline_data.mime_type` gives the mime type
- `inline_data.data` is base64-encoded binary image content

Decode each returned `inline_data` image to a local file and return those local paths in `image_urls`.

## Alternative: Direct Tool Invocation

If the skill's runtime provides a built-in image generation tool, the agent may bypass `render-image.sh` entirely and:

1. call the image tool directly with the final prompt
2. receive an image path or URL from that tool
3. deliver it using the standard image delivery flow

This is preferred when available because it avoids shell-level API orchestration and benefits from built-in auth, retries, and error handling.

`render-image.sh` remains the fallback runtime bridge for environments that prefer or require script-based execution.

## Genre Strategy

Image output uses genre cards rather than H5 pattern cards.

See:

- `./image-genre-chooser.md`
- `./image-genres/meme-sticker.md`
- `./image-genres/mood-photo.md`
- `./image-genres/proxy-character-scene.md`
- `./image-genres/borrowed-media-layout.md`
- `./image-genres/emotion-poster.md`
- `./image-genres/surreal-film.md`

These genres help choose:

- prompt framing
- subject treatment
- text-on-image tolerance
- whether the result should feel like a sticker, photo, poster, proxy-scene, or surreal still
- whether the user should appear directly, indirectly through a proxy character, or not at all
- whether the concept gains power by being framed inside a borrowed cultural medium such as a headline, cover, lyric screen, or certificate
- whether the image should stay mostly realistic while using light symbolic moves, which is often the sweet spot for `mood-photo`
- whether one emotional line should become the visual center of an original poster composition, which often points to `emotion-poster`
- whether the image needs analog grain, glow, and one strong impossible symbolic event, which often points to `surreal-film`

When a chosen genre file contains an `AI Generation Control` section, treat that section as the primary practical prompt-building guide for generation quality.

That means:

- do not stop at the genre's earlier `Prompt Strategy` section
- read the genre's `AI Generation Control` section before writing the final prompt
- use its magic words, poison words, composition rules, text rules, and prompt template as steering guidance rather than rigid formula

Direct self-image is no longer treated as a standalone image genre. If the gift has self-related material, use the chooser to decide whether that presence should become a proxy scene, poster, borrowed-media frame, mood-led still, or surreal symbolic figure.

Division of labor:

- this file defines universal image-quality and prompt-building principles that apply for all users
- `assets/examples/` and the image-genre reference assets define the concrete visual benchmark for what counts as good-looking in this skill; if the needed binary references are missing locally, fetch the relevant bundle first via `{baseDir}/scripts/fetch-asset-bundle.sh`
- the recipient brief, current conversation, and any explicitly supplied taste notes help infer the user's personal taste and how strongly to lean toward it

## When To Prefer Image

Prefer image when:

- one still frame can express the full anchor-plus-return pair
- interaction is unnecessary
- narrative sequencing is unnecessary
- the gift needs very polished visual finish or strong instruction following
- meme, atmosphere, collage, sticker, poster, proxy-character scene, or surreal still treatment is more fitting than panel-based structure
- the user wants the return to land through one precise frame rather than motion or participation

Do not default to image only because it seems easier. Choose it when the still-image form is itself the right return.

## Image As H5 Asset, Not Final Output

Sometimes image generation is not the gift itself.

Sometimes it is only one ingredient inside an H5.

When an H5 is being planned, use generated images only when they materially improve the concept:

- one real-looking background scene behind a wipe, reveal, or atmospheric interaction
- one poster-like environment that anchors the whole H5
- a small set of authored surfaces such as card faces, album pages, or parallel-world panels

Do not reach for image generation when pure code would already be stronger:

- generative particles
- kinetic text
- terminal or changelog aesthetics
- fake apps, dashboards, cards, or other CSS/SVG-first interfaces
- interaction-led concepts where motion, timing, and object behavior matter more than realism

The default for H5 should still be `assets: none (pure code h5)` unless generated images clearly add something code alone cannot achieve well.

If images are used as H5 assets, state what each one is for before rendering begins rather than generating them vaguely "for polish".

## Prompt Quality Rules

Image prompts should be concrete rather than generic.

Describe at least:

- the subject or scene
- the emotional treatment
- the visual style
- the framing or composition
- important objects, clothing, or environment details when relevant

Avoid prompts that only say "make it beautiful" or "in a nice style." The prompt should specify what kind of beauty or style is intended.

## Realism & Human Touch

This section is mandatory reading before writing any image prompt.

### What We Actually Mean

The goal is NOT "make it look like a phone snapshot." The goal is: **make it look like a talented human with good taste made it** — not an algorithm.

A talented human photographer takes beautiful photos. A talented human designer makes striking posters. A talented human illustrator draws with soul. None of their work looks like a 3D render or a stock photo — but none of it looks ugly or mundane either.

"Human touch" means: soul, intention, aesthetic judgment, and the small imperfections that come from physical media and real craftsmanship. It does NOT mean: ugly, documentary, lo-fi, or stripped of beauty.

### The Actual AI Tells To Eliminate

These are the specific things that make images scream "AI generated":

1. **Plastic textures** — surfaces that look like they're made of the same smooth material. Real wood, paper, fabric, ceramic, and metal all behave differently under light.
2. **Shadowless global illumination** — everything lit from nowhere. Real scenes have a light source and shadows follow it.
3. **Uncanny object fusion** — a pen melting into a notebook, earphone wires merging with the table surface. Real objects sit ON TOP of other objects with tiny shadow gaps.
4. **Pseudo-text** — fake characters that look like writing from a distance but are gibberish up close. Especially bad for Chinese characters and barcodes.
5. **Sterile perfection** — razor-straight paper edges, perfectly centered composition, zero wear on any surface. Real objects have been touched, used, and lived with.
6. **Depth-of-field as a filter** — a binary sharp/blurry split instead of gradual optical falloff.

Fix THESE specific problems. Do not overcorrect into ugliness.

### For Photographic Scenes

When the image should feel like a photograph:

- Specify a camera or lens to anchor the optical character: "Fujifilm X-T4 with 35mm f/1.4" gives warm tones and shallow depth; "iPhone 15 Pro" gives computational sharpness with natural night grain. Choose based on the MOOD, not as a dogmatic rule.
- Light should come from somewhere identifiable and all shadows should be consistent with it.
- Depth of field should follow real optics — gradual, not binary.
- Small physical details sell reality: condensation on glass, natural paper curl, fabric drape with gravity. But only include details that serve the scene — do not add ugly debris just for "realism."

**The image should still be beautiful.** Real photographers compose carefully, choose golden hour light, find gorgeous angles. The difference from AI is that the beauty feels OBSERVED and SPECIFIC, not GENERIC and RENDERED.

### For Borrowed-Media Objects (tickets, newspapers, certificates)

When the image is a physical artifact in a scene:

- The object should feel like it has weight and material — paper stock, ink texture, printing artifacts.
- Text, barcodes, and printed elements must be structurally correct and legible.
- Place the object in a real environment with consistent lighting.
- The object should look like it's been handled — not pristine, not destroyed, just naturally present.

### For All Genres (including illustration, poster, surreal)

Human touch is not limited to photographic realism:

- **Handmade quality** — handwriting has baseline variation, printed materials show ink behavior, design layouts have intentional asymmetry.
- **Material truth** — surfaces feel like specific materials, objects have weight and cast shadows.
- **Aesthetic intention** — the image looks like someone with taste CHOSE this composition, this color, this framing. Not like an algorithm averaged a million images together.

### The Cardinal Rule

**Beauty and realism are not opposites.** The best images are both beautiful AND feel human-made. If your prompt produces something ugly or mundane, the problem is NOT that you added too much realism — the problem is that your creative concept or scene choice was weak.

A good test: would someone with good taste save this image to their phone? If no, the issue is the concept or composition, not the realism instructions.

### Quick Self-Check

1. Does this image have a clear creative concept that connects to the gift's emotional thesis? (If the image could be "any rainy street" or "any coffee shop," the concept is too generic)
2. Is the image beautiful or striking in a way that reflects human aesthetic judgment?
3. Are the specific AI tells (plastic textures, no shadows, fused objects, pseudo-text) eliminated?
4. Would the recipient want to look at this image for more than 2 seconds?

## Anti-AI-Cliché

These are specific visual patterns that AI image generators default to. They are not inherently ugly, but they are so overused in AI output that they immediately signal "this was generated." Avoid them unless you have a very specific creative reason to use one.

### Visual Clichés To Avoid

- **Glowing particles / golden light dust / magical embers** floating in the air. This is the single most common AI visual trope.
- **Symmetrical split composition** — left side is one world, right side is another, with something glowing in the middle connecting them.
- **Text floating in the air** with glow effects. If text must appear, it should be printed, written, projected, or displayed on a surface — not hovering.
- **Everything emitting light** — hair glowing, hands glowing, clothes glowing, the ground glowing. In real images, light comes from specific sources and only some surfaces reflect it.
- **HDR color grading** — over-saturated with exaggerated complementary color pairs (purple-gold, teal-orange, blue-amber). Real images and real design can be colorful and vibrant without being HDR-processed.
- **"Concept art" rendering** — the hyper-detailed, semi-realistic digital painting style common in game art and AI galleries. Unless the concept specifically calls for concept art, avoid this look.
- **Literal visual metaphors** — if the concept is "connection," do not draw a bridge or a glowing thread. If the concept is "time passing," do not draw a clock melting. These are visual clichés. The concept should express itself through a specific, concrete scene, not through a symbol diagram.

### What This Is NOT

This is NOT a restriction on style range. Images can be:

- Vibrant, colorful, and maximalist — as long as the color choices feel intentional, not HDR-processed
- Dramatic and high-contrast — as long as not everything is glowing
- Fantastical or surreal — as long as the fantasy element is specific and original, not "generic magic particles"
- Warm and golden — as long as it's motivated by a light source, not a uniform filter

The test is: does this visual choice feel like a specific creative decision, or does it feel like the default output of an image generator?

### Aesthetic Anchoring

When writing prompts, reference a real-world visual style source to anchor the aesthetic. This gives the model a human taste reference instead of defaulting to "AI pretty."

Examples of useful anchors:
- A specific magazine: "Kinfolk editorial photography," "National Geographic natural light"
- A specific filmmaker: "Wong Kar-wai's color palette," "Wes Anderson's symmetry and pastel palette," "Terrence Malick's natural light and landscape"
- A specific photography style: "Japanese street photography," "Magnum photojournalism warmth," "fashion editorial in Dazed magazine"
- A specific design tradition: "Swiss poster design," "Japanese minimalist packaging," "1960s Penguin book covers"

The anchor does not constrain — it orients. A "Wong Kar-wai palette" can appear in many different compositions and subjects. It just prevents the model from falling back on generic AI aesthetics.

Include the aesthetic anchor as the first element in the prompt, before the scene description.

## Universal Aesthetic Principles

These apply to all image genres as a quality floor.

They are not personal style preferences.

### One strong visual idea per image

- a single unexpected composition choice beats stacking multiple beautiful elements
- before writing the prompt, state the one visual idea in one sentence
- everything else in the prompt should serve that one idea

### Describe observation, not inventory

- bad: `a park with cherry trees, a path, petals falling, sunlight, a bench`
- good: `cherry blossom petals trapped in the surface tension of a rain puddle, one petal just breaking through`
- the prompt should describe how we are seeing, not just what is there

### Material over label

- instead of `beautiful light`, describe the light's behavior, such as `low sun refracting through wet petals, casting pink caustics on the stone`
- instead of `dreamy atmosphere`, describe what creates it, such as `shallow depth of field with foreground bokeh from a rain-beaded window`
- specificity produces quality; labels alone usually produce generic images

### Less is usually more

- three well-chosen elements in a frame usually beat ten
- negative space, partial visibility, and what is deliberately left out of frame can be more powerful than what is shown

## Per-Genre Aesthetic Guide

Each genre has a different definition of `good`.

Use the matching guide when writing prompts.

### `mood-photo` / `surreal-film` — viewing method

What makes these genres high-quality is not the subject itself but the way the subject is observed.

Principles:

- prefer indirect observation: reflections, shadows, silhouettes, partial views, refractions, and surfaces
- `spring` can be water ripples distorting cherry blossoms, not just a person standing among flowers
- `rain` can be wet glass with bokeh city lights, not just someone holding an umbrella
- describe light behavior and material texture, not just scene elements
- when in doubt, remove the human figure; a scene that breathes on its own is often stronger than one anchored to a generic figure
- if a person must appear, prefer a back silhouette, a hand entering frame, a shadow, or a blurred form
- AI-generated full human figures often break the mood with uncanny details

Anti-patterns:

- `subject centered + pretty background + dramatic light` equals wallpaper, not art
- listing `6` or more beautiful things in one prompt
- including a person just because the frame feels empty without one

### `meme-sticker` — creative contradiction

What makes memes good is not visual beauty but unexpected emotional contradiction.

Principles:

- the humor comes from the gap between what is shown and what it means
- exaggerate one thing: the emotion, the prop, the scale, or the context, but not everything at once
- keep it readable at thumbnail size; busy memes die fast
- cheap, lo-fi, slightly cursed aesthetics are often funnier than polished renders
- deadpan delivery is often funnier than a character mugging at the camera

Anti-patterns:

- generic cute character plus text caption
- trying to be beautiful and funny at the same time instead of choosing a priority
- overexplaining the joke in the prompt

### `emotion-poster` — typography as emotion

What makes posters good is the fusion of typography and image, not either one alone.

Principles:

- the text is the design, not something pasted on top
- specify exact typographic feeling: size, weight, placement, language, and serif, sans, or handwritten direction
- the image should feel like it was made for this text, not the other way around
- sparse is usually stronger than busy; one line with breathing room often hits harder than a paragraph
- think album cover, film poster, or poetry broadside, not presentation slide

Anti-patterns:

- a beautiful image with floating text unrelated to the composition
- too much text
- commercial or ad-like energy instead of emotional or literary energy

### `borrowed-media-layout` — convincing disguise

What makes this genre work is how convincingly it imitates a real medium.

Principles:

- the borrowed medium should be immediately recognizable: newspaper, karaoke screen, book cover, certificate, album sleeve, movie ticket, and so on
- get the details right: date formats, column layouts, publisher marks, barcodes, issue numbers, age ratings
- the content inside can then be personal, absurd, or touching, creating contrast with the serious shell
- the more real the shell looks, the funnier or more touching the content becomes

Anti-patterns:

- a vaguely newspaper-ish or certificate-ish layout that does not feel like any real medium
- missing metadata details that sell the illusion
- content too generic to justify the borrowed frame

### `proxy-character-scene` — distance creates intimacy

What makes this genre work is the tension between an artificial proxy and a real environment.

Principles:

- the proxy, such as a doll, plush, toy, or figure, should look deliberately artificial
- the environment should feel real, textured, and lit like a photograph
- that contrast, fake being in a real place, creates the emotional register
- the proxy is a stand-in for the user, so its pose, placement, and scale should suggest an emotional state
- lighting and environment do most of the emotional work; the proxy mainly needs to be there

Anti-patterns:

- making the proxy too realistic
- making the environment too artificial
- centering the proxy without giving the environment enough presence

## Text Inside Images

Image generation may include text, but only when it materially improves the gift.

If text is included, specify:

- the exact wording
- the language, which should match the user's dominant interaction language with the skill
- the placement
- the approximate size
- the font feel or typographic direction

Text must feel naturally integrated with the image content rather than pasted on top.

Avoid layouts that are likely to produce broken text structure, especially for Chinese.

Keep on-image text as short as possible. Long paragraphs or dense Chinese copy are high risk and should usually be avoided in favor of a shorter line plus stronger visual composition.

When in doubt, prefer less text and stronger image composition over a text-heavy frame.

## Aspect Ratio

Default to a mobile-friendly `9:16` aspect ratio for image gifts unless another ratio clearly serves the composition better.

Use a different ratio only when the return depends on it, such as a poster-like vertical crop versus a wide cinematic frame.

Genre-specific override:

- `meme-sticker` often works better in `1:1` or `3:4` because the joke needs to read quickly and the subject is usually a compact reaction image rather than a tall scene

## High-Level Rules

- Treat image output as an alternate rendering path, not as a replacement for synthesis or editorial judgment.
- Keep the same anchor-plus-return standard as other formats.
- Prefer image when one frame can carry the full gift.
- Keep the runtime bridge provider-agnostic even though the current dispatched paths are `gemini-direct` and `openrouter`.
- If the runtime cannot finish image generation, return `fallback_h5` rather than blocking the gift.

# Genre: meme-sticker

## Status

Reference-only

## Fit

Use this when the return wants:

- a punchy reaction image
- a sticker-like emotional punchline
- short overlaid text with strong attitude
- humor, teasing, self-mockery, sarcasm, or playful complaint
- a clear contrast between surface behavior and inner feeling

Use this genre when the image should land fast and be funny on first glance rather than requiring slow reading or atmosphere-building.

## Emotional Register

This genre works best when the return is:

- mischievous
- exaggerated
- lightly dramatic
- relatable to ordinary people without needing private lore to decode it

Prefer broad-readable humor over niche cleverness. The user should get the joke quickly, even if the emotional subtext is personal.

## Aspect Ratio

Unlike the default image path, meme-sticker often benefits from shorter frames.

Prefer:

- `1:1` for reaction-image, sticker, and caption-first compositions
- `3:4` for character-with-prop, object gag, or small-scene meme layouts

Use `9:16` only when the joke specifically depends on vertical staging, stacked text beats, or a phone-screen-like composition.

## Subject Strategy

- favor animals, simplified characters, toys, plush-like creatures, objects, or invented non-human mascots over realistic people
- avoid celebrity likenesses, real public figures, or recognizable copyrighted characters
- use one central subject and one emotional action
- let props do narrative work: IV drip, flames, smoke, coffee, trophy, tiny desk, cracked heart, warning sign, hospital bed, etc.
- allow some exaggeration; meme images do not need to be subtle

Small animals, object-characters, and toy-like figures often make the return funnier and less aggressive than a realistic human scene.

## Text Strategy

- keep text short
- make the wording feel native to the user's main interaction language with Hermes
- use text as a punchline, label, speech bubble, or deadpan annotation rather than a paragraph
- specify placement deliberately because text position often carries the joke
- make the font feel match the image: blunt meme caption, hand-drawn label, awkward deadpan subtitle, sticker bubble, etc.

Good text use:

- one short headline
- one speech bubble
- one label on a prop
- one contrast pair such as "outside me / inside me"

Avoid:

- long explanation
- dense Chinese text blocks
- text that repeats what the image already says
- elegant typography that kills the joke

## Prompt Strategy

- describe the character, prop, and emotional contradiction concretely
- state the exact type of humor: teasing, ironic, dramatic, burnt-out, fake-motivational, quietly unhinged, etc.
- if there is contrast, name both sides explicitly
- specify whether the frame should feel cheap, cursed, cute, deadpan, overdramatic, or absurdly sincere
- mention practical meme effects when useful: flames, blast glow, motion blur, hospital drip, giant sweat drop, low-budget photo edit energy
- keep the composition easy to read at thumbnail size

The best meme-sticker prompts usually describe one funny scene very clearly instead of piling on many ideas.

Also follow the per-genre aesthetic guide in `{baseDir}/references/image-integration.md`.

## AI Generation Control

Use this section as practical steering guidance for image models.

These words and structures are references and examples, not a rigid whitelist or blacklist. The goal is to improve model behavior without collapsing the genre into a fixed prompt formula.

### Style Tiers

Meme stickers can operate in different style tiers. Choose the tier that best matches the concept rather than defaulting to one visual language every time.

`Tier 1: chaotic / unhinged`

- doodle energy
- sketchy lines
- flat color
- meme reaction image logic
- derp face or blank-stare comedy
- roughness, motion blur, low-budget edit energy
- exaggerated facial expression

`Tier 2: minimal healing`

- chiikawa-like smallness
- minimal line art
- round shapes
- dot eyes, tiny mouth
- soft pastel flat colors
- thick clean outlines
- muted or nearly empty background

`Tier 3: absurd realistic cute`

- photorealistic fur or object texture
- cute creature in human-coded context
- surreal mismatch between subject and situation
- cinematic absurdity, not cinematic beauty

### Anti-AI Quality Rules

Read `Realism & Human Touch` in `image-integration.md`.

For memes, the AI problem is over-polish rather than under-beauty. Keep it simple and punchy — one subject, one joke, quick read. The humor matters more than the rendering.

### Magic Words

These are often useful prompt ingredients for this genre. Use them selectively. Do not stuff them in mechanically.

- doodle
- sketch
- simple line art
- flat color
- meme style
- sticker
- reaction image
- deadpan
- derp face
- blank stare
- exaggerated expression
- white background
- solid color background
- thick black outline
- chiikawa-like
- kanahei-like
- rough lines
- low-budget edit energy

### Poison Words

These words often make meme-sticker outputs worse because they push the model toward polished beauty instead of readable humor. Avoid them unless you have a very specific reason.

- masterpiece
- highly detailed
- cinematic lighting
- hyper-realistic
- beautiful
- stunning
- gorgeous
- dramatic atmosphere
- professional photography
- 4K
- 8K
- HDR

### Text Rules

`chaotic / unhinged memes`

- font: bold sans-serif, blunt system-caption energy
- style: white text with black outline, or high-saturation red/yellow
- position: top or bottom, large, obvious, slightly crude is fine
- avoid decorative or artistic font language

`cute / healing memes`

- font: rounded or lightly handwritten is acceptable
- color: pull from the image palette rather than fighting it
- placement: can live in a speech bubble, held sign, or floating label if the scene supports it

### Composition Rules

- optimize for thumbnail readability in a phone chat list
- keep to 2-3 major elements at most
- preserve generous negative space
- let the main character occupy roughly 40-60% of the frame
- avoid complex backgrounds unless the background itself is the joke
- prefer one character plus one prop plus one short text beat over multi-part visual clutter

### Emotional Contrast Checklist

Before writing the prompt, identify:

- the surface emotion: what appears to be happening
- the real emotion: what is actually being felt
- the gap between them: this is often where the humor lives

If surface emotion and real emotion are the same, the meme usually needs a stronger contradiction or a more interesting frame.

### Prompt Template

Use this as a structure, not a fixed incantation:

0. `Aesthetic anchor` (optional for memes)
   - if a specific meme tradition or visual reference helps, name it. Example: "Shiba Inu meme energy" or "cursed stock photo." Often unnecessary for memes — skip if the humor speaks for itself.
1. `Style tier + visual language`
   - choose one tier and describe the exact drawing or image behavior
2. `Character`
   - species or subject, expression, pose, size in frame, one key prop
3. `Scene`
   - minimal background type, color, and any one necessary support detail
4. `Humor contrast`
   - what makes the image absurd, deadpan, overdramatic, or funny
5. `Text`
   - exact wording, language, font feel, color, placement, and relative size
6. `Exclusions`
   - what visual tendencies to avoid if they would beautify or overcomplicate the joke

Example prompt skeleton:

`[style tier and style descriptors] [main character/subject] [pose/expression/prop] [minimal scene/background] [humor contrast] [exact on-image text treatment if needed] [what to avoid]`

## Return Uses

- teasing with affection
- turning a repeated frustration into a private in-joke
- making a small emotional truth portable and reusable
- giving the user a funny image they might actually want to save or resend
- returning a complaint in a more lovable, survivable form

## Failure Modes

Avoid this genre when:

- the return needs tenderness more than punch
- the user would likely experience the joke as mocking rather than affectionate
- the image needs long explanatory text to make sense
- the concept depends on elegant atmosphere rather than contrast or punchline
- the humor only works if the model generates precise celebrity likenesses or exact reference characters

## Reference Assets

If these files are missing locally, fetch bundle `image-examples/meme-sticker` first via `bash {baseDir}/scripts/fetch-asset-bundle.sh "image-examples/meme-sticker"`.

- `assets/examples/image-examples/meme-sticker/ref-01.png`
  Borrow: simple animal character, deadpan foreground face, absurd background escalation
  Avoid copying: exact rabbit design or medical prop setup one-to-one

- `assets/examples/image-examples/meme-sticker/ref-02.png`
  Borrow: direct emotion amplification with fire, short text, instant readability
  Avoid copying: exact hamster-fire-laptop composition or multilingual text stack

- `assets/examples/image-examples/meme-sticker/ref-03.png`
  Borrow: tired small creature plus speech bubble plus tiny prop for social fatigue humor
  Avoid copying: exact hat/phone/tea arrangement

- `assets/examples/image-examples/meme-sticker/ref-04.png`
  Borrow: exaggerated facial reaction and uncanny visual intensity for disgust/shock
  Avoid copying: exact doll face or beauty-doll styling

- `assets/examples/image-examples/meme-sticker/ref-05.png`
  Borrow: lo-fi cozy setup with one accessorized animal and one object to define mood
  Avoid copying: exact cat-headphones-coffee-bed palette

- `assets/examples/image-examples/meme-sticker/ref-06.png`
  Borrow: weird point-of-view framing and unexpected scale relationship for absurd humor
  Avoid copying: exact microwave-cat-pizza premise

- `assets/examples/image-examples/meme-sticker/ref-07.png`
  Borrow: minimal line-drawn character plus labeled prop for universal exhausted humor
  Avoid copying: exact "Coffee / me" wording or bear drawing

# Tap To Bloom

## Status

V1 reference pattern with a reusable template.

## Template Status

template-backed

## Reference Assets

- template: `../../assets/templates/tap-to-bloom/`
- reference_images: `none yet`

## Fit Scope

Primary:

- joy
- delight
- renewal
- warmth
- reassurance
- being gently seen
- fresh vitality and creative energy

Stretch:

- quiet celebration
- soft repair
- emotional thaw
- light encouragement
- post-heaviness re-greening
- "something in you is alive again" gifts
- scenes where touch, attention, or play should visibly bring life out of language

## Reference Use

This card is a high-quality reference, not a fixed script. the skill may widen the apparent use case, borrow only the growth mechanic, the touch-triggered bounce, the plant language, the color system, or the overall feeling of vitality, remix it with other patterns, and change the surface treatment as long as the deeper emotional logic still fits.

the skill should not assume that every use of this pattern must literally feature flowers on text. The deeper logic is that attention, touch, or play makes latent life visibly emerge.

## Intended Use

Use for:

- happiness
- joy
- relief
- spring-like warmth
- creative energy
- small but vivid celebration
- life returning after dullness or heaviness

This pattern is especially good when the gift should feel like:

- touching language and making it bloom
- waking up vitality that was already there
- letting delight erupt visibly, not just be stated
- turning text into a living surface

## Emotional Fit

Best for:

- happy news
- gentle excitement
- feeling newly alive
- affectionate cheer
- flourishing energy
- playful optimism

Can also work for:

- emotional recovery after a low period
- encouragement without pressure
- "you are growing" gifts
- celebrating small but meaningful signs of life

Usually not ideal for:

- acute grief
- severe anger
- raw heartbreak
- extremely solemn commemorative moments

This pattern should feel vivid and life-giving, not sugary or childish by default.

## Narrative Role Fit

Strongest roles:

- celebrating
- brightening
- encouraging
- witnessing vitality

Sometimes works for:

- gentle comfort that wants to reintroduce life
- showing that a user's words, habits, or hopes contain creative force

Usually not ideal for:

- heavy explanation
- bitter catharsis
- abstract analysis

## Interaction Grammar

Core mechanic:

- touch, hover, tap, or drag wakes the text and causes visible growth

Supporting mechanic:

- letters bounce or pulse
- leaves, vines, petals, or blossoms emerge from touched language
- small particles or pollen-like traces amplify the sense of aliveness
- repeated interaction can spread growth across the text field

The emotional logic is:

- life is not added from nowhere
- it is drawn out by contact
- the user does not just observe joy, they help it appear

## Visual Logic

- dark or calm ground makes the growth feel luminous
- the text remains readable enough to keep the language present
- growth elements should feel animated and spring-like rather than pasted on
- the scene should look beautiful at rest and richer under interaction
- the piece should feel like a living text garden, not a generic decoration layer

Useful surface directions include:

- flower and leaf bursts
- creeping vines
- soft pollen or magic dust
- bilingual poetic text fields
- a small instruction line that clearly teaches the interaction

## Concept Variations (Not Exhaustive)

- a sky scene where touch reveals glowing sunset clouds
  - center object: sky horizon
  - bloom carrier: warm cloud color and light
- an ocean where tapping summons different sea creatures
  - center object: sea surface
  - bloom carrier: fish, jellyfish, coral, and bubbles
- a barren field where taps grow green plants and shoots
  - center object: dry ground
  - bloom carrier: leaves, stems, and grass
- a grassy scene where interaction causes rabbits or other small creatures to appear
  - center object: meadow
  - bloom carrier: hidden animals and soft motion

## Content Strategy

the skill should adapt:

- source text
- language choice
- whether the text is poem-like, monologue-like, or quote-based
- growth density
- plant vocabulary
- the balance between readability and bloom
- whether the scene should feel more tender, celebratory, or creatively alive

Good source structures:

- joyful lines
- hopeful statements
- user quotes that deserve to be "watered"
- spring, growth, warmth, or possibility themes
- text that becomes more meaningful when physically touched

Avoid:

- overfilling the page until the words disappear entirely
- using the exact sample poem or floral styling as a default
- making the growth so random that it loses emotional focus
- turning a serious moment into decorative forced cheerfulness

## Tone Guidance

Good tones:

- warm
- joyful
- lightly magical
- life-affirming
- creative
- softly celebratory

Can also support:

- reassurance with vitality
- romantic blooming
- playful tenderness

Avoid:

- saccharine cuteness
- empty positivity
- visual chaos that overwhelms the feeling

## Reference Images

- `none yet`

## Customization Knobs

- text content
- font family
- background color
- text color
- plant palette
- plant variety
- growth scale
- interaction radius
- particle density
- maximum bloom density per character

## Implementation Notes

- Keep the growth animated. The emergence should feel elastic, sprouting, or gently explosive rather than static.
- p5.js is a strong fit for this effect because text interaction, per-letter state, particles, and plant growth can all stay lightweight.
- Maintain a readable relationship between text and bloom. The user should still feel that the plants belong to the language.
- If using drag interaction, add cooldown or density limits so the scene stays beautiful rather than muddy.
- On mobile, touch-triggered interaction should be forgiving and obvious.
- If instructions are needed, make them short and clear.

## Good Use Cases

- "Something joyful happened and I want the page itself to come alive."
- "The user feels a little more alive again, and the gift should visibly bloom with them."
- "the user wants to celebrate creativity, tenderness, or spring-like change."
- "A line of text deserves to feel touched into life."

## Risks

- becoming too decorative and losing the emotional center
- burying the text under too much growth
- looking like a random floral sticker effect instead of a living system
- using cheerful blooming in a moment that still needs gravity

## Related References

- `../gift-mechanics.md`
- `../h5-visualizer-workflow.md`
- `../../assets/templates/tap-to-bloom/`

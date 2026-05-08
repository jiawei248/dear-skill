# Wet Letter

## Status

V1 reference pattern with a reusable p5.js template.

## Template Status

template-backed

## Reference Assets

- template: `../../assets/templates/wet-letter/`
- reference_images: `none yet`

## Fit Scope

Primary:

- sadness, disappointment, heartbreak-adjacent hurt, and letter-like emotional aftermath

Stretch:

- any moment where language should feel directly touched, disturbed, or made newly readable through impact rather than pure atmosphere

## Reference Use

This card is a high-quality reference, not a fixed script. the skill may widen the apparent use case, borrow only part of the mechanic or atmosphere, remix it with other patterns, and change the surface treatment as long as the deeper emotional logic still fits. Do not copy the sample text or scene literally.

## Reference Images

- `none yet`

## Intended Use

Use for:

- sadness
- disappointment
- heartbreak-adjacent feelings
- quiet grief
- hurt that wants to be held rather than loudly dramatized

This pattern works when the gift should feel like rain hitting paper, memory, or words directly: not just atmosphere around the text, but text itself being touched, disturbed, and made newly visible through wetness.

## Emotional Fit

Best for:

- soft heartbreak
- disappointment after hope
- post-argument or post-rejection emotional residue
- low, private sadness

Can also work for:

- longing
- reflective distance
- "something important got soaked, but it is still legible" gifts

This pattern should not simply amplify despair. It should turn hurt into a visible texture that the skill witnesses with the user.

## Narrative Role Fit

Strongest roles:

- seeing
- comforting
- gently reframing

Sometimes works for:

- connecting present hurt to a longer pattern

Usually not ideal for:

- playful banter
- practical synthesis
- high-energy celebration

## Interaction Grammar

Core mechanic:

- circular raindrop impacts expand outward and push text apart

Supporting mechanic:

- repeated drops create a field of wet distortions across a letter-like surface
- user taps or presses can add drops manually

This gives the user a light way to "touch" the sadness without turning the gift into a heavy game.

## Visual Logic

- background text behaves like a letter, note, confession, or interior monologue
- each raindrop acts like a temporary transparent lens
- letters are pushed outward in circular dispersal around the drop center
- the screen feels wet, punctured, and intimate

The emotional metaphor is:

- words are still there
- but they have been hit
- and the rain changes how they are read

## Concept Variations (Not Exhaustive)

- a small fish controlled by the user swims through the text and gently pushes it apart
  - center object: watery letter field
  - disturbance carrier: fish movement
- the user's gesture cuts through the text like a wake or brush of water
  - center object: letter surface
  - disturbance carrier: hand-drawn trajectory

## Content Strategy

the skill should adapt:

- background text source
- whether the text is more like a letter, diary fragment, direct quote field, or mixed bilingual layer
- palette
- particle density
- tap interaction allowance
- whether a final steady line appears above or after the rain

Good source text options:

- selected user quotes from the day
- a short user-voiced letter-like note
- a mixed field of user language plus witnessing language
- a reference text only when it genuinely matches the user's mood and taste

Avoid copying the example's exact love-letter framing unless the actual situation really calls for it.

## Tone Guidance

Good tones:

- tender
- warm
- restrained
- low-key intimate

Can include:

- very soft reassurance
- a final line of steadiness after the wet field has done its work

Avoid:

- melodrama
- theatrical romance when the relationship does not support it
- bright cheerfulness
- cleverness that makes the hurt feel aestheticized

## Customization Knobs

- raindrop spawn rate
- target radius range
- particle density
- text size and leading
- page color
- text color
- whether user tap adds drops
- whether the final message sits outside the wet field or inside it

## Implementation Notes

- p5.js is a natural implementation choice for this effect.
- Keep the text readable enough that the user perceives letter-ness, but do not require them to read every line.
- The circular distortions should feel organic rather than perfectly geometric.
- The tap interaction is optional and should remain low-friction.
- On mobile, avoid over-dense particle counts that tank performance.

## Good Use Cases

- "Something hurt, and I want to sit with the after-effect."
- "This disappointment still has language inside it."
- "The user feels let down, but the gift should make them feel accompanied rather than abandoned."

## Risks

- becoming too emo or too romanticized
- making the text field visually muddy
- turning pain into pure aesthetic spectacle
- using too much text so the effect becomes noise

## Related References

- `../gift-mechanics.md`
- `../h5-visualizer-workflow.md`
- `../../assets/templates/wet-letter/`

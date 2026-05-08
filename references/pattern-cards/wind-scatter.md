# Wind Scatter

## Status

V1 reference pattern with a reusable template.

## Template Status

template-backed

## Reference Assets

- template: `../../assets/templates/wind-scatter/`
- reference_images: `../../assets/examples/wind-scatter/`
  Fetch first if missing: `bash {baseDir}/scripts/fetch-asset-bundle.sh "examples/wind-scatter"`

## Fit Scope

Primary:

- quiet release
- lightness
- making peace with the past
- soft reconciliation
- diffusion of life, hope, or feeling
- text or meaning dispersing into the wider world

Stretch:

- renewal after heaviness
- emotional exhale
- seeds of possibility spreading outward
- airy transformation where the original form dissolves without violence
- butterfly-, dandelion-, feather-, or petal-like dispersal when wind-carried motion is the deeper logic

## Reference Use

This card is a high-quality reference, not a fixed script. Hermes may borrow only the outward-scattering motion, the radial text arrangement, the drifting carrier metaphor, the poster-like composition, or the overall feeling of release and propagation, remix it with other patterns, and change copy, composition, assets, and tone freely.

the skill should not assume that every use of this pattern must literally be a dandelion. The deeper logic is that language, feeling, or life detaches from a held center and travels outward with air, lightness, and continuation.

This pattern is near `lift-away`, but it is not the same. `lift-away` is more about setting something down or letting it leave. `wind-scatter` is more about release plus propagation: what leaves also travels, spreads, or carries life forward.

## Intended Use

Use for:

- putting something gently into the air
- making peace with what has happened
- feeling that something can disperse rather than stay condensed
- soft hope after strain
- spreading aliveness, blessing, or memory outward

This pattern is especially good when the gift should feel like:

- a held cluster loosening
- a center releasing its fragments into motion
- language becoming seeds, fluff, butterflies, spores, petals, or breath
- what mattered continuing beyond its original form

## Emotional Fit

Best for:

- quiet reflection
- lightness after heaviness
- reconciliation
- tender release
- hopeful diffusion
- calm aliveness

Can also work for:

- soft farewell
- post-conflict loosening
- gentle spiritual or poetic uplift
- "let this travel further than this moment" gifts
- scattering creativity, joy, or possibility

Usually not ideal for:

- sharp anger
- dense explanation
- highly practical summary
- scenes that need a strong grounded object rather than dispersal

## Narrative Role Fit

Strongest roles:

- releasing
- reconciling
- blessing
- gently transforming

Sometimes works for:

- expanding a user's world
- visualizing the spread of life, influence, or memory
- turning a single line into a field of continuation

Usually not ideal for:

- direct confrontation
- playful banter
- detailed analysis

## Interaction Grammar

Core mechanic:

- a clustered field of text gradually detaches and scatters outward like wind-carried fragments

Supporting mechanic:

- a central anchor drifts subtly rather than staying mechanically fixed
- individual characters or glyphs peel off in small groups
- each piece keeps a visible motion trail or stem-like line
- the user may trigger or intensify the scattering through touch, hover, or drag

The emotional logic is:

- nothing is smashed apart
- it simply stops clinging
- what leaves the center enters air, distance, and continuation

## Visual Logic

- one central cluster or bloom-like mass holds the original text field
- a long stem, ray, or tether can emphasize that the cluster once had a single rooted point
- the background should support airiness, sky, or open-space feeling
- drift lines and motion blur help the eye understand dispersal
- the overall result should feel elegant and breathable, not noisy

Possible carrier forms:

- dandelion seeds
- butterflies
- petals
- feathers
- letters with comet tails
- tiny charms or fragments

## Concept Variations (Not Exhaustive)

- boarding-pass text breaks into paper planes flying toward different destinations
  - center object: boarding pass
  - carrier: paper-plane text fragments
- a letter by an open window gets caught by wind and its words peel away
  - center object: letter sheet
  - carrier: ink fragments and paper flecks
- words written on tree leaves loosen and fall in an autumn gust
  - center object: tree
  - carrier: leaf-borne text
- a flower's petals each hold one worry, and wind removes them one by one
  - center object: flower
  - carrier: petals
- classic dandelion release
  - center object: dandelion head
  - carrier: seed fluff

## Content Strategy

the skill should adapt:

- whether the center cluster is dense or sparse
- whether the scattered units are literal letters, symbolic marks, or tiny motifs
- how quickly the field loosens
- whether the message is bilingual, poetic, or quote-based
- whether the piece feels more reconciliatory, hopeful, or life-spreading

Good source structures:

- a line about letting go
- a phrase that deserves to travel outward
- words that can dissolve into smaller units
- memory or meaning moving from one point into many
- a feeling that wants release without disappearance

Avoid:

- making the motion so fast that the emotional subtlety disappears
- using too much text for the cluster to remain legible
- forcing a single surface motif like dandelion fluff when another carrier form fits better
- turning the page into generic particle spectacle

## Tone Guidance

Good tones:

- airy
- quiet
- tender
- reconciliatory
- softly hopeful
- poetic

Can also support:

- life-affirming spread
- post-storm release
- "this can continue beyond here" companionship

Avoid:

- melodrama
- sentimental overload
- harsh closure
- decorative prettiness without emotional direction

## Reference Images

- `../../assets/examples/wind-scatter/ref-01.png`
  - what to borrow: radial clustering, airy motion trails, and the feeling that letters become wind-borne seeds leaving a living center
  - do not copy literally: the exact blue gradient, exact composition proportions, or the assumption that every version must look like a dandelion against a sky

## Customization Knobs

- source text
- carrier form
- center density
- scatter rate
- drift speed
- trail length
- stem or tether visibility
- background palette
- start delay before dispersal
- whether user interaction accelerates release

## Implementation Notes

- p5.js is a strong fit because the pattern depends on per-character state, radial layout, drifting motion, and lightweight particle-like behavior.
- Keep the center cluster beautiful before scattering begins; the initial held state matters emotionally.
- Preserve some trace of origin, such as a stem, central dot, or radial geometry, so the user can feel what is being released from where.
- The scattered forms should remain readable as intentional carriers, not generic dots.
- If using a non-dandelion metaphor, keep the motion grammar consistent with that carrier.
- On mobile, prioritize clarity over too many tiny moving pieces.

## Good Use Cases

- "A thought can finally loosen and go into the air."
- "The user wants something lighter than a burn or rupture."
- "A gift should suggest that life, hope, or memory can spread beyond the current moment."
- "The scene needs release, but also continuation."

## Risks

- becoming too decorative and losing the emotional center
- looking like a generic particle simulation
- scattering so much that the original meaning disappears too early
- feeling too abstract if no anchor point or guide remains

## Related References

- `../gift-mechanics.md`
- `../h5-visualizer-workflow.md`
- `../../assets/templates/wind-scatter/`
- `../../assets/examples/wind-scatter/`

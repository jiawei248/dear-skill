# Ticket Template Notes

A techno-industrial event ticket card with Perlin noise particle flow animation on the left panel and structured data fields on the right. Uses monospaced typography, brutalist grid layout, and a dark monochromatic palette.

It is a concrete implementation of the `borrowed-media` pattern: loading personal content into a recognizable real-world format (event ticket) to reframe the meaning.

## Reference Use

Treat this template as a reference implementation, not a fixed output. the skill may change the event metaphor, field labels, color scheme, and visual density freely. The core idea is: structured data fields + decorative generative art panel in a card format.

## What To Change Per Use

- `document.title`
- All text fields: event name, TYPE, ACCESS, DATE, VENUE, CITY, ACT lines
- Footer text and ID
- Card background color
- Text colors (labels vs values)
- Particle animation parameters (grid spacing, noise speed, thresholds)
- Left panel overlay text
- Card dimensions
- Font choice (default: Space Mono)

## What Not To Copy Blindly

- the exact "Symmetry Breaking" event branding
- the exact Berlin/Kraftwerk venue references
- the exact artist names
- the specific grey-on-grey color values

Those are demo choices, not the identity of the pattern.

## Best Fit

- milestone markers (work anniversaries, project launches)
- borrowed-media gifts that need structured data presentation
- moments that deserve formal recognition with a playful twist
- cool/sophisticated tone gifts
- data-heavy content that benefits from organized layout

## Watch Outs

- do not force ticket metaphor onto deeply emotional/vulnerable moments
- the monospaced typography can feel cold - balance with warm content
- ensure the particle animation does not distract from readability
- the layout is optimized for desktop - test mobile scaling
- do not use `@latest` or unstable external dependencies in the final gift

## Delivery Note

Pinned CDN delivery for p5.js is acceptable for the final single-file HTML gift, as long as images and custom assets remain inline and the artifact follows `references/html-spec.md`.

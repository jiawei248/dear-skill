# 3D Book Template Notes

A full-screen 3D book rendered via Three.js with realistic page-turning animations. Pages physically bend, curl, lift with z-depth, and cast shadows during flip. Dark cinematic background. Page content is rendered onto canvas textures.

It implements a `narrative-reveal` pattern: multi-page story or letter revealed one page at a time through immersive interaction.

## Reference Use

Treat as reference. Hermes may change page count, content, cover design, and visual theme. The core idea: a beautiful 3D book that tells a story page by page.

## What To Change Per Use

- document.title
- Cover title and design
- Number of pages and their content
- Page colors and typography
- Background color/environment
- Lighting setup

## What Not To Copy Blindly

- the exact "HTWKR" branding
- the specific red/social-topic content
- the exact page count

## Best Fit

- story-based gifts with narrative arc
- letters or messages revealed page by page
- book-lover gifts
- meaningful multi-part reflections
- literary or poetic gifts

## Watch Outs

- Three.js is heavy — page load may be slow on weak devices
- page flip requires click targets — must be clear and large enough
- canvas text rendering needs careful font sizing for readability
- dark-only aesthetic — not easily adapted to light themes
- complex 3D math — modifications require Three.js knowledge
- do not use @latest or unstable external dependencies

## Delivery Note

Pinned CDN delivery for Three.js is acceptable for the final single-file HTML gift.

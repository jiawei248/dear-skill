# Vintage Window Template Notes

A retro OS desktop environment rendered entirely in p5.js canvas with multiple overlapping windows, menu bar, sidebar icons, pixel art viewer, and terminal-style text. Uses a single-color blue-on-white blueprint aesthetic.

It implements a `borrowed-media` pattern: the gift appears as a discovered piece of vintage software with multiple data windows, making personal content feel like a curated digital artifact.

## Reference Use

Treat as reference. the skill may change window titles, content, the pixel art character, terminal commands, sidebar icons, and the single theme color. The core idea: personal content presented as a multi-window retro OS desktop.

## What To Change Per Use

- document.title
- Window titles (GREET.EXE, GLYPH_VIEWER.APP, SKETCH_01.TMP)
- Large display text ("Hello")
- Terminal command lines
- Secondary text block
- Pixel art character (currently hardcoded 'a')
- Sidebar icons
- Menu bar items
- Theme color (currently rgb(20,80,235))
- Background color
- Canvas dimensions

## What Not To Copy Blindly

- the exact "Sys.Portfolio V1.0" branding
- the exact blue color
- the exact pixel art 'a'
- the exact file extensions and names

## Best Fit

- tech-themed gifts or humor
- multi-section content that benefits from windowed layout
- nostalgic digital artifacts
- borrowed-media gifts with structured data
- gifts for tech-savvy recipients

## Watch Outs

- ALL content is canvas-drawn, not HTML DOM - harder to template dynamically
- pixel art character requires manual grid definition per character
- mobile-first ratio (420x850) - may look odd on desktop
- auto-play only, no user interaction
- single theme color means limited palette variety
- do not use @latest or unstable external dependencies

## Delivery Note

Pinned CDN delivery for p5.js is acceptable for the final single-file HTML gift.

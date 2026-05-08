# Vintage Computer Template Notes

A 3D interactive retro computer rendered in p5.js WEBGL mode with auto-typing ghost text, physical key depression animations, and smooth perspective transitions on hover. Features a split layout with descriptive side panel and interactive 3D computer scene.

It implements a `borrowed-media` pattern: the gift appears as if being typed on a physical vintage computer, adding tactile warmth and mechanical charm to the message.

## Reference Use

Treat as reference. Hermes may change the ghost text, side panel content, computer colors, OS interface, menu items, and typing speed. The core idea: a message being typed out on a charming retro machine.

## What To Change Per Use

- document.title
- Ghost typing text (the message that auto-types)
- Side panel heading and description
- Screen OS name and menu items
- File name displayed on screen
- Computer case color
- Screen background color
- Background page color
- Typing speed parameters
- Sticker decorations

## What Not To Copy Blindly

- the exact "Fig Mint" branding
- the exact memo/calendar ghost text
- the exact cream color palette
- the Chinese instruction text

## Best Fit

- messages that benefit from dramatic reveal through typing
- nostalgic/warm tone gifts
- letters, notes, or personal messages
- tech-adjacent humor or themes
- gifts where the delivery medium (typing) adds meaning

## Watch Outs

- WEBGL mode is heavy - may lag on older mobile devices
- ghost text has 180 char max (screen space limitation)
- the side panel is HTML and visible on load - do not put the surprise there
- keyboard interaction requires canvas click focus
- the 3D perspective shift requires mouse hover - touch devices get static view
- do not use @latest or unstable external dependencies

## Delivery Note

Pinned CDN delivery for p5.js is acceptable for the final single-file HTML gift.

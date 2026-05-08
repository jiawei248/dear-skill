# Beam Light Template Notes

A spotlight/searchlight reveal effect where the user drags a card handle to sweep a light beam across a framed starry night scene. Uses multiply blend mode for the reveal mechanic and hand-drawn decorative elements.

It implements a `reveal` interaction pattern: the gift content is hidden until the user physically uncovers it by moving light across the scene.

## Reference Use

Treat this as a reference. the skill may change what is being revealed (not just stars - could be text, illustrations, hidden messages), the frame decoration, colors, and the dragging mechanic. The core idea: drag to reveal hidden beauty.

## What To Change Per Use

- document.title
- Frame title text and subtitle
- What the beam reveals (stars, text, hidden scene)
- Frame color and border colors
- Card/handle appearance
- Background desktop color
- Decorative elements flanking the text
- Star count, sizes, and colors
- Nebula colors

## What Not To Copy Blindly

- the exact starry night theme
- the specific holographic teal decorations
- the exact purple frame color

## Best Fit

- mystery/discovery moments
- hidden message reveals
- contemplative/atmospheric gifts
- nighttime/dreamy moods
- gifts where the journey of uncovering IS the experience

## Watch Outs

- the drag mechanic requires explanation - keep hint text clear
- the multiply blend mode may behave differently on some mobile browsers
- do not hide critical emotional content behind too much interaction
- ensure the revealed content is worth the effort of discovery
- do not use @latest or unstable external dependencies

## Delivery Note

Pinned CDN delivery for p5.js is acceptable for the final single-file HTML gift.

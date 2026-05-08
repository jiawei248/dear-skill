# Fireworks Template Notes

An interactive sparkler/fireworks effect where two sparkler sticks are lit by moving a flame cursor to their tips. Once ignited, characters and numbers burst out as glowing particles with physics simulation.

It implements an `interactive-object` pattern: the user physically ignites sparklers by moving their flame to the tips, creating a tactile celebration moment.

## Reference Use

Treat as reference. the skill may change the spark characters (could spell words or emoji), colors, number of sparklers, burn speed, and overall scene. The core idea: ignite something and watch it burst with character-particles.

## What To Change Per Use

- document.title
- Spark characters (CHARS constant - could be letters spelling a message)
- Instruction text
- Number of sparklers and positions
- Sparkler colors and burn speed
- Particle color palette
- Background color
- Particle physics (gravity, decay)
- Ignition radius

## What Not To Copy Blindly

- the exact number/letter character set
- the exact two-sparkler layout
- the exact red stick color

## Best Fit

- celebrations and milestones
- New Year / birthday / achievement moments
- joyful high-energy gifts
- interactive delight
- moments that deserve fireworks

## Watch Outs

- requires mouse/touch movement - instruction must be clear
- the ignition mechanic needs proximity - may confuse on first try
- particle-heavy - may slow on low-end devices
- dark background only - cannot adapt to light themes
- characters as sparks are tiny and fast - do not rely on them for readable content
- do not use @latest or unstable external dependencies

## Delivery Note

Pinned CDN delivery for p5.js is acceptable for the final single-file HTML gift.

# H5 Interaction Design

Read this when the chosen format is H5 and the concept involves user interaction (tap, swipe, reveal, unlock, etc.). Skip for static or auto-play H5 gifts.

## Core Principle

In an interactive H5 gift, animation IS the emotion. The user's tap is a commitment — the response must reward that commitment with proportional delight. A tap that only changes a CSS class feels like clicking a broken button. A tap that triggers a cascade of motion, light, and surprise feels like magic.

## Emotion Escalation

Interactive gifts with sequential steps (unlock achievements, open envelopes, reveal cards) must build emotional intensity through escalating animation:

### Level 1: Early steps (1-3)
- subtle, satisfying micro-animations
- gentle transitions: fade-in, slight scale bounce, color shift
- small particle burst (4-8 particles)
- brief haptic-like visual pulse
- sound: soft click or chime if audio is present

### Level 2: Middle steps (4-6)
- more pronounced animations
- larger scale bounce, slight overshoot
- more particles (12-20), varied sizes
- glow or shimmer effects on unlocked elements
- maybe a brief screen shake or ripple
- previous unlocked items can react slightly (sympathetic animation)

### Level 3: Climax / Hidden reveal (final)
- MAXIMUM celebration
- full-screen effect: confetti rain, fireworks burst, or radial light explosion
- card/element should dramatically enter: bounce, shake, grow from center, or slam down
- screen flash or pulse
- all previous elements react (glow brighter, bounce once)
- text reveal with typewriter or fade-word-by-word effect
- hold the peak for 1-2 seconds before settling
- if there is a final message, delay it 0.5-1s after the climax so the user has a beat to absorb

## State Transition Design

Every interactive state change needs three phases:

1. **Exit old state** (0.1-0.2s): the locked/hidden element visually breaks, dissolves, or releases — the lock icon could shatter, fade with a puff, or fly away
2. **Transition** (0.2-0.4s): the moment of transformation — scale bounce, color bloom, glow ignition
3. **Enter new state** (0.3-0.5s): the unlocked element settles into its final form with a gentle overshoot

Do NOT skip the exit phase. A lock that simply disappears feels like a rendering glitch. A lock that shatters, dissolves, or pops feels like something happened.

## Specific Patterns

### Unlock / Reveal
- lock icon: shatter into 4-6 fragments that fly outward and fade
- card border: flash bright then settle to unlock color
- icon: scale 0→1.3→1 with slight rotation wobble
- badge: slide in from right with bounce

### Progress Bar
- fill should animate with momentum (ease-out, slight overshoot)
- color should intensify as progress increases
- at 100%: pulse glow effect, then settle

### Hidden / Secret Reveal
- initial reveal: dramatic entrance (grow from 0, bounce, shake 2-3 times)
- background: flash or dim-then-brighten
- confetti / fireworks: 40-80 particles, multiple colors, varied sizes, staggered timing
- the element itself should feel heavier/more important than the others (bigger card, thicker border, different background)
- text content should reveal progressively, not all at once

### Final Message / Emotional Landing
- delay 0.5-1s after the last interaction
- fade in word-by-word or line-by-line (not all at once)
- highlighted words should have their own entrance (scale pulse, color bloom)
- the final message area should feel like a separate emotional space (background shift, increased padding, visual separation)

## Anti-Patterns

- Tap does nothing visible for >0.1s → feels broken
- All steps have identical animation → feels robotic
- Climax has same energy as step 1 → anticlimactic
- Text appears all at once → no pacing, no build
- No transition between states → feels like a slideshow, not an experience
- Particles without variety (same size, same speed, same direction) → feels cheap
- Animation duration >1s per step → feels slow and tedious

## Visual Fidelity Rule

When the concept uses a real-world metaphor (tree, ocean, building, garden, sky), the H5 must make that metaphor visually convincing — not just symbolically present.

A single CSS vertical line does NOT look like a tree. A circle with an emoji does NOT look like a fruit. A gradient background does NOT look like an ocean.

If CSS alone cannot make the metaphor visually convincing, you must either:
1. Generate a background image that establishes the visual metaphor (see stage3-visual-strategy.md Background Asset Strategy)
2. Use detailed SVG illustrations inline
3. Simplify the concept to one that CSS CAN render convincingly (e.g. a data dashboard, a terminal screen, a document)

Do not ship an H5 where the concept promises a "tree" but the user sees a vertical line with circles attached.

### Layout Must Match Metaphor Physics

If the metaphor has physical direction (trees grow up, water flows down, timelines go left-to-right), the H5 layout must respect that direction:
- Trees: roots at BOTTOM, crown at TOP, growth animates upward
- Water: flows downward
- Growth: bottom to top
- Timeline: left to right or top to bottom
- Stack or pile: bottom-up accumulation

Getting the direction wrong breaks the metaphor immediately.

## Related References

- Design philosophy and mobile patterns are now included in this file (see sections below)

## Template Reference Map

Before writing H5 code, find the closest template in `{baseDir}/assets/templates/` and READ its full index.html:

All templates must be available locally at `{baseDir}/assets/templates/<name>/index.html`. They are text/code assets and should be installed with the skill rather than fetched remotely at runtime.

| Emotional register | Template | Key technique to study |
|---|---|---|
| Growth / blooming | tap-to-bloom | p5.js Plant class, trigger radius, per-character state |
| Dispersal / release | wind-scatter | Character physics, ring formation, fly-away velocity |
| Flow / continuity | text-river | Particle stream, canvas text rendering, flow direction |
| Melancholy / rain | rainy-night | Rain particle system, fog layers, ambient motion |
| Destruction / reveal | burn-reveal | Burn edge simulation, reveal mask, ember particles |
| Vulnerability | tear-stained-paper | Paper texture, water stain spread, ink bleed |
| Wistfulness | wet-letter | Water droplet physics, ink dissolution |
| Lightness / joy | o-balloons | Floating physics, string simulation |
| Ceremony / drag | drag-straighten | Drag interaction, crumple/smooth physics |
| Celebration / spark | fireworks | Proximity ignition, character-particle burst, flame cursor, burn physics |
| Discovery / reveal | beam-light | Drag-to-spotlight, multiply blend mode reveal, lerp smoothing on drag |
| Poetic / atmospheric | cloud-text-rain | Text-as-rain transformation, ripple physics, depth-layered ground text |
| Nostalgia / message | vintage-computer | WEBGL 3D rendering, ghost-typing animation, physical key depression, perspective lerp |
| Cool / formal | ticket | Perlin noise dot-grid, monospaced typography hierarchy, HTML+canvas split layout |
| Tech / multi-section | vintage-window | Single-color canvas OS, pixel art grid, multi-window composition, dithered textures |
| Exploration / curation | scroll | Mobile app-style vertical scroll, horizontal card carousel, polka-dot patterns, warm retro-modern |
| Luxury / editorial | multi-cards | Side-by-side tall cards, serif typography, perforated ticket edges, SVG cutout art, 1920s postal |
| Narrative / literary | 3d-book | Three.js 3D book, realistic page-curl physics, canvas page textures, immersive page-turning |
| Planning / review | notebook-planner | Two-page planner spread, schedule timeline, checklist, journal, metal binder rings, month tab flip |
| Bold / streetwear | obj-player | p5.js brutalist card, bold color-blocked grid, Anton typography, WebGL 3D wireframe hover interaction |
| Data / hacker | dashboard-receipt | Receipt-strip layout, zigzag torn edges, monospace data tables, dot-fill bars, SVG waveform, heatmap |
| Nostalgia / intimate | diary-scrapbook | Open diary, scrapbook collage, Polaroid frames, push-pins, Caveat handwriting, steel blue pages |
| Music / dedication | music-player | p5.js 3D vinyl album cover with tilt, minimal player UI, tilted playlist panel, dark audiophile aesthetic |
| Being-seen / profile | dossier-folder | Interactive folder open/close, card pile with z-index stacking, CSS-only stationery (binder clip, cassette, floppy disk), kraft paper textures, polaroid-bordered photos, tri-color star stickers, fold crease at viewport center |

Adapt the technical approach (not content) to your concept. If no template matches the emotional register, pick the one with the closest technical requirements (e.g. particle systems, physics, growth animation) and study that.

Templates are craft references, not creative constraints. Use their techniques to build things they never imagined.

---

## Design Philosophy (Anti-Slop)

Adapted from frontend-design-ultimate for single-page H5 gift contexts using `p5.js`, canvas, and CSS.

## The Problem: AI-Slop H5 Gifts

Generic AI-generated H5 gifts often share these signs:

### Typography Sins

- only one font weight used throughout
- text all the same size, with no hierarchy
- centered everything with no rhythm
- generic system fonts with no personality

### Color Crimes

- pure black background with white text as lazy dark mode
- no color hierarchy
- random accent colors that do not connect to the gift's mood
- no warmth or temperature in the palette

### Layout Laziness

- everything dead-center on screen
- perfectly symmetrical with no tension
- elements stacked vertically with uniform spacing
- no visual surprise or asymmetry

### Motion Mediocrity

- CSS fade-in on everything with the same timing
- no orchestration
- no easing variety
- no relationship between motion and meaning

### Background Boredom

- solid black or solid dark blue
- plain CSS gradient
- no texture, grain, or depth

## The Solution: Intentional H5 Design

### Color As Emotion

Build the palette from the gift's emotional register:

- dark + confident: deep blacks, muted accents, one bright signal color
- warm + healing: cream, amber, sage, soft pink
- poetic + melancholy: desaturated blues, muted purples, rain-grey
- playful + bright: saturated primaries, white space, clean contrast

Use the `60-30-10` rule: `60%` dominant background, `30%` secondary elements, `10%` accent highlights.

**Palette anti-patterns to actively avoid:**
- Gold/bronze + dark blue: reads as "AI-generated luxury" — the single most overused AI palette
- Blue-purple-pink neon gradients: reads as "tech demo" or "cyberpunk cliché"
- Teal + coral/orange on black: reads as "generic SaaS dark mode"
- Uniform pastel: reads as "healing app template" without personality

**Study real palette discipline from the template library:**
- Monochromatic with hierarchy: `ticket` uses ONLY grays but has 5+ distinct luminance stops, each serving a role (background → card → label → value → accent)
- Warm neutral foundation: `vintage-computer` builds on cream (#F0ECE1) with color used ONLY for small functional elements
- Atmospheric depth: `cloud-text-rain` uses 4+ shades of blue, each mapping to a spatial depth layer
- Single-accent discipline: `beam-light` is dark purple throughout, with holographic teal reserved for exactly 2 decorative elements

### Typography As Voice

Even when text is rendered on canvas, keep hierarchy:

- one main text: larger and more visible
- supporting text: smaller and lighter
- accent text such as date stamps or labels: tiny and subdued
- use `textSize()` deliberately, not uniformly
- letter spacing matters; loose feels calm, tight feels urgent

### Motion As Narrative

Animation should tell a story rather than merely move:

- stagger entry timing
- match easing to mood
- use delay to create beats
- connect particles to emotional meaning

### Background As Atmosphere

The background is the first thing the viewer feels:

- generated image backgrounds often add richness CSS gradients cannot
- subtle noise or grain removes sterile digital feel
- vignette helps focus attention
- bokeh or soft light circles add depth

## Design Decision Quick Test

Before shipping an H5 gift, ask:

1. Would I screenshot this?
2. Does it feel designed or generated?
3. What is the one element that makes this gift unique?
4. Is the motion orchestrated or random?
5. Does the background have atmosphere or is it just a color?

## Anti-Pattern Detection

| Anti-Pattern | Fix |
|---|---|
| All text same size | Apply clear size hierarchy |
| All text centered with same spacing | Vary position, alignment, and spacing |
| Pure CSS gradient background | Add texture, grain, or generated image |
| Everything fades in at once | Stagger with meaningful delays |
| No color temperature | Choose warm or cool and commit |
| Particles without purpose | Connect particle type to mood |
| Generic system font | Use a more intentional font choice, including a CDN-loaded web font when appropriate |

---

## Mobile Patterns

Adapted from frontend-design-ultimate for single-page H5 gifts viewed on mobile phones.

## Why This Matters

Daily gift H5s are viewed almost exclusively on mobile phones such as Telegram or WeChat in-app browsers. Every design decision must be mobile-first.

## Viewport Setup

Always include:

```html
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
```

## Font Size Rules

- Minimum body text: `13px`
- Main display text: use `clamp()` or `vw` units to scale with screen width
- iOS zooms on input focus if `font-size < 16px`; avoid form elements below that
- Test readability at `375px` width, the narrowest common screen

## Touch Target Sizes

- Minimum `44x44px` for any tappable element
- Audio toggle button: at least `36x36px` with adequate padding
- If the gift has tap interactions, make tap zones generous

## Safe Areas

- Top `44px`: may be covered by the phone status bar or in-app browser header
- Bottom `34px`: may be covered by the iPhone home indicator
- Keep critical content away from edges; use padding of at least `16px` on all sides

## Canvas Sizing

For `p5.js` gifts:

```javascript
function setup() {
  createCanvas(windowWidth, windowHeight);
}

function windowResized() {
  resizeCanvas(windowWidth, windowHeight);
}
```

Always handle `windowResized()`. Phones rotate, and in-app browsers may resize mid-session.

## Text on Canvas

When using `p5.js text()`:

- `textSize` should be relative to canvas width, not hardcoded pixels
- Example: `textSize(width * 0.04)` instead of `textSize(16)`
- This keeps text proportional across screen sizes
- Test on both narrow (`375px`) and wide (`428px`) phone screens

## Aspect Ratio Considerations

Most gift H5s work best at full-screen mobile, approximately `9:16` to `9:19.5`:

- do not design for desktop-width layouts
- do not assume landscape orientation
- vertical scrolling is acceptable, but auto-play gifts should fit one screen

## Performance

Mobile phones have limited GPU and CPU:

- keep particle count under `100` for smooth animation unless there is a strong reason otherwise
- avoid heavy blur filters on large areas
- base64-encoded audio should be under `500KB`
- total HTML file size should stay under `1MB` for fast loading
- test mentally for mid-range phones, not just flagship devices

## Color and Contrast

- phone screens vary widely in brightness and color accuracy
- avoid very low contrast text
- dark mode gifts often look richer on OLED screens
- consider both bright daylight and dark-room viewing

## Common Mobile Failures

| Failure | Fix |
|---|---|
| Text too small to read | Use relative sizing such as `vw` or width-based sizing |
| Tap targets too small | Keep minimum `44x44px` |
| Content behind status bar | Add top padding |
| Canvas does not resize on rotate | Implement `windowResized()` |
| Animation janky on older phones | Reduce particle count |
| Audio does not play | Add a `touchstart` listener for the first interaction |
| File too large, slow to load | Compress audio and limit total size |

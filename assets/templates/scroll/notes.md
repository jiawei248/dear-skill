# Scroll Template Notes

A mobile app-style vertical scrolling page with horizontally scrollable destination/item cards. Warm peach/cream palette with blue, pink, and yellow accents. Polka-dot patterns and offset shadow cards give it a playful retro-modern feel.

It implements an `extension` pattern: curated items laid out as browsable cards, inviting exploration and discovery.

## Reference Use

Treat as reference. Hermes may change the cards to books, songs, places, ideas, or any curated collection. The core idea: a warm, app-like browsing experience for a list of recommendations or discoveries.

## What To Change Per Use

- document.title
- Header text and greeting
- Card content (images, titles, descriptions)
- Background and accent colors
- Tab labels (Home/Explore/Profile → custom categories)
- Search placeholder text

## What Not To Copy Blindly

- the exact travel/wanderlust theme
- the specific peach color palette
- the bottom tab bar (may not suit all gift types)

## Best Fit

- curated recommendation gifts (books, songs, places, films)
- "things I think you'd love" lists
- exploration/discovery themed gifts
- travel planning or wish-list gifts

## Watch Outs

- horizontal scroll cards need swipe hints on mobile
- many cards may slow rendering — keep to 6-8 max
- Space Mono font is monospace — may not suit all tones
- polka-dot pattern is strong — dial down for quieter moods
- do not use @latest or unstable external dependencies

## Delivery Note

Single HTML file. Google Fonts CDN is acceptable.

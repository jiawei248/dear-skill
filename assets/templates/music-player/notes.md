# Music Player Template Notes

A dark ambient 3D music player interface rendered with p5.js. Left side shows a vinyl record album cover (dark sleeve with colored spine, abstract art, exposed vinyl with label) that tilts/rotates in 3D following cursor with spring-back animation. Below is a minimal player UI with progress bar and playback controls. Right side is a tilted "UP NEXT" playlist panel with track listing.

It implements a new `music-dedication` pattern: a gift built around songs and music, presented as a premium listening experience.

## Reference Use

Treat as reference. Hermes may change the album art, track list, colors, and player style. The core idea: a beautiful music player interface presenting a curated playlist or song dedication.

## What To Change Per Use

- document.title
- Album title and artist name
- Album art colors and design
- Track list (titles, durations)
- Progress bar position
- Background and accent colors
- Vinyl label color/design

## What Not To Copy Blindly

- the exact album art colors
- the specific track titles
- the exact "UP NEXT" label

## Best Fit

- "this song reminds me of you" dedications
- curated playlist gifts
- concert/music event themed gifts
- vinyl/audiophile gifts
- mixtape compilations
- music-memory gifts ("songs from our year")

## Watch Outs

- WebGL 3D tilt requires GPU — test on mobile
- no actual audio playback — purely visual. Consider pairing with a real playlist link
- dark background only — not adaptable to light themes
- p5.js canvas is fixed-size — needs responsive scaling logic
- playlist panel tilt may overlap on narrow screens
- do not use @latest or unstable external dependencies

## Delivery Note

Pinned CDN delivery for p5.js is acceptable for the final single-file HTML gift.

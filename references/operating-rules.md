# Operating Rules — Extended

For core operating rules, see the summary in SKILL.md. This file contains extended rules that are too detailed for the main entry point.

## Series Tracking

Some creative seeds are naturally serializable (travel frog postcards, Proust questions, pocket tool collection). When a gift belongs to a potential series, add a `series_tag` field to `recent_gifts` and ensure the `summary` clearly describes what was specifically sent. Before continuing a series, scan entries with the same `series_tag` to avoid repetition. The 30-entry `recent_gifts` window is sufficient for most series.

## Image References From User

When the user shares an image with positive intent (praising its style, using it as a taste reference, etc.), save it to `./user-references/` and record it in the taste profile's `aesthetic_profile.visual.design_references`.

### Audio in H5 Gifts

Most emotion or atmosphere-driven H5 gifts benefit from background music. Treat audio as a default enhancement for these gifts, not an optional extra.

#### When to add audio (default yes):
- atmospheric, dreamy, poetic, or emotional gifts
- gifts with slow reveal or contemplative pacing
- gifts themed around music, seasons, or memories
- any gift where the emotional tone is the primary return

#### When NOT to add audio:
- meme/funny/ironic gifts where music would undercut the humor
- practical/utility gifts (KPI, checklist, guide)
- fast-interaction gifts (quick tap/swipe games)
- any gift where silence is deliberately part of the effect

#### How to add:

**Step 1: Choose audio.**

Try `{baseDir}/scripts/fetch-music.sh` first to find a scene-matching track:
```
bash {baseDir}/scripts/fetch-music.sh "warm piano calm" ./temp-audio.mp3 30
```
If it returns a path, use that file. If it returns empty (no Freesound token or no results), fall back to a preset from `{baseDir}/assets/audio/`. If the preset bundle is missing locally, fetch it first via `{baseDir}/scripts/fetch-asset-bundle.sh "audio"`.

**Step 2: Fallback presets** (always available, no API needed):
- `warm-piano.mp3` → healing, nostalgic, tender
- `dreamy-ambient.mp3` → dreamy, poetic, surreal
- `playful-cute.mp3` → cute, bright, cheerful
- `night-jazz.mp3` → nighttime, urban, reflective
- `vocal-lofi.mp3` → lo-fi with vocal, cozy
- `rain-melancholy.mp3` → sad, quiet, rainy

**Step 3: Embed in HTML.**

Base64-encode the mp3 and add:
```html
<audio id="bgm" loop autoplay>
  <source src="data:audio/mp3;base64,..." type="audio/mpeg">
</audio>
```

Add touch-to-play for mobile (autoplay is blocked until first user gesture):
```javascript
document.body.addEventListener('touchstart', () => {
  document.getElementById('bgm').play();
}, { once: true });
```

Add a small mute/unmute button (🔇/🔊) in a corner.

Keep audio files under 500KB to avoid bloating the HTML.

#### Audio Selection Priority

1. FIRST: try Freesound search with specific genre terms (e.g. "piano loop", "ambient pad gentle", "acoustic guitar calm") — avoid generic mood words like "calm warm" which match anything
2. Check the result against the filename sanity filter (fetch-music.sh does this automatically)
3. If sanity check passes → use it
4. If sanity check fails or no results after progressive simplification → fallback to preset audio from `{baseDir}/assets/audio/` (fetch bundle `audio` first if the presets are missing locally)

Do NOT skip Freesound and default to preset out of caution. The sanity check exists to catch bad results, not to justify avoiding the search entirely. Presets are the safety net, not the first choice.

#### Audio Quality Check

Freesound search results are not always accurate. The filename sanity check in fetch-music.sh automatically rejects filenames containing alert, bell, notification, alarm, siren, horn, click, beep, ring, train, or whistle.

Additional manual checks before embedding:
1. Verify the file duration is reasonable for a loop (5-30 seconds)
2. Prefer specific genre terms in search queries rather than generic mood words
3. When the sanity check has already passed, trust the result — do not second-guess it into a preset fallback

#### Deferred Freesound Setup

If the agent wants to search for scene-specific music but no Freesound token is configured:
- ask the user once: "想让礼物有背景音乐吗？需要花1分钟注册一个免费的音乐搜索 token~"
- guide them to https://freesound.org/apiv2/apply/
- save token to setup-state under `tools.freesound.api_key`
- if user declines, use preset audio and do not ask again for at least 10 gifts
- do NOT avoid music H5 just because the token is missing - presets are always available

#### Audio Unavailable Handling

When a gift was clearly designed with music in mind, do not silently collapse that intent without leaving a trace in behavior or delivery.

Fallback order:
1. Try scene-specific music via Freesound when configured
2. If Freesound is unavailable or unsuitable, fall back to a local preset from `{baseDir}/assets/audio/` (fetch bundle `audio` first if needed)
3. If neither path is available, continue without music rather than blocking the gift, but note briefly in delivery that background music was intended and could not be included in this run

Do not normalize permanent no-music behavior from a missing token alone. If multiple gifts in a row wanted scene-specific music but could only use presets or silence because Freesound is not configured, the Deferred Freesound Setup mechanism should eventually trigger again according to its cooldown rules instead of being silently skipped forever.
- Do not ask the user to choose a gift style during setup. Gift style should be inferred later from `soul.md`, user interaction patterns, memory, and the actual day.
- Final H5 gifts must follow the self-contained output rules in `{baseDir}/references/html-spec.md`.
- Treat pattern cards and templates as references, not fixed scripts. Borrow their logic, mechanics, pacing, or surface treatment as needed, but keep adapting them to the actual user, day, and relationship context.
- A usable pattern does not need to have a reusable template. Reference-only pattern cards and example images are valid inputs when they provide enough expressive guidance.
- Prefer reading a pattern card's own lightweight metadata when present, especially `Status`, `Template Status`, `Reference Assets`, and `Fit Scope`.
- Do not assume the current pattern library is exhaustive. If none of the existing cards fit well enough, invent a new form or hybrid move that better matches the relationship moment.
- The templates in `{baseDir}/assets/templates/` represent the minimum visual quality bar. Final gifts should be at least as polished as these templates. If the planned output would look significantly simpler, rougher, or more generic than the templates, reconsider the approach before writing HTML.
- Templates define a mechanical reference and quality floor, not a visual composition to reproduce. Every gift must have its own visual metaphor derived from the actual content. `Reskinned template` is not an acceptable outcome.
- When `user_portrait.available` is true, treat the user's appearance description as a persistent creative asset. Use it selectively in gifts where the user's presence adds emotional value. Do not overuse it.


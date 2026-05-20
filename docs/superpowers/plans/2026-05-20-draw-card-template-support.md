# Draw Card Template Support Plan

**Goal:** Add `draw-card` as a ready rich template alongside `paper-house`, `bouquet`, `empty-boxes`, and `folder`, with English production docs, a runtime builder, a GitHub Release asset bundle contract, registry copy, and tests that lock the integration contract.

**Template principle:** the card machine controls the interaction. The experience should draw one meaningful card around a concrete lyric, color, joke, concert, or phrase; final gift copy follows the user's habitual language with the recipient.

## Phase 1 — Template Registry and Documentation

- [x] Create `assets/templates/draw-card/`.
- [x] Add `template.json` with slot schema, activation disclosure, asset bundle metadata, and build contract.
- [x] Add English `README.md`, `SPEC.md`, and `RELEASE.md`.
- [x] Add preview assets for template discovery.
- [x] Document the required production rules:
  - every draw-card gift needs one card thesis
  - fandom language stays playful and respectful
  - lyrics must be short and intentional
  - photos must survive pixelation and card overlays
  - stickers should support the card style, not scatter randomly
  - final gift text uses the user's language, not English by default

## Phase 2 — Runtime Builder and Config Hook

- [x] Copy the canonical `tmp.html` into `template-source/retro-gacha-card.html`.
- [x] Add `window.DRAW_CARD_GIFT_CONFIG` support.
- [x] Support runtime overrides for copy, lyrics, carousel photos, wish photos, stickers, style chips, card templates, and default form values.
- [x] Implement `template-source/build.py`.
- [x] Ensure the builder writes output separately and does not mutate the canonical HTML.
- [x] Inline locally available assets from the build workdir, the fetched `base/` bundle, or `template-source/`.

## Phase 3 — Asset Bundle and GitHub Release

- [x] Stage the bundle from `~/Desktop/draw_card`.
- [x] Include `card_materials/`, `generated_stickers/`, `stickers/`, `轮播图/`, `reference/`, `lyrics.txt`, and `carousel-photos-data.js`.
- [x] Exclude `.git/`, `.DS_Store`, `__pycache__/`, local API material, and source-only scripts that are not part of the runtime bundle.
- [x] Zip as `draw-card-v1.zip`.
- [x] Compute sha256 and update `template.json`.
- [ ] Upload the zip to GitHub Release tag `assets-draw-card-v1` after `gh` auth is refreshed.
- [ ] Confirm the release asset URL and sha256 digest match `template.json`.

## Phase 4 — Tests, Registry Copy, and Verification

- [x] Add schema tests for the template manifest and docs.
- [x] Add builder tests for runtime config injection, workdir-prefixed asset inlining, script inlining, and source immutability.
- [x] Add asset-bundle metadata tests.
- [x] Update `README.md`, `SKILL.md`, and `references/templates.md` so users can discover the template.
- [x] Run focused pytest coverage.
- [x] Build a sample H5 and verify the 3D machine, wish-panel flow, card preview path, and browser console locally.

## Acceptance Criteria

- `assets/templates/draw-card/template.json` is valid JSON and references existing local docs/source/preview files.
- `template-source/build.py` can generate an `index.html` from `filled-slots.json`.
- The generated HTML contains `window.DRAW_CARD_GIFT_CONFIG`.
- The canonical HTML remains unchanged by builds.
- The release bundle is prepared and the manifest hash matches it.
- The docs are English; gift-facing copy rules explicitly require the user's habitual language.
